import { Button } from "./ui/Button";

export function AlertForm() {
  return <form className="grid gap-3 sm:grid-cols-4"><input className="rounded-md border p-2" placeholder="Ticker" /><select className="rounded-md border p-2"><option>price_above</option><option>price_below</option><option>percent_change</option></select><input className="rounded-md border p-2" placeholder="Threshold" /><Button>Create</Button></form>;
}
