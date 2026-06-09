# PATTERN GOAL RATE RANKING V2

## Status

Documento consolidado V2 com as pesquisas, cenarios, filtros, baselines e variacoes testadas no projeto LateGoalResearch ate este ponto.

Nao contem codigo.

Nao cria dataset.

Nao executa baseline.

Nao cria modelo.

Nao faz backtesting.

Nao cria producao.

---

## 1. Objetivo

Consolidar em um unico documento todas as pesquisas relevantes ja realizadas, incluindo:

- hipoteses bloqueadas;
- baselines nao aprovados;
- validacoes estatisticas;
- segmentacoes;
- interacoes;
- odds;
- H8 short-term;
- padroes de gol;
- padroes de no-goal/Under;
- resultados que nao sao diretamente ranqueaveis por taxa de gol.

A finalidade e apoiar analise manual de mercado e orientar futuras pesquisas de EV/preco.

Importante:

```text
Taxa de gol nao e lucro.
Taxa de acerto nao e EV positivo.
Modelo aprovado nao existe.
Backtesting aprovado nao existe.
Producao aprovada nao existe.
```

---

## 2. Fontes Consolidadas

Relatorios e documentos considerados:

- `TARGET_SPECIFICATION.md`
- `STATISTICAL_VALIDATION_H1_H2.md`
- `STATISTICAL_VALIDATION_H3_H4.md`
- `INITIAL_STATISTICAL_VALIDATION_H6_H9.md`
- `BASELINE_PREMATCH_H3_H4_RESULTS.md`
- `BASELINE_INGAME_V1_RESULTS.md`
- `BASELINE_H8_V1_RESULTS.md`
- `TEAM_PROFILE_SEGMENTATION_RESULTS.md`
- `SEGMENTATION_H8_INTERACTION_RESULTS.md`
- `SEGMENTATION_H8_ROBUSTNESS_VALIDATION_RESULTS.md`
- `MATCH_STATE_ANALYSIS.md`
- `ODDS_FEATURE_CATALOG_V1.md`
- `ODDS_INITIAL_STATISTICAL_VALIDATION_RESULTS.md`
- `ODDS_INTERACTION_VALIDATION_RESULTS_V1.md`
- `H8_SHORT_TERM_SIGNAL_VALIDATION_RESULTS_V1.md`
- `PATTERN_GOAL_RATE_RANKING.md`

---

## 3. Como Ler Este Documento

Este documento tem dois tipos de resultado:

### 3.1 Resultados ranqueaveis por taxa

Exemplos:

- visitante vencendo por 1 aos 70;
- 3 gols ja marcados aos 60;
- defensivo_fragile + shots_last_10m;
- cold_game_2of4;
- match_balance_high + shots_last_10m_high.

Esses entram no ranking de taxa de gol ou no-goal.

### 3.2 Resultados nao ranqueaveis por taxa direta

Exemplos:

- H1/H2 bloqueado por leakage;
- Baseline H3/H4 com ROC-AUC/PR-AUC;
- Baseline In-Game H6/H9;
- Baseline H8 V1.

Esses entram como pesquisa/modelagem, nao como padrao operacional direto.

---

# PARTE A — PESQUISAS BLOQUEADAS OU NAO RANQUEAVEIS POR TAXA

## 4. H1/H2 — xG / Forecast Pre-Match

### Status

```text
BLOQUEADO
```

### Motivo

H1/H2 foram bloqueadas porque as fontes disponiveis de xG/forecast nao eram comprovadamente pre-kickoff e tinham risco de data leakage.

Achados principais:

- `matches.home_xg` e `matches.away_xg` representam xG final da propria partida.
- `team_match_stats.xg/xga` sao estatisticas finais por time/partida.
- `forecast_*` vinha de registro final Understat, sem prova de disponibilidade pre-jogo.
- `matches_master` tinha xG/forecast nao utilizavel para a analise segura.

### Decisao

```text
Nao entra em ranking.
Nao entra em dataset.
Nao entra em baseline.
Nao entra em modelo.
```

---

## 5. H3/H4 — Pre-Match Historical Team Form

### Tipo de pesquisa

Features historicas pre-jogo.

### Features testadas no baseline H3/H4

