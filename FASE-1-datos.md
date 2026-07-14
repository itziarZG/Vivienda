# FASE 1 - Datos (semana 2)

## Objetivo

Producir el dataset final agregado por seccion censal con dos variables clave: (a) % de viviendas semi-vacias estimado por consumo electrico, y (b) numero/densidad de listings de Airbnb. Generar archivos listos para la web: `dataset.parquet` (tabla) y `tiles.pmtiles` (visualizacion geoespacial).

## Tareas

### Exploracion y limpieza
- [ ] Cargar `viviendas vacias-hipotecas.xlsx`, inspeccionar las 6 sheets, identificar la que tiene datos por seccion censal
- [ ] Filtrar registros de Illes Balears (codigos INE 07xxx)
- [ ] Normalizar columnas: codigo seccion censal, % viviendas semi-vacias, % viviendas vacias, consumo mediano kWh
- [ ] Cargar `39365(1).xlsx` (tabla 39365 viviendas turisticas), agregar a Balears como dato contextual

### Carga geoespacial
- [ ] Cargar shapefile de secciones censales Balears con geopandas
- [ ] Reproyectar a WGS84 (EPSG:4326) si esta en ETRS89 u otro CRS
- [ ] Inspeccionar: codigo unico de seccion censal, geometria valida, total de features

### Inside Airbnb
- [ ] Cargar los 4 CSVs de listings (Mallorca, Menorca, Eivissa, Formentera)
- [ ] Columnas clave: `id`, `latitude`, `longitude`, `room_type`, `availability_365`, `price`, `neighbourhood`
- [ ] Filtrar listings activos: `availability_365 > 0` y/o `room_type == 'Entire home/apt'`
- [ ] Limpiar precios (quitar `$`, `,`, convertir a float)

### Spatial join
- [ ] Point-in-polygon: cada listing -> seccion censal correspondiente
- [ ] Manejar listings fuera de poligonos (zonas rurales, agua): log + excluir
- [ ] Resultado: DataFrame con `(seccion_censal, n_listings)` por isla

### Agregacion por seccion censal
- [ ] Join: seccion_censal <- (datos INE vivienda) + (conteo Airbnb)
- [ ] Variables finales por seccion censal:
  - `cod_seccion` (PK)
  - `municipio`, `isla`
  - `n_viviendas_total`
  - `pct_viviendas_vacias`
  - `pct_uso_esporadico`
  - `consumo_mediano_kwh`
  - `n_listings_airbnb`
  - `listings_por_100_viviendas`
  - `geometry` (poligono)
- [ ] Guardar como `data/output/dataset.parquet` (formato columnar eficiente)

### Tiles para mapa web
- [ ] Generar `data/output/tiles.pmtiles` con tippecanoe a partir del GeoPackage del dataset
- [ ] Incluir atributos de visualizacion en los tiles (no solo geometria)
- [ ] Generar version "minima" de tiles (zoom 0-12) para web

### Validacion
- [ ] `dataset.parquet` abre con duckdb/pandas
- [ ] `tiles.pmtiles` se sirve correctamente y se ve en MapLibre local
- [ ] Sanity checks: nº listings total razonable (>5.000 en Mallorca, >1.000 en Eivissa), sin nulos en columnas clave
- [ ] Documentar estadisticas descriptivas en `data/output/STATS.md`

### Cierre
- [ ] Commit final con tag `fase-1-completa`
- [ ] Actualizar PLAN.md
- [ ] Visualizar el mapa en un Jupyter notebook rapido para validar (screenshot al menos)

## Comandos clave

```bash
# Convertir a GeoPackage para tippecanoe
ogr2ogr -f GPKG data/output/dataset.gpkg data/output/dataset.parquet

# Generar tiles
tippecanoe -o data/output/tiles.pmtiles \
  -zg \
  --drop-densest-as-needed \
  -l cases \
  --read-parallel \
  data/output/dataset.gpkg

# Servir localmente para testear
python -m http.server 8000 --directory data/output
# Abrir http://localhost:8000 en navegador con MapLibre

# Validar parquet con duckdb
python -c "import duckdb; print(duckdb.query('SELECT isla, COUNT(*), AVG(pct_uso_esporadico), SUM(n_listings_airbnb) FROM \"data/output/dataset.parquet\" GROUP BY isla').to_df())"
```

## Criterio de "fase terminada"

- [x] `data/output/dataset.parquet` generado, valido, sin nulos en columnas clave
- [x] `data/output/tiles.pmtiles` generado y servible
- [x] Spatial join con tasa de exito > 95% (listings asignados a seccion censal)
- [x] `STATS.md` documenta: nº secciones, nº listings por isla, distribuciones, outliers
- [x] Screenshot del mapa en Jupyter notebook como evidencia visual
- [x] Scripts Python reproducibles en `scripts/` con comentarios sobre decisiones
- [x] Commit final con tag `fase-1-completa`

## Decisiones tomadas durante la fase

_Llenar durante la ejecucion. Ejemplos:_
- _Decidimos filtrar listings por `availability_365 > 60` para excluir inactivos esporadicos._
- _Decidimos calcular "pct_uso_esporadico" como 1 - (consumo_mediano / p75 consumo), no como categoria INE directa._
- _El join espacial asigna por punto interior al poligono; los listings a < 50m del borde se asignan al mas cercano (regla documentada)._

## Problemas encontrados

_Llenar durante la ejecucion._

## Proximos pasos

Fase 2: web MVP con Astro + MapLibre. Ver `FASE-2-web-mvp.md`.
