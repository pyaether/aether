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


class MeterAttributes(GlobalHTMLAttributes):
    value: int
    min: int
    max: int
    low: NotRequired[int]
    high: NotRequired[int]
    optimum: NotRequired[int]
    form: NotRequired[str]

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
        return {"min": 0, "max": 1}


class Meter(BaseHTMLElement):
    tag_name = "meter"
    have_children = True

    def __init__(self, **attributes: Unpack[MeterAttributes]):
        try:
            validated_attributes = MeterAttributes.validate(
                attributes, MeterAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
