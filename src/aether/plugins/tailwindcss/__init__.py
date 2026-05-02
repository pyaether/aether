import re

from .utils import get_tw_class_signature, is_color_class, precompute_maps

_VARIANT_REGEX = re.compile(r"^(?:[a-zA-Z0-9-]+:)*")
_ARBITRARY_REGEX = re.compile(r"^(?:[a-zA-Z0-9-]+:)*([a-zA-Z0-9-]+)-\[([^\]]+)\]$")

_CONFLICT_GROUPS: list[tuple[str, list[str]]] = [
    # Display & Visibility
    (
        "display",
        [
            "block",
            "inline-block",
            "inline",
            "flex",
            "inline-flex",
            "table",
            "inline-table",
            "table-caption",
            "table-cell",
            "table-column",
            "table-column-group",
            "table-footer-group",
            "table-header-group",
            "table-row-group",
            "table-row",
            "flow-root",
            "grid",
            "inline-grid",
            "contents",
            "list-item",
            "hidden",
        ],
    ),
    ("visibility", ["visible", "invisible", "collapse"]),
    # Position
    ("position", ["static", "fixed", "absolute", "relative", "sticky"]),
    ("z-index", ["z-"]),
    # Layout
    ("float", ["float-left", "float-right", "float-none", "float-start", "float-end"]),
    (
        "clear",
        [
            "clear-left",
            "clear-right",
            "clear-both",
            "clear-none",
            "clear-start",
            "clear-end",
        ],
    ),
    ("isolation", ["isolate", "isolation-auto"]),
    (
        "object-fit",
        [
            "object-contain",
            "object-cover",
            "object-fill",
            "object-none",
            "object-scale-down",
        ],
    ),
    ("object-position", ["object-"]),
    (
        "overflow",
        [
            "overflow-auto",
            "overflow-hidden",
            "overflow-clip",
            "overflow-visible",
            "overflow-scroll",
        ],
    ),
    (
        "overflow-x",
        [
            "overflow-x-auto",
            "overflow-x-hidden",
            "overflow-x-clip",
            "overflow-x-visible",
            "overflow-x-scroll",
        ],
    ),
    (
        "overflow-y",
        [
            "overflow-y-auto",
            "overflow-y-hidden",
            "overflow-y-clip",
            "overflow-y-visible",
            "overflow-y-scroll",
        ],
    ),
    ("overscroll", ["overscroll-auto", "overscroll-contain", "overscroll-none"]),
    (
        "overscroll-x",
        ["overscroll-x-auto", "overscroll-x-contain", "overscroll-x-none"],
    ),
    (
        "overscroll-y",
        ["overscroll-y-auto", "overscroll-y-contain", "overscroll-y-none"],
    ),
    # Sizing
    ("width", ["w-"]),
    ("min-width", ["min-w-"]),
    ("max-width", ["max-w-"]),
    ("height", ["h-"]),
    ("min-height", ["min-h-"]),
    ("max-height", ["max-h-"]),
    ("size", ["size-"]),
    # Typography
    ("font-family", ["font-sans", "font-serif", "font-mono", "font-"]),
    (
        "font-size",
        [
            "text-xs",
            "text-sm",
            "text-base",
            "text-lg",
            "text-xl",
            "text-2xl",
            "text-3xl",
            "text-4xl",
            "text-5xl",
            "text-6xl",
            "text-7xl",
            "text-8xl",
            "text-9xl",
        ],
    ),
    ("font-smoothing", ["antialiased", "subpixel-antialiased"]),
    ("font-style", ["italic", "not-italic"]),
    (
        "font-weight",
        [
            "font-thin",
            "font-extralight",
            "font-light",
            "font-normal",
            "font-medium",
            "font-semibold",
            "font-bold",
            "font-extrabold",
            "font-black",
        ],
    ),
    (
        "font-variant-numeric",
        [
            "normal-nums",
            "ordinal",
            "slashed-zero",
            "lining-nums",
            "oldstyle-nums",
            "proportional-nums",
            "tabular-nums",
            "diagonal-fractions",
            "stacked-fractions",
        ],
    ),
    ("letter-spacing", ["tracking-"]),
    ("line-clamp", ["line-clamp-"]),
    ("line-height", ["leading-"]),
    ("list-style-image", ["list-image-"]),
    ("list-style-position", ["list-inside", "list-outside"]),
    ("list-style-type", ["list-none", "list-disc", "list-decimal"]),
    (
        "text-align",
        [
            "text-left",
            "text-center",
            "text-right",
            "text-justify",
            "text-start",
            "text-end",
        ],
    ),
    ("text-color", ["text-"]),
    ("text-decoration", ["underline", "overline", "line-through", "no-underline"]),
    ("text-decoration-color", ["decoration-"]),
    (
        "text-decoration-style",
        [
            "decoration-solid",
            "decoration-double",
            "decoration-dotted",
            "decoration-dashed",
            "decoration-wavy",
        ],
    ),
    (
        "text-decoration-thickness",
        [
            "decoration-auto",
            "decoration-from-font",
            "decoration-0",
            "decoration-1",
            "decoration-2",
            "decoration-4",
            "decoration-8",
        ],
    ),
    ("text-underline-offset", ["underline-offset-"]),
    ("text-transform", ["uppercase", "lowercase", "capitalize", "normal-case"]),
    ("text-overflow", ["truncate", "text-ellipsis", "text-clip"]),
    ("text-wrap", ["text-wrap", "text-nowrap", "text-balance", "text-pretty"]),
    ("text-indent", ["indent-"]),
    (
        "vertical-align",
        [
            "align-baseline",
            "align-top",
            "align-middle",
            "align-bottom",
            "align-text-top",
            "align-text-bottom",
            "align-sub",
            "align-super",
        ],
    ),
    (
        "whitespace",
        [
            "whitespace-normal",
            "whitespace-nowrap",
            "whitespace-pre",
            "whitespace-pre-line",
            "whitespace-pre-wrap",
            "whitespace-break-spaces",
        ],
    ),
    ("word-break", ["break-normal", "break-words", "break-all", "break-keep"]),
    ("hyphens", ["hyphens-none", "hyphens-manual", "hyphens-auto"]),
    ("content", ["content-"]),
    # Backgrounds
    ("bg-attachment", ["bg-fixed", "bg-local", "bg-scroll"]),
    (
        "bg-clip",
        ["bg-clip-border", "bg-clip-padding", "bg-clip-content", "bg-clip-text"],
    ),
    ("bg-color", ["bg-"]),
    ("bg-origin", ["bg-origin-border", "bg-origin-padding", "bg-origin-content"]),
    (
        "bg-position",
        [
            "bg-bottom",
            "bg-center",
            "bg-left",
            "bg-left-bottom",
            "bg-left-top",
            "bg-right",
            "bg-right-bottom",
            "bg-right-top",
            "bg-top",
        ],
    ),
    (
        "bg-repeat",
        [
            "bg-repeat",
            "bg-no-repeat",
            "bg-repeat-x",
            "bg-repeat-y",
            "bg-repeat-round",
            "bg-repeat-space",
        ],
    ),
    ("bg-size", ["bg-auto", "bg-cover", "bg-contain"]),
    (
        "bg-image",
        [
            "bg-none",
            "bg-gradient-to-t",
            "bg-gradient-to-tr",
            "bg-gradient-to-r",
            "bg-gradient-to-br",
            "bg-gradient-to-b",
            "bg-gradient-to-bl",
            "bg-gradient-to-l",
            "bg-gradient-to-tl",
        ],
    ),
    # Borders
    (
        "border",
        [
            "border-t-",
            "border-r-",
            "border-b-",
            "border-l-",
            "border-s-",
            "border-e-",
            "border-",
        ],
    ),
    (
        "border-style",
        [
            "border-solid",
            "border-dashed",
            "border-dotted",
            "border-double",
            "border-hidden",
            "border-none",
        ],
    ),
    ("divide-x", ["divide-x-"]),
    ("divide-y", ["divide-y-"]),
    ("divide-color", ["divide-"]),
    (
        "divide-style",
        [
            "divide-solid",
            "divide-dashed",
            "divide-dotted",
            "divide-double",
            "divide-none",
        ],
    ),
    (
        "outline-width",
        ["outline-0", "outline-1", "outline-2", "outline-4", "outline-8"],
    ),
    ("outline-color", ["outline-"]),
    (
        "outline-style",
        [
            "outline-none",
            "outline",
            "outline-dashed",
            "outline-dotted",
            "outline-double",
        ],
    ),
    ("outline-offset", ["outline-offset-"]),
    (
        "ring-width",
        ["ring-0", "ring-1", "ring-2", "ring-4", "ring-8", "ring", "ring-inset"],
    ),
    ("ring-color", ["ring-"]),
    ("ring-opacity", ["ring-opacity-"]),
    (
        "ring-offset-width",
        [
            "ring-offset-0",
            "ring-offset-1",
            "ring-offset-2",
            "ring-offset-4",
            "ring-offset-8",
        ],
    ),
    ("ring-offset-color", ["ring-offset-"]),
    # Effects
    (
        "box-shadow",
        [
            "shadow-xs",
            "shadow-sm",
            "shadow",
            "shadow-md",
            "shadow-lg",
            "shadow-xl",
            "shadow-2xl",
            "shadow-inner",
            "shadow-none",
        ],
    ),
    ("box-shadow-color", ["shadow-"]),
    ("opacity", ["opacity-"]),
    (
        "mix-blend-mode",
        [
            "mix-blend-normal",
            "mix-blend-multiply",
            "mix-blend-screen",
            "mix-blend-overlay",
            "mix-blend-darken",
            "mix-blend-lighten",
            "mix-blend-color-dodge",
            "mix-blend-color-burn",
            "mix-blend-hard-light",
            "mix-blend-soft-light",
            "mix-blend-difference",
            "mix-blend-exclusion",
            "mix-blend-hue",
            "mix-blend-saturation",
            "mix-blend-color",
            "mix-blend-luminosity",
            "mix-blend-plus-lighter",
        ],
    ),
    (
        "background-blend-mode",
        [
            "bg-blend-normal",
            "bg-blend-multiply",
            "bg-blend-screen",
            "bg-blend-overlay",
            "bg-blend-darken",
            "bg-blend-lighten",
            "bg-blend-color-dodge",
            "bg-blend-color-burn",
            "bg-blend-hard-light",
            "bg-blend-soft-light",
            "bg-blend-difference",
            "bg-blend-exclusion",
            "bg-blend-hue",
            "bg-blend-saturation",
            "bg-blend-color",
            "bg-blend-luminosity",
        ],
    ),
    # Flexbox & Grid
    (
        "flex-direction",
        ["flex-row", "flex-row-reverse", "flex-col", "flex-col-reverse"],
    ),
    ("flex-wrap", ["flex-wrap", "flex-wrap-reverse", "flex-nowrap"]),
    ("flex", ["flex-1", "flex-auto", "flex-initial", "flex-none"]),
    ("flex-grow", ["grow", "grow-0"]),
    ("flex-shrink", ["shrink", "shrink-0"]),
    ("order", ["order-"]),
    ("grid-template-columns", ["grid-cols-"]),
    ("grid-column", ["col-auto", "col-span-"]),
    ("grid-column-start", ["col-start-"]),
    ("grid-column-end", ["col-end-"]),
    ("grid-template-rows", ["grid-rows-"]),
    ("grid-row", ["row-auto", "row-span-"]),
    ("grid-row-start", ["row-start-"]),
    ("grid-row-end", ["row-end-"]),
    (
        "grid-auto-flow",
        [
            "grid-flow-row",
            "grid-flow-col",
            "grid-flow-dense",
            "grid-flow-row-dense",
            "grid-flow-col-dense",
        ],
    ),
    (
        "grid-auto-columns",
        ["auto-cols-auto", "auto-cols-min", "auto-cols-max", "auto-cols-fr"],
    ),
    (
        "grid-auto-rows",
        ["auto-rows-auto", "auto-rows-min", "auto-rows-max", "auto-rows-fr"],
    ),
    ("gap", ["gap-"]),
    ("gap-x", ["gap-x-"]),
    ("gap-y", ["gap-y-"]),
    ("space-x", ["space-x-"]),
    ("space-y", ["space-y-"]),
    (
        "justify-content",
        [
            "justify-normal",
            "justify-start",
            "justify-end",
            "justify-center",
            "justify-between",
            "justify-around",
            "justify-evenly",
            "justify-stretch",
        ],
    ),
    (
        "justify-items",
        [
            "justify-items-start",
            "justify-items-end",
            "justify-items-center",
            "justify-items-stretch",
        ],
    ),
    (
        "justify-self",
        [
            "justify-self-auto",
            "justify-self-start",
            "justify-self-end",
            "justify-self-center",
            "justify-self-stretch",
        ],
    ),
    (
        "align-content",
        [
            "content-normal",
            "content-center",
            "content-start",
            "content-end",
            "content-between",
            "content-around",
            "content-evenly",
            "content-baseline",
            "content-stretch",
        ],
    ),
    (
        "align-items",
        ["items-start", "items-end", "items-center", "items-baseline", "items-stretch"],
    ),
    (
        "align-self",
        [
            "self-auto",
            "self-start",
            "self-end",
            "self-center",
            "self-stretch",
            "self-baseline",
        ],
    ),
    (
        "place-content",
        [
            "place-content-center",
            "place-content-start",
            "place-content-end",
            "place-content-between",
            "place-content-around",
            "place-content-evenly",
            "place-content-baseline",
            "place-content-stretch",
        ],
    ),
    (
        "place-items",
        [
            "place-items-start",
            "place-items-end",
            "place-items-center",
            "place-items-baseline",
            "place-items-stretch",
        ],
    ),
    (
        "place-self",
        [
            "place-self-auto",
            "place-self-start",
            "place-self-end",
            "place-self-center",
            "place-self-stretch",
        ],
    ),
]

