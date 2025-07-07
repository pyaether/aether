from __future__ import (
    annotations,
)  # Remove this when Python 3.12 becomes the minimum supported version.

from collections import UserString
from collections.abc import Mapping, Sequence
from decimal import Decimal
from enum import StrEnum
from typing import Annotated, Any, Literal, NotRequired, Self, TypeAlias

from pydantic import BaseModel, Field, field_validator

# Remove this try/except block when Python 3.12 becomes the minimum supported version.
try:
    # Python 3.12+
    from typing import TypedDict

    _AlpineDataType: TypeAlias = (
        bool
        | str
        | int
        | float
        | Decimal
        | None
        | "Statement"
        | list["AlpineHookForm"]
        | Sequence[Any]
        | Mapping[str, Any]
    )
except TypeError:
    from typing import Union

    from typing_extensions import TypedDict

    _AlpineDataType: TypeAlias = Union[
        bool,
        str,
        int,
        float,
        Decimal,
        None,
        "Statement",
        list["AlpineHookForm"],
        Sequence[Any],
        Mapping[str, Any],
    ]


class AlpineValidationTrigger(StrEnum):
    ON_BLUR = "@blur"
    ON_CHANGE = "@change"
    ON_EFFECT = "x-effect"
    ON_INPUT = "@input"


class _AlpineHookFormValidator(TypedDict):
    value_to_validate: NotRequired[str]
    validation_pattern: str | None
    validation_fail_message: str | None
    validation_trigger: AlpineValidationTrigger

    @classmethod
    def default(cls) -> Self:
        return {"validation_trigger": AlpineValidationTrigger.ON_BLUR}


class _AlpineHookFormConstraints(TypedDict):
    min: NotRequired[Decimal]
    min_length: NotRequired[int]
    max: NotRequired[Decimal]
    max_length: NotRequired[int]
    step: NotRequired[Decimal]
    type: NotRequired[Literal["text", "number"]]


class AlpineHookForm(BaseModel):
    name: Annotated[str | None, Field(default=None)]
    required: Annotated[bool | None, Field(default=None)]
    validator: Annotated[
        _AlpineHookFormValidator | None,
        Field(default_factory=_AlpineHookFormValidator.default),
    ]
    constraints: Annotated[_AlpineHookFormConstraints, Field(default_factory=dict)]

    @field_validator("validator", mode="before")
    @classmethod
    def _set_defaults_for_unset_values_for_form_validator(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value

        default_form_validator_values = _AlpineHookFormValidator.default()
        merged_value = {**default_form_validator_values, **value}

        return merged_value


class Statement(UserString):
    def __init__(
        self, content: str, seq_type: Literal["assignment", "definition", "instance"]
    ):
        self.seq_type = seq_type

        super().__init__(content)

    def statement_type(self) -> str:
        return self.seq_type


class AlpineJSData(str):
    data: dict[str, _AlpineDataType]
    directive: Literal["x-data", "x-init", "x-effect"]

    def __new__(
        cls,
        data: dict[str, _AlpineDataType],
        directive: Literal["x-data", "x-init", "x-effect"] = "x-data",
    ):
        parsed_data_object = cls._parse_object(data, directive)
        alpine_js_data_object = super().__new__(cls, parsed_data_object)

        alpine_js_data_object.data = data
        alpine_js_data_object.directive = directive

        return alpine_js_data_object

    @classmethod
    def _parse_object(
        cls,
        data: dict[str, _AlpineDataType],
        directive: Literal["x-data", "x-init", "x-effect"],
    ) -> str:
        data_list = []
        match directive:
            case "x-data":
                separation = ": "
            case "x-init" | "x-effect":
                separation = " = "

        for key, value in data.items():
            if isinstance(value, list):
                if value and all(isinstance(item, AlpineHookForm) for item in value):
                    value = [item.model_dump(exclude_unset=True) for item in value]
                else:
                    value = [
                        item for item in value if not isinstance(item, AlpineHookForm)
                    ]
            elif isinstance(value, AlpineHookForm):
                value = value.model_dump(exclude_unset=True)

            match value:
                case Statement():
                    match value.seq_type:
                        case "definition":
                            data_list.append(f"{key} {value}")
                        case "assignment":
                            if directive == "x-data":
                                data_list.append(f"{key}: {value}")
                            else:
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
            case "x-init" | "x-effect":
                return f"{', '.join(data_list)}"


def alpine_js_data_merge(
    base_alpine_js_data: AlpineJSData | None,
    alpine_js_data_to_merge: AlpineJSData | None,
) -> AlpineJSData | None:
    if base_alpine_js_data is None and alpine_js_data_to_merge is None:
        return None
    if base_alpine_js_data is not None and alpine_js_data_to_merge is None:
        return base_alpine_js_data
    if base_alpine_js_data is None and alpine_js_data_to_merge is not None:
        return alpine_js_data_to_merge

    if base_alpine_js_data.directive != alpine_js_data_to_merge.directive:
        raise TypeError(
            f"{base_alpine_js_data.directive} cannot be merged with {alpine_js_data_to_merge.directive}"
        )

    merged_js_data = base_alpine_js_data.data | alpine_js_data_to_merge.data
    merged_js_data_directive = base_alpine_js_data.directive

    return AlpineJSData(data=merged_js_data, directive=merged_js_data_directive)
