from .base import BaseAttribute, BaseWebElement, WebElementType
from .safe_string import mark_safe


def render(*elements: BaseWebElement, stringify: bool = True) -> str:
    rendered_elements = [
        mark_safe("").join(element.render(stringify=stringify)) for element in elements
    ]
    return mark_safe("").join(rendered_elements)


__version__ = "0.4.13"
__all__ = [
    "render",
    "BaseAttribute",
    "BaseWebElement",
    "WebElementType",
    "mark_safe",
    "__version__",
]
