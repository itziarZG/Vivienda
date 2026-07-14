"""
Build dataset final per seccion censal / municipio.

Entradas:
- data/raw/secciones_balears.gpkg (shapefile)
- data/raw/airbnb_*_listings.csv.gz (Mallorca, Menorca)
- data/raw/hut_eivissa_2026-07-14.csv (HUT Eivissa por municipio)
- data/raw/ibestat_formentera_2019.json (Formentera agregado)

Salidas:
- data/output/dataset.parquet (tabla final)
- data/output/dataset.gpkg (geometrias + atributos, para tiles)
- data/output/dataset_web.json (version simplificada para web)
- data/output/STATS.md (estadisticas descriptivas)
"""

from pathlib import Path
import json
import warnings

import pandas as pd
import geopandas as gpd
import numpy as np

warnings.filterwarnings('ignore')

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "output"
OUT.mkdir(parents=True, exist_ok=True)


def load_airbnb_gdf(isla: str) -> gpd.GeoDataFrame:
    """Carga listings activos de Inside Airbnb y los convierte a GeoDataFrame."""
    df = pd.read_csv(RAW / f"airbnb_{isla.lower()}_listings.csv.gz", low_memory=False)
    df["price_num"] = (
        df["price"].astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace({"nan": None, "": None, "None": None})
        .astype(float)
    )
    df = df[(df["availability_365"] > 0) | (df["room_type"] == "Entire home/apt")].copy()
    df = df.dropna(subset=["latitude", "longitude"])
    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["longitude"], df["latitude"]),
        crs="EPSG:4326",
    )
    return gdf


