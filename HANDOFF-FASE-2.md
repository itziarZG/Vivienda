# HANDOFF - Fase 2: Web MVP

> Documento de arranque para una conversación nueva. Léeme primero.
> Si acabas de empezar a trabajar en este proyecto: lee esto, luego `PLAN.md`, `FASE-1-datos.md` (sección "Decisiones tomadas" y "Problemas encontrados"), y ejecuta los 3 comandos de "Quick start".

## Qué es esto

Web pública que cruza vivienda semi-vacía (INE) con alquiler turístico (Airbnb + HUT + IBESTAT) en las 4 islas Baleares. Audiencia: ciudadanía ibicenca. Fin: denuncia del gap entre lo legal y la realidad.

**Nombre tentativo**: "Cases Tancades" (catalán). Pendiente cerrar en Fase 3.
**Stack**: Python (datos, ya hecho) + Astro (web) + MapLibre GL (mapa) + pmtiles (vector tiles) + Vercel (deploy).
**Estado**: Fase 0 + Fase 1 completadas. Tags `fase-0-completa`, `fase-1-completa` en git.

## Quick start

```bash
cd /Users/ichi/Desktop/DEV/Vivienda
git log --oneline -10                              # ver historia
git checkout fase-1-completa                       # asegurar punto de partida
ls data/output/                                    # ver outputs
cat data/output/STATS.md                           # leer los numeros
```

## Lo que ya existe (no rehacer)

| Archivo | Qué contiene | Tamaño |
|---|---|---|
| `data/output/dataset.parquet` | 674 filas, 33 columnas, sin geometría | 41KB |
| `data/output/dataset.gpkg` | Con geometrías (no en git) | 5.3MB |
| `data/output/dataset_web.json` | Resumen por isla, para `/` y `/metodologia` | 1KB |
| `data/output/tiles.pmtiles` | Vector tiles, layer `cases`, z0–z13 | 1.5MB |
| `data/output/STATS.md` | Números definitivos Fase 1 | 2KB |
| `scripts/01_load_sources.py` | Carga de fuentes | - |
| `scripts/02_build_dataset.py` | Spatial join + agregación | - |
| `scripts/03_generate_tiles.py` | Tippecanoe | - |
| `FASE-0-setup.md`, `FASE-1-datos.md`, `FASE-2-web-mvp.md` | Bitácoras | - |
| `PLAN.md` | Resumen ejecutivo + decisiones cerradas | - |

## Esquema del dataset (para el frontend)

`tiles.pmtiles` layer `cases`, una feature por sección censal:

```
CUSEC, NMUN, isla, granularidad, fuente
airbnb_listings, airbnb_entire_homes, airbnb_price_median
airbnb_accommodates_total, airbnb_revenue_total
airbnb_hosts_unicos, airbnb_con_licencia
hut_registros, hut_plazas, hut_habitaciones
plazas_turisticas
viviendas_vacias_pct_ccaa=16.2, viviendas_uso_esporadico_pct_ccaa=6.9
viviendas_turisticas_pct_ccaa_2025M05=3.74
```

Granularidad: `seccion_censal` (Mallorca+Menorca) o `municipio` (Eivissa+Formentera).

## Lo que hay que hacer (Fase 2)

Orden sugerido (cada paso valida el anterior):

1. `pnpm create astro@latest web/ --template basics --typescript strict --yes` desde `/Users/ichi/Desktop/DEV/Vivienda`
2. `pnpm add maplibre-gl pmtiles` + `pnpm add -D tailwindcss`
3. Copiar outputs a `web/public/`:
   - `data/output/tiles.pmtiles` → `web/public/tiles/dataset.pmtiles`
   - `data/output/dataset_web.json` → `web/public/data/dataset_web.json`
4. Página `/` (home) con 2 cifras de impacto + CTA a `/mapa`
5. Página `/mapa` con MapLibre + tiles pmtiles + popup on-click con stats de la sección
6. Página `/metodologia` con fuentes, limitaciones, snapshot dates
7. `pnpm dev` para iterar
8. Deploy a Vercel con `pnpm dlx vercel` (no requiere cuenta para primer deploy; usa login GitHub)

Snippet MapLibre + PMTiles ya en `FASE-2-web-mvp.md` líneas 79-130. Úsalo como base.

## Headlines y stats a destacar en el home

Cifras de impacto (de `STATS.md`):

- **18.175 listings activos** en Airbnb Mallorca+Menorca, con **105.738 plazas** (`accommodates`)
- **18.184 plazas legales** declaradas en HUT Eivissa — pero **40%** concentradas en Sant Josep (7.296) mientras Eivissa capital solo tiene **236** (41 registros)
- **95.4%** de los listings activos son `Entire home/apt` (pisos completos)
- **98.8%** tiene `license` rellenado en Airbnb — pero el Govern no valida ese campo, es autorreportado
- **$258M** de ingresos estimados Airbnb L365d en Mallorca+Menorca
- INE CCAA: **16.2%** de viviendas vacías + **6.9%** de uso esporádico = **23.1%** del parque residencial potencialmente "ocioso"

**Insight narrativo central** (el que engancha en prensa):
> En Eivissa hay 41 registros HUT legales en la ciudad (50.000 hab.) y 945 en Sant Josep. ¿Dónde están las 7.000+ plazas que oferta Airbnb en Eivissa? El gap entre el dato legal y el rascado ES la denuncia.

## Traps y gotchas (no perder tiempo)

