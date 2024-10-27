from __future__ import annotations

import re
from typing import Any

from lionfuncs import to_dict, to_json
from pydantic import BaseModel, Field, field_validator

from lion_core.operative.fields import ARGUMENTS_FIELD, FUNCTION_FIELD

FUNCTION_ = FUNCTION_FIELD.to_dict()
ARGUMENTS_ = ARGUMENTS_FIELD.to_dict()


class ActionRequestModel(BaseModel):

    function: str | None = Field(**FUNCTION_)
    arguments: dict[str, Any] = Field(**ARGUMENTS_)

    @field_validator("arguments", mode="before")
    def validate_arguments(cls, value: Any) -> dict[str, Any]:
        return to_dict(
            value,
            fuzzy_parse=True,
            suppress=True,
            recursive=True,
        )

    @classmethod
    def create(cls, content: str) -> list[ActionRequestModel]:
        try:
            content = _parse_action_request(content)
            if content:
                return [cls.model_validate(i) for i in content]
            return []
        except Exception:
            return []


class ActionResponseModel(BaseModel):

    function: str = ""
    arguments: dict[str, Any] = Field(default_factory=dict)
    output: Any = None


def _parse_action_request(content: str | dict) -> list[dict]:

    json_blocks = []

    if isinstance(content, BaseModel):
        json_blocks = [content.model_dump()]

    elif content and isinstance(content, dict):
        json_blocks = [content]

    elif isinstance(content, str):
        json_blocks = to_json(content, fuzzy_parse=True)
        if not json_blocks:
            pattern2 = r"```python\s*(.*?)\s*```"
            _d = re.findall(pattern2, content, re.DOTALL)
            json_blocks = [to_dict(match, fuzzy_parse=True) for match in _d]
            json_blocks = [i for i in json_blocks if i]

    out = []

    for i in json_blocks:
        j = {}
        if isinstance(i, dict):
            for k, v in i.items():
                k = (
                    k.replace("action_", "")
                    .replace("recipient_", "")
                    .replace("s", "")
                )
                if k in ["name", "function", "recipient"]:
                    j["function"] = v
                elif k in ["parameter", "argument", "arg"]:
                    j["arguments"] = to_dict(
                        v, str_type="json", fuzzy_parse=True, suppress=True
                    )
            if (
                j
                and all(key in j for key in ["function", "arguments"])
                and j["arguments"]
            ):
                out.append(j)

    return out
