# Phase 6: Advanced Topics 🚀

## Commits 51-57: Production Patterns and Deployment

This final phase covers advanced features, testing, CI/CD, security, and deployment.

### WebSocket Implementation

```python
# app/api/websocket.py
from fastapi import APIRouter, WebSocket, Depends
from app.core.security import decode_token
from typing import Set

router = APIRouter(prefix="/ws", tags=["websocket"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
    
    async def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                pass

manager = ConnectionManager()

@router.websocket("/stocks/{ticker}")
async def websocket_stock_updates(websocket: WebSocket, ticker: str):
    """Real-time stock price updates"""
    await manager.connect(websocket)
    try:
        while True:
            # Receive any message (e.g., keep-alive)
            data = await websocket.receive_text()
            
            # Send stock update
            await websocket.send_json({
                "type": "price_update",
                "ticker": ticker,
                "price": 150.25,
                "timestamp": datetime.utcnow().isoformat()
            })
    except Exception as e:
        await manager.disconnect(websocket)

@router.websocket("/portfolio/{portfolio_id}")
async def websocket_portfolio_updates(websocket: WebSocket, portfolio_id: str):
    """Real-time portfolio updates"""
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
            # Send portfolio metrics
            await websocket.send_json({
                "type": "portfolio_update",
                "portfolio_id": portfolio_id,
                "total_value": 100000.00,
                "positions": [...]
            })
    except Exception:
        await manager.disconnect(websocket)
```

### Testing Strategy

```python
# backend/tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal

client = TestClient(app)

def test_register_user():
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "Test@1234",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login_user():
    """Test user login"""
    # First register
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "Test@1234",
            "full_name": "Test User"
        }
    )
    
    # Then login
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "Test@1234"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "wrong"
        }
    )
    assert response.status_code == 401

@pytest.fixture
def authenticated_client():
    """Fixture for authenticated test client"""
    # Create user
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "Test@1234"
        }
    )
    
    # Get token
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "Test@1234"
        }
    )
    token = response.json()["access_token"]
    
    # Add to headers
    client.headers = {"Authorization": f"Bearer {token}"}
    return client

def test_get_portfolio(authenticated_client):
    """Test getting portfolios with auth"""
    response = authenticated_client.get("/portfolio")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### Frontend Testing

```typescript
// frontend/src/__tests__/Auth.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { LoginPage } from '../pages/Login'
import { AuthProvider } from '../context/AuthContext'

describe('LoginPage', () => {
  it('renders login form', () => {
    render(
      <AuthProvider>
        <LoginPage />
      </AuthProvider>
    )
    
    expect(screen.getByText('Login')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument()
  })

  it('handles successful login', async () => {
    render(
      <AuthProvider>
        <LoginPage />
      </AuthProvider>
    )

    fireEvent.change(screen.getByPlaceholderText('Email'), {
      target: { value: 'user@example.com' }
    })
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'Password123' }
    })
    fireEvent.click(screen.getByText('Login'))

    await waitFor(() => {
      expect(screen.queryByText('Loading')).not.toBeInTheDocument()
    })
  })

  it('shows error on invalid credentials', async () => {
    render(
      <AuthProvider>
        <LoginPage />
      </AuthProvider>
    )

    fireEvent.change(screen.getByPlaceholderText('Email'), {
      target: { value: 'wrong@example.com' }
    })
    fireEvent.change(screen.getByPlaceholderText('Password'), {
      target: { value: 'wrong' }
    })
    fireEvent.click(screen.getByText('Login'))

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument()
    })
  })
})
```

### CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: vaultlink_test
          POSTGRES_PASSWORD: test
      redis:
        image: redis:7

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          pytest tests/ --cov=app --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  frontend-tests:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Run tests
        run: |
          cd frontend
          npm test -- --coverage
      
      - name: Build
        run: |
          cd frontend
          npm run build

  deploy:
    needs: [backend-tests, frontend-tests]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # Add deployment scripts here
```

### Performance Optimization