_SPACING_CSS_PROPERTIES: dict[str, list[str]] = {
    "p-": ["padding-top", "padding-right", "padding-bottom", "padding-left"],
    "px-": ["padding-left", "padding-right"],
    "py-": ["padding-top", "padding-bottom"],
    "ps-": ["padding-inline-start"],
    "pe-": ["padding-inline-end"],
    "pt-": ["padding-top"],
    "pr-": ["padding-right"],
    "pb-": ["padding-bottom"],
    "pl-": ["padding-left"],
    "m-": ["margin-top", "margin-right", "margin-bottom", "margin-left"],
    "mx-": ["margin-left", "margin-right"],
    "my-": ["margin-top", "margin-bottom"],
    "ms-": ["margin-inline-start"],
    "me-": ["margin-inline-end"],
    "mt-": ["margin-top"],
    "mr-": ["margin-right"],
    "mb-": ["margin-bottom"],
    "ml-": ["margin-left"],
}

_INSET_CSS_PROPERTIES: dict[str, list[str]] = {
    "inset-": ["top", "right", "bottom", "left"],
    "inset-x-": ["left", "right"],
    "inset-y-": ["top", "bottom"],
    "inset-s-": ["inset-inline-start"],
    "inset-e-": ["inset-inline-end"],
    "top-": ["top"],
    "right-": ["right"],
    "bottom-": ["bottom"],
    "left-": ["left"],
    "start-": ["inset-inline-start"],
    "end-": ["inset-inline-end"],
}

