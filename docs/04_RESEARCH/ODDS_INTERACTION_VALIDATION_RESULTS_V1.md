# ODDS INTERACTION VALIDATION RESULTS V1

## Resumo Executivo

- Validacao controlada executada conforme `docs/04_RESEARCH/ODDS_INTERACTION_PLAN_V1.md`.
- Foco principal: cutoff 60 com target `goal_after_60`.
- Targets secundarios avaliados apenas para robustez de sinais `MANTER` ou `OBSERVAR` no cutoff 60.
- Amostra principal @60: 380 partidas.
- Baseline `goal_after_60`: 69.7%.
- Classificacao @60: MANTER=0, OBSERVAR=1, DESCARTAR=11.
- Melhor efeito observado @60: `match_balance_high + shots_last_10m_high` com N=30, taxa=76.7%, diff=+6.9 p.p., OR=1.47, p-value=0.5347 e classificacao `OBSERVAR`.
- Nenhuma interacao atingiu criterio `MANTER` no cutoff 60.
- Interacoes `OBSERVAR` seguiram para robustez em 65/70/75: `match_balance_high + shots_last_10m_high`.

## Metodologia

- Fontes: Dataset Odds V1, Dataset H8 V1 e Dataset V1B In-Game.
- Odds usadas: `favorite_strength`, `match_balance`, `favorite_side` e `implied_prob_over25_norm` apenas como auxiliar contextual.
- H8 usado: `shots_last_10m` e `momentum_trend_last_10m`, sempre calculados ate o cutoff.
- Match State usado: `score_state_group`, `score_diff_home_until_cutoff` e `total_goals_until_cutoff`, sempre calculados ate o cutoff.
- Teste estatistico: Fisher exact test bicaudal contra o complemento do grupo.
- Odds ratio e IC 95% calculados por tabela 2x2; quando houve zero em alguma celula, foi usada correcao de Haldane-Anscombe para o IC.
- Classificacao: MANTER, OBSERVAR ou DESCARTAR conforme criterios do plano.

## Cortes Aplicados

- `favorite_strength_high`: top 25%, limiar >= 0.4934.
- `favorite_strength_low`: bottom 25%, limiar <= 0.1346.
- `match_balance_high`: top 25%, limiar >= 0.8304.
- `match_balance_low`: bottom 25%, limiar <= 0.5066.
- `shots_last_10m_high`: top 25% por cutoff.
  - cutoff 60: limiar >= 4.00.
  - cutoff 65: limiar >= 4.00.
  - cutoff 70: limiar >= 4.00.
  - cutoff 75: limiar >= 4.00.
- `momentum_trend_last_10m_positive`: `momentum_trend_last_10m > 0`.

## Baseline Por Cutoff

| Cutoff | Target | N | Positivos | Taxa |
| --- | --- | --- | --- | --- |
| 60 | goal_after_60 | 380 | 265 | 69.7% |
| 65 | goal_after_65 | 380 | 247 | 65.0% |
| 70 | goal_after_70 | 380 | 222 | 58.4% |
| 75 | goal_after_75 | 380 | 189 | 49.7% |

## Resultados Cutoff 60

