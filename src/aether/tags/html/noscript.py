from typing import Self

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


class NoscriptAttributes(GlobalHTMLAttributes):
    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Noscript(BaseHTMLElement):
    tag_name = "noscript"
    have_children = True
    content_category = (
        HTMLContentCategories.METADATA,
        HTMLContentCategories.FLOW,
        HTMLContentCategories.PHRASING,
    )

    def __init__(self, **attributes: Unpack[NoscriptAttributes]):
        try:
            validated_attributes = NoscriptAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
