import { defineCollection, z } from 'astro:content';

const postsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.date(),
    tags: z.array(z.string()).optional(),
    draft: z.boolean().optional(),
  }),
});

const booksCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    author: z.string(),
    genre: z.string(),
    dateCompleted: z.union([z.date(), z.string()]),
    rating: z.number().min(1).max(5).optional(),
  }),
});

export const collections = {
  posts: postsCollection,
  books: booksCollection,
};