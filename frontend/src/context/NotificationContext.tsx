import { createContext, useMemo, useState, type Dispatch, type ReactNode, type SetStateAction } from "react";

type NotificationState = { count: number; setCount: Dispatch<SetStateAction<number>> };

export const NotificationContext = createContext<NotificationState>({ count: 0, setCount: () => undefined });

export function NotificationProvider({ children }: { children: ReactNode }) {
  const [count, setCount] = useState(0);
  const value = useMemo(() => ({ count, setCount }), [count]);
  return <NotificationContext.Provider value={value}>{children}</NotificationContext.Provider>;
}