def spatial_join_airbnb(secciones: gpd.GeoDataFrame, airbnb: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Spatial join: para cada seccion, calcula stats de Airbnb."""
    joined = gpd.sjoin(
        airbnb[["geometry", "id", "room_type", "price_num",
                "estimated_revenue_l365d", "host_id", "license", "accommodates"]],
        secciones[["CUSEC", "NMUN", "geometry"]],
        how="inner",
        predicate="within",
    )
    agg = (
        joined.groupby("CUSEC")
        .agg(
            airbnb_listings=("id", "count"),
            airbnb_entire_homes=("room_type", lambda s: (s == "Entire home/apt").sum()),
            airbnb_price_median=("price_num", "median"),
            airbnb_accommodates_total=("accommodates", "sum"),
            airbnb_revenue_total=("estimated_revenue_l365d", "sum"),
            airbnb_hosts_unicos=("host_id", "nunique"),
            airbnb_con_licencia=("license", lambda s: s.notna().sum()),
        )
        .reset_index()
    )
    return agg


def normalize_municipio(name: str) -> str:
    """Normaliza nombres de municipio de HUT/shapefile."""
    upper = name.upper().strip()
    mapping = {
        "EIVISSA": "Eivissa",
        "SANT ANTONI DE PORTMANY": "Sant Antoni de Portmany",
        "SANT JOAN DE LABRITJA": "Sant Joan de Labritja",
        "SANT JOSEP DE SA TALAIA": "Sant Josep de sa Talaia",
        "SANTA EULARIA DES RIU": "Santa Eulària des Riu",
    }
    return mapping.get(upper, name)


def aggregate_hut_eivissa() -> pd.DataFrame:
    """Agrega HUT Eivissa por municipio normalizado."""
    df = pd.read_csv(RAW / "hut_eivissa_2026-07-14.csv")
    df = df[df["Municipi"] != "NUEVO BOLSA DE PLAZAS"].copy()
    df["plazas"] = pd.to_numeric(df["Total Places"], errors="coerce").fillna(0).astype(int)
    df["habitaciones"] = pd.to_numeric(df["Total Habitacions"], errors="coerce").fillna(0).astype(int)
    df["NMUN"] = df["Municipi"].apply(normalize_municipio)
    agg = (
        df.groupby("NMUN")
        .agg(
            hut_registros=("Número Inscripció", "count"),
            hut_plazas=("plazas", "sum"),
            hut_habitaciones=("habitaciones", "sum"),
        )
        .reset_index()
    )
    agg["isla"] = "Eivissa"
    agg["fuente"] = "HUT Consell d'Eivissa 2026"
    agg["granularidad"] = "municipio"
    return agg


def build_formentera() -> pd.DataFrame:
    """Formentera: 1 fila con totales, asociada al municipio Formentera."""
    with open(RAW / "ibestat_formentera_2019.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame([{
        "NMUN": "Formentera",
        "isla": "Formentera",
        "fuente": "IBESTAT 2019",
        "granularidad": "municipio",
        "hut_registros": data["metadata"]["total_unidades"],
        "hut_plazas": data["metadata"]["total_plazas"],
    }])


def cmun_to_isla(cmun: str) -> str:
    """Mapea CMUN (5 chars) a isla. CMUN balear = 07XXX."""
    code = str(cmun)[2:]  # quita '07' de la provincia
    if code in {"24", "26", "30", "48", "54"}:
        return "Eivissa"
    if code == "17":
        return "Formentera"
    if code in {"02", "15", "32", "37", "40", "64", "65"}:
        return "Menorca"
    return "Mallorca"


def main() -> None:
    print("=== Construyendo dataset ===\n")

    secciones = gpd.read_file(RAW / "secciones_balears.gpkg")
    print(f"Shapefile: {len(secciones)} secciones")

    # 1) Spatial join Airbnb Mallorca
    airbnb_mall = load_airbnb_gdf("mallorca")
    print(f"Airbnb Mallorca: {len(airbnb_mall):,} listings activos geo-localizados")
    agg_mall = spatial_join_airbnb(secciones, airbnb_mall)
    agg_mall["isla"] = "Mallorca"
    agg_mall["fuente"] = "Inside Airbnb 2026-06"
    agg_mall["granularidad"] = "seccion_censal"
    print(f"  -> {len(agg_mall)} secciones con Airbnb en Mallorca")

    # 2) Spatial join Airbnb Menorca
    airbnb_men = load_airbnb_gdf("menorca")
    print(f"Airbnb Menorca: {len(airbnb_men):,} listings activos geo-localizados")
    agg_men = spatial_join_airbnb(secciones, airbnb_men)
    agg_men["isla"] = "Menorca"
    agg_men["fuente"] = "Inside Airbnb 2026-06"
    agg_men["granularidad"] = "seccion_censal"
    print(f"  -> {len(agg_men)} secciones con Airbnb en Menorca")

    # 3) HUT Eivissa por municipio
    hut_eiv = aggregate_hut_eivissa()
    print(f"\nHUT Eivissa: {len(hut_eiv)} municipios, "
          f"{hut_eiv['hut_registros'].sum():,} registros, "
          f"{hut_eiv['hut_plazas'].sum():,} plazas")

    # 4) Formentera
    formentera = build_formentera()
    print(f"IBESTAT Formentera: {formentera.iloc[0]['hut_registros']:,} unidades, "
          f"{formentera.iloc[0]['hut_plazas']:,} plazas")

    # 5) Merge con shapefile
    # Airbnb: secciones con datos
    airbnb_full = pd.concat([agg_mall, agg_men], ignore_index=True)
    gdf = secciones.merge(airbnb_full, on="CUSEC", how="left", suffixes=("", "_air"))

    # Eivissa: join por NMUN
    gdf = gdf.merge(hut_eiv, on="NMUN", how="left", suffixes=("", "_eiv"))

    # Formentera: una sola fila
    gdf = gdf.merge(formentera, on="NMUN", how="left", suffixes=("", "_for"))

    # Resolver columnas finales de isla/fuente/granularidad
    # Para Mallorca/Menorca: ya viene de airbnb
    # Para Eivissa/Formentera: viene del merge de hut
    gdf["isla_final"] = gdf["isla"].fillna(gdf["isla_eiv"]).fillna(gdf["isla_for"])
    gdf["fuente_final"] = gdf["fuente"].fillna(gdf["fuente_eiv"]).fillna(gdf["fuente_for"])
    gdf["granularidad_final"] = (
        gdf["granularidad"]
        .fillna(gdf["granularidad_eiv"])
        .fillna(gdf["granularidad_for"])
    )
    # Fallback isla por CMUN para secciones rurales sin datos de turismo
    mask_no_isla = gdf["isla_final"].isna()
    gdf.loc[mask_no_isla, "isla_final"] = gdf.loc[mask_no_isla, "CMUN"].apply(cmun_to_isla)
    gdf.loc[mask_no_isla, "granularidad_final"] = "seccion_censal"
    gdf.loc[mask_no_isla, "fuente_final"] = "shapefile INE 2025 (sin datos de turismo)"
    # Resolver hut_registros/hut_plazas: para Eivissa vienen del merge directo,
    # para Formentera vienen con sufijo _for (porque el merge de Eivissa ya uso esos nombres).
    gdf["hut_registros_final"] = gdf["hut_registros"].fillna(gdf["hut_registros_for"])
    gdf["hut_plazas_final"] = gdf["hut_plazas"].fillna(gdf["hut_plazas_for"])
    if "hut_habitaciones_for" in gdf.columns:
        gdf["hut_habitaciones_final"] = gdf["hut_habitaciones"].fillna(gdf["hut_habitaciones_for"])
    else:
        gdf["hut_habitaciones_final"] = gdf["hut_habitaciones"]

    # Limpiar columnas auxiliares
    drop_cols = [c for c in gdf.columns if c.endswith(("_air", "_eiv", "_for"))]
    drop_cols += ["isla", "fuente", "granularidad", "hut_registros", "hut_plazas", "hut_habitaciones"]
    gdf = gdf.drop(columns=drop_cols, errors="ignore")
    gdf = gdf.rename(columns={
        "isla_final": "isla",
        "fuente_final": "fuente",
        "granularidad_final": "granularidad",
        "hut_registros_final": "hut_registros",
        "hut_plazas_final": "hut_plazas",
        "hut_habitaciones_final": "hut_habitaciones",
    })

    # Llenar NaN de columnas Airbnb con 0 (seccion existe pero sin listings)
    airbnb_cols = [
        "airbnb_listings", "airbnb_entire_homes", "airbnb_accommodates_total",
        "airbnb_revenue_total", "airbnb_hosts_unicos", "airbnb_con_licencia",
    ]
    for c in airbnb_cols:
        if c in gdf.columns:
            gdf[c] = gdf[c].fillna(0).astype(int)

    # Llenar NaN de columnas HUT con 0
    for c in ["hut_registros", "hut_plazas", "hut_habitaciones"]:
        if c in gdf.columns:
            gdf[c] = gdf[c].fillna(0).astype(int)

    # Viviendas INE a nivel CCAA (documentado en /metodologia)
    gdf["viviendas_vacias_pct_ccaa"] = 16.2
    gdf["viviendas_uso_esporadico_pct_ccaa"] = 6.9
    gdf["viviendas_turisticas_pct_ccaa_2025M05"] = 3.74

    # Total plazas turisticas por seccion (para color en mapa)
    gdf["plazas_turisticas"] = gdf["airbnb_accommodates_total"].fillna(0) + gdf["hut_plazas"].fillna(0)
    # Para Eivissa/Formentera las plazas se asignan a nivel municipio;
    # al pintar por seccion, la division muestra una densidad "diluida" de municipio.
    # Para visualizacion limpia, en el frontend se usara granularidad_final para escalar.

    # Guardar
    gdf.to_file(OUT / "dataset.gpkg", driver="GPKG")
    print(f"\nGuardado dataset.gpkg: {len(gdf)} filas, {len(gdf.columns)} columnas")

    # Parquet (sin geometria, geometria ya en gpkg)
    df = pd.DataFrame(gdf.drop(columns="geometry"))
    df.to_parquet(OUT / "dataset.parquet", index=False)
    print(f"Guardado dataset.parquet: {len(df)} filas")

    # JSON simplificado para web (sin geometria, agregados por isla)
    resumen_isla = (
        gdf.groupby("isla")
        .agg(
            secciones=("CUSEC", "count"),
            airbnb_listings=("airbnb_listings", "sum"),
            airbnb_entire_homes=("airbnb_entire_homes", "sum"),
            airbnb_revenue_total=("airbnb_revenue_total", "sum"),
            airbnb_hosts_unicos=("airbnb_hosts_unicos", "sum"),
            airbnb_con_licencia=("airbnb_con_licencia", "sum"),
            hut_registros=("hut_registros", "sum"),
            hut_plazas=("hut_plazas", "sum"),
        )
        .reset_index()
        .to_dict(orient="records")
    )
    with open(OUT / "dataset_web.json", "w", encoding="utf-8") as f:
        json.dump({"resumen_por_isla": resumen_isla}, f, ensure_ascii=False, indent=2)
    print(f"Guardado dataset_web.json")

    # Stats descriptivas
    # Para HUT Eivissa: usar el dataframe agregado directamente (los totales del merge por seccion
    # no son sumables: misma valor se replica por seccion del mismo municipio).
    hut_eiv_total = int(hut_eiv["hut_registros"].sum())
    hut_eiv_plazas = int(hut_eiv["hut_plazas"].sum())
    formentera_total = int(formentera["hut_registros"].iloc[0])
    formentera_plazas = int(formentera["hut_plazas"].iloc[0])

    stats = []
    stats.append(f"# Estadisticas descriptivas - Cases Tancades\n")
    stats.append(f"Generado: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n")
    stats.append(f"\n## Cobertura geografica\n")
    stats.append(f"- Total secciones censales Balears: **{len(gdf):,}**")
    stats.append(f"- Municipios: **{gdf['NMUN'].nunique()}**")
    stats.append(f"- Islas con datos: **{gdf['isla'].nunique()}**\n")

    stats.append(f"\n## Granularidad por isla\n")
    for isla, gran in gdf.groupby("isla")["granularidad"].first().items():
        stats.append(f"- **{isla}**: {gran}")

    stats.append(f"\n## Airbnb (Mallorca + Menorca)\n")
    airbnb_total = gdf[gdf["isla"].isin(["Mallorca", "Menorca"])]
    stats.append(f"- Listings activos (geo-localizados): **{int(airbnb_total['airbnb_listings'].sum()):,}**")
    stats.append(f"- Entire home/apt: **{int(airbnb_total['airbnb_entire_homes'].sum()):,}**")
    stats.append(f"- Plazas (accommodates): **{int(airbnb_total['airbnb_accommodates_total'].sum()):,}**")
    stats.append(f"- Hosts unicos: **{int(airbnb_total['airbnb_hosts_unicos'].sum()):,}**")
    stats.append(f"- Con numero de licencia: **{int(airbnb_total['airbnb_con_licencia'].sum()):,}** "
                 f"({100 * airbnb_total['airbnb_con_licencia'].sum() / airbnb_total['airbnb_listings'].sum():.1f}%)")
    stats.append(f"- Ingresos estimados L365d: **${int(airbnb_total['airbnb_revenue_total'].sum()):,}**")
    stats.append(f"- Precio mediano por noche: **${airbnb_total['airbnb_price_median'].median():.0f}**\n")

    stats.append(f"\n## HUT Eivissa (legal)\n")
    stats.append(f"- Registros totales: **{hut_eiv_total:,}**")
    stats.append(f"- Plazas totales: **{hut_eiv_plazas:,}**")
    stats.append(f"- Municipios: **5** (Eivissa, Sant Antoni, Sant Joan, Sant Josep, Santa Eulària)")
    stats.append(f"\nDetalle por municipio:\n")
    for _, row in hut_eiv.sort_values("hut_plazas", ascending=False).iterrows():
        stats.append(f"- {row['NMUN']}: {row['hut_registros']:,} registros, {row['hut_plazas']:,} plazas")

    stats.append(f"\n## IBESTAT Formentera (agregado 2019)\n")
    stats.append(f"- Establecimientos: **{formentera_total:,}**")
    stats.append(f"- Plazas: **{formentera_plazas:,}**")

    stats.append(f"\n## INE vivienda (CCAA Balears, base de referencia)\n")
    stats.append(f"- Viviendas totales: **652,123**")
    stats.append(f"- % viviendas vacias: **16.2%** (~105,564)")
    stats.append(f"- % uso esporadico: **6.9%** (~44,996)")
    stats.append(f"- % vivienda turistica (2025M05): **3.74%** (~24,389)")
    stats.append(f"\n> Limitacion: estos porcentajes son a nivel CCAA, no seccion censal. "
                 f"Ver /metodologia.\n")

    stats.append(f"\n## Brecha legal vs realidad (insight narrativo)\n")
    # Mallorca: Airbnb listings (no todos son legales, pero la mayoria no)
    mall_airbnb = int(airbnb_total[airbnb_total["isla"] == "Mallorca"]["airbnb_listings"].sum())
    men_airbnb = int(airbnb_total[airbnb_total["isla"] == "Menorca"]["airbnb_listings"].sum())
    stats.append(f"- Mallorca: ~{mall_airbnb:,} listings activos en Airbnb vs. ~24,389 plazas turisticas legales declaradas en CCAA")
    stats.append(f"- Menorca: ~{men_airbnb:,} listings activos en Airbnb (CCAA-wide)")
    stats.append(f"- Eivissa (HUT, dato legal): {hut_eiv_total:,} registros, "
                 f"{hut_eiv_plazas:,} plazas")
    stats.append(f"  > El Govern reconoce {hut_eiv_plazas:,} plazas legales; el gap legal/realidad "
                 f"se ve con comparativas de Airbnb en municipios donde la regulacion es estricta.\n")

    with open(OUT / "STATS.md", "w", encoding="utf-8") as f:
        f.write("\n".join(stats))
    print(f"Guardado STATS.md")

    print(f"\n=== Dataset construido ===")


if __name__ == "__main__":
    main()
