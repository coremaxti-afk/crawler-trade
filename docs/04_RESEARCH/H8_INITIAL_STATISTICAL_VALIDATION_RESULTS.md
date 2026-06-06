# H8 Initial Statistical Validation Results

Status: EXECUTADA
Data: 2026-06-06
Escopo: H8-A Graph / Momentum e H8-B Shotmap, cutoffs 60, 65, 70 e 75 minutos.

## Resumo executivo

A validacao estatistica inicial H8 foi executada contra o PostgreSQL local e o Dataset V1, usando exclusivamente registros com `minute <= cutoff` para construir as variaveis explicativas. O target avaliado foi `target_late_goal_75`.

Resumo dos testes: 36 combinacoes cutoff-feature avaliadas, com 2 classificadas como MANTER, 27 como OBSERVAR, 7 como DESCARTAR e 0 como NAO TESTAVEL.

A feature de maior valor informacional nesta rodada foi `momentum_trend_last_10m` no cutoff 60, classificada como MANTER. Esta conclusao e preliminar e deve ser tratada como validacao exploratoria, nao como autorizacao para producao ou trading.

## Metodologia aplicada

- Unidade estatistica: uma linha por partida e cutoff.
- Cutoffs avaliados: 60, 65, 70 e 75 minutos.
- Target: `target_late_goal_75` do Dataset V1.
- Graph: usa apenas pontos de `match_graph` com `minute <= cutoff`.
- Shotmap: usa apenas finalizacoes de `match_shotmap` com `minute <= cutoff`.
- Agrupamento: quartis via `qcut` quando possivel; fallback binario zero vs positivo apenas quando quartis colapsam por concentracao em zero.
- Testes: qui-quadrado para tabelas com mais de 2 grupos; Fisher exact para tabelas 2x2.
- Tamanho de efeito: Cramer's V para qui-quadrado; odds ratio para Fisher.
- Criterio: MANTER quando p-value < 0.05 e efeito absoluto >= 5 p.p.; OBSERVAR quando efeito >= 3 p.p. ou p-value < 0.10; DESCARTAR quando efeito e significancia forem fracos; NAO TESTAVEL para baixa variancia ou amostra insuficiente.

## Fontes usadas

- `match_graph`
- `match_shotmap`
- `match_source_status`
- `data/processed/datasets/late_goal_dataset_v1.csv`

Nenhuma estatistica full-match de `match_statistics` foi usada como variavel explicativa.

## Cobertura

- Dataset V1: 380 partidas.
- Target positivo: 189 partidas (49.74%).
- Graph: 34861 pontos em 379 partidas.
- Shotmap: 9883 finalizacoes em 380 partidas.
- Source status: 760 registros.
- Known missing: `12437015` permanece sem `graph.json`, com HTTP 404, e foi excluida apenas das features que dependem de Graph.

## Amostra por cutoff

| Cutoff | N total | Positivos | Negativos | Baseline | Graph validos | Shotmap validos |
|---:|---:|---:|---:|---:|---:|---:|
| 60 | 380 | 189 | 191 | 49.74% | 379 | 380 |
| 65 | 380 | 189 | 191 | 49.74% | 379 | 380 |
| 70 | 380 | 189 | 191 | 49.74% | 379 | 380 |
| 75 | 380 | 189 | 191 | 49.74% | 379 | 380 |

## Resultados H8-A Graph

