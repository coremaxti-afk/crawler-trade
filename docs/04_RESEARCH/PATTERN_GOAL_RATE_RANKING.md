# PATTERN GOAL RATE RANKING

## Status

Documento consolidado para revisao manual e experiencia de mercado.

Nao contem codigo.

Nao cria dataset.

Nao executa baseline.

Nao cria modelo.

Nao faz backtesting.

Nao cria producao.

---

## 1. Objetivo

Consolidar em um unico documento os principais cenarios, filtros e variacoes ja testados no projeto, ordenados por taxa observada de gol ou de ausencia de gol.

A finalidade deste documento e apoiar analise de mercado/trade, principalmente para avaliar quais padroes merecem simulacao futura de lucro/prejuizo com odds reais ou cenarios de odds.

Importante:

```text
Taxa de gol nao e lucro.
Taxa de acerto nao e EV positivo.
Este ranking organiza sinais observados, mas nao autoriza trade, baseline, backtesting ou producao.
```

---

## 2. Fontes Consolidadas

Relatorios usados como base:

- `docs/04_RESEARCH/SEGMENTATION_H8_INTERACTION_RESULTS.md`
- `docs/04_RESEARCH/SEGMENTATION_H8_ROBUSTNESS_VALIDATION_RESULTS.md`
- `docs/04_RESEARCH/MATCH_STATE_ANALYSIS.md`
- `docs/04_RESEARCH/ODDS_INITIAL_STATISTICAL_VALIDATION_RESULTS.md`
- `docs/04_RESEARCH/ODDS_INTERACTION_VALIDATION_RESULTS_V1.md`
- `docs/04_RESEARCH/H8_SHORT_TERM_SIGNAL_VALIDATION_RESULTS_V1.md`

---

## 3. Como Ler Este Documento

Campos:

- **Padrao**: regra/filtro testado.
- **Cutoff / janela**: minuto de entrada/observacao e target usado.
- **N**: numero de jogos no grupo.
- **Taxa**: taxa de gol ou de no-goal observada.
- **Diff**: diferenca vs baseline do mesmo target/cutoff quando disponivel.
- **OR**: odds ratio quando reportado.
- **p-value**: significancia estatistica exploratoria.
- **Classe**: classificacao no relatorio original.
- **Uso de mercado sugerido**: leitura pratica preliminar, nao autorizacao operacional.

Alertas:

- N pequeno: maior risco de instabilidade.
- P-values nao ajustados para multipla testagem.
- Alguns targets sao diferentes entre si, entao comparar taxas diretamente exige cuidado.
- Para trade, a decisao correta depende de odds, cashout, comissao, slippage e timing do gol.

---

# PARTE A — RANKING GERAL DE TAXA DE GOL

## 4. Ranking Consolidado por Taxa de Gol

