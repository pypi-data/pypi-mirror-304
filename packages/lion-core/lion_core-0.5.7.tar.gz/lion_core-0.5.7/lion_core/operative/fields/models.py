from typing import Any

from pydantic import BaseModel, ConfigDict


class FieldModel(BaseModel):
    default: Any = None
    default_factory: Any = None
    title: str | None = None
    description: str | None = None
    examples: list | None = None

    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True, exclude_unset=True)
