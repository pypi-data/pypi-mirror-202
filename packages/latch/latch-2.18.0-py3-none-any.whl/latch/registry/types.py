from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Type, Union

from typing_extensions import TypeAlias

from latch.registry.record import Record
from latch.registry.upstream_types.types import DBType
from latch.registry.upstream_types.values import EmptyCell
from latch.types import LatchDir, LatchFile


@dataclass(frozen=True)
class InvalidValue:
    """Registry :class:`Record` value that failed validation."""

    raw_value: str
    """User-provided string representation of the invalid value.

    May be `""` (the empty string) if the value is missing but the column is required.
    """


RegistryPythonValue: TypeAlias = Union[
    str,
    datetime,
    date,
    int,
    float,
    Record,
    None,
    List["RegistryPythonValue"],
    LatchFile,
    LatchDir,
]

RecordValue: TypeAlias = Union[RegistryPythonValue, EmptyCell, InvalidValue]


@dataclass(frozen=True)
class Column:
    """Registry :class:`Table` column definition.

    :meth:`Table.get_columns` is the typical way to get a :class:`Column`.
    """

    key: str
    """Unique identifier within the table. Not globally unique."""
    type: Union[Type[RegistryPythonValue], Type[Union[RegistryPythonValue, EmptyCell]]]
    """Python equivalent of the stored column type."""
    # fixme(maximsmol): deal with defaults
    # default: Union[RegistryPythonValue, EmptyCell]
    upstream_type: DBType
    """Raw column type.

    Used to convert between Python values and Registry values.
    """
