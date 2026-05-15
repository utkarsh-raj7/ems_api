import re
from typing import Any

def strip_all_strings(data: Any) -> Any:
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, str) and k!= "password":
                data[k] = v.strip()
    return data

def lowercase_email(value: str) -> str :
    return value.lower()

def validate_phone_format(value: str) -> str :
    if not re.match(r"^\+?[1-9]\d{9,14}$", value):
        raise ValueError("Invalid phone number format.")
    return value

def validate_password_complexity(v: str) -> str:
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain at least one uppercase letter.")
    if not re.search(r"\d", v):
        raise ValueError("Password must contain at least one number.")
    if not re.search(r"[@$!%*?&]", v):
        raise ValueError("Password must contain at least one special character (@, $, !, %, *, ?, &).")
    if len(set(v)) < 4:
        raise ValueError("Password does not have enough unique characters.")
    return v