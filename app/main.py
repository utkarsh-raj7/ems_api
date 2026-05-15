from fastapi import FastAPI,status
from app.controller.employee_controller import router as employee_router
from app.controller.auth_controller import router as auth_router
from app.common.error.error_handler import register_error_handlers


app = FastAPI(
    title="Employee Management System",
    version="1.0.0"
)

register_error_handlers(app)

app.include_router(auth_router)
app.include_router(employee_router)

@app.get("/health", tags=["Infrastructure"], status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy", "version": "1.0.0"}