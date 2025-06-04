from typing import NotRequired, Self

from pydantic import ValidationError as PydanticValidationError

from aether.errors import ValidationError
from aether.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseHTMLElement, GlobalHTMLAttributes

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class SourceAttributes(GlobalHTMLAttributes):
    height: NotRequired[int]
    media: NotRequired[str]
    sizes: NotRequired[str]
    src: NotRequired[str]  # Required for video and audio
    srcset: NotRequired[str]  # Required for picture
    type: NotRequired[str]
    width: NotRequired[int]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Source(BaseHTMLElement):
    tag_name = "source"
    have_children = False
    content_category = None

    def __init__(self, **attributes: Unpack[SourceAttributes]):
        try:
            validated_attributes = SourceAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
