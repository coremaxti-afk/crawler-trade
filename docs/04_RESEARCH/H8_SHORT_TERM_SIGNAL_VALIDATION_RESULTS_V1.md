# H8 SHORT-TERM SIGNAL VALIDATION RESULTS V1

## Resumo Executivo

- Validacao executada conforme `docs/04_RESEARCH/H8_SHORT_TERM_LATE_MARKET_STRATEGY_PLAN.md`.
- Cutoff principal: 60 minutos.
- Features H8 usadas apenas ate o cutoff 60.
- Targets de gol/no-gol foram derivados dos `incidents.json` brutos usando apenas gols na janela posterior.
- Amostra: 380 partidas.
- Classificacao geral: PROMISSORA=0, OBSERVAR=5, DESCARTAR=25.
- Melhor sinal observado: `shots_last_10m_high` para `goal_65_80` com N=122, taxa=41.0%, diff=+4.1 p.p., OR=1.30, p-value=0.2568 e classificacao `OBSERVAR`.

## Metodologia

- Fonte de features: Dataset H8 V1 filtrado em `cutoff_minute = 60`.
- Fonte dos targets: `Crawler/Sofascore/data/raw/sofascore/premier_league_61627/matches/{event_id}/incidents.json`.
- Gol de janela: evento com `incidentType = goal` e minuto `> inicio` e `<= fim`.
- No-goal de janela: ausencia de gol na janela definida.
- Teste estatistico: Fisher exact test bicaudal contra o complemento do grupo.
- Odds ratio e IC 95% calculados em tabela 2x2, com correcao de Haldane-Anscombe quando necessario.
- Hot signals foram avaliados contra targets de gol; Cold signals contra targets de no-goal.

## Cortes Aplicados

- `shots_last_10m_high`: top 25%, limiar >= 4.0000.
- `shots_last_10m_low`: bottom 25%, limiar <= 2.0000.
- `xg_last_10m_high`: top 25%, limiar >= 0.447821.
- `xg_last_10m_low`: bottom 25%, limiar <= 0.087494.
- `momentum_trend_last_10m_positive`: `momentum_trend_last_10m > 0`.
- `momentum_trend_last_10m_non_positive`: `momentum_trend_last_10m <= 0`.
- `momentum_last_10m_avg_high`: top 25%, limiar >= 17.7500.
- `momentum_last_10m_avg_low`: bottom 25%, limiar <= -13.6500.
- `hot_game_2of4`: pelo menos 2 dos 4 sinais hot.
- `cold_game_2of4`: pelo menos 2 dos 4 sinais cold.

## Baselines Dos Targets

| Target | Janela | Positivo | N | Positivos | Taxa |
| --- | --- | --- | --- | --- | --- |
| goal_60_70 | 60-70 | goal | 380 | 102 | 26.8% |
| goal_60_75 | 60-75 | goal | 380 | 141 | 37.1% |
| goal_60_80 | 60-80 | goal | 380 | 174 | 45.8% |
| goal_65_80 | 65-80 | goal | 380 | 140 | 36.8% |
| no_goal_60_75 | 60-75 | no_goal | 380 | 239 | 62.9% |
| no_goal_60_80 | 60-80 | no_goal | 380 | 206 | 54.2% |

## Hot Signals - Targets De Gol