| Cutoff | Feature | N | Pos | Neg | Teste | p-value | Efeito | Max diff | Classe |
|---:|---|---:|---:|---:|---|---:|---:|---:|---|
| 60 | `momentum_last_5m_avg` | 379 | 189 | 190 | Chi-square | 0.7201 | 0.0594 | 4.6 p.p. | OBSERVAR |
| 60 | `momentum_last_10m_avg` | 379 | 189 | 190 | Chi-square | 0.7611 | 0.0555 | 4.6 p.p. | OBSERVAR |
| 60 | `momentum_trend_last_10m` | 379 | 189 | 190 | Chi-square | 0.0194 | 0.1616 | 13.0 p.p. | MANTER |
| 60 | `momentum_sum_until_cutoff` | 379 | 189 | 190 | Chi-square | 0.9245 | 0.0354 | 2.3 p.p. | DESCARTAR |
| 65 | `momentum_last_5m_avg` | 379 | 189 | 190 | Chi-square | 0.0608 | 0.1395 | 10.5 p.p. | OBSERVAR |
| 65 | `momentum_last_10m_avg` | 379 | 189 | 190 | Chi-square | 0.9428 | 0.0320 | 2.2 p.p. | DESCARTAR |
| 65 | `momentum_trend_last_10m` | 379 | 189 | 190 | Chi-square | 0.8015 | 0.0513 | 3.3 p.p. | OBSERVAR |
| 65 | `momentum_sum_until_cutoff` | 379 | 189 | 190 | Chi-square | 0.8116 | 0.0503 | 3.8 p.p. | OBSERVAR |
| 70 | `momentum_last_5m_avg` | 379 | 189 | 190 | Chi-square | 0.7900 | 0.0526 | 4.1 p.p. | OBSERVAR |
| 70 | `momentum_last_10m_avg` | 379 | 189 | 190 | Chi-square | 0.7562 | 0.0560 | 4.6 p.p. | OBSERVAR |
| 70 | `momentum_trend_last_10m` | 379 | 189 | 190 | Chi-square | 0.2235 | 0.1075 | 8.8 p.p. | OBSERVAR |
| 70 | `momentum_sum_until_cutoff` | 379 | 189 | 190 | Chi-square | 0.8116 | 0.0503 | 3.8 p.p. | OBSERVAR |
| 75 | `momentum_last_5m_avg` | 379 | 189 | 190 | Chi-square | 0.8108 | 0.0503 | 3.8 p.p. | OBSERVAR |
| 75 | `momentum_last_10m_avg` | 379 | 189 | 190 | Chi-square | 0.8820 | 0.0418 | 3.0 p.p. | DESCARTAR |
| 75 | `momentum_trend_last_10m` | 379 | 189 | 190 | Chi-square | 0.7271 | 0.0588 | 4.4 p.p. | OBSERVAR |
| 75 | `momentum_sum_until_cutoff` | 379 | 189 | 190 | Chi-square | 0.9205 | 0.0361 | 2.5 p.p. | DESCARTAR |

## Resultados H8-B Shotmap

