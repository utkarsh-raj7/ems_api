
from app.common.logger.logger import get_logger
from app.common.security.security import get_password_hash

logger = get_logger(__name__)

def _check_email_is_unique(self, email: str) -> None:
    try:
        existing = self.repository.get_by_email(email)
    except DatabaseOperationError as e:
        logger.error(f"Database lookup failed during email validation: {e}")
        raise EmployeeCreationError(f"Could not verify email uniqueness due to a system error")
    if existing:
        raise DuplicateEmailError(f"The email {email} is already in use")
    
def _generate_passwword_hash(self, password: str)-> None:
    try:
        return get_password_hash(data.password)
    except Exception as e:
        logger.critical(f"Crytography failure during user registration: {e}")
        raise EmployeeCreationError("Failed to securely process user credentials")
    
    
        