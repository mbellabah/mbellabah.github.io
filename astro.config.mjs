// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.bellabah.com',

  integrations: [
    mdx({
      remarkPlugins: [remarkMath, remarkGfm],
      rehypePlugins: [[rehypeKatex, { strict: false, throwOnError: false }]]
    })
  ],

  markdown: {
    remarkPlugins: [remarkMath, remarkGfm],
    rehypePlugins: [[rehypeKatex, { strict: false, throwOnError: false }]]
  },

  vite: {
    plugins: [tailwindcss()]
  }
});