_BORDER_RADIUS_EXACT: dict[str, list[str]] = {
    "rounded": [
        "border-top-left-radius",
        "border-top-right-radius",
        "border-bottom-right-radius",
        "border-bottom-left-radius",
    ],
}
_BORDER_RADIUS_CSS_PROPERTIES: dict[str, list[str]] = {
    "rounded-": [
        "border-top-left-radius",
        "border-top-right-radius",
        "border-bottom-right-radius",
        "border-bottom-left-radius",
    ],
    "rounded-t-": ["border-top-left-radius", "border-top-right-radius"],
    "rounded-r-": ["border-top-right-radius", "border-bottom-right-radius"],
    "rounded-b-": ["border-bottom-right-radius", "border-bottom-left-radius"],
    "rounded-l-": ["border-top-left-radius", "border-bottom-left-radius"],
    "rounded-s-": ["border-start-start-radius", "border-end-start-radius"],
    "rounded-e-": ["border-start-end-radius", "border-end-end-radius"],
    "rounded-tl-": ["border-top-left-radius"],
    "rounded-tr-": ["border-top-right-radius"],
    "rounded-br-": ["border-bottom-right-radius"],
    "rounded-bl-": ["border-bottom-left-radius"],
    "rounded-ss-": ["border-start-start-radius"],
    "rounded-se-": ["border-start-end-radius"],
    "rounded-ee-": ["border-end-end-radius"],
    "rounded-es-": ["border-end-start-radius"],
}
_BORDER_WIDTH_EXACT: dict[str, list[str]] = {
    "border": [
        "border-top-width",
        "border-right-width",
        "border-bottom-width",
        "border-left-width",
    ],
}
_BORDER_WIDTH_CSS_PROPERTIES: dict[str, list[str]] = {
    "border-": [
        "border-top-width",
        "border-right-width",
        "border-bottom-width",
        "border-left-width",
    ],
    "border-t-": ["border-top-width"],
    "border-r-": ["border-right-width"],
    "border-b-": ["border-bottom-width"],
    "border-l-": ["border-left-width"],
    "border-s-": ["border-inline-start-width"],
    "border-e-": ["border-inline-end-width"],
}

