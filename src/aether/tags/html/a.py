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


class AAttributes(GlobalHTMLAttributes):
    href: str
    download: NotRequired[str]
    hreflang: NotRequired[str]
    ping: NotRequired[str]  # space separated list of URLs
    referrerpolicy: NotRequired[
        Literal[
            "no-referrer",
            "no-referrer-when-downgrade",
            "origin",
            "origin-when-cross-origin",
            "same-origin",
            "strict-origin",
            "strict-origin-when-cross-origin",
            "unsafe-url",
        ]
    ]
    rel: NotRequired[str]  # space separated list of link types
    target: Literal["_blank", "_self", "_parent", "_top", "_unfencedTop"]

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
        return {"target": "_self"}


class A(BaseHTMLElement):
    tag_name = "a"
    have_children = True
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.INTERACTIVE,
        HTMLContentCategories.PHRASING,
        HTMLContentCategories.PALPABLE,
    )

    def __init__(self, **attributes: Unpack[AAttributes]):
        try:
            validated_attributes = AAttributes.validate(
                attributes, AAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