```python
# Backend: Query optimization
from sqlalchemy import joinedload

# Bad: N+1 query problem
portfolios = db.query(Portfolio).all()
for portfolio in portfolios:
    positions = portfolio.positions  # Extra query each iteration

# Good: Use eager loading
portfolios = db.query(Portfolio).options(
    joinedload(Portfolio.positions)
).all()

# With pagination
def get_portfolios(
    db: Session,
    skip: int = 0,
    limit: int = 10
) -> list[Portfolio]:
    return db.query(Portfolio).offset(skip).limit(limit).all()
```

```typescript
// Frontend: Code splitting and lazy loading
import { lazy, Suspense } from 'react'

const Dashboard = lazy(() => import('../pages/Dashboard'))
const Portfolio = lazy(() => import('../pages/Portfolio'))

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/portfolio" element={<Portfolio />} />
      </Routes>
    </Suspense>
  )
}
```

### Security Best Practices

```python
# Security hardening
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZIPMiddleware

app = FastAPI()

# Only allow trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "www.example.com"]
)

# Compression
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# HTTPS enforcement in production
@app.middleware("http")
async def https_redirect(request, call_next):
    if request.headers.get('x-forwarded-proto') == 'http' and ENV == 'production':
        return RedirectResponse(url=request.url.replace("http://", "https://"), status_code=301)
    return await call_next(request)
```

### Database Connection Pooling

```python
# Optimized connection management
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool, NullPool

# Development: NullPool (no pooling)
engine = create_engine(
    database_url,
    poolclass=NullPool if ENV == 'test' else QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True  # Verify connections before using
)
```

### Redis Caching Optimization

```python
# Cache warming on startup
@app.on_event("startup")
async def startup_cache():
    """Pre-warm Redis cache"""
    top_stocks = db.query(Stock).limit(100).all()
    for stock in top_stocks:
        price = fetch_price(stock.ticker)
        await redis_client.set(
            f"stock_price:{stock.ticker}",
            str(price),
            ex=300
        )
```

### Deployment Guide

```bash
# Build and push Docker images
docker build -t myregistry/vaultlink-backend:latest ./backend
docker build -t myregistry/vaultlink-frontend:latest ./frontend
docker push myregistry/vaultlink-backend:latest
docker push myregistry/vaultlink-frontend:latest

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Health check
curl http://localhost:8000/health
```

### Monitoring and Observability

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

# Custom metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

active_users = Gauge(
    'active_users',
    'Number of active users'
)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    request_count.labels(
        method=request.method,
        endpoint=request.url.path
    ).inc()
    
    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response
```

---

## 🎯 Phase 6 Summary

By end of Phase 6:
- ✅ WebSocket implementation
- ✅ Real-time features
- ✅ Testing strategies
- ✅ CI/CD pipeline setup
- ✅ Performance optimization
- ✅ Security hardening
- ✅ Production deployment
- ✅ Monitoring and observability

---

## 🎓 Masterclass Complete! 

Congratulations! You've completed the Vaultlink Masterclass covering:

### Backend (Commits 1-31)
- FastAPI fundamentals and advanced patterns
- SQLAlchemy ORM and database design
- Authentication, security, and authorization
- Caching, task queues, and async patterns
- REST API design and implementation

### Frontend (Commits 32-50)
- React 18 and TypeScript patterns
- State management with Context API
- Component architecture and composition
- Custom hooks and form handling
- Responsive UI with Tailwind CSS

### Production (Commits 51-57)
- Real-time WebSocket features
- Testing and quality assurance
- CI/CD automation
- Performance optimization
- Security best practices
- Monitoring and deployment

---

## 📚 Next Steps

1. **Deep Dive**: Choose a topic and go deeper
2. **Contribute**: Add features or improvements
3. **Learn More**: Explore the actual Vaultlink codebase
4. **Build**: Create your own project using these patterns
5. **Share**: Teach others these concepts

---

## 📖 Additional Resources

- [FastAPI Best Practices](https://fastapi.tiangolo.com/)
- [React Patterns](https://react.dev/)
- [SQLAlchemy Guide](https://docs.sqlalchemy.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

**Happy Learning! 🚀**

