# Match State Analysis

## Objetivo

Analisar a frequencia de gols tardios por estado do placar nos cutoffs 60, 65, 70 e 75 minutos.

Esta analise nao cria modelo, nao executa baseline, nao faz backtesting, nao altera banco, schema, importer, crawler, dataset ou dados brutos.

## Fonte

Dataset usado:

- `data/processed/datasets/late_goal_dataset_v1b_ingame.csv`

Grain:

- 1 linha por `match_id + cutoff_minute`.
- Cutoffs usados nesta analise: 60, 65, 70 e 75.
- Linhas analisadas: 1520.
- Partidas unicas: 380.

Campos principais:

- `home_goals_until_cutoff`
- `away_goals_until_cutoff`
- `score_diff_home_until_cutoff`
- `total_goals_until_cutoff`
- `target_goal_after_cutoff`

## Regras Anti-Leakage

- Estado do placar calculado somente com gols ate o cutoff.
- Total de gols calculado somente com gols ate o cutoff.
- Target usa apenas gols apos o cutoff correspondente.
- Placar final nao foi usado como feature.
- Eventos apos cutoff nao foram usados para segmentacao.
- Nenhuma estatistica full-match foi usada.

## Metodologia

Para cada cutoff e segmento foi calculado:

- N de partidas;
- positivos (`target_goal_after_cutoff = 1`);
- negativos;
- taxa de gol apos cutoff;
- diferenca em pontos percentuais contra a media do cutoff;
- odds ratio do segmento contra o restante do mesmo cutoff;
- intervalo de confianca aproximado de 95% do odds ratio;
- p-value por Fisher exact test 2x2, segmento versus restante.

Criterio de classificacao usado:

- **PROMISSOR**: N >= 30, diferenca positiva >= 5 p.p., p-value < 0.10 e OR > 1.25.
- **OBSERVAR**: N >= 20 e efeito absoluto >= 5 p.p. ou p-value < 0.15.
- **DESCARTAR**: efeito fraco, amostra muito pequena ou ausencia de evidencia nesta amostra.

## Media por Cutoff

| Cutoff | N | Positivos | Negativos | Taxa media |
|---:|---:|---:|---:|---:|
| 60 | 380 | 265 | 115 | 69.7% |
| 65 | 380 | 247 | 133 | 65.0% |
| 70 | 380 | 222 | 158 | 58.4% |
| 75 | 380 | 189 | 191 | 49.7% |

## Segmentacao 1 - Estado do Placar

