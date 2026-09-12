import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: process.env.ASTRO_SITE || 'https://ficha-do-politico.github.io',
  base: process.env.ASTRO_BASE || '/',
  integrations: [tailwind()],
  output: 'static',
});
