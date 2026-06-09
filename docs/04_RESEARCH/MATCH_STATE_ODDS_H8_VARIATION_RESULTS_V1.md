# MATCH_STATE_ODDS_H8_VARIATION_RESULTS_V1

## Resumo Executivo

- Validacao exploratoria executada conforme `docs/04_RESEARCH/MATCH_STATE_ODDS_H8_VARIATION_PLAN_V1.md`.
- Escopo: match state vencendo por 1 + odds pre-jogo + H8, com EV teorico simulado.
- Nenhum modelo, baseline, backtesting financeiro real, producao, schema, banco, crawler ou importer foi alterado.
- Amostra base: 380 partidas, 1520 linhas match_id + cutoff.
- Variacoes avaliadas com dados disponiveis: 1944 resultados estatisticos.
- Classificacao estatistica: {'DESCARTAR_ESTATISTICO_LOCAL': 1554, 'OBSERVAR': 357, 'NAO_DISPONIVEL_V1': 78, 'MICRO_AMOSTRA_REPLICAR': 53, 'PROMISSOR_LOCAL': 38}.
- Classificacao de mercado teorico: {'EV_POSITIVO_TEORICO': 972, 'EV_DEPENDE_PRECO': 972, 'NAO_DISPONIVEL_V1': 136}.
- Melhor padrao de gol @70: `away_winning_by_1 + shots_last_10m_low` / `goal_70_80` com N=29, taxa=48.3%, diff=+21.2 p.p., OR=2.75 e classe `PROMISSOR_LOCAL`.
- Melhor padrao de no-goal @70: `home_winning_by_1 + total_goals_4plus` / `no_goal_70_85` com N=6, taxa=100.0%, diff=+38.2 p.p., OR=8.24 e classe `MICRO_AMOSTRA_REPLICAR`.

## Metodologia

- Fontes: Dataset V1B in-game, Dataset H8 V1, Odds Features V1 e incidents brutos SofaScore.
- Cutoffs avaliados: 60, 65, 70, 75; prioridade analitica: 70.
- Odds usadas: `favorite_side`, `favorite_strength`, `match_balance` ja existentes.
- Flags derivadas permitidas: favorito/underdog por lado, favorito vencendo/perdendo por 1, underdog vencendo/perdendo por 1.
- Nao foi criada taxonomia nova de favorito por faixa fixa de odd.
- H8 usa apenas sinais ate cada cutoff.
- Targets `goal_after_cutoff` e janelas fixas foram derivados de `incidents.json`, usando apenas gols posteriores ao cutoff/janela.
- Teste estatistico: Fisher exact test bicaudal contra o complemento do grupo.
- EV teorico por R$100 foi calculado nas odds simuladas do plano; isto nao e backtesting financeiro real.

## Cortes Odds e H8

- `favorite_strength_high`: top 25%, limiar >= 0.4934.
- `favorite_strength_low`: bottom 25%, limiar <= 0.1346.
- `match_balance_high`: top 25%, limiar >= 0.8304.
- `match_balance_low`: bottom 25%, limiar <= 0.5066.
- H8 high/low foi calculado por cutoff usando top/bottom 25%.

## Top Padroes @70 - Gol