- `home_goals_for_avg_last_3`
- `home_goals_for_avg_last_10`
- `home_shots_on_target_for_avg_last_5`
- `home_shots_against_avg_last_5`
- `home_shots_on_target_against_avg_last_5`
- `home_big_chances_against_avg_last_5`
- `away_goals_for_avg_last_3`
- `away_goals_for_avg_last_10`
- `away_shots_on_target_for_avg_last_5`
- `away_shots_against_avg_last_5`
- `away_shots_on_target_against_avg_last_5`
- `away_big_chances_against_avg_last_5`

### Resultado do Baseline 1A Pre-Match H3/H4

Target:

```text
target_late_goal_75
```

Split:

```text
Temporal 60/20/20
```

Resultado no teste:

| Metrica | Valor |
|---|---:|
| ROC-AUC Test | 0.4910 |
| PR-AUC Test | 0.5364 |
| Prevalencia Test | 0.5263 |
| Brier delta vs nulo | +0.0089 |
| LogLoss delta vs nulo | +0.0180 |
| Status criterios | NAO APROVADO |

### Decisao

```text
NAO APROVADO COMO BASELINE
```

### Leitura de mercado

H3/H4 historico pre-jogo, sozinho, nao foi util para orientar estrategia de gol tardio nesta amostra.

---

## 6. H6/H9 — In-Game Simple State Baseline

### Tipo de pesquisa

Features simples in-game ate cutoff 75.

Features:

- `score_diff_home_until_cutoff`
- `cards_until_cutoff`
- `substitutions_until_cutoff`
- `score_state_group`

### Resultado do Baseline In-Game V1

Target:

```text
target_late_goal_75
```

Cutoff:

```text
75
```

Resultado no teste:

| Metrica | Valor |
|---|---:|
| ROC-AUC Test | 0.5250 |
| PR-AUC Test | 0.5541 |
| Prevalencia Test | 0.5263 |
| Delta Brier | +0.0019 |
| Delta LogLoss | +0.0041 |
| Status criterios | NAO APROVADO |

### Decisao

```text
NAO APROVADO COMO BASELINE
```

### Leitura de mercado

Estado simples de jogo aos 75 ajudou pouco. O valor parece estar mais em padroes especificos de Match State do que em modelo simples.

---

## 7. H8 Baseline V1 — Graph / Shotmap

### Tipo de pesquisa

Baseline modelado com features H8 por cutoff.

Features H8 usadas:

- `momentum_last_5m_avg`
- `momentum_last_10m_avg`
- `momentum_trend_last_10m`
- `momentum_sum_until_cutoff`
- `xg_last_5m`
- `xg_last_10m`
- `shots_last_5m`
- `shots_last_10m`
- `xg_sum_until_cutoff`

### Cutoffs avaliados

- 60
- 65
- 70
- 75

### Resultado resumido por cutoff no teste

| Cutoff | ROC-AUC Test | PR-AUC Test | Lift@20% | Melhor feature | Status |
|---:|---:|---:|---:|---|---|
| 60 | 0.5076 | 0.5232 | 0.9500 | `momentum_last_10m_avg` | Melhor cutoff, mas NAO APROVADO |
| 65 | 0.4299 | 0.4771 | 0.8313 | `xg_last_10m` | NAO APROVADO |
| 70 | 0.4903 | 0.5378 | 0.9500 | `xg_last_5m` | NAO APROVADO |
| 75 | 0.4521 | 0.4899 | 0.7125 | `xg_last_10m` | NAO APROVADO |

### Decisao

```text
NAO APROVADO COMO BASELINE
```

### Leitura de mercado

O cutoff 60 apareceu como o melhor em modelagem H8, mas ainda sem performance suficiente. Isso motivou a frente posterior de janela curta.

---

# PARTE B — SEGMENTACAO HISTORICA ISOLADA

## 8. Team Profile Segmentation Results

Target:

```text
target_late_goal_75
```

Taxa geral:

```text
49.7%
```

