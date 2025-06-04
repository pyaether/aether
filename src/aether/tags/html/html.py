from collections.abc import Generator
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


class HtmlAttributes(GlobalHTMLAttributes):
    lang: str
    xmlns: NotRequired[str]

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
        return {"lang": "en"}


class Html(BaseHTMLElement):
    tag_name = "html"
    have_children = True
    content_category = None

    def __init__(
        self, doctype_value: str = "html", **attributes: Unpack[HtmlAttributes]
    ):
        try:
            validated_attributes = HtmlAttributes.validate(
                attributes, HtmlAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
        self.doctype_value = doctype_value

    def render(self, stringify: bool = True) -> Generator[str, None, None]:
        if self.doctype_value:
            yield f"<!DOCTYPE {self.doctype_value}>"
        yield from super().render(stringify)
