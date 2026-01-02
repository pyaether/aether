from typing import Literal, NotRequired, Self

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


class TextAttributes(BaseSVGAttributes):
    x: str
    y: str
    dx: NotRequired[str]
    dy: NotRequired[str]
    rotate: NotRequired[str]
    textLength: NotRequired[str]
    lengthAdjust: Literal["spacing", "spacingAndGlyphs"]

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
        return {"x": "0", "y": "0", "lengthAdjust": "spacing"}


class Text(BaseSVGElement):
    tag_name = "text"
    have_children = True
    content_category = (
        SVGContentCategories.GRAPHICS,
        SVGContentCategories.TEXT_CONTENT,
    )

    def __init__(self, **attributes: Unpack[TextAttributes]):
        try:
            validated_attributes = TextAttributes.validate(
                attributes, TextAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
