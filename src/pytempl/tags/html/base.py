from typing import Dict, List, Literal, Self

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


class BaseAttributes(GlobalHTMLAttributes):
    href: str
    target: Literal["_blank", "_self", "_parent", "_top", "_unfencedTop"]

    @classmethod
    def validate(
        cls,
        data: Dict,
        default_values: Dict | None = None,
        custom_validators: List[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)

    @classmethod
    def set_defaults(cls) -> Dict:
        return {"target": "_self"}


class Base(BaseHTMLElement):
    tag_name = "base"
    have_children = False

    def __init__(self, **attributes: Unpack[BaseAttributes]):
        try:
            validated_attributes = BaseAttributes.validate(
                attributes, BaseAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
