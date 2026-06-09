# H8_COMPOSITE_PRESSURE_SCORE_RESULTS_V1

## Resumo Executivo

- Validacao exploratoria executada conforme `docs/04_RESEARCH/H8_COMPOSITE_PRESSURE_SCORE_PLAN_V1.md`.
- Scores compostos usam shotmap/xG + graph momentum agregado, nunca graph por equipe.
- Pesos fixos foram usados sem ajuste por target.
- Nenhum modelo, baseline preditivo, backtesting financeiro real, producao, schema, banco, crawler ou importer foi alterado.
- Amostra: 380 partidas e 1520 linhas match_id + cutoff.
- Resultados com dados disponiveis: 5040.
- Classes: {'DESCARTAR_ESTATISTICO_LOCAL': 3837, 'OBSERVAR': 813, 'MICRO_AMOSTRA_REPLICAR': 304, 'NAO_DISPONIVEL_V1': 210, 'PROMISSOR_LOCAL': 86}.
- Melhor ranking @70: `favorite_losing_by_1 + h8_hot_combo_10m_3of3` / `no_goal_after_cutoff` com N=2, taxa=100.0%, diff=+58.4 p.p., OR=7.11.

## Definicao Dos Scores Compostos

- `h8_hot_combo_10m_count`: soma de shots high, xG high e momentum trend positivo.
- `h8_cold_combo_10m_count`: soma de shots low, xG low e momentum trend nao positivo.
- `h8_pressure_score_10m`: `0.30*shots_z + 0.35*xg_z + 0.20*momentum_avg_z + 0.15*momentum_trend_score`.
- `h8_shot_quality_score_10m`: `0.45*shots_z + 0.55*xg_z`.
- `h8_graph_momentum_score_10m`: `0.60*momentum_avg_z + 0.40*momentum_trend_score`.
- `h8_conservative_hot_10m`: shots high AND xG high AND momentum trend positivo.
- `h8_graph_only_pressure_10m`: momentum trend positivo AND shots low.
- xGOT opcional: NAO_DISPONIVEL_V1: xGOT nao esta no Dataset H8 V1 validado; raw shotmap possui xgot, mas nao foi integrado a esta V1.

## Confirmacao Anti-Leakage

- Features usam somente informacoes ate o cutoff.
- Graph e momentum sao usados apenas como pressao agregada da partida.
- Nao foi inferida pressao por time via graph.
- Placar final e gols futuros nao foram usados como features.
- Pesos dos scores nao foram ajustados pelo target.
- Odds live nao foram usadas.
- Cutoff 80 foi reportado como `NAO_DISPONIVEL_V1`, pois nao existe no Dataset H8 V1 atual.

## Ranking Estatistico Geral

| variation | cutoff | target | N | rate | baseline | diff | OR | p | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_conservative_hot_10m | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_after_cutoff | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_75_90 | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_after_cutoff | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_75_90 | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | goal_70_80 | 7 | 71.4% | 27.1% | +44.3 | 7.02 | 0.0175 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_70 | 10 | 70.0% | 26.8% | +43.2 | 6.75 | 0.0049 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_70 | 10 | 70.0% | 26.8% | +43.2 | 6.75 | 0.0049 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_75 | 10 | 80.0% | 37.1% | +42.9 | 7.13 | 0.0066 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_75 | 10 | 80.0% | 37.1% | +42.9 | 7.13 | 0.0066 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_graph_momentum_bottom25 | 70 | goal_after_cutoff | 8 | 100.0% | 58.4% | +41.6 | 12.56 | 0.0231 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_graph_momentum_bottom25 | 70 | goal_after_cutoff | 8 | 100.0% | 58.4% | +41.6 | 12.56 | 0.0231 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | no_goal_65_80 | 4 | 100.0% | 63.2% | +36.8 | 5.35 | 0.3012 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | no_goal_65_80 | 4 | 100.0% | 63.2% | +36.8 | 5.35 | 0.3012 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_85 | 8 | 75.0% | 38.2% | +36.8 | 5.03 | 0.0582 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_85 | 8 | 75.0% | 38.2% | +36.8 | 5.03 | 0.0582 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_80 | 8 | 62.5% | 27.1% | +35.4 | 4.66 | 0.0367 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_80 | 8 | 62.5% | 27.1% | +35.4 | 4.66 | 0.0367 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_graph_only_pressure_10m | 65 | goal_after_cutoff | 11 | 100.0% | 65.0% | +35.0 | 12.98 | 0.0098 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | goal_after_cutoff | 4 | 100.0% | 65.0% | +35.0 | 4.93 | 0.3023 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | goal_after_cutoff | 4 | 100.0% | 65.0% | +35.0 | 4.93 | 0.3023 | MICRO_AMOSTRA_REPLICAR |
| match_balance_high + h8_hot_combo_10m_3of3 | 65 | goal_after_cutoff | 4 | 100.0% | 65.0% | +35.0 | 4.93 | 0.3023 | MICRO_AMOSTRA_REPLICAR |
| match_balance_high + h8_conservative_hot_10m | 65 | goal_after_cutoff | 4 | 100.0% | 65.0% | +35.0 | 4.93 | 0.3023 | MICRO_AMOSTRA_REPLICAR |

