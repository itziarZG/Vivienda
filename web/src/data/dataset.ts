import fs from "node:fs";
import path from "node:path";

export interface IslaStats {
  isla: string;
  secciones: number;
  airbnb_listings: number;
  airbnb_entire_homes: number;
  airbnb_revenue_total: number;
  airbnb_hosts_unicos: number;
  airbnb_con_licencia: number;
  hut_registros: number;
  hut_plazas: number;
}

export interface WebDataset {
  resumen_por_isla: IslaStats[];
}

function load(): WebDataset {
  const file = path.resolve(
    process.cwd(),
    "public/data/dataset_web.json",
  );
  const raw = fs.readFileSync(file, "utf-8");
  return JSON.parse(raw) as WebDataset;
}

let cached: WebDataset | null = null;
export function getDataset(): WebDataset {
  if (!cached) cached = load();
  return cached;
}

export function totals(d: WebDataset) {
  const t = {
    airbnb_listings: 0,
    airbnb_entire_homes: 0,
    airbnb_revenue_total: 0,
    airbnb_hosts_unicos: 0,
    airbnb_con_licencia: 0,
    hut_registros: 0,
    hut_plazas: 0,
    secciones: 0,
  };
  for (const r of d.resumen_por_isla) {
    t.airbnb_listings += r.airbnb_listings;
    t.airbnb_entire_homes += r.airbnb_entire_homes;
    t.airbnb_revenue_total += r.airbnb_revenue_total;
    t.airbnb_hosts_unicos += r.airbnb_hosts_unicos;
    t.airbnb_con_licencia += r.airbnb_con_licencia;
    t.hut_registros += r.hut_registros;
    t.hut_plazas += r.hut_plazas;
    t.secciones += r.secciones;
  }
  return t;
}
