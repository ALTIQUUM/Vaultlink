import { AlertForm } from "../components/AlertForm";
import { Card } from "../components/ui/Card";

export function Alerts() {
  return <Card><h1 className="mb-4 text-xl font-semibold">Alerts</h1><AlertForm /><p className="mt-6 text-sm text-slate-500">No triggered alerts yet.</p></Card>;
}
