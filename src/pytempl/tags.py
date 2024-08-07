from typing import Generator, Literal

from .base import BaseTag


class A(BaseTag):
    tag_name = "a"
    have_children = True

    def __init__(self, href: str, newtab=False, **attributes):
        if newtab:
            attributes["target"] = "_blank"
            attributes["rel"] = "noopener noreferrer"
        super().__init__(href=href, **attributes)


class Abbr(BaseTag):
    tag_name = "abbr"
    have_children = True


class Address(BaseTag):
    tag_name = "address"
    have_children = True


class Area(BaseTag):
    tag_name = "area"
    have_children = False


class Article(BaseTag):
    tag_name = "article"
    have_children = True


class Aside(BaseTag):
    tag_name = "aside"
    have_children = True


class Audio(BaseTag):
    tag_name = "audio"
    have_children = True


class B(BaseTag):
    tag_name = "b"
    have_children = True


class Base(BaseTag):
    tag_name = "base"
    have_children = False


class Bdi(BaseTag):
    tag_name = "bdi"
    have_children = True


class Bdo(BaseTag):
    tag_name = "bdo"
    have_children = True


class Blockquote(BaseTag):
    tag_name = "blockquote"
    have_children = True


class Body(BaseTag):
    tag_name = "body"
    have_children = True


class Br(BaseTag):
    tag_name = "br"
    have_children = False


class Button(BaseTag):
    tag_name = "button"
    have_children = True


class Canvas(BaseTag):
    tag_name = "canvas"
    have_children = True


class Caption(BaseTag):
    tag_name = "caption"
    have_children = True


class Cite(BaseTag):
    tag_name = "cite"
    have_children = True


class Code(BaseTag):
    tag_name = "code"
    have_children = True


class Col(BaseTag):
    tag_name = "col"
    have_children = False


class Colgroup(BaseTag):
    tag_name = "colgroup"
    have_children = True


class Data(BaseTag):
    tag_name = "data"
    have_children = True


class Datalist(BaseTag):
    tag_name = "datalist"
    have_children = True


class Dd(BaseTag):
    tag_name = "dd"
    have_children = True


class Del(BaseTag):
    tag_name = "del"
    have_children = True


class Details(BaseTag):
    tag_name = "details"
    have_children = True


class Dfn(BaseTag):
    tag_name = "dfn"
    have_children = True


class Dialog(BaseTag):
    tag_name = "dialog"
    have_children = True


class Div(BaseTag):
    tag_name = "div"
    have_children = True


class Dl(BaseTag):
    tag_name = "dl"
    have_children = True


class Dt(BaseTag):
    tag_name = "dt"
    have_children = True


class Em(BaseTag):
    tag_name = "em"
    have_children = True


class Embed(BaseTag):
    tag_name = "embed"
    have_children = False


class Fieldset(BaseTag):
    tag_name = "fieldset"
    have_children = True


class Figcaption(BaseTag):
    tag_name = "figcaption"
    have_children = True


class Figure(BaseTag):
    tag_name = "figure"
    have_children = True


class Footer(BaseTag):
    tag_name = "footer"
    have_children = True


class Form(BaseTag):
    tag_name = "form"
    have_children = True


class H1(BaseTag):
    tag_name = "h1"
    have_children = True


class H2(BaseTag):
    tag_name = "h2"
    have_children = True


class H3(BaseTag):
    tag_name = "h3"
    have_children = True


class H4(BaseTag):
    tag_name = "h4"
    have_children = True


class H5(BaseTag):
    tag_name = "h5"
    have_children = True


class H6(BaseTag):
    tag_name = "h6"
    have_children = True


class Head(BaseTag):
    tag_name = "head"
    have_children = True


class Header(BaseTag):
    tag_name = "header"
    have_children = True


class Hgroup(BaseTag):
    tag_name = "hgroup"
    have_children = True


class Hr(BaseTag):
    tag_name = "hr"
    have_children = False


class Html(BaseTag):
    tag_name = "html"
    have_children = True

    def __init__(self, doctype=False, **attributes):
        super().__init__(lang=attributes.get("lang", "en"), **attributes)
        self.doctype = doctype

    def render(self, stringify: bool = True) -> Generator[str, None, None]:
        if self.doctype:
            yield "<!DOCTYPE html>"
        yield from super().render(stringify)


class I(BaseTag):  # noqa: E742
    tag_name = "i"
    have_children = True


class Iframe(BaseTag):
    tag_name = "iframe"
    have_children = True


class Img(BaseTag):
    tag_name = "img"
    have_children = False

    def __init__(self, src: str, **attributes):
        super().__init__(src=src, **attributes)


class Input(BaseTag):
    tag_name = "input"
    have_children = False

    def __init__(
        self,
        type: Literal[
            "button",
            "checkbox",
            "color",
            "date",
            "datetime-local",
            "email",
            "file",
            "hidden",
            "image",
            "month",
            "number",
            "password",
            "radio",
            "range",
            "reset",
            "search",
            "submit",
            "tel",
            "text",
            "time",
            "url",
            "week",
        ] = "text",
        **attributes,
    ):
        super().__init__(type=type, **attributes)


