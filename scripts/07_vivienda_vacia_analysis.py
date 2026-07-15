"""
Analisis de la tabla 59532 (Censo 2021) como proxy de vivienda semi-vacia / uso
estacional en Balears.

El Census 2021 no da serie temporal, pero da los percentiles de consumo electrico
por distrito. Interpretacion:
- p10 muy bajo: muchas casas con consumo muy bajo. Posibles vacias, segunda
  residencia de uso solo estival, o personas mayores que apenas usan electricidad.
- p50 (mediana) estable: la mayoria de hogares consume un valor normal.
- p90 alto: hay casas con consumo muy alto (AC, calefaccion, varios miembros).

Ratios utiles:
- p10/p50 bajo (cercano a 0): distribucion normal, todos consumen similar
- p10/p50 alto (cercano a 1): distribucion asimetrica, hay un grupo de bajo consumo
  que arrastra la p10 hacia abajo (posible vacio/estacional)

Tambien se cruza con la presion Airbnb por distrito (sumando listings de M/M
que caen dentro de cada distrito censal) para ver si hay correlacion entre
presion turistica y heterogeneidad de consumo.

Output:
- data/output/vivienda_vacia_analysis.md (reporte markdown)
- data/output/vivienda_vacia_por_distrito.csv (datos por distrito)
"""

from pathlib import Path
import warnings

import pandas as pd
import geopandas as gpd
import numpy as np

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "output"


def parse_kwh(value: str) -> float:
    """Parsea valores de la tabla 59532 con formato mixto espanol.

    Dos formatos observados en el CSV:
    - Decimal: "629.000" -> 629 (los .000 son colas de precision)
    - Miles:   "1.210"   -> 1210 (separador de miles)

    Distingo por la cola: si la parte despues del punto son todos 0, es decimal.
    En otro caso, el punto es separador de miles.
    """
    s = str(value).strip()
    if "." not in s:
        # Sin punto: numero entero
        return float(s)
    int_part, dec_part = s.split(".", 1)
    if set(dec_part) == {"0"}:
        # "629.000" -> 629
        return float(int_part)
    # "1.210" -> 1210
    return float(int_part + dec_part)


def load_consumo_distrito() -> pd.DataFrame:
    """Carga tabla 59532 y agrega a nivel de distrito."""
    df = pd.read_csv(RAW / "59532.csv", sep=";", encoding="latin1", low_memory=False)
    df.columns = ["DISTRITO", "PERCENTIL", "TOTAL"]
    df = df[df["DISTRITO"].astype(str).str.strip().str.startswith("07")].copy()
    df["CDIS"] = df["DISTRITO"].astype(str).str.strip().str[:7]
    df["NMUN_DIST"] = df["DISTRITO"].astype(str).str.strip()
    df["kwh"] = df["TOTAL"].apply(parse_kwh)
    df["percentil"] = df["PERCENTIL"].str.extract(r"Percentil (\d+)").astype(int)
    pivot = df.pivot_table(
        index=["CDIS", "NMUN_DIST"],
        columns="percentil",
        values="kwh",
        aggfunc="first",
    ).reset_index()
    pivot.columns = ["CDIS", "NMUN_DIST"] + [f"consumo_p{p}_kwh" for p in pivot.columns[2:]]
    return pivot


