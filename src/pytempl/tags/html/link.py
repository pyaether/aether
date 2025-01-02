from typing import Dict, List, Literal, NotRequired, Self

from pydantic import ValidationError as PydanticValidationError

from pytempl.errors import ValidationError
from pytempl.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseHTMLElement, GlobalHTMLAttributes

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
        data: Dict,
        default_values: Dict | None = None,
        custom_validators: List[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Link(BaseHTMLElement):
    tag_name = "link"
    have_children = False

    def __init__(self, **attributes: Unpack[LinkAttributes]):
        try:
            validated_attributes = LinkAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
