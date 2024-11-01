from typing import Generator, Literal

from .base import BaseWebElement


class A(BaseWebElement):
    tag_name = "a"
    have_children = True

    def __init__(self, href: str, newtab=False, **attributes):
        if newtab:
            attributes["target"] = "_blank"
            attributes["rel"] = "noopener noreferrer"
        super().__init__(href=href, **attributes)


class Abbr(BaseWebElement):
    tag_name = "abbr"
    have_children = True


class Address(BaseWebElement):
    tag_name = "address"
    have_children = True


class Area(BaseWebElement):
    tag_name = "area"
    have_children = False


class Article(BaseWebElement):
    tag_name = "article"
    have_children = True


class Aside(BaseWebElement):
    tag_name = "aside"
    have_children = True


class Audio(BaseWebElement):
    tag_name = "audio"
    have_children = True


class B(BaseWebElement):
    tag_name = "b"
    have_children = True


class Base(BaseWebElement):
    tag_name = "base"
    have_children = False


class Bdi(BaseWebElement):
    tag_name = "bdi"
    have_children = True


class Bdo(BaseWebElement):
    tag_name = "bdo"
    have_children = True


class Blockquote(BaseWebElement):
    tag_name = "blockquote"
    have_children = True


class Body(BaseWebElement):
    tag_name = "body"
    have_children = True


class Br(BaseWebElement):
    tag_name = "br"
    have_children = False


class Button(BaseWebElement):
    tag_name = "button"
    have_children = True


class Canvas(BaseWebElement):
    tag_name = "canvas"
    have_children = True


class Caption(BaseWebElement):
    tag_name = "caption"
    have_children = True


# SVG Element
class Circle(BaseWebElement):
    tag_name = "circle"
    have_children = False


class Cite(BaseWebElement):
    tag_name = "cite"
    have_children = True


class Code(BaseWebElement):
    tag_name = "code"
    have_children = True


class Col(BaseWebElement):
    tag_name = "col"
    have_children = False


class Colgroup(BaseWebElement):
    tag_name = "colgroup"
    have_children = True


class Data(BaseWebElement):
    tag_name = "data"
    have_children = True


class Datalist(BaseWebElement):
    tag_name = "datalist"
    have_children = True


class Dd(BaseWebElement):
    tag_name = "dd"
    have_children = True


class Del(BaseWebElement):
    tag_name = "del"
    have_children = True


class Details(BaseWebElement):
    tag_name = "details"
    have_children = True


class Dfn(BaseWebElement):
    tag_name = "dfn"
    have_children = True


class Dialog(BaseWebElement):
    tag_name = "dialog"
    have_children = True


class Div(BaseWebElement):
    tag_name = "div"
    have_children = True


class Dl(BaseWebElement):
    tag_name = "dl"
    have_children = True


class Dt(BaseWebElement):
    tag_name = "dt"
    have_children = True


class Em(BaseWebElement):
    tag_name = "em"
    have_children = True


class Embed(BaseWebElement):
    tag_name = "embed"
    have_children = False


class Fieldset(BaseWebElement):
    tag_name = "fieldset"
    have_children = True


class Figcaption(BaseWebElement):
    tag_name = "figcaption"
    have_children = True


class Figure(BaseWebElement):
    tag_name = "figure"
    have_children = True


class Footer(BaseWebElement):
    tag_name = "footer"
    have_children = True


class Form(BaseWebElement):
    tag_name = "form"
    have_children = True


class H1(BaseWebElement):
    tag_name = "h1"
    have_children = True


class H2(BaseWebElement):
    tag_name = "h2"
    have_children = True


class H3(BaseWebElement):
    tag_name = "h3"
    have_children = True


class H4(BaseWebElement):
    tag_name = "h4"
    have_children = True


class H5(BaseWebElement):
    tag_name = "h5"
    have_children = True


class H6(BaseWebElement):
    tag_name = "h6"
    have_children = True


class Head(BaseWebElement):
    tag_name = "head"
    have_children = True


class Header(BaseWebElement):
    tag_name = "header"
    have_children = True


class Hgroup(BaseWebElement):
    tag_name = "hgroup"
    have_children = True


class Hr(BaseWebElement):
    tag_name = "hr"
    have_children = False


class Html(BaseWebElement):
    tag_name = "html"
    have_children = True

    def __init__(self, doctype=False, **attributes):
        super().__init__(lang=attributes.get("lang", "en"), **attributes)
        self.doctype = doctype

    def render(self, stringify: bool = True) -> Generator[str, None, None]:
        if self.doctype:
            yield "<!DOCTYPE html>"
        yield from super().render(stringify)


class I(BaseWebElement):  # noqa: E742
    tag_name = "i"
    have_children = True


class Iframe(BaseWebElement):
    tag_name = "iframe"
    have_children = True


class Img(BaseWebElement):
    tag_name = "img"
    have_children = False

    def __init__(self, src: str, **attributes):
        super().__init__(src=src, **attributes)


class Input(BaseWebElement):
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


class Ins(BaseWebElement):
    tag_name = "ins"
    have_children = True