def load_airbnb_by_distrito() -> pd.DataFrame:
    """Suma listings de Airbnb por distrito censal (Mallorca + Menorca)."""
    out_rows = []
    for isla in ["mallorca", "menorca"]:
        df = pd.read_csv(RAW / f"airbnb_{isla.lower()}_listings.csv.gz", low_memory=False)
        df = df[(df["availability_365"] > 0) | (df["room_type"] == "Entire home/apt")]
        df = df.dropna(subset=["latitude", "longitude"])
        gdf_secc = gpd.read_file(RAW / "secciones_balears.gpkg")[["CUSEC", "geometry"]]
        gdf_secc["CDIS"] = gdf_secc["CUSEC"].astype(str).str[:7]
        gdf_pts = gpd.GeoDataFrame(
            df,
            geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
            crs="EPSG:4326",
        )
        joined = gpd.sjoin(gdf_pts, gdf_secc, how="inner", predicate="within")
        agg = joined.groupby("CDIS").agg(
            airbnb_listings=("id", "count"),
            airbnb_entire_homes=("room_type", lambda s: (s == "Entire home/apt").sum()),
        ).reset_index()
        out_rows.append(agg)
    full = pd.concat(out_rows, ignore_index=True)
    return full.groupby("CDIS", as_index=False).sum()


