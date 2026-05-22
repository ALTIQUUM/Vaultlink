# Phase 1: Foundation & Setup 🚀

## Commits 1-7: Getting Started with Vaultlink

Welcome to the first phase of the Vaultlink Masterclass! This phase covers everything you need to understand the project structure, set up your development environment, and get the application running locally.

---

## 📌 Phase Overview

| Commit | Topic | Focus |
|--------|-------|-------|
| 1 | Project Overview | System architecture and design patterns |
| 2 | Architecture Diagrams | Data flow and component interactions |
| 3 | Prerequisites | Tools and versions required |
| 4 | Docker Setup | Container orchestration explained |
| 5 | Makefile Guide | Automation workflows |
| 6 | Environment Config | Settings and secrets management |
| 7 | Quick Start | First run and verification |

---

## Commit 1: Project Overview

### What is Vaultlink?

Vaultlink is a **production-grade, full-stack financial portfolio management platform** designed to demonstrate modern software architecture patterns in a real-world application.

### Design Philosophy

```
Principle 1: Monorepo Structure
├─ Single repository for coherent cross-layer changes
├─ Shared configuration and environment variables
└─ Atomic commits that affect backend, frontend, and infra

Principle 2: Separation of Concerns
├─ Backend: REST API with business logic (FastAPI)
├─ Frontend: User interface (React + TypeScript)
└─ Infrastructure: Deployment and monitoring (Docker)

Principle 3: Production Readiness
├─ Error handling and logging
├─ Authentication and authorization
├─ Performance optimization
├─ Observability and monitoring
└─ Automated testing and CI/CD
```

### Tech Stack at a Glance

**Backend:**
- Framework: FastAPI (async Python web framework)
- ORM: SQLAlchemy 2.0 (database modeling)
- Database: PostgreSQL (primary data store)
- Cache: Redis (session and data caching)
- Task Queue: Celery (async job processing)
- Auth: JWT tokens + bcrypt password hashing

**Frontend:**
- Framework: React 18 (UI library)
- Language: TypeScript (type-safe JavaScript)
- Build Tool: Vite (next-gen bundler)
- Styling: Tailwind CSS (utility-first CSS)
- HTTP Client: Axios (REST API calls)
- State Management: Context API + Hooks

**Infrastructure:**
- Containerization: Docker
- Orchestration: Docker Compose
- Monitoring: Prometheus + Grafana
- CI/CD: GitHub Actions
- Deployment: Vercel (frontend), Docker (backend)

### Project Structure

```
Vaultlink/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point
│   │   ├── api/routes/             # REST endpoints
│   │   ├── services/               # Business logic
│   │   ├── models/                 # Database models
│   │   ├── schemas/                # Request/response schemas
│   │   ├── core/                   # Config, database, security
│   │   ├── tasks/                  # Celery tasks
│   │   └── utils/                  # Helper functions
│   ├── tests/                       # Unit and integration tests
│   ├── Dockerfile                  # Container definition
│   ├── requirements.txt            # Python dependencies
│   └── pytest.ini                  # Test configuration
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx                # React entry point
│   │   ├── App.tsx                 # Root component
│   │   ├── components/             # Reusable UI components
│   │   ├── pages/                  # Page components
│   │   ├── services/               # API clients
│   │   ├── hooks/                  # Custom React hooks
│   │   ├── context/                # Context providers
│   │   ├── types/                  # TypeScript definitions
│   │   └── utils/                  # Utilities
│   ├── Dockerfile                  # Container definition
│   ├── package.json                # Node dependencies
│   ├── vite.config.ts              # Vite configuration
│   ├── tsconfig.json               # TypeScript configuration
│   └── tailwind.config.js          # Tailwind configuration
│
├── monitoring/
│   ├── prometheus.yml              # Metrics scraping config
│   └── grafana/dashboard.json      # Pre-built dashboards
│
├── docker-compose.yml              # Development orchestration
├── docker-compose.prod.yml         # Production orchestration
├── Makefile                        # Command automation
└── pyproject.toml                  # Python project config
```

### Key Features

1. **Portfolio Management**: Track stocks, crypto, and other assets
2. **Real-time Alerts**: Get notified when prices hit targets
3. **Risk Analysis**: Calculate portfolio metrics and risk
4. **Stock Screener**: Filter stocks by custom criteria
5. **Watchlist**: Monitor stocks of interest
6. **News Integration**: Stay updated with market news
7. **Admin Panel**: System-wide management
8. **Real-time Updates**: WebSocket connections for live data

