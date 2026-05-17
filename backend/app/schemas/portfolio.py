from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from app.utils.validators import normalize_ticker


class PortfolioCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    currency: str = Field(default="USD", min_length=3, max_length=3)


class PositionUpsert(BaseModel):
    ticker: str
    quantity: Decimal = Field(gt=0)
    average_cost: Decimal = Field(gt=0)
    opened_at: date

    @field_validator("ticker")
    @classmethod
    def validate_ticker(cls, value: str) -> str:
        return normalize_ticker(value)


class PositionRead(BaseModel):
    id: int
    ticker: str
    quantity: Decimal
    average_cost: Decimal
    current_price: Decimal
    market_value: Decimal
    unrealized_gain: Decimal
    realized_gain: Decimal


class PortfolioRead(BaseModel):
    id: int
    name: str
    currency: str
    total_value: Decimal
    total_cost: Decimal
    unrealized_gain: Decimal
    realized_gain: Decimal
    positions: list[PositionRead]


class PerformancePoint(BaseModel):
    date: date
    value: Decimal
