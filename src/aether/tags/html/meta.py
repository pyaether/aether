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


class MetaAttributes(GlobalHTMLAttributes):
    charset: NotRequired[str]
    content: NotRequired[str]
    http_equiv: NotRequired[
        Literal[
            "content-security-policy",
            "content-type",
            "default-style",
            "x-ua-compatible",
            "refresh",
        ]
    ]
    media: NotRequired[str]
    name: NotRequired[str]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Meta(BaseHTMLElement):
    tag_name = "meta"
    have_children = False
    content_category = (HTMLContentCategories.FLOW,)

    def __init__(self, **attributes: Unpack[MetaAttributes]):
        try:
            validated_attributes = MetaAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        if validated_attributes.get("itemprop"):
            self.content_category += (
                HTMLContentCategories.FLOW,
                HTMLContentCategories.PHRASING,
            )

        super().__init__(**validated_attributes)
