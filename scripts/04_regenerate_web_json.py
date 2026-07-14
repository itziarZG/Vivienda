"""
Regenera data/output/dataset_web.json con sumas correctas a nivel isla.

Bug original en 02_build_dataset.py: para Eivissa/Formentera hace SUM
de `hut_registros` y `hut_plazas` por seccion censal, pero el valor se
replica a todas las secciones del mismo municipio -> multiplica.

Este script:
- Para Mallorca/Menorca: usa SUM del parquet (correcto, granularidad seccion).
- Para Eivissa: lee el CSV raw `hut_eivissa_2026-07-14.csv` y agrega por municipio.
- Para Formentera: lee el JSON raw `ibestat_formentera_2019.json` (1 fila).

Salida: data/output/dataset_web.json con la misma estructura que antes.
"""

from pathlib import Path
import json

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "output"


def huts_eivissa_total() -> dict:
    """Total HUT Eivissa a nivel isla (sin duplicar por seccion)."""
    df = pd.read_csv(RAW / "hut_eivissa_2026-07-14.csv")
    df = df[df["Municipi"] != "NUEVO BOLSA DE PLAZAS"].copy()
    df["plazas"] = pd.to_numeric(df["Total Places"], errors="coerce").fillna(0).astype(int)
    return {
        "registros": int(len(df)),
        "plazas": int(df["plazas"].sum()),
    }


def formentera_total() -> dict:
    """Total Formentera a nivel isla (1 municipio)."""
    with open(RAW / "ibestat_formentera_2019.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        "registros": int(data["metadata"]["total_unidades"]),
        "plazas": int(data["metadata"]["total_plazas"]),
    }


def airbnb_por_isla() -> dict:
    """Total Airbnb por isla desde el parquet (SUM por seccion es correcto)."""
    df = pd.read_parquet(OUT / "dataset.parquet")
    mall = df[df["isla"] == "Mallorca"]
    men = df[df["isla"] == "Menorca"]
    return {
        "Mallorca": {
            "listings": int(mall["airbnb_listings"].sum()),
            "entire_homes": int(mall["airbnb_entire_homes"].sum()),
            "revenue_total": int(mall["airbnb_revenue_total"].sum()),
            "hosts_unicos": int(mall["airbnb_hosts_unicos"].sum()),
            "con_licencia": int(mall["airbnb_con_licencia"].sum()),
        },
        "Menorca": {
            "listings": int(men["airbnb_listings"].sum()),
            "entire_homes": int(men["airbnb_entire_homes"].sum()),
            "revenue_total": int(men["airbnb_revenue_total"].sum()),
            "hosts_unicos": int(men["airbnb_hosts_unicos"].sum()),
            "con_licencia": int(men["airbnb_con_licencia"].sum()),
        },
    }


def main() -> None:
    print("=== Regenerando dataset_web.json ===\n")
    df = pd.read_parquet(OUT / "dataset.parquet")
    eiv = huts_eivissa_total()
    fmr = formentera_total()
    ab = airbnb_por_isla()
    print(f"HUT Eivissa: {eiv['registros']:,} registros, {eiv['plazas']:,} plazas")
    print(f"IBESTAT Formentera: {fmr['registros']:,} unidades, {fmr['plazas']:,} plazas")
    print(f"Airbnb Mallorca: {ab['Mallorca']['listings']:,} listings, "
          f"{ab['Mallorca']['entire_homes']:,} entire home/apt")
    print(f"Airbnb Menorca: {ab['Menorca']['listings']:,} listings, "
          f"{ab['Menorca']['entire_homes']:,} entire home/apt")

    resumen = []
    isla_meta = df.groupby("isla").size().to_dict()
    for isla in ["Mallorca", "Menorca", "Eivissa", "Formentera"]:
        record = {
            "isla": isla,
            "secciones": int(isla_meta.get(isla, 0)),
            "airbnb_listings": 0,
            "airbnb_entire_homes": 0,
            "airbnb_revenue_total": 0,
            "airbnb_hosts_unicos": 0,
            "airbnb_con_licencia": 0,
            "hut_registros": 0,
            "hut_plazas": 0,
        }
        if isla in ("Mallorca", "Menorca"):
            record["airbnb_listings"] = ab[isla]["listings"]
            record["airbnb_entire_homes"] = ab[isla]["entire_homes"]
            record["airbnb_revenue_total"] = ab[isla]["revenue_total"]
            record["airbnb_hosts_unicos"] = ab[isla]["hosts_unicos"]
            record["airbnb_con_licencia"] = ab[isla]["con_licencia"]
        if isla == "Eivissa":
            record["hut_registros"] = eiv["registros"]
            record["hut_plazas"] = eiv["plazas"]
        if isla == "Formentera":
            record["hut_registros"] = fmr["registros"]
            record["hut_plazas"] = fmr["plazas"]
        resumen.append(record)

    out = {"resumen_por_isla": resumen}
    with open(OUT / "dataset_web.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\nGuardado {OUT / 'dataset_web.json'}")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
