import { request } from "./api";
import type { TokenPair, User } from "../types";

export const authApi = {
  register: (email: string, full_name: string, password: string) =>
    request<User>("/auth/register", { method: "POST", body: JSON.stringify({ email, full_name, password }) }),
  login: (email: string, password: string) =>
    request<TokenPair>("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
  logoutAll: () => request<void>("/auth/logout-all", { method: "POST" }),
};
