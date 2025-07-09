// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import remarkMath from 'remark-math';
import remarkGfm from 'remark-gfm';
import rehypeKatex from 'rehype-katex';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.bellabah.com',
  integrations: [
    mdx({
      remarkPlugins: [remarkMath, remarkGfm],
      rehypePlugins: [[rehypeKatex, { strict: false, throwOnError: false }]]
    }),
    tailwind()
  ],
  markdown: {
    remarkPlugins: [remarkMath, remarkGfm],
    rehypePlugins: [[rehypeKatex, { strict: false, throwOnError: false }]]
  }
});