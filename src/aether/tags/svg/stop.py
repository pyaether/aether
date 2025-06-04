from typing import Self

from pydantic import ValidationError as PydanticValidationError

from aether.errors import ValidationError
from aether.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseSVGAttributes, BaseSVGElement, SVGContentCategories

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class StopAttributes(BaseSVGAttributes):
    offset: str
    stop_color: str
    stop_opacity: float

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
        return {"offset": "0", "stop_color": "black", "stop_opacity": 1.0}


def _validate_stop_opacity_range(data: StopAttributes) -> None:
    if data["stop_opacity"] >= 1.0:
        raise ValidationError(
            message="'stop_opacity' should be less than or equal to '1.0' (fully opaque)",
            expected_type="less_than_equal",
            loc=("stop_opacity",),
            input_value=data["stop_opacity"],
        )

    if data["stop_opacity"] <= 0.0:
        raise ValidationError(
            message="'stop_opacity' should be greater than or equal to '0.0' (fully transparent)",
            expected_type="greater_than_equal",
            loc=("stop_opacity",),
            input_value=data["stop_opacity"],
        )


class Stop(BaseSVGElement):
    tag_name = "stop"
    have_children = False
    content_category = (SVGContentCategories.GRADIENT,)

    def __init__(self, **attributes: Unpack[StopAttributes]):
        try:
            validated_attributes = StopAttributes.validate(
                attributes,
                StopAttributes.set_defaults(),
                [_validate_stop_opacity_range],
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
