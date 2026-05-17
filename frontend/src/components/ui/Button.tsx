import type { ButtonHTMLAttributes, ReactNode } from "react";

type Props = ButtonHTMLAttributes<HTMLButtonElement> & { children: ReactNode; tone?: "primary" | "quiet" | "danger" };

export function Button({ children, tone = "primary", className = "", ...props }: Props) {
  const styles = {
    primary: "bg-slate-950 text-white hover:bg-slate-800",
    quiet: "bg-white text-slate-900 border border-slate-200 hover:bg-slate-50",
    danger: "bg-red-600 text-white hover:bg-red-700",
  };
  return <button className={`inline-flex h-10 items-center justify-center rounded-md px-4 text-sm font-medium transition ${styles[tone]} ${className}`} {...props}>{children}</button>;
}
