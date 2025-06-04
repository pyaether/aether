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

from ._base import BaseHTMLElement, GlobalHTMLAttributes, HTMLContentCategories
from .img import Img
from .source import Source

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class PictureAttributes(GlobalHTMLAttributes):
    disabled: NotRequired[bool]
    label: NotRequired[str]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)


class Picture(BaseHTMLElement):
    tag_name = "picture"
    have_children = True
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.PHRASING,
        HTMLContentCategories.PALPABLE,
    )

    def __init__(self, **attributes: Unpack[PictureAttributes]):
        try:
            validated_attributes = PictureAttributes.validate(attributes)
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)

    def __call__(self, *children: str) -> Self:
        allowed_child_types = (str, Img, Source)
        count_img_child_tags = [isinstance(child, Img) for child in children].count(
            True
        )

        if count_img_child_tags > 1:
            raise ValueError(
                f"Only one `img` child is allowed in a `{self.__class__.__qualname__}` element. Found {count_img_child_tags}."
            )
        elif count_img_child_tags <= 0:
            raise ValueError(
                f"At least one `img` child is required in a `{self.__class__.__qualname__}` element."
            )
        else:
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
