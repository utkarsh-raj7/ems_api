from fastapi import APIRouter
from app.application.model.auth_request_model import LoginRequestModel
from app.dependencies import AuthServiceDep 
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(data: LoginRequestModel, service: AuthServiceDep):
    return service.login(data)