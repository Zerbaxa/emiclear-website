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
    /** 이 자료의 언어. 영문 병행판은 "en". */
    lang: z.enum(["ko", "en"]).default("ko"),
    /** 같은 자료의 다른 언어판 id 목록. 예: ["burn-public.en"] */
    translations: z.array(z.string()).default([]),
    /** 전문가용 PDF 경로. 있으면 자료 페이지에 다운로드 링크가 붙는다. */
    pdf: z.string().optional(),
    /** PDF 판 표기. 예: "2026년 8월판" */
    pdfEdition: z.string().optional(),
    draft: z.boolean().default(true),
  }),
});

export const collections = { education };

