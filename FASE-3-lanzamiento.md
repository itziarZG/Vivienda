# FASE 3 - Lanzamiento (semanas 5-6)

## Objetivo

Web publica completa con todas las paginas, contenido pulido, SEO basico, kit de prensa descargable y outreach a medios locales. Al cerrar esta fase, la web esta lista para ser compartida en redes y enviada a prensa.

## Tareas

### Paginas adicionales
- [ ] `/illes` - comparativa entre las 4 islas (Mallorca, Menorca, Eivissa, Formentera) con graficos de barras/lines
  - Variables: % semi-vacias, densidad Airbnb, €/m² (dato conferencia OHIB)
  - Mini-mapa por isla con su zoom automatico
- [ ] `/dades` - descarga de datos abiertos
  - Link a `dataset.parquet` (raw)
  - Link a `dataset.csv` (version simplificada)
  - Scripts Python de pipeline con instrucciones
  - Licencia CC BY-SA 4.0
- [ ] `/premsa` - kit de prensa
  - Cifras citables (1-2 frases, sin jerga)
  - Graficos PNG exportables en alta resolucion
  - Fotos libres de derecho (mapa) con atribucion
  - Bio del proyecto
  - Contacto (email)
- [ ] `/qui-som` - transparencia
  - Quien esta detras, motivacion, declaracion de conflicto de interes (ninguno)
  - Como contribuir (issues, PRs, donaciones)

### Pulido tecnico
- [ ] SEO: meta description, OG tags, sitemap.xml, robots.txt
- [ ] Open Graph cards con imagen del mapa (1200x630) para compartir en redes
- [ ] Accesibilidad basica: contraste, alt text, navegacion por teclado
- [ ] Performance: lazy load de MapLibre, optimizar tamano de bundle
- [ ] Diseno final: revisar paleta de colores, tipografia, espaciado

### Contenido
- [ ] Redactar textos en catalan como idioma principal
- [ ] Version en castellano (no automatico, traducir y adaptar)
- [ ] Disclaimer legal en pie de pagina
- [ ] Pagina de errores (404) con branding

### Outreach
- [ ] Lista de medios locales: Diario de Ibiza, Ara Balears, La Marea, ElDiario.es Balears
- [ ] Lista de colectivos: PAH Ibiza, GOB, Observatori de l'Habitatge
- [ ] Email tipo para prensa (curado, no spam)
- [ ] Enviar email 1-2 semanas antes del lanzamiento publico

### Dominio definitivo
- [ ] Decidir nombre final del proyecto
- [ ] Comprar dominio (`.cat`, `.es` o `.org`)
- [ ] Configurar en Vercel como dominio principal
- [ ] HTTPS automatico

### Cierre
- [ ] Commit final con tag `fase-3-completa`
- [ ] Actualizar PLAN.md
- [ ] Hacer backup del repo y de los datos
- [ ] Documentar todo el proyecto en README.md

## Comandos clave

```bash
# Deploy con dominio propio
vercel domains add casestancades.cat

# Generar sitemap (Astro plugin)
pnpm add @astrojs/sitemap

# Lighthouse
pnpm dlx lighthouse https://casestancades.cat --view

# Test mobile
# Abrir Chrome DevTools -> Device toolbar -> iPhone 14 Pro
```

## Snippet: meta tags Open Graph

```astro
---
// web/src/layouts/Base.astro
const { title, description } = Astro.props;
---
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} | Cases Tancades</title>
  <meta name="description" content={description} />
  <meta property="og:title" content={title} />
  <meta property="og:description" content={description} />
  <meta property="og:image" content="/og-card.png" />
  <meta property="og:type" content="website" />
  <meta name="twitter:card" content="summary_large_image" />
</head>
```

## Criterio de "fase terminada"

- [x] Las 7 paginas del plan implementadas (`/`, `/mapa`, `/metodologia`, `/illes`, `/dades`, `/premsa`, `/qui-som`)
- [x] Dominio definitivo configurado y HTTPS funcionando
- [x] Lighthouse score > 90 en Performance y Accessibility
- [x] Open Graph card valida (https://www.opengraph.xyz/)
- [x] Sitemap.xml generado
- [x] Email de prensa enviado a al menos 3 medios
- [x] Licencia y disclaimer visibles
- [x] README.md del proyecto con instrucciones para reproducir
- [x] Commit final con tag `lanzamiento-mvp` (o `v0.1.0`)

## Decisiones tomadas durante la fase

_Llenar durante la ejecucion._

## Problemas encontrados

_Llenar durante la ejecucion._

## Proximos pasos (post-MVP)

- Refresh trimestral del dataset (cron o manual)
- Captar feedback de usuarios y prensa
- Iterar visualizaciones segun datos que mas resuenen
- Explorar v2 con datos del registro HUT del Govern (mas completo que Inside Airbnb)
- Explorar alianza con OHIB, universidad o colectivo
- Captar financiacion (subvenciones periodismo de datos) si crece el proyecto
