// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  output: 'static',
  site: 'https://Theneillsaaco.github.io',
  base: '/calculadoraconsumo',
  
  build: {
    assets: '_assets'
  },
  
  vite: {
    plugins: [tailwindcss()]
  }
});