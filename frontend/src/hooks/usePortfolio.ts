import { useEffect, useState } from "react";
import { portfolioApi } from "../services/portfolio";
import type { Portfolio } from "../types";

export function usePortfolio(id: number) {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    portfolioApi.get(id).then(setPortfolio).finally(() => setLoading(false));
  }, [id]);
  return { portfolio, loading };
}
