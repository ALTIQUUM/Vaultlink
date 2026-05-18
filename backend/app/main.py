import logging

import sentry_sdk
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routes import (
    admin,
    alerts,
    auth,
    news,
    portfolio,
    risk,
    screener,
    stocks,
    watchlist,
)
from app.core.config import get_settings

settings = get_settings()
logging.basicConfig(level=logging.INFO)

if settings.sentry_dsn:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        environment=settings.environment,
        traces_sample_rate=0.1,
    )

app = FastAPI(
    title=settings.project_name, version="0.1.0", docs_url="/docs", redoc_url="/redoc"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.backend_cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (
    auth.router,
    portfolio.router,
    stocks.router,
    risk.router,
    watchlist.router,
    alerts.router,
    news.router,
    screener.router,
    admin.router,
):
    app.include_router(router, prefix=settings.api_v1_prefix)

Instrumentator().instrument(app).expose(app)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "vaultlink"}


@app.websocket("/ws/notifications/{user_id}")
async def notification_socket(websocket: WebSocket, user_id: int) -> None:
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_text()
            await websocket.send_json({"user_id": user_id, "echo": message})
    except WebSocketDisconnect:
        logging.getLogger(__name__).info(
            "Notification websocket closed for user_id=%s", user_id
        )
