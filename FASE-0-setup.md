# FASE 0 - Setup (semana 1)

## Objetivo

Tener el entorno listo y los datos crudos descargados y validados, sin procesar. Al cerrar esta fase, `git status` muestra una estructura limpia y `data/raw/` contiene los datasets originales descargados, cada uno abrible sin errores.

## Tareas

### Estructura de carpetas
- [x] Crear en `/Users/ichi/Desktop/DEV/VIvienda/`:
  - `data/raw/` - datos originales, inmutables
  - `data/processed/` - datasets intermedios
  - `data/output/` - parquet, tiles, JSONs finales
  - `web/` - codigo Astro
  - `docs/` - PDFs, capturas, metodologia extendida
  - `scripts/` - pipeline Python

### Repositorio
- [x] `git init` en `/Users/ichi/Desktop/DEV/VIvienda/`
- [x] Crear `.gitignore` que ignore:
  - `data/raw/*.xlsx` y `data/raw/*.csv.gz` (datos pesados)
  - `data/processed/`
  - `data/output/`
  - `node_modules/`
  - `.venv/`, `__pycache__/`
  - `.env`, `.env.local`
- [x] Hacer commit inicial con estructura + `.gitignore` + este PLAN (commit `53f24de`)

### Reorganizacion de archivos existentes
- [x] Mover 15 JPGs unicos a `docs/conferencia-OHIB-2025/` (5 duplicados borrados)
- [x] Mover `viviendas vacias-hipotecas.xlsx` y `39365(1).xlsx` a `data/raw/`
- [x] Mover `Info.pdf` a `docs/conferencia-OHIB-2025/`
- [x] Documentar el origen de cada archivo en `data/raw/ORIGEN.md`

### Entorno Python
- [x] `uv` disponible (v0.7.21)
- [x] `uv venv .venv` (Python 3.10.18 seleccionado por uv para compatibilidad con geopandas)
- [x] `requirements.txt` con: pandas, openpyxl, geopandas, duckdb, shapely, pyproj, fiona, pyarrow
- [x] `uv pip install -r requirements.txt` (todas las deps instaladas)
- [x] Verificar: pandas 2.3.3, geopandas 1.1.4, duckdb 1.5.4, shapely 2.1.2, pyproj 3.7.1, fiona 1.10.1, openpyxl 3.1.5, pyarrow 25.0.0

### Entorno Node
- [x] Node 17.1.0 estaba instalado via nvm pero requiere 20+ para Astro
- [x] `nvm install 20` (v20.20.2) y `nvm alias default 20`
- [x] pnpm v9.15.9 instalado (version 9 porque la 10+ requiere Node 22.13)

### Descarga de datos externos
- [x] Descargar **shapefile de secciones censales de Espana 2025** desde INE
  - URL final: `https://www.ine.es/prodyser/cartografia/seccionado_2025.zip` (57.5 MB)
  - Shapefile procesado: filtrado a Illes Balears (674 features, 67 municipios, 1 provincia)
  - Reproyectado de EPSG:25830 a EPSG:4326 (WGS84)
  - Guardado como `data/raw/secciones_balears.gpkg` (5.3 MB)
- [x] Descargar **Inside Airbnb listings** Mallorca (45.741 listings) y Menorca (8.492 listings)
  - URL Mallorca: `https://data.insideairbnb.com/spain/islas-baleares/mallorca/2026-06-23/data/listings.csv.gz`
  - URL Menorca: `https://data.insideairbnb.com/spain/islas-baleares/menorca/2026-06-30/data/listings.csv.gz`
- [x] Recibir **HUT Eivissa 2026** del usuario (archivo HTML-as-xls, convertido a `hut_eivissa_2026-07-14.csv` con 2.369 registros y 18.184 plazas)
- [x] Recibir **IBESTAT Formentera 2019** del usuario (archivo OLE .xls, convertido a `ibestat_formentera_2019.json` con 1.375 establecimientos y 14.935 plazas)
- [x] **Insight del usuario**: el problema real son los ilegales, no los legales. Mallorca/Menorca (Airbnb) capturan realidad; Eivissa/Formentera (HUT) solo capturan legal. **La diferencia entre ambas cifras ES la denuncia narrativa**.

### Validacion
- [x] Shapefile: 36.554 features Espana, 674 en Illes Balears, CRS WGS84 OK
- [x] XLSXs validados con openpyxl. Solo sheet `tabla-59531` de `viviendas vacias-hipotecas.xlsx` es el dato util (los otros 5 sheets son hipotecas). `39365(1).xlsx` tiene 1 sheet util (`tabla-39365`).
- [x] Listings Airbnb Mallorca y Menorca validados (90 columnas, lat/lon/room_type/price/availability_365 OK)
- [x] HUT Eivissa 2026 validado: 2.369 registros en 5 municipios + 5 anomalias. Columna `Referencia cadastral` (20 chars) geocodificable.
- [x] IBESTAT Formentera 2019 validado: 1.375 establecimientos, 14.935 plazas. Datos agregados a nivel isla.
- [x] Anotado en `data/raw/VALIDACION.md`

