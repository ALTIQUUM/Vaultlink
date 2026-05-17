import logging
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import Alert, AlertKind
from app.models.notification import Notification
from app.schemas.alert import AlertCreate
from app.services.email_service import EmailService
from app.services.stock_service import StockService

logger = logging.getLogger(__name__)


class AlertService:
    def __init__(self, db: Session, stocks: StockService) -> None:
        self.db = db
        self.stocks = stocks

    def create(self, user_id: int, data: AlertCreate) -> Alert:
        alert = Alert(user_id=user_id, ticker=data.ticker, kind=data.kind, threshold=data.threshold)
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def check_active(self) -> int:
        triggered = 0
        alerts = self.db.scalars(select(Alert).where(Alert.is_active.is_(True))).all()
        for alert in alerts:
            quote = self.stocks.quote(alert.ticker)
            hit = (
                (alert.kind == AlertKind.PRICE_ABOVE and quote.price >= alert.threshold)
                or (alert.kind == AlertKind.PRICE_BELOW and quote.price <= alert.threshold)
                or (alert.kind == AlertKind.PERCENT_CHANGE and quote.change_percent is not None and abs(quote.change_percent) >= alert.threshold)
            )
            if hit:
                alert.last_triggered_at = datetime.now(UTC)
                notification = Notification(user_id=alert.user_id, title=f"{alert.ticker} alert triggered", body=f"{alert.kind.value} threshold {alert.threshold} matched at {quote.price}.")
                self.db.add(notification)
                EmailService().send(alert.user.email, notification.title, notification.body)
                triggered += 1
        self.db.commit()
        logger.info("Alert scan triggered %s alerts", triggered)
        return triggered