1. **Typo persistente**: el XLSX del INE se llama `viviendas vacias-hiopotecas.xlsx` (con "h-i-o", no "h-i-p-o"). Si alguien lo "arregla" por legibilidad, el script 01 va a fallar.
2. **Dataset hybrid**: la columna `granularidad` indica si la feature es `seccion_censal` o `municipio`. NO mezclar al pintar — Eivissa/Formentera tienen un solo valor por municipio replicado a todas las secciones del municipio.
3. **Vivienda INE solo CCAA**: los `*_pct_ccaa` son constantes para TODAS las features. La sección censal no tiene dato de vivienda per se. **Documentar esto claramente en `/metodologia`**.
4. **No scrappear**: nunca Idealista, nunca Airbnb directo. Solo datos abiertos o del usuario. (Ya está en `.gitignore` y en el plan, pero confirmarlo en `/metodologia`.)
5. **No build sin pedir**: el usuario es dev pero odia perder tiempo en builds innecesarios. Iterar con `pnpm dev` y solo build cuando pida.
6. **Conventional commits**: usar `feat(web):`, `fix(map):`, etc. NUNCA añadir "Co-Authored-By" ni atribución a IA.
7. **Encoding**: los archivos raw ya están normalizados a UTF-8. Si reaparece algo raro, revisar.
8. **macOS case-insensitive**: la carpeta se creó como `VIvienda` pero el filesystem la resuelve como `Vivienda`. No es bug, ignorarlo.
9. **Node 20 obligatorio**: `nvm use 20` antes de cualquier `pnpm`. `pnpm 10+` requiere Node 22; usar `pnpm 9`.

## Preferencias del usuario (descubiertas en sesiones anteriores)

- Idioma del proyecto: **catalán principal** + castellano. El usuario escribe en español.
- Estilo: **documentación modular** (`PLAN.md` + 1 .md por fase), iteración paso a paso.
- Verificar claims antes de decir "sí": el usuario detecta acuerdo fácil y lo penaliza. Si no estás seguro, **di "dejame verificar"** y comprueba.
- Respetar la regla "no build": no compilar/ejecutar proyectos sin pedir.
- NO asumir respuestas: si hay duda, **preguntar con `question` tool**.
- **Honestidad radical sobre limitaciones**: si una fuente es CCAA, decirlo en `/metodologia` y en el tooltip del mapa.

## Datos cuantitativos de la conferencia OHIB (12-13 nov 2025)

Guardados en `docs/conferencia-OHIB-2025/` (15 JPGs + Info.pdf, ignorados en git). Datos clave para usar en el storytelling:

- Compraventa 2024 €/m²: Formentera 7.353 / Ibiza 4.331 / Mallorca 3.500 / Menorca 2.748 / Balears media 3.609
- CEE parque residencial Balears: 1,1% A, 2,2% B, 3,7% C, 9,5% D, 43,9% E, 12,5% F, 27,0% G → **83,4% en E/F/G**
- 34,79% unifamiliares vs 1,16% plurifamiliares
- Fuentes oficiales mapeadas: INE, Catastro, MIVAU, MTERD, DGHA, IBAVI, ATIB, IBESTAT, ICGIB

Frase literal del usuario que define el proyecto:
> "el problema no son los legales, son los que no son legales. En Ibiza, ninguna vivienda en plurifamiliar puede alquilarse y hay miles de anuncios."

## Preguntas abiertas (preguntar al usuario en la nueva sesión)

1. **¿Idioma del UI?** Catalan, castellano o bilingüe. Mi recomendación: catalán primario + toggle a castellano.
2. **¿Color del choropleth?** Variable: `plazas_turisticas` (visual) o `plazas_turisticas / viviendas_ccaa` (densidad relativa). Recomiendo densidad relativa con fallback a absoluto.
3. **¿Clustering Airbnb en `/mapa`?** Recomiendo SÍ: 18K puntos saturan el mapa. Sumar capa de puntos al pmtiles si se decide, o usar capa GeoJSON aparte.
4. **¿Vercel ya configurado?** Si no, decidir nombre del proyecto (`casestancades.vercel.app` está disponible presumiblemente).
5. **¿Dominio `.cat` o `.org` para Fase 3?** El usuario dijo "de momento el dominio no es importante".

## Estructura de archivos esperada al cerrar Fase 2

```
web/
├── astro.config.mjs
├── package.json
├── tailwind.config.mjs
├── public/
│   ├── tiles/dataset.pmtiles        # copiado de data/output/
│   └── data/dataset_web.json       # copiado de data/output/
├── src/
│   ├── components/
│   │   ├── Mapa.astro              # MapLibre + PMTiles
│   │   ├── CifraImpacto.astro
│   │   └── ...
│   ├── layouts/Base.astro
│   ├── pages/
│   │   ├── index.astro             # home
│   │   ├── mapa.astro
│   │   └── metodologia.astro
│   └── styles/global.css
└── README.md
```

## Convenciones de commits

```
feat(web): ...
fix(map): ...
chore(web): ...
docs(plan): ...
```

Tags al cerrar fase: `fase-2-completa`.

## Qué NO hacer

- No scrappear Idealista o Airbnb.
- No usar Leaflet (usar MapLibre GL).
- No usar TileMill/MBTiles (usar tippecanoe → pmtiles).
- No meter viviendas vacías a nivel CCAA fingiendo que son sección censal.
- No desplegar en dominio definitivo en Fase 2 (eso es Fase 3).
- No añadir "Co-Authored-By" ni atribución a IA en commits.

## TL;DR

Fase 2 = Astro + MapLibre + pmtiles + 3 páginas + Vercel. Los datos ya están. Las decisiones difíciles (granularidad, fuentes, framing) ya están tomadas. Solo queda ejecutar.