## Ranking @70

| variation | cutoff | target | N | rate | baseline | diff | OR | p | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_conservative_hot_10m | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | goal_70_80 | 7 | 71.4% | 27.1% | +44.3 | 7.02 | 0.0175 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_graph_momentum_bottom25 | 70 | goal_after_cutoff | 8 | 100.0% | 58.4% | +41.6 | 12.56 | 0.0231 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_graph_momentum_bottom25 | 70 | goal_after_cutoff | 8 | 100.0% | 58.4% | +41.6 | 12.56 | 0.0231 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_85 | 8 | 75.0% | 38.2% | +36.8 | 5.03 | 0.0582 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_85 | 8 | 75.0% | 38.2% | +36.8 | 5.03 | 0.0582 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_80 | 8 | 62.5% | 27.1% | +35.4 | 4.66 | 0.0367 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_80 | 8 | 62.5% | 27.1% | +35.4 | 4.66 | 0.0367 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_85 | 7 | 71.4% | 38.2% | +33.3 | 4.16 | 0.1110 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | goal_70_85 | 7 | 71.4% | 38.2% | +33.3 | 4.16 | 0.1110 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_85 | 7 | 71.4% | 38.2% | +33.3 | 4.16 | 0.1110 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_shot_quality_bottom25 | 70 | goal_70_80 | 15 | 60.0% | 27.1% | +32.9 | 4.32 | 0.0064 | PROMISSOR_LOCAL |
| favorite_strength_low + h8_graph_only_pressure_10m | 70 | goal_70_80 | 17 | 58.8% | 27.1% | +31.7 | 4.15 | 0.0049 | PROMISSOR_LOCAL |
| favorite_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | goal_70_80 | 14 | 57.1% | 27.1% | +30.0 | 3.80 | 0.0262 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_80 | 7 | 57.1% | 27.1% | +30.0 | 3.69 | 0.0897 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_80 | 7 | 57.1% | 27.1% | +30.0 | 3.69 | 0.0897 | MICRO_AMOSTRA_REPLICAR |
| match_balance_high + h8_graph_only_pressure_10m | 70 | goal_70_80 | 16 | 56.2% | 27.1% | +29.1 | 3.69 | 0.0170 | PROMISSOR_LOCAL |
| favorite_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_after_cutoff | 8 | 87.5% | 58.4% | +29.1 | 5.11 | 0.1468 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_conservative_hot_10m | 70 | goal_after_cutoff | 8 | 87.5% | 58.4% | +29.1 | 5.11 | 0.1468 | MICRO_AMOSTRA_REPLICAR |
| team_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_80 | 11 | 54.5% | 27.1% | +27.4 | 3.36 | 0.0765 | MICRO_AMOSTRA_REPLICAR |
| team_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_80 | 11 | 54.5% | 27.1% | +27.4 | 3.36 | 0.0765 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_80 | 2 | 100.0% | 72.9% | +27.1 | 1.88 | 1.0000 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_80 | 2 | 100.0% | 72.9% | +27.1 | 1.88 | 1.0000 | MICRO_AMOSTRA_REPLICAR |

## Ranking Back Over Sem Cashout

| variation | cutoff | target | N | p_goal | odd | hold_ev | cashout_ev | lay_ev | preferred |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| favorite_losing_by_1 + h8_graph_momentum_bottom25 | 70 | goal_after_cutoff | 8 | 100.0% | 1.70 | 70.00 | NA | -70.00 | Back Over |
| favorite_losing_by_1 + h8_graph_momentum_bottom25 | 70 | no_goal_after_cutoff | 8 | 100.0% | 1.70 | 70.00 | NA | -70.00 | Back Over |
| underdog_winning_by_1 + h8_graph_momentum_bottom25 | 70 | goal_after_cutoff | 8 | 100.0% | 1.70 | 70.00 | NA | -70.00 | Back Over |
| underdog_winning_by_1 + h8_graph_momentum_bottom25 | 70 | no_goal_after_cutoff | 8 | 100.0% | 1.70 | 70.00 | NA | -70.00 | Back Over |
| total_goals_3plus + h8_hot_combo_10m_3of3 | 75 | goal_after_cutoff | 14 | 78.6% | 2.00 | 57.14 | NA | -57.14 | Back Over |
| total_goals_3plus + h8_hot_combo_10m_3of3 | 75 | no_goal_after_cutoff | 14 | 78.6% | 2.00 | 57.14 | NA | -57.14 | Back Over |
| total_goals_3plus + h8_hot_combo_10m_3of3 | 75 | goal_75_90 | 14 | 78.6% | 2.00 | 57.14 | NA | -57.14 | Back Over |
| total_goals_3plus + h8_hot_combo_10m_3of3 | 75 | no_goal_75_90 | 14 | 78.6% | 2.00 | 57.14 | NA | -57.14 | Back Over |
| total_goals_3plus + h8_conservative_hot_10m | 75 | goal_after_cutoff | 14 | 78.6% | 2.00 | 57.14 | NA | -57.14 | Back Over |
| total_goals_3plus + h8_conservative_hot_10m | 75 | no_goal_after_cutoff | 14 | 78.6% | 2.00 | 57.14 | NA | -57.14 | Back Over |
| total_goals_3plus + h8_conservative_hot_10m | 75 | goal_75_90 | 14 | 78.6% | 2.00 | 57.14 | NA | -57.14 | Back Over |
| total_goals_3plus + h8_conservative_hot_10m | 75 | no_goal_75_90 | 14 | 78.6% | 2.00 | 57.14 | NA | -57.14 | Back Over |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | goal_after_cutoff | 4 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | no_goal_after_cutoff | 4 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | goal_after_cutoff | 4 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | no_goal_after_cutoff | 4 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |
| away_winning_by_1 + h8_graph_only_pressure_10m | 65 | goal_after_cutoff | 11 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |
| away_winning_by_1 + h8_graph_only_pressure_10m | 65 | no_goal_after_cutoff | 11 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 65 | goal_after_cutoff | 2 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 65 | no_goal_after_cutoff | 2 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |
| favorite_losing_by_1 + h8_conservative_hot_10m | 65 | goal_after_cutoff | 2 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |
| favorite_losing_by_1 + h8_conservative_hot_10m | 65 | no_goal_after_cutoff | 2 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |
| underdog_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | goal_after_cutoff | 2 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |
| underdog_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | no_goal_after_cutoff | 2 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |
| underdog_winning_by_1 + h8_conservative_hot_10m | 65 | goal_after_cutoff | 2 | 100.0% | 1.50 | 50.00 | NA | -50.00 | Back Over |