| variation_name | cutoff | target | N | pos | rate | baseline | diff_pp | OR | IC95 | p_value | multi_class | market_class | back_min_odd | lay_max_odd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| away_winning_by_1 + shots_last_10m_low | 70 | goal_70_80 | 29 | 14 | 48.3% | 27.1% | +21.2 | 2.75 | 1.28-5.92 | 0.0148 | PROMISSOR_LOCAL | EV_DEPENDE_PRECO | 2.20 | 2.00 |
| away_winning_by_1 + shots_last_10m_low | 70 | goal_70_85 | 29 | 17 | 58.6% | 38.2% | +20.5 | 2.47 | 1.14-5.33 | 0.0272 | PROMISSOR_LOCAL | EV_DEPENDE_PRECO | 1.80 | 1.70 |
| away_winning_by_1 + xg_last_10m_low | 70 | goal_70_80 | 17 | 8 | 47.1% | 27.1% | +20.0 | 2.51 | 0.94-6.69 | 0.0891 | PROMISSOR_LOCAL | EV_DEPENDE_PRECO | 2.20 | 2.00 |
| away_winning_by_1 + away_favorite | 70 | goal_70_85 | 33 | 19 | 57.6% | 38.2% | +19.4 | 2.38 | 1.15-4.91 | 0.0233 | PROMISSOR_LOCAL | EV_POSITIVO_TEORICO | 1.80 | 1.70 |
| away_winning_by_1 + home_underdog | 70 | goal_70_85 | 33 | 19 | 57.6% | 38.2% | +19.4 | 2.38 | 1.15-4.91 | 0.0233 | PROMISSOR_LOCAL | EV_POSITIVO_TEORICO | 1.80 | 1.70 |
| away_winning_by_1 + favorite_winning_by_1 | 70 | goal_70_85 | 33 | 19 | 57.6% | 38.2% | +19.4 | 2.38 | 1.15-4.91 | 0.0233 | PROMISSOR_LOCAL | EV_POSITIVO_TEORICO | 1.80 | 1.70 |
| away_winning_by_1 + momentum_last_10m_avg_low | 70 | goal_after_cutoff | 13 | 10 | 76.9% | 58.4% | +18.5 | 2.44 | 0.66-9.00 | 0.2527 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | 1.30 | NA |
| away_winning_by_1 + momentum_last_10m_avg_low | 70 | goal_70_90 | 13 | 10 | 76.9% | 58.4% | +18.5 | 2.44 | 0.66-9.00 | 0.2527 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | 1.30 | NA |
| home_winning_by_1 + home_underdog | 70 | goal_after_cutoff | 17 | 13 | 76.5% | 58.4% | +18.0 | 2.39 | 0.77-7.49 | 0.1387 | OBSERVAR | EV_DEPENDE_PRECO | 1.40 | 1.30 |
| home_winning_by_1 + home_underdog | 70 | goal_70_90 | 17 | 13 | 76.5% | 58.4% | +18.0 | 2.39 | 0.77-7.49 | 0.1387 | OBSERVAR | EV_DEPENDE_PRECO | 1.40 | 1.30 |
| home_winning_by_1 + away_favorite | 70 | goal_after_cutoff | 17 | 13 | 76.5% | 58.4% | +18.0 | 2.39 | 0.77-7.49 | 0.1387 | OBSERVAR | EV_DEPENDE_PRECO | 1.40 | 1.30 |
| home_winning_by_1 + away_favorite | 70 | goal_70_90 | 17 | 13 | 76.5% | 58.4% | +18.0 | 2.39 | 0.77-7.49 | 0.1387 | OBSERVAR | EV_DEPENDE_PRECO | 1.40 | 1.30 |
| home_winning_by_1 + favorite_losing_by_1 | 70 | goal_after_cutoff | 17 | 13 | 76.5% | 58.4% | +18.0 | 2.39 | 0.77-7.49 | 0.1387 | OBSERVAR | EV_DEPENDE_PRECO | 1.40 | 1.30 |
| home_winning_by_1 + favorite_losing_by_1 | 70 | goal_70_90 | 17 | 13 | 76.5% | 58.4% | +18.0 | 2.39 | 0.77-7.49 | 0.1387 | OBSERVAR | EV_DEPENDE_PRECO | 1.40 | 1.30 |
| home_winning_by_1 + underdog_winning_by_1 | 70 | goal_after_cutoff | 17 | 13 | 76.5% | 58.4% | +18.0 | 2.39 | 0.77-7.49 | 0.1387 | OBSERVAR | EV_DEPENDE_PRECO | 1.40 | 1.30 |
| home_winning_by_1 + underdog_winning_by_1 | 70 | goal_70_90 | 17 | 13 | 76.5% | 58.4% | +18.0 | 2.39 | 0.77-7.49 | 0.1387 | OBSERVAR | EV_DEPENDE_PRECO | 1.40 | 1.30 |
| away_winning_by_1 + match_balance_low | 70 | goal_70_85 | 11 | 6 | 54.5% | 38.2% | +16.4 | 1.99 | 0.59-6.63 | 0.3459 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | 1.90 | 1.80 |
| away_winning_by_1 + favorite_strength_high | 70 | goal_70_85 | 11 | 6 | 54.5% | 38.2% | +16.4 | 1.99 | 0.59-6.63 | 0.3459 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | 1.90 | 1.80 |
| home_winning_by_1 + momentum_last_10m_avg_low | 70 | goal_after_cutoff | 23 | 17 | 73.9% | 58.4% | +15.5 | 2.10 | 0.81-5.45 | 0.1324 | OBSERVAR | EV_DEPENDE_PRECO | 1.40 | 1.30 |
| home_winning_by_1 + momentum_last_10m_avg_low | 70 | goal_70_90 | 23 | 17 | 73.9% | 58.4% | +15.5 | 2.10 | 0.81-5.45 | 0.1324 | OBSERVAR | EV_DEPENDE_PRECO | 1.40 | 1.30 |
| favorite_losing_by_1 + momentum_trend_positive | 70 | goal_70_80 | 22 | 9 | 40.9% | 27.1% | +13.8 | 1.94 | 0.80-4.70 | 0.1426 | OBSERVAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + match_balance_high | 70 | goal_after_cutoff | 25 | 18 | 72.0% | 58.4% | +13.6 | 1.90 | 0.78-4.67 | 0.2077 | OBSERVAR | EV_DEPENDE_PRECO | 1.40 | 1.30 |
| home_winning_by_1 + match_balance_high | 70 | goal_70_90 | 25 | 18 | 72.0% | 58.4% | +13.6 | 1.90 | 0.78-4.67 | 0.2077 | OBSERVAR | EV_DEPENDE_PRECO | 1.40 | 1.30 |
| away_winning_by_1 + momentum_trend_positive | 70 | goal_70_80 | 37 | 15 | 40.5% | 27.1% | +13.4 | 1.98 | 0.98-3.98 | 0.0777 | PROMISSOR_LOCAL | EV_POSITIVO_TEORICO | NA | 2.20 |
| away_winning_by_1 + total_goals_3 | 70 | goal_after_cutoff | 21 | 15 | 71.4% | 58.4% | +13.0 | 1.84 | 0.70-4.84 | 0.2590 | OBSERVAR | EV_DEPENDE_PRECO | 1.50 | 1.40 |

