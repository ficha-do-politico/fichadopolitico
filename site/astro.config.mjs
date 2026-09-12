import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: process.env.ASTRO_SITE || 'https://ficha-do-politico.github.io',
  base: process.env.ASTRO_BASE || '/',
  output: 'static',
  vite: {
    plugins: [tailwindcss()],
  },
});
