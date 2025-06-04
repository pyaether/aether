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
from .a import A
from .p import P
from .source import Source
from .track import Track

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class VideoAttributes(GlobalHTMLAttributes):
    autoplay: NotRequired[bool]
    controls: NotRequired[bool]
    controlslist: NotRequired[
        set[Literal["nodownload", "nofullscreen", "noremoteplayback"]]
    ]
    crossorigin: NotRequired[Literal["anonymous", "use-credentials"]]
    disablepictureinpicture: NotRequired[bool]
    disableremoteplayback: NotRequired[bool]
    height: NotRequired[int]
    loop: NotRequired[bool]
    muted: NotRequired[bool]
    playsinline: NotRequired[bool]
    poster: NotRequired[str]
    preload: NotRequired[Literal["auto", "metadata", "none"]]
    src: str | None
    width: NotRequired[int]

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
        return {"src": None}


class Video(BaseHTMLElement):
    tag_name = "video"
    have_children = True
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.PHRASING,
        HTMLContentCategories.EMBEDDED,
    )

    def __init__(self, **attributes: Unpack[VideoAttributes]):
        try:
            validated_attributes = VideoAttributes.validate(
                attributes, VideoAttributes.set_defaults()
            )
        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        if validated_attributes.get("controls"):
            self.content_category += (
                HTMLContentCategories.INTERACTIVE,
                HTMLContentCategories.PALPABLE,
            )

        super().__init__(**validated_attributes)

    def __call__(self, *children: str) -> Self:
        has_src_attribute = self.attributes.get("src") is not None
        has_any_source_child_tag = any(isinstance(child, Source) for child in children)
        allowed_child_types = (str, A, P, Source, Track)
        if self.have_children:
            if not has_src_attribute and not has_any_source_child_tag:
                raise ValueError(
                    f"Either `src` attribute or `Source` child tag must be provided for `{self.__class__.__qualname__}`."
                )
            if has_src_attribute and has_any_source_child_tag:
                warnings.warn(
                    "Both `src` attribute and `Source` child tag are provided. Ignoring `src` attribute.",
                    UserWarning,
                    stacklevel=2,
                )
                self.attributes.pop("src")

            for child in children:
                if isinstance(child, allowed_child_types) or not isinstance(
                    child, Iterable
                ):
                    self.children.append(child)
                elif isinstance(child, Generator):
                    serialized_children_generator = list(child)
                    if all(
                        isinstance(node, allowed_child_types)
                        for node in serialized_children_generator
                    ):
                        self.children.extend(serialized_children_generator)
                    else:
                        raise ValueError(
                            f"Invalid child type found. `{self.__class__.__qualname__}` can only have {', '.join([type(allowed_type).__class__.__qualname__ for allowed_type in allowed_child_types])}."
                        )
                elif isinstance(child, type(None)):
                    continue
                else:
                    if all(isinstance(node, allowed_child_types) for node in child):
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
