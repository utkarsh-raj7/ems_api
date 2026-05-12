from pydantic import BaseModel, Field
from typing import List, Any
from app.application.model.employee_model import EmployeeResponse

class EmployeeQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=50, ge=1, le=100)
    name: str | None = None
    department: str | None = None
    
class PaginatedResponse(BaseModel):
    data: List[EmployeeResponse]
    total_count: int
    page: int
    limit: int