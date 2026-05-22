# Phase 3: Backend API Routes 🔌

## Commits 23-31: REST Endpoints and Real-time Features

This phase explores all REST API endpoints and how the frontend communicates with the backend.

### API Route Organization

```
/auth              - Authentication (register, login, logout)
/portfolio         - Portfolio CRUD operations
/stocks            - Stock data and quotes
/watchlist         - Watchlist management
/alerts            - Alert rules and notifications
/risk              - Risk calculations and metrics
/news              - News integration and feeds
/screener          - Stock screening with filters
/admin             - System administration
```

### Authentication Endpoints

```python
# POST /auth/register
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}

Response:
{
  "id": "uuid...",
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true
}

# POST /auth/login
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response:
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 1800
}

# GET /auth/me
Response:
{
  "id": "uuid...",
  "email": "user@example.com",
  "full_name": "John Doe",
  "portfolios": [...]
}
```

### Portfolio Endpoints

```python
# GET /portfolio - List all portfolios
# POST /portfolio - Create new portfolio
# GET /portfolio/{portfolio_id} - Get portfolio details
# PUT /portfolio/{portfolio_id} - Update portfolio
# DELETE /portfolio/{portfolio_id} - Delete portfolio

# GET /portfolio/{portfolio_id}/positions - List positions
# POST /portfolio/{portfolio_id}/positions - Add position
# DELETE /portfolio/{portfolio_id}/positions/{position_id} - Remove position
```

### Stock Endpoints

```python
# GET /stocks - List stocks with pagination
# GET /stocks/{ticker} - Get specific stock
# GET /stocks/{ticker}/quote - Real-time quote
# GET /stocks/{ticker}/historical - Historical price data
# GET /stocks/search?q=query - Search stocks

Response Example:
{
  "ticker": "AAPL",
  "name": "Apple Inc.",
  "current_price": 150.25,
  "change_percent": 2.5,
  "market_cap": 2400000000000,
  "pe_ratio": 28.5,
  "sector": "Technology"
}
```

### Other Major Endpoints

**Watchlist:**
- `GET /watchlist` - List watchlists
- `POST /watchlist` - Create watchlist
- `POST /watchlist/{id}/items` - Add stock to watchlist
- `DELETE /watchlist/{id}/items/{stock_id}` - Remove stock

**Alerts:**
- `GET /alerts` - List user's alerts
- `POST /alerts` - Create alert rule
- `PUT /alerts/{id}` - Update alert
- `DELETE /alerts/{id}` - Delete alert

**Screener:**
- `POST /screener/scan` - Run stock screener
- Parameters: min_price, max_price, min_market_cap, sector, etc.

**Risk:**
- `GET /risk/metrics` - Portfolio risk metrics
- `GET /risk/allocation` - Asset allocation analysis
- `GET /risk/correlation` - Stock correlations

**News:**
- `GET /news` - Trending market news
- `GET /news/{ticker}` - News for specific stock

**Admin:**
- `GET /admin/users` - List all users
- `GET /admin/system/health` - System health check
- `POST /admin/tasks` - Manage background tasks

### Error Response Format

```python
{
  "detail": {
    "error": "error_code",
    "message": "Human-readable message",
    "field": "field_name (optional)",
    "timestamp": "2024-05-23T10:30:00Z"
  }
}
```

---

## 🎯 Phase 3 Summary

By end of Phase 3:
- ✅ Understand all REST endpoints
- ✅ API request/response patterns
- ✅ Error handling conventions
- ✅ Authentication flow
- ✅ Pagination and filtering
- ✅ Rate limiting

**Next Phase**: [Frontend Architecture](../04-frontend-architecture/README.md)

