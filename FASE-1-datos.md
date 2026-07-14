# FASE 1 - Datos (semana 2)

## Objetivo

Producir el dataset final por seccion censal con dos variables clave: (a) % de viviendas semi-vacias (CCAA, del INE) y (b) listings de Airbnb + HUT + IBESTAT por seccion censal (Mallorca, Menorca, Eivissa, Formentera). Generar archivos listos para la web: `dataset.parquet` y `tiles.pmtiles`.

## Limitacion importante detectada

El XLSX `tabla-59531` del INE (vivienda por intensidad de uso a partir del consumo electrico) **solo tiene 2 filas de datos**: Total Nacional y Balears, Illes. Esta a nivel de CCAA, **no a nivel de seccion censal**. No podemos cruzar vivienda semi-vacia con seccion censal.

**Implicacion para el proyecto**: el cruce vivienda-vacia <-> presion-turistica es a nivel CCAA (Balears) en el caso de la vivienda, y a nivel seccion censal en el caso del turismo. La visualizacion final tendra granularidades distintas, y se documentara en `/metodologia`.

**Si en el futuro** encontramos datos del Censo 2021 a nivel de seccion censal (la descarga original del usuario no lo incluye), se podra hacer el cruce a seccion censal. Pendiente explorar.

## Granularidad por fuente de datos

| Fuente | Nivel de dato | Granularidad real |
|---|---|---|
| INE XLSX vivienda | CCAA | Balears Illes (no seccion censal) |
| INE XLSX vivienda turistica | CCAA | Balears Illes serie temporal |
| Inside Airbnb Mallorca+Menorca | Punto (lat/lon) | Seccion censal (spatial join) |
| Shapefile INE | Poligono | Seccion censal |
| HUT Eivissa | Direccion + Ref. Catastral | Municipio (5 chars de la RC) o seccion censal (geocodificando RC) |
| IBESTAT Formentera 2019 | Isla | Isla (agregado, sin parcela) |

## Tareas

### 1. Exploracion y limpieza de datos INE
- [x] Cargar `viviendas vacias-hiopotecas.xlsx` -> sheet `tabla-59531`. Extraer:
  - Viviendas totales (Balears Illes): 652.123
  - Viviendas vacias: 105.632 (16.2%)
  - Mediana consumo: 2.869 kWh
  - Viviendas de uso esporadico: 44.802 (6.9%)
- [x] Cargar `39365(1).xlsx` -> sheet `tabla-39365`. Extraer serie temporal % viviendas turisticas en Balears (ultimo: 3.74% en 2025M05)

### 2. Carga geoespacial
- [x] Cargar `data/raw/secciones_balears.gpkg` con geopandas (674 features, CRS WGS84)

### 3. Inside Airbnb Mallorca+Menorca
- [x] Cargar `airbnb_mallorca_listings.csv.gz` y `airbnb_menorca_listings.csv.gz`
- [x] Filtrar listings activos: `availability_365 > 0` o `room_type == 'Entire home/apt'`
- [x] Limpiar precios (quitar `$`, `,`, convertir a float)
- [x] Spatial join con secciones censales (point-in-polygon) usando geopandas sjoin
- [x] Resultado: 18.175 listings geo-localizados (14.644 Mallorca + 3.531 Menorca) en 456 secciones

### 4. HUT Eivissa
- [x] Cargar `hut_eivissa_2026-07-14.csv` (2.364 registros)
- [x] Extraer municipio de la `Referencia cadastral` (primeros 5 chars = CUMUN)
- [x] Join con shapefile por NMUN -> agregar a nivel municipio
- [x] Detalle: Sant Josep 945/7296, Santa Eulària 803/6249, Sant Antoni 330/2486, Sant Joan 245/1917, Eivissa 41/236
- [ ] (Opcional, v2) Geocodificar la RC exacta contra el Catastro para llegar a seccion censal

### 5. IBESTAT Formentera
- [x] Cargar `ibestat_formentera_2019.json`
- [x] Solo permite agregacion a nivel isla (1.375 establecimientos, 14.935 plazas)

### 6. Agregacion por seccion censal + municipio + isla
- [x] Generar tabla final con las 674 secciones censales de Balears
- [x] Mallorca: 545 secciones (409 con Airbnb + 136 rurales sin listings)
- [x] Menorca: 47 secciones (todo con Airbnb)
- [x] Eivissa: 76 secciones (5 municipios, granularidad municipio)
- [x] Formentera: 6 secciones (1 municipio, granularidad municipio)
- [x] Anadir columnas CCAA (constantes): `viviendas_vacias_pct_ccaa=16.2`, `viviendas_uso_esporadico_pct_ccaa=6.9`, `viviendas_turisticas_pct_ccaa_2025M05=3.74`
- [x] Fallback: secciones rurales sin datos asignadas a Mallorca/Menorca por CMUN

