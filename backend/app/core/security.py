from datetime import UTC, datetime, timedelta
from secrets import token_urlsafe
from uuid import uuid4

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_token(
    subject: str, token_type: str, expires_delta: timedelta, session_id: str
) -> str:
    settings = get_settings()
    now = datetime.now(UTC)
    payload = {
        "sub": subject,
        "typ": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
        "jti": str(uuid4()),
        "sid": session_id,
    }
    return jwt.encode(
        payload, settings.resolved_jwt_secret, algorithm=settings.jwt_algorithm
    )


def decode_token(token: str) -> dict[str, object]:
    settings = get_settings()
    try:
        return jwt.decode(
            token, settings.resolved_jwt_secret, algorithms=[settings.jwt_algorithm]
        )
    except JWTError as exc:
        raise ValueError("Invalid or expired token") from exc


def generate_otp() -> str:
    return f"{int.from_bytes(token_urlsafe(6).encode(), 'little') % 1000000:06d}"


def generate_session_id() -> str:
    return token_urlsafe(32)
