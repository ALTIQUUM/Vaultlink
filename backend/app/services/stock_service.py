import logging
from datetime import UTC, datetime
from decimal import Decimal

import requests
import yfinance as yf
from redis import Redis

from app.core.config import get_settings
from app.schemas.stock import StockProfile, StockQuote
from app.utils.cache import get_model, set_model
from app.utils.validators import normalize_ticker

logger = logging.getLogger(__name__)


class StockService:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    def quote(self, ticker: str) -> StockQuote:
        symbol = normalize_ticker(ticker)
        cache_key = f"quote:{symbol}"
        cached = get_model(self.redis, cache_key, StockQuote)
        if cached:
            return cached
        quote = self._from_yfinance(symbol) or self._from_alpha_vantage(symbol)
        set_model(self.redis, cache_key, quote, 300)
        logger.info("Fetched quote for %s from %s", symbol, quote.source)
        return quote

    def profile(self, ticker: str) -> StockProfile:
        symbol = normalize_ticker(ticker)
        info = yf.Ticker(symbol).get_info()
        return StockProfile(
            ticker=symbol,
            name=info.get("shortName") or symbol,
            sector=info.get("sector"),
            market_cap=info.get("marketCap"),
            pe_ratio=Decimal(str(info["trailingPE"])) if info.get("trailingPE") else None,
            fifty_two_week_high=Decimal(str(info["fiftyTwoWeekHigh"])) if info.get("fiftyTwoWeekHigh") else None,
            fifty_two_week_low=Decimal(str(info["fiftyTwoWeekLow"])) if info.get("fiftyTwoWeekLow") else None,
            next_earnings_date=None,
        )

    def _from_yfinance(self, ticker: str) -> StockQuote | None:
        try:
            fast = yf.Ticker(ticker).fast_info
            price = Decimal(str(fast["last_price"]))
            previous = Decimal(str(fast["previous_close"])) if fast.get("previous_close") else None
            change = ((price - previous) / previous * 100) if previous else None
            return StockQuote(ticker=ticker, price=price, previous_close=previous, change_percent=change, source="yfinance", captured_at=datetime.now(UTC))
        except Exception:
            logger.exception("yfinance quote failed for %s", ticker)
            return None

    def _from_alpha_vantage(self, ticker: str) -> StockQuote:
        key = get_settings().alpha_vantage_api_key
        if not key:
            raise RuntimeError("ALPHA_VANTAGE_API_KEY is required when yfinance fails")
        response = requests.get(
            "https://www.alphavantage.co/query",
            params={"function": "GLOBAL_QUOTE", "symbol": ticker, "apikey": key},
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()["Global Quote"]
        return StockQuote(
            ticker=ticker,
            price=Decimal(data["05. price"]),
            previous_close=Decimal(data["08. previous close"]),
            change_percent=Decimal(data["10. change percent"].rstrip("%")),
            source="alpha_vantage",
            captured_at=datetime.now(UTC),
        )
