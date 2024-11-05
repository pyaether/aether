from html import escape as escape_html
from typing import Any, Self


class SafeData:
    def __html__(self) -> Self:
        return self


class SafeString(str, SafeData):
    def __add__(self, rhs: str):
        t = super().__add__(rhs)
        if isinstance(rhs, SafeData):
            return SafeString(t)
        return t

    def __str__(self) -> str:
        return self


def mark_safe(string: str | SafeString) -> str | SafeString:
    if hasattr(string, "__html__"):
        return string
    return SafeString(string)


def safestring_escape(value: Any, escape_quote: bool) -> str | SafeString:
    if hasattr(value, "__html__"):
        return value.__html__()
    else:
        return mark_safe(escape_html(str(value), quote=escape_quote))
