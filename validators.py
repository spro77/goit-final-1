import re
from typing import Optional


def length_validator(value: str) -> Optional[str]:
    if len(value) == 0:
        raise ValueError('Value is too short, need more than 0 symbol')
    else:
        return value


def phone_number_validator(pattern, number: str) -> Optional[str]:
    if re.fullmatch(pattern, number.strip()):
        return number
    else:
        raise ValueError('The "phone number" field must contain 10 digits')


def email_validator(pattern: str, email: str) -> str:
    if re.fullmatch(pattern, email.strip()):
        return email.strip()
    else:
        raise ValueError("Invalid email format.")