| Cutoff | Feature | N | Pos | Neg | Teste | p-value | Efeito | Max diff | Classe |
|---:|---|---:|---:|---:|---|---:|---:|---:|---|
| 60 | `xg_last_5m` | 380 | 189 | 191 | Chi-square | 0.6149 | 0.0688 | 5.0 p.p. | OBSERVAR |
| 60 | `xg_last_10m` | 380 | 189 | 191 | Chi-square | 0.3228 | 0.0958 | 7.6 p.p. | OBSERVAR |
| 60 | `shots_last_5m` | 380 | 189 | 191 | Chi-square | 0.7652 | 0.0375 | 3.6 p.p. | OBSERVAR |
| 60 | `shots_last_10m` | 380 | 189 | 191 | Chi-square | 0.0492 | 0.1437 | 11.7 p.p. | MANTER |
| 60 | `xg_sum_until_cutoff` | 380 | 189 | 191 | Chi-square | 0.4501 | 0.0834 | 6.1 p.p. | OBSERVAR |
| 65 | `xg_last_5m` | 380 | 189 | 191 | Chi-square | 0.6908 | 0.0621 | 4.5 p.p. | OBSERVAR |
| 65 | `xg_last_10m` | 380 | 189 | 191 | Chi-square | 0.9899 | 0.0175 | 1.3 p.p. | DESCARTAR |
| 65 | `shots_last_5m` | 380 | 189 | 191 | Chi-square | 0.6358 | 0.0488 | 4.4 p.p. | OBSERVAR |
| 65 | `shots_last_10m` | 380 | 189 | 191 | Chi-square | 0.9951 | 0.0136 | 1.2 p.p. | DESCARTAR |
| 65 | `xg_sum_until_cutoff` | 380 | 189 | 191 | Chi-square | 0.4501 | 0.0834 | 7.1 p.p. | OBSERVAR |
| 70 | `xg_last_5m` | 380 | 189 | 191 | Chi-square | 0.7911 | 0.0524 | 4.5 p.p. | OBSERVAR |
| 70 | `xg_last_10m` | 380 | 189 | 191 | Chi-square | 0.4501 | 0.0834 | 6.6 p.p. | OBSERVAR |
| 70 | `shots_last_5m` | 380 | 189 | 191 | Chi-square | 0.6555 | 0.0471 | 2.8 p.p. | DESCARTAR |
| 70 | `shots_last_10m` | 380 | 189 | 191 | Chi-square | 0.7069 | 0.0606 | 4.8 p.p. | OBSERVAR |
| 70 | `xg_sum_until_cutoff` | 380 | 189 | 191 | Chi-square | 0.7707 | 0.0544 | 3.9 p.p. | OBSERVAR |
| 75 | `xg_last_5m` | 380 | 189 | 191 | Chi-square | 0.5071 | 0.0598 | 4.5 p.p. | OBSERVAR |
| 75 | `xg_last_10m` | 380 | 189 | 191 | Chi-square | 0.3454 | 0.0934 | 6.1 p.p. | OBSERVAR |
| 75 | `shots_last_5m` | 380 | 189 | 191 | Chi-square | 0.6646 | 0.0464 | 5.4 p.p. | OBSERVAR |
| 75 | `shots_last_10m` | 380 | 189 | 191 | Chi-square | 0.8851 | 0.0413 | 3.1 p.p. | OBSERVAR |
| 75 | `xg_sum_until_cutoff` | 380 | 189 | 191 | Chi-square | 0.2913 | 0.0992 | 7.6 p.p. | OBSERVAR |

## Ranking preliminar geral