| Rank | Padrao / variacao | Cutoff / Target | N | Pos | Taxa gol | Diff | OR | p-value | Classe original | Observacao de mercado |
|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | `favorite_strength_high + favorito_perdendo_aos_cutoff` | @60 / `goal_after_60` | 13 | 10 | **76.9%** | +7.2 p.p. | 1.46 | 0.7619 | DESCARTAR | Taxa alta, mas N muito pequeno. Candidato apenas exploratorio para Back Over se odd compensar. |
| 2 | `match_balance_high + shots_last_10m_high` | @60 / `goal_after_60` | 30 | 23 | **76.7%** | +6.9 p.p. | 1.47 | 0.5347 | OBSERVAR | Melhor sinal Odds+H8 em @60. Interessante para avaliar Back Over, mas p fraco. |
| 3 | `3 gols ja marcados` | @60 / `goal_after_60` | 69 | 52 | **75.4%** | +5.6 p.p. | 1.41 | 0.3112 | OBSERVAR | Padrão simples de match state; bom N. Pode ser util para precificacao manual. |
| 4 | `visitante vencendo por 1` | @60 / `goal_after_60` | 73 | 55 | **75.3%** | +5.6 p.p. | 1.41 | 0.2609 | OBSERVAR | Forte candidato para analise de Back Over com odd real. |
| 5 | `ofensivo_forte_vs_defesa_fragil + shots_last_10m` | @60 / `target_late_goal_75` | 20 | 15 | **75.0%** | +25.0 p.p. | 3.01 | 0.0353 | OBSERVAR | Maior efeito bruto, mas N pequeno. Nao robusto depois. |
| 6 | `favorite_strength_low + shots_last_10m_high` | @60 / `goal_after_60` | 33 | 24 | **72.7%** | +3.0 p.p. | 1.17 | 0.8434 | DESCARTAR | Taxa alta mas diff pequeno vs baseline alto de goal_after_60. |
| 7 | `favorite_strength_high + favorito_vencendo_por_1_aos_cutoff` | @60 / `goal_after_60` | 35 | 25 | **71.4%** | +1.7 p.p. | 1.09 | 1.0000 | DESCARTAR | Taxa alta, mas praticamente baseline. |
| 8 | `match_balance_high + empate_aos_cutoff` | @60 / `goal_after_60` | 28 | 20 | **71.4%** | +1.7 p.p. | 1.09 | 1.0000 | DESCARTAR | N abaixo de 30 e sem edge claro. |
| 9 | `mandante vencendo por 1` | @60 / `goal_after_60` | 110 | 78 | **70.9%** | +1.2 p.p. | 1.08 | 0.8061 | DESCARTAR | Alto por baseline do cutoff, nao diferencial. |
| 10 | `0 gols ja marcados` | @60 / `goal_after_60` | 55 | 39 | **70.9%** | +1.2 p.p. | 1.07 | 0.8755 | DESCARTAR | Estado simples; nao diferencial. |
| 11 | `1 gol ja marcado` | @60 / `goal_after_60` | 127 | 90 | **70.9%** | +1.1 p.p. | 1.08 | 0.8130 | DESCARTAR | Alto N, mas efeito fraco. |
| 12 | `mandante vencendo por 2+` | @60 / `goal_after_60` | 51 | 36 | **70.6%** | +0.9 p.p. | 1.05 | 1.0000 | DESCARTAR | Quase baseline. |
| 13 | `match_balance_high + total_goals_until_cutoff_eq_2_or_3` | @60 / `goal_after_60` | 42 | 29 | **69.0%** | -0.7 p.p. | 0.96 | 1.0000 | DESCARTAR | Abaixo do baseline @60. |
| 14 | `favorite_strength_high + momentum_trend_last_10m_positive` | @60 / `goal_after_60` | 44 | 30 | **68.2%** | -1.6 p.p. | 0.92 | 0.8618 | DESCARTAR | Abaixo do baseline @60. |
| 15 | `visitante vencendo por 1` | @65 / `goal_after_65` | 72 | 49 | **68.1%** | +3.1 p.p. | 1.18 | 0.5853 | DESCARTAR | Pode interessar se odds forem altas, mas estatisticamente fraco. |
| 16 | `3 gols ja marcados` | @65 / `goal_after_65` | 68 | 46 | **67.6%** | +2.6 p.p. | 1.15 | 0.6750 | DESCARTAR | Efeito fraco. |
| 17 | `favorite_strength_high + shots_last_10m_high` | @60 / `goal_after_60` | 34 | 23 | **67.6%** | -2.1 p.p. | 0.90 | 0.8452 | DESCARTAR | Contraintuitivo: favorito forte + shots nao superou baseline. |
| 18 | `match_balance_low + shots_last_10m_high` | @60 / `goal_after_60` | 34 | 23 | **67.6%** | -2.1 p.p. | 0.90 | 0.8452 | DESCARTAR | Abaixo do baseline @60. |
| 19 | `defensivo_fragile + shots_last_10m` | @60 / `target_late_goal_75` | 52 | 34 | **65.4%** | +15.4 p.p. | 2.10 | 0.0224 | PROMISSOR inicial / OBSERVAR robustez | Forte no cutoff 60 para gol apos 75; perdeu forca em 65/70. |
| 20 | `match_balance_high + shots_last_10m_high` | @65 / `goal_after_65` | 31 | 20 | **64.5%** | -0.5 p.p. | 0.98 | 1.0000 | DESCARTAR | Sem robustez em 65. |
| 21 | `3 gols ja marcados` | @70 / `goal_after_70` | 72 | 46 | **63.9%** | +5.5 p.p. | 1.33 | 0.3528 | OBSERVAR | Bom candidato para olhar com preco/odd aos 70. |
| 22 | `visitante vencendo por 1` | @70 / `goal_after_70` | 74 | 47 | **63.5%** | +5.1 p.p. | 1.30 | 0.3588 | OBSERVAR | Candidato importante para Back Over se odd media >= break-even. |
| 23 | `favorite_strength_high + empate_aos_cutoff` | @60 / `goal_after_60` | 19 | 12 | **63.2%** | -6.6 p.p. | 0.73 | 0.6089 | DESCARTAR | N pequeno e abaixo baseline. |
| 24 | `match_balance_low + empate_aos_cutoff` | @60 / `goal_after_60` | 19 | 12 | **63.2%** | -6.6 p.p. | 0.73 | 0.6089 | DESCARTAR | N pequeno e abaixo baseline. |
| 25 | `mandante vencendo por 2+` | @70 / `goal_after_70` | 62 | 39 | **62.9%** | +4.5 p.p. | 1.25 | 0.4827 | DESCARTAR | Quase OBSERVAR, mas nao passou criterio. |
| 26 | `match_balance_high + momentum_trend_last_10m_positive` | @60 / `goal_after_60` | 44 | 27 | **61.4%** | -8.4 p.p. | 0.65 | 0.2226 | DESCARTAR | Sinal negativo para Over. |
| 27 | `1 gol ja marcado` | @70 / `goal_after_70` | 106 | 64 | **60.4%** | +2.0 p.p. | 1.12 | 0.6445 | DESCARTAR | Fraco. |
| 28 | `4+ gols ja marcados` | @60 / `goal_after_60` | 39 | 23 | **59.0%** | -10.8 p.p. | 0.59 | 0.1414 | OBSERVAR negativo | Possivel leitura Under, nao Over. |
| 29 | `0 gols ja marcados` | @70 / `goal_after_70` | 39 | 23 | **59.0%** | +0.6 p.p. | 1.03 | 1.0000 | DESCARTAR | Fraco. |
| 30 | `3 gols ja marcados` | @75 / `goal_after_75` | 85 | 49 | **57.6%** | +7.9 p.p. | 1.51 | 0.1100 | OBSERVAR | Um dos melhores em 75; interessante se odd pagar bem. |
| 31 | `match_balance_high + shots_last_10m_high` | @75 / `goal_after_75` | 26 | 15 | **57.7%** | +8.0 p.p. | 1.41 | 0.4238 | OBSERVAR | N pequeno; reaparece em 75 mas instavel. |
| 32 | `visitante vencendo por 1` | @75 / `goal_after_75` | 74 | 41 | **55.4%** | +5.7 p.p. | 1.33 | 0.3015 | OBSERVAR | Candidato para odd alta em fim de jogo. |
| 33 | `defensivo_fragile + shots_last_10m` | @65 / `target_late_goal_75` | 48 | 26 | **54.2%** | +4.2 p.p. | 1.21 | 0.6389 | OBSERVAR robustez fraca | Perdeu bastante forca vs cutoff 60. |
| 34 | `defensivo_fragile + shots_last_10m` | @70 / `target_late_goal_75` | 46 | 25 | **54.3%** | +4.3 p.p. | 1.22 | 0.6330 | OBSERVAR robustez fraca | Sinal positivo, mas fraco. |
| 35 | `favorite_side = none_clear` | pre-jogo / `target_late_goal_75` | 24 | 14 | **58.3%** | +8.6 p.p. | 1.45 | 0.4072 | OBSERVAR | N pequeno; odds pre-game isolada. |

