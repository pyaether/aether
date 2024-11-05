from typing import Any, Dict

from .safe_string import safestring_escape


def flatten_attributes(attributes: Dict[str, Any]) -> str:
    attribute_list = []
    for key, value in attributes.items():
        if isinstance(value, bool) and key != "value":
            if value is True:
                attribute_list.append(f"{safestring_escape(key, True)}")
        else:
            attribute_list.append(
                f'{safestring_escape(key, True)}="{safestring_escape(value, True)}"'
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
