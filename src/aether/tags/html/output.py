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


class OutputAttributes(GlobalHTMLAttributes):
    _for: NotRequired[str]
    form: NotRequired[str]
    name: NotRequired[str]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Output(BaseHTMLElement):
    tag_name = "output"
    have_children = True
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.PHRASING,
        HTMLContentCategories.FORM_ASSOCIATED,
        HTMLContentCategories.PALPABLE,
    )

    def __init__(self, **attributes: Unpack[OutputAttributes]):
        try:
            validated_attributes = OutputAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
