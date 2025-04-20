from __future__ import (
    annotations,
)  # Remove this when Python 3.12 becomes the minimum supported version.

from collections import UserString
from collections.abc import Mapping, Sequence
from typing import Any, Literal, TypeAlias

# Remove this try/except block when Python 3.12 becomes the minimum supported version.
try:
    # Python 3.12+
    _AlpineDataType: TypeAlias = (
        bool
        | str
        | int
        | float
        | None
        | "Statement"
        | Sequence[Any]
        | Mapping[str, Any]
    )
except TypeError:
    from typing import Union

    _AlpineDataType: TypeAlias = Union[
        bool, str, int, float, None, "Statement", Sequence[Any], Mapping[str, Any]
    ]


class Statement(UserString):
    def __init__(
        self, content: str, seq_type: Literal["assignment", "definition", "instance"]
    ):
        self.seq_type = seq_type

        super().__init__(content)

    def statement_type(self) -> str:
        return self.seq_type


class AlpineJSData(str):
    def __new__(
        cls, data: _AlpineDataType, directive: Literal["x-data", "x-init"] = "x-data"
    ):
        parsed_data_object = cls._parse_object(data, directive)
        return super().__new__(cls, parsed_data_object)

    @classmethod
    def _parse_object(
        cls,
        data: dict[str, _AlpineDataType],
        directive: Literal["x-data", "x-init"],
    ) -> str:
        data_list = []
        match directive:
            case "x-data":
                separation = ": "
            case "x-init":
                separation = " = "

        for key, value in data.items():
            match value:
                case Statement():
                    match value.seq_type:
                        case "definition":
                            data_list.append(f"{key} {value}")
                        case "assignment":
                            data_list.append(f"{key} = {value}")
                        case "instance":
                            data_list.append(f"{value}")
                case bool():
                    data_list.append(f"{key}{separation}{str(value).lower()}")
                case str():
                    data_list.append(f"{key}{separation}'{value}'")
                case int() | float() | Sequence():
                    data_list.append(f"{key}{separation}{value}")
                case None:
                    data_list.append(f"{key}{separation}null")
                case Mapping():
                    data_list.append(
                        f"{key}{separation}{cls._parse_object(value, directive)}"
                    )
                case _:
                    raise ValueError(f"Unsupported value type: {type(value)}")

        match directive:
            case "x-data":
                return f"{{ {', '.join(data_list)} }}"
            case "x-init":
                return f"{', '.join(data_list)}"
