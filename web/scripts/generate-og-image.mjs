// Genera l'Open Graph image (1200x630 PNG) per a previsualitzacions en xarxes.
// Output: web/public/og-image.png
//
// Re-executar si canvien les xifres d'impacto o el missatge principal.
// Dependència: sharp (devDep de web/). El text s'incrusta al SVG i es
// rasteritza amb el motor de sharp. Si volem una font corporativa pròpia
// (Inter, etc.) caldrà incrustar el fitxer .ttf i passar-lo a sharp.
//
// Ús:
//   cd web && node scripts/generate-og-image.mjs
//   export PATH="/Users/ichi/.nvm/versions/node/v22.13.1/bin:$PATH"  # Node 22 + pnpm 11

import sharp from "sharp";
import { writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const outPath = resolve(__dirname, "../public/og-image.png");

// Paleta extreta de web/src/styles/global.css (@theme brand)
const COLOR_BRAND = "#c2410c";
const COLOR_BRAND_DARK = "#9a3412";
const COLOR_INK = "#1c1917";
const COLOR_PAPER = "#fafaf9";
const COLOR_LINE = "#e7e5e4";
const COLOR_MUTED = "#78716c";

const FONT = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif";

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <!-- Background -->
  <rect width="1200" height="630" fill="${COLOR_PAPER}"/>

  <!-- Top accent bar -->
  <rect width="1200" height="8" fill="${COLOR_BRAND}"/>

  <!-- Eyebrow -->
  <text x="60" y="78" font-family="${FONT}" font-size="20" font-weight="700"
        fill="${COLOR_BRAND_DARK}" letter-spacing="2">CASES TANCADES · ILLES BALEARS</text>

  <!-- Main title (2 lines) -->
  <text x="60" y="190" font-family="${FONT}" font-size="76" font-weight="800" fill="${COLOR_INK}">Quants pisos tancats</text>
  <text x="60" y="278" font-family="${FONT}" font-size="76" font-weight="800" fill="${COLOR_INK}">hi ha a les Balears?</text>

  <!-- Subtitle -->
  <text x="60" y="338" font-family="${FONT}" font-size="26" font-weight="400" fill="#44403c">Creuem dades oficials d'habitatge semi-buit amb lloguer turístic.</text>
  <text x="60" y="372" font-family="${FONT}" font-size="26" font-weight="400" fill="#44403c">La diferència entre el legal i el real és la denúncia.</text>

  <!-- Stat card 1: Airbnb -->
  <g transform="translate(60, 430)">
    <rect width="340" height="150" rx="10" fill="#ffffff" stroke="${COLOR_LINE}" stroke-width="2"/>
    <text x="22" y="58" font-family="${FONT}" font-size="46" font-weight="800" fill="${COLOR_BRAND}">18.175</text>
    <text x="22" y="98" font-family="${FONT}" font-size="20" font-weight="600" fill="${COLOR_INK}">Listings Airbnb actius</text>
    <text x="22" y="124" font-family="${FONT}" font-size="16" font-weight="400" fill="${COLOR_MUTED}">Mallorca + Menorca (geo-localitzats)</text>
  </g>

  <!-- Stat card 2: HUT -->
  <g transform="translate(430, 430)">
    <rect width="340" height="150" rx="10" fill="#ffffff" stroke="${COLOR_LINE}" stroke-width="2"/>
    <text x="22" y="58" font-family="${FONT}" font-size="46" font-weight="800" fill="${COLOR_BRAND}">18.184</text>
    <text x="22" y="98" font-family="${FONT}" font-size="20" font-weight="600" fill="${COLOR_INK}">Places HUT legals</text>
    <text x="22" y="124" font-family="${FONT}" font-size="16" font-weight="400" fill="${COLOR_MUTED}">Eivissa · 40% a Sant Josep</text>
  </g>

  <!-- Stat card 3: Vivenda buida -->
  <g transform="translate(800, 430)">
    <rect width="340" height="150" rx="10" fill="#ffffff" stroke="${COLOR_LINE}" stroke-width="2"/>
    <text x="22" y="58" font-family="${FONT}" font-size="46" font-weight="800" fill="${COLOR_BRAND}">16,2%</text>
    <text x="22" y="98" font-family="${FONT}" font-size="20" font-weight="600" fill="${COLOR_INK}">Habitatges buits</text>
    <text x="22" y="124" font-family="${FONT}" font-size="16" font-weight="400" fill="${COLOR_MUTED}">INE Balears (CCAA, 2024)</text>
  </g>

  <!-- Footer URL -->
  <text x="60" y="615" font-family="${FONT}" font-size="20" font-weight="600" fill="${COLOR_BRAND_DARK}">casestancades.vercel.app</text>
  <text x="1140" y="615" text-anchor="end" font-family="${FONT}" font-size="16" font-weight="400" fill="${COLOR_MUTED}">Dades públiques · CC BY-SA 4.0</text>
</svg>`;

const png = await sharp(Buffer.from(svg), { density: 150 })
  .png({ compressionLevel: 9 })
  .toBuffer();

await writeFile(outPath, png);
console.log(`OG image written: ${outPath} (${png.length} bytes, 1200x630)`);
