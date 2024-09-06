from . import tags
from .base import BaseWebElement
from .safe_string import mark_safe
from .utils import html_class_merge


def render(root: BaseWebElement) -> str:
    return mark_safe("").join(root.render(stringify=True))


__version__ = "0.0.0"
__all__ = ["render", "tags", "BaseWebElement", "mark_safe", "html_class_merge"]