| Grupo | Interacao | Cutoff | Target | N | Pos | Neg | Taxa | Baseline | Diff p.p. | OR | IC 95% | p-value | Comp. isolados | Class. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A - favorite_strength + H8 | favorite_strength_high + shots_last_10m_high | 60 | goal_after_60 | 34 | 23 | 11 | 67.6% | 69.7% | -2.1 | 0.90 | 0.42-1.91 | 0.8452 | favorite_strength_high=69.5%; shots_last_10m_high=72.1% | DESCARTAR |
| A - favorite_strength + H8 | favorite_strength_high + momentum_trend_last_10m_positive | 60 | goal_after_60 | 44 | 30 | 14 | 68.2% | 69.7% | -1.6 | 0.92 | 0.47-1.81 | 0.8618 | favorite_strength_high=69.5%; momentum_trend_last_10m_positive=67.0% | DESCARTAR |
| A - favorite_strength + H8 | favorite_strength_low + shots_last_10m_high | 60 | goal_after_60 | 33 | 24 | 9 | 72.7% | 69.7% | +3.0 | 1.17 | 0.53-2.61 | 0.8434 | favorite_strength_low=67.4%; shots_last_10m_high=72.1% | DESCARTAR |
| B - match_balance + H8 | match_balance_high + shots_last_10m_high | 60 | goal_after_60 | 30 | 23 | 7 | 76.7% | 69.7% | +6.9 | 1.47 | 0.61-3.52 | 0.5347 | match_balance_high=70.5%; shots_last_10m_high=72.1% | OBSERVAR |
| B - match_balance + H8 | match_balance_high + momentum_trend_last_10m_positive | 60 | goal_after_60 | 44 | 27 | 17 | 61.4% | 69.7% | -8.4 | 0.65 | 0.34-1.25 | 0.2226 | match_balance_high=70.5%; momentum_trend_last_10m_positive=67.0% | DESCARTAR |
| B - match_balance + H8 | match_balance_low + shots_last_10m_high | 60 | goal_after_60 | 34 | 23 | 11 | 67.6% | 69.7% | -2.1 | 0.90 | 0.42-1.91 | 0.8452 | match_balance_low=69.5%; shots_last_10m_high=72.1% | DESCARTAR |
| C - favorite_strength + Match State | favorite_strength_high + empate_aos_cutoff | 60 | goal_after_60 | 19 | 12 | 7 | 63.2% | 69.7% | -6.6 | 0.73 | 0.28-1.91 | 0.6089 | favorite_strength_high=69.5%; draw_at_cutoff=68.6% | DESCARTAR |
| C - favorite_strength + Match State | favorite_strength_high + favorito_perdendo_aos_cutoff | 60 | goal_after_60 | 13 | 10 | 3 | 76.9% | 69.7% | +7.2 | 1.46 | 0.40-5.42 | 0.7619 | favorite_strength_high=69.5%; favorite_losing_at_cutoff=76.7% | DESCARTAR |
| C - favorite_strength + Match State | favorite_strength_high + favorito_vencendo_por_1_aos_cutoff | 60 | goal_after_60 | 35 | 25 | 10 | 71.4% | 69.7% | +1.7 | 1.09 | 0.51-2.36 | 1.0000 | favorite_strength_high=69.5%; favorite_winning_by_1_at_cutoff=70.6% | DESCARTAR |
| D - match_balance + Match State | match_balance_high + empate_aos_cutoff | 60 | goal_after_60 | 28 | 20 | 8 | 71.4% | 69.7% | +1.7 | 1.09 | 0.47-2.56 | 1.0000 | match_balance_high=70.5%; draw_at_cutoff=68.6% | DESCARTAR |
| D - match_balance + Match State | match_balance_high + total_goals_until_cutoff_eq_2_or_3 | 60 | goal_after_60 | 42 | 29 | 13 | 69.0% | 69.7% | -0.7 | 0.96 | 0.48-1.93 | 1.0000 | match_balance_high=70.5%; total_goals_2_or_3_at_cutoff=71.1% | DESCARTAR |
| D - match_balance + Match State | match_balance_low + empate_aos_cutoff | 60 | goal_after_60 | 19 | 12 | 7 | 63.2% | 69.7% | -6.6 | 0.73 | 0.28-1.91 | 0.6089 | match_balance_low=69.5%; draw_at_cutoff=68.6% | DESCARTAR |

## Ranking @60

| Rank | Interacao | Classificacao | N | Taxa | Diff p.p. | OR | p-value | Superior aos componentes? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | match_balance_high + shots_last_10m_high | OBSERVAR | 30 | 76.7% | +6.9 | 1.47 | 0.5347 | True |
| 2 | favorite_strength_high + favorito_perdendo_aos_cutoff | DESCARTAR | 13 | 76.9% | +7.2 | 1.46 | 0.7619 | True |
| 3 | favorite_strength_low + shots_last_10m_high | DESCARTAR | 33 | 72.7% | +3.0 | 1.17 | 0.8434 | True |
| 4 | favorite_strength_high + favorito_vencendo_por_1_aos_cutoff | DESCARTAR | 35 | 71.4% | +1.7 | 1.09 | 1.0000 | True |
| 5 | match_balance_high + empate_aos_cutoff | DESCARTAR | 28 | 71.4% | +1.7 | 1.09 | 1.0000 | True |
| 6 | match_balance_high + total_goals_until_cutoff_eq_2_or_3 | DESCARTAR | 42 | 69.0% | -0.7 | 0.96 | 1.0000 | False |
| 7 | favorite_strength_high + momentum_trend_last_10m_positive | DESCARTAR | 44 | 68.2% | -1.6 | 0.92 | 0.8618 | False |
| 8 | favorite_strength_high + shots_last_10m_high | DESCARTAR | 34 | 67.6% | -2.1 | 0.90 | 0.8452 | False |
| 9 | match_balance_low + shots_last_10m_high | DESCARTAR | 34 | 67.6% | -2.1 | 0.90 | 0.8452 | False |
| 10 | favorite_strength_high + empate_aos_cutoff | DESCARTAR | 19 | 63.2% | -6.6 | 0.73 | 0.6089 | False |
| 11 | match_balance_low + empate_aos_cutoff | DESCARTAR | 19 | 63.2% | -6.6 | 0.73 | 0.6089 | False |
| 12 | match_balance_high + momentum_trend_last_10m_positive | DESCARTAR | 44 | 61.4% | -8.4 | 0.65 | 0.2226 | False |

