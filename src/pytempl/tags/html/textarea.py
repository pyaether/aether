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


class TextareaAttributes(GlobalHTMLAttributes):
    autocomplete: NotRequired[Literal["on", "off"] | str]
    autocorrect: NotRequired[Literal["on", "off"]]
    cols: NotRequired[int]
    dirname: NotRequired[str]
    disabled: NotRequired[bool]
    form: NotRequired[str]
    maxlength: NotRequired[int]
    minlength: NotRequired[int]
    name: NotRequired[str]
    placeholder: NotRequired[str]
    readonly: NotRequired[bool]
    required: NotRequired[bool]
    rows: NotRequired[int]
    spellcheck: NotRequired[Literal["true", "false", "default"]]
    wrap: NotRequired[Literal["hard", "soft"]]

    @classmethod
    def validate(
        cls,
        data: Dict,
        default_values: Dict | None = None,
        custom_validators: List[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Textarea(BaseHTMLElement):
    tag_name = "textarea"
    have_children = True

    def __init__(self, **attributes: Unpack[TextareaAttributes]):
        try:
            validated_attributes = TextareaAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
