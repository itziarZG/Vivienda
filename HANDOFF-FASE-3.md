# HANDOFF - Fase 3: Lanzamiento

> Documento de arranque para una conversacion nueva. Leeme primero.
> Si acabas de empezar a trabajar en este proyecto: lee esto, luego `PLAN.md`, `FASE-3-lanzamiento.md`, y ejecuta los 3 comandos de "Quick start".

## Que es esto

Web publica que cruza vivienda semi-vacia (INE) con alquiler turistico (Airbnb + HUT + IBESTAT) en las 4 islas Baleares. Audiencia: ciudadania ibicenca. Fin: denuncia del gap entre lo legal y la realidad.

**Nombre tentativo**: "Cases Tancades" (catalan). **Estado**: confirmado en Fase 2 (header y meta tags).

**Stack**:
- Datos: Python (pandas, geopandas, duckdb) — pipeline en `scripts/`
- Web: Astro 7.0.9 + Tailwind 4.3.2 + MapLibre GL 5.24.0 + PMTiles 4.4.1
- Node 22.13.1 + pnpm 11.9.0
- Deploy: Vercel (aun sin configurar)

**Estado**: Fases 0, 1 y 2 completadas. Tags `fase-0-completa`, `fase-1-completa`, `fase-2-completa` en git.

## Quick start

```bash
cd /Users/ichi/Desktop/DEV/Vivienda
git log --oneline -10                  # ver historia
git checkout fase-2-completa           # asegurar punto de partida
ls web/                                # ver estructura web
cd web && pnpm dev                     # iterar (http://localhost:4321)
```

## Lo que ya existe (no rehacer)

| Archivo | Que contiene | Tamano |
|---|---|---|
| `data/output/dataset.parquet` | 674 filas, 33 columnas, sin geometria | 41KB |
| `data/output/dataset.gpkg` | Con geometrias (no en git) | 5.3MB |
| `data/output/dataset_web.json` | Resumen por isla, para / y /metodologia | 1KB |
| `data/output/tiles.pmtiles` | Vector tiles, layer `cases`, z0-z13 | 1.5MB |
| `data/output/STATS.md` | Numeros definitivos Fase 1 | 2KB |
| `web/public/tiles/dataset.pmtiles` | Copia de tiles para Vercel | 1.5MB |
| `web/public/data/dataset_web.json` | Copia del JSON para el frontend | 1KB |
| `web/public/data/airbnb_listings.geojson` | 18.391 puntos para clusters | 3MB |
| `web/src/pages/{index,mapa,metodologia}.astro` | 3 paginas con i18n CA/ES | - |
| `web/src/i18n/{ca,es}.json` | Diccionario i18n (~120 keys) | - |
| `scripts/01_load_sources.py` | Carga de fuentes | - |
| `scripts/02_build_dataset.py` | Spatial join + agregacion (Fase 1) | - |
| `scripts/03_generate_tiles.py` | Tippecanoe | - |
| `scripts/04_regenerate_web_json.py` | Fix bug suma por seccion en JSON | - |
| `scripts/05_export_airbnb_geojson.py` | Genera GeoJSON para clusters | - |
| `FASE-0-setup.md`, `FASE-1-datos.md`, `FASE-2-web-mvp.md` | Bitacoras | - |
| `PLAN.md` | Resumen ejecutivo + decisiones cerradas | - |

## Estructura del proyecto web

```
web/
├── astro.config.mjs         # Tailwind via @tailwindcss/vite
├── package.json             # astro, maplibre-gl, pmtiles, tailwind
├── tsconfig.json            # extends astro/tsconfigs/strict
├── public/
│   ├── tiles/dataset.pmtiles
│   ├── data/dataset_web.json
│   └── data/airbnb_listings.geojson
└── src/
    ├── data/dataset.ts      # Lee public/data/dataset_web.json en SSR
    ├── i18n/
    │   ├── ca.json          # ~120 keys
    │   ├── es.json
    │   └── index.ts         # getLangFromAstroCookies + t() + format()
    ├── components/
    │   ├── CifraImpacto.astro
    │   ├── Footer.astro
    │   ├── Header.astro     # Nav + LanguageToggle
    │   ├── LanguageToggle.astro
    │   └── Mapa.astro       # MapLibre + PMTiles + clusters
    ├── layouts/
    │   └── Base.astro       # Lee cookie lang + OpenGraph
    ├── pages/
    │   ├── index.astro      # Home
    │   ├── mapa.astro       # Mapa interactivo
    │   └── metodologia.astro
    └── styles/global.css    # Tailwind + @theme brand
```

