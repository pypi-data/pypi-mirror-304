from .models import FieldModel

_description = (
    "Specify whether the step requires actions to be "
    "performed. If **True**, the actions in `action_requests` "
    "must be performed. If **False**, the actions in "
    "`action_requests` are optional. If no tool_schemas"
    " are provided, this field is ignored."
)

ACTION_REQUIRED_FIELD = FieldModel(
    default=False,
    title="Action Required",
    description=_description,
)

__all__ = ["ACTION_REQUIRED_FIELD"]