class Ins(BaseTag):
    tag_name = "ins"
    have_children = True


class Kbd(BaseTag):
    tag_name = "kbd"
    have_children = True


class Label(BaseTag):
    tag_name = "label"
    have_children = True


class Legend(BaseTag):
    tag_name = "legend"
    have_children = True


class Li(BaseTag):
    tag_name = "li"
    have_children = True


class Link(BaseTag):
    tag_name = "link"
    have_children = False


class Main(BaseTag):
    tag_name = "main"
    have_children = True


class Map(BaseTag):
    tag_name = "map"
    have_children = True


class Mark(BaseTag):
    tag_name = "mark"
    have_children = True


class Math(BaseTag):
    tag_name = "math"
    have_children = True


class Menu(BaseTag):
    tag_name = "menu"
    have_children = True


class Meta(BaseTag):
    tag_name = "meta"
    have_children = False


class Meter(BaseTag):
    tag_name = "meter"
    have_children = True


class Nav(BaseTag):
    tag_name = "nav"
    have_children = True


class Noscript(BaseTag):
    tag_name = "noscript"
    have_children = True


class Object(BaseTag):
    tag_name = "object"
    have_children = True


class Ol(BaseTag):
    tag_name = "ol"
    have_children = True


class Optgroup(BaseTag):
    tag_name = "optgroup"
    have_children = True


class Option(BaseTag):
    tag_name = "option"
    have_children = True


class Output(BaseTag):
    tag_name = "output"
    have_children = True


class P(BaseTag):
    tag_name = "p"
    have_children = True


class Picture(BaseTag):
    tag_name = "picture"
    have_children = True


class Pre(BaseTag):
    tag_name = "pre"
    have_children = True


class Progress(BaseTag):
    tag_name = "progress"
    have_children = True


class Q(BaseTag):
    tag_name = "q"
    have_children = True


class Rp(BaseTag):
    tag_name = "rp"
    have_children = True


class Rt(BaseTag):
    tag_name = "rt"
    have_children = True


class Ruby(BaseTag):
    tag_name = "ruby"
    have_children = True


class S(BaseTag):
    tag_name = "s"
    have_children = True


class Samp(BaseTag):
    tag_name = "samp"
    have_children = True


class Script(BaseTag):
    tag_name = "script"
    have_children = True

    def __init__(self, **attributes):
        if attributes.get("_defer") and attributes.get("_async"):
            raise ValueError(
                "'Script' element cannot have both '_defer' and '_async' attributes."
            )

        if (
            attributes.get("_defer") or attributes.get("_async")
        ) and not attributes.get("src"):
            raise ValueError(
                "'Script' element must have a 'src' attribute when '_defer' or '_async' attribute is used."
            )

        super().__init__(**attributes)


class Search(BaseTag):
    tag_name = "search"
    have_children = True


class Section(BaseTag):
    tag_name = "section"
    have_children = True


class Select(BaseTag):
    tag_name = "select"
    have_children = True


class Slot(BaseTag):
    tag_name = "slot"
    have_children = True


class Small(BaseTag):
    tag_name = "small"
    have_children = True


class Source(BaseTag):
    tag_name = "source"
    have_children = False


class Span(BaseTag):
    tag_name = "span"
    have_children = True


class Strong(BaseTag):
    tag_name = "strong"
    have_children = True


class Style(BaseTag):
    tag_name = "style"
    have_children = True


class Sub(BaseTag):
    tag_name = "sub"
    have_children = True


class Summary(BaseTag):
    tag_name = "summary"
    have_children = True


class Sup(BaseTag):
    tag_name = "sup"
    have_children = True


class Svg(BaseTag):
    tag_name = "svg"
    have_children = True

    def __init__(self, **attributes):
        attributes.setdefault("xmlns", "http://www.w3.org/2000/svg")
        super().__init__(**attributes)


class Table(BaseTag):
    tag_name = "table"
    have_children = True


class Tbody(BaseTag):
    tag_name = "tbody"
    have_children = True


class Td(BaseTag):
    tag_name = "td"
    have_children = True


class Template(BaseTag):
    tag_name = "template"
    have_children = True


class Textarea(BaseTag):
    tag_name = "textarea"
    have_children = True


class Tfoot(BaseTag):
    tag_name = "tfoot"
    have_children = True


class Th(BaseTag):
    tag_name = "th"
    have_children = True


class THead(BaseTag):
    tag_name = "thead"
    have_children = True


class Time(BaseTag):
    tag_name = "time"
    have_children = True


class Title(BaseTag):
    tag_name = "title"
    have_children = True


class Tr(BaseTag):
    tag_name = "tr"
    have_children = True


class Track(BaseTag):
    tag_name = "track"
    have_children = False


class U(BaseTag):
    tag_name = "u"
    have_children = True


class Ul(BaseTag):
    tag_name = "ul"
    have_children = True


class Var(BaseTag):
    tag_name = "var"
    have_children = True


class Video(BaseTag):
    tag_name = "video"
    have_children = True


class Wbr(BaseTag):
    tag_name = "wbr"
    have_children = False
