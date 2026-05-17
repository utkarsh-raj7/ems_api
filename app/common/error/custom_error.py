from fastapi import status
from app.common.constant.error_code import ErrorCode
class AppException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code
        super().__init__(message)
        
        
# ---400 family ------------------------------------
class BadRequestException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST

class InvalidCredentialsException(BadRequestException):
    pass

class ValidationException(BadRequestException):
    pass

# ---401 family ----------------------------------
class UnauthorizedException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    
class TokenExpiredException(UnauthorizedException):
    pass

# ---404 family ----------------------------------
class NotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND

class EmployeeNotFoundException(NotFoundException):
    pass

# ---409 family ----------------------------------

class ConflictException(AppException):
    status_code = status.HTTP_409_CONFLICT
    
class DuplicateEmailException(ConflictException):
    pass

# ---500 family ----------------------------------
class InternalServerException(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

class DatabaseOperationError(InternalServerException):
    pass

class CryptographyException(InternalServerException):
    pass
# ---403 family ----------------------------------
class ForbiddenException(AppException):
    status_code = status.HTTP_403_FORBIDDEN

class PermissionDeniedError(ForbiddenException):
    pass
        
# ---422 family ----------------------------------
class InvalidInputError(AppException):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    
    