| Rank | Segmento | N | Pos | Taxa | Diff | OR | p-value | Classe |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `ofensivo_forte_vs_defesa_fragil` | 56 | 32 | **57.1%** | +7.4 p.p. | 1.42 | 0.2492 | OBSERVAR |
| 2 | `sem_ofensivo_forte_sem_defesa_fragil` | 43 | 23 | **53.5%** | +3.7 p.p. | 1.18 | 0.6302 | OBSERVAR |
| 3 | `ambos_defesa_forte` | 30 | 16 | **53.3%** | +3.6 p.p. | 1.17 | 0.7077 | OBSERVAR |
| 4 | `ao_menos_uma_defesa_fragil` | 163 | 83 | **50.9%** | +1.2 p.p. | 1.09 | 0.7559 | DESCARTAR |
| 5 | `ao_menos_um_ofensivo_forte` | 177 | 88 | **49.7%** | 0.0 p.p. | 1.00 | 1.0000 | DESCARTAR |
| 6 | `ofensivo_fraco_vs_defesa_forte` | 52 | 25 | **48.1%** | -1.7 p.p. | 0.93 | 0.8816 | DESCARTAR |
| 7 | `defesa_fragil_vs_defesa_fragil` | 26 | 12 | **46.2%** | -3.6 p.p. | 0.86 | 0.8395 | DESCARTAR |
| 8 | `ofensivo_forte_vs_ofensivo_forte` | 27 | 12 | **44.4%** | -5.3 p.p. | 0.80 | 0.6905 | DESCARTAR |

### Decisao

```text
PROMISSOR: 0
OBSERVAR: 3
DESCARTAR: 5
```

### Leitura de mercado

Segmentacao historica isolada e fraca. O melhor candidato isolado foi `ofensivo_forte_vs_defesa_fragil`, mas sem significancia suficiente.

---

# PARTE C — SEGMENTACAO + H8

## 9. Interacoes Segmentacao x H8 @60

Target:

```text
target_late_goal_75
```

Cutoff:

```text
60
```

| Rank | Interacao | N | Pos | Taxa gol | Diff | OR | p-value | Classe inicial |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `ofensivo_forte_vs_defesa_fragil + shots_last_10m` | 20 | 15 | **75.0%** | +25.0 p.p. | 3.01 | 0.0353 | OBSERVAR por N pequeno |
| 2 | `defensivo_fragile + shots_last_10m` | 52 | 34 | **65.4%** | +15.4 p.p. | 2.10 | 0.0224 | PROMISSOR inicial |
| 3 | `ofensivo_forte_vs_defesa_fragil + momentum_trend_last_10m` | 16 | 8 | **50.0%** | -0.2 p.p. | 0.99 | 1.0000 | DESCARTAR |
| 4 | `ofensivo_strong + shots_last_10m` | 56 | 28 | **50.0%** | +0.0 p.p. | 1.00 | 1.0000 | DESCARTAR |
| 5 | `ofensivo_strong + momentum_trend_last_10m` | 59 | 25 | **42.4%** | -7.8 p.p. | 0.68 | 0.1971 | DESCARTAR |
| 6 | `defensivo_fragile + momentum_trend_last_10m` | 52 | 22 | **42.3%** | -7.8 p.p. | 0.69 | 0.2288 | DESCARTAR |

---

## 10. Robustez Segmentacao x H8

### defensivo_fragile + shots_last_10m

| Cutoff | N | Pos | Taxa | Diff | OR | p-value | Classe robustez |
|---:|---:|---:|---:|---:|---:|---:|---|
| 60 | 52 | 34 | **65.4%** | +15.4 p.p. | 2.10 | 0.0224 | Forte no 60 |
| 65 | 48 | 26 | **54.2%** | +4.2 p.p. | 1.21 | 0.6389 | Fraco |
| 70 | 46 | 25 | **54.3%** | +4.3 p.p. | 1.22 | 0.6330 | Fraco |

Classificacao final:

```text
OBSERVAR
```

### ofensivo_forte_vs_defesa_fragil + shots_last_10m

| Cutoff | N | Pos | Taxa | Diff | OR | p-value | Classe robustez |
|---:|---:|---:|---:|---:|---:|---:|---|
| 60 | 20 | 15 | **75.0%** | +25.0 p.p. | 3.01 | 0.0353 | Forte, mas N pequeno |
| 65 | 18 | 10 | **55.6%** | +5.6 p.p. | 1.25 | 0.8091 | Fraco |
| 70 | 17 | 11 | **64.7%** | +14.7 p.p. | 1.83 | 0.3190 | N pequeno |

Classificacao final:

```text
DESCARTAR COMO ROBUSTO
```

---

# PARTE D — MATCH STATE

## 11. Estado do Placar por Cutoff

