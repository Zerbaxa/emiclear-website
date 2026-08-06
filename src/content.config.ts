import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const education = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/education" }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    audience: z.enum(["clinicians", "public"]),
    topic: z.string(),
    materialType: z.string(),
    publishedAt: z.coerce.date(),
    reviewedAt: z.coerce.date(),
    nextReviewAt: z.coerce.date(),
    references: z.array(z.string()).default([]),
    draft: z.boolean().default(true),
  }),
});

const news = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content/news" }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    publishedAt: z.coerce.date(),
    draft: z.boolean().default(true),
  }),
});

export const collections = { education, news };

