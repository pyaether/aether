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


class ScriptAttributes(GlobalHTMLAttributes):
    _async: NotRequired[bool]
    _defer: NotRequired[bool]
    blocking: NotRequired[Literal["render"]]
    crossorigin: NotRequired[str]
    fetchpriority: NotRequired[Literal["high", "low", "auto"]]
    integrity: NotRequired[str]
    nomodule: NotRequired[bool]
    nonce: NotRequired[str]
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
    src: NotRequired[str]
    type: NotRequired[Literal["importmap", "module"] | str]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Script(BaseHTMLElement):
    tag_name = "script"
    have_children = True
    content_category = (
        HTMLContentCategories.METADATA,
        HTMLContentCategories.FLOW,
        HTMLContentCategories.PHRASING,
    )

    def __init__(self, **attributes: Unpack[ScriptAttributes]):
        if attributes.get("_defer") and attributes.get("_async"):
            raise ValueError(
                f"`_defer` and `_async` attributes must not be used on the `{self.__class__.__qualname__}` element."
            )

        if (
            attributes.get("_defer")
            or attributes.get("_async")
            or attributes.get("integrity")
        ) and not attributes.get("src"):
            raise ValueError(
                f"`src` attribute must be specified on the `{self.__class__.__qualname__}` element when '_defer' or '_async' or 'integrity' attribute is used."
            )

        try:
            validated_attributes = ScriptAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
