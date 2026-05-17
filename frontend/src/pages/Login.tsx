import { Button } from "../components/ui/Button";

export function Login() {
  return <div className="mx-auto max-w-md space-y-4 p-6"><h1 className="text-2xl font-semibold">Sign in</h1><input className="w-full rounded-md border p-3" placeholder="Email" /><input className="w-full rounded-md border p-3" type="password" placeholder="Password" /><Button>Continue</Button></div>;
}
