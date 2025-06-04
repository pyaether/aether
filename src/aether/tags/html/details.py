from typing import Self

from pydantic import ValidationError as PydanticValidationError

from aether.errors import ValidationError
from aether.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseHTMLElement, GlobalHTMLAttributes, HTMLContentCategories
from .summary import Summary

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class DetailsAttributes(GlobalHTMLAttributes):
    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Details(BaseHTMLElement):
    tag_name = "details"
    have_children = True
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.SECTIONING,
        HTMLContentCategories.INTERACTIVE,
        HTMLContentCategories.PALPABLE,
    )

    def __init__(self, **attributes: Unpack[DetailsAttributes]):
        try:
            validated_attributes = DetailsAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)

    def __call__(self, *children: str) -> Self:
        count_summary_child_tags = [
            isinstance(child, Summary) for child in children
        ].count(True)

        if count_summary_child_tags > 1:
            raise ValueError(
                f"Only one `summary` child is allowed in a `{self.__class__.__qualname__}` element. Found {count_summary_child_tags}."
            )
        elif count_summary_child_tags <= 0:
            raise ValueError(
                f"At least one `summary` child is required in a `{self.__class__.__qualname__}` element."
            )
        else:
            return super().__call__(*children)
