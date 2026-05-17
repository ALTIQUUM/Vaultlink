import type { ReactNode } from "react";
import { Button } from "./Button";

export function Modal({ open, title, children, onClose }: { open: boolean; title: string; children: ReactNode; onClose: () => void }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-50 grid place-items-center bg-black/40 p-4">
      <div className="w-full max-w-lg rounded-lg bg-white p-5 shadow-xl">
        <div className="mb-4 flex items-center justify-between"><h2 className="text-lg font-semibold">{title}</h2><Button tone="quiet" onClick={onClose}>Close</Button></div>
        {children}
      </div>
    </div>
  );
}
