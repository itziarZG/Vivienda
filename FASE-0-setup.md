# FASE 0 - Setup (semana 1)

## Objetivo

Tener el entorno listo y los datos crudos descargados y validados, sin procesar. Al cerrar esta fase, `git status` muestra una estructura limpia y `data/raw/` contiene los datasets originales descargados, cada uno abrible sin errores.

## Tareas

### Estructura de carpetas
- [ ] Crear en `/Users/ichi/Desktop/DEV/VIvienda/`:
  - `data/raw/` - datos originales, inmutables
  - `data/processed/` - datasets intermedios
  - `data/output/` - parquet, tiles, JSONs finales
  - `web/` - codigo Astro
  - `docs/` - PDFs, capturas, metodologia extendida
  - `scripts/` - pipeline Python

### Repositorio
- [ ] `git init` en `/Users/ichi/Desktop/DEV/VIvienda/`
- [ ] Crear `.gitignore` que ignore:
  - `data/raw/*.xlsx` y `data/raw/*.csv.gz` (datos pesados)
  - `data/processed/`
  - `data/output/`
  - `node_modules/`
  - `.venv/`, `__pycache__/`
  - `.env`, `.env.local`
- [ ] Hacer commit inicial con estructura + `.gitignore` + este PLAN
- [ ] (Opcional) crear repo en GitHub y vincular

### Reorganizacion de archivos existentes
- [ ] Mover `Info.pdf` y los 19 `.jpg` de la conferencia a `docs/conferencia-OHIB-2025/`
- [ ] Mover `viviendas vacias-hipotecas.xlsx` y `39365(1).xlsx` a `data/raw/`
- [ ] Documentar el origen de cada archivo en `data/raw/ORIGEN.md`

### Entorno Python
- [ ] Instalar `uv` (gestor de entornos y paquetes rapido)
- [ ] `uv venv .venv` en la raiz del proyecto
- [ ] Crear `requirements.txt` con: pandas, openpyxl, geopandas, duckdb, shapely, pyproj, fiona, pyarrow
- [ ] `uv pip install -r requirements.txt`
- [ ] Verificar: `python -c "import geopandas, duckdb; print('OK')"`

### Entorno Node
- [ ] Instalar Node 20+ (con `nvm` o `brew`)
- [ ] Instalar pnpm (`npm install -g pnpm`)

### Descarga de datos externos
- [ ] Descargar **shapefile de secciones censales de Balears** desde INE
  - Fuente: https://www.ine.es/prodyser/cartografia/seccionado_2025/
  - Descargar las 4 provincias: Mallorca (07), Menorca (07), Eivissa (07), Formentera (07)
  - Verificar que incluye geometria poligonal
- [ ] Descargar **Inside Airbnb listings** para las 4 islas
  - Fuente: http://insideairbnb.com/get-the-data/
  - Snapshot mas reciente disponible para: Mallorca, Menorca, Eivissa, Formentera
  - Formato: `listings.csv.gz` (revisar tamano y fecha)

### Validacion
- [ ] Shapefile abre con geopandas, tiene CRS correcto, conteo de features > 0
- [ ] Listings CSV abre con pandas, columnas esperadas presentes
- [ ] XLSXs del usuario abren con openpyxl/pandas
- [ ] Anotar numero de filas de cada dataset en `data/raw/VALIDACION.md`

### Cierre
- [ ] Commit final con tag `fase-0-completa`
- [ ] Actualizar PLAN.md: marcar Fase 0 como completada
- [ ] Anotar problemas y decisiones en este documento

## Comandos clave

```bash
# Estructura
cd /Users/ichi/Desktop/DEV/VIvienda
mkdir -p data/raw data/processed data/output web docs/conferencia-OHIB-2025 scripts

# Git
git init
git add .
git commit -m "chore: estructura inicial del proyecto"

# Python
brew install uv   # o pipx install uv
uv venv .venv
source .venv/bin/activate
uv pip install pandas openpyxl geopandas duckdb shapely pyproj fiona pyarrow

# Node
brew install node pnpm   # o nvm install 20 && npm i -g pnpm

# Validacion shapefile (despues de descargar)
python -c "import geopandas as gpd; gdf = gpd.read_file('data/raw/secciones_censales_balears.shp'); print(gdf.head()); print('CRS:', gdf.crs); print('Features:', len(gdf))"

# Validacion listings
python -c "import pandas as pd; df = pd.read_csv('data/raw/eivissa_listings.csv.gz', low_memory=False); print(df.shape); print(df.columns.tolist()[:20])"

# Validacion XLSX
python -c "import pandas as pd; df = pd.read_excel('data/raw/viviendas vacias-hipotecas.xlsx', sheet_name=None); print({k: v.shape for k, v in df.items()})"
```

## Criterio de "fase terminada" (Definition of Done)

- [x] Repo git inicializado con branch `main`
- [x] Estructura de carpetas creada
- [x] `.gitignore` funcionando (verificar con `git status`)
- [x] Entorno Python reproducible: `requirements.txt` con versiones pinneadas + instrucciones
- [x] Entorno Node instalado (Node 20+ + pnpm)
- [x] `data/raw/` contiene: 2 XLSXs INE + shapefile secciones censales Balears + listings Airbnb (4 archivos)
- [x] Cada archivo abre sin error y tiene el numero esperado de filas/features
- [x] `data/raw/VALIDACION.md` documenta conteos y CRS
- [x] Commit final con tag `fase-0-completa`
- [x] PLAN.md actualizado con check de Fase 0

## Decisiones tomadas durante la fase

_Llenar durante la ejecucion. Ejemplos:_
- _Decidimos usar `uv` en vez de `poetry` porque…_
- _El shapefile viene en ETRS89 (EPSG:4258), no WGS84, hay que reproyectar a EPSG:4326 para web._
- _Decidimos ignorar `data/raw/*.xlsx` en git por tamano; el repo solo guarda scripts y docs._

## Problemas encontrados

_Llenar durante la ejecucion. Ejemplos:_
- _El shapefile de Formentera viene en un ZIP separado y CRS distinto al de Mallorca._
- _Inside Airbnb no tiene snapshot para Formentera separado; el de Eivissa incluye ambos._

## Proximos pasos

Fase 1: pipeline de datos Python. Entrada: archivos en `data/raw/`. Salida: `dataset.parquet` y `tiles.pmtiles` en `data/output/`. Ver `FASE-1-datos.md`.
