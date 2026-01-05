import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = await getCollection('posts', ({ data }) => {
    return data.draft !== true;
  });

  return rss({
    title: 'Mohamadou Bella Bah',
    description: 'Essays and notes on mathematics, philosophy, and poetry.',
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.date,
      description: post.body.substring(0, 300) + '...', // Simple truncation for description
      link: `/posts/${post.slug}/`,
    })),
    customData: `<language>en-us</language>`,
  });
}
