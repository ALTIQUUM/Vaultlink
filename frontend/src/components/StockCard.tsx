import type { StockQuote } from "../types";
import { currency, percent } from "../utils/formatters";
import { Card } from "./ui/Card";

export function StockCard({ quote }: { quote: StockQuote }) {
  return <Card><div className="flex items-center justify-between"><div><p className="text-sm text-slate-500">{quote.ticker}</p><p className="text-2xl font-semibold">{currency(quote.price, quote.currency)}</p></div><p className="text-sm font-medium text-emerald-600">{quote.change_percent ? percent(quote.change_percent) : "0.00%"}</p></div></Card>;
}
