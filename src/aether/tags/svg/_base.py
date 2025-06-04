from enum import StrEnum

from aether.base import BaseAttribute, BaseWebElement, WebElementType


class SVGContentCategories(StrEnum):
    ANIMATION = "animation"
    BASIC = "basic"
    CONTAINER = "container"
    DESCRIPTIVE = "descriptive"
    FILTER = "filter"
    FONT = "font"
    GRADIENT = "gradient"
    GRAPHICS = "graphics"
    GRAPHICS_REFERENCING = "graphics_referencing"
    LIGHT_SOURCE = "light_source"
    NEVER_RENDERED = "never_rendered"
    PAINT_SERVER = "paint_server"
    RENDERABLE = "renderable"
    SHAPE = "shape"
    STRUCTURAL = "structural"
    TEXT_CONTENT = "text_content"
    TEXT_CONTENT_CHILD = "text_content_child"
    UNCATEGORIZED = "uncategorized"


class BaseSVGElement(BaseWebElement[SVGContentCategories]):
    web_element_type = WebElementType.SVG


class BaseSVGAttributes(BaseAttribute):
    pass