### 7. Generacion de archivos finales
- [x] `data/output/dataset.parquet` (41KB, 674 filas, 33 columnas sin geometria)
- [x] `data/output/dataset.gpkg` (5.3MB, geometrias completas)
- [x] `data/output/dataset_web.json` (1.1KB, resumen por isla)
- [x] `data/output/tiles.pmtiles` (1.5MB, choropleth con tippecanoe z0-z13)
- [ ] (Fase 2) Copiar outputs a `web/public/data/`

### 8. Validacion
- [x] `dataset.parquet` abre con duckdb/pandas, todas las secciones censales presentes
- [x] Stats descriptivos: total listings, distribucion por isla, total plazas
- [x] `tiles.pmtiles` magic `PMTi` valido
- [ ] Screenshots del mapa en Jupyter notebook (diferido a Fase 2 con web real)

### 9. Cierre
- [ ] Commit final con tag `fase-1-completa`
- [ ] Actualizar PLAN.md
- [x] Documentar en `data/output/STATS.md` las estadisticas finales

## Comandos clave

```bash
# Validar parquet con duckdb
python -c "import duckdb; print(duckdb.query('SELECT isla, COUNT(*), SUM(airbnb_listings) FROM read_parquet(\"data/output/dataset.parquet\") GROUP BY isla').to_df())"

# Pipeline completo (reproducible)
python3 scripts/01_load_sources.py
python3 scripts/02_build_dataset.py
python3 scripts/03_generate_tiles.py
```

## Criterio de "fase terminada"

- [x] `data/output/dataset.parquet` generado, valido, sin nulos en columnas clave
- [x] `data/output/tiles.pmtiles` generado y servible
- [x] Spatial join Mallorca+Menorca con tasa de exito: 18.175/54.233 = 33.5% (filtrados por actividad real; el resto son anuncios inactivos)
- [x] `STATS.md` documenta: n secciones, n listings por isla, distribuciones, limitaciones
- [x] Scripts Python reproducibles en `scripts/`
- [ ] Screenshots del mapa en Jupyter notebook (diferido a Fase 2)
- [ ] Commit final con tag `fase-1-completa`

## Decisiones tomadas durante la fase

1. **Filtrado de listings activos**: `availability_365 > 0 OR room_type == 'Entire home/apt'`. Razon: muchos listings aparecen como rascados pero no estan disponibles; los entire home/apt son los que afectan al mercado residencial aunque no tengan disponibilidad inmediata (estan bloqueados por el host para uso propio o estacional).
2. **Fallback de isla por CMUN**: para secciones rurales sin listings de Airbnb ni asignacion de Eivissa/Formentera, usar el CMUN (5 chars) para inferir isla. Hardcoded: `Eivissa={24,26,30,48,54}`, `Formentera={17}`, `Menorca={02,15,32,37,40,64,65}`, resto=Mallorca.
3. **Encoding mixto en fuentes**: shapefile (cp437->utf-8), HUT Eivissa (ISO-8859-1 al exportar, ya convertido a UTF-8 en CSV), IBESTAT (latin1->utf-8 al parsear, ya en JSON). El script `01_load_sources.py` asume los archivos ya normalizados en `data/raw/`.
4. **Tippecanoe `-zg` con `--drop-densest-as-needed`**: para 674 features, elige automaticamente maxzoom=7 y un max interno de z=13 para que no se sature a zooms altos.
5. **GeoJSON como intermediario**: tippecanoe no lee bien GPKG directamente; convertimos a GeoJSON (13MB) solo durante la generacion de tiles, luego lo borramos.
6. **Comits de los outputs**: `data/output/dataset.gpkg` (5.3MB) y `dataset.geojson` (intermedio) se ignoran en git; `dataset.parquet` (41KB), `dataset_web.json` (1.1KB), `tiles.pmtiles` (1.5MB) y `STATS.md` (2KB) se commitean para que la web funcione sin re-correr el pipeline.

## Problemas encontrados

1. **Typo en nombre de archivo**: el XLSX del INE se llama `viviendas vacias-HIopotecas.xlsx` (con "hiopotecas" en vez de "hipotecas"). El primer `01_load_sources.py` tenia un typo distinto (`h-i-p-o`) que daba FileNotFoundError. Resuelto en este pase.
2. **Conflicto de sufijos en merge**: el primer `02_build_dataset.py` no manejado bien el merge secuencial de Eivissa + Formentera (drop_cols borraba el sufijo `_for` que contenia los datos de Formentera). Resuelto con columnas `*_final` explicitas.
3. **Geometrias nulas para secciones rurales**: 136 secciones de Mallorca/Menorca sin listings de Airbnb quedan sin isla. Resuelto con fallback CMUN.
4. **Maximo vs suma en stats agregadas**: el primer `STATS.md` calculaba `hut_registros.max()` para Eivissa, que daba 945 (el municipio mas grande), no 2.364 (el total). Resuelto calculando el total antes del merge con secciones.

## Proximos pasos

Fase 2: web MVP con Astro + MapLibre GL JS. Ver `FASE-2-web-mvp.md`.
