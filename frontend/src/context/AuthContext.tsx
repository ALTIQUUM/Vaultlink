import { createContext, useMemo, useState, type ReactNode } from "react";
import type { User } from "../types";

export type AuthState = { user: User | null; setUser: (user: User | null) => void };
export const AuthContext = createContext<AuthState>({ user: null, setUser: () => undefined });

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const value = useMemo(() => ({ user, setUser }), [user]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
