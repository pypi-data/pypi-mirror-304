from typing import Literal, Union, Optional
from genotype import Model
from .payload import PayloadV1
from .package import PackageSettings


class CollectionBase(Model):
    """Collection base type."""

    v: Literal[1]
    """Schema version."""
    time: int
    """Unix timestamp in milliseconds when the collection version was updated."""
    major: int
    """Major collection version number."""
    minor: int
    """Minor collection version number."""
    draft: bool
    """Signifies if the collection version is a draft."""


class CollectionV1(Model, "CollectionBase"):
    """Collection version."""

    payload: str
    """Collection payload JSON."""
    settings: str
    """Collection settings JSON."""


class CollectionParsedV1(Model, "CollectionBase"):
    """Parsed collection version. Unlike regular collection, the payload property is a parsed JSON object."""

    payload: PayloadV1
    """Collection payload."""
    settings: Union["CollectionSettings", None]
    """Collection settings."""


class CollectionSettings(Model):
    """Collection settings object."""

    package: Optional[PackageSettings] = None
    """Package settings object."""
