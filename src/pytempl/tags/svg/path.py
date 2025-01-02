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


class PathAttributes(BaseSVGAttributes):
    d: str
    pathLength: str | Literal["none"]

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
        return {"d": "", "pathLength": "none"}


class Path(BaseSVGElement):
    tag_name = "path"
    have_children = False

    def __init__(self, **attributes: Unpack[PathAttributes]):
        try:
            validated_attributes = PathAttributes.validate(
                attributes, PathAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