---

# PARTE B — RANKING COM N MINIMO

## 5. Ranking de Over Candidates com N >= 30

| Rank | Padrao | Cutoff / Target | N | Taxa gol | Diff | Classe | Leitura de mercado |
|---:|---|---|---:|---:|---:|---|---|
| 1 | `match_balance_high + shots_last_10m_high` | @60 / `goal_after_60` | 30 | **76.7%** | +6.9 p.p. | OBSERVAR | Melhor candidato combinado Odds+H8 para Back Over, mas p fraco. |
| 2 | `3 gols ja marcados` | @60 / `goal_after_60` | 69 | **75.4%** | +5.6 p.p. | OBSERVAR | Padrao simples, bom N, pode ser facil de operar manualmente. |
| 3 | `visitante vencendo por 1` | @60 / `goal_after_60` | 73 | **75.3%** | +5.6 p.p. | OBSERVAR | Padrao operacional claro. |
| 4 | `favorite_strength_low + shots_last_10m_high` | @60 / `goal_after_60` | 33 | **72.7%** | +3.0 p.p. | DESCARTAR | Taxa alta mas edge fraco vs baseline. |
| 5 | `favorite_strength_high + favorito_vencendo_por_1` | @60 / `goal_after_60` | 35 | **71.4%** | +1.7 p.p. | DESCARTAR | Taxa alta mas nao diferencial. |
| 6 | `mandante vencendo por 1` | @60 / `goal_after_60` | 110 | **70.9%** | +1.2 p.p. | DESCARTAR | Muito proximo do baseline. |
| 7 | `1 gol ja marcado` | @60 / `goal_after_60` | 127 | **70.9%** | +1.1 p.p. | DESCARTAR | Alto N, baixo diferencial. |
| 8 | `0 gols ja marcados` | @60 / `goal_after_60` | 55 | **70.9%** | +1.2 p.p. | DESCARTAR | Alto por baseline do 60. |
| 9 | `defensivo_fragile + shots_last_10m` | @60 / `target_late_goal_75` | 52 | **65.4%** | +15.4 p.p. | OBSERVAR apos robustez | Forte relativo ao target 75, mas nao robusto em 65/70. |
| 10 | `visitante vencendo por 1` | @70 / `goal_after_70` | 74 | **63.5%** | +5.1 p.p. | OBSERVAR | Bom candidato de mercado aos 70 se odd >= break-even. |
| 11 | `3 gols ja marcados` | @70 / `goal_after_70` | 72 | **63.9%** | +5.5 p.p. | OBSERVAR | Similar ao visitante vencendo por 1 em 70. |
| 12 | `3 gols ja marcados` | @75 / `goal_after_75` | 85 | **57.6%** | +7.9 p.p. | OBSERVAR | Menor taxa, mas odd no mercado tende ser maior. |
| 13 | `visitante vencendo por 1` | @75 / `goal_after_75` | 74 | **55.4%** | +5.7 p.p. | OBSERVAR | Pode ter EV se odd for alta o suficiente. |