class Kbd(BaseWebElement):
    tag_name = "kbd"
    have_children = True


class Label(BaseWebElement):
    tag_name = "label"
    have_children = True


class Legend(BaseWebElement):
    tag_name = "legend"
    have_children = True


class Li(BaseWebElement):
    tag_name = "li"
    have_children = True


# SVG Element
class Line(BaseWebElement):
    tag_name = "line"
    have_children = False


class Link(BaseWebElement):
    tag_name = "link"
    have_children = False


class Main(BaseWebElement):
    tag_name = "main"
    have_children = True


class Map(BaseWebElement):
    tag_name = "map"
    have_children = True


class Mark(BaseWebElement):
    tag_name = "mark"
    have_children = True


class Math(BaseWebElement):
    tag_name = "math"
    have_children = True


class Menu(BaseWebElement):
    tag_name = "menu"
    have_children = True


class Meta(BaseWebElement):
    tag_name = "meta"
    have_children = False


class Meter(BaseWebElement):
    tag_name = "meter"
    have_children = True


class Nav(BaseWebElement):
    tag_name = "nav"
    have_children = True


class Noscript(BaseWebElement):
    tag_name = "noscript"
    have_children = True


class Object(BaseWebElement):
    tag_name = "object"
    have_children = True


class Ol(BaseWebElement):
    tag_name = "ol"
    have_children = True


class Optgroup(BaseWebElement):
    tag_name = "optgroup"
    have_children = True


class Option(BaseWebElement):
    tag_name = "option"
    have_children = True


class Output(BaseWebElement):
    tag_name = "output"
    have_children = True


class P(BaseWebElement):
    tag_name = "p"
    have_children = True


# SVG Element
class Path(BaseWebElement):
    tag_name = "path"
    have_children = False


class Picture(BaseWebElement):
    tag_name = "picture"
    have_children = True


class Pre(BaseWebElement):
    tag_name = "pre"
    have_children = True


class Progress(BaseWebElement):
    tag_name = "progress"
    have_children = True


class Q(BaseWebElement):
    tag_name = "q"
    have_children = True


# SVG Element
class Rect(BaseWebElement):
    tag_name = "rect"
    have_children = False


class Rp(BaseWebElement):
    tag_name = "rp"
    have_children = True


class Rt(BaseWebElement):
    tag_name = "rt"
    have_children = True


class Ruby(BaseWebElement):
    tag_name = "ruby"
    have_children = True


class S(BaseWebElement):
    tag_name = "s"
    have_children = True


class Samp(BaseWebElement):
    tag_name = "samp"
    have_children = True


class Script(BaseWebElement):
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


class Search(BaseWebElement):
    tag_name = "search"
    have_children = True


class Section(BaseWebElement):
    tag_name = "section"
    have_children = True


class Select(BaseWebElement):
    tag_name = "select"
    have_children = True


class Slot(BaseWebElement):
    tag_name = "slot"
    have_children = True


class Small(BaseWebElement):
    tag_name = "small"
    have_children = True


class Source(BaseWebElement):
    tag_name = "source"
    have_children = False


class Span(BaseWebElement):
    tag_name = "span"
    have_children = True


class Strong(BaseWebElement):
    tag_name = "strong"
    have_children = True


class Style(BaseWebElement):
    tag_name = "style"
    have_children = True


class Sub(BaseWebElement):
    tag_name = "sub"
    have_children = True


class Summary(BaseWebElement):
    tag_name = "summary"
    have_children = True


class Sup(BaseWebElement):
    tag_name = "sup"
    have_children = True


# SVG Element
class Svg(BaseWebElement):
    tag_name = "svg"
    have_children = True

    def __init__(self, **attributes):
        attributes.setdefault("xmlns", "http://www.w3.org/2000/svg")
        super().__init__(**attributes)


class Table(BaseWebElement):
    tag_name = "table"
    have_children = True


class Tbody(BaseWebElement):
    tag_name = "tbody"
    have_children = True


class Td(BaseWebElement):
    tag_name = "td"
    have_children = True


class Template(BaseWebElement):
    tag_name = "template"
    have_children = True


class Textarea(BaseWebElement):
    tag_name = "textarea"
    have_children = True


class Tfoot(BaseWebElement):
    tag_name = "tfoot"
    have_children = True


class Th(BaseWebElement):
    tag_name = "th"
    have_children = True


class THead(BaseWebElement):
    tag_name = "thead"
    have_children = True


class Time(BaseWebElement):
    tag_name = "time"
    have_children = True


class Title(BaseWebElement):
    tag_name = "title"
    have_children = True


class Tr(BaseWebElement):
    tag_name = "tr"
    have_children = True


class Track(BaseWebElement):
    tag_name = "track"
    have_children = False


class U(BaseWebElement):
    tag_name = "u"
    have_children = True


class Ul(BaseWebElement):
    tag_name = "ul"
    have_children = True


class Var(BaseWebElement):
    tag_name = "var"
    have_children = True


class Video(BaseWebElement):
    tag_name = "video"
    have_children = True


class Wbr(BaseWebElement):
    tag_name = "wbr"
    have_children = False
