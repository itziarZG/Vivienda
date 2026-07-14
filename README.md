# Cases Tancades

Web publica que visibilitza la pressio turistica sobre el parc residencial de Balears, creuant dades oficiales d'INE (consum electric per seccio censal, com a proxy de vivenda semi-vacia) amb dades d'Inside Airbnb (listings georreferenciats).

Veure [PLAN.md](PLAN.md) per al plan complet i l'arquitectura.

## Estructura

```
data/raw/         Dades originals descarregades (no commitejades)
data/processed/   Dades intermiges del pipeline
data/output/      Dades finals (parquet, tiles, JSON)
docs/             Documentacio i materials de suport
scripts/          Pipeline Python
web/              Codi Astro de la web
FASE-*.md         Bitacora de cada fase del projecte
```

## Setup rapid

```bash
# Python
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Node
nvm use 20
```

## Estat

| Fase | Estat |
|---|---|
| Fase 0 - Setup | En curs |
| Fase 1 - Dades | Pendent |
| Fase 2 - Web MVP | Pendent |
| Fase 3 - Llanament | Pendent |

## Fonts de dades

- INE - Intensitat d'us per consum electric: taula del fitxer `data/raw/viviendas vacias-hipotecas.xlsx` (full 1).
- INE - Seccions censals de Balears: shapefile descarregat de https://www.ine.es/prodyser/cartografia/seccionado_2025/
- Inside Airbnb - Listings Balears: http://insideairbnb.com/get-the-data/
- Captures conferencia OHIB (12-13 nov 2025): `docs/conferencia-OHIB-2025/`

## Llicencia

A determinar. Probablement CC BY-SA 4.0.
