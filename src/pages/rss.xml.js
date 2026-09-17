import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const posts = (await getCollection('blog', ({ data }) => !data.draft)).sort(
    (a, b) => b.data.date.valueOf() - a.data.date.valueOf()
  );

  return rss({
    title: 'Chesnel Ekogha - Cybersécurité Automobile',
    description:
      "Articles et analyses de Chesnel Ekogha, ingénieur en cybersécurité automobile et systèmes embarqués : ISO/SAE 21434, TARA, ECU, bus CAN.",
    site: context.site,
    customData: '<language>fr-FR</language>',
    items: posts.map((post) => ({
      title: post.data.title,
      description: post.data.excerpt,
      pubDate: post.data.date,
      link: new URL(`/blog/${post.id}/`, context.site).href,
      categories: post.data.tags,
      author: 'Chesnel Ekogha',
    })),
  });
}
