import sys
from dataclasses import dataclass, field
from typing import Optional, Tuple, TypedDict, Union

from .formatters import ColumnFormatter

if sys.version_info < (3, 12):
    from typing_extensions import TypedDict  # noqa: F811
else:
    from typing import TypedDict

__all__ = ("ColumnDef", "ColumnSpecDict", "ColumnSpec")


class ColumnSpecDict(TypedDict, total=False):
    name: str
    formatter: ColumnFormatter


@dataclass
class ColumnSpec:
    path: str
    """Dot-delimited path to the column in the input data."""
    name: Optional[str] = field(default=None)
    """Name of the column in the output dataframe. If not provided, the terminal path is used."""
    formatter: Optional[ColumnFormatter] = field(default=None)
    """Formatter to apply to the column data."""

    @classmethod
    def from_tuple(cls, column_def: Tuple[str, ColumnSpecDict]) -> "ColumnSpec":
        path, spec = column_def
        return cls(path, **spec)

    @classmethod
    def from_str(cls, path: str) -> "ColumnSpec":
        return cls(path)

    @classmethod
    def from_def(cls, column_def: "ColumnDef") -> "ColumnSpec":
        if isinstance(column_def, str):
            return cls.from_str(column_def)

        elif isinstance(column_def, tuple):
            return cls.from_tuple(column_def)
        return column_def


ColumnDef = Union[Tuple[str, ColumnSpecDict], str, ColumnSpec]