---

## Commit 2: Architecture Diagrams

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER BROWSER                             │
│  (React 18 + TypeScript + Vite + Tailwind CSS)             │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS
                     ↓
┌─────────────────────────────────────────────────────────────┐
│                 VAULTLINK API GATEWAY                       │
│  FastAPI Application (Port 8000)                           │
├─────────────────────────────────────────────────────────────┤
│  MIDDLEWARE LAYER                                           │
│  ├─ CORS Middleware       (Cross-origin requests)          │
│  ├─ JWT Auth Middleware   (Authentication)                 │
│  ├─ Error Handler         (Exception handling)             │
│  └─ Request/Response Log  (Observability)                  │
├─────────────────────────────────────────────────────────────┤
│  API ROUTES LAYER                                           │
│  ├─ /auth            (Login, Register, Token Refresh)      │
│  ├─ /portfolio       (Portfolio operations)                │
│  ├─ /stocks          (Stock data and quotes)               │
│  ├─ /watchlist       (Watchlist management)                │
│  ├─ /alerts          (Alert creation and management)       │
│  ├─ /risk            (Risk calculations)                   │
│  ├─ /news            (News aggregation)                    │
│  ├─ /screener        (Stock screening)                     │
│  └─ /admin           (Admin operations)                    │
├─────────────────────────────────────────────────────────────┤
│  SERVICE LAYER                                              │
│  ├─ AuthService      (User auth and JWT)                   │
│  ├─ PortfolioService (Portfolio logic)                     │
│  ├─ StockService     (Stock data fetching)                 │
│  ├─ RiskEngine       (Risk calculations)                   │
│  ├─ AlertService     (Alert management)                    │
│  ├─ NewsService      (News aggregation)                    │
│  ├─ ScreenerService  (Stock screening)                     │
│  └─ EmailService     (Email notifications)                 │
├─────────────────────────────────────────────────────────────┤
│  DATA ACCESS LAYER                                          │
│  ├─ SQLAlchemy ORM   (Database abstraction)                │
│  └─ Redis Cache      (Data caching)                        │
└──────┬──────────────────────────────────────────────┬───────┘
       │                                              │
       ↓                                              ↓
┌─────────────────┐ ┌──────────────┐  ┌─────────────────────┐
│   PostgreSQL    │ │    Redis     │  │  External APIs      │
│   Database      │ │   Cache/Q    │  │  ├─ Stock quotes    │
│  (Primary Data  │ │              │  │  └─ News feeds      │
│   Store)        │ └──────────────┘  └─────────────────────┘
└────────┬────────┘
         │ Monitoring
         ↓
┌─────────────────────────────────────────────────────────────┐
│         OBSERVABILITY STACK                                 │
│  ├─ Prometheus (Metrics Collection)   Port: 9090          │
│  ├─ Grafana    (Metrics Dashboard)     Port: 3000         │
│  └─ Sentry     (Error Tracking)                           │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow: User Login

```
1. User enters credentials in browser
   └─→ Frontend/pages/Login.tsx

2. Frontend sends POST /auth/login
   └─→ frontend/services/auth.ts

3. Backend validates credentials
   AuthRoute ──→ AuthService ──→ Database query
   └─→ Verify password with bcrypt

4. Backend generates JWT token
   └─→ Contains user ID, email, role, expiration

5. Frontend receives token
   └─→ Stored in AuthContext (in-memory + localStorage)

6. Subsequent requests include Authorization header
   └─→ JWT Auth Middleware validates each request

7. User redirected to Dashboard
   └─→ Dashboard fetches data with authenticated JWT
```

### Data Flow: Stock Price Update

```
1. Scheduler triggers price update task
   └─→ tasks/price_updater.py (Celery Beat)

2. Task fetches current prices
   └─→ StockService.fetch_latest_quotes()
   └─→ Calls external stock API

3. Prices saved to database
   └─→ Update stock.current_price
   └─→ Update stock.updated_at timestamp

4. WebSocket event broadcast
   └─→ Notify all connected clients
   └─→ Frontend receives real-time update

5. Frontend updates Portfolio Chart
   └─→ React component re-renders
   └─→ Tailwind CSS animation plays

6. Alert check triggers
   └─→ If price hits target, notification sent
   └─→ Email + in-app notification
```

### Component Interaction Diagram

