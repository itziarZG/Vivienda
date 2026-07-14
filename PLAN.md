# Plan: Cases Buides / Tancades (Vivienda vacía + alquiler temporal en Balears)

## 1. Resumen ejecutivo

Web publica que cruza dos datos oficiales - INE (consumo electrico por seccion censal, como proxy de vivienda semi-vacia) + Inside Airbnb (listings georreferenciados) - para visibilizar la presion turistica sobre el parque residencial de Balears. Audiencia principal: ciudadania general ibicenca. Plazo objetivo: MVP publico en 4-6 semanas. Stack: Python (pipeline de datos) + Astro (web estatica) + MapLibre GL (mapas interactivos) + Vercel (hosting).

## 2. Decisiones cerradas

| Decision | Valor | Razon |
|---|---|---|
| Formato entregable | Web publica | Compartible, viralizable, accesible para prensa y ciudadania |
| Audiencia | Ciudadania general ibicenca | Lenguaje accesible, storytelling visual, foco local |
| Granularidad datos | Seccion censal (500-2.000 hogares) | INE solo llega a este nivel, defendible y honesto |
| Plazo total | 4-6 semanas (MVP) | Validar rapido, iterar despues |
| Datos vivienda vacia | Consumo electrico INE (ya disponible) | Unico dato publico oficial con cobertura islenya completa |
| Datos alquiler temporal | Inside Airbnb (datos abiertos) | Legal, reproducible, suficiente para cota inferior |
| Alcance geografico | Balears entero (4 islas) | Comparativa potente entre islas, reutiliza trabajo |
| Recursos | Solo, perfil tecnico dev | Plan realista sin dependencias externas |
| Estilo iteracion | Waterfall secuencial (4 fases) | Mantener foco, evitar scope creep |
| Documentacion | PLAN.md + 1 doc por fase | Modular, facil de iterar, auditable |

## 3. Fases (resumen)

- **Fase 0 (sem 1) - Setup.** Repo git, entorno Python/Node, descarga de shapefile de secciones censales Balears (INE) e Inside Airbnb listings para las 4 islas, mover XLSXs del usuario a `data/raw/`.
- **Fase 1 (sem 2) - Datos.** Pipeline Python: limpiar XLSX INE -> cargar shapefile -> cargar listings -> spatial join listings->seccion censal -> agregar dataset -> generar `dataset.parquet` y `tiles.pmtiles`.
- **Fase 2 (sem 3-4) - Web MVP.** Astro + MapLibre GL: home con headline + `/mapa` interactivo (capa semi-vacias + capa Airbnb) + `/metodologia`. Despliegue en Vercel con URL temporal.
- **Fase 3 (sem 5-6) - Lanzamiento.** `/illes` comparativa entre islas + `/dades` descarga de CSVs/parquet + `/premsa` kit de prensa + SEO basico + Open Graph cards + outreach a prensa local.

## 4. Riesgos

| Riesgo | Mitigacion |
|---|---|
| Inside Airbnb no se actualiza con frecuencia | Snapshot con fecha visible en `/metodologia`; documentar fuente alternativa (registro HUT del Govern) para v2 |
| Sesgo: no todos los listings estan en Airbnb | Comunicar en metodologia: es **cota inferior** de la presion turistica real |
| Granularidad seccion censal (no direccion exacta) | Reenmarcar narrativamente: "mapa por barrio de 500-2.000 hogares" en vez de portal exacto. Honesto y defendible. |
| Scraping / TOS de portales | NO scrappear Idealista/Airbnb directamente; usar solo datos abiertos (Inside Airbnb + INE/Catastro) |
| Dominio `.cat` ocupado o caro | Plan B: `.es`, `.org`, subdominio Vercel (`casestancades.vercel.app`) |
| Demanda legal por denuncia publica | Disclaimer "datos publicos, metodologia abierta, sin acusacion individual" en pie de pagina |
| Shapefile secciones censales no incluye Formentera como tal | Validar en Fase 0; si falta, trabajar con secciones censales de los 4 municipios de Eivissa + Formentera juntos |

## 5. Estado actual

- [x] Carpeta `/Users/ichi/Desktop/DEV/VIvienda/` identificada con datos del usuario
- [x] XLSXs INE descargados por el usuario (`viviendas vacias-hipotecas.xlsx`, `39365(1).xlsx`)
- [x] Capturas de conferencia OHIB (12-13 nov 2025) revisadas
- [x] Plan inicial creado y validado con el usuario
- [x] `PLAN.md` escrito
- [x] `FASE-0-setup.md` escrito (pendiente ejecucion)
- [x] Fase 0 ejecutada (estructura, entornos, shapefile, listings Mallorca+Menorca)
- [x] Limitacion detectada: Eivissa y Formentera no tienen datos en Inside Airbnb
- [ ] Fase 1 ejecutada
- [ ] Fase 2 ejecutada
- [ ] Fase 3 ejecutada
- [ ] Web publica desplegada en dominio definitivo

## 6. Notas de iteracion

_Espacio para cambios futuros. Cada vez que se ajuste el plan, dejar nota con fecha y razon._

- **2026-07-13** - Plan inicial creado tras revision de datos del usuario y conferencia OHIB. Decisiones cerradas: web publica, ciudadania ibicenca, seccion censal, 4-6 semanas, Inside Airbnb, Balears entero, dev solo, waterfall, documentacion modular.
