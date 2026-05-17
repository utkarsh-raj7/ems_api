import re
from typing import Any
from app.common.error.custom_error import InvalidInputError
from app.common.constant.error_code import ErrorCode

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
        raise InvalidInputError(message="Invalid phone number format.", error_code=ErrorCode.INVALID_PHONE)
    return value

def validate_password_complexity(v: str) -> str:
    if not re.search(r"[A-Z]", v):
        raise InvalidInputError(message="Password must contain at least one uppercase letter.", error_code=ErrorCode.INVALID_PASSWORD)
    if not re.search(r"\d", v):
        raise InvalidInputError(message= "Password must contain at least one number.", error_code=ErrorCode.INVALID_PASSWORD)
    if not re.search(r"[@$!%*?&]", v):
        raise InvalidInputError(message= "Password must contain at least one special character (@, $, !, %, *, ?, &).", error_code=ErrorCode.INVALID_PASSWORD)
    if len(set(v)) < 4:
        raise InvalidInputError(message= "Password does not have enough unique characters.", error_code=ErrorCode.INVALID_PASSWORD)
    return v