import rss from "@astrojs/rss";
import { getCollection } from "astro:content";

export async function GET(context: { site: URL }) {
  const posts = await getCollection("news", ({ data }) => !data.draft);
  posts.sort((a, b) => b.data.publishedAt.valueOf() - a.data.publishedAt.valueOf());

  return rss({
    title: "EM-I-CLEAR 활동소식",
    description: "응급의학혁신교육연구회의 활동과 공개자료 업데이트",
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.summary,
      pubDate: post.data.publishedAt,
      link: `/news/${post.id}/`,
    })),
  });
}

