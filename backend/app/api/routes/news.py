from fastapi import APIRouter, Depends

from app.api.dependencies import current_user
from app.schemas.stock import NewsItem
from app.services.news_service import NewsService

router = APIRouter(prefix="/news", tags=["news"], dependencies=[Depends(current_user)])


@router.get("/{ticker}", response_model=list[NewsItem])
def stock_news(ticker: str) -> list[NewsItem]:
    return NewsService().stock_news(ticker)
