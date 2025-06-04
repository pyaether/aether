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


class ObjectAttributes(GlobalHTMLAttributes):
    data: str
    form: NotRequired[str]
    height: NotRequired[int]
    name: NotRequired[str]
    type: str
    width: NotRequired[int]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Object(BaseHTMLElement):
    tag_name = "object"
    have_children = True
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.PHRASING,
        HTMLContentCategories.EMBEDDED,
        HTMLContentCategories.PALPABLE,
    )

    def __init__(self, **attributes: Unpack[ObjectAttributes]):
        try:
            validated_attributes = ObjectAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
