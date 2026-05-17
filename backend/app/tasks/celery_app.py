from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery("vaultlink", broker=settings.resolved_redis_url, backend=settings.resolved_redis_url)
celery_app.conf.beat_schedule = {
    "check-alerts-every-five-minutes": {
        "task": "app.tasks.alert_worker.check_alerts",
        "schedule": 300.0,
    },
    "refresh-prices-every-five-minutes": {
        "task": "app.tasks.price_updater.refresh_watchlist_prices",
        "schedule": 300.0,
    },
}
