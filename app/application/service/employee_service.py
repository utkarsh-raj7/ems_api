from app.common.logger.logger import get_logger
from app.common.security.security import get_password_hash
from app.common.errors.custom_errors import ResourceNotFoundException, DuplicateEmailException
from app.repository.employee_repository import EmployeeRepository
from app.application.model.query_model import EmployeeQueryParams
from app.application.model.employee_model import EmployeeCreate, EmployeeUpdate

logger = get_logger(__name__)

class EmployeeService:
    def __init__(self, *, repository: EmployeeRepository):
        self.repository = repository
        
    def create(self, *, data: EmployeeCreate) -> int:
        existing = self.repository.get_by_email(email=data.email)
        if existing:
            raise DuplicateEmailException(message="This email is already registered.")
        try:
            hashed_password = get_password_hash(data.password)
        except Exception as e:
            logger.critical(f"Crytography failure during user registration: {e}")
            raise Exception("Internal server error during registration.")
    
        return self.repository.create(data=data, hashed_password=hashed_password)
    
        
    def list(self, *,  params: EmployeeQueryParams):
        offset = (params.page - 1)* params.limit
        active_filters = params.model_dump(exclude_none=True, exclude={"page","limit"})
        data, total_count = self.repository.list(limit=params.limit, offset=offset, filters=active_filters)
        
        return {
            "data": data,
            "total_count" : total_count,
            "page": params.page,
            "limit": params.limit
        }
    
    
    def get_by_id(self, *, id: int):
        employee = self.repository.get_by_id(id=id)
        
        if not employee:
            raise ResourceNotFoundException(message = f"Employee with ID {id} not found.")

        return employee
    
    
    def get_by_email(self, *, email: str):
        return self.repository.get_by_email(email=email)
         
    
    def update(self, *, id: int, data: EmployeeUpdate):
        self.get_by_id(id=id)
        self.repository.update(id=id, data=data)
        
    
    def delete(self, *, id: int):
        self.get_by_id(id=id)
        self.repository.delete(id=id)
            
            
        