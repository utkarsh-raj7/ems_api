
from app.common.logger.logger import get_logger
from app.common.constant.error_code import ErrorCode
from app.common.security.security import get_password_hash
from app.repository.entity.employee_entity import EmployeeEntity
from app.repository.employee_repository import EmployeeRepository
from app.application.model.query_model import EmployeeQueryParams, PaginatedResponse
from app.application.model.employee_response_model import GetEmployeeResponseModel
from app.common.error.custom_error import EmployeeNotFoundException, DuplicateEmailException
from app.application.model.employee_request_model import CreateEmployeeRequestModel, UpdateEmployeeRequestModel

logger = get_logger(__name__)

class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository
        
    def create(self, data: CreateEmployeeRequestModel) -> GetEmployeeResponseModel:
        self._check_email_is_unique(data.email)
        hashed_password = get_password_hash(data.password)
        entity = self.repository.create(data, hashed_password)
        return GetEmployeeResponseModel.model_validate(entity)
    
    def get_by_id(self, id: int):
        entity = self._get_existing_employee(id)  
        return GetEmployeeResponseModel.model_validate(entity) 
    
    def list(self, params: EmployeeQueryParams) -> PaginatedResponse:
        offset = (params.page - 1)* params.limit
        results, total = self.repository.list(
            limit=params.limit,
            offset=offset,
            filters=params
        )
        
        return PaginatedResponse( 
            data=[GetEmployeeResponseModel.model_validate(e) for e in results],
            total_count=total,
            page=params.page,
            limit=params.limit
        )
    
    def update(self, id: int, data: UpdateEmployeeRequestModel, current_user: EmployeeEntity) -> None:
        existing_employee = self._get_existing_employee(id)
        if data.email and data.email != existing_employee.email:
            self._ensure_email_is_unique(data.email)
        self.repository.update(id, data, current_user.email)
        
    
    def delete(self, id: int) -> None:
        self.get_by_id(id)
        self.repository.delete(id)
            
            
    def _get_existing_employee(self, id: int):
        entity = self.repository.get_by_id(id)
        if not entity:
            raise EmployeeNotFoundException(
                message = f"Employee {id} not found.",
                error_code=ErrorCode.EMPLOYEE_NOT_FOUND
            )
        return entity
    
    
    def _ensure_email_is_unique(self, email: str):
        return self.repository.get_by_email(email)
    
    
    def _check_email_is_unique(self, email: str) -> None:
        if self.repository.get_by_email(email):
            raise DuplicateEmailException(
                message=f"The email {email} is already in use.",
                error_code=ErrorCode.DUPLICATE_EMAIL
            )  
            
        