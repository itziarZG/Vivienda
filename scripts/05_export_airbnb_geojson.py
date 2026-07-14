"""
Genera web/public/data/airbnb_listings.geojson a partir de los CSVs raw
de Inside Airbnb Mallorca y Menorca.

Output: FeatureCollection con ~18K puntos. Solo geometria + 2 props
(isla, room_type) para mantener el fichero ligero (~700KB).
"""

from pathlib import Path
import json

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "web" / "public" / "data"
OUT.mkdir(parents=True, exist_ok=True)


def load_isla(name: str) -> pd.DataFrame:
    df = pd.read_csv(RAW / f"airbnb_{name.lower()}_listings.csv.gz", low_memory=False)
    df = df[(df["availability_365"] > 0) | (df["room_type"] == "Entire home/apt")]
    df = df.dropna(subset=["latitude", "longitude"])
    df["isla"] = name
    return df[["id", "latitude", "longitude", "room_type", "isla"]]


def main() -> None:
    mall = load_isla("mallorca")
    men = load_isla("menorca")
    df = pd.concat([mall, men], ignore_index=True)
    print(f"Total puntos: {len(df):,}")

    features = []
    for _, row in df.iterrows():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(row["longitude"]), float(row["latitude"])],
            },
            "properties": {
                "id": str(row["id"]),
                "isla": row["isla"],
                "room_type": row["room_type"],
            },
        })

    out = {"type": "FeatureCollection", "features": features}
    out_path = OUT / "airbnb_listings.geojson"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"Guardado {out_path} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
