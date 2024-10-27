from .models import FieldModel

_description = (
    "Provide an objective numeric confidence score between 0 and 1 (with 3 "
    "decimal places) indicating how likely you successfully achieved the task"
    " according to user expectation. Interpret the score as:\n"
    "- **1**: Very confident in a good job.\n"
    "- **0**: Not confident at all.\n"
    "- **[0.8, 1]**: You can continue the path of reasoning if needed.\n"
    "- **[0.5, 0.8)**: Recheck your reasoning and consider reverting to a "
    "previous, more confident reasoning path.\n"
    "- **[0, 0.5)**: Stop because the reasoning is starting to be off track."
)

CONFIDENCE_SCORE_FIELD = FieldModel(
    default=None,
    title="Confidence Score",
    description=_description,
    examples=[0.821, 0.257, 0.923, 0.439],
)

__all__ = ["CONFIDENCE_SCORE_FIELD"]
