import { Bell } from "lucide-react";

export function NotificationBell({ count }: { count: number }) {
  return <button className="relative rounded-md p-2 hover:bg-slate-100" aria-label="Notifications"><Bell size={20} />{count > 0 && <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-red-600" />}</button>;
}
