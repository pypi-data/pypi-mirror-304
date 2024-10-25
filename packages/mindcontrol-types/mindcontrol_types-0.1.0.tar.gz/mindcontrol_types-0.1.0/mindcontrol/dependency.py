from typing import TypeAlias, Literal, Union
from genotype import Model


DependencyV1 : TypeAlias = "DependencyProviderV1"
"""Dependency. What the collection depends on."""


class DependencyProviderV1(Model):
    """Provider dependency."""

    type: Literal["provider"]
    """Dependency type."""
    id: Union[Literal["openai"], Literal["azure"], Literal["aws"], Literal["anthropic"], Literal["gcp"]]
    """Provider id."""
