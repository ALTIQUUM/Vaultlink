import logging
from datetime import datetime

import requests
from textblob import TextBlob

from app.core.config import get_settings
from app.schemas.stock import NewsItem
from app.utils.validators import normalize_ticker

logger = logging.getLogger(__name__)


class NewsService:
    def stock_news(self, ticker: str) -> list[NewsItem]:
        symbol = normalize_ticker(ticker)
        key = get_settings().news_api_key
        if not key:
            logger.info(
                "NEWS_API_KEY missing; returning empty news feed for %s", symbol
            )
            return []
        response = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": symbol,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 20,
                "apiKey": key,
            },
            timeout=15,
        )
        response.raise_for_status()
        items: list[NewsItem] = []
        for article in response.json().get("articles", []):
            title = article["title"]
            items.append(
                NewsItem(
                    ticker=symbol,
                    title=title,
                    url=article["url"],
                    source=article["source"]["name"],
                    published_at=datetime.fromisoformat(
                        article["publishedAt"].replace("Z", "+00:00")
                    ),
                    sentiment=float(TextBlob(title).sentiment.polarity),
                )
            )
        return items
