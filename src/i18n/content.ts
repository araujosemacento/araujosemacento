import enContent from './pages/en.json';
import ptBRContent from './pages/pt-BR.json';

export type Conteudo = {
  titulo?: string;
  descricao?: string;
  [key: string]: unknown;
};

export const contentMap: Record<string, Conteudo> = {
  en: enContent,
  'pt-BR': ptBRContent,
};

export function getContent(locale: string): Conteudo {
  return contentMap[locale] || contentMap['en'];
}
