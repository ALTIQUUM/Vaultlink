import csv
from decimal import Decimal
from io import StringIO

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import not_found
from app.models.portfolio import Portfolio
from app.models.position import Position
from app.schemas.portfolio import PortfolioCreate, PortfolioRead, PositionRead, PositionUpsert
from app.services.stock_service import StockService


class PortfolioService:
    def __init__(self, db: Session, stocks: StockService) -> None:
        self.db = db
        self.stocks = stocks

    def create(self, user_id: int, data: PortfolioCreate) -> Portfolio:
        portfolio = Portfolio(user_id=user_id, name=data.name, currency=data.currency.upper())
        self.db.add(portfolio)
        self.db.commit()
        self.db.refresh(portfolio)
        return portfolio

    def upsert_position(self, portfolio_id: int, data: PositionUpsert) -> Position:
        position = self.db.scalar(select(Position).where(Position.portfolio_id == portfolio_id, Position.ticker == data.ticker))
        if position:
            position.quantity = data.quantity
            position.average_cost = data.average_cost
            position.opened_at = data.opened_at
        else:
            position = Position(portfolio_id=portfolio_id, ticker=data.ticker, quantity=data.quantity, average_cost=data.average_cost, opened_at=data.opened_at)
            self.db.add(position)
        self.db.commit()
        self.db.refresh(position)
        return position

    def summary(self, portfolio_id: int, user_id: int) -> PortfolioRead:
        portfolio = self.db.scalar(select(Portfolio).where(Portfolio.id == portfolio_id, Portfolio.user_id == user_id))
        if not portfolio:
            raise not_found("Portfolio not found")
        rows: list[PositionRead] = []
        total_value = Decimal("0")
        total_cost = Decimal("0")
        realized = Decimal("0")
        for position in portfolio.positions:
            quote = self.stocks.quote(position.ticker)
            market_value = position.quantity * quote.price
            cost = position.quantity * position.average_cost
            total_value += market_value
            total_cost += cost
            realized += position.realized_gain
            rows.append(PositionRead(id=position.id, ticker=position.ticker, quantity=position.quantity, average_cost=position.average_cost, current_price=quote.price, market_value=market_value, unrealized_gain=market_value - cost, realized_gain=position.realized_gain))
        return PortfolioRead(id=portfolio.id, name=portfolio.name, currency=portfolio.currency, total_value=total_value, total_cost=total_cost, unrealized_gain=total_value - total_cost, realized_gain=realized, positions=rows)

    def export_csv(self, portfolio_id: int, user_id: int) -> str:
        summary = self.summary(portfolio_id, user_id)
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(["ticker", "quantity", "average_cost", "current_price", "market_value", "unrealized_gain", "realized_gain"])
        for position in summary.positions:
            writer.writerow([position.ticker, position.quantity, position.average_cost, position.current_price, position.market_value, position.unrealized_gain, position.realized_gain])
        return output.getvalue()
