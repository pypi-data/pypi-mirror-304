from datetime import datetime
from typing import Any, TypeVar
from zoneinfo import ZoneInfo

from lionabc.exceptions import LionIDError
from pydantic import ConfigDict, field_validator
from typing_extensions import override

from lion_core._class_registry import LION_CLASS_REGISTRY, get_class
from lion_core.generic.base import RealElement
from lion_core.setting import DEFAULT_TIMEZONE
from lion_core.sys_utils import SysUtil
from lion_core.types import IDTypes

T = TypeVar("T", bound="Element")


class Element(RealElement):
    """Base class in the Lion framework."""

    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        populate_by_name=True,
    )

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        """Initialize and register subclasses in the global class registry."""
        super().__pydantic_init_subclass__(**kwargs)
        LION_CLASS_REGISTRY[cls.__name__] = cls

    @property
    def created_datetime(self) -> datetime:
        """Get the creation datetime of the Element."""
        return datetime.fromtimestamp(self.timestamp, tz=DEFAULT_TIMEZONE)

    @field_validator("ln_id", mode="before")
    def _validate_id(cls, value: IDTypes.IDOnly) -> str:
        try:
            return SysUtil.get_id(value)
        except Exception:
            raise LionIDError(f"Invalid lion id: {value}")

    @field_validator("timestamp", mode="before")
    def _validate_timestamp(cls, value: Any) -> float:
        try:
            return validate_timestamp(value)
        except Exception as e:
            raise ValueError(f"Invalid datetime string format: {value}") from e

    @override
    @classmethod
    def from_dict(cls, data: dict, /, **kwargs: Any) -> T:
        """create an instance of the Element or its subclass"""
        if "lion_class" in data:
            cls = get_class(class_name=data.pop("lion_class"))
        if cls.from_dict.__func__ != Element.from_dict.__func__:
            return cls.from_dict(data, **kwargs)
        return cls.model_validate(data, **kwargs)

    @override
    def to_dict(self, **kwargs: Any) -> dict:
        """Convert the Element to a dictionary representation."""
        dict_ = self.model_dump(**kwargs)
        dict_["lion_class"] = self.class_name()
        return dict_

    @override
    def __str__(self) -> str:
        timestamp_str = self.created_datetime.isoformat(timespec="minutes")
        return (
            f"{self.class_name()}(ln_id={self.ln_id[:6]}.., "
            f"timestamp={timestamp_str})"
        )

    def __hash__(self) -> int:
        return hash(self.ln_id)

    def __bool__(self) -> bool:
        """Always True"""
        return True

    def __len__(self) -> int:
        """Return the length of the Element."""
        return 1


def validate_timestamp(
    value: Any,
    tz: str | ZoneInfo = "UTC",
    allow_none: bool = False,
) -> float | None:
    if value is None:
        if allow_none:
            return None
        raise ValueError("Timestamp value cannot be None")

    # Convert timezone string to ZoneInfo object
    if isinstance(tz, str):
        try:
            tz = ZoneInfo(tz)
        except Exception as e:
            raise ValueError(f"Invalid timezone: {tz}") from e

    try:
        # Handle datetime objects
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=tz)
            return value.timestamp()

        # Handle ISO format strings
        if isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=tz)
                return dt.timestamp()
            except ValueError as e:
                raise ValueError(
                    f"Invalid datetime string format: {value}"
                ) from e

        # Handle numeric timestamps
        if isinstance(value, (int, float)):
            # Basic validation - timestamps should be reasonable
            if not (0 <= value <= 9999999999999):  # Up to year 2286
                raise ValueError(
                    f"Timestamp value out of reasonable range: {value}"
                )
            # Convert milliseconds to seconds if needed
            if value > 9999999999:  # If timestamp is in milliseconds
                value = value / 1000
            return float(value)

        # Handle Pandas Timestamp objects
        pd_timestamp_types = (
            "Timestamp",  # Avoid direct Pandas import for lighter dependencies
            "DatetimeTZDtype",
            "datetime64",
            "datetime64[ns]",
        )
        if type(value).__name__ in pd_timestamp_types:
            return value.timestamp()

        raise TypeError(
            f"Unsupported type for timestamp validation: {type(value)}"
        )

    except Exception as e:
        if isinstance(e, (ValueError, TypeError)):
            raise
        raise ValueError(f"Failed to validate timestamp: {str(e)}") from e


__all__ = ["Element"]

# File: lion_core/generic/element.py
