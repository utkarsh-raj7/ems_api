import uuid
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.common.errors.custom_errors import (
    DatabaseOperationError,
    ResourceNotFoundException,
    DuplicateEmailException
)

logger = logging.getLogger(__name__)

def add_exception_handlers(app: FastAPI):
    """Registers all global exception handlers to the FastAPI app"""
    @app.exception_handler(DatabaseOperationError)
    async def database_error_handler(request: Request, exc: DatabaseOperationError):
        error_id = uuid.uuid4()
        logger.error(f"ID: {error_id} | Database error: {exc.message} | PATH: {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "An unexpected error occured. Please try again later.",
                "reference_id": str(error_id)
            }
        )
    
    @app.exception_handler(ResourceNotFoundException)
    async def not_found_handler(request: Request, exc: ResourceNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content = {"detail" : "The requested resource could not be found."}
        )
    @app.exception_handler(DuplicateEmailException)
    async def conflict_handler(request: Request, exc: DuplicateEmailException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content = {"detail" : "This information is already registered in our system."}
        )