```
App.tsx
├─ AuthContext (Authentication state)
├─ NotificationContext (Alerts and toasts)
└─ Routes
   ├─ Login.tsx
   │  └─ Uses: AuthContext, auth.service
   │
   ├─ Dashboard.tsx
   │  ├─ PortfolioChart.tsx
   │  │  └─ Uses: usePortfolio hook
   │  ├─ RiskMetrics.tsx
   │  │  └─ Uses: portfolio.service
   │  └─ NewsCard.tsx
   │     └─ Uses: stocks.service
   │
   ├─ Portfolio.tsx
   │  ├─ PositionList
   │  └─ AddPositionForm
   │     └─ Uses: portfolio.service
   │
   ├─ Watchlist.tsx
   │  ├─ WatchlistCard
   │  └─ AddStockForm
   │
   └─ StockDetail.tsx
      ├─ PriceChart.tsx
      ├─ StockInfo.tsx
      └─ Uses: useWebSocket hook (real-time)
```

---

## Commit 3: Prerequisites

### System Requirements

**Operating System:**
- Windows 10+ (with WSL2 for Linux containers)
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian 11+)

**Required Software:**

| Software | Version | Purpose |
|----------|---------|---------|
| Docker | 20.10+ | Container runtime |
| Docker Compose | 2.0+ | Multi-container orchestration |
| Python | 3.10+ | Backend runtime |
| Node.js | 18+ | Frontend build and runtime |
| npm | 8+ | Node package manager |
| Git | 2.30+ | Version control |
| Make | 4.3+ | Command automation |

### Installation Guides

**Docker (Windows):**
```bash
# Download Docker Desktop from https://www.docker.com/products/docker-desktop
# Run installer, accept defaults
# Verify installation
docker --version
docker compose version
```

**Docker (macOS):**
```bash
# Using Homebrew
brew install docker docker-compose

# Start Docker daemon
open /Applications/Docker.app

# Verify
docker --version
```

**Docker (Linux - Ubuntu):**
```bash
# Install Docker
sudo apt-get update
sudo apt-get install docker.io docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify
docker --version
```

**Python 3.10+:**
```bash
# macOS (Homebrew)
brew install python@3.10

# Windows (Chocolatey)
choco install python

# Linux (Ubuntu)
sudo apt-get install python3.10

# Verify
python --version
```

**Node.js 18+:**
```bash
# Using nvm (recommended)
nvm install 18
nvm use 18

# Or direct download
# Visit https://nodejs.org/

# Verify
node --version
npm --version
```

### Verify Your Setup

```bash
# Clone the repository
git clone https://github.com/ALTIQUUM/Vaultlink.git
cd Vaultlink

# Check all tools
python --version           # Should be 3.10+
node --version            # Should be 18+
npm --version             # Should be 8+
docker --version          # Should be 20.10+
docker compose version    # Should be 2.0+

# If all pass, you're ready!
```

---

## Commit 4: Docker Setup Explained

### Docker Compose Structure

The project uses **two Docker Compose files**:
1. `docker-compose.yml` - Development environment
2. `docker-compose.prod.yml` - Production environment

### Development Environment (docker-compose.yml)

```yaml
version: '3.8'

services:
  # Backend API Service
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: vaultlink-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/vaultlink
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend:/app  # Hot reload code changes
    command: uvicorn app.main:app --host 0.0.0.0 --reload

  # Frontend Service
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: vaultlink-frontend
    ports:
      - "5173:5173"  # Vite dev server
    volumes:
      - ./frontend:/app
    command: npm run dev

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: vaultlink-postgres
    environment:
      - POSTGRES_USER=vaultlink
      - POSTGRES_PASSWORD=dev_password
      - POSTGRES_DB=vaultlink_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: vaultlink-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Prometheus Monitoring
  prometheus:
    image: prom/prometheus:latest
    container_name: vaultlink-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  # Grafana Visualization
  grafana:
    image: grafana/grafana:latest
    container_name: vaultlink-grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

### Service Details

**Backend Container:**
- Runs FastAPI application
- Hot-reload on code changes (development mode)
- Connected to PostgreSQL and Redis
- Exposes metrics to Prometheus

**Frontend Container:**
- Runs Vite development server
- Fast HMR (Hot Module Replacement)
- Proxies API calls to backend

**PostgreSQL Container:**
- Persists data to `postgres_data` volume
- Development credentials: user=`vaultlink`, password=`dev_password`
- Default database: `vaultlink_db`

**Redis Container:**
- In-memory cache
- Session storage
- Celery task queue

**Prometheus Container:**
- Scrapes metrics every 15 seconds
- Stores metrics in `prometheus_data` volume
- Accessible at `http://localhost:9090`

