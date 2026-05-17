import psutil
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.dependencies import admin_user
from app.core.database import get_db
from app.models.portfolio import Portfolio
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(admin_user)])


@router.get("/health")
def health(db: Session = Depends(get_db)) -> dict[str, object]:
    return {
        "users": db.scalar(select(func.count(User.id))),
        "active_portfolios": db.scalar(select(func.count(Portfolio.id))),
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
    }


@router.post("/users/{user_id}/ban")
def ban_user(user_id: int, db: Session = Depends(get_db)) -> dict[str, bool]:
    user = db.get(User, user_id)
    if user:
        user.is_active = False
        db.commit()
    return {"banned": bool(user)}
