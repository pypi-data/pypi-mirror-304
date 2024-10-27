from typing import Any, Literal

from lionabc import Communicatable
from pydantic import Field, field_validator

from lion_core.communication.utils import validate_sender_recipient
from lion_core.generic import Element
from lion_core.types import LnID


class BaseMail(Element, Communicatable):
    """
    Base class for mail-like communication in the LION system.

    Attributes:
        sender (str): The ID of the sender node.
        recipient (str): The ID of the recipient node.
    """

    sender: LnID | Literal["system", "user", "N/A", "assistant"] = Field(
        default="N/A",
        title="Sender",
        description="The ID of the sender node or a role.",
    )

    recipient: LnID | Literal["system", "user", "N/A", "assistant"] = Field(
        default="N/A",
        title="Recipient",
        description="The ID of the recipient node, or a role",
    )

    @field_validator("sender", "recipient", mode="before")
    @classmethod
    def _validate_sender_recipient(cls, value: Any) -> LnID | str:
        return validate_sender_recipient(value)


# File: lion_core/communication/base.py