| Cutoff | Segmento | N | Positivos | Taxa | Dif. vs media | OR | IC 95% OR | p-value | Classe |
|---:|---|---:|---:|---:|---:|---:|---|---:|---|
| 60 | empate | 105 | 72 | 68.6% | -1.2 p.p. | 0.93 | 0.57-1.51 | 0.8031 | DESCARTAR |
| 60 | mandante vencendo por 1 | 110 | 78 | 70.9% | +1.2 p.p. | 1.08 | 0.67-1.76 | 0.8061 | DESCARTAR |
| 60 | visitante vencendo por 1 | 73 | 55 | 75.3% | +5.6 p.p. | 1.41 | 0.79-2.53 | 0.2609 | OBSERVAR |
| 60 | mandante vencendo por 2+ | 51 | 36 | 70.6% | +0.9 p.p. | 1.05 | 0.55-2.00 | 1.0000 | DESCARTAR |
| 60 | visitante vencendo por 2+ | 41 | 24 | 58.5% | -11.2 p.p. | 0.57 | 0.30-1.12 | 0.1072 | OBSERVAR |
| 65 | empate | 102 | 66 | 64.7% | -0.3 p.p. | 0.98 | 0.61-1.58 | 1.0000 | DESCARTAR |
| 65 | mandante vencendo por 1 | 100 | 65 | 65.0% | +0.0 p.p. | 1.00 | 0.62-1.61 | 1.0000 | DESCARTAR |
| 65 | visitante vencendo por 1 | 72 | 49 | 68.1% | +3.1 p.p. | 1.18 | 0.68-2.05 | 0.5853 | DESCARTAR |
| 65 | mandante vencendo por 2+ | 59 | 40 | 67.8% | +2.8 p.p. | 1.16 | 0.64-2.10 | 0.6590 | DESCARTAR |
| 65 | visitante vencendo por 2+ | 47 | 27 | 57.4% | -7.6 p.p. | 0.69 | 0.37-1.29 | 0.2562 | OBSERVAR |
| 70 | empate | 103 | 58 | 56.3% | -2.1 p.p. | 0.89 | 0.56-1.40 | 0.6404 | DESCARTAR |
| 70 | mandante vencendo por 1 | 93 | 55 | 59.1% | +0.7 p.p. | 1.04 | 0.65-1.67 | 0.9041 | DESCARTAR |
| 70 | visitante vencendo por 1 | 74 | 47 | 63.5% | +5.1 p.p. | 1.30 | 0.77-2.20 | 0.3588 | OBSERVAR |
| 70 | mandante vencendo por 2+ | 62 | 39 | 62.9% | +4.5 p.p. | 1.25 | 0.71-2.19 | 0.4827 | DESCARTAR |
| 70 | visitante vencendo por 2+ | 48 | 23 | 47.9% | -10.5 p.p. | 0.61 | 0.33-1.13 | 0.1200 | OBSERVAR |
| 75 | empate | 96 | 44 | 45.8% | -3.9 p.p. | 0.81 | 0.51-1.29 | 0.4095 | DESCARTAR |
| 75 | mandante vencendo por 1 | 92 | 47 | 51.1% | +1.4 p.p. | 1.07 | 0.67-1.72 | 0.8111 | DESCARTAR |
| 75 | visitante vencendo por 1 | 74 | 41 | 55.4% | +5.7 p.p. | 1.33 | 0.80-2.21 | 0.3015 | OBSERVAR |
| 75 | mandante vencendo por 2+ | 66 | 36 | 54.5% | +4.8 p.p. | 1.26 | 0.74-2.15 | 0.4185 | DESCARTAR |
| 75 | visitante vencendo por 2+ | 52 | 21 | 40.4% | -9.4 p.p. | 0.65 | 0.36-1.17 | 0.1791 | OBSERVAR |

## Segmentacao 2 - Total de Gols Ja Marcados

