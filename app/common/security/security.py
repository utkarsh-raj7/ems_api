import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jwt.exceptions import ExpiredSignatureError, PyJWTError
from app.common.error.custom_error import CryptographyException, TokenExpiredException, UnauthorizedException
from app.common.config.config import settings
from app.common.logger.logger import get_logger
from app.common.constant.error_code import ErrorCode

logger = get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def get_password_hash(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.critical(f"Cryptography failure during hashing: {e}")
        raise CryptographyException(
            message="Failed to process credentials.",
            error_code=ErrorCode.CRYPTO_FAILURE
        )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.critical(f"Cryptography failure during verification: {e}")
        raise CryptographyException(
            message="Failed to verify credentials.",
            error_code=ErrorCode.CRYPTO_FAILURE
        )


def create_access_token(email: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": email, "role": role, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except ExpiredSignatureError:
        raise TokenExpiredException(
            message="Your session has expired. Please log in again.",
            error_code=ErrorCode.TOKEN_EXPIRED
        )
    except PyJWTError as e:
        logger.warning(f"JWT validation failed: {e}")
        raise UnauthorizedException(
            message="Could not validate credentials.",
            error_code=ErrorCode.UNAUTHORIZED
        )