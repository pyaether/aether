from typing import Dict, List, Literal, Self

from pydantic import ValidationError as PydanticValidationError

from pytempl.errors import ValidationError
from pytempl.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseSVGAttributes, BaseSVGElement

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class SvgAttributes(BaseSVGAttributes):
    height: str
    preserveAspectRatio: str
    viewBox: str | Literal["none"]
    width: str
    x: str
    y: str
    xmlns: str

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
        return {
            "height": "auto",
            "preserveAspectRatio": "xMidYMid meet",
            "viewBox": "none",
            "width": "auto",
            "x": "0",
            "y": "0",
            "xmlns": "http://www.w3.org/2000/svg",
        }


class Svg(BaseSVGElement):
    tag_name = "svg"
    have_children = True

    def __init__(self, **attributes: Unpack[SvgAttributes]):
        try:
            validated_attributes = SvgAttributes.validate(
                attributes, SvgAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
