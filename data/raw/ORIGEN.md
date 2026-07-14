# Origen de las dades en `data/raw/`

## `viviendas vacias-hipotecas.xlsx`

- **Origen**: Instituto Nacional de Estadistica (INE). Tabla derivada del "Censo de poblacion y viviendas" + datos de consumo electrico.
- **URL de descarga**: https://www.ine.es (tabla 39365 + tabla especifica d'intensitat d'us)
- **Fecha de descarga**: 2025 (proporcionado por el usuario del proyecto)
- **Descripcion**: 6 fulles. La full 1 conte dades d'intensitat d'us de les vivendes segons consum electric per seccio censal. Inclou Total Nacional + Illes Balears (provincies + seccions).
- **Tamano**: 35 KB

## `39365(1).xlsx`

- **Origen**: Instituto Nacional de Estadistica (INE). Tabla 39365 - "Viviendas turisticas en Espana".
- **URL de descarga**: https://www.ine.es/jaxiT3/Tabla.htm?t=39365
- **Fecha de descarga**: 2025 (proporcionado por el usuario del proyecto)
- **Descripcion**: 1 full. Serie temporal 2020M08 - 2025M05. Percentage de vivendes turistiques sobre el total per comunitat autonoma.
- **Tamano**: 10 KB

## Shapefile de secciones censales de Balears

- **Origen**: Instituto Nacional de Estadistica (INE). Cartografia censal.
- **URL de descarga**: https://www.ine.es/prodyser/cartografia/seccionado_2025/
- **Fecha de descarga**: (pendiente, ejecutar en setup de Fase 0)
- **Descripcion**: Poligons de les seccions censals per a les Illes Balears.
- **CRS original**: ETRS89 (EPSG:4258), reprojectar a WGS84 (EPSG:4326) per a la web.

## Inside Airbnb listings

- **Origen**: Inside Airbnb (proyecto independiente que scrapea Airbnb y publica datos abiertos).
- **URL de descarga**: http://insideairbnb.com/get-the-data/
- **Fecha de descarga**: (pendiente, ejecutar en setup de Fase 0)
- **Descripcion**: Listings georreferenciats (lat/lon) amb informacio de tipus, disponibilitat i preu. Snapshots separats per Mallorca, Menorca, Eivissa i Formentera.
- **Licencia**: Creative Commons (consultar web del proyecto).
