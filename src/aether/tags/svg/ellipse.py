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


class EllipseAttributes(BaseSVGAttributes):
    cx: str
    cy: str
    rx: str
    ry: str
    pathLength: NotRequired[str]

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
        return {"cx": "0", "cy": "0", "rx": "0", "ry": "0"}


class Ellipse(BaseSVGElement):
    tag_name = "ellipse"
    have_children = False
    content_category = (
        SVGContentCategories.BASIC,
        SVGContentCategories.GRAPHICS,
        SVGContentCategories.SHAPE,
    )

    def __init__(self, **attributes: Unpack[EllipseAttributes]):
        try:
            validated_attributes = EllipseAttributes.validate(
                attributes, EllipseAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
