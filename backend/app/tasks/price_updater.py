import logging

from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.redis import get_redis
from app.models.watchlist import WatchlistItem
from app.services.stock_service import StockService
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.price_updater.refresh_watchlist_prices")
def refresh_watchlist_prices() -> int:
    redis = get_redis()
    service = StockService(redis)
    with SessionLocal() as db:
        tickers = sorted(set(db.scalars(select(WatchlistItem.ticker)).all()))
    for ticker in tickers:
        service.quote(ticker)
    logger.info("Refreshed %s watchlist quotes", len(tickers))
    return len(tickers)
