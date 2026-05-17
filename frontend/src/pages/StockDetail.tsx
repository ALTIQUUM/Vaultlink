import { PriceChart } from "../components/charts/PriceChart";
import { Card } from "../components/ui/Card";

export function StockDetail() {
  return <Card><h1 className="mb-4 text-xl font-semibold">AAPL</h1><PriceChart /></Card>;
}
