import { Table } from "../components/ui/Table";
import { currency } from "../utils/formatters";

const rows = [{ ticker: "AAPL", quantity: 20, price: 192.4, value: 3848 }, { ticker: "MSFT", quantity: 8, price: 430.2, value: 3441.6 }];

export function Portfolio() {
  return <Table headers={["Ticker", "Quantity", "Price", "Value"]}>{rows.map((row) => <tr key={row.ticker}><td className="px-4 py-3 font-medium">{row.ticker}</td><td className="px-4 py-3">{row.quantity}</td><td className="px-4 py-3">{currency(row.price)}</td><td className="px-4 py-3">{currency(row.value)}</td></tr>)}</Table>;
}
