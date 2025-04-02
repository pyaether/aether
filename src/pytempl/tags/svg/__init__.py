# https://developer.mozilla.org/en-US/docs/Web/SVG

from ._base import BaseSVGAttributes, BaseSVGElement
from .circle import Circle, CircleAttributes
from .g import G, GAttributes
from .line import Line, LineAttributes
from .path import Path, PathAttributes
from .polygon import Polygon, PolygonAttributes
from .rect import Rect, RectAttributes
from .svg import Svg, SvgAttributes

__all__ = [
    "BaseSVGElement",
    "Circle",
    "CircleAttributes",
    "G",
    "GAttributes",
    "Line",
    "LineAttributes",
    "Path",
    "PathAttributes",
    "Polygon",
    "PolygonAttributes",
    "Rect",
    "RectAttributes",
    "Svg",
    "SvgAttributes",
    "BaseSVGAttributes",
]
