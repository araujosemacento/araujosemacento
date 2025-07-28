// @ts-check
import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';

// https://astro.build/config
export default defineConfig({
  i18n: {
    locales: ['en', 'pt-BR'],
    defaultLocale: 'en',
    routing: {
      prefixDefaultLocale: false,
    },
  },
  vite: {
    ssr: {
      noExternal: ['webcoreui'],
    },
  },
  integrations: [svelte()],
});
