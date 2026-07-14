// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

// Vite plugin inline: añade Content-Type correcto para .pmtiles y .geojson
// en dev server. Sin esto, Astro/Vite sirve .pmtiles con Content-Type vacío
// y la librería pmtiles del cliente falla al parsear el header del archivo.
function assetMimePlugin() {
  return {
    name: 'cases-tancades-asset-mime',
    configureServer(/** @type {any} */ server) {
      // @ts-expect-error tipos de Vite no exportados
      server.middlewares.use((_req, res, next) => {
        const url = _req.url ?? '';
        if (url.endsWith('.pmtiles')) {
          res.setHeader('Content-Type', 'application/octet-stream');
        } else if (url.endsWith('.geojson')) {
          res.setHeader('Content-Type', 'application/geo+json');
        } else if (url.endsWith('.json') && url.includes('/data/')) {
          res.setHeader('Content-Type', 'application/json; charset=utf-8');
        }
        next();
      });
    },
  };
}

// https://astro.build/config
export default defineConfig({
  site: 'https://casestancades.vercel.app',
  integrations: [sitemap()],
  vite: {
    plugins: [assetMimePlugin(), tailwindcss()],
  },
});
