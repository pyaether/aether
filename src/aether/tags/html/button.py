from typing import Literal, NotRequired, Self

from pydantic import ValidationError as PydanticValidationError

from aether.errors import ValidationError
from aether.utils import (
    ValidatorFunction,
    format_validation_error_message,
    validate_dictionary_data,
)

from ._base import BaseHTMLElement, GlobalHTMLAttributes, HTMLContentCategories

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class ButtonAttributes(GlobalHTMLAttributes):
    disabled: NotRequired[bool]
    form: NotRequired[str]
    formaction: NotRequired[
        str
    ]  # the form action URL. Overrides the action attribute of the button's form owner.
    formenctype: NotRequired[
        Literal[
            "application/x-www-form-urlencoded", "multipart/form-data", "text/plain"
        ]
    ]  # overrides the `enctype` attribute of the button's form owner.
    formmethod: NotRequired[
        Literal["get", "post", "dialog"]
    ]  # overrides the `method` attribute of the button's form owner.
    formnovalidate: NotRequired[
        bool
    ]  # overrides the `novalidate` attribute of the button's form owner.
    formtarget: NotRequired[Literal["_self", "_blank", "_parent", "_top"]]
    name: NotRequired[str]
    popovertarget: NotRequired[str]
    popovertargetaction: NotRequired[Literal["hide", "show", "toggle"]]
    type: Literal["button", "submit", "reset"]
    value: NotRequired[str]

    @classmethod
    def validate(
        cls,
        data: dict,
        default_values: dict | None = None,
        custom_validators: list[ValidatorFunction] | None = None,
    ) -> Self:
        return validate_dictionary_data(cls, data, default_values, custom_validators)

    @classmethod
    def set_defaults(cls) -> dict:
        return {"type": "button"}


def _validate_form_conditional(data: ButtonAttributes) -> None:
    if data["type"] == "button":
        if data.get("formaction") is not None:
            raise ValidationError(
                message="`Formaction` is not allowed when `type` is `button`",
                expected_type="none_required",
                loc=("formaction",),
                input_value=data["formaction"],
            )

        if data.get("formenctype") is not None:
            raise ValidationError(
                message="`Formenctype` is not allowed when `type` is `button`",
                expected_type="none_required",
                loc=("formenctype",),
                input_value=data["formenctype"],
            )

        if data.get("formmethod") is not None:
            raise ValidationError(
                message="`Formmethod` is not allowed when `type` is `button`",
                expected_type="none_required",
                loc=("formmethod",),
                input_value=data["formmethod"],
            )

        if data.get("formnovalidate") is not None:
            raise ValidationError(
                message="`Formnovalidate` is not allowed when `type` is `button`",
                expected_type="none_required",
                loc=("Formnovalidate",),
                input_value=data["Formnovalidate"],
            )

        if data.get("formtarget") is not None:
            raise ValidationError(
                message="`Formtarget` is not allowed when `type` is `button`",
                expected_type="none_required",
                loc=("formtarget",),
                input_value=data["formtarget"],
            )


class Button(BaseHTMLElement):
    tag_name = "button"
    have_children = True
    content_category = (
        HTMLContentCategories.FLOW,
        HTMLContentCategories.PHRASING,
        HTMLContentCategories.INTERACTIVE,
        HTMLContentCategories.FORM_ASSOCIATED,
        HTMLContentCategories.PALPABLE,
    )

    def __init__(self, **attributes: Unpack[ButtonAttributes]):
        try:
            validated_attributes = ButtonAttributes.validate(
                attributes,
                ButtonAttributes.set_defaults(),
                [_validate_form_conditional],
            )

            if (
                validated_attributes["type"] != "button"
                and validated_attributes.get("formtarget") is None
            ):
                validated_attributes["formtarget"] = "_self"

            if (
                validated_attributes.get("popovertarget") is not None
                and validated_attributes.get("popovertargetaction") is None
            ):
                validated_attributes["popovertargetaction"] = "toggle"

        except (ValidationError, PydanticValidationError) as err:
            raise ValueError(format_validation_error_message(err))

        super().__init__(**validated_attributes)
