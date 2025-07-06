// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.bellabah.com',
  markdown: {
    remarkPlugins: [
      'remark-math',
      'remark-gfm'
    ],
    rehypePlugins: [
      ['rehype-katex', { 
        strict: false,
        throwOnError: false
      }]
    ]
  },
  vite: {
    plugins: [tailwindcss()]
  }
});