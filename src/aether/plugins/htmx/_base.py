from typing import Literal, NotRequired

from aether.base import BaseAttribute


class HTMXAttributes(BaseAttribute):
    hx_boost: NotRequired[Literal["true"]]
    hx_confirm: NotRequired[str]
    hx_delete: NotRequired[str]
    hx_disable: NotRequired[bool]
    hx_disabled_elt: NotRequired[Literal["this", "next", "previous"] | str]
    hx_disinherit: NotRequired[Literal["*"] | str]
    hx_encoding: NotRequired[str]
    hx_ext: NotRequired[str]
    hx_get: NotRequired[str]
    hx_headers: NotRequired[str]
    hx_history: NotRequired[Literal["false"]]
    hx_history_elt: NotRequired[bool]
    hx_include: NotRequired[Literal["this", "next", "previous"] | str]
    hx_indicator: NotRequired[str]
    hx_inherit: NotRequired[str]
    # 'hx_on*' is bit complicated to implement hence ignored
    hx_params: NotRequired[Literal["*", "none"] | str]
    hx_patch: NotRequired[str]
    hx_preserve: NotRequired[bool]
    hx_post: NotRequired[str]
    hx_prompt: NotRequired[str]
    hx_push_url: NotRequired[Literal["true", "false"] | str]
    hx_put: NotRequired[str]
    hx_replace_url: NotRequired[Literal["true", "false"] | str]
    hx_request: NotRequired[str]
    hx_select: NotRequired[str]
    hx_select_oob: NotRequired[str]
    hx_swap: NotRequired[
        Literal[
            "innerHTML",
            "outerHTML",
            "textContent",
            "beforebegin",
            "afterbegin",
            "beforeend",
            "afterend",
            "delete",
            "none",
        ]
        | str
    ]
    hx_swap_oob: NotRequired[Literal["true"] | str]
    hx_sync: NotRequired[str]
    hx_target: NotRequired[Literal["this", "next", "previous"] | str]
    hx_trigger: NotRequired[str]
    hx_validate: NotRequired[Literal["true"]]
    hx_vals: NotRequired[str]
