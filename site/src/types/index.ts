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

export interface PatrimonioComparativo {
  ano: number;
  total_declarado: number;
  total_formatado: string;
}

export interface PatrimonioCongresso {
  total_declarado: number;
  total_formatado: string;
  ano: number;
  tse_url: string;
  bens: BemItem[];
  comparativo_anterior?: PatrimonioComparativo;
}

export interface Candidatura2026 {
  cargo: string;
  reeleicao: boolean;
  numero_urna: string;
  partido: string;
  uf: string;
  situacao_registro: string;
  url_divulgacand: string;
  patrimonio?: PatrimonioCongresso;
}

export interface DespesaCategoria {
  categoria: string;
  valor: number;
  valor_formatado: string;
  percentual: number;
}

export interface DespesaItem {
  data: string;
  fornecedor: string;
  cnpj_cpf: string;
  categoria: string;
  valor: number;
  valor_formatado: string;
  url_documento?: string | null;
}

export interface DespesasCEAP {
  ano: number;
  total_gasto: number;
  total_formatado: string;
  total_documentos: number;
  categorias: DespesaCategoria[];
  maiores_despesas: DespesaItem[];
  fonte_oficial: string;
}

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
  candidatura_2026?: Candidatura2026 | null;
  despesas_2026?: DespesasCEAP | null;
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
  candidatura_2026?: Candidatura2026 | null;
  despesas_2026?: DespesasCEAP | null;
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
  is_candidato_2026?: boolean;
  is_reeleicao?: boolean;
  cargo_2026?: string;
}

export interface TemaSenadoInfo {
  votacao_id: number;
  sessao_id: number;
  codigo_materia: number;
  proposicao: string;
  data: string;
  resultado_oficial: string;
  url_votacao: string;
  url_proposicao: string;
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
  senado?: TemaSenadoInfo;
}

export interface OrientacaoBancada {
  bancada: string;
  orientacao: string;
}

export interface VotacaoCamaraDetalhe {
  votacao_id: string;
  dataHora?: string;
  descricao?: string;
  siglaOrgao?: string;
  total_votos_registrados: number;
  total_deputados_locais: number;
  total_ausentes: number;
  distribuicao_votos: Record<string, number>;
  orientacoes: OrientacaoBancada[];
}

export interface VotacaoSenadoDetalhe {
  senado_votacao_id?: number;
  senado_sessao_id?: number;
  codigo_materia?: number;
  data?: string;
  descricao?: string;
  resultado_oficial?: string;
  url_votacao?: string;
  url_proposicao?: string;
  total_votos_registrados: number;
  total_senadores: number;
  total_ausentes: number;
  distribuicao_votos: Record<string, number>;
}

export interface VotacaoDetalhe {
  id: string;
  camara: VotacaoCamaraDetalhe;
  senado?: VotacaoSenadoDetalhe;
}

export interface VotoParlamentarItem {
  id: number;
  nome_eleitoral: string;
  nome_civil: string;
  partido: string;
  uf: string;
  url_foto: string;
  casa: CasaLegislativa;
  cargo: string;
  voto: string;
  href: string;
}

export interface BemItem {
  tipo: string;
  descricao: string;
  valor: number;
}

export interface HistoricoPatrimonial {
  ano: number;
  cargoDisputado: string;
  totalDeclarado: number;
  totalFormatado: string;
  tseUrl: string;
  bens: BemItem[];
}

export interface CandidatoPresidencia {
  id: string;
  nomeUrna: string;
  nomeCivil: string;
  partido: string;
  partidoNome: string;
  numeroUrna: string;
  cargo: string;
  fotoUrl: string;
  fotoFonteOficial?: string;
  tsePerfilUrl: string;
  situacaoCandidatura: string;
  vice?: {
    nomeUrna: string;
    partido: string;
  };
  historicoPatrimonial: HistoricoPatrimonial[];
}


