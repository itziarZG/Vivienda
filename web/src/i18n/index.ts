import ca from "./ca.json";
import es from "./es.json";

export type Lang = "ca" | "es";
export type Dict = typeof ca;

const DICTS: Record<Lang, Dict> = { ca, es };

export function getLangFromCookies(
  cookieHeader: string | null | undefined,
): Lang {
  if (!cookieHeader) return "ca";
  const m = cookieHeader.match(/(?:^|;\s*)lang=([a-z]{2})/);
  if (m && (m[1] === "ca" || m[1] === "es")) return m[1];
  return "ca";
}

export function getLangFromAstroCookies(
  cookies: { get(name: string): { value: string } | undefined },
): Lang {
  const c = cookies.get("lang");
  if (c && (c.value === "ca" || c.value === "es")) return c.value;
  return "ca";
}

export function t(lang: Lang, key: string): string {
  const dict = DICTS[lang];
  const parts = key.split(".");
  let cur: unknown = dict;
  for (const p of parts) {
    if (cur && typeof cur === "object" && p in (cur as Record<string, unknown>)) {
      cur = (cur as Record<string, unknown>)[p];
    } else {
      return key;
    }
  }
  return typeof cur === "string" ? cur : key;
}

export function format(lang: Lang, key: string, vars: Record<string, string | number>): string {
  let s = t(lang, key);
  for (const [k, v] of Object.entries(vars)) {
    s = s.replaceAll(`{${k}}`, String(v));
  }
  return s;
}