| Rank | Segmento | Cutoff | N | Pos | Taxa gol | Diff | OR | p-value | Classe |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `visitante vencendo por 1` | 60 | 73 | 55 | **75.3%** | +5.6 p.p. | 1.41 | 0.2609 | OBSERVAR |
| 2 | `mandante vencendo por 1` | 60 | 110 | 78 | **70.9%** | +1.2 p.p. | 1.08 | 0.8061 | DESCARTAR |
| 3 | `mandante vencendo por 2+` | 60 | 51 | 36 | **70.6%** | +0.9 p.p. | 1.05 | 1.0000 | DESCARTAR |
| 4 | `empate` | 60 | 105 | 72 | **68.6%** | -1.2 p.p. | 0.93 | 0.8031 | DESCARTAR |
| 5 | `visitante vencendo por 1` | 65 | 72 | 49 | **68.1%** | +3.1 p.p. | 1.18 | 0.5853 | DESCARTAR |
| 6 | `visitante vencendo por 1` | 70 | 74 | 47 | **63.5%** | +5.1 p.p. | 1.30 | 0.3588 | OBSERVAR |
| 7 | `visitante vencendo por 1` | 75 | 74 | 41 | **55.4%** | +5.7 p.p. | 1.33 | 0.3015 | OBSERVAR |
| 8 | `visitante vencendo por 2+` | 60 | 41 | 24 | **58.5%** | -11.2 p.p. | 0.57 | 0.1072 | OBSERVAR negativo |
| 9 | `visitante vencendo por 2+` | 70 | 48 | 23 | **47.9%** | -10.5 p.p. | 0.61 | 0.1200 | OBSERVAR negativo |
| 10 | `visitante vencendo por 2+` | 75 | 52 | 21 | **40.4%** | -9.4 p.p. | 0.65 | 0.1791 | OBSERVAR negativo |

---

## 12. Total de Gols Ja Marcados

| Rank | Segmento | Cutoff | N | Pos | Taxa gol | Diff | OR | p-value | Classe |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `3 gols ja marcados` | 60 | 69 | 52 | **75.4%** | +5.6 p.p. | 1.41 | 0.3112 | OBSERVAR |
| 2 | `0 gols ja marcados` | 60 | 55 | 39 | **70.9%** | +1.2 p.p. | 1.07 | 0.8755 | DESCARTAR |
| 3 | `1 gol ja marcado` | 60 | 127 | 90 | **70.9%** | +1.1 p.p. | 1.08 | 0.8130 | DESCARTAR |
| 4 | `2 gols ja marcados` | 60 | 90 | 61 | **67.8%** | -2.0 p.p. | 0.89 | 0.6939 | DESCARTAR |
| 5 | `3 gols ja marcados` | 65 | 68 | 46 | **67.6%** | +2.6 p.p. | 1.15 | 0.6750 | DESCARTAR |
| 6 | `3 gols ja marcados` | 70 | 72 | 46 | **63.9%** | +5.5 p.p. | 1.33 | 0.3528 | OBSERVAR |
| 7 | `4+ gols ja marcados` | 60 | 39 | 23 | **59.0%** | -10.8 p.p. | 0.59 | 0.1414 | OBSERVAR negativo |
| 8 | `3 gols ja marcados` | 75 | 85 | 49 | **57.6%** | +7.9 p.p. | 1.51 | 0.1100 | OBSERVAR |
| 9 | `4+ gols ja marcados` | 75 | 67 | 29 | **43.3%** | -6.5 p.p. | 0.73 | 0.2820 | OBSERVAR negativo |

---

# PARTE E — ODDS PRE-JOGO ISOLADAS

## 13. Odds Isoladas contra target_late_goal_75

| Padrao | N | Pos | Taxa gol | Diff | OR | p-value | Classe |
|---|---:|---:|---:|---:|---:|---:|---|
| `favorite_side = none_clear` | 24 | 14 | **58.3%** | +8.6 p.p. | 1.45 | 0.4072 | OBSERVAR |
| `implied_prob_over25_norm bottom25` | 95 | 51 | **53.7%** | +3.9 p.p. | 1.23 | 0.4078 | DESCARTAR |
| `over25_closing_strength bottom25` | 95 | 51 | **53.7%** | +3.9 p.p. | 1.23 | 0.4078 | DESCARTAR |
| `match_balance top25` | 95 | 51 | **53.7%** | +3.9 p.p. | 1.23 | 0.4078 | DESCARTAR |
| `favorite_strength bottom25` | 95 | 50 | **52.6%** | +2.9 p.p. | 1.17 | 0.5544 | DESCARTAR |
| `favorite_side = away` | 127 | 66 | **52.0%** | +2.2 p.p. | 1.14 | 0.5869 | DESCARTAR |
| `favorite_side = home` | 229 | 109 | **47.6%** | -2.1 p.p. | 0.81 | 0.3456 | DESCARTAR |
| `implied_prob_over25_norm top25` | 96 | 45 | **46.9%** | -2.9 p.p. | 0.86 | 0.5558 | DESCARTAR |
| `over25_closing_strength top25` | 96 | 45 | **46.9%** | -2.9 p.p. | 0.86 | 0.5558 | DESCARTAR |
| `favorite_strength top25` | 95 | 43 | **45.3%** | -4.5 p.p. | 0.79 | 0.3441 | OBSERVAR negativo |
| `match_balance bottom25` | 95 | 43 | **45.3%** | -4.5 p.p. | 0.79 | 0.3441 | OBSERVAR negativo |