## Top Padroes @70 - No Goal

| variation_name | cutoff | target | N | pos | rate | baseline | diff_pp | OR | IC95 | p_value | multi_class | market_class | back_min_odd | lay_max_odd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| home_winning_by_1 + total_goals_4plus | 70 | no_goal_70_85 | 6 | 6 | 100.0% | 61.8% | +38.2 | 8.24 | 0.46-147.41 | 0.0866 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + total_goals_4plus | 70 | no_goal_70_80 | 6 | 6 | 100.0% | 72.9% | +27.1 | 4.96 | 0.28-88.76 | 0.1963 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| away_winning_by_1 + total_goals_4plus | 70 | no_goal_after_cutoff | 3 | 2 | 66.7% | 41.6% | +25.1 | 2.83 | 0.25-31.52 | 0.5728 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| away_winning_by_1 + total_goals_4plus | 70 | no_goal_70_90 | 3 | 2 | 66.7% | 41.6% | +25.1 | 2.83 | 0.25-31.52 | 0.5728 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| favorite_losing_by_1 + favorite_strength_high | 70 | no_goal_after_cutoff | 7 | 4 | 57.1% | 41.6% | +15.6 | 1.90 | 0.42-8.59 | 0.4562 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| favorite_losing_by_1 + favorite_strength_high | 70 | no_goal_70_90 | 7 | 4 | 57.1% | 41.6% | +15.6 | 1.90 | 0.42-8.59 | 0.4562 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| underdog_winning_by_1 + favorite_strength_high | 70 | no_goal_after_cutoff | 7 | 4 | 57.1% | 41.6% | +15.6 | 1.90 | 0.42-8.59 | 0.4562 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| underdog_winning_by_1 + favorite_strength_high | 70 | no_goal_70_90 | 7 | 4 | 57.1% | 41.6% | +15.6 | 1.90 | 0.42-8.59 | 0.4562 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| favorite_losing_by_1 + xg_last_10m_high | 70 | no_goal_after_cutoff | 9 | 5 | 55.6% | 41.6% | +14.0 | 1.78 | 0.47-6.74 | 0.4986 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| favorite_losing_by_1 + xg_last_10m_high | 70 | no_goal_70_90 | 9 | 5 | 55.6% | 41.6% | +14.0 | 1.78 | 0.47-6.74 | 0.4986 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| favorite_losing_by_1 + favorite_strength_high | 70 | no_goal_70_80 | 7 | 6 | 85.7% | 72.9% | +12.8 | 2.26 | 0.27-18.99 | 0.6794 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| underdog_winning_by_1 + favorite_strength_high | 70 | no_goal_70_80 | 7 | 6 | 85.7% | 72.9% | +12.8 | 2.26 | 0.27-18.99 | 0.6794 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| away_winning_by_1 + momentum_last_10m_avg_high | 70 | no_goal_70_85 | 23 | 17 | 73.9% | 61.8% | +12.1 | 1.81 | 0.70-4.69 | 0.2715 | OBSERVAR | EV_DEPENDE_PRECO | NA | 2.20 |
| favorite_losing_by_1 + total_goals_3plus | 70 | no_goal_70_85 | 19 | 14 | 73.7% | 61.8% | +11.8 | 1.77 | 0.63-5.03 | 0.3383 | OBSERVAR | EV_DEPENDE_PRECO | NA | 2.20 |
| underdog_winning_by_1 + total_goals_3plus | 70 | no_goal_70_85 | 19 | 14 | 73.7% | 61.8% | +11.8 | 1.77 | 0.63-5.03 | 0.3383 | OBSERVAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + shots_last_10m_low | 70 | no_goal_70_85 | 43 | 31 | 72.1% | 61.8% | +10.3 | 1.68 | 0.84-3.40 | 0.1821 | OBSERVAR | EV_POSITIVO_TEORICO | NA | 2.20 |
| away_winning_by_1 + momentum_last_10m_avg_high | 70 | no_goal_70_80 | 23 | 19 | 82.6% | 72.9% | +9.7 | 1.82 | 0.60-5.49 | 0.3410 | OBSERVAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + momentum_last_10m_avg_low | 70 | no_goal_70_80 | 23 | 19 | 82.6% | 72.9% | +9.7 | 1.82 | 0.60-5.49 | 0.3410 | OBSERVAR | EV_DEPENDE_PRECO | NA | 2.20 |
| away_winning_by_1 + match_balance_high | 70 | no_goal_70_80 | 22 | 18 | 81.8% | 72.9% | +8.9 | 1.72 | 0.57-5.21 | 0.4602 | OBSERVAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + cold_game_2of4 | 70 | no_goal_70_80 | 49 | 40 | 81.6% | 72.9% | +8.7 | 1.76 | 0.82-3.78 | 0.1692 | OBSERVAR | EV_POSITIVO_TEORICO | NA | 2.20 |
| home_winning_by_1 + home_favorite | 70 | no_goal_70_80 | 70 | 57 | 81.4% | 72.9% | +8.5 | 1.79 | 0.94-3.44 | 0.1007 | OBSERVAR | EV_POSITIVO_TEORICO | NA | 2.20 |
| home_winning_by_1 + away_underdog | 70 | no_goal_70_80 | 70 | 57 | 81.4% | 72.9% | +8.5 | 1.79 | 0.94-3.44 | 0.1007 | OBSERVAR | EV_POSITIVO_TEORICO | NA | 2.20 |
| home_winning_by_1 + favorite_winning_by_1 | 70 | no_goal_70_80 | 70 | 57 | 81.4% | 72.9% | +8.5 | 1.79 | 0.94-3.44 | 0.1007 | OBSERVAR | EV_POSITIVO_TEORICO | NA | 2.20 |
| home_winning_by_1 + xg_last_10m_low | 70 | no_goal_70_85 | 27 | 19 | 70.4% | 61.8% | +8.5 | 1.51 | 0.64-3.54 | 0.4142 | OBSERVAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + favorite_strength_low | 70 | no_goal_70_85 | 27 | 19 | 70.4% | 61.8% | +8.5 | 1.51 | 0.64-3.54 | 0.4142 | OBSERVAR | EV_DEPENDE_PRECO | NA | 2.20 |