| Rank | Cutoff | Grupo | Feature | Classe | p-value | Efeito | Max diff |
|---:|---:|---|---|---|---:|---:|---:|
| 1 | 60 | H8-A Graph | `momentum_trend_last_10m` | MANTER | 0.0194 | 0.1616 | 13.0 p.p. |
| 2 | 60 | H8-B Shotmap | `shots_last_10m` | MANTER | 0.0492 | 0.1437 | 11.7 p.p. |
| 3 | 65 | H8-A Graph | `momentum_last_5m_avg` | OBSERVAR | 0.0608 | 0.1395 | 10.5 p.p. |
| 4 | 70 | H8-A Graph | `momentum_trend_last_10m` | OBSERVAR | 0.2235 | 0.1075 | 8.8 p.p. |
| 5 | 75 | H8-B Shotmap | `xg_sum_until_cutoff` | OBSERVAR | 0.2913 | 0.0992 | 7.6 p.p. |
| 6 | 60 | H8-B Shotmap | `xg_last_10m` | OBSERVAR | 0.3228 | 0.0958 | 7.6 p.p. |
| 7 | 65 | H8-B Shotmap | `xg_sum_until_cutoff` | OBSERVAR | 0.4501 | 0.0834 | 7.1 p.p. |
| 8 | 70 | H8-B Shotmap | `xg_last_10m` | OBSERVAR | 0.4501 | 0.0834 | 6.6 p.p. |
| 9 | 75 | H8-B Shotmap | `xg_last_10m` | OBSERVAR | 0.3454 | 0.0934 | 6.1 p.p. |
| 10 | 60 | H8-B Shotmap | `xg_sum_until_cutoff` | OBSERVAR | 0.4501 | 0.0834 | 6.1 p.p. |
| 11 | 75 | H8-B Shotmap | `shots_last_5m` | OBSERVAR | 0.6646 | 0.0464 | 5.4 p.p. |
| 12 | 60 | H8-B Shotmap | `xg_last_5m` | OBSERVAR | 0.6149 | 0.0688 | 5.0 p.p. |
| 13 | 70 | H8-B Shotmap | `shots_last_10m` | OBSERVAR | 0.7069 | 0.0606 | 4.8 p.p. |
| 14 | 60 | H8-A Graph | `momentum_last_5m_avg` | OBSERVAR | 0.7201 | 0.0594 | 4.6 p.p. |
| 15 | 70 | H8-A Graph | `momentum_last_10m_avg` | OBSERVAR | 0.7562 | 0.0560 | 4.6 p.p. |
| 16 | 60 | H8-A Graph | `momentum_last_10m_avg` | OBSERVAR | 0.7611 | 0.0555 | 4.6 p.p. |
| 17 | 75 | H8-B Shotmap | `xg_last_5m` | OBSERVAR | 0.5071 | 0.0598 | 4.5 p.p. |
| 18 | 65 | H8-B Shotmap | `xg_last_5m` | OBSERVAR | 0.6908 | 0.0621 | 4.5 p.p. |
| 19 | 70 | H8-B Shotmap | `xg_last_5m` | OBSERVAR | 0.7911 | 0.0524 | 4.5 p.p. |
| 20 | 75 | H8-A Graph | `momentum_trend_last_10m` | OBSERVAR | 0.7271 | 0.0588 | 4.4 p.p. |
| 21 | 65 | H8-B Shotmap | `shots_last_5m` | OBSERVAR | 0.6358 | 0.0488 | 4.4 p.p. |
| 22 | 70 | H8-A Graph | `momentum_last_5m_avg` | OBSERVAR | 0.7900 | 0.0526 | 4.1 p.p. |
| 23 | 70 | H8-B Shotmap | `xg_sum_until_cutoff` | OBSERVAR | 0.7707 | 0.0544 | 3.9 p.p. |
| 24 | 75 | H8-A Graph | `momentum_last_5m_avg` | OBSERVAR | 0.8108 | 0.0503 | 3.8 p.p. |
| 25 | 65 | H8-A Graph | `momentum_sum_until_cutoff` | OBSERVAR | 0.8116 | 0.0503 | 3.8 p.p. |
| 26 | 70 | H8-A Graph | `momentum_sum_until_cutoff` | OBSERVAR | 0.8116 | 0.0503 | 3.8 p.p. |
| 27 | 60 | H8-B Shotmap | `shots_last_5m` | OBSERVAR | 0.7652 | 0.0375 | 3.6 p.p. |
| 28 | 65 | H8-A Graph | `momentum_trend_last_10m` | OBSERVAR | 0.8015 | 0.0513 | 3.3 p.p. |
| 29 | 75 | H8-B Shotmap | `shots_last_10m` | OBSERVAR | 0.8851 | 0.0413 | 3.1 p.p. |
| 30 | 75 | H8-A Graph | `momentum_last_10m_avg` | DESCARTAR | 0.8820 | 0.0418 | 3.0 p.p. |
| 31 | 70 | H8-B Shotmap | `shots_last_5m` | DESCARTAR | 0.6555 | 0.0471 | 2.8 p.p. |
| 32 | 75 | H8-A Graph | `momentum_sum_until_cutoff` | DESCARTAR | 0.9205 | 0.0361 | 2.5 p.p. |
| 33 | 60 | H8-A Graph | `momentum_sum_until_cutoff` | DESCARTAR | 0.9245 | 0.0354 | 2.3 p.p. |
| 34 | 65 | H8-A Graph | `momentum_last_10m_avg` | DESCARTAR | 0.9428 | 0.0320 | 2.2 p.p. |
| 35 | 65 | H8-B Shotmap | `xg_last_10m` | DESCARTAR | 0.9899 | 0.0175 | 1.3 p.p. |
| 36 | 65 | H8-B Shotmap | `shots_last_10m` | DESCARTAR | 0.9951 | 0.0136 | 1.2 p.p. |

