export function currency(value: string | number, code = "USD"): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: code }).format(Number(value));
}

export function percent(value: string | number): string {
  return `${Number(value).toFixed(2)}%`;
}