---

# PARTE C — UNDER / NO-GOAL CANDIDATES

## 6. Ranking de Sinais de Ausencia de Gol

| Rank | Padrao / variacao | Cutoff / Target | N | Taxa sem gol | Diff | OR | p-value | Classe | Uso de mercado sugerido |
|---:|---|---|---:|---:|---:|---:|---:|---|---|
| 1 | `momentum_trend_last_10m_non_positive` | @60 / `no_goal_60_75` | 197 | **66.5%** | +3.6 p.p. | 1.38 | 0.1381 | OBSERVAR | Candidato simples para Lay Over / Back Under, mas edge pequeno. |
| 2 | `cold_game_2of4` | @60 / `no_goal_60_75` | 170 | **65.9%** | +3.0 p.p. | 1.26 | 0.2876 | OBSERVAR | Combina sinais frios; bom N, mas diff pequena. |
| 3 | `shots_last_10m_low` | @60 / `no_goal_60_75` | 166 | **65.1%** | +2.2 p.p. | 1.18 | 0.4555 | DESCARTAR | Pode ser util com preco bom, mas estatisticamente fraco. |
| 4 | `xg_last_10m_low` | @60 / `no_goal_60_75` | 95 | **63.2%** | +0.3 p.p. | 1.02 | 1.0000 | DESCARTAR | Quase baseline. |
| 5 | `xg_last_10m_low` | @60 / `no_goal_60_80` | 95 | **56.8%** | +2.6 p.p. | 1.15 | 0.6345 | DESCARTAR | Fraco. |
| 6 | `momentum_trend_last_10m_non_positive` | @60 / `no_goal_60_80` | 197 | **55.3%** | +1.1 p.p. | 1.10 | 0.6808 | DESCARTAR | Fraco em janela 60-80. |
| 7 | `shots_last_10m_low` | @60 / `no_goal_60_80` | 166 | **54.8%** | +0.6 p.p. | 1.04 | 0.8364 | DESCARTAR | Quase baseline. |
| 8 | `cold_game_2of4` | @60 / `no_goal_60_80` | 170 | **54.7%** | +0.5 p.p. | 1.04 | 0.9176 | DESCARTAR | Quase baseline. |
| 9 | `momentum_last_10m_avg_low` | @60 / `no_goal_60_75` | 95 | **56.8%** | -6.1 p.p. | 0.71 | 0.1778 | DESCARTAR | Pior que baseline de no-goal. |
| 10 | `momentum_last_10m_avg_low` | @60 / `no_goal_60_80` | 95 | **47.4%** | -6.8 p.p. | 0.69 | 0.1245 | DESCARTAR | Sinal contrario ao esperado para Under. |

