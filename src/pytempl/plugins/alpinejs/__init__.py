from typing import Any, Dict, Mapping, Sequence


def python_object_to_alpinejs_x_data(data: Dict[str, Any]) -> str:
    data_list = []
    for key, value in data.items():
        if isinstance(value, str):
            data_list.append(f"{key}: '{value}'")
        elif isinstance(value, bool):
            data_list.append(f"{key}: {str(value).lower()}")
        elif isinstance(value, (int, float, Sequence)):
            data_list.append(f"{key}: {value}")
        elif isinstance(value, Mapping):
            data_list.append(f"{key}: {python_object_to_alpinejs_x_data(value)}")
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    return f"{{{', '.join(data_list)}}}"


def python_object_to_alpinejs_x_init(data: Dict[str, Any]) -> str:
    data_list = []
    for key, value in data.items():
        if isinstance(value, str):
            data_list.append(f"{key} = '{value}'")
        elif isinstance(value, bool):
            data_list.append(f"{key} = {str(value).lower()}")
        elif isinstance(value, (int, float, Sequence)):
            data_list.append(f"{key} = {value}")
        elif isinstance(value, Mapping):
            data_list.append(f"{key} = {python_object_to_alpinejs_x_data(value)}")
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    return f"{', '.join(data_list)}"
