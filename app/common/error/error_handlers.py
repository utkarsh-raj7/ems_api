from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.common.error.custom_error import AppException
from app.common.constant.error_code import ErrorCode
from app.common.logger.logger import get_logger

logger = get_logger(__name__)

def register_error_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppException)
    async def handle_app_exception(request: Request, exc: AppException):
        return JSONResponse(
            status_code= exc.status_code,
            content={
                "error_code": exc.error_code,
                "message": exc.message,
                "detail": None
            }
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content = {"error_code" : ErrorCode.VALIDATION_ERROR,
                       "message": "Invalid request data.",
                       "detail": exc.errors()
            }
        )
    @app.exception_handler(Exception)
    async def handle_unexpected(request: Request, exc: Exception):
        logger.critical(f"Unhandled exception at {request.method} {request.url.path}: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {"error_code": ErrorCode.INTERNAL_ERROR,
                       "message": "Something went wrong",
                       "detail" : None
            }
        )