from .base import BaseTag
from .safe_string import mark_safe
from .tags import *  # noqa: F403


def render(root: BaseTag) -> str:
    return mark_safe("").join(root.render(stringify=True))


__version__ = "0.0.0"