## Ranking por cutoff

### Cutoff 60

| Rank | Cutoff | Grupo | Feature | Classe | p-value | Efeito | Max diff |
|---:|---:|---|---|---|---:|---:|---:|
| 1 | 60 | H8-A Graph | `momentum_trend_last_10m` | MANTER | 0.0194 | 0.1616 | 13.0 p.p. |
| 2 | 60 | H8-B Shotmap | `shots_last_10m` | MANTER | 0.0492 | 0.1437 | 11.7 p.p. |
| 3 | 60 | H8-B Shotmap | `xg_last_10m` | OBSERVAR | 0.3228 | 0.0958 | 7.6 p.p. |
| 4 | 60 | H8-B Shotmap | `xg_sum_until_cutoff` | OBSERVAR | 0.4501 | 0.0834 | 6.1 p.p. |
| 5 | 60 | H8-B Shotmap | `xg_last_5m` | OBSERVAR | 0.6149 | 0.0688 | 5.0 p.p. |
| 6 | 60 | H8-A Graph | `momentum_last_5m_avg` | OBSERVAR | 0.7201 | 0.0594 | 4.6 p.p. |
| 7 | 60 | H8-A Graph | `momentum_last_10m_avg` | OBSERVAR | 0.7611 | 0.0555 | 4.6 p.p. |
| 8 | 60 | H8-B Shotmap | `shots_last_5m` | OBSERVAR | 0.7652 | 0.0375 | 3.6 p.p. |
| 9 | 60 | H8-A Graph | `momentum_sum_until_cutoff` | DESCARTAR | 0.9245 | 0.0354 | 2.3 p.p. |

### Cutoff 65

| Rank | Cutoff | Grupo | Feature | Classe | p-value | Efeito | Max diff |
|---:|---:|---|---|---|---:|---:|---:|
| 1 | 65 | H8-A Graph | `momentum_last_5m_avg` | OBSERVAR | 0.0608 | 0.1395 | 10.5 p.p. |
| 2 | 65 | H8-B Shotmap | `xg_sum_until_cutoff` | OBSERVAR | 0.4501 | 0.0834 | 7.1 p.p. |
| 3 | 65 | H8-B Shotmap | `xg_last_5m` | OBSERVAR | 0.6908 | 0.0621 | 4.5 p.p. |
| 4 | 65 | H8-B Shotmap | `shots_last_5m` | OBSERVAR | 0.6358 | 0.0488 | 4.4 p.p. |
| 5 | 65 | H8-A Graph | `momentum_sum_until_cutoff` | OBSERVAR | 0.8116 | 0.0503 | 3.8 p.p. |
| 6 | 65 | H8-A Graph | `momentum_trend_last_10m` | OBSERVAR | 0.8015 | 0.0513 | 3.3 p.p. |
| 7 | 65 | H8-A Graph | `momentum_last_10m_avg` | DESCARTAR | 0.9428 | 0.0320 | 2.2 p.p. |
| 8 | 65 | H8-B Shotmap | `xg_last_10m` | DESCARTAR | 0.9899 | 0.0175 | 1.3 p.p. |
| 9 | 65 | H8-B Shotmap | `shots_last_10m` | DESCARTAR | 0.9951 | 0.0136 | 1.2 p.p. |

### Cutoff 70

