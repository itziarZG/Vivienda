"""
Pipeline de datos - Cases Tancades
Carga todas las fuentes de datos y produce el dataset final por seccion censal.

Entradas (data/raw/):
- viviendas vacias-hiopotecas.xlsx (INE, CCAA)
- 39365(1).xlsx (INE, CCAA serie temporal)
- secciones_balears.gpkg (shapefile procesado, 674 secciones)
- airbnb_mallorca_listings.csv.gz (Inside Airbnb)
- airbnb_menorca_listings.csv.gz (Inside Airbnb)
- hut_eivissa_2026-07-14.csv (HUT oficial, con Ref. Catastral)
- ibestat_formentera_2019.json (IBESTAT agregado)

Salidas (data/output/):
- dataset.parquet (tabla final por seccion censal)
- dataset.json (version simplificada para web)
- stats.md (estadisticas descriptivas)
"""

from pathlib import Path
import json
import warnings

import pandas as pd
import geopandas as gpd
import duckdb

warnings.filterwarnings('ignore')

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
OUT = Path(__file__).resolve().parent.parent / "data" / "output"
OUT.mkdir(parents=True, exist_ok=True)


def load_ine_vivienda() -> dict:
    """Carga XLSX tabla-59531 (vivienda por intensidad de uso, CCAA)."""
    import openpyxl
    wb = openpyxl.load_workbook(RAW / "viviendas vacias-hiopotecas.xlsx", read_only=True, data_only=True)
    ws = wb["tabla-59531"]
    rows = list(ws.iter_rows(values_only=True))
    # header en row 7 (index 6)
    header = list(rows[6])
    # data en row 8 (index 7) y 9 (index 8)
    balears = dict(zip(header, rows[8]))
    nacional = dict(zip(header, rows[7]))
    wb.close()
    # Calcular porcentajes
    balears["pct_vacias"] = balears["Viviendas vacías"] / balears["Viviendas totales"] * 100
    balears["pct_uso_esporadico"] = balears["Viviendas de uso esporádico"] / balears["Viviendas totales"] * 100
    return {"balears": balears, "nacional": nacional}


def load_ine_vivienda_turistica() -> pd.DataFrame:
    """Carga XLSX tabla-39365 (vivienda turistica, CCAA serie temporal)."""
    import openpyxl
    wb = openpyxl.load_workbook(RAW / "39365(1).xlsx", read_only=True, data_only=True)
    ws = wb["tabla-39365"]
    rows = list(ws.iter_rows(values_only=True))
    # header en row 7 (index 6) - meses como columnas
    header = list(rows[6])
    # data en row 8 (Total Nacional) y 9 (Balears)
    balears_row = list(rows[8])
    nacional_row = list(rows[7])
    wb.close()
    # Solo nos interesa la serie de Balears
    balears = []
    for h, v in zip(header[1:], balears_row[1:]):
        balears.append({"periodo": h, "pct_viviendas_turisticas": float(v) if v else None})
    df = pd.DataFrame(balears)
    df["ambito"] = "Balears, Illes"
    return df


def load_shapefile() -> gpd.GeoDataFrame:
    """Carga el shapefile procesado de Balears."""
    gdf = gpd.read_file(RAW / "secciones_balears.gpkg")
    print(f"Shapefile: {len(gdf)} features, CRS={gdf.crs}")
    return gdf


def load_airbnb(isla: str) -> pd.DataFrame:
    """Carga listings de Inside Airbnb para una isla."""
    path = RAW / f"airbnb_{isla.lower()}_listings.csv.gz"
    df = pd.read_csv(path, low_memory=False)
    df["isla"] = isla
    # Limpiar precio (quitar $ y ,)
    df["price_num"] = (
        df["price"].astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace({"nan": None, "": None, "None": None})
        .astype(float)
    )
    # Filtrar listings activos (tienen disponibilidad o son piso completo)
    df_active = df[(df["availability_365"] > 0) | (df["room_type"] == "Entire home/apt")].copy()
    return df_active


def load_hut_eivissa() -> pd.DataFrame:
    """Carga HUT Eivissa y extrae municipio de la Ref. Catastral."""
    df = pd.read_csv(RAW / "hut_eivissa_2026-07-14.csv")
    # Limpiar Ref. Catastral (puede tener espacios, etc)
    df["ref_cat"] = df["Referència cadastral"].astype(str).str.strip().str.upper()
    # Referencia catastral: 20 chars, primeros 5 = CUMUN (provincia+municipio)
    df["CUMUN"] = df["ref_cat"].str[:5]
    df["CPRO"] = df["ref_cat"].str[:2]
    # Filtrar anomalias
    df = df[df["Municipi"] != "NUEVO BOLSA DE PLAZAS"].copy()
    # Limpiar plazas (puede ser string)
    df["plazas"] = pd.to_numeric(df["Total Places"], errors="coerce").fillna(0).astype(int)
    df["habitaciones"] = pd.to_numeric(df["Total Habitacions"], errors="coerce").fillna(0).astype(int)
    return df


def load_ibestat_formentera() -> dict:
    """Carga IBESTAT agregado de Formentera 2019."""
    with open(RAW / "ibestat_formentera_2019.json", "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    print("=== Cargando fuentes ===\n")

    ine = load_ine_vivienda()
    print(f"INE vivienda (Balears): {ine['balears']['Viviendas totales']:,} viviendas, "
          f"{ine['balears']['pct_vacias']:.1f}% vacias, "
          f"{ine['balears']['pct_uso_esporadico']:.1f}% esporadico")
    print(f"  Mediana consumo: {ine['balears']['Mediana consumo anual']} kWh\n")

    ine_tur = load_ine_vivienda_turistica()
    print(f"INE vivienda turistica: {len(ine_tur)} periodos, ultimo: "
          f"{ine_tur.iloc[0]['periodo']} = {ine_tur.iloc[0]['pct_viviendas_turisticas']}%\n")

    gdf = load_shapefile()
    print(f"  Municipios: {gdf['NMUN'].nunique()}, "
          f"Provincias: {gdf['NPRO'].unique().tolist()}\n")

    for isla in ["mallorca", "menorca"]:
        airbnb = load_airbnb(isla)
        print(f"Airbnb {isla}: {len(airbnb):,} listings activos, "
              f"precio mediana: ${airbnb['price_num'].median():.0f}")

    print()
    hut = load_hut_eivissa()
    print(f"HUT Eivissa: {len(hut):,} registros, "
          f"plazas totales: {hut['plazas'].sum():,}, "
          f"municipios: {hut['Municipi'].nunique()}")

    print()
    ibestat = load_ibestat_formentera()
    print(f"IBESTAT Formentera 2019: {ibestat['metadata']['total_unidades']:,} unidades, "
          f"{ibestat['metadata']['total_plazas']:,} plazas")

    print("\n=== Carga completa ===")
