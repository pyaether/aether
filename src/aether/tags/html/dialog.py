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


class DialogAttributes(GlobalHTMLAttributes):
    open: NotRequired[bool]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Dialog(BaseHTMLElement):
    tag_name = "dialog"
    have_children = True
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.SECTIONING,
    )

    def __init__(self, **attributes: Unpack[DialogAttributes]):
        if attributes.get("tabindex") is not None:
            raise ValueError(
                f"`tabindex` attribute must not be used on the `{self.__class__.__qualname__}` element."
            )

        try:
            validated_attributes = DialogAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
