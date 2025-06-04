# https://developer.mozilla.org/en-US/docs/Web/HTML

from ._base import BaseHTMLElement, GlobalHTMLAttributes
from .a import A, AAttributes
from .abbr import Abbr, AbbrAttributes
from .address import Address, AddressAttributes
from .area import Area, AreaAttributes
from .article import Article, ArticleAttributes
from .aside import Aside, AsideAttributes
from .audio import Audio, AudioAttributes
from .b import B, BAttributes
from .bdi import Bdi, BdiAttributes
from .bdo import Bdo, BdoAttributes
from .blockquote import Blockquote, BlockquoteAttributes
from .body import Body, BodyAttributes
from .br import Br, BrAttributes
from .button import Button, ButtonAttributes
from .canvas import Canvas, CanvasAttributes
from .caption import Caption, CaptionAttributes
from .cite import Cite, CiteAttributes
from .code import Code, CodeAttributes
from .col import Col, ColAttributes
from .colgroup import Colgroup, ColgroupAttributes
from .data import Data, DataAttributes
from .datalist import Datalist, DatalistAttributes
from .dd import Dd, DdAttributes
from .del_ import Del, DelAttributes
from .details import Details, DetailsAttributes
from .dfn import Dfn, DfnAttributes
from .dialog import Dialog, DialogAttributes
from .div import Div, DivAttributes
from .dl import Dl, DlAttributes
from .dt import Dt, DtAttributes
from .em import Em, EmAttributes
from .embed import Embed, EmbedAttributes
from .fieldset import Fieldset, FieldsetAttributes
from .figcaption import Figcaption, FigcaptionAttributes
from .figure import Figure, FigureAttributes
from .footer import Footer, FooterAttributes
from .form import Form, FormAttributes
from .h import H1, H2, H3, H4, H5, H6, HAttributes
from .head import Head, HeadAttributes
from .header import Header, HeaderAttributes
from .hgroup import Hgroup, HgroupAttributes
from .hr import Hr, HrAttributes
from .html import Html, HtmlAttributes
from .i import I, IAttributes
from .iframe import Iframe, IframeAttributes
from .img import Img, ImgAttributes
from .input import Input, InputAttributes
from .ins import Ins, InsAttributes
from .kbd import Kbd, KbdAttributes
from .label import Label, LabelAttributes
from .legend import Legend, LegendAttributes
from .li import Li, LiAttributes
from .link import Link, LinkAttributes
from .main import Main, MainAttributes
from .map import Map, MapAttributes
from .mark import Mark, MarkAttributes
from .menu import Menu, MenuAttributes
from .meta import Meta, MetaAttributes
from .meter import Meter, MeterAttributes
from .nav import Nav, NavAttributes
from .noscript import Noscript, NoscriptAttributes
from .object import Object, ObjectAttributes
from .ol import Ol, OlAttributes
from .optgroup import Optgroup, OptgroupAttributes
from .option import Option, OptionAttributes
from .output import Output, OutputAttributes
from .p import P, PAttributes
from .picture import Picture, PictureAttributes
from .pre import Pre, PreAttributes
from .progress import Progress, ProgressAttributes
from .q import Q, QAttributes
from .rp import Rp, RpAttributes
from .rt import Rt, RtAttributes
from .ruby import Ruby, RubyAttributes
from .s import S, SAttributes
from .samp import Samp, SampAttributes
from .script import Script, ScriptAttributes
from .search import Search, SearchAttributes
from .section import Section, SectionAttributes
from .select import Select, SelectAttributes
from .slot import Slot, SlotAttributes
from .small import Small, SmallAttributes
from .source import Source, SourceAttributes
from .span import Span, SpanAttributes
from .strong import Strong, StrongAttributes
from .style import Style, StyleAttributes
from .sub import Sub, SubAttributes
from .summary import Summary, SummaryAttributes
from .sup import Sup, SupAttributes
from .table import Table, TableAttributes
from .tbody import Tbody, TbodyAttributes
from .td import Td, TdAttributes
from .template import Template, TemplateAttributes
from .textarea import Textarea, TextareaAttributes
from .tfoot import Tfoot, TfootAttributes
from .th import Th, ThAttributes
from .thead import Thead, TheadAttributes
from .time import Time, TimeAttributes
from .title import Title, TitleAttributes
from .tr import Tr, TrAttributes
from .track import Track, TrackAttributes
from .u import U, UAttributes
from .ul import Ul, UlAttributes
from .var import Var, VarAttributes
from .video import Video, VideoAttributes
from .wbr import Wbr, WbrAttributes

