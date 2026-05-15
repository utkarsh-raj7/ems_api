from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class GetEmployeeResponseModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    department: str
    role: str
    
    created_at: datetime
    modified_at: datetime | None = None
    created_by: str | None = None
    modified_by: str | None = None
    
    model_config = ConfigDict(from_attributes=True)