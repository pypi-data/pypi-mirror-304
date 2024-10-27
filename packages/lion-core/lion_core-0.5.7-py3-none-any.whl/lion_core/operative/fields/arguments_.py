from .models import FieldModel

_arguments_description = (
    "Provide the arguments to pass to the function as a "
    "dictionary. **Use "
    "argument names and types as specified in the "
    "`tool_schemas`; do not "
    "invent argument names.**"
)

ARGUMENTS_FIELD = FieldModel(
    default_factory=dict,
    title="Arguments",
    description=_arguments_description,
    examples=[{"num1": 1, "num2": 2}, {"x": "hello", "y": "world"}],
)

__all__ = ["ARGUMENTS_FIELD"]
