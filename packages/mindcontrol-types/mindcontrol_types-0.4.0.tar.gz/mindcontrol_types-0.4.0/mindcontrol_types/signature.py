from .var import VarV1
from typing import List, Literal, Union, TypeAlias
from genotype import Model


class SignatureV1(Model):
    """Prompt signature. It defines the input and output types of the prompt."""

    input: List["SignatureInputV1"]
    """Input definition."""
    output: "SignatureOutputV1"
    """Output definition."""
    n: int
    """The number of choices to generate."""


class SignatureInputV1(Model):
    """Input schema. It defines individual input variable and type."""

    type: "SignatureInputV1Type"
    """Input type."""
    var: VarV1
    """Input variable."""


SignatureInputV1Type : TypeAlias = Union[Literal["string"], Literal["number"]]


class SignatureOutputV1(Model):
    """Output type. It defines output variable and type."""

    type: "SignatureOutputV1Type"
    """Output type."""
    var: VarV1
    """Output variable."""


SignatureOutputV1Type : TypeAlias = Union[Literal["string"], Literal["json"]]