Leitura:

- Os melhores sinais Under ficaram em torno de 65% a 66% sem gol em 60-75.
- O baseline de `no_goal_60_75` era 62.9%, entao o ganho incremental foi pequeno.
- Mesmo assim, para trade, pode haver valor se a odd do Lay Over / Back Under for favoravel.

---

# PARTE D — H8 SHORT-TERM HOT SIGNALS

## 7. H8 Hot Signals por Janela Curta

| Padrao | Target | N | Taxa gol | Baseline | Diff | OR | p-value | Classe | Leitura |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| `shots_last_10m_high` | `goal_60_70` | 122 | 25.4% | 26.8% | -1.4 | 0.90 | 0.7110 | DESCARTAR | Nao serve para gol imediato 60-70. |
| `shots_last_10m_high` | `goal_60_75` | 122 | 36.1% | 37.1% | -1.0 | 0.94 | 0.8205 | DESCARTAR | Nao melhora 60-75. |
| `shots_last_10m_high` | `goal_60_80` | 122 | 47.5% | 45.8% | +1.8 | 1.11 | 0.6602 | DESCARTAR | Leve melhora. |
| `shots_last_10m_high` | `goal_65_80` | 122 | 41.0% | 36.8% | +4.1 | 1.30 | 0.2568 | OBSERVAR | Melhor hot signal curto; efeito atrasado. |
| `xg_last_10m_high` | `goal_60_70` | 95 | 23.2% | 26.8% | -3.7 | 0.77 | 0.4226 | DESCARTAR | Sinal negativo. |
| `xg_last_10m_high` | `goal_60_75` | 95 | 35.8% | 37.1% | -1.3 | 0.93 | 0.8069 | DESCARTAR | Fraco. |
| `xg_last_10m_high` | `goal_60_80` | 95 | 48.4% | 45.8% | +2.6 | 1.15 | 0.5549 | DESCARTAR | Leve. |
| `xg_last_10m_high` | `goal_65_80` | 95 | 40.0% | 36.8% | +3.2 | 1.20 | 0.4640 | DESCARTAR | Leve. |
| `momentum_trend_last_10m_positive` | `goal_60_70` | 182 | 30.8% | 26.8% | +3.9 | 1.47 | 0.1057 | OBSERVAR | Quase relevante para gol imediato. |
| `momentum_trend_last_10m_positive` | `goal_60_75` | 182 | 41.2% | 37.1% | +4.1 | 1.40 | 0.1366 | OBSERVAR | Melhor sinal conceitual para Over curto. |
| `momentum_trend_last_10m_positive` | `goal_60_80` | 182 | 47.3% | 45.8% | +1.5 | 1.12 | 0.6073 | DESCARTAR | Fraco. |
| `momentum_trend_last_10m_positive` | `goal_65_80` | 182 | 39.0% | 36.8% | +2.2 | 1.20 | 0.4563 | DESCARTAR | Fraco. |
| `momentum_last_10m_avg_high` | `goal_60_70` | 95 | 26.3% | 26.8% | -0.5 | 0.96 | 1.0000 | DESCARTAR | Fraco. |
| `momentum_last_10m_avg_high` | `goal_60_75` | 95 | 33.7% | 37.1% | -3.4 | 0.82 | 0.4632 | DESCARTAR | Sinal contrario. |
| `momentum_last_10m_avg_high` | `goal_60_80` | 95 | 41.1% | 45.8% | -4.7 | 0.77 | 0.3416 | DESCARTAR | Sinal contrario. |
| `momentum_last_10m_avg_high` | `goal_65_80` | 95 | 33.7% | 36.8% | -3.2 | 0.83 | 0.5394 | DESCARTAR | Sinal contrario. |
| `hot_game_2of4` | `goal_60_70` | 148 | 26.4% | 26.8% | -0.5 | 0.96 | 0.9058 | DESCARTAR | Quase baseline. |
| `hot_game_2of4` | `goal_60_75` | 148 | 35.8% | 37.1% | -1.3 | 0.91 | 0.7441 | DESCARTAR | Fraco. |
| `hot_game_2of4` | `goal_60_80` | 148 | 45.9% | 45.8% | +0.2 | 1.01 | 1.0000 | DESCARTAR | Baseline. |
| `hot_game_2of4` | `goal_65_80` | 148 | 38.5% | 36.8% | +1.7 | 1.12 | 0.6628 | DESCARTAR | Fraco. |

