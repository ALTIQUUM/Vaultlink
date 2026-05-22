# Phase 5: Frontend Components 🧩

## Commits 41-50: Building UI Components and Pages

This phase focuses on actual React component implementation and page layouts.

### Layout Components

```typescript
// src/components/Layout/Navbar.tsx
import React from 'react'
import { useAuth } from '../../hooks/useAuth'
import { Link, useNavigate } from 'react-router-dom'

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-8">
            <h1 className="text-2xl font-bold text-primary">Vaultlink</h1>
            <div className="hidden md:flex space-x-4">
              <Link to="/dashboard" className="text-gray-700 hover:text-primary">
                Dashboard
              </Link>
              <Link to="/portfolio" className="text-gray-700 hover:text-primary">
                Portfolio
              </Link>
              <Link to="/screener" className="text-gray-700 hover:text-primary">
                Screener
              </Link>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700">{user?.email}</span>
            <button
              onClick={handleLogout}
              className="bg-danger text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
```

### Dashboard Page

```typescript
// src/pages/Dashboard.tsx
import React, { useEffect } from 'react'
import { useAuth } from '../hooks/useAuth'
import { usePortfolio } from '../hooks/usePortfolio'
import { PortfolioChart } from '../components/charts/PortfolioChart'
import { RiskMetrics } from '../components/RiskMetrics'
import { NewsCard } from '../components/NewsCard'

export const Dashboard: React.FC = () => {
  const { user } = useAuth()
  const { portfolios, isLoading } = usePortfolio()

  if (isLoading) return <div>Loading...</div>

  const totalValue = portfolios.reduce((sum, p) => sum + parseFloat(p.total_value), 0)
  const totalReturn = portfolios.reduce((sum, p) => sum + parseFloat(p.total_return), 0)

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-8">Welcome, {user?.full_name}</h1>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-600">Total Portfolio Value</p>
          <p className="text-3xl font-bold text-primary">${totalValue.toFixed(2)}</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-600">Total Return</p>
          <p className={`text-3xl font-bold ${totalReturn >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            ${totalReturn.toFixed(2)}
          </p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-600">Number of Holdings</p>
          <p className="text-3xl font-bold">{portfolios.length}</p>
        </div>
      </div>

      {/* Charts and Data */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Portfolio Performance</h2>
          <PortfolioChart data={portfolios} />
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">Risk Metrics</h2>
          <RiskMetrics portfolios={portfolios} />
        </div>
      </div>

      {/* News Section */}
      <div className="mt-8 bg-white p-6 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4">Market News</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* News cards rendered here */}
        </div>
      </div>
    </div>
  )
}
```

### Portfolio Page

```typescript
// src/pages/Portfolio.tsx
import React, { useState } from 'react'
import { usePortfolio } from '../hooks/usePortfolio'
import { PortfolioCard } from '../components/Portfolio/PortfolioCard'
import { AddPortfolioForm } from '../components/Portfolio/AddPortfolioForm'

export const Portfolio: React.FC = () => {
  const { portfolios, refetch } = usePortfolio()
  const [showForm, setShowForm] = useState(false)

  const handleAddPortfolio = async (data: any) => {
    // API call to add portfolio
    await refetch()
    setShowForm(false)
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">My Portfolios</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-primary text-white px-6 py-2 rounded hover:bg-blue-600"
        >
          + New Portfolio
        </button>
      </div>

      {showForm && <AddPortfolioForm onSubmit={handleAddPortfolio} />}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {portfolios.map((portfolio) => (
          <PortfolioCard key={portfolio.id} portfolio={portfolio} />
        ))}
      </div>
    </div>
  )
}
```

### Stock Detail Page

```typescript
// src/pages/StockDetail.tsx
import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { Stock } from '../types'
import { getStock } from '../services/stocks'
import { PriceChart } from '../components/charts/PriceChart'
import { useWebSocket } from '../hooks/useWebSocket'

