import { Table } from "../components/ui/Table";

export function Screener() {
  return <Table headers={["Ticker", "Sector", "Market Cap", "P/E"]}><tr><td className="px-4 py-3">NVDA</td><td className="px-4 py-3">Technology</td><td className="px-4 py-3">$2.7T</td><td className="px-4 py-3">64.2</td></tr></Table>;
}