## Ranking Back Over Com Cashout

| variation | cutoff | target | N | p_goal | odd | hold_ev | cashout_ev | lay_ev | preferred |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| away_winning_by_1 + h8_graph_momentum_bottom25 | 75 | goal_75_85 | 10 | 60.0% | 2.00 | 20.00 | 47.59 | -20.00 | Back Over |
| away_winning_by_1 + h8_graph_momentum_bottom25 | 75 | no_goal_75_85 | 10 | 60.0% | 2.00 | 20.00 | 47.59 | -20.00 | Back Over |
| total_goals_3 + h8_graph_only_pressure_10m | 75 | goal_75_85 | 5 | 60.0% | 2.00 | 20.00 | 47.59 | -20.00 | Back Over |
| total_goals_3 + h8_graph_only_pressure_10m | 75 | no_goal_75_85 | 5 | 60.0% | 2.00 | 20.00 | 47.59 | -20.00 | Back Over |
| favorite_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_85 | 8 | 75.0% | 1.70 | 27.50 | 42.16 | -27.50 | Back Over |
| favorite_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_85 | 8 | 75.0% | 1.70 | 27.50 | 42.16 | -27.50 | Back Over |
| favorite_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_85 | 8 | 75.0% | 1.70 | 27.50 | 42.16 | -27.50 | Back Over |
| favorite_winning_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_85 | 8 | 75.0% | 1.70 | 27.50 | 42.16 | -27.50 | Back Over |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_85 | 7 | 71.4% | 1.70 | 21.43 | 38.18 | -21.43 | Back Over |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_85 | 7 | 71.4% | 1.70 | 21.43 | 38.18 | -21.43 | Back Over |
| away_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | goal_70_85 | 7 | 71.4% | 1.70 | 21.43 | 38.18 | -21.43 | Back Over |
| away_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | no_goal_70_85 | 7 | 71.4% | 1.70 | 21.43 | 38.18 | -21.43 | Back Over |
| away_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_85 | 7 | 71.4% | 1.70 | 21.43 | 38.18 | -21.43 | Back Over |
| away_winning_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_85 | 7 | 71.4% | 1.70 | 21.43 | 38.18 | -21.43 | Back Over |
| total_goals_3 + h8_cold_combo_10m_3of3 | 75 | goal_75_85 | 6 | 50.0% | 2.00 | 0.00 | 34.48 | 0.00 | Neutro |
| total_goals_3 + h8_cold_combo_10m_3of3 | 75 | no_goal_75_85 | 6 | 50.0% | 2.00 | 0.00 | 34.48 | 0.00 | Neutro |
| total_goals_3plus + h8_graph_only_pressure_10m | 75 | goal_75_85 | 14 | 50.0% | 2.00 | 0.00 | 34.48 | 0.00 | Neutro |
| total_goals_3plus + h8_graph_only_pressure_10m | 75 | no_goal_75_85 | 14 | 50.0% | 2.00 | 0.00 | 34.48 | 0.00 | Neutro |
| favorite_strength_low + h8_graph_only_pressure_10m | 70 | goal_70_85 | 17 | 64.7% | 1.70 | 10.00 | 30.69 | -10.00 | Back Over |
| favorite_strength_low + h8_graph_only_pressure_10m | 70 | no_goal_70_85 | 17 | 64.7% | 1.70 | 10.00 | 30.69 | -10.00 | Back Over |
| total_goals_3 + h8_shot_quality_bottom25 | 75 | goal_75_85 | 15 | 46.7% | 2.00 | -6.67 | 30.11 | 6.67 | Lay Over / Back Under |
| total_goals_3 + h8_shot_quality_bottom25 | 75 | no_goal_75_85 | 15 | 46.7% | 2.00 | -6.67 | 30.11 | 6.67 | Lay Over / Back Under |
| team_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_85 | 11 | 63.6% | 1.70 | 8.18 | 29.50 | -8.18 | Back Over |
| team_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_85 | 11 | 63.6% | 1.70 | 8.18 | 29.50 | -8.18 | Back Over |
| team_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_85 | 11 | 63.6% | 1.70 | 8.18 | 29.50 | -8.18 | Back Over |

