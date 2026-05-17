import type { RiskMetric } from "../types";
import { Card } from "./ui/Card";

export function RiskMetrics({ metric }: { metric: RiskMetric }) {
  const rows = [["Sharpe", metric.sharpe_ratio], ["Sortino", metric.sortino_ratio], ["Beta", metric.beta], ["VaR 95", metric.value_at_risk_95]];
  return <Card><h3 className="mb-3 font-semibold">{metric.ticker} Risk</h3><div className="grid grid-cols-2 gap-3">{rows.map(([k, v]) => <div key={k}><p className="text-xs text-slate-500">{k}</p><p className="font-semibold">{v}</p></div>)}</div></Card>;
}
