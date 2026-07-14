# Origen de las dades en `data/raw/`

## Archivos INE (proporcionados por el usuario)

### `viviendas vacias-hipotecas.xlsx`

- **Origen**: Instituto Nacional de Estadistica (INE). Tabla derivada del "Censo de poblacion y viviendas" + datos de consumo electrico.
- **URL de descarga**: https://www.ine.es (tabla 39365 + tabla especifica d'intensitat d'us)
- **Fecha de descarga**: 2025 (proporcionado por el usuario del proyecto)
- **Descripcion**: 6 fulles. La full 1 conte dades d'intensitat d'us de les vivendes segons consum electric per seccio censal. Inclou Total Nacional + Illes Balears (provincies + seccions).
- **Tamano**: 35 KB

### `39365(1).xlsx`

- **Origen**: Instituto Nacional de Estadistica (INE). Tabla 39365 - "Viviendas turisticas en Espana".
- **URL de descarga**: https://www.ine.es/jaxiT3/Tabla.htm?t=39365
- **Fecha de descarga**: 2025 (proporcionado por el usuario del proyecto)
- **Descripcion**: 1 full. Serie temporal 2020M08 - 2025M05. Percentage de vivendes turistiques sobre el total per comunitat autonoma.
- **Tamano**: 10 KB

## Shapefile de secciones censales de Balears

- **Origen**: Instituto Nacional de Estadistica (INE). Cartografia censal.
- **URL de descarga**: https://www.ine.es/prodyser/cartografia/seccionado_2025.zip
- **Fecha de descarga**: 14 julio 2026 (descargado por el asistente)
- **Descripcion**: Poligons de les seccions censals per a les Illes Balears.
- **CRS original**: ETRS89 (EPSG:25830), reprojectat a WGS84 (EPSG:4326) per a la web.
- **Tamano ZIP**: 60 MB (todo Espana), GPKG Balearic Islands: 5.3 MB

## Inside Airbnb listings

- **Origen**: Inside Airbnb (proyecto independiente que scrapea Airbnb y publica datos abiertos).
- **URL de descarga**: http://insideairbnb.com/get-the-data/
- **Archivos descargados**:
  - Mallorca: `https://data.insideairbnb.com/spain/islas-baleares/mallorca/2026-06-23/data/listings.csv.gz` (10 MB)
  - Menorca: `https://data.insideairbnb.com/spain/islas-baleares/menorca/2026-06-30/data/listings.csv.gz` (2.3 MB)
- **Fecha**: snapshot 2026-06
- **Licencia**: Creative Commons (consultar web del proyecto)
- **Limitacion**: NO hay datos para Eivissa ni Formentera

## Registro oficial HUT de Eivissa (proporcionado por el usuario)

- **Origen**: Govern de les Illes Balears - Conselleria de Turisme. Registro oficial de Habitatges d'Us Turistic.
- **URL del portal**: https://www.caib.es (buscador publico, no descarga directa)
- **Archivo recibido**: `List-habitatges-turistics_-14072026.xls` (HTML con extension .xls, encoding ISO-8859-1)
- **Fecha**: 14 julio 2026
- **Tamano**: 4.2 MB original, 568 KB CSV limpio
- **Coverage**: SOLO accommodations legales registradas
- **Insight**: el problema real son los ilegales (no capturados aqui)

## IBESTAT Formentera 2019 (proporcionado por el usuario)

- **Origen**: IBESTAT (Institut d'Estadistica de les Illes Balears). Indicador 208.34208023 - "Establiments turistics de Formentera".
- **URL del portal**: https://ibestat.caib.es/ (indicador 208.34208023)
- **Archivo recibido**: `IBESTAT_indicador_208_34208023_Establiments_turístics_2019.xls` (OLE binary .xls)
- **Ano de referencia**: 2019 (no se encontro nada mas reciente)
- **Tamano**: 38.5 KB original, 2 KB JSON limpio
- **Coverage**: Datos agregados de Formentera (no por municipio, no por direccion)
- **Limitacion**: Solo establishments legales (oficial)