| Cutoff | Segmento | N | Positivos | Taxa | Dif. vs media | OR | IC 95% OR | p-value | Classe |
|---:|---|---:|---:|---:|---:|---:|---|---:|---|
| 60 | 0 gols | 55 | 39 | 70.9% | +1.2 p.p. | 1.07 | 0.57-2.00 | 0.8755 | DESCARTAR |
| 60 | 1 gol | 127 | 90 | 70.9% | +1.1 p.p. | 1.08 | 0.68-1.73 | 0.8130 | DESCARTAR |
| 60 | 2 gols | 90 | 61 | 67.8% | -2.0 p.p. | 0.89 | 0.53-1.48 | 0.6939 | DESCARTAR |
| 60 | 3 gols | 69 | 52 | 75.4% | +5.6 p.p. | 1.41 | 0.77-2.56 | 0.3112 | OBSERVAR |
| 60 | 4+ gols | 39 | 23 | 59.0% | -10.8 p.p. | 0.59 | 0.30-1.16 | 0.1414 | OBSERVAR |
| 65 | 0 gols | 47 | 31 | 66.0% | +1.0 p.p. | 1.05 | 0.55-2.00 | 1.0000 | DESCARTAR |
| 65 | 1 gol | 115 | 74 | 64.3% | -0.7 p.p. | 0.96 | 0.61-1.52 | 0.9069 | DESCARTAR |
| 65 | 2 gols | 100 | 66 | 66.0% | +1.0 p.p. | 1.06 | 0.66-1.72 | 0.9029 | DESCARTAR |
| 65 | 3 gols | 68 | 46 | 67.6% | +2.6 p.p. | 1.15 | 0.66-2.02 | 0.6750 | DESCARTAR |
| 65 | 4+ gols | 50 | 30 | 60.0% | -5.0 p.p. | 0.78 | 0.42-1.44 | 0.4303 | OBSERVAR |
| 70 | 0 gols | 39 | 23 | 59.0% | +0.6 p.p. | 1.03 | 0.52-2.01 | 1.0000 | DESCARTAR |
| 70 | 1 gol | 106 | 64 | 60.4% | +2.0 p.p. | 1.12 | 0.71-1.77 | 0.6445 | DESCARTAR |
| 70 | 2 gols | 103 | 59 | 57.3% | -1.1 p.p. | 0.94 | 0.59-1.48 | 0.8154 | DESCARTAR |
| 70 | 3 gols | 72 | 46 | 63.9% | +5.5 p.p. | 1.33 | 0.78-2.26 | 0.3528 | OBSERVAR |
| 70 | 4+ gols | 60 | 30 | 50.0% | -8.4 p.p. | 0.67 | 0.38-1.16 | 0.1561 | OBSERVAR |
| 75 | 0 gols | 33 | 17 | 51.5% | +1.8 p.p. | 1.08 | 0.53-2.21 | 0.8573 | DESCARTAR |
| 75 | 1 gol | 93 | 48 | 51.6% | +1.9 p.p. | 1.10 | 0.69-1.76 | 0.7210 | DESCARTAR |
| 75 | 2 gols | 102 | 46 | 45.1% | -4.6 p.p. | 0.78 | 0.49-1.22 | 0.2984 | DESCARTAR |
| 75 | 3 gols | 85 | 49 | 57.6% | +7.9 p.p. | 1.51 | 0.93-2.45 | 0.1100 | OBSERVAR |
| 75 | 4+ gols | 67 | 29 | 43.3% | -6.5 p.p. | 0.73 | 0.43-1.24 | 0.2820 | OBSERVAR |

## Ranking dos Maiores Efeitos Positivos

| Cutoff | Segmento | N | Taxa | Dif. vs media | OR | p-value | Classe |
|---:|---|---:|---:|---:|---:|---:|---|
| 75 | 3 gols | 85 | 57.6% | +7.9 p.p. | 1.51 | 0.1100 | OBSERVAR |
| 75 | visitante vencendo por 1 | 74 | 55.4% | +5.7 p.p. | 1.33 | 0.3015 | OBSERVAR |
| 60 | 3 gols | 69 | 75.4% | +5.6 p.p. | 1.41 | 0.3112 | OBSERVAR |
| 60 | visitante vencendo por 1 | 73 | 75.3% | +5.6 p.p. | 1.41 | 0.2609 | OBSERVAR |
| 70 | 3 gols | 72 | 63.9% | +5.5 p.p. | 1.33 | 0.3528 | OBSERVAR |
| 70 | visitante vencendo por 1 | 74 | 63.5% | +5.1 p.p. | 1.30 | 0.3588 | OBSERVAR |
| 75 | mandante vencendo por 2+ | 66 | 54.5% | +4.8 p.p. | 1.26 | 0.4185 | DESCARTAR |
| 70 | mandante vencendo por 2+ | 62 | 62.9% | +4.5 p.p. | 1.25 | 0.4827 | DESCARTAR |
| 65 | visitante vencendo por 1 | 72 | 68.1% | +3.1 p.p. | 1.18 | 0.5853 | DESCARTAR |
| 65 | mandante vencendo por 2+ | 59 | 67.8% | +2.8 p.p. | 1.16 | 0.6590 | DESCARTAR |

## Segmentos Promissores

- Nenhum segmento atingiu criterio PROMISSOR nesta amostra.

## Segmentos em Observacao

