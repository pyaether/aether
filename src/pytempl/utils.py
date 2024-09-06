from typing import Any, Dict

from .safe_string import safestring_escape


def flatten_attributes(attributes: Dict[str, Any]) -> str:
    attribute_list = []
    for key, value in attributes.items():
        if isinstance(value, bool) and key != "value":
            if value is True:
                attribute_list.append(f"{safestring_escape(key)}")
        else:
            attribute_list.append(
                f'{safestring_escape(key)}="{safestring_escape(value)}"'
            )
    return " ".join(attribute_list)


# TODO: Make this function more informative
def handle_exception(exception):
    yield (
        '<pre style="border: solid 1px red; color: red; padding: 1rem; '
        'background-color: #ffdddd">'
        f"    <code>~~~ Exception: {safestring_escape(exception)} ~~~</code>"
        "</pre>"
        f'<script>console.log("Error: {safestring_escape(exception)}")</script>'
    )


def html_class_merge(base_html_class_list: str, html_class_list_to_merge: str) -> str:
    base_html_classes = base_html_class_list.split()
    base_html_class_prefix = {cls.split("-")[0] for cls in base_html_classes}

    unique_html_classes = [
        cls
        for cls in html_class_list_to_merge.split()
        if cls.split("-")[0] not in base_html_class_prefix
    ]

    return " ".join(base_html_classes + unique_html_classes)
