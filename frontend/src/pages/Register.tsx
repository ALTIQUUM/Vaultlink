import { Button } from "../components/ui/Button";

export function Register() {
  return <div className="mx-auto max-w-md space-y-4 p-6"><h1 className="text-2xl font-semibold">Create account</h1><input className="w-full rounded-md border p-3" placeholder="Full name" /><input className="w-full rounded-md border p-3" placeholder="Email" /><input className="w-full rounded-md border p-3" type="password" placeholder="Password" /><Button>Create</Button></div>;
}
