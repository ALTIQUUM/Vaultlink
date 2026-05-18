from fastapi import APIRouter, Depends
from redis import Redis

from app.api.dependencies import current_user, redis_client
from app.schemas.stock import StockProfile, StockQuote
from app.services.stock_service import StockService

router = APIRouter(
    prefix="/stocks", tags=["stocks"], dependencies=[Depends(current_user)]
)


@router.get("/{ticker}/quote", response_model=StockQuote)
def quote(ticker: str, redis: Redis = Depends(redis_client)) -> StockQuote:
    return StockService(redis).quote(ticker)


@router.get("/{ticker}/profile", response_model=StockProfile)
def profile(ticker: str, redis: Redis = Depends(redis_client)) -> StockProfile:
    return StockService(redis).profile(ticker)
