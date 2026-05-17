export type TokenPair = { access_token: string; refresh_token: string; token_type: "bearer" };
export type User = { id: number; email: string; full_name: string; role: string; is_verified: boolean };
export type Position = {
  id: number;
  ticker: string;
  quantity: string;
  average_cost: string;
  current_price: string;
  market_value: string;
  unrealized_gain: string;
  realized_gain: string;
};
export type Portfolio = {
  id: number;
  name: string;
  currency: string;
  total_value: string;
  total_cost: string;
  unrealized_gain: string;
  realized_gain: string;
  positions: Position[];
};
export type StockQuote = { ticker: string; price: string; currency: string; change_percent: string | null; source: string; captured_at: string };
export type RiskMetric = { ticker: string; sharpe_ratio: string; sortino_ratio: string; volatility_30d: string; volatility_90d: string; beta: string; alpha: string; max_drawdown: string; value_at_risk_95: string };
export type Alert = { id: number; ticker: string; kind: "price_above" | "price_below" | "percent_change"; threshold: string; is_active: boolean; last_triggered_at: string | null };
export type NewsItem = { ticker: string; title: string; url: string; source: string; published_at: string; sentiment: number };
