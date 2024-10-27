from lionfuncs import to_num
from pydantic import BaseModel, Field, JsonValue, field_validator

from .fields import CONFIDENCE_SCORE_FIELD

CONFIDENCE_SOCRE_ = CONFIDENCE_SCORE_FIELD.to_dict()


class ReasonModel(BaseModel):

    title: str | None = None
    content: str | None = None
    confidence_score: float | None = Field(**CONFIDENCE_SOCRE_)

    @field_validator("confidence_score", mode="before")
    def validate_confidence_score(cls, value: JsonValue) -> float:
        try:
            return to_num(
                value,
                upper_bound=1,
                lower_bound=0,
                num_type=float,
                precision=3,
            )
        except Exception:
            return -1
