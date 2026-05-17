import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis } from "recharts";

const data = Array.from({ length: 20 }, (_, i) => ({ t: i + 1, price: 180 + Math.sin(i / 2) * 4 + i * 0.7 }));

export function PriceChart() {
  return <ResponsiveContainer width="100%" height={220}><LineChart data={data}><XAxis dataKey="t" /><Tooltip /><Line type="monotone" dataKey="price" stroke="#2563eb" strokeWidth={2} dot={false} /></LineChart></ResponsiveContainer>;
}
