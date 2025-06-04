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


class InputAttributes(GlobalHTMLAttributes):
    autocomplete: NotRequired[Literal["on", "off"] | str]
    disabled: NotRequired[bool]
    form: NotRequired[str]
    name: NotRequired[str]
    type: Literal[
        "button",
        "checkbox",
        "color",
        "date",
        "datetime-local",
        "email",
        "file",
        "hidden",
        "image",
        "month",
        "number",
        "password",
        "radio",
        "range",
        "reset",
        "search",
        "submit",
        "tel",
        "text",
        "time",
        "url",
        "week",
    ]
    value: NotRequired[str]

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
        return {"type": "text"}


class Input(BaseHTMLElement):
    tag_name = "input"
    have_children = False
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.PHRASING,
        HTMLContentCategories.FORM_ASSOCIATED,
    )

    def __init__(self, **attributes: Unpack[InputAttributes]):
        try:
            validated_attributes = InputAttributes.validate(
                attributes, InputAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        if validated_attributes.get("type") != "hidden":
            self.content_category += (HTMLContentCategories.PALPABLE,)

        super().__init__(**validated_attributes)
