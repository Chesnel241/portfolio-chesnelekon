/**
 * Images Open Graph générées au build, une par article et par projet.
 * Routes produites : /og/blog/<slug>.png et /og/projets/<slug>.png
 */
import type { APIRoute, GetStaticPaths } from 'astro';
import { getCollection } from 'astro:content';
import { renderOgImage } from '../../../lib/og-image';

export const getStaticPaths = (async () => {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const projects = await getCollection('projects');

  return [
    ...posts.map((post) => ({
      params: { collection: 'blog', slug: post.id },
      props: { eyebrow: 'Article', title: post.data.title },
    })),
    ...projects.map((project) => ({
      params: { collection: 'projets', slug: project.id },
      props: { eyebrow: 'Projet', title: project.data.title },
    })),
  ];
}) satisfies GetStaticPaths;

export const GET: APIRoute = async ({ props }) => {
  const { eyebrow, title } = props as { eyebrow: string; title: string };
  const png = await renderOgImage({ eyebrow, title });

  return new Response(new Uint8Array(png), {
    headers: {
      'Content-Type': 'image/png',
      'Cache-Control': 'public, max-age=31536000, immutable',
    },
  });
};
