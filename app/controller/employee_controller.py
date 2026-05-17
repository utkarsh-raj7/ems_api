from fastapi import APIRouter, Depends, status
from app.dependencies import EmployeeServiceDep, CurrentUser, AdminUser, ManagerUser
from app.application.model.employee_request_model import CreateEmployeeRequestModel, UpdateEmployeeRequestModel
from app.application.model.query_model import EmployeeQueryParams, PaginatedResponse
from app.application.model.employee_response_model import GetEmployeeResponseModel

router = APIRouter(prefix ="/employee", tags=["Employee"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create(
    data: CreateEmployeeRequestModel,
    service: EmployeeServiceDep,
    current_user: AdminUser ):
    return service.create(data, current_user)

@router.get("/", response_model=PaginatedResponse, status_code=status.HTTP_200_OK)
def list(
    service: EmployeeServiceDep,
    current_user: CurrentUser,
    params: EmployeeQueryParams = Depends()
):
    return service.list(params)

@router.get("/{id}", response_model=GetEmployeeResponseModel, status_code=status.HTTP_200_OK)
def get_by_id(
    id: int,
    service: EmployeeServiceDep,
    current_user: CurrentUser ):
    return service.get_by_id(id)
    

@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update(
    id : int,
    data: UpdateEmployeeRequestModel,
    service: EmployeeServiceDep,
    current_user: ManagerUser
):
    service.update(id, data, current_user)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    service: EmployeeServiceDep,
    current_user: AdminUser
):

    service.delete(id)