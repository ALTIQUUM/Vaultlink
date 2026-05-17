.PHONY: up down logs backend-test frontend-test lint format migrate worker

up:
	docker compose up --build

down:
	docker compose down --remove-orphans

logs:
	docker compose logs -f

backend-test:
	cd backend && pytest

frontend-test:
	cd frontend && npm test -- --watchAll=false

lint:
	cd backend && black --check app tests && isort --check-only app tests && flake8 app tests
	cd frontend && npm run lint

format:
	cd backend && black app tests && isort app tests
	cd frontend && npm run format

migrate:
	cd backend && alembic upgrade head

worker:
	cd backend && celery -A app.tasks.celery_app.celery_app worker --beat --loglevel=INFO
