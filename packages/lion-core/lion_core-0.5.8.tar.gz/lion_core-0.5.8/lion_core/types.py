from collections.abc import Mapping, Sequence
from typing import Annotated, Literal, TypeAlias

from lionabc import Container, Observable, Ordering
from pydantic import Field

# Basic ID type
LnID: TypeAlias = Annotated[
    str,
    Field(description="Lion ID string ('ln...')"),
]


# Reference types for different contexts
class IDTypes:
    """Type definitions for different ID usage contexts."""

    # For functions that accept either ID or item
    Ref: TypeAlias = LnID | Observable

    # For functions requiring just the ID
    IDOnly: TypeAlias = LnID

    # For functions requiring Observable object
    ItemOnly = Observable

    # For collections
    IDSeq: TypeAlias = Sequence[LnID] | Ordering
    ItemSeq: TypeAlias = (
        Sequence[Observable] | Mapping[LnID, Observable] | Container
    )
    RefSeq: TypeAlias = IDSeq | ItemSeq

    SenderRecipient: TypeAlias = (
        LnID | Observable | Literal["system", "user", "N/A", "assistant"]
    )


__all__ = ["LnID", "IDTypes"]
