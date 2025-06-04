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


class FormAttributes(GlobalHTMLAttributes):
    accept_charset: NotRequired[str]
    autocapitalize: NotRequired[Literal["none", "sentences", "words", "characters"]]
    autocomplete: NotRequired[Literal["on", "off"]]
    name: NotRequired[str]
    rel: NotRequired[str]  # space separated list of link types

    action: NotRequired[
        str
    ]  # Can be overridden by formaction attribute on a <button>, <input type="submit">, or <input type="image"> element.
    enctype: NotRequired[
        Literal[
            "application/x-www-form-urlencoded", "multipart/form-data", "text/plain"
        ]
    ]  # Can be overridden by formenctype attributes on a <button>, <input type="submit">, or <input type="image"> element.
    method: NotRequired[
        Literal["get", "post", "dialog"]
    ]  # Can be overridden by formmethod attributes on a <button>, <input type="submit">, or <input type="image"> element.
    novalidate: NotRequired[
        bool
    ]  # Can be overridden by formnovalidate attribute on a <button>, <input type="submit">, or <input type="image"> element.
    target: NotRequired[
        Literal["_self", "_blank", "_parent", "_top", "_unfencedTop"]
    ]  # Can be overridden by formtarget attribute on a <button>, <input type="submit">, or <input type="image"> element.

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Form(BaseHTMLElement):
    tag_name = "form"
    have_children = True
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.PALPABLE,
    )

    def __init__(self, **attributes: Unpack[FormAttributes]):
        try:
            validated_attributes = FormAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