| Grupo | Sinal | Target | N | Pos | Neg | Taxa | Baseline | Diff p.p. | OR | IC 95% | p-value | Componentes | Top time | Class. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Hot | shots_last_10m_high | goal_60_70 | 122 | 31 | 91 | 25.4% | 26.8% | -1.4 | 0.90 | 0.55-1.47 | 0.7110 | shots_last_10m_high=25.4% | Tottenham Hotspur (14.8%) | DESCARTAR |
| Hot | shots_last_10m_high | goal_60_75 | 122 | 44 | 78 | 36.1% | 37.1% | -1.0 | 0.94 | 0.60-1.46 | 0.8205 | shots_last_10m_high=36.1% | Tottenham Hotspur (14.8%) | DESCARTAR |
| Hot | shots_last_10m_high | goal_60_80 | 122 | 58 | 64 | 47.5% | 45.8% | +1.8 | 1.11 | 0.72-1.71 | 0.6602 | shots_last_10m_high=47.5% | Tottenham Hotspur (14.8%) | DESCARTAR |
| Hot | shots_last_10m_high | goal_65_80 | 122 | 50 | 72 | 41.0% | 36.8% | +4.1 | 1.30 | 0.83-2.02 | 0.2568 | shots_last_10m_high=41.0% | Tottenham Hotspur (14.8%) | OBSERVAR |
| Hot | xg_last_10m_high | goal_60_70 | 95 | 22 | 73 | 23.2% | 26.8% | -3.7 | 0.77 | 0.45-1.33 | 0.4226 | xg_last_10m_high=23.2% | Southampton (13.7%) | DESCARTAR |
| Hot | xg_last_10m_high | goal_60_75 | 95 | 34 | 61 | 35.8% | 37.1% | -1.3 | 0.93 | 0.57-1.50 | 0.8069 | xg_last_10m_high=35.8% | Southampton (13.7%) | DESCARTAR |
| Hot | xg_last_10m_high | goal_60_80 | 95 | 46 | 49 | 48.4% | 45.8% | +2.6 | 1.15 | 0.72-1.83 | 0.5549 | xg_last_10m_high=48.4% | Southampton (13.7%) | DESCARTAR |
| Hot | xg_last_10m_high | goal_65_80 | 95 | 38 | 57 | 40.0% | 36.8% | +3.2 | 1.20 | 0.74-1.93 | 0.4640 | xg_last_10m_high=40.0% | Southampton (13.7%) | DESCARTAR |
| Hot | momentum_trend_last_10m_positive | goal_60_70 | 182 | 56 | 126 | 30.8% | 26.8% | +3.9 | 1.47 | 0.93-2.32 | 0.1057 | momentum_trend_last_10m_positive=30.8% | Manchester United (11.5%) | OBSERVAR |
| Hot | momentum_trend_last_10m_positive | goal_60_75 | 182 | 75 | 107 | 41.2% | 37.1% | +4.1 | 1.40 | 0.92-2.13 | 0.1366 | momentum_trend_last_10m_positive=41.2% | Manchester United (11.5%) | OBSERVAR |
| Hot | momentum_trend_last_10m_positive | goal_60_80 | 182 | 86 | 96 | 47.3% | 45.8% | +1.5 | 1.12 | 0.75-1.68 | 0.6073 | momentum_trend_last_10m_positive=47.3% | Manchester United (11.5%) | DESCARTAR |
| Hot | momentum_trend_last_10m_positive | goal_65_80 | 182 | 71 | 111 | 39.0% | 36.8% | +2.2 | 1.20 | 0.79-1.82 | 0.4563 | momentum_trend_last_10m_positive=39.0% | Manchester United (11.5%) | DESCARTAR |
| Hot | momentum_last_10m_avg_high | goal_60_70 | 95 | 25 | 70 | 26.3% | 26.8% | -0.5 | 0.96 | 0.57-1.63 | 1.0000 | momentum_last_10m_avg_high=26.3% | Brentford (14.7%) | DESCARTAR |
| Hot | momentum_last_10m_avg_high | goal_60_75 | 95 | 32 | 63 | 33.7% | 37.1% | -3.4 | 0.82 | 0.50-1.34 | 0.4632 | momentum_last_10m_avg_high=33.7% | Brentford (14.7%) | DESCARTAR |
| Hot | momentum_last_10m_avg_high | goal_60_80 | 95 | 39 | 56 | 41.1% | 45.8% | -4.7 | 0.77 | 0.48-1.24 | 0.3416 | momentum_last_10m_avg_high=41.1% | Brentford (14.7%) | DESCARTAR |
| Hot | momentum_last_10m_avg_high | goal_65_80 | 95 | 32 | 63 | 33.7% | 36.8% | -3.2 | 0.83 | 0.51-1.36 | 0.5394 | momentum_last_10m_avg_high=33.7% | Brentford (14.7%) | DESCARTAR |
| Hot | hot_game_2of4 | goal_60_70 | 148 | 39 | 109 | 26.4% | 26.8% | -0.5 | 0.96 | 0.60-1.53 | 0.9058 | shots_last_10m_high=25.4%; xg_last_10m_high=23.2%; momentum_trend_last_10m_positive=30.8%; momentum_last_10m_avg_high=26.3% | Brentford (16.9%) | DESCARTAR |
| Hot | hot_game_2of4 | goal_60_75 | 148 | 53 | 95 | 35.8% | 37.1% | -1.3 | 0.91 | 0.60-1.40 | 0.7441 | shots_last_10m_high=36.1%; xg_last_10m_high=35.8%; momentum_trend_last_10m_positive=41.2%; momentum_last_10m_avg_high=33.7% | Brentford (16.9%) | DESCARTAR |
| Hot | hot_game_2of4 | goal_60_80 | 148 | 68 | 80 | 45.9% | 45.8% | +0.2 | 1.01 | 0.67-1.53 | 1.0000 | shots_last_10m_high=47.5%; xg_last_10m_high=48.4%; momentum_trend_last_10m_positive=47.3%; momentum_last_10m_avg_high=41.1% | Brentford (16.9%) | DESCARTAR |
| Hot | hot_game_2of4 | goal_65_80 | 148 | 57 | 91 | 38.5% | 36.8% | +1.7 | 1.12 | 0.73-1.72 | 0.6628 | shots_last_10m_high=41.0%; xg_last_10m_high=40.0%; momentum_trend_last_10m_positive=39.0%; momentum_last_10m_avg_high=33.7% | Brentford (16.9%) | DESCARTAR |