## Paginas funcionales

- **/** (home) — Hero con headline + 6 cifras impacto (18.175 listings, 19.696 plazas, 18.184 HUT, 40% concentracion Sant Josep, 16,2% vacios, 6,9% esporadico) + 3 parrafos narrativos + tabla per illa + 4 story cards.
- **/mapa** — MapLibre 100vh. Filtro por isla. Toggle de capas. Popup on-click en seccion censal con stats. Clusters Airbnb clickables (zoom expansion). Leyenda dual.
- **/metodologia** — 5 fuentes con links, seccion "Por que dos escalas al mapa", 4 limitaciones, tabla de fechas de snapshot, licencia CC BY-SA 4.0.

## Lo que hay que hacer (Fase 3)

Segun `FASE-3-lanzamiento.md`, las tareas originales son:

1. Pagina `/illes` comparativa entre islas (4 cards: Mallorca, Menorca, Eivissa, Formentera con datos especificos de cada una)
2. Pagina `/dades` descarga de CSVs/parquet
3. Pagina `/premsa` kit de prensa
4. SEO basico (sitemap, robots.txt, meta description, OG image)
5. Open Graph cards (imagen de 1200x630 para previsualizaciones)
6. Outreach a prensa local
7. Deploy a Vercel con dominio definitivo
8. Configurar analytics (opcional)

**Decision pendiente con el usuario**: nombre del proyecto en Vercel (`casestancades.vercel.app`?) y dominio definitivo (`.cat`, `.org`, `.es`?).

## Headlines y stats a destacar en el home

(Ya implementados en `/` y `/mapa` en Fase 2)

- **18.175 listings activos** en Airbnb Mallorca+Menorca, con **105.738 plazas** (`accommodates`)
- **18.184 plazas legales** declaradas en HUT Eivissa — **40%** concentradas en Sant Josep (7.296) mientras Eivissa capital solo tiene **236** (41 registros)
- **95.4%** de los listings activos son `Entire home/apt` (pisos completos)
- **98.8%** tiene `license` rellenado en Airbnb — pero el Govern no valida ese campo
- **$258M** de ingresos estimados Airbnb L365d en Mallorca+Menorca
- INE CCAA: **16.2%** de viviendas vacias + **6.9%** de uso esporadico

**Insight narrativo central**:
> En Eivissa hay 41 registros HUT legales en la ciudad (50.000 hab.) y 945 en Sant Josep. Donde estan las 7.000+ plazas que oferta Airbnb en Eivissa? El gap entre el dato legal y el rascado ES la denuncia.

## Traps y gotchas (no perder tiempo)

1. **Bug pre-existente en `dataset_web.json`**: arreglado en `scripts/04_regenerate_web_json.py`. NO usar el output directo de `02_build_dataset.py` (multiplica valores de Eivissa/Formentera por n secciones).
2. **Typo persistente**: el XLSX del INE se llama `viviendas vacias-hiopotecas.xlsx` (con "h-i-o"). Si alguien lo "arregla", el script 01 falla.
3. **Dataset hybrid**: la columna `granularidad` indica si la feature es `seccion_censal` o `municipio`. NO mezclar al pintar — Eivissa/Formentera tienen un solo valor por municipio replicado a todas las secciones.
4. **Vivienda INE solo CCAA**: los `*_pct_ccaa` son constantes para TODAS las features. Documentar en /metodologia y en el popup del mapa.
5. **No scrappear**: nunca Idealista, nunca Airbnb directo. Solo datos abiertos.
6. **No build sin pedir**: el usuario es dev pero odia perder tiempo en builds innecesarios. Iterar con `pnpm dev` y solo build cuando pida.
7. **Conventional commits**: usar `feat(web):`, `fix(map):`, etc. NUNCA anadir "Co-Authored-By" ni atribucion a IA.
8. **Encoding**: los archivos raw ya estan normalizados a UTF-8.
9. **macOS case-insensitive**: la carpeta se creo como `VIvienda` pero el filesystem la resuelve como `Vivienda`. No es bug.
10. **Node 22 + pnpm 11 obligatorio** (NO Node 20). El HANDOFF original decia Node 20 pero Astro 7 requiere Node 22+. Decidido en sesion de Fase 2.
11. **TypeScript 5.x** (NO 7.x) por incompatibilidad con `@astrojs/check`.
12. **`prerender = false` en cada pagina** para que el i18n funcione. Sin esto, el cookie no se lee en dev/build.

