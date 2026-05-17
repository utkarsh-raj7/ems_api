from pydantic import BaseModel, Field
from typing import List, Any
from app.application.model.employee_response_model import GetEmployeeResponseModel
from app.common.constant.role import Role

class EmployeeQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=50, ge=1, le=100)
    name: str | None = None
    department: str | None = None
    phone: str | None = None
    role: Role | None = None
    
    
class PaginatedResponse(BaseModel):
    data: List[GetEmployeeResponseModel]
    total_count: int
    page: int
    limit: int
    
class EmployeeFilters(BaseModel):
    name: str | None = None
    department: str | None = None
    phone: str | None = None
    role: Role | None = None