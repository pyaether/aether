import re
import warnings
from collections.abc import Generator, Iterable
from enum import StrEnum
from typing import Any, Generic, Self, TypedDict, TypeVar

from pydantic import ConfigDict

from .safe_string import safestring_escape
from .utils import flatten_attributes, handle_exception


class WebElementType(StrEnum):
    HTML = "html"
    SVG = "svg"
    MATHML = "mathml"


class BaseAttribute(TypedDict):
    __pydantic_config__ = ConfigDict(extra="allow")


T = TypeVar("T")


class BaseWebElement(Generic[T]):
    web_element_type: WebElementType
    tag_name: str
    have_children: bool
    content_category: tuple[T] | None

    def __init__(self, escape_quote: bool = True, **attributes: dict) -> None:
        self.attributes = {
            re.sub(r"^_", "", key).replace("_", "-"): value
            for key, value in attributes.items()
            if value is not None and (not isinstance(value, bool) or value)
        }
        if self.have_children:
            self.children = []

        self.escape_quote = escape_quote

    def __call__(self, *children: tuple) -> Self:
        if self.have_children:
            for child in children:
                if (
                    isinstance(child, str)
                    or isinstance(child, BaseWebElement)
                    or not isinstance(child, Iterable)
                ):
                    self.children.append(child)
                elif isinstance(child, Generator):
                    self.children.extend(list(child))
                elif isinstance(child, type(None)):
                    continue
                else:
                    self.children.extend(child)
        else:
            warnings.warn(
                f"Trying to add child to a non-child element: {self.__class__.__qualname__}",
                UserWarning,
                stacklevel=2,
            )
        return self

    def render(self, stringify: bool = True) -> Generator[str, None, None]:
        attribute_string = flatten_attributes(self.attributes)
        attribute_string = (
            (" " + attribute_string) if attribute_string else attribute_string
        )

        if self.have_children:
            yield f"<{self.tag_name}{attribute_string}>"
            for child in self.children:
                yield from _render_element(child, stringify, self.escape_quote)
            yield f"</{self.tag_name}>"
        else:
            yield f"<{self.tag_name}{attribute_string} />"


def _render_element(
    element: Any, stringify: bool = True, escape_quote: bool = True
) -> Generator[str, None, None]:
    try:
        if isinstance(element, BaseWebElement):
            yield from element.render(stringify=stringify)
        elif element is not None:
            yield safestring_escape(element, escape_quote) if stringify else element
    except (Exception, RuntimeError) as e:
        yield from handle_exception(e)
