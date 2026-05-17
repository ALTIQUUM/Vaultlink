# VAULTLINK
### Institutional-grade financial intelligence. Open source.
> Built in silence. Found in history. — ALTIQUUM

![CI/CD](https://img.shields.io/badge/CI%2FCD-passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-80%25%2B-brightgreen)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![License](https://img.shields.io/badge/license-MIT-black)

## Features
VAULTLINK provides authenticated portfolio tracking, cached market quotes, portfolio P&L, risk analytics, watchlists, alerts, market news sentiment, stock screening, admin health views, WebSocket notifications, and production observability.

## Tech Stack
FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL 15, Redis 7, Celery 5, React 18, TypeScript, TailwindCSS, Recharts, Framer Motion, Docker, GitHub Actions, Prometheus, Grafana, Sentry, Railway, and Vercel.

## Architecture Diagram (ASCII)
```text
React/Vercel -> FastAPI/Railway -> PostgreSQL
      |              |
      |              +-> Redis cache/broker -> Celery workers
      |              |
      +-> WebSocket notifications
FastAPI -> Prometheus -> Grafana
FastAPI -> Sentry
```

## Quick Start (Docker — one command)
```bash
docker compose up --build
```

## Environment Variables
Copy `.env.example` to `.env`, then set `JWT_SECRET`, `DATABASE_URL`, `REDIS_URL`, OAuth credentials, SMTP credentials, `ALPHA_VANTAGE_API_KEY`, `NEWS_API_KEY`, and deployment secrets in GitHub Actions.

## API Documentation
Swagger UI is available at `http://localhost:8000/docs`; ReDoc is available at `http://localhost:8000/redoc`.

## Contributing
Use feature branches, keep commits scoped, run `make lint` and `make backend-test`, and include tests for every behavior change.

## License
MIT. See `LICENSE`.
