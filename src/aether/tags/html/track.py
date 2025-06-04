from typing import Literal, NotRequired, Self

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


class TrackAttributes(GlobalHTMLAttributes):
    default: NotRequired[bool]
    kind: NotRequired[Literal["subtitles", "captions", "chapters", "metadata"]]
    label: NotRequired[str]
    src: str
    srclang: NotRequired[str]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Track(BaseHTMLElement):
    tag_name = "track"
    have_children = False
    content_category = None

    def __init__(self, **attributes: Unpack[TrackAttributes]):
        try:
            validated_attributes = TrackAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
