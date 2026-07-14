"""
Exporta data/output/dataset.parquet a data/output/dataset.csv (sin geometria).

Es el archivo "amigable" para gente que no trabaja con parquet: se abre
en Excel, LibreOffice, Google Sheets, pandas, R, etc.

Output:
- data/output/dataset.csv (~50KB, 674 filas, 33 columnas)
- web/public/data/dataset.csv (copia para descarga via /dades)

Uso:
    python scripts/06_export_csv.py
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "output" / "dataset.parquet"
OUT_LOCAL = ROOT / "data" / "output" / "dataset.csv"
OUT_WEB = ROOT / "web" / "public" / "data" / "dataset.csv"


def main() -> None:
    df = pd.read_parquet(SRC)
    print(f"Loaded {SRC.name}: {len(df):,} filas, {len(df.columns)} columnas")

    # CSV en UTF-8 con coma decimal europea-friendly? Usamos ; como separador
    # para que Excel en locales es-ES/ca-ES lo abra directamente sin wizard.
    df.to_csv(OUT_LOCAL, index=False, sep=",", encoding="utf-8")
    df.to_csv(OUT_WEB, index=False, sep=",", encoding="utf-8")

    for path in (OUT_LOCAL, OUT_WEB):
        kb = path.stat().st_size / 1024
        print(f"Guardado {path.relative_to(ROOT)} ({kb:.1f} KB)")


if __name__ == "__main__":
    main()
