from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import get_employee_service
from app.application.service.employee_service import EmployeeService
from app.common.security.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: EmployeeService = Depends(get_employee_service)
):
    employee = service.get_by_email(email=form_data.username)
    
    if not employee or not verify_password(plain_password=form_data.password, hashed_password=employee["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": str(employee["id"])})
    
    return {"access_token": access_token, "token_type": "bearer"}