export const StockDetail: React.FC = () => {
  const { ticker } = useParams<{ ticker: string }>()
  const [stock, setStock] = useState<Stock | null>(null)
  const [price, setPrice] = useState<number | null>(null)

  useEffect(() => {
    const fetchStock = async () => {
      const data = await getStock(ticker!)
      setStock(data)
      setPrice(data.current_price)
    }
    fetchStock()
  }, [ticker])

  // Real-time price updates via WebSocket
  useWebSocket(`ws://localhost:8000/ws/stocks/${ticker}`, (data) => {
    if (data.type === 'price_update') {
      setPrice(data.price)
    }
  })

  if (!stock) return <div>Loading...</div>

  const priceChange = price ? ((price - stock.current_price) / stock.current_price) * 100 : 0

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h1 className="text-4xl font-bold">{stock.ticker}</h1>
            <p className="text-gray-600">{stock.name}</p>
          </div>
          <div className="text-right">
            <p className="text-4xl font-bold">${price?.toFixed(2)}</p>
            <p className={priceChange >= 0 ? 'text-green-600' : 'text-red-600'}>
              {priceChange > 0 ? '+' : ''}{priceChange.toFixed(2)}%
            </p>
          </div>
        </div>

        {/* Price Chart */}
        <div className="mb-8 h-96">
          <PriceChart ticker={ticker!} />
        </div>

        {/* Stock Info Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-gray-600">Market Cap</p>
            <p className="text-xl font-bold">${(stock.market_cap / 1e9).toFixed(2)}B</p>
          </div>
          <div>
            <p className="text-gray-600">P/E Ratio</p>
            <p className="text-xl font-bold">{stock.pe_ratio?.toFixed(2)}</p>
          </div>
          <div>
            <p className="text-gray-600">Dividend Yield</p>
            <p className="text-xl font-bold">{(stock.dividend_yield || 0).toFixed(2)}%</p>
          </div>
          <div>
            <p className="text-gray-600">Sector</p>
            <p className="text-xl font-bold">{stock.sector}</p>
          </div>
        </div>
      </div>
    </div>
  )
}
```

### Alert Component

```typescript
// src/components/Alerts/AlertForm.tsx
import React, { useState } from 'react'
import { createAlert } from '../../services/alerts'

interface AlertFormProps {
  ticker: string
  onSuccess?: () => void
}

export const AlertForm: React.FC<AlertFormProps> = ({ ticker, onSuccess }) => {
  const [alertType, setAlertType] = useState('price_target')
  const [value, setValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      await createAlert({
        ticker,
        alert_type: alertType,
        condition: { type: alertType === 'price_target' ? 'above' : 'change', value: parseFloat(value) }
      })
      onSuccess?.()
      setValue('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create alert')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-bold mb-4">Create Alert for {ticker}</h3>

      {error && <div className="text-red-600 mb-4">{error}</div>}

      <div className="mb-4">
        <label className="block text-gray-700 font-bold mb-2">Alert Type</label>
        <select
          value={alertType}
          onChange={(e) => setAlertType(e.target.value)}
          className="w-full border rounded px-3 py-2"
        >
          <option value="price_target">Price Target</option>
          <option value="percentage_change">Percentage Change</option>
        </select>
      </div>

      <div className="mb-4">
        <label className="block text-gray-700 font-bold mb-2">
          {alertType === 'price_target' ? 'Target Price' : 'Change Percentage'}
        </label>
        <input
          type="number"
          step="0.01"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          required
          className="w-full border rounded px-3 py-2"
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-primary text-white py-2 rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {isLoading ? 'Creating...' : 'Create Alert'}
      </button>
    </form>
  )
}
```

### Notification Bell Component

```typescript
// src/components/NotificationBell.tsx
import React, { useState, useEffect } from 'react'
import { useNotifications } from '../hooks/useNotifications'

export const NotificationBell: React.FC = () => {
  const { notifications, unreadCount } = useNotifications()
  const [showDropdown, setShowDropdown] = useState(false)

  return (
    <div className="relative">
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        className="relative p-2"
      >
        🔔
        {unreadCount > 0 && (
          <span className="absolute top-0 right-0 bg-red-600 text-white rounded-full w-5 h-5 text-xs flex items-center justify-center">
            {unreadCount}
          </span>
        )}
      </button>

      {showDropdown && (
        <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg p-4 z-50">
          <h3 className="font-bold mb-4">Notifications</h3>
          <div className="max-h-96 overflow-y-auto">
            {notifications.length === 0 ? (
              <p className="text-gray-500">No notifications</p>
            ) : (
              notifications.map((notif) => (
                <div
                  key={notif.id}
                  className="border-b pb-3 mb-3 last:border-0 hover:bg-gray-50 p-2 rounded"
                >
                  <p className="font-semibold">{notif.title}</p>
                  <p className="text-sm text-gray-600">{notif.message}</p>
                  <p className="text-xs text-gray-400 mt-1">{notif.created_at}</p>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  )
}
```

---

## 🎯 Phase 5 Summary

By end of Phase 5:
- ✅ Complete page implementations
- ✅ Reusable component patterns
- ✅ Forms and validation
- ✅ Real-time UI updates
- ✅ Responsive design with Tailwind
- ✅ Error handling and loading states
- ✅ Chart components and visualizations

**Next Phase**: [Advanced Topics](../06-advanced-topics/README.md)

