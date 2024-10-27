import logging
from collections.abc import Callable

from lionfuncs import copy, validate_boolean
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    create_model,
    field_validator,
)
from pydantic.fields import FieldInfo

from lion_core.operative.action_model import (
    ActionRequestModel,
    ActionResponseModel,
)
from lion_core.operative.reason_model import ReasonModel

from .fields import ACTION_REQUESTS_FIELD, ACTION_REQUIRED_FIELD, REASON_FIELD

REASON_ = REASON_FIELD.model_dump()
ACTION_REQUESTS_ = ACTION_REQUESTS_FIELD.to_dict()
ACTION_REQUIRED_ = ACTION_REQUIRED_FIELD.to_dict()


class StepModel(BaseModel):

    reason: ReasonModel | None = Field(**REASON_)
    action_responses: list[ActionRequestModel] = Field(default_factory=list)
    action_requests: list[ActionResponseModel] = Field(**ACTION_REQUESTS_)
    action_required: bool = Field(**ACTION_REQUIRED_)

    @field_validator("action_required", mode="before")
    def validate_action_required(cls, value: JsonValue) -> bool:
        try:
            return validate_boolean(value)
        except Exception as e:
            logging.error(
                f"Failed to convert {value} to a boolean. Error: {e}"
            )
            return False

    @classmethod
    def parse_request_to_response(
        cls,
        request_model: BaseModel,
        data: dict,
        exclude_fields: list | dict | None = None,
        include_fields: list | dict | None = None,
        operative_model: type[BaseModel] | None = None,
        config_dict: ConfigDict | None = None,
        doc: str | None = None,
        validators: dict[str, Callable] | None = None,
        use_base_kwargs: bool = False,
        inherit_base: bool = True,
        field_descriptions: dict[str, str] | None = None,
        frozen: bool = False,
        extra_fields: dict[str, FieldInfo] | None = None,
        use_all_fields: bool = False,
    ) -> BaseModel:
        response_model = cls.as_response_model(
            request_model=request_model,
            exclude_fields=exclude_fields,
            include_fields=include_fields,
            operative_model=operative_model,
            config_dict=config_dict,
            doc=doc,
            validators=validators,
            use_base_kwargs=use_base_kwargs,
            inherit_base=inherit_base,
            field_descriptions=field_descriptions,
            frozen=frozen,
            extra_fields=extra_fields,
            use_all_fields=use_all_fields,
        )
        data = {
            k: v
            for k, v in data.items()
            if k in response_model.model_fields and v is not None
        }
        return response_model.model_validate(data)

    @classmethod
    def as_request_model(
        cls,
        reason: bool = False,
        actions: bool = False,
        exclude_fields: list | dict | None = None,
        include_fields: list | dict | None = None,
        operative_model: type[BaseModel] | None = None,
        config_dict: ConfigDict | None = None,
        doc: str | None = None,
        validators: dict[str, Callable] | None = None,
        use_base_kwargs: bool = False,
        inherit_base: bool = True,
        field_descriptions: dict[str, str] | None = None,
        frozen: bool = False,
        extra_fields: dict[str, FieldInfo] | None = None,
        use_all_fields: bool = False,
    ) -> type[BaseModel]:
        """kwargs, extra fields, dict[str: FieldInfo]"""

        exclude_fields = exclude_fields or []
        exclude_fields.append("action_responses")

        if not reason:
            exclude_fields.append("reason")

        if not actions:
            exclude_fields.extend(["action_requests", "action_required"])

        else:
            validators = validators or {}
            validators["action_required"] = cls.validate_action_required

        fields, class_kwargs, name = _prepare_fields(
            cls,
            exclude_fields=exclude_fields,
            include_fields=include_fields,
            use_all_fields=use_all_fields,
            field_descriptions=field_descriptions,
            operative_model=operative_model,
            use_base_kwargs=use_base_kwargs,
            **(extra_fields or {}),
        )

        model: type[BaseModel] = create_model(
            name + "Request",
            __config__=config_dict,
            __doc__=doc,
            __base__=operative_model if inherit_base else BaseModel,
            __validators__=validators,
            __cls_kwargs__=class_kwargs,
            **fields,
        )
        if frozen:
            model.model_config.frozen = True
        return model

    @classmethod
    def as_response_model(
        cls,
        request_model: BaseModel,
        exclude_fields: list | dict | None = None,
        include_fields: list | dict | None = None,
        operative_model: type[BaseModel] | None = None,
        config_dict: ConfigDict | None = None,
        doc: str | None = None,
        validators: dict[str, Callable] | None = None,
        use_base_kwargs: bool = False,
        inherit_base: bool = True,
        field_descriptions: dict[str, str] | None = None,
        frozen: bool = False,
        extra_fields: dict[str, FieldInfo] | None = None,
        use_all_fields: bool = False,
    ) -> type[BaseModel]:

        exclude_fields = exclude_fields or []

        if ("action_required" not in request_model.model_fields) or (
            not request_model.action_required
        ):
            exclude_fields.extend(
                ["action_responses", "action_required", "action_requests"]
            )
        if "reason" not in request_model.model_fields:
            exclude_fields.extend(["reason"])

        fields, class_kwargs, name = _prepare_fields(
            cls,
            exclude_fields=exclude_fields,
            include_fields=include_fields,
            use_all_fields=use_all_fields,
            field_descriptions=field_descriptions,
            operative_model=operative_model,
            use_base_kwargs=use_base_kwargs,
            **(extra_fields or {}),
        )

        model: type[BaseModel] = create_model(
            name + "Response",
            __config__=config_dict,
            __doc__=doc,
            __base__=operative_model if inherit_base else BaseModel,
            __validators__=validators,
            __cls_kwargs__=class_kwargs,
            **fields,
        )
        if frozen:
            model.model_config.frozen = True
        return model


