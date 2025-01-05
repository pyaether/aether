import warnings
from typing import Dict, Generator, Iterable, List, Self

from pydantic import ValidationError as PydanticValidationError

from pytempl.errors import ValidationError
from pytempl.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseHTMLElement, GlobalHTMLAttributes
from .dd import Dd
from .div import Div
from .dt import Dt

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class DlAttributes(GlobalHTMLAttributes):
    @classmethod
    def validate(
        cls,
        data: Dict,
        default_values: Dict | None = None,
        custom_validators: List[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Dl(BaseHTMLElement):
    tag_name = "dl"
    have_children = True

    def __init__(self, **attributes: Unpack[DlAttributes]):
        try:
            validated_attributes = DlAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)

    def __call__(self, *children: str) -> Self:
        allowed_child_types = (Dd, Dt, Div)

        if self.have_children:
            for child in children:
                if (
                    isinstance(child, str)
                    or isinstance(child, allowed_child_types)
                    or not isinstance(child, Iterable)
                ):
                    self.children.append(child)
                elif isinstance(child, Generator):
                    serialized_children_generator = list(child)
                    if all(
                        isinstance(gen_child, allowed_child_types)
                        for gen_child in serialized_children_generator
                    ):
                        self.children.extend(serialized_children_generator)
                    else:
                        raise ValueError(
                            f"Invalid child type found. `{self.__class__.__qualname__}` can only have {', '.join([type(allowed_type).__class__.__qualname__ for allowed_type in allowed_child_types])}."
                        )
                elif isinstance(child, type(None)):
                    continue
                else:
                    if all(
                        isinstance(iter_child, allowed_child_types)
                        for iter_child in child
                    ):
                        self.children.extend(child)
                    else:
                        raise ValueError(
                            f"Invalid child type found. `{self.__class__.__qualname__}` can only have {', '.join([type(allowed_type).__class__.__qualname__ for allowed_type in allowed_child_types])}."
                        )
        else:
            warnings.warn(
                f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
                UserWarning,
                stacklevel=2,
            )
        return self