---

# PARTE E — ODDS ISOLADAS

## 8. Odds Pre-Jogo Isoladas contra `target_late_goal_75`

| Padrao | N | Taxa gol | Diff | OR | p-value | Classe | Observacao |
|---|---:|---:|---:|---:|---:|---|---|
| `favorite_side = none_clear` | 24 | **58.3%** | +8.6 p.p. | 1.45 | 0.4072 | OBSERVAR | N pequeno; possivel proxy de jogo equilibrado. |
| `implied_prob_over25_norm bottom25` | 95 | **53.7%** | +3.9 p.p. | 1.23 | 0.4078 | DESCARTAR | Contraintuitivo: menor expectativa de over teve taxa maior. |
| `over25_closing_strength bottom25` | 95 | **53.7%** | +3.9 p.p. | 1.23 | 0.4078 | DESCARTAR | Mesmo comportamento do item anterior. |
| `match_balance top25` | 95 | **53.7%** | +3.9 p.p. | 1.23 | 0.4078 | DESCARTAR | Pode servir como moderador. |
| `favorite_side = away` | 127 | **52.0%** | +2.2 p.p. | 1.14 | 0.5869 | DESCARTAR | Fraco. |
| `favorite_strength bottom25` | 95 | **52.6%** | +2.9 p.p. | 1.17 | 0.5544 | DESCARTAR | Fraco. |
| `implied_prob_over25_norm top25` | 96 | **46.9%** | -2.9 p.p. | 0.86 | 0.5558 | DESCARTAR | Over pre-jogo forte nao ajudou. |
| `over25_closing_strength top25` | 96 | **46.9%** | -2.9 p.p. | 0.86 | 0.5558 | DESCARTAR | Over pre-jogo forte nao ajudou. |
| `favorite_strength top25` | 95 | **45.3%** | -4.5 p.p. | 0.79 | 0.3441 | OBSERVAR negativo | Favoritos fortes tiveram menos gol tardio. |
| `match_balance bottom25` | 95 | **45.3%** | -4.5 p.p. | 0.79 | 0.3441 | OBSERVAR negativo | Jogos desequilibrados menos propensos. |

---

# PARTE F — PADROES COM LEITURA DE MERCADO

## 9. Candidatos para Back Over +1 Gol

Ordem sugerida para analise manual de mercado:

| Prioridade | Padrao | Motivo | Cuidado |
|---:|---|---|---|
| 1 | `visitante vencendo por 1 @70` | N=74, taxa 63.5%, odd aos 70 pode pagar melhor. | Precisa odd media real; exemplo @1.70 deu EV positivo bruto. |
| 2 | `3 gols ja marcados @70` | N=72, taxa 63.9%, sinal similar ao visitante vencendo por 1. | Pode depender do placar exato e ritmo. |
| 3 | `match_balance_high + shots_last_10m_high @60` | Taxa 76.7%, melhor combinado Odds+H8. | N=30 e p-value fraco. |
| 4 | `visitante vencendo por 1 @60` | Taxa 75.3%, N=73. | Odd @60 pode ser baixa demais. |
| 5 | `3 gols ja marcados @60` | Taxa 75.4%, N=69. | Odd @60 pode nao compensar. |
| 6 | `defensivo_fragile + shots_last_10m @60` | Taxa 65.4% para late goal 75, OR 2.10 inicial. | Robustez caiu em 65/70; target diferente. |
| 7 | `3 gols ja marcados @75` | Taxa 57.6%, diff +7.9. | Odd pode ser bem maior; precisa preco real. |
| 8 | `visitante vencendo por 1 @75` | Taxa 55.4%, diff +5.7. | Boa para estudar preco alto no fim. |

