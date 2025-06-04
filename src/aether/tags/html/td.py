from typing import NotRequired, Self

from pydantic import ValidationError as PydanticValidationError

from aether.errors import ValidationError
from aether.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseHTMLElement, GlobalHTMLAttributes, HTMLContentCategories

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class TdAttributes(GlobalHTMLAttributes):
    colspan: int
    headers: NotRequired[str]
    rowspan: int

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)

    @classmethod
    def set_defaults(cls) -> dict:
        return {"colspan": 1, "rowspan": 1}


class Td(BaseHTMLElement):
    tag_name = "td"
    have_children = True
    content_category = (HTMLContentCategories.SECTIONING,)

    def __init__(self, **attributes: Unpack[TdAttributes]):
        try:
            validated_attributes = TdAttributes.validate(
                attributes, TdAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
