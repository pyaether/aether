from .base import BaseWebElement
from .safe_string import mark_safe
from .tags import *  # noqa: F403


def render(root: BaseWebElement) -> str:
    return mark_safe("").join(root.render(stringify=True))


__version__ = "0.0.0"
