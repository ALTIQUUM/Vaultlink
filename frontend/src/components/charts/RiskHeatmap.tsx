const cells = ["AAPL", "MSFT", "NVDA", "JPM"].flatMap((a, i, arr) => arr.map((b, j) => ({ a, b, v: i === j ? 1 : 0.35 + ((i + j) % 4) * 0.14 })));

export function RiskHeatmap() {
  return <div className="grid grid-cols-4 gap-1">{cells.map((c) => <div key={`${c.a}-${c.b}`} className="grid h-16 place-items-center rounded text-xs font-medium text-white" style={{ backgroundColor: `rgba(15,23,42,${c.v})` }}>{c.a}/{c.b}</div>)}</div>;
}
