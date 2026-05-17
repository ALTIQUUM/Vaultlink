import { PortfolioChart } from "../components/charts/PortfolioChart";
import { RiskHeatmap } from "../components/charts/RiskHeatmap";
import { Card } from "../components/ui/Card";

export function Dashboard() {
  return <div className="grid gap-4 lg:grid-cols-3"><Card className="lg:col-span-2"><h1 className="mb-4 text-xl font-semibold">Portfolio performance</h1><PortfolioChart /></Card><Card><h2 className="mb-4 font-semibold">Correlation</h2><RiskHeatmap /></Card></div>;
}