## Top Padroes Gerais

| variation_name | cutoff | target | N | pos | rate | baseline | diff_pp | OR | IC95 | p_value | multi_class | market_class | back_min_odd | lay_max_odd |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| away_winning_by_1 + total_goals_4plus | 65 | no_goal_after_cutoff | 1 | 1 | 100.0% | 35.0% | +65.0 | 5.60 | 0.23-138.53 | 0.3500 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + total_goals_4plus | 70 | no_goal_70_85 | 6 | 6 | 100.0% | 61.8% | +38.2 | 8.24 | 0.46-147.41 | 0.0866 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + total_goals_4plus | 60 | no_goal_60_75 | 4 | 4 | 100.0% | 62.9% | +37.1 | 5.41 | 0.29-101.19 | 0.3013 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + total_goals_4plus | 65 | no_goal_65_80 | 5 | 5 | 100.0% | 63.2% | +36.8 | 6.56 | 0.36-119.59 | 0.1626 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| away_winning_by_1 + total_goals_4plus | 65 | no_goal_65_80 | 1 | 1 | 100.0% | 63.2% | +36.8 | 1.76 | 0.07-43.50 | 1.0000 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + total_goals_4plus | 70 | no_goal_70_80 | 6 | 6 | 100.0% | 72.9% | +27.1 | 4.96 | 0.28-88.76 | 0.1963 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + total_goals_4plus | 65 | no_goal_65_75 | 5 | 5 | 100.0% | 73.2% | +26.8 | 4.12 | 0.23-75.22 | 0.3300 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + total_goals_4plus | 60 | no_goal_60_70 | 4 | 4 | 100.0% | 73.2% | +26.8 | 3.36 | 0.18-62.97 | 0.5775 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + total_goals_4plus | 75 | no_goal_75_85 | 7 | 7 | 100.0% | 73.4% | +26.6 | 5.59 | 0.32-98.72 | 0.1968 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + xg_last_10m_high | 65 | goal_65_80 | 19 | 12 | 63.2% | 36.8% | +26.3 | 3.12 | 1.20-8.12 | 0.0253 | PROMISSOR_LOCAL | EV_DEPENDE_PRECO | 1.60 | 1.50 |
| away_winning_by_1 + total_goals_4plus | 70 | no_goal_after_cutoff | 3 | 2 | 66.7% | 41.6% | +25.1 | 2.83 | 0.25-31.52 | 0.5728 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| away_winning_by_1 + total_goals_4plus | 70 | no_goal_70_90 | 3 | 2 | 66.7% | 41.6% | +25.1 | 2.83 | 0.25-31.52 | 0.5728 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | NA | 2.20 |
| favorite_losing_by_1 + xg_last_10m_high | 65 | goal_after_cutoff | 10 | 9 | 90.0% | 65.0% | +25.0 | 4.99 | 0.63-39.83 | 0.1751 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | 1.30 | NA |
| away_winning_by_1 + xg_last_10m_high | 65 | no_goal_65_80 | 16 | 14 | 87.5% | 63.2% | +24.3 | 4.27 | 0.96-19.09 | 0.0603 | PROMISSOR_LOCAL | EV_DEPENDE_PRECO | NA | 2.20 |
| away_winning_by_1 + momentum_last_10m_avg_low | 65 | goal_65_80 | 15 | 9 | 60.0% | 36.8% | +23.2 | 2.68 | 0.93-7.69 | 0.0975 | PROMISSOR_LOCAL | EV_DEPENDE_PRECO | 1.70 | 1.60 |
| favorite_losing_by_1 + xg_last_10m_high | 65 | goal_65_75 | 10 | 5 | 50.0% | 26.8% | +23.2 | 2.81 | 0.80-9.93 | 0.1406 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | 2.20 | 1.90 |
| favorite_losing_by_1 + xg_last_10m_high | 65 | goal_65_80 | 10 | 6 | 60.0% | 36.8% | +23.2 | 2.64 | 0.73-9.53 | 0.1817 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | 1.70 | 1.60 |
| favorite_losing_by_1 + favorite_strength_high | 60 | goal_60_70 | 8 | 4 | 50.0% | 26.8% | +23.2 | 2.80 | 0.69-11.39 | 0.2184 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | 2.20 | 1.90 |
| underdog_winning_by_1 + favorite_strength_high | 60 | goal_60_70 | 8 | 4 | 50.0% | 26.8% | +23.2 | 2.80 | 0.69-11.39 | 0.2184 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | 2.20 | 1.90 |
| away_winning_by_1 + match_balance_low | 60 | goal_after_cutoff | 11 | 10 | 90.9% | 69.7% | +21.2 | 4.47 | 0.57-35.34 | 0.1842 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | 1.30 | NA |
| away_winning_by_1 + favorite_strength_high | 60 | goal_after_cutoff | 11 | 10 | 90.9% | 69.7% | +21.2 | 4.47 | 0.57-35.34 | 0.1842 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | 1.30 | NA |
| away_winning_by_1 + shots_last_10m_low | 70 | goal_70_80 | 29 | 14 | 48.3% | 27.1% | +21.2 | 2.75 | 1.28-5.92 | 0.0148 | PROMISSOR_LOCAL | EV_DEPENDE_PRECO | 2.20 | 2.00 |
| away_winning_by_1 + xg_last_10m_high | 65 | no_goal_65_75 | 16 | 15 | 93.8% | 73.2% | +20.6 | 5.76 | 0.75-44.18 | 0.0804 | PROMISSOR_LOCAL | EV_DEPENDE_PRECO | NA | 2.20 |
| home_winning_by_1 + xg_last_10m_high | 65 | goal_65_75 | 19 | 9 | 47.4% | 26.8% | +20.5 | 2.59 | 1.02-6.58 | 0.0590 | PROMISSOR_LOCAL | EV_DEPENDE_PRECO | 2.20 | 2.00 |
| away_winning_by_1 + away_favorite | 75 | goal_75_85 | 34 | 16 | 47.1% | 26.6% | +20.5 | 2.73 | 1.33-5.59 | 0.0075 | PROMISSOR_LOCAL | EV_POSITIVO_TEORICO | 2.20 | 2.00 |
| away_winning_by_1 + home_underdog | 75 | goal_75_85 | 34 | 16 | 47.1% | 26.6% | +20.5 | 2.73 | 1.33-5.59 | 0.0075 | PROMISSOR_LOCAL | EV_POSITIVO_TEORICO | 2.20 | 2.00 |
| away_winning_by_1 + favorite_winning_by_1 | 75 | goal_75_85 | 34 | 16 | 47.1% | 26.6% | +20.5 | 2.73 | 1.33-5.59 | 0.0075 | PROMISSOR_LOCAL | EV_POSITIVO_TEORICO | 2.20 | 2.00 |
| away_winning_by_1 + shots_last_10m_low | 70 | goal_70_85 | 29 | 17 | 58.6% | 38.2% | +20.5 | 2.47 | 1.14-5.33 | 0.0272 | PROMISSOR_LOCAL | EV_DEPENDE_PRECO | 1.80 | 1.70 |
| favorite_losing_by_1 + xg_last_10m_high | 60 | goal_after_cutoff | 10 | 9 | 90.0% | 69.7% | +20.3 | 4.01 | 0.50-32.01 | 0.2936 | MICRO_AMOSTRA_REPLICAR | EV_DEPENDE_PRECO | 1.30 | NA |
| away_winning_by_1 + xg_last_10m_high | 75 | goal_75_85 | 15 | 7 | 46.7% | 26.6% | +20.1 | 2.52 | 0.89-7.15 | 0.0806 | PROMISSOR_LOCAL | EV_DEPENDE_PRECO | 2.20 | 2.00 |