## Robustez 65/70/75

| Grupo | Interacao | Cutoff | Target | N | Pos | Neg | Taxa | Baseline | Diff p.p. | OR | IC 95% | p-value | Comp. isolados | Class. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B - match_balance + H8 | match_balance_high + shots_last_10m_high | 65 | goal_after_65 | 31 | 20 | 11 | 64.5% | 65.0% | -0.5 | 0.98 | 0.45-2.11 | 1.0000 | match_balance_high=64.2%; shots_last_10m_high=65.4% | DESCARTAR |
| B - match_balance + H8 | match_balance_high + shots_last_10m_high | 70 | goal_after_70 | 28 | 14 | 14 | 50.0% | 58.4% | -8.4 | 0.69 | 0.32-1.50 | 0.4262 | match_balance_high=57.9%; shots_last_10m_high=59.8% | DESCARTAR |
| B - match_balance + H8 | match_balance_high + shots_last_10m_high | 75 | goal_after_75 | 26 | 15 | 11 | 57.7% | 49.7% | +8.0 | 1.41 | 0.63-3.16 | 0.4238 | match_balance_high=53.7%; shots_last_10m_high=50.5% | OBSERVAR |

## Comparacao Com Componentes Isolados

- A coluna `Comp. isolados` nas tabelas reporta a taxa do componente odds isolado e do componente H8/Match State isolado.
- Uma interacao so atende integralmente o criterio `MANTER` quando supera ambos os componentes isolados, alem de N, efeito, OR e p-value.
- Nos resultados @60, os sinais fortes foram avaliados contra seus componentes equivalentes para reduzir risco de atribuir ao par uma informacao que ja estava em um componente isolado.

## Respostas As Perguntas Do Plano

1. Existe interacao superior aos componentes isolados? Sim em pelo menos uma combinacao @60.
2. Existe interacao superior ao H8 isolado? Sim nas combinacoes Odds + H8 @60.
3. Existe interacao superior ao Match State isolado? Sim nas combinacoes Odds + Match State @60.
4. Maior efeito observado: `match_balance_high + shots_last_10m_high`.
5. Existe pelo menos uma interacao MANTER? Nao.

## Regras Anti-Leakage Confirmadas

- Odds usadas sao pre-jogo/closing Football-Data; nenhuma odd live/in-play foi usada.
- Asian Handicap nao foi usado.
- H8 usa somente dados ate o cutoff correspondente.
- Match State usa somente placar/eventos ate o cutoff correspondente.
- Target usa somente `target_goal_after_cutoff` do cutoff correspondente.
- Placar final e estatisticas full-match nao foram usados como features.
- Cutoff 60 foi avaliado primeiro e nao foi escolhido retroativamente.

## Limitacoes

- Football-Data nao fornece timestamp individual das closing odds; a semantica closing foi tratada como pre-jogo conforme documentado.
- A amostra de interacoes pode ficar pequena apos cruzamentos.
- Uma unica temporada limita inferencia estatistica.
- P-values nao foram ajustados para multipla testagem; por isso classificacoes `OBSERVAR` devem ser tratadas como exploratorias.
- Alguns sinais podem refletir componentes isolados, por isso a comparacao contra odds/H8/Match State isolados foi reportada.

## Recomendacao Quant

- Recomendacao: observar os sinais classificados como `OBSERVAR`; nao autorizar baseline ainda sem revisao Quant da robustez.
