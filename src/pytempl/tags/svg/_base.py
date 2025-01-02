from pytempl.base import BaseAttribute, BaseWebElement, WebElementType


class BaseSVGElement(BaseWebElement):
    web_element_type = WebElementType.SVG


class SVGAttributes(BaseAttribute):
    pass