---

# PARTE F — ODDS + H8 / MATCH STATE

## 14. Interacoes Odds + H8 / Match State @60

Target:

```text
goal_after_60
```

Baseline:

```text
69.7%
```

| Rank | Interacao | N | Pos | Taxa gol | Diff | OR | p-value | Classe |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | `favorite_strength_high + favorito_perdendo_aos_cutoff` | 13 | 10 | **76.9%** | +7.2 p.p. | 1.46 | 0.7619 | DESCARTAR por N pequeno |
| 2 | `match_balance_high + shots_last_10m_high` | 30 | 23 | **76.7%** | +6.9 p.p. | 1.47 | 0.5347 | OBSERVAR |
| 3 | `favorite_strength_low + shots_last_10m_high` | 33 | 24 | **72.7%** | +3.0 p.p. | 1.17 | 0.8434 | DESCARTAR |
| 4 | `favorite_strength_high + favorito_vencendo_por_1_aos_cutoff` | 35 | 25 | **71.4%** | +1.7 p.p. | 1.09 | 1.0000 | DESCARTAR |
| 5 | `match_balance_high + empate_aos_cutoff` | 28 | 20 | **71.4%** | +1.7 p.p. | 1.09 | 1.0000 | DESCARTAR |
| 6 | `match_balance_high + total_goals_2_or_3` | 42 | 29 | **69.0%** | -0.7 p.p. | 0.96 | 1.0000 | DESCARTAR |
| 7 | `favorite_strength_high + momentum_trend_positive` | 44 | 30 | **68.2%** | -1.6 p.p. | 0.92 | 0.8618 | DESCARTAR |
| 8 | `favorite_strength_high + shots_last_10m_high` | 34 | 23 | **67.6%** | -2.1 p.p. | 0.90 | 0.8452 | DESCARTAR |
| 9 | `match_balance_low + shots_last_10m_high` | 34 | 23 | **67.6%** | -2.1 p.p. | 0.90 | 0.8452 | DESCARTAR |
| 10 | `favorite_strength_high + empate_aos_cutoff` | 19 | 12 | **63.2%** | -6.6 p.p. | 0.73 | 0.6089 | DESCARTAR |
| 11 | `match_balance_low + empate_aos_cutoff` | 19 | 12 | **63.2%** | -6.6 p.p. | 0.73 | 0.6089 | DESCARTAR |
| 12 | `match_balance_high + momentum_trend_positive` | 44 | 27 | **61.4%** | -8.4 p.p. | 0.65 | 0.2226 | DESCARTAR |

### Robustez do principal OBSERVAR

`match_balance_high + shots_last_10m_high`

| Cutoff | Target | N | Pos | Taxa gol | Diff | Classe |
|---:|---|---:|---:|---:|---:|---|
| 60 | `goal_after_60` | 30 | 23 | **76.7%** | +6.9 p.p. | OBSERVAR |
| 65 | `goal_after_65` | 31 | 20 | **64.5%** | -0.5 p.p. | DESCARTAR |
| 70 | `goal_after_70` | 28 | 14 | **50.0%** | -8.4 p.p. | DESCARTAR |
| 75 | `goal_after_75` | 26 | 15 | **57.7%** | +8.0 p.p. | OBSERVAR |

---

# PARTE G — H8 SHORT-TERM / JANELAS CURTAS

## 15. Hot Signals para Gol

