import type { NewsItem, StockQuote } from "../types";
import { request } from "./api";

export const stocksApi = {
  quote: (ticker: string) => request<StockQuote>(`/stocks/${ticker}/quote`),
  news: (ticker: string) => request<NewsItem[]>(`/news/${ticker}`),
};