## Cold Signals - Targets De No-Goal

| Grupo | Sinal | Target | N | Pos | Neg | Taxa | Baseline | Diff p.p. | OR | IC 95% | p-value | Componentes | Top time | Class. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cold | shots_last_10m_low | no_goal_60_75 | 166 | 108 | 58 | 65.1% | 62.9% | +2.2 | 1.18 | 0.77-1.80 | 0.4555 | shots_last_10m_low=65.1% | Wolverhampton (14.5%) | DESCARTAR |
| Cold | shots_last_10m_low | no_goal_60_80 | 166 | 91 | 75 | 54.8% | 54.2% | +0.6 | 1.04 | 0.70-1.57 | 0.8364 | shots_last_10m_low=54.8% | Wolverhampton (14.5%) | DESCARTAR |
| Cold | xg_last_10m_low | no_goal_60_75 | 95 | 60 | 35 | 63.2% | 62.9% | +0.3 | 1.02 | 0.63-1.64 | 1.0000 | xg_last_10m_low=63.2% | Everton (13.7%) | DESCARTAR |
| Cold | xg_last_10m_low | no_goal_60_80 | 95 | 54 | 41 | 56.8% | 54.2% | +2.6 | 1.15 | 0.72-1.84 | 0.6345 | xg_last_10m_low=56.8% | Everton (13.7%) | DESCARTAR |
| Cold | momentum_trend_last_10m_non_positive | no_goal_60_75 | 197 | 131 | 66 | 66.5% | 62.9% | +3.6 | 1.38 | 0.91-2.09 | 0.1381 | momentum_trend_last_10m_non_positive=66.5% | Brighton & Hove Albion (13.7%) | OBSERVAR |
| Cold | momentum_trend_last_10m_non_positive | no_goal_60_80 | 197 | 109 | 88 | 55.3% | 54.2% | +1.1 | 1.10 | 0.73-1.64 | 0.6808 | momentum_trend_last_10m_non_positive=55.3% | Brighton & Hove Albion (13.7%) | DESCARTAR |
| Cold | momentum_last_10m_avg_low | no_goal_60_75 | 95 | 54 | 41 | 56.8% | 62.9% | -6.1 | 0.71 | 0.44-1.14 | 0.1778 | momentum_last_10m_avg_low=56.8% | Liverpool FC (14.7%) | DESCARTAR |
| Cold | momentum_last_10m_avg_low | no_goal_60_80 | 95 | 45 | 50 | 47.4% | 54.2% | -6.8 | 0.69 | 0.44-1.10 | 0.1245 | momentum_last_10m_avg_low=47.4% | Liverpool FC (14.7%) | DESCARTAR |
| Cold | cold_game_2of4 | no_goal_60_75 | 170 | 112 | 58 | 65.9% | 62.9% | +3.0 | 1.26 | 0.83-1.92 | 0.2876 | shots_last_10m_low=65.1%; xg_last_10m_low=63.2%; momentum_trend_last_10m_non_positive=66.5%; momentum_last_10m_avg_low=56.8% | Everton (12.9%) | OBSERVAR |
| Cold | cold_game_2of4 | no_goal_60_80 | 170 | 93 | 77 | 54.7% | 54.2% | +0.5 | 1.04 | 0.69-1.56 | 0.9176 | shots_last_10m_low=54.8%; xg_last_10m_low=56.8%; momentum_trend_last_10m_non_positive=55.3%; momentum_last_10m_avg_low=47.4% | Everton (12.9%) | DESCARTAR |

