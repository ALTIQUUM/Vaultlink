from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class StockQuote(BaseModel):
    ticker: str
    price: Decimal
    currency: str = "USD"
    previous_close: Decimal | None = None
    change_percent: Decimal | None = None
    source: str
    captured_at: datetime


class StockProfile(BaseModel):
    ticker: str
    name: str
    sector: str | None
    market_cap: int | None
    pe_ratio: Decimal | None
    fifty_two_week_high: Decimal | None
    fifty_two_week_low: Decimal | None
    next_earnings_date: date | None


class NewsItem(BaseModel):
    ticker: str
    title: str
    url: str
    source: str
    published_at: datetime
    sentiment: float
