from typing import Literal, NotRequired

from pytempl.base import BaseAttribute, BaseWebElement, WebElementType


class BaseMathMLElement(BaseWebElement):
    web_element_type = WebElementType.MATHML


class GlobalMathMLAttributes(BaseAttribute):
    dir: NotRequired[Literal["ltr", "rtl", "auto"]]
    displaystyle: NotRequired[Literal["true", "false"]]
    scriptlevel: NotRequired[int]