## Sensibilidade EV Teorico

| variation_name | cutoff | target | N | p_goal | odd | back_ev | lay_ev | preferred_side |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| away_winning_by_1 + match_balance_low | 60 | goal_after_cutoff | 11 | 90.9% | 2.20 | 100.00 | -100.00 | Back Over |
| away_winning_by_1 + match_balance_low | 60 | no_goal_after_cutoff | 11 | 90.9% | 2.20 | 100.00 | -100.00 | Back Over |
| away_winning_by_1 + favorite_strength_high | 60 | goal_after_cutoff | 11 | 90.9% | 2.20 | 100.00 | -100.00 | Back Over |
| away_winning_by_1 + favorite_strength_high | 60 | no_goal_after_cutoff | 11 | 90.9% | 2.20 | 100.00 | -100.00 | Back Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_70 | 4 | 0.0% | 1.30 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_70 | 4 | 0.0% | 1.40 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_70 | 4 | 0.0% | 1.50 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_70 | 4 | 0.0% | 1.60 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_70 | 4 | 0.0% | 1.70 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_70 | 4 | 0.0% | 1.80 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_70 | 4 | 0.0% | 1.90 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_70 | 4 | 0.0% | 2.00 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_70 | 4 | 0.0% | 2.20 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | no_goal_60_70 | 4 | 0.0% | 1.30 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | no_goal_60_70 | 4 | 0.0% | 1.40 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | no_goal_60_70 | 4 | 0.0% | 1.50 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | no_goal_60_70 | 4 | 0.0% | 1.60 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | no_goal_60_70 | 4 | 0.0% | 1.70 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | no_goal_60_70 | 4 | 0.0% | 1.80 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | no_goal_60_70 | 4 | 0.0% | 1.90 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | no_goal_60_70 | 4 | 0.0% | 2.00 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | no_goal_60_70 | 4 | 0.0% | 2.20 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_75 | 4 | 0.0% | 1.30 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_75 | 4 | 0.0% | 1.40 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_75 | 4 | 0.0% | 1.50 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_75 | 4 | 0.0% | 1.60 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_75 | 4 | 0.0% | 1.70 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_75 | 4 | 0.0% | 1.80 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_75 | 4 | 0.0% | 1.90 | -100.00 | 100.00 | Lay Over |
| home_winning_by_1 + total_goals_4plus | 60 | goal_60_75 | 4 | 0.0% | 2.00 | -100.00 | 100.00 | Lay Over |

