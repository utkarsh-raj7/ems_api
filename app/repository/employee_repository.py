from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import  SQLAlchemyError
from app.common.logger.logger import get_logger
from app.common.constant.error_code import ErrorCode
from app.repository.entity.employee_entity import EmployeeEntity
from app.common.error.db_decorator import _handle_db_exceptions
from app.common.error.custom_error import DatabaseOperationError
from app.application.model.query_model import EmployeeQueryParams, EmployeeFilters
from app.application.model.employee_request_model import CreateEmployeeRequestModel, UpdateEmployeeRequestModel

logger = get_logger(__name__)

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db
    
    @_handle_db_exceptions   
    def get_by_id(self, id: int) -> EmployeeEntity | None:
        return self.db.query(EmployeeEntity).filter(EmployeeEntity.id == id).first()
 
    @_handle_db_exceptions
    def get_by_email(self, email:str) -> EmployeeEntity | None:
        return self.db.query(EmployeeEntity).filter(EmployeeEntity.email == email).first()
                
    @_handle_db_exceptions
    def list(self, limit: int, offset: int, filters: EmployeeFilters):
        query = self.db.query(EmployeeEntity)
            
        if filters.name: 
            search_term = f"%{filters.name}%"
            query = query.filter(
                or_(
                    EmployeeEntity.first_name.ilike(search_term),
                    EmployeeEntity.last_name.ilike(search_term),
                    func.concat(EmployeeEntity.first_name, ' ', EmployeeEntity.last_name).ilike(search_term)
                )
            )
        if filters.department:
            query = query.filter(EmployeeEntity.department == filters.department)
        if filters.phone:
            query = query.filter(EmployeeEntity.phone == filters.phone)
        if filters.role:
            query = query.filter(EmployeeEntity.role == filters.role.value)
            
        total = query.count()

        results = query.offset(offset).limit(limit).all()
        
        return results, total
        
    @_handle_db_exceptions
    def create(self, data: CreateEmployeeRequestModel, hashed_password: str,  created_by: str | None) -> EmployeeEntity:
        entity = EmployeeEntity(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            role = data.role.value,
            password_hash=hashed_password,
            department=data.department,
            created_by = created_by
        )
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    @_handle_db_exceptions
    def update(self, id: int, data: UpdateEmployeeRequestModel, modified_by: str) -> None:
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)
        if not update_data:
            return
        if "role" in update_data and hasattr(update_data["role"], "value"):
            update_data["role"] = update_data["role"].value
        update_data["modified_by"] = modified_by
        self.db.query(EmployeeEntity).filter(EmployeeEntity.id == id).update(update_data) # type: ignore[arg-type]
        self.db.commit()
        self.db.commit()
        
    @_handle_db_exceptions
    def delete(self, id: int) -> None:
        self.db.query(EmployeeEntity).filter(EmployeeEntity.id == id).delete()
        self.db.commit()
                

            
        
    