from fastapi import APIRouter, Depends, status
from redis import Redis
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import current_user, redis_client
from app.core.database import get_db
from app.models.alert import Alert
from app.models.user import User
from app.schemas.alert import AlertCreate, AlertRead, NotificationRead
from app.services.alert_service import AlertService
from app.services.stock_service import StockService

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertRead])
def list_alerts(user: User = Depends(current_user)) -> list[Alert]:
    return user.alerts


@router.post("", response_model=AlertRead, status_code=status.HTTP_201_CREATED)
def create_alert(data: AlertCreate, user: User = Depends(current_user), db: Session = Depends(get_db), redis: Redis = Depends(redis_client)) -> Alert:
    return AlertService(db, StockService(redis)).create(user.id, data)


@router.get("/notifications", response_model=list[NotificationRead])
def notifications(user: User = Depends(current_user)) -> list[object]:
    return user.notifications


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
def disable(alert_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)) -> None:
    alert = db.scalar(select(Alert).where(Alert.id == alert_id, Alert.user_id == user.id))
    if alert:
        alert.is_active = False
        db.commit()
