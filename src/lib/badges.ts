interface IconConfig {
  slug: string;
  color: string;
}

const KNOWN: Record<string, IconConfig> = {
  'Linux': { slug: 'linux', color: 'fcc624' },
  'Python': { slug: 'python', color: '3776ab' },
  'C/C++': { slug: 'cplusplus', color: '00599c' },
  'Metasploit': { slug: 'metasploit', color: '1f77b4' },
  'Nmap': { slug: 'nmap', color: '1f77b4' },
  'Burp Suite': { slug: 'burpsuite', color: 'ff6600' },
  'Node.js': { slug: 'nodedotjs', color: '339933' },
  'Docker Compose': { slug: 'docker', color: '2496ed' },
  'Dockerode': { slug: 'docker', color: '2496ed' },
  'Traefik': { slug: 'traefik', color: '24a1de' },
  'Supabase': { slug: 'supabase', color: '3ecf8e' },
  'Next.js': { slug: 'nextdotjs', color: 'ffffff' },
  'Astro': { slug: 'astro', color: 'ff5d01' },
  'TypeScript': { slug: 'typescript', color: '3178c6' },
};

export function techIconUrl(tech: string): string | undefined {
  const cfg = KNOWN[tech];
  return cfg ? `https://cdn.simpleicons.org/${cfg.slug}/${cfg.color}` : undefined;
}
