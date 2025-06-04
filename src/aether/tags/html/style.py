from typing import Literal, NotRequired, Self

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


class StyleAttributes(GlobalHTMLAttributes):
    blocking: NotRequired[Literal["render"]]
    media: NotRequired[str]
    nonce: NotRequired[str]
    title: NotRequired[str]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Style(BaseHTMLElement):
    tag_name = "style"
    have_children = True
    content_category = (HTMLContentCategories.METADATA,)

    def __init__(self, **attributes: Unpack[StyleAttributes]):
        try:
            validated_attributes = StyleAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