__all__ = [
    "A",
    "AAttributes",
    "Abbr",
    "AbbrAttributes",
    "Address",
    "AddressAttributes",
    "Area",
    "AreaAttributes",
    "Article",
    "ArticleAttributes",
    "Aside",
    "AsideAttributes",
    "Audio",
    "AudioAttributes",
    "B",
    "BAttributes",
    "BaseHTMLElement",
    "Bdi",
    "BdiAttributes",
    "Bdo",
    "BdoAttributes",
    "Blockquote",
    "BlockquoteAttributes",
    "Body",
    "BodyAttributes",
    "Br",
    "BrAttributes",
    "Button",
    "ButtonAttributes",
    "Canvas",
    "CanvasAttributes",
    "Caption",
    "CaptionAttributes",
    "Cite",
    "CiteAttributes",
    "Code",
    "CodeAttributes",
    "Col",
    "ColAttributes",
    "Colgroup",
    "ColgroupAttributes",
    "Data",
    "DataAttributes",
    "Datalist",
    "DatalistAttributes",
    "Dd",
    "DdAttributes",
    "Del",
    "DelAttributes",
    "Details",
    "DetailsAttributes",
    "Dfn",
    "DfnAttributes",
    "Dialog",
    "DialogAttributes",
    "Div",
    "DivAttributes",
    "Dl",
    "DlAttributes",
    "Dt",
    "DtAttributes",
    "Em",
    "EmAttributes",
    "Embed",
    "EmbedAttributes",
    "Fieldset",
    "FieldsetAttributes",
    "Figcaption",
    "FigcaptionAttributes",
    "Figure",
    "FigureAttributes",
    "Footer",
    "FooterAttributes",
    "Form",
    "FormAttributes",
    "GlobalHTMLAttributes",
    "H1",
    "H2",
    "H3",
    "H4",
    "H5",
    "H6",
    "HAttributes",
    "Head",
    "HeadAttributes",
    "Header",
    "HeaderAttributes",
    "Hgroup",
    "HgroupAttributes",
    "Hr",
    "HrAttributes",
    "Html",
    "HtmlAttributes",
    "I",
    "IAttributes",
    "Iframe",  # TODO: Revisit this later
    "IframeAttributes",
    "Img",
    "ImgAttributes",
    "Input",  # TODO: Revisit this later
    "InputAttributes",
    "Ins",
    "InsAttributes",
    "Kbd",
    "KbdAttributes",
    "Label",
    "LabelAttributes",
    "Legend",
    "LegendAttributes",
    "Li",
    "LiAttributes",
    "Link",  # TODO: Revisit this later
    "LinkAttributes",
    "Main",
    "MainAttributes",
    "Map",
    "MapAttributes",
    "Mark",
    "MarkAttributes",
    "Menu",
    "MenuAttributes",
    "Meta",
    "MetaAttributes",
    "Meter",
    "MeterAttributes",
    "Nav",
    "NavAttributes",
    "Noscript",
    "NoscriptAttributes",
    "Object",
    "ObjectAttributes",
    "Ol",
    "OlAttributes",
    "Optgroup",
    "OptgroupAttributes",
    "Option",
    "OptionAttributes",
    "Output",
    "OutputAttributes",
    "P",
    "PAttributes",
    "Picture",
    "PictureAttributes",
    "Pre",
    "PreAttributes",
    "Progress",
    "ProgressAttributes",
    "Q",
    "QAttributes",
    "Rp",
    "RpAttributes",
    "Rt",
    "RtAttributes",
    "Ruby",
    "RubyAttributes",
    "S",
    "SAttributes",
    "Samp",
    "SampAttributes",
    "Script",
    "ScriptAttributes",
    "Search",
    "SearchAttributes",
    "Section",
    "SectionAttributes",
    "Select",
    "SelectAttributes",
    "Slot",
    "SlotAttributes",
    "Small",
    "SmallAttributes",
    "Source",
    "SourceAttributes",
    "Span",
    "SpanAttributes",
    "Strong",
    "StrongAttributes",
    "Style",
    "StyleAttributes",
    "Sub",
    "SubAttributes",
    "Summary",
    "SummaryAttributes",
    "Sup",
    "SupAttributes",
    "Table",
    "TableAttributes",
    "Tbody",
    "TbodyAttributes",
    "Td",
    "TdAttributes",
    "Template",
    "TemplateAttributes",
    "Textarea",
    "TextareaAttributes",
    "Tfoot",
    "TfootAttributes",
    "Th",
    "ThAttributes",
    "Thead",
    "TheadAttributes",
    "Time",
    "TimeAttributes",
    "Title",
    "TitleAttributes",
    "Tr",
    "TrAttributes",
    "Track",
    "TrackAttributes",
    "U",
    "UAttributes",
    "Ul",
    "UlAttributes",
    "Var",
    "VarAttributes",
    "Video",
    "VideoAttributes",
    "Wbr",
    "WbrAttributes",
]
