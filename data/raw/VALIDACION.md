# VALIDACION de los datos en `data/raw/`

Resultado de la validacion de los archivos descargados. Ejecutado en setup de Fase 0.

## Datos INE (proporcionados por el usuario)

### `viviendas vacias-hipotecas.xlsx`

- Tamano: 34.2 KB
- 6 sheets
- **Sheet util: `tabla-59531`** (Viviendas por intensidad de uso a partir del consumo electrico)
- Los otros 5 sheets son datos de hipotecas (NO se usan en este proyecto)
- Encoding: UTF-8 (con cabecera en espanol)

### `39365(1).xlsx`

- Tamano: 10.0 KB
- 1 sheet util: `tabla-39365` (Viviendas turisticas en Espana, % sobre total, serie 2020M08-2025M05)

## Shapefile INE 2025

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

## Datos de alquiler turistico / temporal

### Inside Airbnb listings (Mallorca + Menorca)

- **Origen**: Inside Airbnb (datos abiertos scrapeados de Airbnb)
- **URLs**:
  - Mallorca: `https://data.insideairbnb.com/spain/islas-baleares/mallorca/2026-06-23/data/listings.csv.gz` (10.0 MB, 45.741 listings)
  - Menorca: `https://data.insideairbnb.com/spain/islas-baleares/menorca/2026-06-30/data/listings.csv.gz` (2.3 MB, 8.492 listings)
- **Columnas clave**: id, latitude, longitude, room_type, property_type, price, availability_365, minimum_nights, neighbourhood, host_id
- **90 columnas** en total (snapshot completo)
- **Coverage**: Airbnb listings (incluye legales E ILEGALES - cota inferior de la presion real)
- **Limitacion**: NO hay datos para Eivissa ni Formentera

### Registro oficial HUT de Eivissa (proporcionado por el usuario)

- **Origen**: Govern de les Illes Balears - Conselleria de Turisme
- **Archivo original**: `List-habitatges-turistics_-14072026.xls` (HTML con extension .xls, encoding ISO-8859-1)
- **CSV limpio**: `hut_eivissa_2026-07-14.csv` (568 KB)
- **Snapshot**: 14 de julio de 2026
- **2.369 registros** totales (5 municipios + 5 anomalias "NUEVO BOLSA DE PLAZAS")
- **18.184 plazas/camas** totales
- **Distribucion por municipio**:
  - SANT JOSEP DE SA TALAIA: 945
  - SANTA EULARIA DES RIU: 803
  - SANT ANTONI DE PORTMANY: 330
  - SANT JOAN DE LABRITJA: 245
  - EIVISSA: 41
  - NUEVO BOLSA DE PLAZAS: 5 (anomalias, excluir)
- **Columnas clave**:
  - Numero Inscripcio (numero de registro oficial)
  - Referencia cadastral (20 caracteres, geocodificable a parcela)
  - Direccion (texto)
  - Municipi (municipio)
  - Total Places (plazas/camas)
  - Sub-tipus (Estancia/Vivienda Turistica Vacacional)
- **Coverage**: SOLO accommodations legales registradas
- **Insight del usuario**: "el problema no son los legales, son los que no son legales. En Ibiza, ninguna vivienda en plurifamiliar puede alquilarse y hay miles de anuncios". Por tanto, el HUT es una COTA INFERIOR muy conservadora.

### IBESTAT Formentera 2019 (proporcionado por el usuario)

- **Origen**: IBESTAT (Institut d'Estadistica de les Illes Balears) - indicador 208.34208023
- **Archivo original**: `IBESTAT_indicador_208_34208023_Establiments_turístics_2019.xls` (38.5 KB, OLE binary .xls)
- **JSON limpio**: `ibestat_formentera_2019.json` (2 KB)
- **Snapshot**: ano 2019 (datos antiguos, no se encontro nada mas reciente)
- **Datos**: Tabla agregada con tipologia, unidades y plazas para Formentera como una unidad
- **1.375 unidades totales, 14.935 plazas totales**
- **Desglose**:
  - HABITATGES TURISTICS DE VACANCES (HTV): 168 unidades, 1.927 plazas
  - ESTADES TURISTIQUES: 1.086 unidades, 4.912 plazas
  - Hotels (1-5*): 19 unidades, 3.008 plazas
  - Apartments: 73 unidades, 2.758 plazas
  - Otros: resto
- **Coverage**: SOLO establishments legales (datos oficiales agregados)
- **Limitacion**: No incluye datos a nivel de parcela/direccion. Datos agregados solo a nivel isla.

## Resumen de cobertura

| Isla | Shapefile | Listings (todos) | Legal (HUT) | Plazas legales | Calidad |
|---|---|---|---|---|---|
| Mallorca | OK (674 secc.) | OK (45.741 Airbnb) | n.d. | n.d. | Buena (Airbnb) |
| Menorca | OK (674 secc.) | OK (8.492 Airbnb) | n.d. | n.d. | Buena (Airbnb) |
| Eivissa | OK (674 secc.) | NO en Airbnb | OK (2.369 HUT 2026) | 18.184 | Cota inferior (HUT) |
| Formentera | OK (674 secc.) | NO en Airbnb | OK (1.375 estab. 2019) | 14.935 | Cota inferior (agregado) |

**Total listings Airbnb disponibles**: 54.233 (Mallorca + Menorca)
**Total establishments legales documentados**: 3.744 (Eivissa 2.369 + Formentera 1.375)
**Total plazas legales documentadas**: 33.119 (Eivissa 18.184 + Formentera 14.935)

## Implicaciones para el proyecto

- **Cobertura geografica**: 4/4 islas, pero con calidad desigual
- **Cobertura de realidad**: Mallorca+Menorca capturan Airbnb (cota inferior de presion real). Eivissa+Formentera solo capturan legal (cota inferior de legal). La realidad (legal+ilegal) es desconocida para Eivissa/Formentera
- **Mensaje narrativo**: la diferencia entre Airbnb y HUT es la denuncia. "El Govern reconoce X plazas legales en Eivissa, pero en Mallorca donde tenemos el dato completo, las plazas reales son Y veces mas"
- **Falta**: scraping o fuente complementaria para Eivissa/Formentera que capture listings ilegales (no en v0)

## Resumen de espacio en disco

- Carpeta `data/raw/`: ~79 MB total
  - XLSXs INE: 45 KB
  - Shapefile ZIP: 60 MB
  - GeoPackage Balears: 5.3 MB
  - Listings Airbnb Mallorca+Menorca: 12.3 MB
  - HUT Eivissa HTML fuente: 4.2 MB
  - HUT Eivissa CSV limpio: 568 KB
  - IBESTAT Formentera JSON: 2 KB
- Carpeta `docs/conferencia-OHIB-2025/`: ~50 MB (15 JPGs + PDF)
- Total proyecto local: ~130 MB