- **visitante vencendo por 1 @ 60**: N=73, taxa=75.3%, diff=+5.6 p.p., OR=1.41, p=0.2609.
- **visitante vencendo por 2+ @ 60**: N=41, taxa=58.5%, diff=-11.2 p.p., OR=0.57, p=0.1072.
- **visitante vencendo por 2+ @ 65**: N=47, taxa=57.4%, diff=-7.6 p.p., OR=0.69, p=0.2562.
- **visitante vencendo por 1 @ 70**: N=74, taxa=63.5%, diff=+5.1 p.p., OR=1.30, p=0.3588.
- **visitante vencendo por 2+ @ 70**: N=48, taxa=47.9%, diff=-10.5 p.p., OR=0.61, p=0.1200.
- **visitante vencendo por 1 @ 75**: N=74, taxa=55.4%, diff=+5.7 p.p., OR=1.33, p=0.3015.
- **visitante vencendo por 2+ @ 75**: N=52, taxa=40.4%, diff=-9.4 p.p., OR=0.65, p=0.1791.
- **3 gols @ 60**: N=69, taxa=75.4%, diff=+5.6 p.p., OR=1.41, p=0.3112.
- **4+ gols @ 60**: N=39, taxa=59.0%, diff=-10.8 p.p., OR=0.59, p=0.1414.
- **4+ gols @ 65**: N=50, taxa=60.0%, diff=-5.0 p.p., OR=0.78, p=0.4303.
- **3 gols @ 70**: N=72, taxa=63.9%, diff=+5.5 p.p., OR=1.33, p=0.3528.
- **4+ gols @ 70**: N=60, taxa=50.0%, diff=-8.4 p.p., OR=0.67, p=0.1561.
- **3 gols @ 75**: N=85, taxa=57.6%, diff=+7.9 p.p., OR=1.51, p=0.1100.
- **4+ gols @ 75**: N=67, taxa=43.3%, diff=-6.5 p.p., OR=0.73, p=0.2820.

## Leitura Quantitativa

### Estado do placar

O estado **empate** nao apresentou sinal positivo nesta amostra. Em todos os cutoffs avaliados a taxa ficou abaixo ou praticamente igual a media do cutoff, portanto o empate isolado deve ser descartado como segmento forte nesta formulacao.

O melhor sinal positivo por estado do placar apareceu em **visitante vencendo por 1**, com diferenca positiva em 60, 70 e 75. Ainda assim, os p-values ficaram fracos e o padrao nao atingiu criterio PROMISSOR.

Estados com visitante vencendo por 2+ tiveram diferenca negativa relevante em varios cutoffs. Esse sinal pode ser interpretado como possivel segmento de menor probabilidade de novo gol tardio, mas nao como oportunidade positiva.

### Total de gols ja marcados

O melhor sinal positivo por total de gols apareceu em **3 gols ja marcados**, especialmente no cutoff 75, com taxa de 57,6%, diferenca de +7,9 p.p. e OR 1,51. O sinal tambem aparece em 60 e 70, mas sem significancia estatistica forte.

Segmentos com 0, 1 ou 2 gols nao apresentaram aumento consistente da taxa de gol apos cutoff. O segmento 4+ gols teve diferenca negativa em todos os cutoffs analisados, sugerindo possivel saturacao do placar ou menor janela de gols adicionais, mas sem criterio forte para conclusao operacional.

## Conclusao Quant

A analise confirma que match state possui algum valor exploratorio, mas **nenhum segmento atingiu criterio PROMISSOR** nesta rodada.

Principais sinais para observacao futura:

1. **3 gols ja marcados**, principalmente nos cutoffs 60, 70 e 75.
2. **Visitante vencendo por 1**, principalmente nos cutoffs 60, 70 e 75.
3. **Visitante vencendo por 2+** e **4+ gols** como possiveis sinais negativos/protetivos, nao como sinais de maior probabilidade.

Recomendacao:

- Manter match state como familia candidata apenas para interacoes, nao como sinal isolado aprovado.
- Testar interacoes entre `3 gols ja marcados`, `visitante vencendo por 1`, H8 momentum/shotmap e segmentos de perfil de equipe.
- Nao iniciar modelo ou backtesting apenas com esta analise.
- Descartar `empate` como sinal isolado forte nesta amostra.

## Status Final

MATCH STATE ANALYSIS concluida.

Status: **APTO PARA REVISAO QUANT**.