| Rank | Sinal | Target | N | Pos | Taxa gol | Baseline | Diff | OR | p-value | Classe |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `shots_last_10m_high` | `goal_65_80` | 122 | 50 | **41.0%** | 36.8% | +4.1 p.p. | 1.30 | 0.2568 | OBSERVAR |
| 2 | `momentum_trend_positive` | `goal_60_75` | 182 | 75 | **41.2%** | 37.1% | +4.1 p.p. | 1.40 | 0.1366 | OBSERVAR |
| 3 | `momentum_trend_positive` | `goal_60_70` | 182 | 56 | **30.8%** | 26.8% | +3.9 p.p. | 1.47 | 0.1057 | OBSERVAR |
| 4 | `xg_last_10m_high` | `goal_65_80` | 95 | 38 | **40.0%** | 36.8% | +3.2 p.p. | 1.20 | 0.4640 | DESCARTAR |
| 5 | `xg_last_10m_high` | `goal_60_80` | 95 | 46 | **48.4%** | 45.8% | +2.6 p.p. | 1.15 | 0.5549 | DESCARTAR |
| 6 | `shots_last_10m_high` | `goal_60_80` | 122 | 58 | **47.5%** | 45.8% | +1.8 p.p. | 1.11 | 0.6602 | DESCARTAR |
| 7 | `hot_game_2of4` | `goal_65_80` | 148 | 57 | **38.5%** | 36.8% | +1.7 p.p. | 1.12 | 0.6628 | DESCARTAR |
| 8 | `momentum_trend_positive` | `goal_60_80` | 182 | 86 | **47.3%** | 45.8% | +1.5 p.p. | 1.12 | 0.6073 | DESCARTAR |
| 9 | `shots_last_10m_high` | `goal_60_75` | 122 | 44 | **36.1%** | 37.1% | -1.0 p.p. | 0.94 | 0.8205 | DESCARTAR |
| 10 | `shots_last_10m_high` | `goal_60_70` | 122 | 31 | **25.4%** | 26.8% | -1.4 p.p. | 0.90 | 0.7110 | DESCARTAR |

---

## 16. Cold Signals para No-Goal / Under

| Rank | Sinal | Target | N | Pos(no-goal) | Taxa no-goal | Baseline | Diff | OR | p-value | Classe |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | `momentum_trend_non_positive` | `no_goal_60_75` | 197 | 131 | **66.5%** | 62.9% | +3.6 p.p. | 1.38 | 0.1381 | OBSERVAR |
| 2 | `cold_game_2of4` | `no_goal_60_75` | 170 | 112 | **65.9%** | 62.9% | +3.0 p.p. | 1.26 | 0.2876 | OBSERVAR |
| 3 | `shots_last_10m_low` | `no_goal_60_75` | 166 | 108 | **65.1%** | 62.9% | +2.2 p.p. | 1.18 | 0.4555 | DESCARTAR |
| 4 | `xg_last_10m_low` | `no_goal_60_75` | 95 | 60 | **63.2%** | 62.9% | +0.3 p.p. | 1.02 | 1.0000 | DESCARTAR |
| 5 | `xg_last_10m_low` | `no_goal_60_80` | 95 | 54 | **56.8%** | 54.2% | +2.6 p.p. | 1.15 | 0.6345 | DESCARTAR |
| 6 | `momentum_trend_non_positive` | `no_goal_60_80` | 197 | 109 | **55.3%** | 54.2% | +1.1 p.p. | 1.10 | 0.6808 | DESCARTAR |
| 7 | `shots_last_10m_low` | `no_goal_60_80` | 166 | 91 | **54.8%** | 54.2% | +0.6 p.p. | 1.04 | 0.8364 | DESCARTAR |
| 8 | `cold_game_2of4` | `no_goal_60_80` | 170 | 93 | **54.7%** | 54.2% | +0.5 p.p. | 1.04 | 0.9176 | DESCARTAR |
| 9 | `momentum_last_10m_avg_low` | `no_goal_60_75` | 95 | 54 | **56.8%** | 62.9% | -6.1 p.p. | 0.71 | 0.1778 | DESCARTAR |
| 10 | `momentum_last_10m_avg_low` | `no_goal_60_80` | 95 | 45 | **47.4%** | 54.2% | -6.8 p.p. | 0.69 | 0.1245 | DESCARTAR |

---

# PARTE H — RANKING GERAL CONSOLIDADO DE GOL

## 17. Top padroes por taxa de gol observada