## Ranking Geral

| Rank | Grupo | Sinal | Target | Classificacao | N | Taxa | Diff p.p. | OR | p-value |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Hot | shots_last_10m_high | goal_65_80 | OBSERVAR | 122 | 41.0% | +4.1 | 1.30 | 0.2568 |
| 2 | Hot | momentum_trend_last_10m_positive | goal_60_75 | OBSERVAR | 182 | 41.2% | +4.1 | 1.40 | 0.1366 |
| 3 | Hot | momentum_trend_last_10m_positive | goal_60_70 | OBSERVAR | 182 | 30.8% | +3.9 | 1.47 | 0.1057 |
| 4 | Cold | momentum_trend_last_10m_non_positive | no_goal_60_75 | OBSERVAR | 197 | 66.5% | +3.6 | 1.38 | 0.1381 |
| 5 | Cold | cold_game_2of4 | no_goal_60_75 | OBSERVAR | 170 | 65.9% | +3.0 | 1.26 | 0.2876 |
| 6 | Hot | xg_last_10m_high | goal_65_80 | DESCARTAR | 95 | 40.0% | +3.2 | 1.20 | 0.4640 |
| 7 | Hot | xg_last_10m_high | goal_60_80 | DESCARTAR | 95 | 48.4% | +2.6 | 1.15 | 0.5549 |
| 8 | Cold | xg_last_10m_low | no_goal_60_80 | DESCARTAR | 95 | 56.8% | +2.6 | 1.15 | 0.6345 |
| 9 | Hot | momentum_trend_last_10m_positive | goal_65_80 | DESCARTAR | 182 | 39.0% | +2.2 | 1.20 | 0.4563 |
| 10 | Cold | shots_last_10m_low | no_goal_60_75 | DESCARTAR | 166 | 65.1% | +2.2 | 1.18 | 0.4555 |
| 11 | Hot | shots_last_10m_high | goal_60_80 | DESCARTAR | 122 | 47.5% | +1.8 | 1.11 | 0.6602 |
| 12 | Hot | hot_game_2of4 | goal_65_80 | DESCARTAR | 148 | 38.5% | +1.7 | 1.12 | 0.6628 |
| 13 | Hot | momentum_trend_last_10m_positive | goal_60_80 | DESCARTAR | 182 | 47.3% | +1.5 | 1.12 | 0.6073 |
| 14 | Cold | momentum_trend_last_10m_non_positive | no_goal_60_80 | DESCARTAR | 197 | 55.3% | +1.1 | 1.10 | 0.6808 |
| 15 | Cold | shots_last_10m_low | no_goal_60_80 | DESCARTAR | 166 | 54.8% | +0.6 | 1.04 | 0.8364 |
| 16 | Cold | cold_game_2of4 | no_goal_60_80 | DESCARTAR | 170 | 54.7% | +0.5 | 1.04 | 0.9176 |
| 17 | Cold | xg_last_10m_low | no_goal_60_75 | DESCARTAR | 95 | 63.2% | +0.3 | 1.02 | 1.0000 |
| 18 | Hot | hot_game_2of4 | goal_60_80 | DESCARTAR | 148 | 45.9% | +0.2 | 1.01 | 1.0000 |
| 19 | Hot | hot_game_2of4 | goal_60_70 | DESCARTAR | 148 | 26.4% | -0.5 | 0.96 | 0.9058 |
| 20 | Hot | momentum_last_10m_avg_high | goal_60_70 | DESCARTAR | 95 | 26.3% | -0.5 | 0.96 | 1.0000 |
| 21 | Hot | shots_last_10m_high | goal_60_75 | DESCARTAR | 122 | 36.1% | -1.0 | 0.94 | 0.8205 |
| 22 | Hot | hot_game_2of4 | goal_60_75 | DESCARTAR | 148 | 35.8% | -1.3 | 0.91 | 0.7441 |
| 23 | Hot | xg_last_10m_high | goal_60_75 | DESCARTAR | 95 | 35.8% | -1.3 | 0.93 | 0.8069 |
| 24 | Hot | shots_last_10m_high | goal_60_70 | DESCARTAR | 122 | 25.4% | -1.4 | 0.90 | 0.7110 |
| 25 | Hot | momentum_last_10m_avg_high | goal_65_80 | DESCARTAR | 95 | 33.7% | -3.2 | 0.83 | 0.5394 |
| 26 | Hot | momentum_last_10m_avg_high | goal_60_75 | DESCARTAR | 95 | 33.7% | -3.4 | 0.82 | 0.4632 |
| 27 | Hot | xg_last_10m_high | goal_60_70 | DESCARTAR | 95 | 23.2% | -3.7 | 0.77 | 0.4226 |
| 28 | Hot | momentum_last_10m_avg_high | goal_60_80 | DESCARTAR | 95 | 41.1% | -4.7 | 0.77 | 0.3416 |
| 29 | Cold | momentum_last_10m_avg_low | no_goal_60_75 | DESCARTAR | 95 | 56.8% | -6.1 | 0.71 | 0.1778 |
| 30 | Cold | momentum_last_10m_avg_low | no_goal_60_80 | DESCARTAR | 95 | 47.4% | -6.8 | 0.69 | 0.1245 |

