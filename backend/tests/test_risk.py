import pandas as pd

from app.services.risk_engine import RiskEngine


def test_risk_metric_handles_flat_benchmark() -> None:
    returns = pd.Series([0.01, -0.02, 0.03, 0.01])
    benchmark = pd.Series([0.0, 0.0, 0.0, 0.0])
    metric = RiskEngine()._metric("TEST", returns, benchmark)
    assert metric.ticker == "TEST"
    assert metric.recovery_days >= 0
