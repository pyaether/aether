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
            else:
                exact_map[item] = group_id

    sorted_prefix_list = sorted(prefix_list, key=len, reverse=True)

    return exact_map, prefix_map, sorted_prefix_list


def get_tw_class_signature(
    tw_class: str,
    variant_regex: Pattern[str],
    arbitrary_regex: Pattern[str],
    exact_map: dict[str, str],
    prefix_map: dict[str, str],
    sorted_prefix_list: list[str],
) -> tuple[str, str]:
    arbitrary_match = arbitrary_regex.match(tw_class)
    if arbitrary_match:
        pass

    variant_match = variant_regex.match(tw_class)
    variants = variant_match.group(0) if variant_match else ""
    core_tw_class = tw_class[len(variants) :]

    if core_tw_class in exact_map:
        return (variants, exact_map[core_tw_class])

    for prefix in sorted_prefix_list:
        if core_tw_class.startswith(prefix):
            group_id = prefix_map[prefix]

            if prefix in ("border-", "text-"):
                is_color = any(
                    _class.isalpha() for _class in core_tw_class.split("-")[-1]
                )
                return (
                    (variants, f"{group_id}color")
                    if is_color
                    else (variants, f"{group_id}size_or_width")
                )

            return (variants, group_id)

    return (variants, core_tw_class)
