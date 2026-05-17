const items = ["Dashboard", "Portfolio", "Watchlist", "Screener", "Alerts", "Admin"];

export function Sidebar({ current, onSelect }: { current: string; onSelect: (page: string) => void }) {
  return <aside className="hidden w-64 border-r border-slate-200 bg-white p-4 md:block">{items.map((item) => <button key={item} onClick={() => onSelect(item)} className={`mb-1 block w-full rounded-md px-3 py-2 text-left text-sm ${current === item ? "bg-slate-950 text-white" : "hover:bg-slate-100"}`}>{item}</button>)}</aside>;
}
