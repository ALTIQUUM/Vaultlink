from decimal import Decimal

from app.utils.helpers import money, percent
from app.utils.validators import normalize_ticker


def test_financial_rounding_helpers() -> None:
    assert money(Decimal("10.115")) == Decimal("10.12")
    assert percent(Decimal("0.123456")) == Decimal("0.1235")


def test_ticker_normalization() -> None:
    assert normalize_ticker(" aapl ") == "AAPL"
