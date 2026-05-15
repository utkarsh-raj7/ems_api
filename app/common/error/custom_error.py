class AppException(Exception):
    status_code: int = 500
    
    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code
        super().__init__(message)
        
        
# ---400 family ------------------------------------
class BadRequestException(AppException):
    status_code = 400

class InvalidCredentialsException(BadRequestException):
    pass

class ValidationException(BadRequestException):
    pass

# ---401 family ----------------------------------
class UnauthorizedException(AppException):
    status_code = 401
    
class TokenExpiredException(UnauthorizedException):
    pass

# ---404 family ----------------------------------
class NotFoundException(AppException):
    status_code = 404

class EmployeeNotFoundException(NotFoundException):
    pass

# ---409 family ----------------------------------

class ConflictException(AppException):
    status_code = 409
    
class DuplicateEmailException(ConflictException):
    pass

# ---500 family ----------------------------------
class InternalServerException(AppException):
    status_code = 500

class DatabaseOperationError(InternalServerException):
    pass

class CryptographyException(InternalServerException):
    pass
# ---403 family ----------------------------------
class ForbiddenException(AppException):
    status_code = 403

class PermissionDeniedError(ForbiddenException):
    pass
        