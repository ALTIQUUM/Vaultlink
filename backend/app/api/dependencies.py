from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis import Redis
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import forbidden, unauthorized
from app.core.redis import get_redis
from app.core.security import decode_token
from app.models.user import User, UserRole

bearer = HTTPBearer(auto_error=False)


def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)) -> User:
    if credentials is None:
        raise unauthorized()
    try:
        payload = decode_token(credentials.credentials)
    except ValueError:
        raise unauthorized("Invalid token")
    if payload.get("typ") != "access":
        raise unauthorized("Access token required")
    user = db.get(User, int(str(payload["sub"])))
    if not user or not user.is_active:
        raise unauthorized("Inactive account")
    return user


def admin_user(user: User = Depends(current_user)) -> User:
    if user.role != UserRole.ADMIN:
        raise forbidden("Admin role required")
    return user


def redis_client() -> Redis:
    return get_redis()
