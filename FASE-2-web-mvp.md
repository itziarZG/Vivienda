# FASE 2 - Web MVP (semanas 3-4)

## Objetivo

Web minima viable desplegada en URL temporal con 3 paginas funcionales: home con headline + `/mapa` interactivo + `/metodologia`. La web consume `dataset.parquet` y `tiles.pmtiles` generados en Fase 1. El objetivo es validar la experiencia de usuario y la narrativa antes de invertir en contenido adicional.

## Tareas

### Inicializacion del proyecto web
- [ ] `pnpm create astro@latest web/` con template "basics" (TypeScript: strict)
- [ ] Integrar Tailwind CSS (configuracion por defecto)
- [ ] Integrar MapLibre GL JS como dependencia
- [ ] Configurar estructura de paginas: `src/pages/index.astro`, `mapa.astro`, `metodologia.astro`
- [ ] Configurar layout comun en `src/layouts/Base.astro` (header + footer + meta tags)

### Datos
- [ ] Copiar `tiles.pmtiles` a `web/public/tiles/`
- [ ] Crear `web/public/data/dataset.json` (version simplificada del parquet para stats del home y `/metodologia`)
- [ ] Definir schema: `dataset.json` con stats agregadas por isla (4 entradas) y headline stats globales

### Pagina `/` (home)
- [ ] Hero section con headline + cifra impacto (ej: "El X% de las viviendas de Balears estan semi-vacias")
- [ ] Cifra destacada 2: nº total de listings de Airbnb en Balears
- [ ] Mini-mapa estatico (PNG exportado) con CTA "Ver mapa interactivo"
- [ ] Explicacion breve (3 parrafos) de que es el proyecto
- [ ] CTA a `/mapa`

### Pagina `/mapa` (interactivo)
- [ ] MapLibre GL inicializado ocupando 100% del viewport
- [ ] Capa choropleth: seccion censal coloreada por `pct_uso_esporadico`
- [ ] Capa puntos: listings de Airbnb (clustered a bajo zoom)
- [ ] Toggle UI para cambiar entre capas / activar/desactivar
- [ ] Popup on-click de seccion censal con stats
- [ ] Sidebar con leyenda y stats principales
- [ ] Filtro por isla (dropdown: Mallorca, Menorca, Eivissa, Formentera)

### Pagina `/metodologia`
- [ ] Explicacion de fuentes (INE, Inside Airbnb) con links
- [ ] Limitaciones: sesgo de Airbnb como cota inferior, granularidad seccion censal
- [ ] Formula de "vivienda semi-vacia" explicada
- [ ] Fecha de los datos (snapshot)
- [ ] Licencia del proyecto (CC BY-SA 4.0 recomendado)
- [ ] Contacto

### Despliegue
- [ ] Crear cuenta en Vercel (free tier)
- [ ] `vercel link` y configurar como static site
- [ ] Primer deploy: URL `casestancades.vercel.app` (o el nombre que se elija)
- [ ] Verificar que el mapa carga tiles correctamente
- [ ] Compartir URL con 2-3 personas de confianza para feedback inicial

### Cierre
- [ ] Commit final con tag `fase-2-completa`
- [ ] Actualizar PLAN.md
- [ ] Anotar feedback recibido en este documento

## Comandos clave

```bash
# Crear proyecto
cd /Users/ichi/Desktop/DEV/VIvienda
pnpm create astro@latest web -- --template basics --typescript strict --yes
cd web
pnpm install
pnpm add maplibre-gl pmtiles tailwindcss

# Dev local
pnpm dev  # http://localhost:4321

# Build
pnpm build

# Deploy
pnpm dlx vercel
```

## Snippet: inicializar MapLibre con PMTiles

```typescript
// web/src/components/Mapa.astro
<script>
  import maplibregl from 'maplibre-gl';
  import { Protocol } from 'pmtiles';
  import 'maplibre-gl/dist/maplibre-gl.css';

  const protocol = new Protocol();
  maplibregl.addProtocol('pmtiles', protocol.tile);

  const map = new maplibregl.Map({
    container: 'map',
    style: {
      version: 8,
      sources: {
        cases: {
          type: 'vector',
          url: 'pmtiles:///tiles/dataset.pmtiles',
          attribution: 'INE + Inside Airbnb',
        },
      },
      layers: [
        { id: 'background', type: 'background', paint: { 'background-color': '#f5f5f4' } },
        {
          id: 'secciones-fill',
          type: 'fill',
          source: 'cases',
          'source-layer': 'cases',
          paint: {
            'fill-color': [
              'interpolate', ['linear'], ['get', 'pct_uso_esporadico'],
              0, '#fef3c7', 10, '#fbbf24', 25, '#ea580c', 50, '#991b1b',
            ],
            'fill-opacity': 0.65,
          },
        },
        {
          id: 'secciones-line',
          type: 'line',
          source: 'cases',
          'source-layer': 'cases',
          paint: { 'line-color': '#78716c', 'line-width': 0.3 },
        },
      ],
    },
    center: [2.85, 39.6],
    zoom: 8,
  });
</script>

<div id="map" class="w-full h-screen"></div>
```

## Criterio de "fase terminada"

- [x] Web desplegada en URL temporal de Vercel
- [x] 3 paginas funcionales: home, /mapa, /metodologia
- [x] Mapa interactivo carga tiles y permite explorar Balears
- [x] Sin errores en consola del navegador
- [x] Mobile responsive (mapa con dedos funciona)
- [x] Feedback de al menos 1 persona ajena al proyecto
- [x] Commit final con tag `fase-2-completa`

## Decisiones tomadas durante la fase

_Llenar durante la ejecucion._

## Problemas encontrados

_Llenar durante la ejecucion._

## Proximos pasos

Fase 3: lanzamiento publico. Ver `FASE-3-lanzamiento.md`.
