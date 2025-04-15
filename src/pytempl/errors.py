from typing import Any


class ValidationError(Exception):
    def __init__(self, message: str, expected_type: str, loc: tuple, input_value: Any):
        super().__init__(message)
        self.error_list = [
            {
                "msg": message,
                "type": expected_type,
                "loc": loc,
                "input": input_value,
            }
        ]

    def errors(self):
        return self.error_list
