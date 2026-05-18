from fastapi import APIRouter, Depends, Response, status
from redis import Redis
from sqlalchemy.orm import Session

from app.api.dependencies import current_user, redis_client
from app.core.database import get_db
from app.models.user import User
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PositionUpsert
from app.services.portfolio_service import PortfolioService
from app.services.stock_service import StockService

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


def service(db: Session, redis: Redis) -> PortfolioService:
    return PortfolioService(db, StockService(redis))


@router.post("", status_code=status.HTTP_201_CREATED)
def create_portfolio(
    data: PortfolioCreate,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
    redis: Redis = Depends(redis_client),
) -> dict[str, int]:
    portfolio = service(db, redis).create(user.id, data)
    return {"id": portfolio.id}


@router.put("/{portfolio_id}/positions")
def upsert_position(
    portfolio_id: int,
    data: PositionUpsert,
    db: Session = Depends(get_db),
    redis: Redis = Depends(redis_client),
    _: User = Depends(current_user),
) -> dict[str, int]:
    position = service(db, redis).upsert_position(portfolio_id, data)
    return {"id": position.id}


@router.get("/{portfolio_id}", response_model=PortfolioRead)
def summary(
    portfolio_id: int,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
    redis: Redis = Depends(redis_client),
) -> PortfolioRead:
    return service(db, redis).summary(portfolio_id, user.id)


@router.get("/{portfolio_id}/export.csv")
def export_csv(
    portfolio_id: int,
    user: User = Depends(current_user),
    db: Session = Depends(get_db),
    redis: Redis = Depends(redis_client),
) -> Response:
    return Response(
        service(db, redis).export_csv(portfolio_id, user.id), media_type="text/csv"
    )
