import warnings
from collections.abc import Generator, Iterable
from typing import NotRequired, Self

from pydantic import ValidationError as PydanticValidationError

from aether.errors import ValidationError
from aether.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseHTMLElement, GlobalHTMLAttributes
from .col import Col

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class ColgroupAttributes(GlobalHTMLAttributes):
    span: NotRequired[int]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Colgroup(BaseHTMLElement):
    tag_name = "colgroup"
    have_children = True
    content_category = None

    def __init__(self, **attributes: Unpack[ColgroupAttributes]):
        try:
            validated_attributes = ColgroupAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)

    def __call__(self, *children: str) -> Self:
        has_span_attribute = self.attributes.get("span") is not None
        has_any_col_child_tag = any(isinstance(child, Col) for child in children)
        allowed_child_types = (str, Col)

        if self.have_children:
            if has_span_attribute and has_any_col_child_tag:
                warnings.warn(
                    "`span` attribute is not permitted if there are one or more `col` child tags are provided. Ignoring `span` attribute.",
                    UserWarning,
                    stacklevel=2,
                )
                self.attributes.pop("span")
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
