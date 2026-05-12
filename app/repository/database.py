import mysql.connector.pooling
from app.common.config.config import settings
from app.common.logger.logger import get_logger

logger = get_logger(__name__)

try:
    db_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="employee_pool",
        pool_size=settings.db_pool_size,
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name
    )
    logger.info("Database connection pool initialized successfully.")
except Exception as e:
    logger.error(f"FATAL: Could not initialize database pool: {e}")
    raise e