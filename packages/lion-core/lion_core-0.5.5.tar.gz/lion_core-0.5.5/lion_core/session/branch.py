import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any, Literal

import pandas as pd
from lion_service import iModel
from lionabc import Real, Traversal
from lionfuncs import (
    LN_UNDEFINED,
    alcall,
    break_down_pydantic_annotation,
    copy,
    is_same_dtype,
    to_df,
    to_dict,
    to_json,
    validate_mapping,
)
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.fields import FieldInfo
from pydantic.types import JsonValue

from lion_core.action import Tool, ToolManager
from lion_core.action.tool_manager import FUNCTOOL
from lion_core.communication import (
    MESSAGE_FIELDS,
    ActionRequest,
    ActionResponse,
    AssistantResponse,
    Instruction,
    Mail,
    Package,
    RoledMessage,
    System,
)
from lion_core.generic import Exchange, Pile, Progression, progression
from lion_core.log_manager import LogManager
from lion_core.operative.action_model import (
    ActionRequestModel,
    ActionResponseModel,
)
from lion_core.operative.step_model import StepModel
from lion_core.session.base import BaseSession
from lion_core.session.msg_handlers import create_instruction, validate_message
from lion_core.sys_utils import SysUtil
from lion_core.types import ID

from .utils import create_message


