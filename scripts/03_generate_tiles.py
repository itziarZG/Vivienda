"""
Genera tiles pmtiles a partir de data/output/dataset.gpkg
usando tippecanoe (https://github.com/felt/tippecanoe).

Salida: data/output/tiles.pmtiles
"""

import shutil
import subprocess
from pathlib import Path
import warnings

import geopandas as gpd

warnings.filterwarnings('ignore')

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "output"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    if not shutil.which("tippecanoe"):
        print("ERROR: tippecanoe no esta instalado.")
        print("Instala con: brew install tippecanoe")
        return

    print("Convirtiendo dataset.gpkg a GeoJSON (formato que tippecanoe lee bien)...")
    gdf = gpd.read_file(OUT / "dataset.gpkg")
    cols = [
        "CUSEC", "NMUN", "isla", "granularidad", "fuente",
        "airbnb_listings", "airbnb_entire_homes", "airbnb_price_median",
        "airbnb_accommodates_total", "airbnb_revenue_total",
        "airbnb_hosts_unicos", "airbnb_con_licencia",
        "hut_registros", "hut_plazas", "hut_habitaciones",
        "plazas_turisticas",
        # INE Censo 2021 (viven en dataset tras Fase 3 mejora)
        "viviendas_totales", "viviendas_vacias_pct_ccaa",
        "viviendas_uso_esporadico_pct_ccaa", "viviendas_turisticas_pct_ccaa_2025M05",
        "consumo_p10_kwh", "consumo_p25_kwh", "consumo_p50_kwh",
        "consumo_p75_kwh", "consumo_p90_kwh",
        "airbnb_listings_por_1000_viviendas",
        "geometry",
    ]
    cols = [c for c in cols if c in gdf.columns]
    geojson_path = OUT / "dataset.geojson"
    gdf[cols].to_file(geojson_path, driver="GeoJSON")
    print(f"  -> {geojson_path.name} ({geojson_path.stat().st_size // 1024} KB)")

    print("\nGenerando tiles pmtiles...")
    cmd = [
        "tippecanoe",
        "--output", str(OUT / "tiles.pmtiles"),
        "--name", "cases",
        "--layer", "cases",
        "-zg",
        "--drop-densest-as-needed",
        "--read-parallel",
        "--minimum-zoom", "4",
        "--force",
        str(geojson_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR tippecanoe (codigo {result.returncode}):")
        print(result.stderr[-2000:])
        return

    tiles = OUT / "tiles.pmtiles"
    if tiles.exists():
        size_kb = tiles.stat().st_size // 1024
        print(f"\ntiles.pmtiles generado: {size_kb} KB")
        with open(tiles, "rb") as f:
            magic = f.read(4)
        print(f"  Magic: {magic} (esperado: b'PMTi')")
    else:
        print("ERROR: tiles.pmtiles no se genero")

    geojson_path.unlink()
    print(f"  Limpiado {geojson_path.name} (intermedio)")


if __name__ == "__main__":
    main()