## Leitura Dos Resultados

- Melhor hot signal: `shots_last_10m_high` em `goal_65_80` com diff=+4.1 p.p. e classificacao `OBSERVAR`.
- Melhor cold signal: `momentum_trend_last_10m_non_positive` em `no_goal_60_75` com diff=+3.6 p.p. e classificacao `OBSERVAR`.
- Sinais PROMISSORA: 0.
- Sinais OBSERVAR: 5.
- Existem sinais para observacao, mas nao ha evidencia suficiente para autorizar baseline/backtesting sem revisao Quant.

## Regras Anti-Leakage Confirmadas

- Nenhuma feature usou eventos apos o minuto 60.
- Targets usam apenas gols dentro da janela posterior definida.
- Placar final nao foi usado como feature.
- Estatisticas full-match nao foram usadas como feature.
- Odds live nao foram usadas.
- Nenhum modelo, baseline, backtesting ou producao foi executado.

## Limitacoes

- A analise usa uma unica temporada EPL 2024/25.
- P-values nao foram ajustados para multipla testagem.
- Sem odds live, a conclusao permitida e apenas sobre sinal estatistico de evento, nao sobre valor esperado de trade.
- Minutos de gols seguem a granularidade disponivel no SofaScore incidents.

## Recomendacao Quant

- Revisar sinais OBSERVAR e considerar filtros moderadores apenas se Quant entender que a interpretacao e coerente. Nao executar baseline/backtesting ainda.
