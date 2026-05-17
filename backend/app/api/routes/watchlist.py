from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import current_user
from app.core.database import get_db
from app.models.user import User
from app.models.watchlist import WatchlistItem
from app.utils.validators import normalize_ticker

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.get("")
def list_watchlist(user: User = Depends(current_user)) -> list[str]:
    return [item.ticker for item in user.watchlist_items]


@router.post("/{ticker}", status_code=status.HTTP_201_CREATED)
def add(ticker: str, user: User = Depends(current_user), db: Session = Depends(get_db)) -> dict[str, str]:
    symbol = normalize_ticker(ticker)
    exists = db.scalar(select(WatchlistItem).where(WatchlistItem.user_id == user.id, WatchlistItem.ticker == symbol))
    if not exists:
        db.add(WatchlistItem(user_id=user.id, ticker=symbol))
        db.commit()
    return {"ticker": symbol}


@router.delete("/{ticker}", status_code=status.HTTP_204_NO_CONTENT)
def remove(ticker: str, user: User = Depends(current_user), db: Session = Depends(get_db)) -> None:
    symbol = normalize_ticker(ticker)
    item = db.scalar(select(WatchlistItem).where(WatchlistItem.user_id == user.id, WatchlistItem.ticker == symbol))
    if item:
        db.delete(item)
        db.commit()
