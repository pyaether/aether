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


class EmbedAttributes(GlobalHTMLAttributes):
    height: NotRequired[int]  # in pixels
    src: str
    type: str
    width: NotRequired[int]  # in pixels

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Embed(BaseHTMLElement):
    tag_name = "embed"
    have_children = False
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.PHRASING,
        HTMLContentCategories.INTERACTIVE,
        HTMLContentCategories.EMBEDDED,
        HTMLContentCategories.PALPABLE,
    )

    def __init__(self, **attributes: Unpack[EmbedAttributes]):
        try:
            validated_attributes = EmbedAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
