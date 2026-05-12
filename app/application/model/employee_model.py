import re
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator

class Role(str, Enum):
    ADMIN   = "admin"
    MANAGER = "manager"
    STAFF   = "staff"

class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    department: str
    role: Role = Role.STAFF
    
class EmployeeCreate(EmployeeBase):
    password: str = Field(..., min_length=12)
    
    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number.")
        if not re.search(r"[@$!%*?&]", v):
            raise ValueError("Password must contain at least one special character (@, $, !, %, *, ?, &).")
        if len(set(v)) < 4:
            raise ValueError("Password does not have enough unique characters.")
        return v
            

class EmployeeResponse(EmployeeBase):
    id: int
    
    class Config:
        from_attributes = True
        
class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    department: str | None = None
    role: Role | None = None
