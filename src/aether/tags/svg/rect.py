from typing import Self

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


class RectAttributes(BaseSVGAttributes):
    x: str
    y: str
    width: str
    height: str
    rx: str
    ry: str
    pathLength: str

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
            "x": "0",
            "y": "0",
            "width": "auto",
            "height": "auto",
            "rx": "auto",
            "ry": "auto",
            "pathLength": "",
        }


class Rect(BaseSVGElement):
    tag_name = "rect"
    have_children = False
    content_category = (
        SVGContentCategories.BASIC,
        SVGContentCategories.GRAPHICS,
        SVGContentCategories.SHAPE,
    )

    def __init__(self, **attributes: Unpack[RectAttributes]):
        try:
            validated_attributes = RectAttributes.validate(
                attributes, RectAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
