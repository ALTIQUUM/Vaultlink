import { Card } from "../components/ui/Card";

export function Admin() {
  return <div className="grid gap-4 md:grid-cols-3">{["Users 128", "Portfolios 74", "API calls 18.2k"].map((item) => <Card key={item}><p className="text-sm text-slate-500">{item.split(" ")[0]}</p><p className="text-2xl font-semibold">{item.split(" ").slice(1).join(" ")}</p></Card>)}</div>;
}
