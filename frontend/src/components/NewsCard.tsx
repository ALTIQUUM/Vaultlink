import type { NewsItem } from "../types";

export function NewsCard({ item }: { item: NewsItem }) {
  return <a className="block rounded-lg border border-slate-200 bg-white p-4 hover:border-slate-400" href={item.url} target="_blank" rel="noreferrer"><p className="text-sm text-slate-500">{item.source}</p><h3 className="font-medium">{item.title}</h3><p className="text-xs text-slate-500">Sentiment {item.sentiment.toFixed(2)}</p></a>;
}
