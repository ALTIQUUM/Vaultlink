from fastapi import APIRouter, Depends, status
from redis import Redis
from sqlalchemy.orm import Session

from app.api.dependencies import current_user, redis_client
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshRequest,
    RegisterRequest,
    TokenPair,
    UserRead,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
    redis: Redis = Depends(redis_client),
) -> User:
    return AuthService(db, redis).register(data)


@router.post("/login", response_model=TokenPair)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
    redis: Redis = Depends(redis_client),
) -> TokenPair:
    return AuthService(db, redis).login(data)


@router.post("/refresh", response_model=TokenPair)
def refresh(
    data: RefreshRequest,
    db: Session = Depends(get_db),
    redis: Redis = Depends(redis_client),
) -> TokenPair:
    return AuthService(db, redis).refresh(data.refresh_token)


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
def logout_all(
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
    redis: Redis = Depends(redis_client),
) -> None:
    AuthService(db, redis).logout_all(user.id)


@router.post("/password-reset/request", status_code=status.HTTP_202_ACCEPTED)
def password_reset_request(_: PasswordResetRequest) -> dict[str, str]:
    return {"status": "accepted"}


@router.post("/password-reset/confirm", status_code=status.HTTP_202_ACCEPTED)
def password_reset_confirm(_: PasswordResetConfirm) -> dict[str, str]:
    return {"status": "accepted"}
