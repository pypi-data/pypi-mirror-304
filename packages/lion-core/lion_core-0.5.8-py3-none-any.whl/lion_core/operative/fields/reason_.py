from .models import FieldModel

_description = "**Provide a concise reason for the decision made.**"


REASON_FIELD = FieldModel(
    default=None,
    title="Reason",
    description=_description,
)