def _prepare_fields(
    cls,
    exclude_fields: list | dict | None = None,
    include_fields: list | dict | None = None,
    field_descriptions: dict = None,
    use_base_kwargs: bool = False,
    operative_model=None,
    use_all_fields: bool = True,
    **kwargs,
):
    kwargs = copy(kwargs)

    operative_model = operative_model or BaseModel
    if (
        use_all_fields
        and hasattr(operative_model, "all_fields")
        and isinstance(operative_model, BaseModel)
    ):
        kwargs.update(copy(cls.all_fields))
    else:
        kwargs.update(copy(cls.model_fields))

    if exclude_fields:
        exclude_fields = (
            list(exclude_fields.keys())
            if isinstance(exclude_fields, dict)
            else exclude_fields
        )

    if include_fields:
        include_fields = (
            list(include_fields.keys())
            if isinstance(include_fields, dict)
            else include_fields
        )

    if exclude_fields and include_fields:
        for i in include_fields:
            if i in exclude_fields:
                raise ValueError(
                    f"Field {i} is repeated. Operation include "
                    "fields and exclude fields cannot have common elements."
                )

    if exclude_fields:
        for i in exclude_fields:
            kwargs.pop(i, None)

    if include_fields:
        for i in list(kwargs.keys()):
            if i not in include_fields:
                kwargs.pop(i, None)

    fields = {k: (v.annotation, v) for k, v in kwargs.items()}

    if field_descriptions:
        for field_name, description in field_descriptions.items():
            if field_name in fields:
                field_info = fields[field_name]
                if isinstance(field_info, tuple):
                    fields[field_name] = (
                        field_info[0],
                        Field(..., description=description),
                    )
                elif isinstance(field_info, FieldInfo):
                    fields[field_name] = field_info.model_copy(
                        update={"description": description}
                    )

    # Prepare class attributes
    class_kwargs = {}
    if use_base_kwargs:
        class_kwargs.update(
            {
                k: getattr(operative_model, k)
                for k in operative_model.__dict__
                if not k.startswith("__")
            }
        )

    class_kwargs = {k: v for k, v in class_kwargs.items() if k in fields}

    name = None
    if hasattr(operative_model, "class_name"):
        if callable(operative_model.class_name):
            name = operative_model.class_name()
        else:
            name = operative_model.class_name
    else:
        name = operative_model.__name__
        if name == "BaseModel":
            name = cls.__name__

    return fields, class_kwargs, name