## Features NAO DISPONIVEL V1

- `favorite_pressure_high`: H8 V1 atual nao separa pressao por time; nao foi improvisado.
- `losing_team_pressure_high`: H8 V1 atual nao separa pressao por time; nao foi improvisado.

## Regras Anti-Leakage Confirmadas

- Estado do placar usa somente gols ate o cutoff.
- H8 usa somente eventos ate o cutoff.
- Odds sao pre-game closing/features Football-Data; nenhuma odd live/in-play foi usada.
- Placar final nao foi usado como feature.
- Target foi usado somente como resposta.
- Features por time nao existentes foram marcadas como `NAO_DISPONIVEL_V1`.

## Limitacoes

- Analise local em uma unica liga/temporada; classes multi-liga robustas dependem de replicacao futura.
- Documento `MULTI_LEAGUE_REPLICATION_CLASSIFICATION_V1.md` nao foi encontrado; foi aplicada regra operacional documentada com as classes permitidas pelo plano.
- EV e apenas sensibilidade teorica por taxa observada e odd simulada; sem odds live reais, sem liquidez, sem slippage e sem PnL.
- Padroes com N pequeno foram marcados para replicacao quando fortes, nao descartados automaticamente.

## Recomendacao

- Enviar para Quant Research revisar os padroes `PROMISSOR_LOCAL`, `MICRO_AMOSTRA_REPLICAR` e `OBSERVAR`.
- Nao executar baseline, modelo, backtesting financeiro real ou producao sem nova autorizacao.
- Proxima etapa recomendada: decidir se vale replicar os melhores padroes em multi-liga antes de qualquer estudo de odds live.
