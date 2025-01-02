# https://developer.mozilla.org/en-US/docs/Web/SVG

from ._base import BaseSVGElement, SVGAttributes
from .circle import Circle
from .line import Line
from .path import Path
from .rect import Rect
from .svg import Svg

__all__ = [
    "BaseSVGElement",
    "Circle",
    "Line",
    "Path",
    "Rect",
    "Svg",
    "SVGAttributes",
]
