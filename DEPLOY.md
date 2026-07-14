# Deploy a Vercel

## Opción A — Dashboard (recomendada para primer deploy)

1. Ve a https://vercel.com/new
2. Conecta el repo `itziarZG/Vivienda` desde GitHub
3. En "Project Name" escribe `casestancades`
4. En "Root Directory" selecciona `web`
5. Vercel detecta Astro automáticamente y usa Node 22 (definido en `web/vercel.json`)
6. Click "Deploy"
7. La URL será `https://casestancades.vercel.app`

## Opción B — CLI

```bash
cd web
npx vercel login              # abre navegador para autorizar
npx vercel link               # vincula el proyecto
npx vercel --prod             # deploy a producción
```

## Variables de entorno

No requiere ninguna variable. Todo es estático.

## Dominio propio

Más adelante (post-MVP): comprar `.cat`/`.org`/`.es` y configurarlo en
Vercel → Settings → Domains.
