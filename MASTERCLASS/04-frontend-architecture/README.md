# Phase 4: Frontend Architecture 🎨

## Commits 32-40: React, TypeScript, and State Management

This phase covers React component patterns, TypeScript setup, and state management using Context API and hooks.

### React Project Structure

```
frontend/src/
├── main.tsx                    # Entry point
├── App.tsx                     # Root component
├── styles.css                  # Global styles
├── components/
│   ├── Layout/
│   │   ├── Navbar.tsx
│   │   ├── Sidebar.tsx
│   │   └── Footer.tsx
│   ├── Common/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Modal.tsx
│   │   └── Spinner.tsx
│   ├── Stock/
│   │   ├── StockCard.tsx
│   │   ├── StockTable.tsx
│   │   └── PriceChart.tsx
│   ├── Portfolio/
│   │   ├── PortfolioCard.tsx
│   │   ├── PortfolioChart.tsx
│   │   └── PositionCard.tsx
│   ├── Alerts/
│   │   ├── AlertForm.tsx
│   │   ├── AlertList.tsx
│   │   └── NotificationBell.tsx
│   └── charts/
│       ├── LineChart.tsx
│       ├── PieChart.tsx
│       └── BarChart.tsx
├── pages/
│   ├── Login.tsx
│   ├── Register.tsx
│   ├── Dashboard.tsx
│   ├── Portfolio.tsx
│   ├── StockDetail.tsx
│   ├── Watchlist.tsx
│   ├── Alerts.tsx
│   ├── Screener.tsx
│   └── Admin.tsx
├── context/
│   ├── AuthContext.tsx         # Auth state
│   ├── NotificationContext.tsx # Notifications/alerts
│   └── PortfolioContext.tsx    # Portfolio data
├── hooks/
│   ├── useAuth.ts
│   ├── useNotifications.ts
│   ├── usePortfolio.ts
│   ├── useWebSocket.ts
│   └── useFetch.ts
├── services/
│   ├── api.ts                  # Axios instance
│   ├── auth.ts                 # Auth API calls
│   ├── portfolio.ts            # Portfolio API
│   ├── stocks.ts               # Stock API
│   └── alerts.ts               # Alert API
├── types/
│   └── index.ts                # TypeScript definitions
├── utils/
│   ├── constants.ts
│   ├── formatters.ts           # Number, date formatting
│   ├── validators.ts           # Form validation
│   └── helpers.ts              # Utility functions
└── vite-env.d.ts               # Vite type definitions
```

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    
    // Strict mode for type safety
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    
    // Module resolution
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx"
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### Type Definitions

```typescript
// src/types/index.ts
export interface User {
  id: string
  email: string
  username: string
  full_name: string
  is_active: boolean
  created_at: string
}

export interface Stock {
  id: string
  ticker: string
  name: string
  current_price: number
  market_cap: number
  sector: string
  change_percent: number
}

export interface Portfolio {
  id: string
  name: string
  total_value: number
  total_return: number
  return_percentage: number
  positions: Position[]
}

export interface Position {
  id: string
  ticker: string
  quantity: number
  average_cost: number
  current_price: number
  unrealized_gain_loss: number
  unrealized_percentage: number
}

export interface Alert {
  id: string
  ticker: string
  alert_type: string
  condition: Record<string, any>
  status: 'active' | 'triggered' | 'paused'
}
```

### Context API Setup

```typescript
// src/context/AuthContext.tsx
import React, { createContext, useReducer, ReactNode } from 'react'
import { User } from '../types'

interface AuthContextType {
  user: User | null
  token: string | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  register: (data: any) => Promise<void>
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined)

type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: { user: User; token: string } }
  | { type: 'LOGIN_ERROR' }
  | { type: 'LOGOUT' }

interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
}

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, isLoading: true }
    case 'LOGIN_SUCCESS':
      return {
        user: action.payload.user,
        token: action.payload.token,
        isLoading: false
      }
    case 'LOGOUT':
      return { user: null, token: null, isLoading: false }
    default:
      return state
  }
}

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, {
    user: null,
    token: localStorage.getItem('token'),
    isLoading: false
  })

  const login = async (email: string, password: string) => {
    dispatch({ type: 'LOGIN_START' })
    try {
      const response = await api.post('/auth/login', { email, password })
      const { access_token, user } = response.data
      localStorage.setItem('token', access_token)
      dispatch({ type: 'LOGIN_SUCCESS', payload: { user, token: access_token } })
    } catch (error) {
      dispatch({ type: 'LOGIN_ERROR' })
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    dispatch({ type: 'LOGOUT' })
  }

  return (
    <AuthContext.Provider value={{ ...state, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}
```

### Custom Hooks

```typescript
// src/hooks/useAuth.ts
import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

// src/hooks/usePortfolio.ts
import { useState, useEffect } from 'react'
import { Portfolio } from '../types'
import { getPortfolios } from '../services/portfolio'

export const usePortfolio = () => {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchPortfolios()
  }, [])

  const fetchPortfolios = async () => {
    setIsLoading(true)
    try {
      const data = await getPortfolios()
      setPortfolios(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setIsLoading(false)
    }
  }

  return { portfolios, isLoading, error, refetch: fetchPortfolios }
}

// src/hooks/useWebSocket.ts
import { useEffect, useCallback } from 'react'

export const useWebSocket = (url: string, onMessage: (data: any) => void) => {
  useEffect(() => {
    const ws = new WebSocket(url)

    ws.onopen = () => console.log('WebSocket connected')
    ws.onmessage = (event) => onMessage(JSON.parse(event.data))
    ws.onerror = (error) => console.error('WebSocket error:', error)

    return () => ws.close()
  }, [url, onMessage])
}
```

### API Client Layer

```typescript
// src/services/api.ts
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

### Tailwind CSS Setup

```javascript
// tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#10B981',
        danger: '#EF4444'
      }
    }
  },
  plugins: []
}
```

---

## 🎯 Phase 4 Summary

By end of Phase 4:
- ✅ React component architecture
- ✅ TypeScript strict mode usage
- ✅ Context API for state management
- ✅ Custom hooks patterns
- ✅ API client configuration
- ✅ Form handling and validation
- ✅ Tailwind CSS utility usage

**Next Phase**: [Frontend Components](../05-frontend-components/README.md)

