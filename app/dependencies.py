
from fastapi import Depends
from app.repository.database import db_pool
from app.repository.employee_repository import EmployeeRepository
from app.application.service.employee_service import EmployeeService

def get_employee_repository() -> EmployeeRepository:
    return EmployeeRepository(db_pool=db_pool)

def get_employee_service(
    repository: EmployeeRepository = Depends(get_employee_repository)
) -> EmployeeService:
    return EmployeeService(repository=repository)