_SPACING_PREFIXES = sorted(_SPACING_CSS_PROPERTIES, key=len, reverse=True)
_INSET_PREFIXES = sorted(_INSET_CSS_PROPERTIES, key=len, reverse=True)
_BORDER_RADIUS_PREFIXES = sorted(_BORDER_RADIUS_CSS_PROPERTIES, key=len, reverse=True)
_BORDER_WIDTH_PREFIXES = sorted(_BORDER_WIDTH_CSS_PROPERTIES, key=len, reverse=True)

_EXACT_MAP, _PREFIX_MAP, _PREFIX_LIST = precompute_maps(
    conflict_groups=_CONFLICT_GROUPS
)


def _find_prefix_match(
    core_class: str,
    prefix_list: list[str],
    prop_map: dict[str, list[str]],
) -> list[str] | None:
    for prefix in prefix_list:
        if core_class.startswith(prefix):
            return prop_map[prefix]
    return None


def tw_merge(*tw_classes: str) -> str:
    if not tw_classes:
        return ""

    all_classes_with_positions = []
    position = 0

    # Use `last-win` resolution
    for class_string in tw_classes:
        if class_string:
            for tw_class in class_string.split():
                if tw_class:
                    all_classes_with_positions.append((tw_class, position))
                    position += 1

    conflict_tw_classes = {}  # (variant, group_id)
    tw_css_property_classes = {}  # (variants, css_property)

    for tw_class, pos in all_classes_with_positions:
        variants, group_id = get_tw_class_signature(
            tw_class,
            variant_regex=_VARIANT_REGEX,
            arbitrary_regex=_ARBITRARY_REGEX,
            exact_map=_EXACT_MAP,
            prefix_map=_PREFIX_MAP,
            sorted_prefix_list=_PREFIX_LIST,
        )

        core_class = tw_class[len(variants) :]

        css_properties: list[str] | None = None

        css_properties = _find_prefix_match(
            core_class, _SPACING_PREFIXES, _SPACING_CSS_PROPERTIES
        )

        if css_properties is None:
            css_properties = _find_prefix_match(
                core_class, _INSET_PREFIXES, _INSET_CSS_PROPERTIES
            )

        if css_properties is None:
            if core_class in _BORDER_RADIUS_EXACT:
                css_properties = _BORDER_RADIUS_EXACT[core_class]
            else:
                css_properties = _find_prefix_match(
                    core_class, _BORDER_RADIUS_PREFIXES, _BORDER_RADIUS_CSS_PROPERTIES
                )

        if css_properties is None:
            if core_class in _BORDER_WIDTH_EXACT:
                css_properties = _BORDER_WIDTH_EXACT[core_class]
            else:
                for prefix in _BORDER_WIDTH_PREFIXES:
                    if core_class.startswith(prefix) and not is_color_class(
                        core_class, prefix
                    ):
                        css_properties = _BORDER_WIDTH_CSS_PROPERTIES[prefix]
                        break

        if css_properties is not None:
            for css_property in css_properties:
                key = (variants, css_property)
                if (
                    key not in tw_css_property_classes
                    or tw_css_property_classes[key][1] < pos
                ):
                    tw_css_property_classes[key] = (tw_class, pos)
        else:
            key = (variants, group_id)
            if key not in conflict_tw_classes or conflict_tw_classes[key][1] < pos:
                conflict_tw_classes[key] = (tw_class, pos)

    final_classes = []
    used_classes = set()

    # Add spacing classes (from CSS property registry)
    for tw_class, pos in tw_css_property_classes.values():
        if tw_class not in used_classes:
            final_classes.append((tw_class, pos))
            used_classes.add(tw_class)

    # Add non-spacing classes
    for tw_class, pos in conflict_tw_classes.values():
        if tw_class not in used_classes:
            final_classes.append((tw_class, pos))
            used_classes.add(tw_class)

    final_classes.sort(key=lambda x: x[1])
    return " ".join(tw_cls for tw_cls, _ in final_classes)
