from decimal import Decimal

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import current_user
from app.services.screener_service import ScreenerFilter, ScreenerService

router = APIRouter(prefix="/screener", tags=["screener"], dependencies=[Depends(current_user)])


@router.get("")
def screen(
    tickers: list[str] = Query(default=["AAPL", "MSFT", "NVDA", "JPM", "GS"]),
    sector: str | None = None,
    min_market_cap: int | None = None,
    max_pe_ratio: Decimal | None = None,
    min_volume: int | None = None,
) -> list[dict[str, object]]:
    return ScreenerService().screen(tickers, ScreenerFilter(sector, min_market_cap, max_pe_ratio, min_volume))
