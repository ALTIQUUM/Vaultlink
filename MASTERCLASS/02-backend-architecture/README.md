# Phase 2: Backend Architecture 🏗️

## Commits 8-22: FastAPI, Database, and Services

This phase dives deep into the backend architecture, exploring how data is structured, how services communicate, and how the FastAPI application is organized.

---

## 📌 Phase Overview

| Commit | Topic | Focus |
|--------|-------|-------|
| 8 | Core Configuration | Settings and environment management |
| 9 | Database Setup | SQLAlchemy ORM and connection pooling |
| 10 | User & Auth Models | User data structure and security |
| 11 | Portfolio Models | Position and holdings data |
| 12 | Stock Models | Stock and ticker data |
| 13 | Alert Models | Alert rules and notifications |
| 14 | Authentication | JWT tokens and security |
| 15 | Redis Caching | Cache strategies and patterns |
| 16 | Celery Tasks | Async job processing |
| 17 | Dependencies | Dependency injection patterns |
| 18 | Error Handling | Custom exceptions and error responses |
| 19 | Logging | Structured logging and monitoring |
| 20 | Database Migrations | Alembic migration strategy |
| 21 | Fixtures & Seeds | Test data and fixtures |
| 22 | Testing Strategy | Backend testing patterns |

---

## Commit 8: Core Configuration System

### Settings Management Architecture

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application configuration from environment variables"""
    
    # Application
    project_name: str = "Vaultlink"
    environment: str = "development"
    debug: bool = False
    
    # Database
    database_url: str
    database_echo: bool = False
    database_pool_size: int = 20
    database_max_overflow: int = 40
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    redis_max_connections: int = 50
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS
    backend_cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000"
    ]
    
    # External APIs
    stock_api_key: str
    news_api_key: str
    
    # Email
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    
    # Sentry
    sentry_dsn: str | None = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton"""
    return Settings()
```

### Configuration Usage

```python
# In FastAPI app
from app.core.config import get_settings

settings = get_settings()

# Access settings
app = FastAPI(
    title=settings.project_name,
    version="0.1.0",
    debug=settings.debug
)
```

### Environment Variables Hierarchy

```
1. System Environment Variables (highest priority)
2. .env file in backend directory
3. Default values in Settings class (lowest priority)
```

---

## Commit 9: Database Setup and Connection

### SQLAlchemy Configuration

```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
from app.core.config import get_settings

settings = get_settings()

