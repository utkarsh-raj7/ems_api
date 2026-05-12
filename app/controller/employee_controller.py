from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import get_employee_service
from app.application.service.employee_service import EmployeeService
from app.application.model.employee_model import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.application.model.query_model import EmployeeQueryParams, PaginatedResponse

router = APIRouter(prefix ="/employee", tags=["Employee"])
    
@router.get("/", response_model=PaginatedResponse, status_code=status.HTTP_200_OK)
def list_all(
    params: EmployeeQueryParams = Depends(),
    service: EmployeeService = Depends(get_employee_service)
):
    return service.list(params=params)

@router.get("/{id}", response_model=EmployeeResponse, status_code=status.HTTP_200_OK)
def get_by_id(
    id: int,
    service: EmployeeService = Depends(get_employee_service)
):
    return service.get_by_id(id=id)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    request_data: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service)
):
    new_id = service.create(data=request_data)
    return {"message": "Employee created successfully", "id": new_id}

@router.put("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
def update(
    id : int,
    request_data: EmployeeUpdate,
    service: EmployeeService = Depends(get_employee_service)
):
    service.update(id=id, data=request_data)
    return {"message": f"Employee {id} updated successfully"}

@router.delete("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
def delete(
    id: int,
    service: EmployeeService = Depends(get_employee_service)
):
    service.delete(id=id)
    return {"message": f"Employee {id} deleted successfully"}

