/**
 * Contratos centrais de tipos para o portal Ficha do Político.
 * Alinhado às decisões AD-005, AD-006, AD-009 e AD-014.
 */

export type VotoTipo =
  | 'Sim'
  | 'Não'
  | 'Abstenção'
  | 'Obstrução'
  | 'Artigo 17'
  | 'Não votou / Ausente'
  | string;

export interface Deputado {
  id: number;
  nome_eleitoral: string;
  nome_civil: string;
  partido: string;
  uf: string;
  situacao: string;
  url_foto: string;
  url_perfil_camara: string;
  votos: Record<string, string>;
}

export interface Senador {
  id: number;
  nome_eleitoral: string;
  nome_civil: string;
  partido: string;
  uf: string;
  situacao: string;
  url_foto: string;
  url_perfil_senado: string;
  votos: Record<string, string>;
}

export type CasaLegislativa = 'camara' | 'senado';

export interface ParlamentarCardData {
  id: number;
  nome_eleitoral: string;
  nome_civil: string;
  partido: string;
  uf: string;
  url_foto: string;
  casa: CasaLegislativa;
  cargo: string;
  href: string;
}

export interface Tema {
  id: string;
  ordem: number;
  titulo: string;
  subtitulo: string;
  tipo: string;
  numero: number;
  ano: number;
  proposicao: string;
  proposicao_id: number;
  data: string;
  resultado_oficial: string;
  url_votacao: string;
  url_proposicao: string;
  criterio_resumo: string;
}
