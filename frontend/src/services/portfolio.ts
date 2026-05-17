import type { Portfolio } from "../types";
import { request } from "./api";

export const portfolioApi = {
  create: (name: string, currency = "USD") => request<{ id: number }>("/portfolio", { method: "POST", body: JSON.stringify({ name, currency }) }),
  get: (id: number) => request<Portfolio>(`/portfolio/${id}`),
};
