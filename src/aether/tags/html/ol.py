import warnings
from collections.abc import Generator, Iterable
from typing import Literal, NotRequired, Self

from pydantic import ValidationError as PydanticValidationError

from aether.errors import ValidationError
from aether.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseHTMLElement, GlobalHTMLAttributes, HTMLContentCategories
from .li import Li
from .script import Script
from .template import Template

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class OlAttributes(GlobalHTMLAttributes):
    reversed: NotRequired[bool]
    start: NotRequired[int]
    type: Literal["a", "A", "i", "I", "1"]

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
        return {"type": "1"}


class Ol(BaseHTMLElement):
    tag_name = "ol"
    have_children = True
    content_category = (HTMLContentCategories.FLOW,)

    def __init__(self, **attributes: Unpack[OlAttributes]):
        try:
            validated_attributes = OlAttributes.validate(
                attributes, OlAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)

    def __call__(self, *children: str) -> Self:
        allowed_child_types = (str, Li, Script, Template)
        has_any_li_child_tag = any(isinstance(child, Li) for child in children)

        if has_any_li_child_tag:
            self.content_category += (HTMLContentCategories.PALPABLE,)

        if self.have_children:
            for child in children:
                if isinstance(child, allowed_child_types) or not isinstance(
                    child, Iterable
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
