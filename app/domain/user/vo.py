from dataclasses import dataclass

import email_validator


@dataclass(init=False, eq=True, frozen=True)
class Email:
    """
    Email Value Object
    """

    value: str

    def __init__(self, value: str):
        try:
            email_validator.validate_email(value, check_deliverability=False)
        except email_validator.EmailNotValidError as e:
            raise ValueError(f"邮箱格式不正确: {e}")
        else:
            object.__setattr__(self, "value", value)