| Rank | Padrao | Cutoff / Target | N | Taxa gol | Classe / observacao |
|---:|---|---|---:|---:|---|
| 1 | `favorite_strength_high + favorito_perdendo` | @60 / `goal_after_60` | 13 | **76.9%** | DESCARTAR por N pequeno |
| 2 | `match_balance_high + shots_last_10m_high` | @60 / `goal_after_60` | 30 | **76.7%** | OBSERVAR |
| 3 | `3 gols ja marcados` | @60 / `goal_after_60` | 69 | **75.4%** | OBSERVAR |
| 4 | `visitante vencendo por 1` | @60 / `goal_after_60` | 73 | **75.3%** | OBSERVAR |
| 5 | `ofensivo_forte_vs_defesa_fragil + shots_last_10m` | @60 / `target_late_goal_75` | 20 | **75.0%** | OBSERVAR / N pequeno |
| 6 | `favorite_strength_low + shots_last_10m_high` | @60 / `goal_after_60` | 33 | **72.7%** | DESCARTAR |
| 7 | `favorite_strength_high + favorito_vencendo_por_1` | @60 / `goal_after_60` | 35 | **71.4%** | DESCARTAR |
| 8 | `match_balance_high + empate` | @60 / `goal_after_60` | 28 | **71.4%** | DESCARTAR |
| 9 | `mandante vencendo por 1` | @60 / `goal_after_60` | 110 | **70.9%** | DESCARTAR |
| 10 | `0 gols ja marcados` | @60 / `goal_after_60` | 55 | **70.9%** | DESCARTAR |
| 11 | `1 gol ja marcado` | @60 / `goal_after_60` | 127 | **70.9%** | DESCARTAR |
| 12 | `mandante vencendo por 2+` | @60 / `goal_after_60` | 51 | **70.6%** | DESCARTAR |
| 13 | `visitante vencendo por 1` | @65 / `goal_after_65` | 72 | **68.1%** | DESCARTAR |
| 14 | `3 gols ja marcados` | @65 / `goal_after_65` | 68 | **67.6%** | DESCARTAR |
| 15 | `defensivo_fragile + shots_last_10m` | @60 / `target_late_goal_75` | 52 | **65.4%** | OBSERVAR robustez |
| 16 | `3 gols ja marcados` | @70 / `goal_after_70` | 72 | **63.9%** | OBSERVAR |
| 17 | `visitante vencendo por 1` | @70 / `goal_after_70` | 74 | **63.5%** | OBSERVAR |
| 18 | `3 gols ja marcados` | @75 / `goal_after_75` | 85 | **57.6%** | OBSERVAR |
| 19 | `visitante vencendo por 1` | @75 / `goal_after_75` | 74 | **55.4%** | OBSERVAR |
| 20 | `defensivo_fragile + shots_last_10m` | @65 / `target_late_goal_75` | 48 | **54.2%** | OBSERVAR fraco |
| 21 | `defensivo_fragile + shots_last_10m` | @70 / `target_late_goal_75` | 46 | **54.3%** | OBSERVAR fraco |
| 22 | `ofensivo_forte_vs_defesa_fragil` | pre-match segment / `target_late_goal_75` | 56 | **57.1%** | OBSERVAR |
| 23 | `favorite_side = none_clear` | odds pre-game / `target_late_goal_75` | 24 | **58.3%** | OBSERVAR / N pequeno |

---

# PARTE I — CANDIDATOS DE MERCADO

## 18. Back Over +1 Gol — candidatos para analisar preco

| Prioridade | Padrao | Por que analisar | Cuidado |
|---:|---|---|---|
| 1 | `visitante vencendo por 1 @70` | Taxa 63.5%; odd aos 70 pode estar melhor que aos 60. | Precisa preco real; back @1.70 teve EV positivo em exemplo simplificado. |
| 2 | `3 gols ja marcados @70` | Taxa 63.9%; N=72; padrao simples. | Pode depender do ritmo real do jogo. |
| 3 | `3 gols ja marcados @75` | Taxa 57.6%; odd tende maior. | Menor tempo restante e maior variancia. |
| 4 | `visitante vencendo por 1 @75` | Taxa 55.4%; odd tende maior. | Precisa EV por odd. |
| 5 | `match_balance_high + shots_last_10m_high @60` | Taxa 76.7%; melhor combinado Odds+H8. | N=30; p-value fraco. |
| 6 | `visitante vencendo por 1 @60` | Taxa 75.3%; N=73. | Odd aos 60 pode ser baixa demais. |
| 7 | `3 gols ja marcados @60` | Taxa 75.4%; N=69. | Odd aos 60 pode nao compensar. |
| 8 | `defensivo_fragile + shots_last_10m @60` | Taxa 65.4%; OR 2.10 inicial. | Target diferente e robustez parcial. |

