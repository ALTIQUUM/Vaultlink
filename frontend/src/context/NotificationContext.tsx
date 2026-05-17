import { createContext, useMemo, useState, type ReactNode } from "react";

export const NotificationContext = createContext({ count: 0, setCount: (_count: number) => undefined });

export function NotificationProvider({ children }: { children: ReactNode }) {
  const [count, setCount] = useState(0);
  const value = useMemo(() => ({ count, setCount }), [count]);
  return <NotificationContext.Provider value={value}>{children}</NotificationContext.Provider>;
}
