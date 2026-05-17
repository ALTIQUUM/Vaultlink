import { StockCard } from "../components/StockCard";

const quotes = ["AAPL", "MSFT", "NVDA"].map((ticker) => ({ ticker, price: "190.00", currency: "USD", change_percent: "1.24", source: "cache", captured_at: new Date().toISOString() }));

export function Watchlist() {
  return <div className="grid gap-4 md:grid-cols-3">{quotes.map((quote) => <StockCard key={quote.ticker} quote={quote} />)}</div>;
}
