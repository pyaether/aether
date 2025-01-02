from typing import Literal, NotRequired

from pytempl.base import BaseAttribute, BaseWebElement, WebElementType


class BaseHTMLElement(BaseWebElement):
    web_element_type = WebElementType.HTML


class GlobalHTMLAttributes(BaseAttribute):
    accesskey: NotRequired[str]
    # 'anchor' is experimental hence ignored
    autocapitalize: NotRequired[Literal["none", "sentences", "words", "characters"]]
    # 'autocorrect' is experimental hence ignored
    autofocus: NotRequired[bool]
    _class: NotRequired[str]
    contenteditable: NotRequired[Literal["true", "false", "plaintext-only"]]
    # 'data-*' is ignored
    dir: NotRequired[Literal["ltr", "rtl", "auto"]]
    draggable: NotRequired[bool]
    enterkeyhint: NotRequired[str]
    exportparts: NotRequired[str]
    hidden: NotRequired[bool | Literal["until-found"]]
    id: NotRequired[str]
    inert: NotRequired[bool]
    inputmode: NotRequired[
        Literal["none", "text", "decimal", "numeric", "tel", "search", "email", "url"]
    ]
    _is: NotRequired[str]
    itemid: NotRequired[str]
    itemprop: NotRequired[str]
    itemref: NotRequired[str]
    itemscope: NotRequired[bool]
    itemtype: NotRequired[str]  # This should be a URL
    lang: NotRequired[str]
    nonce: NotRequired[str]
    # 'part' is ignored
    popover: NotRequired[Literal["auto", "manual"]]
    role: NotRequired[str]  # This can further extended by defining WAI-ARIA roles
    slot: NotRequired[str]
    spellcheck: NotRequired[Literal["true", "false"]]
    style: NotRequired[str]
    tabindex: NotRequired[int]
    title: NotRequired[str]
    translate: NotRequired[Literal["yes", "no"]]
    writingsuggestions: NotRequired[Literal["true", "false"]]
