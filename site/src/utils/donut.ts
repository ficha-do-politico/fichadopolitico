/**
 * Utilitário geométrico para cálculo de arcos SVG e visualização do Hemiciclo Parlamentar (Semi-Donut).
 * 
 * Apartidarismo estrito (AD-004): ordenação canônica neutra (maiores bancadas primeiro).
 * Sem bibliotecas externas pesadas; renderização estática e ultraleve em SVG puro.
 */

import type { BancadaItem } from '../types';

export interface DonutDimensions {
  cx: number;
  cy: number;
  outerRadius: number;
  innerRadius: number;
}

export interface DonutSlice extends BancadaItem {
  color: string;
  startAngle: number;
  endAngle: number;
  path: string;
  centerAngle: number;
  labelX: number;
  labelY: number;
}

export interface MajorityMarker {
  label: string;
  cadeiras: number;
  angle: number;
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  labelX: number;
  labelY: number;
}

/**
 * Cores neutras e distintivas para cada legenda partidária com assento no Congresso.
 * Mapeadas com base na identidade visual pública das legendas e contraste otimizado.
 */
export const PARTIDO_CORES: Record<string, string> = {
  PL: '#1e3a8a',          // Azul Marinho
  PT: '#dc2626',          // Vermelho
  UNIÃO: '#0d9488',       // Verde Azulado / Teal
  PSD: '#d97706',         // Âmbar / Laranja Queimado
  PP: '#0284c7',          // Azul Celeste
  REPUBLICANOS: '#4338ca',// Índigo / Azul Real
  MDB: '#15803d',         // Verde MDB
  PODE: '#059669',        // Esmeralda
  PSDB: '#2563eb',        // Azul Cobalto
  PSB: '#e11d48',         // Rosa Escuro / Framboesa
  PSOL: '#9333ea',        // Roxo
  PCdoB: '#991b1b',       // Carmesim Escuro
  PDT: '#b45309',         // Bronze / Âmbar Escuro
  PV: '#16a34a',          // Verde Claro
  AVANTE: '#0891b2',      // Ciano
  NOVO: '#ea580c',        // Laranja Vivo
  SOLIDARIEDADE: '#f59e0b',// Amarelo Ouro
  PRD: '#64748b',         // Ardósia Médio
  REDE: '#10b981',        // Verde Menta
  CIDADANIA: '#db2777',   // Rosa Choque
  DC: '#475569',          // Ardósia Escuro
  MISSÃO: '#6b7280',      // Cinza Neutro
  'S/Partido': '#94a3b8', // Cinza Claro
};

const PALETA_FALLBACK = [
  '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
  '#ec4899', '#06b6d4', '#84cc16', '#14b8a6', '#6366f1',
];

export function getPartidoColor(sigla: string): string {
  if (PARTIDO_CORES[sigla]) {
    return PARTIDO_CORES[sigla];
  }
  // Fallback determinístico baseado no hash da sigla
  let hash = 0;
  for (let i = 0; i < sigla.length; i++) {
    hash = sigla.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash) % PALETA_FALLBACK.length;
  return PALETA_FALLBACK[index];
}

/**
 * Calcula o path SVG de um arco de anel (donut slice) entre startAngle e endAngle.
 * Ângulos em radianos: Math.PI (180° = esquerda horizontal) a 0 (0° = direita horizontal).
 */
export function describeArc(
  cx: number,
  cy: number,
  outerRadius: number,
  innerRadius: number,
  startAngle: number,
  endAngle: number
): string {
  const x1 = (cx + outerRadius * Math.cos(startAngle)).toFixed(2);
  const y1 = (cy - outerRadius * Math.sin(startAngle)).toFixed(2);
  const x2 = (cx + outerRadius * Math.cos(endAngle)).toFixed(2);
  const y2 = (cy - outerRadius * Math.sin(endAngle)).toFixed(2);

  const x3 = (cx + innerRadius * Math.cos(endAngle)).toFixed(2);
  const y3 = (cy - innerRadius * Math.sin(endAngle)).toFixed(2);
  const x4 = (cx + innerRadius * Math.cos(startAngle)).toFixed(2);
  const y4 = (cy - innerRadius * Math.sin(startAngle)).toFixed(2);

  const angleSpan = Math.abs(startAngle - endAngle);
  const largeArcFlag = angleSpan > Math.PI ? 1 : 0;

  return `M ${x1} ${y1} A ${outerRadius} ${outerRadius} 0 ${largeArcFlag} 1 ${x2} ${y2} L ${x3} ${y3} A ${innerRadius} ${innerRadius} 0 ${largeArcFlag} 0 ${x4} ${y4} Z`;
}

/**
 * Computa as fatias do semi-donut a partir da lista de bancadas.
 */
export function computeSemiDonutSlices(
  bancadas: BancadaItem[],
  totalCadeiras: number,
  dimensions: DonutDimensions
): DonutSlice[] {
  const { cx, cy, outerRadius, innerRadius } = dimensions;
  let currentAngle = Math.PI; // Inicia em 180° (esquerda)

  return bancadas.map(b => {
    const fraction = b.cadeiras / totalCadeiras;
    const sliceAngle = fraction * Math.PI;
    const startAngle = currentAngle;
    const endAngle = currentAngle - sliceAngle;
    currentAngle = endAngle;

    const path = describeArc(cx, cy, outerRadius, innerRadius, startAngle, endAngle);
    const centerAngle = (startAngle + endAngle) / 2;
    const midRadius = (outerRadius + innerRadius) / 2;
    const labelX = Number((cx + midRadius * Math.cos(centerAngle)).toFixed(2));
    const labelY = Number((cy - midRadius * Math.sin(centerAngle)).toFixed(2));

    return {
      ...b,
      color: getPartidoColor(b.sigla),
      startAngle,
      endAngle,
      path,
      centerAngle,
      labelX,
      labelY,
    };
  });
}

/**
 * Calcula marcadores de maioria (simples e qualificada) no semi-donut.
 */
export function computeMajorityMarkers(
  totalCadeiras: number,
  maioriaSimples: number,
  maioriaQualificada: number,
  dimensions: DonutDimensions
): MajorityMarker[] {
  const { cx, cy, outerRadius, innerRadius } = dimensions;
  const markers: MajorityMarker[] = [];

  const configs = [
    { label: '50% (Maioria simples)', cadeiras: maioriaSimples },
    { label: '3/5 (Maioria qualificada)', cadeiras: maioriaQualificada },
  ];

  for (const cfg of configs) {
    const fraction = cfg.cadeiras / totalCadeiras;
    const angle = Math.PI * (1 - fraction);

    const x1 = Number((cx + (innerRadius - 4) * Math.cos(angle)).toFixed(2));
    const y1 = Number((cy - (innerRadius - 4) * Math.sin(angle)).toFixed(2));
    const x2 = Number((cx + (outerRadius + 8) * Math.cos(angle)).toFixed(2));
    const y2 = Number((cy - (outerRadius + 8) * Math.sin(angle)).toFixed(2));

    const labelRadius = outerRadius + 18;
    const labelX = Number((cx + labelRadius * Math.cos(angle)).toFixed(2));
    const labelY = Number((cy - labelRadius * Math.sin(angle)).toFixed(2));

    markers.push({
      label: cfg.label,
      cadeiras: cfg.cadeiras,
      angle,
      x1,
      y1,
      x2,
      y2,
      labelX,
      labelY,
    });
  }

  return markers;
}
