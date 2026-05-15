from app.repository.employee_repository import EmployeeRepository
from app.application.model.auth_request_model import LoginRequestModel, TokenResponseModel
from app.common.security.security import verify_password, create_access_token
from app.common.error.custom_error import InvalidCredentialsException
from app.common.constant.error_code import ErrorCode


class AuthService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    def login(self, data: LoginRequestModel) -> TokenResponseModel:
        employee = self.repository.get_by_email(email=data.username)
        if not employee or not verify_password(data.password, employee.password_hash):
            raise InvalidCredentialsException(
                message="Invalid username or password.",
                error_code=ErrorCode.INVALID_CREDENTIALS
            )
        token = create_access_token(employee.email, employee.role)
        return TokenResponseModel(access_token=token)