## Ranking Lay Over / Back Under

| variation | cutoff | target | N | p_goal | odd | hold_ev | cashout_ev | lay_ev | preferred |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | goal_65_75 | 4 | 0.0% | 1.50 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | no_goal_65_75 | 4 | 0.0% | 1.50 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | goal_65_80 | 4 | 0.0% | 1.50 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | no_goal_65_80 | 4 | 0.0% | 1.50 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | goal_65_75 | 4 | 0.0% | 1.50 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | no_goal_65_75 | 4 | 0.0% | 1.50 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | goal_65_80 | 4 | 0.0% | 1.50 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | no_goal_65_80 | 4 | 0.0% | 1.50 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| match_balance_high + h8_cold_combo_10m_3of3 | 65 | goal_65_75 | 11 | 0.0% | 1.50 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| match_balance_high + h8_cold_combo_10m_3of3 | 65 | no_goal_65_75 | 11 | 0.0% | 1.50 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| favorite_strength_low + h8_cold_combo_10m_3of3 | 65 | goal_65_75 | 10 | 0.0% | 1.50 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| favorite_strength_low + h8_cold_combo_10m_3of3 | 65 | no_goal_65_75 | 10 | 0.0% | 1.50 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_after_cutoff | 2 | 0.0% | 1.70 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_after_cutoff | 2 | 0.0% | 1.70 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_80 | 2 | 0.0% | 1.70 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_80 | 2 | 0.0% | 1.70 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_85 | 2 | 0.0% | 1.70 | -100.00 | -41.38 | 100.00 | Lay Over / Back Under |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_85 | 2 | 0.0% | 1.70 | -100.00 | -41.38 | 100.00 | Lay Over / Back Under |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | goal_after_cutoff | 2 | 0.0% | 1.70 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_after_cutoff | 2 | 0.0% | 1.70 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | goal_70_80 | 2 | 0.0% | 1.70 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_80 | 2 | 0.0% | 1.70 | -100.00 | NA | 100.00 | Lay Over / Back Under |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | goal_70_85 | 2 | 0.0% | 1.70 | -100.00 | -41.38 | 100.00 | Lay Over / Back Under |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_85 | 2 | 0.0% | 1.70 | -100.00 | -41.38 | 100.00 | Lay Over / Back Under |
| underdog_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_after_cutoff | 2 | 0.0% | 1.70 | -100.00 | NA | 100.00 | Lay Over / Back Under |

## Comparacao Scores Compostos vs Variaveis Isoladas

### Top Scores Compostos

| variation | cutoff | target | N | rate | baseline | diff | OR | p | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_conservative_hot_10m | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_after_cutoff | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_75_90 | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_after_cutoff | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_75_90 | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | goal_70_80 | 7 | 71.4% | 27.1% | +44.3 | 7.02 | 0.0175 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_70 | 10 | 70.0% | 26.8% | +43.2 | 6.75 | 0.0049 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_70 | 10 | 70.0% | 26.8% | +43.2 | 6.75 | 0.0049 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_75 | 10 | 80.0% | 37.1% | +42.9 | 7.13 | 0.0066 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_75 | 10 | 80.0% | 37.1% | +42.9 | 7.13 | 0.0066 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_graph_momentum_bottom25 | 70 | goal_after_cutoff | 8 | 100.0% | 58.4% | +41.6 | 12.56 | 0.0231 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_graph_momentum_bottom25 | 70 | goal_after_cutoff | 8 | 100.0% | 58.4% | +41.6 | 12.56 | 0.0231 | MICRO_AMOSTRA_REPLICAR |

### Top Variaveis Isoladas De Referencia

