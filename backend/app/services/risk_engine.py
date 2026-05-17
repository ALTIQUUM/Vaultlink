from decimal import Decimal

import numpy as np
import pandas as pd
import yfinance as yf

from app.schemas.risk import CorrelationCell, PortfolioRisk, RiskMetric


class RiskEngine:
    def analyze(self, tickers: list[str]) -> PortfolioRisk:
        symbols = sorted(set(tickers)) or ["SPY"]
        prices = yf.download(symbols + ["SPY"], period="1y", progress=False, auto_adjust=True)["Close"].dropna()
        returns = prices.pct_change().dropna()
        metrics = [self._metric(symbol, returns[symbol], returns["SPY"]) for symbol in symbols]
        overall_returns = returns[symbols].mean(axis=1)
        overall = self._metric("PORTFOLIO", overall_returns, returns["SPY"])
        corr = returns[symbols].corr().fillna(0)
        cells = [CorrelationCell(ticker_a=a, ticker_b=b, correlation=Decimal(str(round(float(corr.loc[a, b]), 4)))) for a in symbols for b in symbols]
        score = Decimal(str(round(float(1 - np.mean(np.abs(corr.values[np.triu_indices_from(corr.values, 1)]))) if len(symbols) > 1 else 1, 4)))
        return PortfolioRisk(overall=overall, positions=metrics, correlation_matrix=cells, sector_diversification_score=score)

    def _metric(self, ticker: str, returns: pd.Series, benchmark: pd.Series) -> RiskMetric:
        aligned = pd.concat([returns, benchmark], axis=1).dropna()
        r = aligned.iloc[:, 0]
        b = aligned.iloc[:, 1]
        downside = r[r < 0]
        beta = float(np.cov(r, b)[0, 1] / np.var(b)) if np.var(b) else 0.0
        annual_return = float(r.mean() * 252)
        alpha = annual_return - beta * float(b.mean() * 252)
        cumulative = (1 + r).cumprod()
        drawdown = cumulative / cumulative.cummax() - 1
        return RiskMetric(
            ticker=ticker,
            sharpe_ratio=Decimal(str(round(float(r.mean() / r.std() * np.sqrt(252)) if r.std() else 0, 4))),
            sortino_ratio=Decimal(str(round(float(r.mean() / downside.std() * np.sqrt(252)) if len(downside) and downside.std() else 0, 4))),
            volatility_30d=Decimal(str(round(float(r.tail(30).std() * np.sqrt(252)), 4))),
            volatility_90d=Decimal(str(round(float(r.tail(90).std() * np.sqrt(252)), 4))),
            beta=Decimal(str(round(beta, 4))),
            alpha=Decimal(str(round(alpha, 4))),
            max_drawdown=Decimal(str(round(float(drawdown.min()), 4))),
            recovery_days=int((drawdown < 0).astype(int).groupby((drawdown == 0).cumsum()).sum().max()),
            value_at_risk_95=Decimal(str(round(float(np.percentile(r, 5)), 4))),
        )
