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
        data: Dict,
        default_values: Dict | None = None,
        custom_validators: List[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Meta(BaseHTMLElement):
    tag_name = "meta"
    have_children = False

    def __init__(self, **attributes: Unpack[MetaAttributes]):
        try:
            validated_attributes = MetaAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
