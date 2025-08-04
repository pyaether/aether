from re import Pattern


def precompute_maps(
    conflict_groups: list[tuple[str, list[str]]],
) -> tuple[dict[str, str], dict[str, str], list[str]]:
    exact_map: dict[str, str] = {}
    prefix_map: dict[str, str] = {}

    prefix_list: list[str] = []

    for group_id, classes in conflict_groups:
        for item in classes:
            if item.endswith("-"):
                prefix_map[item] = group_id
                prefix_list.append(item)
            else:
                exact_map[item] = group_id

    sorted_prefix_list = sorted(prefix_list, key=len, reverse=True)

    return exact_map, prefix_map, sorted_prefix_list


def _is_color_class(core_class: str, prefix: str) -> bool:
    suffix = core_class[len(prefix) :]

    parts = suffix.split("-")
    if not parts:
        return False

    special_colors = {"current", "transparent", "inherit", "black", "white"}
    if suffix in special_colors:
        return True

    # Check if first part is a known color name
    color_names = {
        "slate",
        "gray",
        "zinc",
        "neutral",
        "stone",
        "red",
        "orange",
        "amber",
        "yellow",
        "lime",
        "green",
        "emerald",
        "teal",
        "cyan",
        "sky",
        "blue",
        "indigo",
        "violet",
        "purple",
        "fuchsia",
        "pink",
        "rose",
    }

    first_part = parts[0]
    if first_part in color_names:
        return True

    # Check if it follows color-[number] pattern
    if len(parts) == 2 and first_part in color_names and parts[1].isdigit():
        return True

    # For text- prefix, also check for common size keywords that are NOT colors
    if prefix == "text-":
        size_keywords = {
            "xs",
            "sm",
            "base",
            "lg",
            "xl",
            "2xl",
            "3xl",
            "4xl",
            "5xl",
            "6xl",
            "7xl",
            "8xl",
            "9xl",
        }
        if suffix in size_keywords:
            return False

    # For border- prefix, check for width keywords that are NOT colors
    if prefix == "border-":
        width_keywords = {"0", "1", "2", "4", "8"}
        if suffix in width_keywords:
            return False

    # If we can't determine definitively, assume it's a color for ambiguous prefixes
    return prefix in (
        "text-",
        "border-",
        "bg-",
        "ring-",
        "outline-",
        "decoration-",
        "caret-",
        "accent-",
        "fill-",
        "stroke-",
        "shadow-",
        "ring-offset-",
        "divide-",
    )


def get_tw_class_signature(
    tw_class: str,
    variant_regex: Pattern[str],
    arbitrary_regex: Pattern[str],
    exact_map: dict[str, str],
    prefix_map: dict[str, str],
    sorted_prefix_list: list[str],
) -> tuple[str, str]:
    # Handle arbitrary values like text-[#ff0000] or hover:text-[#ff0000]
    arbitrary_match = arbitrary_regex.match(tw_class)
    if arbitrary_match:
        variants = tw_class[: arbitrary_match.start(1)]
        base_class = arbitrary_match.group(1)

        base_signature = get_tw_class_signature(
            base_class,
            variant_regex=variant_regex,
            arbitrary_regex=arbitrary_regex,
            exact_map=exact_map,
            prefix_map=prefix_map,
            sorted_prefix_list=sorted_prefix_list,
        )

        return (variants, base_signature[1])

    # Extract variants (modifiers) from the class
    variant_match = variant_regex.match(tw_class)
    variants = variant_match.group(0) if variant_match else ""
    core_tw_class = tw_class[len(variants) :]

    # Check for exact match first
    if core_tw_class in exact_map:
        return (variants, exact_map[core_tw_class])

    # Check prefix matches (longest first)
    for prefix in sorted_prefix_list:
        if core_tw_class.startswith(prefix):
            group_id = prefix_map[prefix]

            if prefix in (
                "border-",
                "text-",
                "ring-",
                "outline-",
                "decoration-",
                "shadow-",
            ):
                if _is_color_class(core_tw_class, prefix):
                    return (variants, f"{group_id}-color")
                else:
                    return (variants, f"{group_id}-size_or_width")

            return (variants, group_id)

    # No match found, return the core class as its own group
    return (variants, core_tw_class)
