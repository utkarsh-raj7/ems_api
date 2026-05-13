from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.controller import employee_controller, auth_controller
from app.common.errors.error_handlers import add_exception_handlers
from app.common.logger.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Employee Management System",
    version="1.0.0"
)

add_exception_handlers(app)

app.include_router(auth_controller.router)
app.include_router(employee_controller.router)

@app.get("/health", tags=["Infrastructure"], status_code=200)
def health_check():
    return {"status": "healthy", "version": "1.0.0"}