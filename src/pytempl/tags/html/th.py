from typing import Dict, List, Literal, NotRequired, Self

from pydantic import ValidationError as PydanticValidationError

from pytempl.errors import ValidationError
from pytempl.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseHTMLElement, GlobalHTMLAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class ThAttributes(GlobalHTMLAttributes):
    abbr: NotRequired[str]
    colspan: int
    headers: NotRequired[str]
    rowspan: int
    scope: NotRequired[Literal["row", "col", "rowgroup", "colgroup"]]

    @classmethod
    def validate(
        cls,
        data: Dict,
        default_values: Dict | None = None,
        custom_validators: List[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)

    @classmethod
    def set_defaults(cls) -> Dict:
        return {"colspan": 1, "rowspan": 1}


class Th(BaseHTMLElement):
    tag_name = "th"
    have_children = True

    def __init__(self, **attributes: Unpack[ThAttributes]):
        try:
            validated_attributes = ThAttributes.validate(
                attributes, ThAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
