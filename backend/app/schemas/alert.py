from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.models.alert import AlertKind
from app.utils.validators import normalize_ticker


class AlertCreate(BaseModel):
    ticker: str
    kind: AlertKind
    threshold: Decimal = Field(gt=0)

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, value: str) -> str:
        return normalize_ticker(value)


class AlertRead(BaseModel):
    id: int
    ticker: str
    kind: AlertKind
    threshold: Decimal
    is_active: bool
    last_triggered_at: datetime | None

    model_config = {"from_attributes": True}


class NotificationRead(BaseModel):
    id: int
    title: str
    body: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