| variation | cutoff | target | N | rate | baseline | diff | OR | p | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| isolated_shots_last_10m_high | 65 | goal_65_75 | 127 | 33.1% | 26.8% | +6.2 | 1.59 | 0.0653 | OBSERVAR |
| isolated_xg_last_10m_low | 60 | goal_after_cutoff | 95 | 75.8% | 69.7% | +6.1 | 1.49 | 0.1568 | OBSERVAR |
| isolated_xg_last_10m_high | 75 | goal_75_85 | 95 | 32.6% | 26.6% | +6.1 | 1.49 | 0.1404 | OBSERVAR |
| isolated_xg_last_10m_high | 75 | goal_after_cutoff | 95 | 55.8% | 49.7% | +6.1 | 1.38 | 0.1931 | OBSERVAR |
| isolated_xg_last_10m_high | 75 | goal_75_90 | 95 | 55.8% | 49.7% | +6.1 | 1.38 | 0.1931 | OBSERVAR |
| isolated_xg_last_10m_low | 65 | no_goal_65_75 | 95 | 78.9% | 73.2% | +5.8 | 1.51 | 0.1809 | OBSERVAR |
| isolated_momentum_trend_positive | 65 | goal_65_80 | 176 | 42.0% | 36.8% | +5.2 | 1.52 | 0.0554 | OBSERVAR |
| isolated_momentum_trend_non_positive | 65 | no_goal_65_80 | 203 | 67.5% | 63.2% | +4.3 | 1.49 | 0.0701 | DESCARTAR_ESTATISTICO_LOCAL |
| isolated_xg_last_10m_high | 65 | goal_65_80 | 95 | 41.1% | 36.8% | +4.2 | 1.27 | 0.3289 | DESCARTAR_ESTATISTICO_LOCAL |
| isolated_momentum_trend_positive | 60 | goal_60_75 | 182 | 41.2% | 37.1% | +4.1 | 1.40 | 0.1366 | DESCARTAR_ESTATISTICO_LOCAL |
| isolated_shots_last_10m_high | 65 | goal_65_80 | 127 | 40.9% | 36.8% | +4.1 | 1.30 | 0.2604 | DESCARTAR_ESTATISTICO_LOCAL |
| isolated_shots_last_10m_high | 70 | no_goal_70_80 | 117 | 76.9% | 72.9% | +4.0 | 1.35 | 0.2621 | DESCARTAR_ESTATISTICO_LOCAL |
| isolated_xg_last_10m_low | 65 | no_goal_after_cutoff | 95 | 38.9% | 35.0% | +3.9 | 1.26 | 0.3852 | DESCARTAR_ESTATISTICO_LOCAL |
| isolated_xg_last_10m_high | 70 | goal_70_85 | 95 | 42.1% | 38.2% | +3.9 | 1.25 | 0.3940 | DESCARTAR_ESTATISTICO_LOCAL |
| isolated_momentum_trend_positive | 60 | goal_60_70 | 182 | 30.8% | 26.8% | +3.9 | 1.47 | 0.1057 | DESCARTAR_ESTATISTICO_LOCAL |

## Padroes Com Visitante Vencendo Por 1

| variation | cutoff | target | N | rate | baseline | diff | OR | p | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| away_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | goal_70_80 | 7 | 71.4% | 27.1% | +44.3 | 7.02 | 0.0175 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | no_goal_65_80 | 4 | 100.0% | 63.2% | +36.8 | 5.35 | 0.3012 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | no_goal_65_80 | 4 | 100.0% | 63.2% | +36.8 | 5.35 | 0.3012 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_graph_only_pressure_10m | 65 | goal_after_cutoff | 11 | 100.0% | 65.0% | +35.0 | 12.98 | 0.0098 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | goal_after_cutoff | 4 | 100.0% | 65.0% | +35.0 | 4.93 | 0.3023 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | goal_after_cutoff | 4 | 100.0% | 65.0% | +35.0 | 4.93 | 0.3023 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_graph_momentum_bottom25 | 75 | goal_75_85 | 10 | 60.0% | 26.6% | +33.4 | 4.34 | 0.0250 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_85 | 7 | 71.4% | 38.2% | +33.3 | 4.16 | 0.1110 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | goal_70_85 | 7 | 71.4% | 38.2% | +33.3 | 4.16 | 0.1110 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_85 | 7 | 71.4% | 38.2% | +33.3 | 4.16 | 0.1110 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_shot_quality_bottom25 | 70 | goal_70_80 | 15 | 60.0% | 27.1% | +32.9 | 4.32 | 0.0064 | PROMISSOR_LOCAL |
| away_winning_by_1 + h8_cold_combo_10m_3of3 | 60 | goal_after_cutoff | 10 | 100.0% | 69.7% | +30.3 | 9.49 | 0.0360 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_80 | 7 | 57.1% | 27.1% | +30.0 | 3.69 | 0.0897 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_80 | 7 | 57.1% | 27.1% | +30.0 | 3.69 | 0.0897 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_pressure_score_10m_top33 | 65 | no_goal_65_80 | 23 | 91.3% | 63.2% | +28.1 | 6.62 | 0.0031 | PROMISSOR_LOCAL |
| away_winning_by_1 + h8_shot_quality_top25 | 65 | no_goal_65_80 | 20 | 90.0% | 63.2% | +26.8 | 5.59 | 0.0088 | PROMISSOR_LOCAL |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | no_goal_65_75 | 4 | 100.0% | 73.2% | +26.8 | 3.36 | 0.5775 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | no_goal_65_75 | 4 | 100.0% | 73.2% | +26.8 | 3.36 | 0.5775 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_graph_only_pressure_10m | 65 | goal_65_80 | 11 | 63.6% | 36.8% | +26.8 | 3.11 | 0.1078 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_pressure_score_10m_top25 | 65 | no_goal_65_80 | 19 | 89.5% | 63.2% | +26.3 | 5.26 | 0.0141 | PROMISSOR_LOCAL |

