# VALIDACION de los datos en `data/raw/`

Resultado de la validacion de los archivos descargados. Ejecutado en setup de Fase 0.

## `viviendas vacias-hipotecas.xlsx`

- Tamano: 34.2 KB
- 6 sheets
- **Sheet util: `tabla-59531`** (Viviendas por intensidad de uso a partir del consumo electrico)
- Los otros 5 sheets son datos de hipotecas (NO se usan en este proyecto)
- Encoding: UTF-8 (con cabecera en espanol)

## `39365(1).xlsx`

- Tamano: 10.0 KB
- 1 sheet util: `tabla-39365` (Viviendas turisticas en Espana, % sobre total, serie 2020M08-2025M05)

## `seccionado_2025.zip` + `secciones_balears.gpkg`

- **Origen**: Instituto Nacional de Estadistica (INE). Cartografia censal 2025.
- **URL**: https://www.ine.es/prodyser/cartografia/seccionado_2025.zip
- **Tamano ZIP**: 57.5 MB (todo Espana, 36.554 features)
- **CRS original**: EPSG:25830 (ETRS89 Huso 30 Norte)
- **Tamano GeoPackage Balearic Islands**: 5.3 MB
- **CRS final**: EPSG:4326 (WGS84, listo para web)
- **Features en Illes Balears**: 674 secciones censales
- **Municipios en Illes Balears**: 67
- **Columnas**: CUSEC, CUMUN, CSEC, CDIS, CMUN, CPRO, CCA, CUDIS, CLAU2, NPRO, NCA, CNUT0/1/2/3, NMUN, geometry
- **Codigos clave**:
  - CPRO = '07' para Balears
  - CCA = '04' para Illes Balears
  - CUSEC = CPRO(2) + CMUN(3) + CDIS(2) + CSEC(3), total 10 digitos

## Inside Airbnb listings

- **Origen**: Inside Airbnb (datos abiertos scrapeados de Airbnb)
- **URLs**:
  - Mallorca: `https://data.insideairbnb.com/spain/islas-baleares/mallorca/2026-06-23/data/listings.csv.gz` (10.0 MB, 45.741 listings)
  - Menorca: `https://data.insideairbnb.com/spain/islas-baleares/menorca/2026-06-30/data/listings.csv.gz` (2.3 MB, 8.492 listings)
- **Limitation**: Inside Airbnb NO tiene datos para Eivissa ni Formentera. Solo Mallorca y Menorca estan disponibles.
- **Columnas clave**: id, latitude, longitude, room_type, property_type, price, availability_365, minimum_nights, neighbourhood, host_id
- **90 columnas** en total (snapshot completo)

## Resumen de cobertura

| Isla | Shapefile | Listings Airbnb | Cobertura |
|---|---|---|---|
| Mallorca | OK (secciones censales) | OK (45.741) | Completa |
| Menorca | OK (secciones censales) | OK (8.492) | Completa |
| Eivissa | OK (secciones censales) | **NO DISPONIBLE** | Parcial |
| Formentera | OK (secciones censales) | **NO DISPONIBLE** | Parcial |

**Total listings disponibles**: 54.233 (Mallorca + Menorca)
**Total listings Eivissa+Formentera**: 0 (pendiente fuente alternativa)

## Resumen de espacio en disco

- Carpeta `data/raw/`: ~78 MB (60 MB del ZIP, 5.3 MB del GPKG, 12.3 MB de listings Airbnb, 44 KB de XLSXs)
- Carpeta `docs/conferencia-OHIB-2025/`: ~50 MB (15 JPGs + PDF)
- Total proyecto local: ~130 MB