**Grafana Container:**
- Visualizes Prometheus metrics
- Pre-built dashboard included
- Default credentials: admin/admin
- Accessible at `http://localhost:3000`

---

## Commit 5: Makefile Commands Guide

The project provides automation through a `Makefile`. Here are the common commands:

```makefile
# Development
make up              # Start all services
make down            # Stop all services
make build           # Build Docker images
make logs-backend    # View backend logs
make logs-frontend   # View frontend logs
make logs            # View all logs

# Database
make db-migrate      # Run pending migrations
make db-seed         # Seed database with sample data
make db-reset        # Reset database

# Testing
make test            # Run all tests
make test-backend    # Run backend tests only
make test-frontend   # Run frontend tests only
make test-coverage   # Generate coverage report

# Code Quality
make lint            # Run all linters
make lint-backend    # Lint backend code
make lint-frontend   # Lint frontend code
make format          # Format all code
make type-check      # Run type checker

# Cleanup
make clean           # Remove all containers and volumes
make clean-images    # Remove Docker images
make help            # Show all available commands
```

### Common Workflows

**First-time setup:**
```bash
make build           # Build images
make up              # Start services
make db-migrate      # Run migrations
make db-seed         # Load sample data
# App is ready at localhost:5173
```

**Daily development:**
```bash
make up              # Start services
make logs            # Watch logs in another terminal
# Edit code... changes auto-reload
make test            # Run tests before committing
```

**Before pushing:**
```bash
make lint            # Check code style
make format          # Auto-format code
make test-coverage   # Check test coverage
make type-check      # Check TypeScript types
```

**Cleanup:**
```bash
make down            # Stop services
make clean           # Remove everything
make build           # Rebuild from scratch
```

---

## Commit 6: Environment Configuration

### Configuration Hierarchy

```
1. Docker Compose Environment Variables (.env file)
2. FastAPI Settings (app.core.config)
3. React Build-time Variables
4. Runtime Overrides
```

### Backend Configuration (.env example)

```env
# Application
PROJECT_NAME=Vaultlink
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=postgresql://vaultlink:dev_password@postgres:5432/vaultlink_db
DATABASE_ECHO=true

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# External APIs
STOCK_API_KEY=your_api_key_here
NEWS_API_KEY=your_news_api_key

# Email (for alerts and notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Sentry (Error tracking)
SENTRY_DSN=https://your-sentry-dsn@sentry.io/project

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2
```

### Frontend Configuration (vite.config.ts)

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
})
```

### Accessing Configuration

**In FastAPI:**
```python
from app.core.config import get_settings

settings = get_settings()
print(settings.database_url)
print(settings.project_name)
```

**In React:**
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

---

## Commit 7: Quick Start Guide

### First-Time Setup (10 minutes)

```bash
# 1. Clone repository
git clone https://github.com/ALTIQUUM/Vaultlink.git
cd Vaultlink

# 2. Create .env file with sample values
cp backend/.env.example backend/.env

# 3. Build and start services
make build
make up

# 4. In another terminal, migrate database
make db-migrate

# 5. Seed with sample data (optional)
make db-seed

# 6. Open browser
# Frontend: http://localhost:5173
# Backend API Docs: http://localhost:8000/docs
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
```

### Verification Checklist

✅ All containers running:
```bash
docker compose ps
```

✅ Backend API responding:
```bash
curl http://localhost:8000/docs
# Should see Swagger UI
```

✅ Frontend loading:
```bash
# Open http://localhost:5173 in browser
# Should see login page
```

✅ Database connected:
```bash
make db-migrate
# Should show no pending migrations
```

✅ Redis working:
```bash
docker exec vaultlink-redis redis-cli PING
# Should return PONG
```

### Test Login

1. Open `http://localhost:5173`
2. Click "Register"
3. Create account with:
   - Email: `user@example.com`
   - Password: `Test@1234`
4. Login with credentials
5. You should see Dashboard

---

## 🎯 Phase 1 Summary

By the end of Phase 1, you should understand:

- ✅ Project structure and organization
- ✅ Tech stack and how components interact
- ✅ System architecture and data flow
- ✅ Development environment setup
- ✅ Docker and containerization
- ✅ Configuration management
- ✅ How to get everything running locally

**Next Phase**: [Backend Architecture](../02-backend-architecture/README.md)

