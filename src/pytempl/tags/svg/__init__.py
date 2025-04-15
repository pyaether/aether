# https://developer.mozilla.org/en-US/docs/Web/SVG

from ._base import BaseSVGAttributes, BaseSVGElement
from .circle import Circle, CircleAttributes
from .defs import Defs, DefsAttributes
from .g import G, GAttributes
from .line import Line, LineAttributes
from .linear_gradient import LinearGradient, LinearGradientAttributes
from .path import Path, PathAttributes
from .polygon import Polygon, PolygonAttributes
from .rect import Rect, RectAttributes
from .stop import Stop, StopAttributes
from .svg import Svg, SvgAttributes

__all__ = [
    "BaseSVGElement",
    "Circle",
    "CircleAttributes",
    "Defs",
    "DefsAttributes",
    "G",
    "GAttributes",
    "Line",
    "LineAttributes",
    "LinearGradient",
    "LinearGradientAttributes",
    "Path",
    "PathAttributes",
    "Polygon",
    "PolygonAttributes",
    "Rect",
    "RectAttributes",
    "Stop",
    "StopAttributes",
    "Svg",
    "SvgAttributes",
    "BaseSVGAttributes",
]
