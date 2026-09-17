// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://portfolio-chesnelekon.vercel.app',
  integrations: [
    sitemap({
      // La page 404 n'a pas vocation à être indexée.
      filter: (page) => !page.includes('/404'),
    }),
  ],
});
