from dataclasses import dataclass
from decimal import Decimal

import yfinance as yf


@dataclass(frozen=True)
class ScreenerFilter:
    sector: str | None = None
    min_market_cap: int | None = None
    max_pe_ratio: Decimal | None = None
    min_volume: int | None = None


class ScreenerService:
    def screen(
        self, tickers: list[str], filters: ScreenerFilter
    ) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        for ticker in tickers:
            info = yf.Ticker(ticker).get_info()
            row = {
                "ticker": ticker,
                "name": info.get("shortName") or ticker,
                "sector": info.get("sector"),
                "market_cap": info.get("marketCap") or 0,
                "pe_ratio": info.get("trailingPE"),
                "volume": info.get("volume") or 0,
            }
            if filters.sector and row["sector"] != filters.sector:
                continue
            if (
                filters.min_market_cap
                and int(row["market_cap"]) < filters.min_market_cap
            ):
                continue
            if (
                filters.max_pe_ratio
                and row["pe_ratio"]
                and Decimal(str(row["pe_ratio"])) > filters.max_pe_ratio
            ):
                continue
            if filters.min_volume and int(row["volume"]) < filters.min_volume:
                continue
            rows.append(row)
        return sorted(rows, key=lambda item: int(item["market_cap"]), reverse=True)
