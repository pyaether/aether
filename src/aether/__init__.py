from .base import BaseAttribute, BaseWebElement, WebElementType
from .safe_string import mark_safe


def render(root: BaseWebElement) -> str:
    return mark_safe("").join(root.render(stringify=True))


__version__ = "0.3.1"
__all__ = [
    "render",
    "BaseAttribute",
    "BaseWebElement",
    "WebElementType",
    "mark_safe",
    "__version__",
]