| Rank | Cutoff | Grupo | Feature | Classe | p-value | Efeito | Max diff |
|---:|---:|---|---|---|---:|---:|---:|
| 1 | 70 | H8-A Graph | `momentum_trend_last_10m` | OBSERVAR | 0.2235 | 0.1075 | 8.8 p.p. |
| 2 | 70 | H8-B Shotmap | `xg_last_10m` | OBSERVAR | 0.4501 | 0.0834 | 6.6 p.p. |
| 3 | 70 | H8-B Shotmap | `shots_last_10m` | OBSERVAR | 0.7069 | 0.0606 | 4.8 p.p. |
| 4 | 70 | H8-A Graph | `momentum_last_10m_avg` | OBSERVAR | 0.7562 | 0.0560 | 4.6 p.p. |
| 5 | 70 | H8-B Shotmap | `xg_last_5m` | OBSERVAR | 0.7911 | 0.0524 | 4.5 p.p. |
| 6 | 70 | H8-A Graph | `momentum_last_5m_avg` | OBSERVAR | 0.7900 | 0.0526 | 4.1 p.p. |
| 7 | 70 | H8-B Shotmap | `xg_sum_until_cutoff` | OBSERVAR | 0.7707 | 0.0544 | 3.9 p.p. |
| 8 | 70 | H8-A Graph | `momentum_sum_until_cutoff` | OBSERVAR | 0.8116 | 0.0503 | 3.8 p.p. |
| 9 | 70 | H8-B Shotmap | `shots_last_5m` | DESCARTAR | 0.6555 | 0.0471 | 2.8 p.p. |

### Cutoff 75

| Rank | Cutoff | Grupo | Feature | Classe | p-value | Efeito | Max diff |
|---:|---:|---|---|---|---:|---:|---:|
| 1 | 75 | H8-B Shotmap | `xg_sum_until_cutoff` | OBSERVAR | 0.2913 | 0.0992 | 7.6 p.p. |
| 2 | 75 | H8-B Shotmap | `xg_last_10m` | OBSERVAR | 0.3454 | 0.0934 | 6.1 p.p. |
| 3 | 75 | H8-B Shotmap | `shots_last_5m` | OBSERVAR | 0.6646 | 0.0464 | 5.4 p.p. |
| 4 | 75 | H8-B Shotmap | `xg_last_5m` | OBSERVAR | 0.5071 | 0.0598 | 4.5 p.p. |
| 5 | 75 | H8-A Graph | `momentum_trend_last_10m` | OBSERVAR | 0.7271 | 0.0588 | 4.4 p.p. |
| 6 | 75 | H8-A Graph | `momentum_last_5m_avg` | OBSERVAR | 0.8108 | 0.0503 | 3.8 p.p. |
| 7 | 75 | H8-B Shotmap | `shots_last_10m` | OBSERVAR | 0.8851 | 0.0413 | 3.1 p.p. |
| 8 | 75 | H8-A Graph | `momentum_last_10m_avg` | DESCARTAR | 0.8820 | 0.0418 | 3.0 p.p. |
| 9 | 75 | H8-A Graph | `momentum_sum_until_cutoff` | DESCARTAR | 0.9205 | 0.0361 | 2.5 p.p. |

## Comparacao Graph vs Shotmap

| Grupo | Testes | MANTER | OBSERVAR | DESCARTAR | NAO TESTAVEL | Melhor p-value | Maior efeito |
|---|---:|---:|---:|---:|---:|---:|---:|
| H8-A Graph | 16 | 1 | 11 | 4 | 0 | 0.0194 | 13.0 p.p. |
| H8-B Shotmap | 20 | 1 | 16 | 3 | 0 | 0.0492 | 11.7 p.p. |

Leitura inicial: Graph e Shotmap devem ser avaliados como familias complementares. Graph representa pressao/momentum agregado minuto a minuto; Shotmap representa volume e qualidade de finalizacoes ate o cutoff. A comparacao acima mostra qual familia concentrou maior sinal estatistico nesta amostra, mas ainda nao substitui validacao multivariada futura.

## Comportamento por cutoff

