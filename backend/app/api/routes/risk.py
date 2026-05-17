from fastapi import APIRouter, Depends, Query

from app.api.dependencies import current_user
from app.schemas.risk import PortfolioRisk
from app.services.risk_engine import RiskEngine

router = APIRouter(prefix="/risk", tags=["risk"], dependencies=[Depends(current_user)])


@router.get("", response_model=PortfolioRisk)
def analyze(tickers: list[str] = Query(min_length=1)) -> PortfolioRisk:
    return RiskEngine().analyze(tickers)
