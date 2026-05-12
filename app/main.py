from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.controller import employee_controller, auth_controller
from app.common.errors.error_handlers import DatabaseOperationError
from app.common.logger.logger import get_logger

logger = get_logger(__name__)
app = FastAPI()
@app.exception_handler(DatabaseOperationError)
async def database_eror_handler(request: Request, exc: DatabaseOperationError):
    logger.error(f"Global handler caught a database error: {exc.message}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": exc.message
        },
    )
app.include_router(employee_controller.router)
app.include_router(auth_controller.router)