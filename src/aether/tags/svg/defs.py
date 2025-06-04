from typing import NotRequired, Self

from pydantic import ValidationError as PydanticValidationError

from aether.errors import ValidationError
from aether.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseSVGAttributes, BaseSVGElement, SVGContentCategories

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class DefsAttributes(BaseSVGAttributes):
    id: NotRequired[str]

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
        return {}


class Defs(BaseSVGElement):
    tag_name = "defs"
    have_children = True
    content_category = (
        SVGContentCategories.CONTAINER,
        SVGContentCategories.STRUCTURAL,
    )

    def __init__(self, **attributes: Unpack[DefsAttributes]):
        try:
            validated_attributes = DefsAttributes.validate(
                attributes, DefsAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