| Cutoff | Testes | MANTER | OBSERVAR | DESCARTAR | NAO TESTAVEL | Melhor p-value | Maior efeito |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 60 | 9 | 2 | 6 | 1 | 0 | 0.0194 | 13.0 p.p. |
| 65 | 9 | 0 | 6 | 3 | 0 | 0.0608 | 10.5 p.p. |
| 70 | 9 | 0 | 8 | 1 | 0 | 0.2235 | 8.8 p.p. |
| 75 | 9 | 0 | 7 | 2 | 0 | 0.2913 | 7.6 p.p. |

| Feature | 60 | 65 | 70 | 75 | Leitura |
|---|---:|---:|---:|---:|---|
| `momentum_last_5m_avg` | 4.6 p.p. | 10.5 p.p. | 4.1 p.p. | 3.8 p.p. | sinal relativamente estavel |
| `momentum_last_10m_avg` | 4.6 p.p. | 2.2 p.p. | 4.6 p.p. | 3.0 p.p. | sinal enfraquece ate 75 |
| `momentum_trend_last_10m` | 13.0 p.p. | 3.3 p.p. | 8.8 p.p. | 4.4 p.p. | sinal enfraquece ate 75 |
| `momentum_sum_until_cutoff` | 2.3 p.p. | 3.8 p.p. | 3.8 p.p. | 2.5 p.p. | sinal relativamente estavel |
| `xg_last_5m` | 5.0 p.p. | 4.5 p.p. | 4.5 p.p. | 4.5 p.p. | sinal relativamente estavel |
| `xg_last_10m` | 7.6 p.p. | 1.3 p.p. | 6.6 p.p. | 6.1 p.p. | sinal enfraquece ate 75 |
| `shots_last_5m` | 3.6 p.p. | 4.4 p.p. | 2.8 p.p. | 5.4 p.p. | sinal melhora ate 75 |
| `shots_last_10m` | 11.7 p.p. | 1.2 p.p. | 4.8 p.p. | 3.1 p.p. | sinal enfraquece ate 75 |
| `xg_sum_until_cutoff` | 6.1 p.p. | 7.1 p.p. | 3.9 p.p. | 7.6 p.p. | sinal melhora ate 75 |

## Maior valor informacional

A combinacao mais forte nesta rodada foi `momentum_trend_last_10m` no cutoff 60, com classificacao MANTER, p-value 0.0194 e efeito maximo de 13.0 p.p. contra o baseline da amostra.

## Riscos de leakage

- As features foram calculadas apenas com `minute <= cutoff`.
- O target `target_late_goal_75` foi usado apenas como variavel resposta.
- Nenhuma feature target-derived foi usada como explicativa.
- Nenhum dado de placar final, forecast, xG/xGA pre-jogo ambiguo ou estatistica full-match foi usado.
- Para cutoff 75, o target representa gol apos 75; portanto as features incluem no maximo informacao ate o minuto 75.

## Limitacoes

- Esta e uma validacao univariada/exploratoria, sem modelo e sem controle multivariado.
- A interpretacao de `momentum_value` ainda depende da semantica original do SofaScore; o valor foi preservado sem inversao, normalizacao ou transformacao direcional.
- O event_id `12437015` nao possui Graph por HTTP 404 conhecido, reduzindo a amostra de features H8-A para 379 partidas.
- Features de Shotmap concentradas em zero podem exigir agrupamento binario quando quartis nao sao informativos.
- Resultados estatisticamente fracos nesta amostra nao descartam definitivamente uso futuro em combinacao multivariada.

## Recomendacao para proxima etapa

- Promover para etapa seguinte apenas as features classificadas como MANTER ou OBSERVAR.
- Manter Graph e Shotmap separados no proximo desenho experimental para medir contribuicao incremental.
- Antes de qualquer baseline H8, gerar um Feature Builder H8 auditavel com as mesmas regras de cutoff e whitelist.
- Nao iniciar producao, backtesting financeiro ou automacao operacional com estes resultados.