---

## 19. Lay Over / Back Under — candidatos para analisar preco

| Prioridade | Padrao | Por que analisar | Cuidado |
|---:|---|---|---|
| 1 | `momentum_trend_non_positive @60 -> no_goal_60_75` | N=197; sem gol 66.5%. | Diff vs baseline pequena. |
| 2 | `cold_game_2of4 @60 -> no_goal_60_75` | N=170; sem gol 65.9%. | Diff pequena, mas operacionalmente simples. |
| 3 | `shots_last_10m_low @60 -> no_goal_60_75` | N=166; sem gol 65.1%. | Estatisticamente descartado, mas pode ter EV se odd ajudar. |
| 4 | `visitante vencendo por 2+ @60` | taxa de gol 58.5%, abaixo do baseline 69.7. | Precisa converter para no-goal e preco de mercado. |
| 5 | `4+ gols ja marcados @60` | taxa de gol 59.0%, bem abaixo do baseline. | Pode ser leitura Under por jogo ja resolvido/cansaco. |
| 6 | `visitante vencendo por 2+ @70` | taxa de gol 47.9%, abaixo do baseline 58.4. | Forte candidato teorico para Under se mercado nao precificar demais. |
| 7 | `visitante vencendo por 2+ @75` | taxa de gol 40.4%, abaixo do baseline 49.7. | Odd do Lay/Back Under no fim pode ser sensivel. |

---

# PARTE J — CONCLUSAO E PROXIMA ETAPA

## 20. O que foi esquecido na V1 e corrigido aqui

A V1 nao incluiu explicitamente:

- H1/H2 bloqueado;
- H3/H4 baseline pre-match;
- H6/H9 baseline in-game;
- H8 baseline completo por cutoff;
- segmentacao historica isolada completa.

A V2 inclui essas frentes, separando o que e ranqueavel por taxa do que e pesquisa/modelagem nao diretamente comparavel.

---

## 21. Conclusao Quant

As pesquisas ate agora indicam:

1. Pre-match historico H3/H4 nao funcionou como baseline.
2. Estado simples H6/H9 nao funcionou como baseline.
3. H8 modelado nao funcionou como baseline, mas apontou cutoff 60 como melhor regiao.
4. Segmentacao isolada foi fraca.
5. Segmentacao + H8 teve o melhor sinal estatistico inicial, principalmente `defensivo_fragile + shots_last_10m @60`.
6. Match State simples gerou padroes operacionais claros, especialmente `visitante vencendo por 1` e `3 gols ja marcados`.
7. Odds pre-jogo isoladas foram fracas.
8. Odds + H8 teve um sinal observavel: `match_balance_high + shots_last_10m_high @60`.
9. H8 short-term nao gerou PROMISSOR, mas confirmou alguns sinais OBSERVAR para janelas curtas/no-goal.
10. Para trade, a proxima etapa deve ser EV por odd, nao apenas taxa de acerto.

---

## 22. Proxima etapa recomendada

Criar:

```text
docs/04_RESEARCH/MARKET_PRICE_SENSITIVITY_PLAN_V1.md
```

Objetivo:

- usar os padroes deste ranking;
- simular Back Over e Lay Over por faixa de odd;
- calcular break-even;
- calcular EV por R$100;
- calcular ROI teorico;
- separar cenarios de Over e Under;
- nao executar backtesting real ainda;
- nao usar dinheiro real;
- nao criar producao.

---

## 23. Formulas de mercado para analise manual

### Back Over

```text
break_even = 1 / odd_back
EV_por_100 = P(gol) * ((odd_back - 1) * 100) - P(sem_gol) * 100
```

### Lay Over

```text
responsabilidade = stake * (odd_lay - 1)
break_even_sem_gol = responsabilidade / (stake + responsabilidade)
EV_por_100 = P(sem_gol) * stake - P(gol) * responsabilidade
```

---

## 24. Decisao final deste documento

```text
PATTERN_GOAL_RATE_RANKING_V2 CONCLUIDO
```

Uso recomendado:

```text
Base para analise manual de mercado e para o plano de sensibilidade de preco/EV.
```

Restricoes mantidas:

- nao autoriza trade real;
- nao autoriza modelo;
- nao autoriza baseline;
- nao autoriza backtesting financeiro;
- nao autoriza producao.