def load_viviendas_municipio() -> pd.DataFrame:
    """Carga viviendas totales por municipio (tabla 59531)."""
    df = pd.read_csv(RAW / "59531.csv", sep=";", encoding="latin1", low_memory=False)
    df.columns = ["NAC", "CCAA", "PROV", "MUN", "INDICADOR", "TOTAL"]
    df = df[df["PROV"].astype(str).str.contains("Balears", na=False, regex=False)].copy()
    df = df[df["INDICADOR"] == "Viviendas totales"].copy()
    df["CMUN"] = df["MUN"].astype(str).str.strip().str[:5]
    df["NMUN"] = df["MUN"].astype(str).str.strip().str[6:]
    df = df[df["CMUN"] != "07999"].copy()
    df["viviendas_totales"] = pd.to_numeric(
        df["TOTAL"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
        errors="coerce",
    ).fillna(0).astype(int)
    return df[["CMUN", "NMUN", "viviendas_totales"]]


def main() -> None:
    print("=== Analisis vivienda semi-vacia (proxy p10/p50) ===\n")

    consumo = load_consumo_distrito()
    print(f"Distritos con dato de consumo: {len(consumo)}")

    airbnb = load_airbnb_by_distrito()
    print(f"Distritos con listings Airbnb (M/M): {len(airbnb)}")

    viviendas = load_viviendas_municipio()
    print(f"Municipios con dato de viviendas: {len(viviendas)}")

    # Compute ratios
    consumo["ratio_p10_p50"] = consumo["consumo_p10_kwh"] / consumo["consumo_p50_kwh"]
    consumo["ratio_p25_p50"] = consumo["consumo_p25_kwh"] / consumo["consumo_p50_kwh"]
    consumo["ratio_p90_p50"] = consumo["consumo_p90_kwh"] / consumo["consumo_p50_kwh"]
    consumo["rango_p10_p90"] = consumo["consumo_p90_kwh"] - consumo["consumo_p10_kwh"]
    # Indicador de "heterogeneidad": diferencia entre p10 y p50 normalizada
    consumo["gap_bajo_consumo_pct"] = (1 - consumo["ratio_p10_p50"]) * 100

    # Cross-reference
    merged = consumo.merge(airbnb, on="CDIS", how="left").fillna({"airbnb_listings": 0, "airbnb_entire_homes": 0})

    # Add municipio name (extract from CDIS: 07001 = municipio code)
    merged["CMUN"] = merged["CDIS"].str[:5]
    merged = merged.merge(viviendas[["CMUN", "NMUN", "viviendas_totales"]], on="CMUN", how="left").fillna({"viviendas_totales": 0})
    # Airbnbs per 1000 viviendas (proxy de presion)
    merged["airbnb_per_1000_viv"] = np.where(
        merged["viviendas_totales"] > 0,
        merged["airbnb_listings"] / merged["viviendas_totales"] * 1000,
        0,
    )

    # Save CSV
    csv_out = OUT / "vivienda_vacia_por_distrito.csv"
    merged.drop(columns=["NMUN_DIST"], errors="ignore").to_csv(csv_out, index=False, encoding="utf-8")
    print(f"\nGuardado {csv_out.relative_to(ROOT)}: {len(merged)} distritos")

    # Stats summary
    p10_mediana = float(merged["ratio_p10_p50"].median())
    p10_p25 = merged["ratio_p10_p50"].quantile(0.25)
    p10_p75 = merged["ratio_p10_p50"].quantile(0.75)
    print(f"\nratio p10/p50 mediana: {p10_mediana:.3f}")
    print(f"  Q1: {p10_p25:.3f}, Q3: {p10_p75:.3f}")
    # Interpretation: ratio bajo = distribucion normal, ratio alto = muchas casas con poco consumo
    n_alto = (merged["ratio_p10_p50"] < 0.4).sum()
    print(f"  distritos con ratio < 0.4 (mucha cola de bajo consumo): {n_alto}/{len(merged)}")

    # Correlacion airbnb per 1000 viv vs ratio p10/p50
    corr = merged[["airbnb_per_1000_viv", "ratio_p10_p50"]].corr().iloc[0, 1]
    print(f"\nCorrelacion airbnb/1000viv vs ratio p10/p50: {corr:.3f}")

    # Top 10 distritos con mas "cola de bajo consumo" (potencialmente vacios/estacionales)
    top_gap = merged.nsmallest(10, "ratio_p10_p50")[["NMUN_DIST", "consumo_p10_kwh", "consumo_p50_kwh", "ratio_p10_p50", "airbnb_listings", "airbnb_per_1000_viv"]]

    # Top 10 distritos con mas presion Airbnb
    top_airbnb = merged.nlargest(10, "airbnb_per_1000_viv")[["NMUN_DIST", "airbnb_listings", "viviendas_totales", "airbnb_per_1000_viv", "ratio_p10_p50"]]

    # Generate markdown report
    md = []
    md.append("# Analisis vivienda semi-vacia Balears (Censo 2021)\n")
    md.append("**Fuente**: INE Censo 2021 - Tabla 59532 (percentiles consumo electrico por distrito censal) y Tabla 59531 (viviendas totales por municipio).\n")
    md.append("**Limitacion importante**: El Censo 2021 da un snapshot anual, NO serie temporal. Los percentiles no distinguen invierno vs verano. Se usan como PROXY de la heterogeneidad de uso:\n")
    md.append("- `p10` bajo: hay casas que consumen muy poco. Podrian ser vacias, segunda residencia estival, o mayores que apenas usan luz.\n")
    md.append("- `p50` (mediana): el hogar tipico del distrito.\n")
    md.append("- `ratio_p10_p50` bajo (<0.4): cola izquierda larga = mas casas con consumo muy bajo = potencial vivienda semi-vacia.\n")
    md.append("- `ratio_p10_p50` alto (~0.7+): distribucion normal = la mayoria de casas se parecen.\n\n")

    md.append("## Metodologia\n")
    md.append("Para cada distrito censal:\n")
    md.append("1. Se extrae p10/p25/p50/p75/p90 del consumo anual de electricidad (kWh)\n")
    md.append("2. Se calcula `ratio_p10_p50 = p10 / p50`. Bajo = distribucion asimetrica con cola de bajo consumo\n")
    md.append("3. Se cruza con listings de Airbnb del Inside Airbnb (junio 2026) por distrito\n")
    md.append("4. Se cruza con viviendas totales del municipio (Censo 2021) para normalizar\n\n")

    md.append("## Resultados globales\n")
    md.append(f"- **Distritos analizados**: {len(merged)}\n")
    md.append(f"- **ratio p10/p50 mediana**: {p10_mediana:.3f} (Q1: {p10_p25:.3f}, Q3: {p10_p75:.3f})\n")
    md.append(f"- **Distritos con ratio < 0.4** (posible concentracion de vivienda semi-vacia): **{n_alto} de {len(merged)} ({100*n_alto/len(merged):.0f}%)**\n")
    md.append(f"- **Correlacion airbnb/1000viv vs ratio p10/p50**: {corr:.3f}\n")
    if corr < -0.2:
        md.append("  > Correlacion negativa moderada: mas Airbnb, MENOS cola de bajo consumo. ")
        md.append("  > Interpretacion: los distritos turisticos tienen MENOS vacio relativo (las casas estan alquiladas).\n")
    elif corr > 0.2:
        md.append("  > Correlacion positiva: mas Airbnb, MAS cola de bajo consumo. ")
        md.append("  > Interpretacion: los distritos turisticos tienen mas vivienda vacia (desplazamiento).\n")
    else:
        md.append("  > Correlacion debil: no hay patron claro entre Airbnb y vacio residencial.\n")

    md.append("\n## Top 10 distritos con MENOR ratio p10/p50 (mas cola de bajo consumo)\n")
    md.append("Estos distritos tienen el percentil 10 mas bajo en relacion a la mediana. Indica que hay un grupo de casas con consumo electrico muy bajo.\n\n")
    md.append("| Distrito | p10 (kWh) | p50 (kWh) | ratio p10/p50 | Listings Airbnb | Airbnb/1000 viv |\n")
    md.append("|---|---:|---:|---:|---:|---:|\n")
    for _, r in top_gap.iterrows():
        md.append(f"| {r['NMUN_DIST'][:50]} | {r['consumo_p10_kwh']:,.0f} | {r['consumo_p50_kwh']:,.0f} | {r['ratio_p10_p50']:.2f} | {int(r['airbnb_listings'])} | {r['airbnb_per_1000_viv']:.1f} |\n")

    md.append("\n## Top 10 distritos con MAS presion Airbnb (per capita)\n")
    md.append("| Distrito | Listings Airbnb | Viviendas | Airbnb/1000 viv | ratio p10/p50 |\n")
    md.append("|---|---:|---:|---:|---:|\n")
    for _, r in top_airbnb.iterrows():
        md.append(f"| {r['NMUN_DIST'][:50]} | {int(r['airbnb_listings'])} | {int(r['viviendas_totales']):,} | {r['airbnb_per_1000_viv']:.1f} | {r['ratio_p10_p50']:.2f} |\n")

    md.append("\n## Lectura del hallazgo\n\n")
    md.append("**No podemos demostrar aumento de demanda invierno vs verano** con estos datos (es un snapshot del ano 2021, no serie temporal).\n\n")
    md.append("**Lo que SI podemos hacer**: usar `ratio p10_p50` como **proxy de heterogeneidad de uso**. La hipotesis es que:\n")
    md.append("- En zonas donde la mayoria de casas se usan como segunda residencia estival, la cola izquierda del consumo electrico es mas larga (ratio bajo).\n")
    md.append("- En zonas de uso residencial estable, la distribucion es mas homogenea (ratio alto).\n\n")
    md.append("Para comparar **realmente invierno vs verano** haria falta:\n")
    md.append("- Serie temporal de REE (API rota para geo_limit=baleares)\n")
    md.append("- O datos del Govern Balear / CNMC con desglose mensual\n")
    md.append("- O microdatos del Censo 2021 (no accesibles publicamente con granularidad mensual)\n")

    md.append("\n## Recomendaciones para profundizar\n\n")
    md.append("1. **Solicitar datos** a la Conselleria de Transicio Energetica del Govern Balear\n")
    md.append("2. **Esperar a que REE arregle** la API para `geo_limit=baleares` (reporte en su portal)\n")
    md.append("3. **Cruzar con datos de agua** (Conselleria de Medi Ambient): una vivienda vacia consume menos agua, mismo patron\n")

    with open(OUT / "vivienda_vacia_analysis.md", "w", encoding="utf-8") as f:
        f.write("".join(md))
    print(f"Guardado {OUT / 'vivienda_vacia_analysis.md'}")


if __name__ == "__main__":
    main()