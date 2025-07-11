import re

from .utils import get_tw_class_signature, precompute_maps

_VARIANT_REGEX = re.compile(r"^(?:[a-zA-Z0-9-]+:)*")
_ARBITRARY_REGEX = re.compile(r"^(?:[a-zA-Z0-9-]+:)*([a-zA-Z0-9-]+)-\[([^\]]+)\]$")

__CONFLICT_GROUPS: list[tuple[str, list[str]]] = [
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
            "grid",
            "hidden",
        ],
    ),
    ("visibility", ["visible", "invisible"]),
    # Position
    ("position", ["static", "fixed", "absolute", "relative", "sticky"]),
    ("inset", ["inset-x-", "inset-y-", "top-", "right-", "bottom-", "left-", "inset-"]),
    # Sizing
    ("width", ["w-"]),
    ("min-width", ["min-w-"]),
    ("max-width", ["max-w-"]),
    ("height", ["h-"]),
    ("min-height", ["min-h-"]),
    ("max-height", ["max-h-"]),
    # Spacing (Padding, Margin, Space)
    ("padding", ["pt-", "pr-", "pb-", "pl-", "px-", "py-", "p-"]),
    ("margin", ["mt-", "mr-", "mb-", "ml-", "mx-", "my-", "m-"]),
    ("space", ["space-x-", "space-y-"]),
    # Typography
    ("font-size", ["text-xs", "text-sm", "text-base", "text-lg", "text-xl"]),
    (
        "font-weight",
        ["font-thin", "font-light", "font-normal", "font-medium", "font-bold"],
    ),
    # Ambiguous prefixes need special handling in the logic, but are defined here.
    ("text-color", ["text-"]),
    ("text-align", ["text-left", "text-center", "text-right", "text-justify"]),
    # Backgrounds
    ("bg-color", ["bg-"]),
    ("bg-opacity", ["bg-opacity-"]),
    # Borders
    (
        "border-radius",
        ["rounded-t-", "rounded-r-", "rounded-b-", "rounded-l-", "rounded-"],
    ),
    ("border-width", ["border-t-", "border-r-", "border-b-", "border-l-", "border-"]),
    ("border-color", ["border-"]),
    ("border-style", ["border-solid", "border-dashed", "border-dotted", "border-none"]),
    # Flexbox & Grid
    ("flex-direction", ["flex-row", "flex-col"]),
    ("flex-wrap", ["flex-wrap", "flex-nowrap"]),
    ("justify-content", ["justify-"]),
    ("align-items", ["items-"]),
    ("gap", ["gap-x-", "gap-y-", "gap-"]),
    # Effects
    ("opacity", ["opacity-"]),
    ("shadow", ["shadow"]),
]

_EXACT_MAP, _PREFIX_MAP, _PREFIX_LIST = precompute_maps(
    conflict_groups=__CONFLICT_GROUPS
)


def tw_merge(*tw_classes: str) -> str:
    merged_tw_classes = []
    seen_signatures = set()

    for tw_class in reversed(" ".join(tw_classes).split()):
        if not tw_class:
            continue

        signature = get_tw_class_signature(
            tw_class,
            variant_regex=_VARIANT_REGEX,
            arbitrary_regex=_ARBITRARY_REGEX,
            exact_map=_EXACT_MAP,
            prefix_map=_PREFIX_MAP,
            sorted_prefix_list=_PREFIX_LIST,
        )
        if signature not in seen_signatures:
            merged_tw_classes.append(tw_class)
            seen_signatures.add(signature)

    return " ".join(reversed(merged_tw_classes))