## Padroes Com Mandante Vencendo Por 1

| variation | cutoff | target | N | rate | baseline | diff | OR | p | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| home_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | goal_65_80 | 7 | 71.4% | 36.8% | +34.6 | 4.41 | 0.1058 | MICRO_AMOSTRA_REPLICAR |
| home_winning_by_1 + h8_conservative_hot_10m | 65 | goal_65_80 | 7 | 71.4% | 36.8% | +34.6 | 4.41 | 0.1058 | MICRO_AMOSTRA_REPLICAR |
| home_winning_by_1 + h8_shot_quality_top25 | 65 | goal_65_80 | 20 | 70.0% | 36.8% | +33.2 | 4.33 | 0.0031 | PROMISSOR_LOCAL |
| home_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | goal_65_75 | 7 | 57.1% | 26.8% | +30.3 | 3.74 | 0.0869 | MICRO_AMOSTRA_REPLICAR |
| home_winning_by_1 + h8_conservative_hot_10m | 65 | goal_65_75 | 7 | 57.1% | 26.8% | +30.3 | 3.74 | 0.0869 | MICRO_AMOSTRA_REPLICAR |
| home_winning_by_1 + h8_pressure_score_10m_top25 | 65 | goal_65_80 | 23 | 65.2% | 36.8% | +28.4 | 3.48 | 0.0062 | PROMISSOR_LOCAL |
| home_winning_by_1 + h8_shot_quality_top25 | 65 | goal_65_75 | 20 | 55.0% | 26.8% | +28.2 | 3.61 | 0.0074 | PROMISSOR_LOCAL |
| home_winning_by_1 + h8_hot_combo_10m_3of3 | 75 | no_goal_75_85 | 5 | 100.0% | 73.4% | +26.6 | 4.07 | 0.3308 | MICRO_AMOSTRA_REPLICAR |
| home_winning_by_1 + h8_conservative_hot_10m | 75 | no_goal_75_85 | 5 | 100.0% | 73.4% | +26.6 | 4.07 | 0.3308 | MICRO_AMOSTRA_REPLICAR |
| home_winning_by_1 + h8_pressure_score_10m_top25 | 65 | goal_65_75 | 23 | 52.2% | 26.8% | +25.3 | 3.24 | 0.0074 | PROMISSOR_LOCAL |
| home_winning_by_1 + h8_cold_combo_10m_3of3 | 65 | no_goal_after_cutoff | 17 | 58.8% | 35.0% | +23.8 | 2.79 | 0.0649 | PROMISSOR_LOCAL |
| home_winning_by_1 + h8_cold_combo_10m_3of3 | 60 | goal_after_cutoff | 14 | 92.9% | 69.7% | +23.1 | 5.88 | 0.0733 | MICRO_AMOSTRA_REPLICAR |
| home_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_80 | 4 | 50.0% | 27.1% | +22.9 | 2.72 | 0.2973 | MICRO_AMOSTRA_REPLICAR |
| home_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_80 | 4 | 50.0% | 27.1% | +22.9 | 2.72 | 0.2973 | MICRO_AMOSTRA_REPLICAR |
| home_winning_by_1 + h8_cold_combo_10m_3of3 | 60 | no_goal_60_75 | 14 | 85.7% | 62.9% | +22.8 | 3.67 | 0.0919 | MICRO_AMOSTRA_REPLICAR |
| home_winning_by_1 + h8_pressure_score_10m_top25 | 70 | goal_70_80 | 17 | 47.1% | 27.1% | +20.0 | 2.51 | 0.0891 | PROMISSOR_LOCAL |
| home_winning_by_1 + h8_graph_only_pressure_10m | 75 | goal_after_cutoff | 13 | 69.2% | 49.7% | +19.5 | 2.34 | 0.1704 | MICRO_AMOSTRA_REPLICAR |
| home_winning_by_1 + h8_graph_only_pressure_10m | 75 | goal_75_90 | 13 | 69.2% | 49.7% | +19.5 | 2.34 | 0.1704 | MICRO_AMOSTRA_REPLICAR |
| home_winning_by_1 + h8_cold_combo_10m_3of3 | 65 | no_goal_65_80 | 17 | 82.4% | 63.2% | +19.2 | 2.83 | 0.1233 | OBSERVAR |
| home_winning_by_1 + h8_hot_combo_10m_3of3 | 60 | goal_after_cutoff | 9 | 88.9% | 69.7% | +19.2 | 3.55 | 0.2875 | MICRO_AMOSTRA_REPLICAR |

## Padroes Com Favorito Perdendo Por 1

