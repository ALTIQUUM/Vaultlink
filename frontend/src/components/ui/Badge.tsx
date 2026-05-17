export function Badge({ children }: { children: string }) {
  return <span className="inline-flex rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-medium text-emerald-700">{children}</span>;
}
