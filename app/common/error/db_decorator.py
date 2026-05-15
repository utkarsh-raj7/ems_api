from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from app.common.logger.logger import get_logger
from app.common.error.custom_error import DatabaseOperationError
from app.common.constant.error_code import ErrorCode

logger = get_logger(__name__)

def _handle_db_exceptions(func):
    """
    Decorator to wrap repository models.
    catches SQLAlchemy errors, rolls back the session, logs the errror, and raises a standard DatabaseOperationError.
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except SQLAlchemyError as e:
            if hasattr(self, 'db'): #self.db here the variable name in repository
                self.db.rollback()
            
            logger.error(f"Database error in repository method '{func.__name__}': {e}")
            raise DatabaseOperationError(
                message="A database operation failed.",
                error_code=ErrorCode.DATABASE_ERROR
            )
    return wrapper