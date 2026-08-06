import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://excist.dothome.co.kr",
  integrations: [mdx(), sitemap()],
  output: "static",
  trailingSlash: "always",
});

