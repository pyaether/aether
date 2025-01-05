from typing import Dict, List, Self

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


class HAttributes(GlobalHTMLAttributes):
    @classmethod
    def validate(
        cls,
        data: Dict,
        default_values: Dict | None = None,
        custom_validators: List[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


### H1 ###
class H1(BaseHTMLElement):
    tag_name = "h1"
    have_children = True

    def __init__(self, **attributes: Unpack[HAttributes]):
        try:
            validated_attributes = HAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)


### H2 ###
class H2(BaseHTMLElement):
    tag_name = "h2"
    have_children = True

    def __init__(self, **attributes: Unpack[HAttributes]):
        try:
            validated_attributes = HAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)


### H3 ###
class H3(BaseHTMLElement):
    tag_name = "h3"
    have_children = True

    def __init__(self, **attributes: Unpack[HAttributes]):
        try:
            validated_attributes = HAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)


### H4 ###
class H4(BaseHTMLElement):
    tag_name = "h4"
    have_children = True

    def __init__(self, **attributes: Unpack[HAttributes]):
        try:
            validated_attributes = HAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)


### H5 ###
class H5(BaseHTMLElement):
    tag_name = "h5"
    have_children = True

    def __init__(self, **attributes: Unpack[HAttributes]):
        try:
            validated_attributes = HAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)


### H6 ###
class H6(BaseHTMLElement):
    tag_name = "h6"
    have_children = True

    def __init__(self, **attributes: Unpack[HAttributes]):
        try:
            validated_attributes = HAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
