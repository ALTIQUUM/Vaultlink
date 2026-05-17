from decimal import Decimal

from pydantic import BaseModel


class RiskMetric(BaseModel):
    ticker: str
    sharpe_ratio: Decimal
    sortino_ratio: Decimal
    volatility_30d: Decimal
    volatility_90d: Decimal
    beta: Decimal
    alpha: Decimal
    max_drawdown: Decimal
    recovery_days: int
    value_at_risk_95: Decimal


class CorrelationCell(BaseModel):
    ticker_a: str
    ticker_b: str
    correlation: Decimal


class PortfolioRisk(BaseModel):
    overall: RiskMetric
    positions: list[RiskMetric]
    correlation_matrix: list[CorrelationCell]
    sector_diversification_score: Decimal
