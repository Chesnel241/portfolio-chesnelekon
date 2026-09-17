/**
 * Utilitaires partagés du blog : temps de lecture et gestion des tags.
 * Aucune dépendance externe : tout est calculé à la compilation.
 */

/**
 * Vitesse de lecture retenue. 200 mots/minute est une valeur prudente,
 * adaptée à du contenu technique en français (schémas, extraits de code,
 * références normatives qui ralentissent la lecture).
 */
const WORDS_PER_MINUTE = 200;

/**
 * Compte les mots « lisibles » d'un corps markdown.
 *
 * Le contenu des blocs de code est conservé (sur ces articles il fait partie
 * de ce qu'on lit réellement), mais tout ce qui n'est jamais lu est retiré :
 * délimiteurs de code, URL d'images et de liens, balises HTML.
 */
export function countWords(markdown: string): number {
  const text = markdown
    // Front matter éventuel en tête de fichier
    .replace(/^---\r?\n[\s\S]*?\r?\n---/, ' ')
    // Délimiteurs des blocs de code (et leur identifiant de langage)
    .replace(/^\s*```[^\n]*$/gm, ' ')
    // Accents graves du code en ligne
    .replace(/`/g, ' ')
    // Images : ni l'alt ni l'URL ne sont « lus »
    .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ')
    // Liens : on garde le libellé, on jette l'URL
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    // Balises HTML éventuelles
    .replace(/<[^>]*>/g, ' ');

  const words = text.match(/[\p{L}\p{N}]+(?:['’\-][\p{L}\p{N}]+)*/gu);
  return words ? words.length : 0;
}

/** Temps de lecture estimé, en minutes (minimum 1). */
export function readingTimeMinutes(markdown: string): number {
  return Math.max(1, Math.round(countWords(markdown) / WORDS_PER_MINUTE));
}

/** Libellé français prêt à afficher, par ex. « 8 min de lecture ». */
export function readingTimeLabel(minutes: number): string {
  return `${minutes} min de lecture`;
}

/**
 * URL de la page d'un tag. Les tags sont libres côté contenu : ils peuvent
 * contenir des espaces, des accents ou des caractères réservés, d'où
 * l'encodage systématique du segment d'URL.
 */
export function tagHref(tag: string): string {
  return `/tags/${encodeURIComponent(tag)}`;
}

/** Un tag et le nombre d'articles publiés qui le portent. */
export interface TagCount {
  tag: string;
  count: number;
}

/**
 * Agrège les tags d'une liste d'articles, triés par nombre d'articles
 * décroissant puis par ordre alphabétique français.
 */
export function collectTags(posts: { data: { tags: string[] } }[]): TagCount[] {
  const counts = new Map<string, number>();
  for (const post of posts) {
    for (const tag of post.data.tags) {
      counts.set(tag, (counts.get(tag) ?? 0) + 1);
    }
  }
  return [...counts.entries()]
    .map(([tag, count]) => ({ tag, count }))
    .sort((a, b) => b.count - a.count || a.tag.localeCompare(b.tag, 'fr'));
}

/** Accord singulier/pluriel pour un décompte d'articles. */
export function articleCountLabel(count: number): string {
  return `${count} article${count > 1 ? 's' : ''}`;
}