# Create engine with connection pooling
engine = create_engine(
    settings.database_url,
    poolclass=QueuePool,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    echo=settings.database_echo,
    connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()

# Dependency injection for database session
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Connection Pooling Strategy

```
┌──────────────────────────────────────┐
│    FastAPI Request Handler           │
├──────────────────────────────────────┤
│ Need DB connection?                  │
│ ├─ Check QueuePool for available     │
│ ├─ If available: use existing        │
│ ├─ If not: create new (up to limit)  │
│ └─ Await if at max (with timeout)    │
│                                      │
│ Use connection...                    │
│                                      │
│ Return to pool on complete           │
│ (Connection not closed, reused)      │
└──────────────────────────────────────┘

Benefits:
- Reduced connection setup overhead
- Better resource utilization
- Handles concurrent requests efficiently
```

### Database Initialization

```python
# Create all tables
Base.metadata.create_all(bind=engine)

# In practice, use Alembic migrations (Commit 20)
```

---

## Commit 10: User and Authentication Models

### User Model

```python
# app/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    
    # Profile
    avatar_url = Column(String(500), nullable=True)
    bio = Column(String(500), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    portfolios = relationship("Portfolio", back_populates="owner")
    watchlists = relationship("Watchlist", back_populates="owner")
    alerts = relationship("Alert", back_populates="user")
    positions = relationship("Position", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
```

### Password Security

```python
# app/core/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed: str) -> bool:
    """Verify password matches hash"""
    return pwd_context.verify(plain_password, hashed)

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    """Create JWT access token"""
    if expires_delta is None:
        expires_delta = timedelta(
            minutes=get_settings().access_token_expire_minutes
        )
    
    expire = datetime.utcnow() + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        get_settings().secret_key,
        algorithm=get_settings().algorithm
    )
    return encoded_jwt
```

### JWT Token Structure

```json
{
  "sub": "user@example.com",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "role": "user",
  "iat": 1684234567,
  "exp": 1684238167,
  "aud": "vaultlink"
}
```

---

## Commit 11: Portfolio and Position Models

### Portfolio Model

```python
# app/models/portfolio.py
from sqlalchemy import Column, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Portfolio info
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    currency = Column(String(3), default="USD")
    
    # Performance
    total_value = Column(Numeric(20, 2), default=0)
    total_invested = Column(Numeric(20, 2), default=0)
    total_return = Column(Numeric(20, 2), default=0)  # total_value - total_invested
    return_percentage = Column(Numeric(10, 4), default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="portfolios")
    positions = relationship("Position", back_populates="portfolio", cascade="all, delete-orphan")
    
    # Methods
    def calculate_total_value(self) -> float:
        """Calculate total portfolio value"""
        return sum(pos.current_value for pos in self.positions)
    
    def calculate_return_percentage(self) -> float:
        """Calculate total return %"""
        if self.total_invested == 0:
            return 0.0
        return (self.total_return / self.total_invested) * 100
```

### Position Model

```python
# app/models/position.py
class Position(Base):
    __tablename__ = "positions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey("portfolios.id"))
    stock_id = Column(UUID(as_uuid=True), ForeignKey("stocks.id"))
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Position details
    quantity = Column(Numeric(20, 4), nullable=False)
    average_cost = Column(Numeric(20, 4), nullable=False)
    total_cost = Column(Numeric(20, 2), nullable=False)  # quantity * average_cost
    
    # Current value
    current_price = Column(Numeric(20, 4), nullable=True)
    current_value = Column(Numeric(20, 2), nullable=True)
    unrealized_gain_loss = Column(Numeric(20, 2), nullable=True)
    unrealized_percentage = Column(Numeric(10, 4), nullable=True)
    
    # Status
    is_closed = Column(Boolean, default=False)
    
    # Timestamps
    opened_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    portfolio = relationship("Portfolio", back_populates="positions")
    stock = relationship("Stock", back_populates="positions")
    owner = relationship("User", back_populates="positions")
    transactions = relationship("Transaction", back_populates="position")
    
    # Methods
    def calculate_unrealized_gain_loss(self):
        if self.current_price:
            return (self.current_price - self.average_cost) * self.quantity
        return None
```

---

## Commit 12: Stock and Watchlist Models

### Stock Model

```python
# app/models/stock.py
class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identifiers
    ticker = Column(String(10), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    exchange = Column(String(10), nullable=True)
    
    # Current data
    current_price = Column(Numeric(20, 4), nullable=True)
    market_cap = Column(Numeric(20, 0), nullable=True)
    pe_ratio = Column(Numeric(10, 2), nullable=True)
    dividend_yield = Column(Numeric(8, 4), nullable=True)
    
    # Performance
    price_52w_high = Column(Numeric(20, 4), nullable=True)
    price_52w_low = Column(Numeric(20, 4), nullable=True)
    price_change_percent = Column(Numeric(10, 4), nullable=True)
    
    # Metadata
    sector = Column(String(100), nullable=True)
    industry = Column(String(100), nullable=True)
    description = Column(String(2000), nullable=True)
    website = Column(String(500), nullable=True)
    logo_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_price_update = Column(DateTime, nullable=True)
    
    # Relationships
    positions = relationship("Position", back_populates="stock")
    watchlist_items = relationship("WatchlistItem", back_populates="stock")
```

### Watchlist Model

```python
# app/models/watchlist.py
class Watchlist(Base):
    __tablename__ = "watchlists"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    name = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    is_default = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="watchlists")
    items = relationship("WatchlistItem", back_populates="watchlist", cascade="all, delete-orphan")

class WatchlistItem(Base):
    __tablename__ = "watchlist_items"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    watchlist_id = Column(UUID(as_uuid=True), ForeignKey("watchlists.id"))
    stock_id = Column(UUID(as_uuid=True), ForeignKey("stocks.id"))
    
    # Watchlist specific info
    notes = Column(String(1000), nullable=True)
    target_price = Column(Numeric(20, 4), nullable=True)
    alert_enabled = Column(Boolean, default=False)
    
    added_at = Column(DateTime, default=datetime.utcnow)
    
    watchlist = relationship("Watchlist", back_populates="items")
    stock = relationship("Stock", back_populates="watchlist_items")
```

---

## Commit 13: Alert and Notification Models

### Alert Model

```python
# app/models/alert.py
from enum import Enum

class AlertType(str, Enum):
    PRICE_TARGET = "price_target"
    PERCENTAGE_CHANGE = "percentage_change"
    NEWS = "news"
    EARNINGS = "earnings"
    PORTFOLIO_MILESTONE = "portfolio_milestone"

class AlertStatus(str, Enum):
    ACTIVE = "active"
    TRIGGERED = "triggered"
    PAUSED = "paused"
    EXPIRED = "expired"

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    stock_id = Column(UUID(as_uuid=True), ForeignKey("stocks.id"), nullable=True)
    
    # Alert config
    alert_type = Column(String(50), nullable=False)
    condition = Column(JSON, nullable=False)  # Flexible condition storage
    
    # Examples:
    # {"type": "above", "value": 150.00}
    # {"type": "below", "value": 100.00}
    # {"type": "change_percent", "value": 5.0, "direction": "up"}
    
    status = Column(String(20), default="active")
    priority = Column(Integer, default=0)
    
    # Notification
    notify_via_email = Column(Boolean, default=True)
    notify_via_app = Column(Boolean, default=True)
    
    # Lifecycle
    created_at = Column(DateTime, default=datetime.utcnow)
    triggered_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    paused_until = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="alerts")
    notifications = relationship("Notification", back_populates="alert")
```

### Notification Model

```python
# app/models/notification.py
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    alert_id = Column(UUID(as_uuid=True), ForeignKey("alerts.id"), nullable=True)
    
    # Content
    title = Column(String(255), nullable=False)
    message = Column(String(1000), nullable=False)
    notification_type = Column(String(50), nullable=False)
    
    # Metadata
    data = Column(JSON, nullable=True)  # Extra data (stock_id, new_price, etc)
    
    # Status
    is_read = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    read_at = Column(DateTime, nullable=True)
    
    user = relationship("User")
    alert = relationship("Alert", back_populates="notifications")
```

---

## Commit 14: Authentication Implementation

### AuthService

```python
# app/services/auth_service.py
from app.models.user import User
from app.schemas.auth import UserCreate, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from sqlalchemy.orm import Session

class AuthService:
    @staticmethod
    def register_user(db: Session, user_create: UserCreate) -> User:
        """Create new user"""
        # Check if user exists
        existing = db.query(User).filter(User.email == user_create.email).first()
        if existing:
            raise ValueError("Email already registered")
        
        # Create user
        user = User(
            email=user_create.email,
            username=user_create.email.split('@')[0],
            hashed_password=hash_password(user_create.password),
            full_name=user_create.full_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User | None:
        """Authenticate user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        
        if not verify_password(password, user.hashed_password):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        return user
    
    @staticmethod
    def get_or_create_refresh_token(user: User, db: Session) -> str:
        """Create refresh token"""
        return create_access_token(
            data={"sub": user.email, "user_id": str(user.id)},
            expires_delta=timedelta(days=7)
        )
```

### Auth Routes

```python
# app/api/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """Register new user"""
    try:
        user = AuthService.register_user(db, user_create)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """Login user"""
    user = AuthService.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id)}
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: User = Depends(get_current_user)
):
    """Get current authenticated user"""
    return current_user
```

---

## Commit 15: Redis Caching Strategy

### Redis Configuration

```python
# app/core/redis.py
import aioredis
from app.core.config import get_settings

class RedisClient:
    def __init__(self):
        self.redis = None
    
    async def connect(self):
        """Connect to Redis"""
        self.redis = await aioredis.from_url(
            get_settings().redis_url,
            encoding="utf8",
            decode_responses=True,
            max_connections=get_settings().redis_max_connections
        )
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str) -> str | None:
        """Get value from cache"""
        return await self.redis.get(key)
    
    async def set(self, key: str, value: str, ex: int = 3600):
        """Set value in cache with TTL"""
        await self.redis.setex(key, ex, value)
    
    async def delete(self, key: str):
        """Delete key from cache"""
        await self.redis.delete(key)

redis_client = RedisClient()
```

### Caching Patterns

```python
# app/utils/cache.py
from functools import wraps
import json
import hashlib

def cache_key(*args, **kwargs) -> str:
    """Generate cache key from function args"""
    key_data = f"{args}{kwargs}".encode()
    return hashlib.md5(key_data).hexdigest()

def cached(
    ttl: int = 3600,
    prefix: str = ""
):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            key = f"{prefix}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_value = await redis_client.get(key)
            if cached_value:
                return json.loads(cached_value)
            
            # Call function
            result = await func(*args, **kwargs)
            
            # Store in cache
            await redis_client.set(key, json.dumps(result), ex=ttl)
            return result
        
        return wrapper
    return decorator
```

### Usage Example

```python
@cached(ttl=300, prefix="stock_price")
async def get_stock_price(ticker: str) -> dict:
    """Get stock price (cached for 5 minutes)"""
    # Expensive API call
    price = await fetch_from_external_api(ticker)
    return price
```

---

## Commit 16: Celery Task Queue

### Celery Configuration

```python
# app/tasks/celery_app.py
from celery import Celery
from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "vaultlink",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000
)
```

### Example Task: Price Update

```python
# app/tasks/price_updater.py
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def update_stock_prices(self):
    """Celery task to update stock prices"""
    try:
        db = SessionLocal()
        
        # Get all stocks
        stocks = db.query(Stock).all()
        
        for stock in stocks:
            try:
                # Fetch latest price
                price = fetch_external_price(stock.ticker)
                
                # Update in database
                stock.current_price = price
                stock.last_price_update = datetime.utcnow()
                
                # Broadcast to WebSocket clients
                broadcast_price_update(stock.id, price)
                
            except Exception as e:
                logger.error(f"Error updating {stock.ticker}: {e}")
        
        db.commit()
        logger.info(f"Updated prices for {len(stocks)} stocks")
        
    except Exception as exc:
        logger.error(f"Task failed: {exc}")
        raise self.retry(exc=exc, countdown=60)

# Schedule this task every 5 minutes
# Using Celery Beat (periodic task scheduler)
```

### Scheduled Tasks Configuration

```python
# app/tasks/celery_app.py
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'update-stock-prices': {
        'task': 'app.tasks.price_updater.update_stock_prices',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
    'check-alerts': {
        'task': 'app.tasks.alert_worker.check_alerts',
        'schedule': crontab(minute='*/2'),  # Every 2 minutes
    },
    'send-digest-emails': {
        'task': 'app.tasks.email_service.send_digest_emails',
        'schedule': crontab(hour=9, minute=0),  # Daily at 9 AM
    }
}
```

---

## Commits 17-22: More Services Explored

### Commit 17: Dependency Injection

```python
# app/api/dependencies.py
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
    except:
        raise HTTPException(status_code=401)
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401)
    
    return user

async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current user and verify admin role"""
    if not current_user.is_superuser:
        raise HTTPException(status_code=403)
    return current_user
```

### Commits 18-22: Error Handling, Logging, Migrations, Testing

These commits cover:
- Custom exception handlers
- Structured logging with contextual information
- Alembic database migration strategy
- Seed data and test fixtures
- Backend testing patterns (unit, integration, e2e)

---

## 🎯 Phase 2 Summary

By the end of Phase 2, you understand:

- ✅ How FastAPI is configured and organized
- ✅ SQLAlchemy ORM and database models
- ✅ User authentication and JWT tokens
- ✅ Redis caching patterns and TTLs
- ✅ Celery async task processing
- ✅ Service layer architecture
- ✅ Dependency injection patterns
- ✅ Error handling and logging
- ✅ Database migrations
- ✅ Testing strategies

**Next Phase**: [Backend API Routes](../03-backend-api/README.md)

