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


class ImgAttributes(GlobalHTMLAttributes):
    alt: str
    crossorigin: NotRequired[Literal["anonymous", "use-credentials"]]
    decoding: NotRequired[Literal["auto", "sync", "async"]]
    elementtiming: NotRequired[str]
    fetchpriority: NotRequired[Literal["high", "low", "auto"]]
    height: NotRequired[int]
    ismap: NotRequired[bool]
    loading: NotRequired[Literal["lazy", "eager"]]
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
    sizes: NotRequired[str]
    src: str
    srcset: NotRequired[str]
    width: NotRequired[int]
    usemap: NotRequired[
        str
    ]  # cannot use this attribute if the <img> element is inside an <a> or <button> element

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Img(BaseHTMLElement):
    tag_name = "img"
    have_children = False
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.PHRASING,
        HTMLContentCategories.EMBEDDED,
        HTMLContentCategories.PALPABLE,
    )

    def __init__(self, **attributes: Unpack[ImgAttributes]):
        try:
            validated_attributes = ImgAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        if validated_attributes.get("usemap"):
            self.content_category += (HTMLContentCategories.INTERACTIVE,)

        super().__init__(**validated_attributes)
