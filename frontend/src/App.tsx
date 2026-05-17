import { motion } from "framer-motion";
import { useState } from "react";
import { Navbar } from "./components/Navbar";
import { Sidebar } from "./components/Sidebar";
import { Admin } from "./pages/Admin";
import { Alerts } from "./pages/Alerts";
import { Dashboard } from "./pages/Dashboard";
import { Portfolio } from "./pages/Portfolio";
import { Screener } from "./pages/Screener";
import { Watchlist } from "./pages/Watchlist";

const pages = { Dashboard, Portfolio, Watchlist, Screener, Alerts, Admin };

export function App() {
  const [page, setPage] = useState<keyof typeof pages>("Dashboard");
  const Page = pages[page];
  return <div className="min-h-screen"><Navbar /><div className="flex"><Sidebar current={page} onSelect={(next) => setPage(next as keyof typeof pages)} /><main className="flex-1 p-4 md:p-6"><motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} key={page}><Page /></motion.div></main></div></div>;
}
