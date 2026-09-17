/**
 * Génération des images Open Graph (1200x630) au moment du build.
 *
 * 100 % local : satori transforme un arbre d'éléments en SVG (les glyphes sont
 * convertis en tracés à partir des fichiers de police lus sur le disque), puis
 * resvg rastérise ce SVG en PNG. Aucun appel réseau, ni au build ni à
 * l'exécution.
 */
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';

const require = createRequire(import.meta.url);

/** Les polices sont lues en .woff : satori ne sait pas décoder le woff2. */
function loadFont(specifier: string): Buffer {
  return readFileSync(require.resolve(specifier));
}

const interRegular = loadFont('@fontsource/inter/files/inter-latin-400-normal.woff');
const interSemiBold = loadFont('@fontsource/inter/files/inter-latin-600-normal.woff');
const interBold = loadFont('@fontsource/inter/files/inter-latin-700-normal.woff');
const monoMedium = loadFont(
  '@fontsource/jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff'
);

const WIDTH = 1200;
const HEIGHT = 630;

const COLORS = {
  bg: '#000000',
  panel: '#0b0b0d',
  border: 'rgba(255, 255, 255, 0.12)',
  ink: '#f5f5f7',
  inkSoft: '#a1a1a6',
  accent: '#2997ff',
};

const SIGNATURE = 'Chesnel Ekogha - Ingénieur Cybersécurité Automobile';

type Node = {
  type: string;
  props: Record<string, unknown> & { children?: unknown };
};

const el = (
  type: string,
  style: Record<string, unknown>,
  children?: unknown
): Node => ({ type, props: { style, children } });

/** Réduit la taille du titre pour les titres longs, afin qu'il tienne toujours. */
function titleFontSize(title: string): number {
  if (title.length > 110) return 44;
  if (title.length > 80) return 52;
  if (title.length > 55) return 60;
  return 70;
}

export interface OgImageOptions {
  /** Libellé affiché au-dessus du titre, ex. « Article » ou « Projet ». */
  eyebrow: string;
  /** Titre de la page. */
  title: string;
}

export async function renderOgImage({ eyebrow, title }: OgImageOptions): Promise<Buffer> {
  const markup = el(
    'div',
    {
      width: '100%',
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      padding: '72px 80px',
      backgroundColor: COLORS.bg,
      backgroundImage: `radial-gradient(1000px 520px at 88% -12%, rgba(41, 151, 255, 0.22) 0%, rgba(0, 0, 0, 0) 60%), linear-gradient(160deg, ${COLORS.panel} 0%, ${COLORS.bg} 55%)`,
      color: COLORS.ink,
      fontFamily: 'Inter',
    },
    [
      // En-tête : pastille de section + domaine du site
      el(
        'div',
        {
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          width: '100%',
        },
        [
          el(
            'div',
            { display: 'flex', alignItems: 'center' },
            [
              el('div', {
                width: 14,
                height: 14,
                borderRadius: 999,
                backgroundColor: COLORS.accent,
                marginRight: 16,
              }),
              el(
                'div',
                {
                  fontFamily: 'JetBrains Mono',
                  fontSize: 26,
                  fontWeight: 500,
                  letterSpacing: 6,
                  textTransform: 'uppercase',
                  color: COLORS.accent,
                },
                eyebrow
              ),
            ]
          ),
          el(
            'div',
            {
              fontFamily: 'JetBrains Mono',
              fontSize: 20,
              fontWeight: 500,
              color: COLORS.inkSoft,
            },
            'portfolio-chesnelekon.vercel.app'
          ),
        ]
      ),
      // Titre
      el(
        'div',
        {
          display: 'flex',
          fontSize: titleFontSize(title),
          fontWeight: 700,
          lineHeight: 1.16,
          letterSpacing: -1.5,
          maxWidth: 1000,
        },
        title
      ),
      // Pied de page : signature
      el(
        'div',
        {
          display: 'flex',
          flexDirection: 'column',
        },
        [
          el('div', {
            width: 120,
            height: 4,
            borderRadius: 999,
            backgroundColor: COLORS.accent,
            marginBottom: 28,
          }),
          el(
            'div',
            { display: 'flex', fontSize: 30, fontWeight: 600, color: COLORS.ink },
            SIGNATURE
          ),
        ]
      ),
    ]
  );

  const svg = await satori(markup as never, {
    width: WIDTH,
    height: HEIGHT,
    fonts: [
      { name: 'Inter', data: interRegular, weight: 400, style: 'normal' },
      { name: 'Inter', data: interSemiBold, weight: 600, style: 'normal' },
      { name: 'Inter', data: interBold, weight: 700, style: 'normal' },
      { name: 'JetBrains Mono', data: monoMedium, weight: 500, style: 'normal' },
    ],
  });

  const png = new Resvg(svg, {
    fitTo: { mode: 'width', value: WIDTH },
    font: { loadSystemFonts: false },
  })
    .render()
    .asPng();

  return Buffer.from(png);
}
