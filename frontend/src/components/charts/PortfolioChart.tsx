import { Area, AreaChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const data = [
  { date: "Mon", value: 104000 },
  { date: "Tue", value: 106400 },
  { date: "Wed", value: 105800 },
  { date: "Thu", value: 109200 },
  { date: "Fri", value: 111740 },
];

export function PortfolioChart() {
  return <ResponsiveContainer width="100%" height={260}><AreaChart data={data}><XAxis dataKey="date" /><YAxis /><Tooltip /><Area type="monotone" dataKey="value" stroke="#0f172a" fill="#cbd5e1" /></AreaChart></ResponsiveContainer>;
}
