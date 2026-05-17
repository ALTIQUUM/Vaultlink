import re

TICKER_RE = re.compile(r"^[A-Z][A-Z0-9.\-]{0,14}$")


def normalize_ticker(ticker: str) -> str:
    value = ticker.strip().upper()
    if not TICKER_RE.match(value):
        raise ValueError("Ticker must be 1-15 uppercase market symbols")
    return value
