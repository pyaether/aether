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


class LinkAttributes(GlobalHTMLAttributes):
    _as: NotRequired[
        Literal[
            "audio",
            "document",
            "embed",
            "fetch",
            "font",
            "image",
            "object",
            "script",
            "style",
            "track",
            "video",
            "worker",
        ]
    ]
    blocking: NotRequired[Literal["render"]]
    crossorigin: NotRequired[Literal["anonymous", "use-credentials"]]
    disabled: NotRequired[bool]
    fetchpriority: NotRequired[Literal["high", "low", "auto"]]
    href: str
    hreflang: NotRequired[str]
    imagesizes: NotRequired[str]
    imagesrcset: NotRequired[str]
    integrity: NotRequired[str]
    media: NotRequired[str]
    referrerpolicy: NotRequired[
        Literal[
            "no-referrer",
            "no-referrer-when-downgrade",
            "origin",
            "origin-when-cross-origin",
            "unsafe-url",
        ]
    ]
    rel: str
    sizes: NotRequired[str]
    title: NotRequired[str]
    type: NotRequired[str]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Link(BaseHTMLElement):
    tag_name = "link"
    have_children = False
    content_category = (HTMLContentCategories.METADATA,)

    def __init__(self, **attributes: Unpack[LinkAttributes]):
        try:
            validated_attributes = LinkAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        if validated_attributes.get("itemprop"):
            self.content_category += (
                HTMLContentCategories.FLOW,
                HTMLContentCategories.PHRASING,
            )

        super().__init__(**validated_attributes)