## Preferencias del usuario (descubiertas en sesiones anteriores)

- Idioma del proyecto: **catalan principal** + castellano. El usuario escribe en espanol.
- Estilo: **documentacion modular** (`PLAN.md` + 1 .md por fase), iteracion paso a paso.
- Verificar claims antes de decir "si": el usuario detecta acuerdo facil y lo penaliza. Si no estas seguro, **di "dejame verificar"** y comprueba.
- Respetar la regla "no build": no compilar/ejecutar proyectos sin pedir.
- NO asumir respuestas: si hay duda, **preguntar con `question` tool**.
- **Honestidad radical sobre limitaciones**: si una fuente es CCAA, decirlo en /metodologia y en el popup del mapa.

## Datos cuantitativos de la conferencia OHIB (12-13 nov 2025)

Guardados en `docs/conferencia-OHIB-2025/` (15 JPGs + Info.pdf, ignorados en git). Datos clave para usar en el storytelling:

- Compraventa 2024 €/m²: Formentera 7.353 / Ibiza 4.331 / Mallorca 3.500 / Menorca 2.748 / Balears media 3.609
- CEE parque residencial Balears: 1,1% A, 2,2% B, 3,7% C, 9,5% D, 43,9% E, 12,5% F, 27,0% G → **83,4% en E/F/G**
- 34,79% unifamiliares vs 1,16% plurifamiliares
- Fuentes oficiales mapeadas: INE, Catastro, MIVAU, MTERD, DGHA, IBAVI, ATIB, IBESTAT, ICGIB

Frase literal del usuario que define el proyecto:
> "el problema no son los legales, son los que no son legales. En Ibiza, ninguna vivienda en plurifamiliar puede alquilarse y hay miles de anuncios."

## Preguntas abiertas (preguntar al usuario en la nueva sesion)

1. **¿Vercel ya configurado / nombre del proyecto?** Recomendacion: `casestancades.vercel.app` (libre presumiblemente). Login con GitHub, free tier.
2. **¿Dominio `.cat` o `.org` para lanzamiento?** El usuario dijo "de momento el dominio no es importante" pero para outreach a prensa conviene uno definitivo.
3. **¿Open Graph image estatica o dinamica?** Estatica: 1 imagen fija. Dinamica: HTML+canvas que genera una imagen con la headline y las cifras (mas viralizable).
4. **¿Outreach a prensa local ahora o despues del lanzamiento?** Recomiendo despues: tener URL definitiva + URL de /premsa + OG images listas.
5. **¿Analytics?** Posibilidad: Plausible (privacy-friendly, sin cookies) o ninguno. Para una web de denuncia, menos tracking = mejor.
6. **¿Nombre de la organizacion/portavoz?** Para la pagina /premsa y para la nota de contacto en /metodologia. Si no tiene, dejar como "iniciativa ciudadana" o "colectivo X".

## Estructura de archivos esperada al cerrar Fase 3

```
web/src/pages/
├── index.astro           # home
├── mapa.astro            # mapa interactivo
├── metodologia.astro     # fuentes y limitaciones
├── illes.astro           # comparativa por isla (NUEVO)
├── dades.astro           # descarga de datasets (NUEVO)
└── premsa.astro          # kit de prensa (NUEVO)

web/public/
├── og-image.png          # 1200x630 Open Graph (NUEVO)
├── press/                # kit de prensa descargable (NUEVO)
└── (resto igual)

web/src/content/          # opcional: blog/notas
```

## Convenciones de commits

```
feat(web): ...
fix(map): ...
chore(web): ...
docs(plan): ...
```

Tags al cerrar fase: `fase-3-completa`.

## Que NO hacer

- No scrappear Idealista o Airbnb.
- No usar Leaflet (usar MapLibre GL).
- No usar TileMill/MBTiles (usar tippecanoe → pmtiles).
- No meter viviendas vacias a nivel CCAA fingiendo que son seccion censal.
- No anadir "Co-Authored-By" ni atribucion a IA en commits.
- No commitear archivos raw grandes (ya en `.gitignore`).
- No asumir respuestas: si hay duda, **preguntar con `question` tool**.

## TL;DR

Fase 3 = 3 paginas nuevas (illes, dades, premsa) + SEO + OG + Vercel + outreach. La web MVP ya funciona en local. Las decisiones tecnicas estan todas tomadas en Fase 2. Solo queda ejecutar outreach, contenido editorial y deploy.
