import logging

from app.core.database import SessionLocal
from app.core.redis import get_redis
from app.services.alert_service import AlertService
from app.services.stock_service import StockService
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.alert_worker.check_alerts")
def check_alerts() -> int:
    with SessionLocal() as db:
        count = AlertService(db, StockService(get_redis())).check_active()
    logger.info("Alert worker completed with %s triggers", count)
    return count
