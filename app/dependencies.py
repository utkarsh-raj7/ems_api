
from typing import Annotated, List
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session #type =ignore


from app.common.constant.role import Role
from app.repository.database import get_db
from app.common.constant.error_code import ErrorCode
from app.common.error.custom_error import PermissionDeniedError, UnauthorizedException
from app.repository.employee_repository import EmployeeRepository
from app.application.service.employee_service import EmployeeService
from app.application.service.auth_service import AuthService
from app.repository.entity.employee_entity import EmployeeEntity
from app.common.security.security import decode_access_token

bearer_scheme = HTTPBearer()

def get_employee_repository(db: Annotated[Session, Depends(get_db)]) -> EmployeeRepository:
    return EmployeeRepository(db)

def get_employee_service(
    repository: Annotated[EmployeeRepository, Depends(get_employee_repository)]
) -> EmployeeService:
    return EmployeeService(repository)

def get_auth_service(
    repository: Annotated[EmployeeRepository, Depends(get_employee_repository)]
) -> AuthService:
    return AuthService(repository)

def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    repository: Annotated[EmployeeRepository, Depends(get_employee_repository)]
) -> EmployeeEntity:
    payload = decode_access_token(credentials.credentials)
    email = payload.get("sub")
    
    if not email:
        raise UnauthorizedException(message="Invalid token payload.", error_code=ErrorCode.INVALID_CREDENTIALS)
        
    employee = repository.get_by_email(email)
    if not employee:
        raise UnauthorizedException(message="User no longer exists.", error_code=ErrorCode.EMPLOYEE_NOT_FOUND)
        
    return employee

class RequireRole:
    def __init__(self, allowed_roles: List[Role]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: EmployeeEntity = Depends(get_current_user)) -> EmployeeEntity:
        if current_user.role not in [r.value for r in self.allowed_roles]:
            raise PermissionDeniedError(
                message="You do not have permission to perform this action.",
                error_code=ErrorCode.UNAUTHORIZED
            )
        return current_user

DatabaseDep = Annotated[Session, Depends(get_db)]
EmployeeServiceDep = Annotated[EmployeeService, Depends(get_employee_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
CurrentUser = Annotated[EmployeeEntity, Depends(get_current_user)]
AdminUser = Annotated[EmployeeEntity, Depends(RequireRole([Role.ADMIN]))]
ManagerUser = Annotated[EmployeeEntity, Depends(RequireRole([Role.ADMIN, Role.MANAGER]))]