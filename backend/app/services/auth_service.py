import logging
from datetime import timedelta

from redis import Redis
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import conflict, unauthorized
from app.core.security import create_token, decode_token, generate_otp, generate_session_id, hash_password, verify_password
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenPair
from app.services.email_service import EmailService

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, db: Session, redis: Redis) -> None:
        self.db = db
        self.redis = redis

    def register(self, data: RegisterRequest) -> User:
        existing = self.db.scalar(select(User).where(User.email == data.email.lower()))
        if existing:
            raise conflict("Email is already registered")
        user = User(email=data.email.lower(), full_name=data.full_name, hashed_password=hash_password(data.password))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        otp = generate_otp()
        self.redis.setex(f"verify:{user.email}", 900, otp)
        EmailService().send(user.email, "Verify your VAULTLINK account", f"Your verification code is {otp}.")
        logger.info("Registered user %s", user.email)
        return user

    def login(self, data: LoginRequest) -> TokenPair:
        user = self.db.scalar(select(User).where(User.email == data.email.lower()))
        if not user or not user.hashed_password or not verify_password(data.password, user.hashed_password):
            raise unauthorized("Invalid email or password")
        if not user.is_active:
            raise unauthorized("Account is disabled")
        return self._issue_tokens(user)

    def refresh(self, refresh_token: str) -> TokenPair:
        payload = decode_token(refresh_token)
        if payload.get("typ") != "refresh":
            raise unauthorized("Refresh token required")
        session_id = str(payload["sid"])
        user_id = str(payload["sub"])
        stored = self.redis.get(f"session:{user_id}:{session_id}")
        if stored != refresh_token:
            raise unauthorized("Refresh token has been rotated")
        self.redis.delete(f"session:{user_id}:{session_id}")
        user = self.db.get(User, int(user_id))
        if not user or not user.is_active:
            raise unauthorized("Account is disabled")
        return self._issue_tokens(user)

    def logout_all(self, user_id: int) -> None:
        for key in self.redis.scan_iter(f"session:{user_id}:*"):
            self.redis.delete(key)
        logger.info("Revoked all sessions for user_id=%s", user_id)

    def _issue_tokens(self, user: User) -> TokenPair:
        settings = get_settings()
        session_id = generate_session_id()
        access = create_token(str(user.id), "access", timedelta(minutes=settings.access_token_expire_minutes), session_id)
        refresh = create_token(str(user.id), "refresh", timedelta(days=settings.refresh_token_expire_days), session_id)
        self.redis.setex(f"session:{user.id}:{session_id}", settings.refresh_token_expire_days * 86400, refresh)
        logger.info("Issued token pair for user_id=%s", user.id)
        return TokenPair(access_token=access, refresh_token=refresh)
