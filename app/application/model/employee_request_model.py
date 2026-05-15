import re
from typing import Any
from app.common.constant.role import Role
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from app.application.model.validator_function import (
    strip_all_strings, 
    lowercase_email, 
    validate_password_complexity, 
    validate_phone_format)

class EmployeeBaseModel(BaseModel):
    
    @model_validator(mode="before")
    @classmethod
    def normalise_trailing_and_leading_spaces(cls, data: Any) -> Any:
        return strip_all_strings(data)
    
    @field_validator("email", mode="before", check_fields=False)
    @classmethod
    def lowercase(cls, value: str | None) -> str | None:
        return lowercase_email(value) if value else value

    @field_validator("phone", mode="before", check_fields=False)
    @classmethod
    def validate_phone_input(cls, value: str | None) -> str | None:
        return validate_phone_format(value) if value else value
        


class CreateEmployeeRequestModel(EmployeeBaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    phone: str
    department: str
    role: Role = Field(default=Role.STAFF)
    password: str = Field(..., min_length=12)
    
    @field_validator('password')
    @classmethod
    def validate_password_input(cls, value: str) -> str:
        return validate_password_complexity(value)
        
    
    
class UpdateEmployeeRequestModel(EmployeeBaseModel):
    first_name: str | None = Field(None, min_length=1, max_length=50)
    last_name: str | None = Field(None, min_length=1, max_length=50)
    email: EmailStr | None = None
    phone: str | None = None
    department: str | None = None
    role: Role | None = None
    