| variation | cutoff | target | N | rate | baseline | diff | OR | p | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_after_cutoff | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_75_90 | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_70 | 10 | 70.0% | 26.8% | +43.2 | 6.75 | 0.0049 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_75 | 10 | 80.0% | 37.1% | +42.9 | 7.13 | 0.0066 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_graph_momentum_bottom25 | 70 | goal_after_cutoff | 8 | 100.0% | 58.4% | +41.6 | 12.56 | 0.0231 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 65 | goal_after_cutoff | 2 | 100.0% | 65.0% | +35.0 | 2.72 | 0.5438 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 65 | goal_after_cutoff | 2 | 100.0% | 65.0% | +35.0 | 2.72 | 0.5438 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_graph_momentum_bottom25 | 60 | goal_60_75 | 13 | 69.2% | 37.1% | +32.1 | 4.01 | 0.0195 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_after_cutoff | 10 | 100.0% | 69.7% | +30.3 | 9.49 | 0.0360 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_cold_combo_10m_3of3 | 60 | goal_after_cutoff | 6 | 100.0% | 69.7% | +30.3 | 5.79 | 0.1840 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 60 | goal_after_cutoff | 4 | 100.0% | 69.7% | +30.3 | 3.98 | 0.3195 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 60 | goal_after_cutoff | 4 | 100.0% | 69.7% | +30.3 | 3.98 | 0.3195 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_80 | 2 | 100.0% | 72.9% | +27.1 | 1.88 | 1.0000 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_80 | 2 | 100.0% | 72.9% | +27.1 | 1.88 | 1.0000 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_graph_momentum_bottom25 | 60 | goal_60_70 | 13 | 53.8% | 26.8% | +27.0 | 3.34 | 0.0488 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_75_85 | 4 | 100.0% | 73.4% | +26.6 | 3.32 | 0.5771 | MICRO_AMOSTRA_REPLICAR |

## Padroes Com Favorito Vencendo Por 1 + Jogo Frio

| variation | cutoff | target | N | rate | baseline | diff | OR | p | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| favorite_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | goal_70_80 | 14 | 57.1% | 27.1% | +30.0 | 3.80 | 0.0262 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_cold_combo_10m_3of3 | 60 | goal_after_cutoff | 17 | 94.1% | 69.7% | +24.4 | 7.33 | 0.0282 | PROMISSOR_LOCAL |
| favorite_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | goal_70_85 | 14 | 57.1% | 38.2% | +19.0 | 2.23 | 0.1642 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_cold_combo_10m_3of3 | 65 | no_goal_after_cutoff | 18 | 50.0% | 35.0% | +15.0 | 1.92 | 0.2068 | OBSERVAR |
| favorite_winning_by_1 + h8_cold_combo_10m_3of3 | 60 | no_goal_60_75 | 17 | 76.5% | 62.9% | +13.6 | 1.97 | 0.3083 | OBSERVAR |
| favorite_winning_by_1 + h8_graph_momentum_bottom25 | 75 | goal_75_85 | 30 | 40.0% | 26.6% | +13.4 | 1.96 | 0.0886 | PROMISSOR_LOCAL |
| favorite_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | goal_after_cutoff | 14 | 71.4% | 58.4% | +13.0 | 1.82 | 0.4121 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_pressure_score_10m_bottom25 | 70 | goal_70_80 | 28 | 39.3% | 27.1% | +12.2 | 1.83 | 0.1828 | OBSERVAR |
| favorite_winning_by_1 + h8_pressure_score_10m_bottom25 | 60 | no_goal_60_75 | 36 | 75.0% | 62.9% | +12.1 | 1.87 | 0.1466 | OBSERVAR |
| favorite_winning_by_1 + h8_pressure_score_10m_bottom25 | 70 | goal_70_85 | 28 | 50.0% | 38.2% | +11.8 | 1.69 | 0.2251 | OBSERVAR |
| favorite_winning_by_1 + h8_cold_combo_10m_2of3 | 60 | no_goal_60_75 | 54 | 74.1% | 62.9% | +11.2 | 1.82 | 0.0698 | PROMISSOR_LOCAL |
| favorite_winning_by_1 + h8_cold_combo_10m_3of3 | 65 | no_goal_65_75 | 18 | 83.3% | 73.2% | +10.2 | 1.88 | 0.4202 | OBSERVAR |
| favorite_winning_by_1 + h8_cold_combo_10m_3of3 | 60 | no_goal_60_70 | 17 | 82.4% | 73.2% | +9.2 | 1.75 | 0.5762 | OBSERVAR |
| favorite_winning_by_1 + h8_graph_momentum_bottom25 | 65 | goal_after_cutoff | 31 | 74.2% | 65.0% | +9.2 | 1.60 | 0.3277 | OBSERVAR |
| favorite_winning_by_1 + h8_cold_combo_10m_3of3 | 65 | no_goal_65_80 | 18 | 72.2% | 63.2% | +9.1 | 1.55 | 0.4652 | OBSERVAR |
| favorite_winning_by_1 + h8_shot_quality_bottom25 | 70 | goal_70_80 | 25 | 36.0% | 27.1% | +8.9 | 1.56 | 0.3514 | OBSERVAR |
| favorite_winning_by_1 + h8_graph_momentum_bottom25 | 65 | goal_65_75 | 31 | 35.5% | 26.8% | +8.6 | 1.56 | 0.2906 | OBSERVAR |
| favorite_winning_by_1 + h8_shot_quality_bottom25 | 60 | goal_after_cutoff | 37 | 78.4% | 69.7% | +8.6 | 1.64 | 0.2629 | OBSERVAR |
| favorite_winning_by_1 + h8_graph_momentum_bottom25 | 70 | no_goal_70_80 | 27 | 81.5% | 72.9% | +8.6 | 1.69 | 0.3731 | OBSERVAR |
| favorite_winning_by_1 + h8_pressure_score_10m_bottom25 | 65 | no_goal_after_cutoff | 30 | 43.3% | 35.0% | +8.3 | 1.47 | 0.3248 | OBSERVAR |