### Cierre
- [x] Commit final con tag `fase-0-completa` (commits `1e86070` y `99ad1f8`)
- [x] Actualizar PLAN.md: marcar Fase 0 como completada
- [x] Anotar problemas y decisiones en este documento

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

Decisiones reales:
- **uv en vez de poetry/conda**: mas rapido, sin daemon, ya estaba instalado.
- **Python 3.10.18 seleccionado por uv** (no la 3.14.3 del sistema) para maxima compatibilidad con geopandas y GDAL.
- **Node 20 (no la 17 que estaba via nvm)** porque Astro requiere 18.17+ o 20.3+.
- **pnpm 9 (no 10)** porque pnpm 10+ requiere Node 22.13.
- **Shapefile procesado a GeoPackage (.gpkg) en vez de mantener .shp**: 110MB de SHP -> 5.3MB de GPKG, mas portable, mejor soporte en geopandas.
- **Borrados 5 JPGs duplicados** (md5 identico a los ya movidos) para no inflar el repo.
- **15 JPGs y capturas fuera de git** (40MB) por tamano, solo Info.pdf en git (36KB).
- **Dataset hibrido por isla segun la fuente mas adecuada**:
  - Mallorca + Menorca: Inside Airbnb (cubre realidad, legal+ilegal, snapshot 2026-06)
  - Eivissa: registro HUT oficial (snapshot 2026-07, 2.369 legal, con direccion y referencia catastral)
  - Formentera: IBESTAT agregado (snapshot 2019, 1.375 establecimientos, 14.935 plazas)
- **Mensaje narrativo clave**: la diferencia entre HUT (legal) y Airbnb (real) ES la denuncia. Documentar esto en `/metodologia`.

## Problemas encontrados

Problemas reales:
- **URLs INE tradicionales 404**: `https://www.ine.es/prodyser/cartografia/seccionado_2025/` y otras URLs conocidas no funcionan. **Solucion**: la URL real del ZIP es `https://www.ine.es/prodyser/cartografia/seccionado_2025.zip` (sin `/` final, extension `.zip`). El HTML de la pagina es una SPA y no expone el link.
- **Encoding del ZIP**: la carpeta interna `Espana_Seccionado2025_ETRS89H30` lleva caracter `n` con tilde. `unzip` por defecto falla con "Illegal byte sequence" en macOS. **Solucion**: extraer con `zipfile` de Python aplicando cp437 -> utf-8 fallback.
- **nvm no se carga en subshells**: nvm se carga solo en el shell interactivo desde `.zshrc`. Para usarlo en scripts/comandos one-shot hay que hacer `export NVM_DIR="$HOME/.nvm" && . "$NVM_DIR/nvm.sh" && nvm use 20` o usar la ruta absoluta `~/.nvm/versions/node/v20.20.2/bin/`.
- **Disk al 90%**: solo 22GB libres. Considerar borrar el ZIP de 60MB tras validar el .gpkg.
- **Inside Airbnb solo Mallorca+Menorca**: confirmado que no hay datos para Eivissa/Formentera. Resolucion: usar HUT oficial (proporcionado por usuario) + IBESTAT (tambien del usuario).
- **Archivos del usuario con formato incorrecto**:
  - `List-habitatges-turistics_*.xls` es HTML con extension .xls (encoding ISO-8859-1, no UTF-8).
  - `IBESTAT_indicador_*.xls` es binario OLE .xls real (encoding latin1 implicito).
  - Para .xls en pandas moderno: instalar `xlrd<2.0` y usar `engine='xlrd'`. Para .xls binario: usar `xlrd.open_workbook` directo.

## Proximos pasos

Fase 1: pipeline de datos Python. Entrada: archivos en `data/raw/`. Salida: `dataset.parquet` y `tiles.pmtiles` en `data/output/`. Ver `FASE-1-datos.md`.

**Decisiones para Fase 1**:
- Como geocodificar el HUT de Eivissa con su `Referencia cadastral` para hacer join con secciones censales (Catastro publica descargador por referencia, o servicio WFS)
- Como estimar el dato de "vivienda semi-vacia" por seccion censal a partir del XLSX INE (el XLSX tiene datos agregados por municipio, NO por seccion)
- Como unir Airbnb (lat/lon, por isla) con HUT (direccion+catastral, por municipio) en un unico dataset por seccion censal
- Como presentar la falta de uniformidad Mallorca/Menorca vs Eivissa/Formentera en la visualizacion final
