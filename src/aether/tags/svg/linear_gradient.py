from typing import Literal, Self

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


class LinearGradientAttributes(BaseSVGAttributes):
    gradientUnits: Literal["userSpaceOnUse", "objectBoundingBox"]
    gradientTransform: str
    href: str | Literal["none"]
    spreadMethod: Literal["pad", "reflect", "repeat"]
    x1: str
    x2: str
    y1: str
    y2: str

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
        return {
            "gradientUnits": "objectBoundingBox",
            "gradientTransform": "identity transform",
            "href": "none",
            "spreadMethod": "pad",
            "x1": "0",
            "x2": "0",
            "y1": "0",
            "y2": "0",
        }


class LinearGradient(BaseSVGElement):
    tag_name = "defs"
    have_children = True
    content_category = (SVGContentCategories.GRADIENT,)

    def __init__(self, **attributes: Unpack[LinearGradientAttributes]):
        try:
            validated_attributes = LinearGradientAttributes.validate(
                attributes, LinearGradientAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
