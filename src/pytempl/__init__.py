from . import tags
from .base import BaseWebElement
from .safe_string import mark_safe


def render(root: BaseWebElement) -> str:
    return mark_safe("").join(root.render(stringify=True))


__version__ = "0.1.0"
__all__ = ["render", "tags", "BaseWebElement", "mark_safe", "__version__"]
