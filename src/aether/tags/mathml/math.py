from typing import Literal, Self

from pydantic import ValidationError as PydanticValidationError

from aether.errors import ValidationError
from aether.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseMathMLElement, GlobalMathMLAttributes, MathMLContentCategories

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class MathAttributes(GlobalMathMLAttributes):
    display: Literal["block", "inline"]

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
        return {"display": "inline"}


class Math(BaseMathMLElement):
    tag_name = "math"
    have_children = True
    content_category = (MathMLContentCategories.TOP_LEVEL,)

    def __init__(self, **attributes: Unpack[MathAttributes]):
        try:
            validated_attributes = MathAttributes.validate(
                attributes, MathAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