---

## 10. Candidatos para Lay Over / Back Under

Ordem sugerida para analise manual de mercado:

| Prioridade | Padrao | Motivo | Cuidado |
|---:|---|---|---|
| 1 | `momentum_trend_last_10m_non_positive @60 -> no_goal_60_75` | N=197, taxa sem gol 66.5%. | Diff vs baseline pequena (+3.6 p.p.). |
| 2 | `cold_game_2of4 @60 -> no_goal_60_75` | N=170, taxa sem gol 65.9%. | Diff pequena (+3.0 p.p.). |
| 3 | `shots_last_10m_low @60 -> no_goal_60_75` | N=166, taxa sem gol 65.1%. | Classificado DESCARTAR estatisticamente. |
| 4 | `4+ gols ja marcados @60` | Taxa de gol depois do 60 abaixo do baseline, 59.0% vs 69.7%. | E um sinal de menor gol, nao no-goal puro. |
| 5 | `visitante vencendo por 2+ @60` | Taxa de gol 58.5%, -11.2 p.p. vs baseline. | Pode ser bom para Under se odd permitir; precisa simular. |
| 6 | `momentum_last_10m_avg_low` | Sinal esperado de jogo morno. | Nos testes foi pior que baseline para no-goal, entao cuidado. |

---

# PARTE G — OBSERVACOES IMPORTANTES PARA SUA ANALISE DE MERCADO

## 11. O que a pesquisa mostrou ate agora

1. Padroes com maior taxa de gol aparecem majoritariamente no cutoff 60.
2. Alguns padroes em 70 tem taxa menor, mas podem pagar odds melhores.
3. A taxa isolada nao decide valor.
4. O mercado provavelmente vai precificar muitos sinais obvios.
5. Onde pode haver valor:
   - padroes com taxa moderada mas odd alta;
   - padroes com taxa alta mas odd ainda aceitavel;
   - Lay Over quando o break-even da odd for menor que a taxa real de sem gol;
   - Back Over quando a taxa real de gol for maior que o break-even da odd.

---

## 12. Formulas para analise manual de EV

### Back Over

```text
break_even = 1 / odd_back
EV_por_100 = P(gol) * ((odd - 1) * 100) - P(sem_gol) * 100
```

Exemplo:

```text
Back Over @1.70 precisa de 58.8% de gol.
```

### Lay Over

```text
responsabilidade = stake * (odd_lay - 1)
break_even_sem_gol = responsabilidade / (stake + responsabilidade)
EV_por_100 = P(sem_gol) * 100 - P(gol) * responsabilidade
```

Exemplo:

```text
Lay Over @1.70 precisa de 41.2% sem gol.
```

---

## 13. Proximos estudos sugeridos

### Estudo 1 — Market Price Sensitivity

Criar matriz para cada padrao:

- odd 1.30;
- odd 1.50;
- odd 1.70;
- odd 1.80;
- odd 2.00;
- odd 2.20.

Calcular:

- break-even;
- EV por R$100;
- ROI esperado;
- lucro/prejuizo teorico.

### Estudo 2 — Trade Timing

Avaliar janelas:

- 60-70;
- 60-75;
- 65-75;
- 65-80;
- 70-80;
- 70-85;
- 70-90.

### Estudo 3 — Separar Over vs Under

Dois rankings separados:

- Back Over candidates;
- Lay Over / Back Under candidates.

### Estudo 4 — Adicionar odds live reais

Somente futuro, se houver fonte confiavel com timestamp.

---

## 14. Decisao Quant

Este documento nao aprova nenhuma estrategia.

Ele consolida os padroes ja testados para analise de mercado.

Conclusao:

```text
O proximo passo mais util nao e testar mais padroes cegamente.
O proximo passo e simular EV por faixa de odd para os padroes deste ranking.
```

Recomendacao:

```text
Criar MARKET_PRICE_SENSITIVITY_PLAN_V1.md
```

Objetivo:

- transformar taxa de gol/no-goal em lucro esperado por odd;
- comparar Back Over e Lay Over;
- priorizar padroes por EV teorico, nao apenas taxa de acerto.
