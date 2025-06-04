from enum import StrEnum
from typing import Literal, NotRequired

from aether.base import BaseAttribute, BaseWebElement, WebElementType


class MathMLContentCategories(StrEnum):
    TOP_LEVEL = "top_level"
    TOKEN = "token"  # noqa: S105
    GENERAL = "general"
    SCRIPT_AND_LIMIT = "script_and_limit"
    TABULAR = "tabular"
    UNCATEGORIZED = "uncategorized"


class BaseMathMLElement(BaseWebElement[MathMLContentCategories]):
    web_element_type = WebElementType.MATHML


class GlobalMathMLAttributes(BaseAttribute):
    dir: NotRequired[Literal["ltr", "rtl", "auto"]]
    displaystyle: NotRequired[Literal["true", "false"]]
    scriptlevel: NotRequired[int]
