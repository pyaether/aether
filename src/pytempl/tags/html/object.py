from typing import Dict, List, NotRequired, Self

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


class ObjectAttributes(GlobalHTMLAttributes):
    data: str
    form: NotRequired[str]
    height: NotRequired[int]
    name: NotRequired[str]
    type: str
    width: NotRequired[int]

    @classmethod
    def validate(
        cls,
        data: Dict,
        default_values: Dict | None = None,
        custom_validators: List[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Object(BaseHTMLElement):
    tag_name = "object"
    have_children = True

    def __init__(self, **attributes: Unpack[ObjectAttributes]):
        try:
            validated_attributes = ObjectAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