## Candidatos Para Replicacao Multi-Liga

| variation | cutoff | target | N | rate | baseline | diff | OR | p | class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_conservative_hot_10m | 70 | no_goal_after_cutoff | 2 | 100.0% | 41.6% | +58.4 | 7.11 | 0.1722 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_after_cutoff | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_75_90 | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_after_cutoff | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_cold_combo_10m_3of3 | 75 | no_goal_75_90 | 4 | 100.0% | 50.3% | +49.7 | 9.10 | 0.1230 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_cold_combo_10m_3of3 | 70 | goal_70_80 | 7 | 71.4% | 27.1% | +44.3 | 7.02 | 0.0175 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_70 | 10 | 70.0% | 26.8% | +43.2 | 6.75 | 0.0049 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_70 | 10 | 70.0% | 26.8% | +43.2 | 6.75 | 0.0049 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_75 | 10 | 80.0% | 37.1% | +42.9 | 7.13 | 0.0066 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_pressure_score_10m_bottom25 | 60 | goal_60_75 | 10 | 80.0% | 37.1% | +42.9 | 7.13 | 0.0066 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_graph_momentum_bottom25 | 70 | goal_after_cutoff | 8 | 100.0% | 58.4% | +41.6 | 12.56 | 0.0231 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_graph_momentum_bottom25 | 70 | goal_after_cutoff | 8 | 100.0% | 58.4% | +41.6 | 12.56 | 0.0231 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| favorite_losing_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| underdog_winning_by_1 + h8_conservative_hot_10m | 70 | no_goal_70_85 | 2 | 100.0% | 61.8% | +38.2 | 3.12 | 0.5268 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | no_goal_65_80 | 4 | 100.0% | 63.2% | +36.8 | 5.35 | 0.3012 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | no_goal_65_80 | 4 | 100.0% | 63.2% | +36.8 | 5.35 | 0.3012 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_85 | 8 | 75.0% | 38.2% | +36.8 | 5.03 | 0.0582 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_85 | 8 | 75.0% | 38.2% | +36.8 | 5.03 | 0.0582 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_hot_combo_10m_3of3 | 70 | goal_70_80 | 8 | 62.5% | 27.1% | +35.4 | 4.66 | 0.0367 | MICRO_AMOSTRA_REPLICAR |
| favorite_winning_by_1 + h8_conservative_hot_10m | 70 | goal_70_80 | 8 | 62.5% | 27.1% | +35.4 | 4.66 | 0.0367 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_graph_only_pressure_10m | 65 | goal_after_cutoff | 11 | 100.0% | 65.0% | +35.0 | 12.98 | 0.0098 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_hot_combo_10m_3of3 | 65 | goal_after_cutoff | 4 | 100.0% | 65.0% | +35.0 | 4.93 | 0.3023 | MICRO_AMOSTRA_REPLICAR |
| away_winning_by_1 + h8_conservative_hot_10m | 65 | goal_after_cutoff | 4 | 100.0% | 65.0% | +35.0 | 4.93 | 0.3023 | MICRO_AMOSTRA_REPLICAR |
| match_balance_high + h8_hot_combo_10m_3of3 | 65 | goal_after_cutoff | 4 | 100.0% | 65.0% | +35.0 | 4.93 | 0.3023 | MICRO_AMOSTRA_REPLICAR |
| match_balance_high + h8_conservative_hot_10m | 65 | goal_after_cutoff | 4 | 100.0% | 65.0% | +35.0 | 4.93 | 0.3023 | MICRO_AMOSTRA_REPLICAR |

## Limitacoes

- Analise local em uma unica temporada EPL.
- Sem odds live reais, liquidez, slippage ou PnL.
- EV financeiro e teorico, usando odds medias travadas.
- `MULTI_LEAGUE_REPLICATION_CLASSIFICATION_V1.md` nao estava disponivel localmente/GitHub; foi usada regra operacional com classes permitidas.
- xGOT raw existe em shotmap, mas nao esta no Dataset H8 V1 validado; foi reportado como `NAO_DISPONIVEL_V1` nesta execucao.

## Proximas Etapas

- Quant Research revisar se scores compostos superam variaveis isoladas de forma suficiente.
- Replicar candidatos em multi-liga antes de qualquer baseline/modelo/backtesting.
- Criar H8 por equipe em V2 usando shotmap/incidents por `isHome`, mantendo graph por equipe bloqueado ate validacao do sinal.