class Branch(BaseSession, Traversal):
    """
    Represents a branch in the conversation tree with tools and messages.

    This class manages a conversation branch, including messages, tools,
    and communication within the branch.

    Attributes:
        messages (Pile): Collection of messages in the branch.
        tool_manager (ToolManager): Manages tools available in the branch.
        mailbox (Exchange): Handles mail communication for the branch.
        progress (Progression): Tracks the order of messages.
        system (System | None): System message for the branch.
        user (str): Identifier for the user in the conversation.
        imodel (iModel | None): AI model associated with the branch.
        operative_model (type[BaseModel] | None): Model for operation results.
    """

    messages: Pile | None = Field(default_factory=Pile)
    tool_manager: ToolManager | None = Field(default_factory=ToolManager)
    mailbox: Exchange | None = Field(default_factory=Exchange)
    progress: Progression | None = Field(default_factory=progression)
    system: System | None = None
    user: str | None = None
    imodel: iModel | None = None
    operative_model: type[BaseModel] | None = BaseModel
    message_log_manager: LogManager | None = Field(None, exclude=True)
    action_log_manager: LogManager | None = Field(None, exclude=True)

    @model_validator(mode="before")
    def _validate_input(cls, data: dict) -> dict:
        messages = data.pop("messages", None)
        persist_dir = data.pop("persist_dir", None)
        data["message_log_manager"] = data.get(
            "message_log_manager",
            LogManager(
                persist_dir=persist_dir,
                subfolder="messages",
                file_prefix="message_",
            ),
        )
        data["action_log_manager"] = data.get(
            "action_log_manager",
            LogManager(
                persist_dir=persist_dir,
                subfolder="actions",
                file_prefix="action_",
            ),
        )
        data["messages"] = Pile(
            validate_message(messages),
            {RoledMessage},
            strict=False,
        )
        data["progress"] = progression(
            list(data.pop("messages", [])),
        )
        data["tool_manager"] = data.pop(
            "tool_manager",
            ToolManager(),
        )
        data["mailbox"] = data.pop(
            "mailbox",
            Exchange(),
        )
        if "tools" in data:
            tool_manager = data.get("tool_manager", None)
            tool_manager = tool_manager or ToolManager()
            tool_manager.register_tools(data.pop("tools"))
            data["tool_manager"] = tool_manager
        return cls.validate_system(data)

    @model_validator(mode="after")
    def _check_system(self):
        if self.system is None:
            return self
        if self.system not in self.messages:
            self.messages.include(self.system)
            self.progress.insert(0, self.system)
        return self

    def set_system(self, system: System) -> None:
        """
        Sets or updates the system message for the branch.
        Do not use this method. use add_message instead.
        We are considering making this method private.

        Args:
            system (System): The new system message to set.
        """
        if len(self.progress) < 1:
            self.messages.include(system)
            self.system = system
            self.progress[0] = self.system
        else:
            self._change_system(system, delete_previous_system=True)
            self.progress[0] = self.system

    async def a_add_message(self, **kwargs):
        """async add a message, check add_message for details"""
        async with self.messages.async_lock:
            self.add_message(**kwargs)

    def add_message(
        self,
        *,
        sender: ID = None,
        recipient: ID = None,
        instruction: Instruction | JsonValue = None,
        context: Any = None,
        guidance: JsonValue = None,
        plain_content: str = None,
        request_fields: list[str] | dict[str, Any] = None,
        request_model: type[BaseModel] | BaseModel = None,
        system: System | JsonValue = None,
        system_sender: ID = None,
        system_datetime: bool | str = None,
        images: list = None,
        image_detail: Literal["low", "high", "auto"] = None,
        assistant_response: AssistantResponse | JsonValue = None,
        action_request: ActionRequest = None,
        action_response: ActionResponse = None,
        action_request_model: ActionRequestModel = None,
        action_response_model: ActionResponseModel = None,
        delete_previous_system: bool = None,
        metadata: dict[str, Any] = None,
    ):
        """Adds a message to the branch. Only use this to add a message"""

        _msg = create_message(
            sender=sender,
            recipient=recipient,
            instruction=instruction,
            context=context,
            guidance=guidance,
            plain_content=plain_content,
            request_fields=request_fields,
            request_model=request_model,
            system=system,
            system_sender=system_sender,
            system_datetime=system_datetime,
            images=images,
            image_detail=image_detail,
            assistant_response=assistant_response,
            action_request=action_request,
            action_response=action_response,
            action_request_model=action_request_model,
            action_response_model=action_response_model,
        )

        if isinstance(_msg, System):
            _msg.recipient = self.ln_id
            _msg.sender = system_sender or "system"
            self._change_system(_msg, delete_previous_system)

        if isinstance(_msg, Instruction):
            _sender = copy(_msg.sender)
            if not _sender or _sender == "N/A":
                _msg.sender = sender or self.user
            _msg.recipient = recipient or self.ln_id

        if isinstance(_msg, AssistantResponse):
            _sender = copy(_msg.sender)
            if not _sender or _sender == "N/A":
                _msg.sender = sender or self.ln_id
            _msg.recipient = recipient or self.user or "user"

        if isinstance(_msg, ActionRequest):
            _sender = copy(_msg.sender)
            if not SysUtil.is_id(_sender):
                _msg.sender = sender or self.ln_id

            _msg.recipient = copy(_msg.recipient)

            if not SysUtil.is_id(_msg.recipient):
                if _msg.function in self.tool_manager.registry:
                    _msg.recipient = self.tool_manager.registry[
                        _msg.function
                    ].ln_id
                else:
                    _msg.recipient = "N/A"

        if isinstance(_msg, ActionResponse):
            _sender = copy(_msg.sender)
            if not SysUtil.is_id(_sender):
                if _msg.function in self.tool_manager.registry:
                    _msg.sender = self.tool_manager.registry[
                        _msg.function
                    ].ln_id
                else:
                    _msg.sender = "N/A"

            _recipient = copy(_msg.recipient)
            if not SysUtil.is_id(_recipient):
                _msg.recipient = recipient or self.ln_id

        if metadata:
            _msg.metadata.update(metadata, ["extra"])

        if _msg in self.messages:
            self.messages[_msg] = _msg
        else:
            self.messages.include(_msg)

        # we are paranoid about losing any data, thus we keep a
        # log of all messages in addition to the messages themselves
        log = _msg.to_log()
        self.message_log_manager.logs.include(log)

    def clear_messages(self) -> None:
        """Clears all messages from the branch except the system message."""
        self.messages.clear()
        self.progress.clear()
        if self.system:
            self.messages.include(self.system)
            self.progress.insert(0, self.system)

    def _change_system(
        self,
        system: System,
        delete_previous_system: bool = False,
    ) -> None:
        """
        Change the system message.

        Args:
            system: The new system message.
            delete_previous_system: If True, delete the previous system
                message.
        """
        old_system = self.system
        self.system = system
        self.messages.insert(0, self.system)

        if delete_previous_system:
            self.messages.exclude(old_system)

    def send(
        self,
        recipient: ID,
        category: str,
        package: Any,
        request_source: str,
    ) -> None:
        """
        Sends a mail to a recipient.

        Args:
            recipient (str): The recipient's ID.
            category (str): The category of the mail.
            package (Any): The content of the mail.
            request_source (str): The source of the request.
        """
        package = Package(
            category=category,
            package=package,
            request_source=request_source,
        )

        mail = Mail(
            sender=self.ln_id,
            recipient=recipient,
            package=package,
        )
        self.mailbox.include(mail, "out")

    def receive(
        self,
        sender: ID,
        message: bool = False,
        tool: bool = False,
        imodel: bool = False,
    ) -> None:
        """
        Receives mail from a sender.

        Args:
            sender (str): The ID of the sender.
            message (bool): Whether to process message mails.
            tool (bool): Whether to process tool mails.
            imodel (bool): Whether to process imodel mails.

        Raises:
            ValueError: If the sender does not exist or the mail category is
            invalid.
        """
        skipped_requests = progression()
        if not isinstance(sender, str):
            sender = sender.ln_id
        if sender not in self.mailbox.pending_ins.keys():
            raise ValueError(f"No package from {sender}")
        while self.mailbox.pending_ins[sender].size() > 0:
            mail_id = self.mailbox.pending_ins[sender].popleft()
            mail: Mail = self.mailbox.pile_[mail_id]

            if mail.category == "message" and message:
                if not isinstance(mail.package.package, RoledMessage):
                    raise ValueError("Invalid message format")
                new_message = mail.package.package.clone()
                new_message.sender = mail.sender
                new_message.recipient = self.ln_id
                self.messages.include(new_message)
                self.mailbox.pile_.pop(mail_id)

            elif mail.category == "tool" and tool:
                if not isinstance(mail.package.package, Tool):
                    raise ValueError("Invalid tools format")
                self.tool_manager.register_tools(mail.package.package)
                self.mailbox.pile_.pop(mail_id)

            elif mail.category == "imodel" and imodel:
                if not isinstance(mail.package.package, iModel):
                    raise ValueError("Invalid iModel format")
                self.imodel = mail.package.package
                self.mailbox.pile_.pop(mail_id)

            else:
                skipped_requests.append(mail)

        self.mailbox.pending_ins[sender] = skipped_requests

        if self.mailbox.pending_ins[sender].size() == 0:
            self.mailbox.pending_ins.pop(sender)

    def receive_all(self) -> None:
        """Receives mail from all senders."""
        for key in list(self.mailbox.pending_ins.keys()):
            self.receive(key)

    @property
    def last_response(self) -> AssistantResponse | None:
        """
        Retrieves the last assistant response in the branch.

        Returns:
            AssistantResponse | None: The last assistant response, if any.
        """
        for i in reversed(self.progress):
            if isinstance(self.messages[i], AssistantResponse):
                return self.messages[i]

    @property
    def assistant_responses(self) -> Pile:
        """
        Retrieves all assistant responses in the branch.

        Returns:
            Pile: A Pile containing all assistant responses.
        """
        return Pile(
            [
                self.messages[i]
                for i in self.progress
                if isinstance(self.messages[i], AssistantResponse)
            ]
        )

    @property
    def action_requests(self) -> Pile:
        """
        Retrieves all action requests in the branch.

        Returns:
            Pile: A Pile containing all action requests.
        """
        return Pile(
            [
                self.messages[i]
                for i in self.progress
                if isinstance(self.messages[i], ActionRequest)
            ]
        )

    @property
    def action_responses(self) -> Pile:
        """
        Retrieves all action responses in the branch.

        Returns:
            Pile: A Pile containing all action responses.
        """
        return Pile(
            [
                self.messages[i]
                for i in self.progress
                if isinstance(self.messages[i], ActionResponse)
            ]
        )

    @property
    def instructions(self) -> Pile:
        """
        Retrieves all instructions in the branch.

        Returns:
            Pile: A Pile containing all instructions.
        """
        return Pile(
            [
                self.messages[i]
                for i in self.progress
                if isinstance(self.messages[i], Instruction)
            ]
        )

    def has_tools(self) -> bool:
        """
        Checks if the branch has any registered tools.

        Returns:
            bool: True if tools are registered, False otherwise.
        """
        return self.tool_manager.registry != {}

    def register_tools(
        self, tools: FUNCTOOL | list[FUNCTOOL], update: bool = False
    ) -> None:
        """
        Registers new tools to the tool manager.

        Args:
            tools (Any): Tools to be registered.
        """
        self.tool_manager.register_tools(tools=tools, update=update)

    def delete_tools(
        self,
        tools: FUNCTOOL | str | list[FUNCTOOL | str],
        verbose: bool = True,
    ) -> bool:
        """
        Deletes specified tools from the tool manager.

        Args:
            tools (Any): Tools to be deleted.
            verbose (bool): If True, print status messages.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        if not isinstance(tools, list):
            tools = [tools]
        if is_same_dtype(input_=tools, dtype=str):
            for act_ in tools:
                if act_ in self.tool_manager.registry:
                    self.tool_manager.registry.pop(act_)
            if verbose:
                print("tools successfully deleted")
            return True
        elif is_same_dtype(input_=tools, dtype=Tool):
            for act_ in tools:
                if act_.function_name in self.tool_manager.registry:
                    self.tool_manager.registry.pop(act_.function_name)
            if verbose:
                print("tools successfully deleted")
            return True
        if verbose:
            print("tools deletion failed")
        return False

    def to_chat_messages(
        self, progress: Progression | list[str] = None
    ) -> list[dict[str, Any]]:
        """
        Converts messages to a list of chat message dictionaries.

        Args:
            progress (Progression, optional): Specific progression to convert.

        Returns:
            list[dict[str, Any]]: A list of chat message dictionaries.

        Raises:
            ValueError: If the provided progress is invalid.
        """
        if progress == []:
            return []
        if not all(i in self.messages for i in (progress or self.progress)):
            raise ValueError("Invalid progress")
        return [self.messages[i].chat_msg for i in (progress or self.progress)]

    async def invoke_action(
        self,
        action_request_model: ActionRequestModel = None,
        action_request: ActionRequest = None,
        suppress_errors: bool = False,
    ) -> ActionResponseModel:
        try:
            if action_request and action_request_model:
                raise ValueError(
                    "Cannot have both action_request and action_request_model"
                )
            if not action_request and not action_request_model:
                raise ValueError(
                    "Either action_request or action_request_model must "
                    "be provided"
                )

            if not action_request:
                action_request = ActionRequest(
                    function=action_request_model.function,
                    arguments=action_request_model.arguments,
                    sender=self.ln_id,
                )

            if not action_request_model:
                action_request_model = ActionRequestModel(
                    function=action_request.function,
                    arguments=action_request.arguments,
                )

            if action_request not in self.messages:
                await self.a_add_message(action_request=action_request)
            else:
                self.messages[action_request] = action_request

            result, log = await self.tool_manager.invoke(action_request)
            await self.action_log_manager.alog(log)
            action_response_model = ActionResponseModel(
                function=action_request.function,
                arguments=action_request.arguments,
                output=result,
            )
            await self.a_add_message(
                action_request=action_request,
                action_response_model=action_response_model,
                metadata={"log": log.to_dict()},
            )
            return action_response_model
        except Exception as e:
            if suppress_errors:
                logging.warning(f"Failed to invoke action: {e}")
                return None
            raise e

    def get_tool_schema(self, tools: str | Tool | list[Tool | str]) -> dict:
        tools = tools if isinstance(tools, list) else [tools]
        for i in tools:
            if isinstance(i, Tool | Callable) and i not in self.tool_manager:
                self.tool_manager.register_tools(i)
        return self.tool_manager.get_tool_schema(tools)

    async def communicate(
        self,
        instruction: Instruction | JsonValue = None,
        guidance: JsonValue = None,
        context: JsonValue = None,
        sender: ID = None,
        recipient: ID = None,
        progress: Progression | list[ID] = None,
        request_model: type[BaseModel] | BaseModel = None,
        request_fields: dict[str, Any] | list[str] = None,
        imodel: iModel = None,
        images: list = None,
        image_detail: Literal["low", "high", "auto"] = None,
        tools: str | FUNCTOOL | list[FUNCTOOL | str] | bool = None,
        num_parse_retries: int = 0,
        retry_imodel: iModel = None,
        retry_kwargs: dict = {},
        handle_validation: Literal[
            "raise", "return_value", "return_none"
        ] = "return_value",
        skip_validation: bool = False,
        clear_messages: bool = False,
        invoke_action: bool = False,
        **kwargs,
    ):
        imodel = imodel or self.imodel
        retry_imodel = retry_imodel or imodel
        if clear_messages:
            self.clear_messages()

        if num_parse_retries > 5:
            logging.warning(
                f"Are you sure you want to retry {num_parse_retries} "
                "times? lowering retry attempts to 5. Suggestion is under 3"
            )
            num_parse_retries = 5

        ins, res = await self._invoke_imodel(
            instruction=instruction,
            guidance=guidance,
            context=context,
            sender=sender,
            recipient=recipient,
            request_model=request_model,
            progress=progress,
            imodel=imodel,
            images=images,
            image_detail=image_detail,
            tool_schemas=self.get_tool_schema(tools) if tools else None,
            **kwargs,
        )
        await self.a_add_message(instruction=ins)
        await self.a_add_message(assistant_response=res)

        action_request_models = None
        action_response_models = None

        if skip_validation:
            return res.response

        if tools:
            action_request_models = ActionRequestModel.create(res.response)

        if action_request_models and invoke_action:
            action_response_models = await alcall(
                action_request_models,
                self.invoke_action,
                suppress_errors=True,
            )

        if action_request_models and not action_response_models:
            for i in action_request_models:
                await self.a_add_message(
                    action_request_model=i,
                    sender=self,
                    recipient=None,
                )

        parse_success = False

        _d = None
        if request_fields or request_model:
            while parse_success is False and num_parse_retries > 0:
                if request_fields:
                    try:
                        _d = to_json(res.response)
                        _d = validate_mapping(
                            _d,
                            request_fields,
                            handle_unmatched="force",
                            fill_value=LN_UNDEFINED,
                        )
                        _d = {k: v for k, v in _d.items() if v != LN_UNDEFINED}
                    except Exception:
                        pass
                    if _d and isinstance(_d, dict):
                        parse_success = True
                        if res not in self.messages:
                            await self.a_add_message(assistant_response=res)

                elif request_model:
                    _d = to_json(res.response)
                    _d = validate_mapping(
                        _d,
                        break_down_pydantic_annotation(request_model),
                        handle_unmatched="force",
                        fill_value=LN_UNDEFINED,
                    )

                    _d = {k: v for k, v in _d.items() if v != LN_UNDEFINED}
                    if _d and isinstance(_d, dict):
                        try:
                            _d = request_model.model_validate(_d)
                            parse_success = True
                            if res not in self.messages:
                                await self.a_add_message(
                                    assistant_response=res
                                )
                        except Exception as e:
                            logging.warning(
                                "Failed to parse model response into "
                                f"pydantic model: {e}"
                            )

                if parse_success is False:
                    logging.warning(
                        "Failed to parse response into request "
                        f"format, retrying... with {retry_imodel.model}"
                    )
                    _, res = await self._invoke_imodel(
                        instruction="reformat text into specified model",
                        context=res.response,
                        request_model=request_model,
                        request_fields=request_fields,
                        progress=[],
                        imodel=retry_imodel or imodel,
                        **retry_kwargs,
                    )
                    num_parse_retries -= 1

        if request_fields and not isinstance(_d, dict):
            if handle_validation == "raise":
                raise ValueError(
                    "Failed to parse response into request format"
                )
            if handle_validation == "return_none":
                return None
            if handle_validation == "return_value":
                return res.response

        if request_model and not isinstance(_d, BaseModel):
            if handle_validation == "raise":
                raise ValueError(
                    "Failed to parse response into request format"
                )
            if handle_validation == "return_none":
                return None
            if handle_validation == "return_value":
                return res.response

        return _d if _d else res.response

    async def operate(
        self,
        instruction: Instruction | JsonValue = None,
        guidance: JsonValue = None,
        context: JsonValue = None,
        sender: Real = None,
        recipient: Real = None,
        operative_model: BaseModel | type[BaseModel] = None,
        progress: Progression | list[str] = None,
        imodel: iModel = None,
        reason: bool = True,
        actions: bool = True,
        tools: str | FUNCTOOL | list[FUNCTOOL | str] | bool = None,
        images: list = None,
        image_detail: Literal["low", "high", "auto"] = None,
        num_parse_retries: int = 0,
        retry_imodel: iModel = None,
        retry_kwargs: dict = {},
        clear_messages: bool = False,
        skip_validation: bool = False,
        handle_validation: Literal[
            "raise", "return_value", "return_none"
        ] = "return_value",
        invoke_action: bool = True,
        exclude_fields: list | dict = None,
        include_fields: list | dict = None,
        config_dict: ConfigDict = None,
        frozen: bool = False,
        doc: str = None,
        validators: dict = None,
        use_base_kwargs: bool = False,
        inherit_base: bool = True,
        field_descriptions: dict[str, str] = None,
        extra_fields: dict[str, FieldInfo] = None,
        **kwargs,
    ) -> BaseModel | str | dict:
        """
        if skip validation,
        action won't be invoked and response will be returned as is
        """

        if clear_messages:
            self.clear_messages()

        if num_parse_retries > 5:
            logging.warning(
                f"Are you sure you want to retry {num_parse_retries} "
                "times? lowering retry attempts to 5. Suggestion is under 3"
            )
            num_parse_retries = 5

        request_model = await self._operate(
            instruction=instruction,
            guidance=guidance,
            context=context,
            sender=sender,
            recipient=recipient,
            operative_model=operative_model,
            progress=progress,
            imodel=imodel,
            reason=reason,
            actions=actions,
            exclude_fields=exclude_fields,
            include_fields=include_fields,
            config_dict=config_dict,
            doc=doc,
            frozen=frozen,
            validators=validators,
            use_base_kwargs=use_base_kwargs,
            inherit_base=inherit_base,
            field_descriptions=field_descriptions,
            extra_fields=extra_fields,
            tool_schemas=self.get_tool_schema(tools) if tools else None,
            images=images,
            image_detail=image_detail,
            num_parse_retries=num_parse_retries,
            retry_imodel=retry_imodel,
            retry_kwargs=retry_kwargs,
            **kwargs,
        )

        if skip_validation:
            return request_model

        if isinstance(request_model, dict | str):
            if handle_validation == "raise":
                request_: type[BaseModel] = StepModel.as_request_model(
                    reason=reason,
                    actions=actions,
                    operative_model=operative_model,
                )
                raise ValueError(
                    "Operative model validation failed. iModel response"
                    " not parsed into operative model:"
                    f" {request_.__name__}"
                )
            if handle_validation == "return_none":
                return None
            if handle_validation == "return_value":
                return request_model

        dict_ = request_model.model_dump()
        if (
            actions
            and invoke_action
            and hasattr(request_model, "action_required")
            and request_model.action_required
            and hasattr(request_model, "action_requests")
            and request_model.action_requests
        ):
            action_response_models = await alcall(
                request_model.action_requests,
                self.invoke_action,
                suppress_errors=True,
            )
            dict_ = request_model.model_dump()
            action_response_models = [
                to_dict(i) for i in action_response_models if i
            ]
            dict_["action_responses"] = action_response_models

            try:
                return StepModel.parse_request_to_response(
                    request_model=request_model,
                    data=dict_,
                    exclude_fields=exclude_fields,
                    operative_model=operative_model,
                    config_dict=config_dict,
                    doc=doc,
                    frozen=frozen,
                    validators=validators,
                    use_base_kwargs=use_base_kwargs,
                    inherit_base=inherit_base,
                    field_descriptions=field_descriptions,
                    extra_fields=extra_fields,
                )
            except Exception as e:
                logging.warning(
                    f"Failed to parse model response into operative model: {e}"
                )
                request_model = dict_

        elif (
            hasattr(request_model, "action_requests")
            and request_model.action_requests
        ):
            for i in request_model.action_requests:
                act_req = ActionRequest(
                    function=i.function,
                    arguments=i.arguments,
                    sender=self,
                )
                await self.a_add_message(
                    action_request=act_req,
                    sender=act_req.sender,
                    recipient=None,
                )

        try:
            return StepModel.parse_request_to_response(
                request_model=request_model,
                data=dict_,
                exclude_fields=exclude_fields,
                operative_model=operative_model,
                config_dict=config_dict,
                doc=doc,
                frozen=frozen,
                validators=validators,
                use_base_kwargs=use_base_kwargs,
                inherit_base=inherit_base,
                field_descriptions=field_descriptions,
                extra_fields=extra_fields,
            )
        except Exception as e:
            logging.warning(
                f"Failed to parse model response into operative model: {e}"
            )

        return request_model

    async def _invoke_imodel(
        self,
        instruction=None,
        guidance=None,
        context=None,
        sender=None,
        recipient=None,
        request_fields=None,
        request_model: type[BaseModel] = None,
        progress=None,
        imodel: iModel = None,
        tool_schemas=None,
        images: list = None,
        image_detail: Literal["low", "high", "auto"] = None,
        **kwargs,
    ) -> tuple[Instruction, AssistantResponse]:

        ins = create_instruction(
            instruction=instruction,
            guidance=guidance,
            context=context,
            sender=sender or self.user or "user",
            recipient=recipient or self.ln_id,
            request_model=request_model,
            request_fields=request_fields,
            images=images,
            image_detail=image_detail,
        )
        if tool_schemas:
            ins.update_context(tool_schemas=tool_schemas)

        kwargs["messages"] = self.to_chat_messages(progress)
        kwargs["messages"].append(ins.chat_msg)

        imodel = imodel or self.imodel
        api_request = imodel.parse_to_data_model(**kwargs)
        api_response = await imodel.invoke(**api_request)
        res = AssistantResponse(
            assistant_response=api_response,
            sender=self,
            recipient=self.user,
        )
        return ins, res

    async def _operate(
        self,
        instruction=None,
        guidance=None,
        context=None,
        sender=None,
        recipient=None,
        operative_model: type[BaseModel] = None,
        progress=None,
        imodel: iModel = None,
        reason: bool = True,
        actions: bool = True,
        exclude_fields: list | dict | None = None,
        include_fields: list | dict | None = None,
        config_dict: ConfigDict | None = None,
        doc: str | None = None,
        validators: dict = None,
        use_base_kwargs: bool = False,
        inherit_base: bool = True,
        field_descriptions: dict[str, str] | None = None,
        extra_fields: dict[str, FieldInfo] | None = None,
        frozen: bool = False,
        tool_schemas=None,
        images: list = None,
        image_detail: Literal["low", "high", "auto"] = None,
        num_parse_retries: int = 0,
        retry_imodel: iModel = None,
        retry_kwargs: dict = {},
        **kwargs,
    ) -> BaseModel | str | dict:
        imodel = imodel or self.imodel
        retry_imodel = retry_imodel or imodel
        request_model: type[BaseModel] = StepModel.as_request_model(
            reason=reason,
            actions=actions,
            exclude_fields=exclude_fields,
            include_fields=include_fields,
            operative_model=operative_model,
            config_dict=config_dict,
            doc=doc,
            frozen=frozen,
            validators=validators,
            use_base_kwargs=use_base_kwargs,
            inherit_base=inherit_base,
            field_descriptions=field_descriptions,
            extra_fields=extra_fields,
        )

        ins, res = await self._invoke_imodel(
            instruction=instruction,
            guidance=guidance,
            context=context,
            sender=sender,
            recipient=recipient,
            request_model=request_model,
            progress=progress,
            imodel=imodel,
            tool_schemas=tool_schemas,
            images=images,
            image_detail=image_detail,
            **kwargs,
        )

        await self.a_add_message(instruction=ins)
        await self.a_add_message(assistant_response=res)

        def _validate_pydantic(_s, pyd=True):
            d_ = to_json(_s, fuzzy_parse=True)
            d_ = validate_mapping(
                _s,
                request_model.model_fields,
                handle_unmatched="force",
                fuzzy_match=True,
                fill_value=LN_UNDEFINED,
            )
            d_ = {k: v for k, v in d_.items() if v != LN_UNDEFINED}
            if pyd:
                step_request_model = request_model.model_validate(d_)
                return d_, step_request_model
            return d_

        step_request_model = None
        dict_ = {}

        try:
            dict_, step_request_model = _validate_pydantic(res.response, True)

        except Exception:
            while num_parse_retries > 0 and step_request_model is None:

                _, res1 = await self._invoke_imodel(
                    instruction="reformat text into specified model",
                    context=res.response,
                    request_model=request_model,
                    progress=[],
                    imodel=retry_imodel,
                    **retry_kwargs,
                )
                try:
                    dict_, step_request_model = _validate_pydantic(
                        res1.response, True
                    )
                    await self.a_add_message(assistant_response=res1)
                    break

                except Exception:
                    if num_parse_retries == 1:
                        try:
                            dict_ = _validate_pydantic(res1.response, False)
                            break
                        except Exception:
                            dict_ = res.response
                            logging.warning(
                                f"Failed to parse response: {res.response}. "
                                "max retries reached, returning raw response"
                            )
                            break

                    logging.warning(
                        f"Failed to parse response: {res.response}. "
                        f"Retrying with {retry_imodel.model} ..."
                    )
                    step_request_model = None
                    num_parse_retries -= 1

        return step_request_model if step_request_model else dict_

    def dump_logs(self, clear: bool = True, persist_path: str | Path = None):
        self.message_log_manager.dump(clear, persist_path)
        self.action_log_manager.dump(clear, persist_path)

    def to_df(self, *, progress: Progression = None) -> pd.DataFrame:
        if progress:
            _dicts = [self.messages[i].formatted_dict for i in progress]
        else:
            _dicts = [i.formatted_dict for i in self.messages]
        df = to_df(_dicts, columns=MESSAGE_FIELDS)
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="us")
        return df


__all__ = ["Branch"]
# File: lion_core/session/branch.py
