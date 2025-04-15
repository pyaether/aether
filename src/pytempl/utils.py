from collections.abc import Callable
from typing import Any, TypedDict

from pydantic import TypeAdapter
from pydantic import ValidationError as PydanticValidationError

from .errors import ValidationError
from .safe_string import safestring_escape

ValidatorFunction = Callable[
    [TypedDict], None
]  # TODO: Change the `None` to Error-as-value Type if and when I create it


def validate_dictionary_data(
    cls,
    data: dict,
    default_values: dict | None = None,
    custom_validators: list[ValidatorFunction] | None = None,
):
    if default_values:
        data_with_defaults = {**default_values, **data}
    else:
        data_with_defaults = data

    type_adapter = TypeAdapter(cls)
    validated_data = type_adapter.validate_python(data_with_defaults)

    if custom_validators:
        for validator in custom_validators:
            validator(validated_data)

    return validated_data


def flatten_attributes(attributes: dict[str, Any]) -> str:
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


def format_validation_error_message(error: PydanticValidationError | ValidationError):
    formatted_errors = [
        f"`{' -> '.join(str(loc) for loc in err['loc'])}`: {err['msg']}. (type: '{err['type']}', input_type: '{type(err['input']).__name__}', input_value: '{err['input']}')"
        for err in error.errors()
    ]
    return "\n".join(formatted_errors)
