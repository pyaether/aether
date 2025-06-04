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


class AreaAttributes(GlobalHTMLAttributes):
    alt: NotRequired[str]
    coords: (
        str | None
    )  # comma-separated list of coordinates if shape is rect/poly and `x,y,radius` if shape is circle
    download: NotRequired[str]
    href: NotRequired[str]
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
    shape: Literal["default", "rect", "circle", "poly"]
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
        return {"coords": None, "target": "_self"}


def _validate_coords_conditional(data: AreaAttributes) -> None:
    if data["shape"] == "default" and data["coords"] is not None:
        raise ValidationError(
            message="`Coords` is not allowed when `shape` is `default`",
            expected_type="none_required",
            loc=("coords",),
            input_value=data["coords"],
        )


def _validate_href_alt_conditional(data: AreaAttributes) -> None:
    if data.get("href") is not None and data.get("alt") is None:
        raise ValidationError(
            message="`alt` is required when `href` is provided",
            expected_type="required",
            loc=("alt",),
            input_value=None,
        )


# NOTE: element is used only within a <map> element.


class Area(BaseHTMLElement):
    tag_name = "area"
    have_children = False
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.PHRASING,
    )

    def __init__(self, **attributes: Unpack[AreaAttributes]):
        try:
            validated_attributes = AreaAttributes.validate(
                attributes,
                AreaAttributes.set_defaults(),
                [_validate_coords_conditional, _validate_href_alt_conditional],
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
