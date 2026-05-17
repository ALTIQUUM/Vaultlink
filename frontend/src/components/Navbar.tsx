import { Bell, Shield } from "lucide-react";

export function Navbar() {
  return <header className="flex h-16 items-center justify-between border-b border-slate-200 bg-white px-6"><div className="flex items-center gap-2 font-semibold"><Shield size={20} />VAULTLINK</div><button className="rounded-md p-2 hover:bg-slate-100" aria-label="Notifications"><Bell size={20} /></button></header>;
}
