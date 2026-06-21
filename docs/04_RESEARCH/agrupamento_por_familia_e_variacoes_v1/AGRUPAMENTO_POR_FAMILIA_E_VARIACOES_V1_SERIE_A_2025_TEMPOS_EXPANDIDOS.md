# AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS

## Status

`APROVADA COMO V1 EXPLORATORIA`

## Objetivo

Agrupar estrategias por familia operacional, identificar variacoes de cutoff/target/window, medir overlap entre variacoes e apontar candidatas principais sem excluir nenhuma variacao das proximas analises.

Este estudo e exploratorio. Ele nao aprova operacao, nao descarta variacoes e nao substitui as proximas frentes do roadmap.

## Fontes usadas

- Trades DD: `C:\LateGoalResearch\data\processed\reports\drawdown\strategy_drawdown_trades_serie_a_2025_tempos_expandidos.csv`
- Summary DD: `C:\LateGoalResearch\data\processed\reports\drawdown\strategy_drawdown_summary_serie_a_2025_tempos_expandidos.csv`
- Rentabilidade por time V4: `C:\LateGoalResearch\data\processed\reports\rentabilidade_das_estrategias_por_time_v4.csv`

## Campos encontrados e campos ausentes

- Campos trades presentes: `fixture_id, season_id, league_id, strategy_name, target, cutoff, window, market_type, settlement, profit`
- Campos trades ausentes: `team_id/team_side`
- Campos summary presentes: `strategy_name, target, cutoff, window, market_type, settlement, profit_final, ROI, max_drawdown_abs, max_losing_streak`
- Campos summary ausentes: `nenhum`

## Resultado geral

- Total de familias: `18`
- Total de variacoes: `714`
- Familias com alta sobreposicao: `18`
- Overlap maximo por fixture: `100%` em todas as familias

## Achado principal

Todas as familias apresentaram alta sobreposicao entre variacoes.

Isso confirma que o projeto nao deve somar lucro de variacoes da mesma familia como se fossem estrategias independentes.

Exemplo de familia com variacoes sobrepostas:

```text
both_teams_cold_2of3 no_goal_60_75
both_teams_cold_2of3 no_goal_60_80
both_teams_cold_2of3 no_goal_60_85
both_teams_cold_2of3 no_goal_60_90
```

Essas linhas podem representar praticamente a mesma oportunidade operacional com cutoff/window/saida diferentes.

## Familias com mais variacoes

| strategy_family | qtd_variacoes | qtd_fixtures_unicos_familia | overlap_max_fixture_pct |
| --- | ---: | ---: | ---: |
| away_winning_by_1_home_pressing__goal | 42 | 71 | 100.0000 |
| big_chances_recent__goal | 42 | 259 | 100.0000 |
| corners_recent_high__goal | 42 | 380 | 100.0000 |
| dangerous_attacks_accelerating__goal | 42 | 352 | 100.0000 |
| favorite_drawing_pressure_high_2of3__goal | 42 | 134 | 100.0000 |
| favorite_losing_pressure_high_2of3__goal | 42 | 89 | 100.0000 |
| home_winning_by_1_visitor_pressing__goal | 42 | 125 | 100.0000 |
| key_passes_recent_high__goal | 42 | 360 | 100.0000 |
| shots_on_target_recent__goal | 42 | 366 | 100.0000 |
| team_losing_pressure_high_2of3__goal | 42 | 227 | 100.0000 |
| underdog_winning_favorite_pressing_2of3__goal | 42 | 89 | 100.0000 |
| both_teams_cold_2of3__no_goal | 36 | 226 | 100.0000 |
| favorite_winning_by_1_opp_cold_2of3__no_goal | 36 | 109 | 100.0000 |
| opponent_no_big_chances__no_goal | 36 | 215 | 100.0000 |
| opponent_no_recent_key_passes__no_goal | 36 | 192 | 100.0000 |
| team_winning_by_1_low_dangerous_attacks_against__no_goal | 36 | 118 | 100.0000 |
| team_winning_by_1_no_sot_against__no_goal | 36 | 206 | 100.0000 |
| team_winning_by_1_opp_cold_2of3__no_goal | 36 | 183 | 100.0000 |

## Melhores variacoes por lucro

| strategy_family | variant_id | N_trades | profit_total | ROI | max_drawdown_abs |
| --- | --- | ---: | ---: | ---: | ---: |
| opponent_no_big_chances__no_goal | opponent_no_big_chances__no_goal_65_90__cutoff_65__window_last_5m | 152 | 3520.0000 | 0.2316 | -580.0000 |
| opponent_no_big_chances__no_goal | opponent_no_big_chances__no_goal_75_90__cutoff_75__window_last_15m | 133 | 3500.0000 | 0.2632 | -600.0000 |
| opponent_no_big_chances__no_goal | opponent_no_big_chances__no_goal_75_90__cutoff_75__window_last_10m | 142 | 3400.0000 | 0.2394 | -600.0000 |
| opponent_no_big_chances__no_goal | opponent_no_big_chances__no_goal_75_90__cutoff_75__window_last_5m | 154 | 3400.0000 | 0.2208 | -600.0000 |
| opponent_no_big_chances__no_goal | opponent_no_big_chances__no_goal_65_90__cutoff_65__window_last_15m | 131 | 3340.0000 | 0.2550 | -540.0000 |
| opponent_no_big_chances__no_goal | opponent_no_big_chances__no_goal_65_90__cutoff_65__window_last_10m | 139 | 3180.0000 | 0.2288 | -660.0000 |
| opponent_no_big_chances__no_goal | opponent_no_big_chances__no_goal_70_90__cutoff_70__window_last_10m | 144 | 3060.0000 | 0.2125 | -760.0000 |
| opponent_no_big_chances__no_goal | opponent_no_big_chances__no_goal_70_90__cutoff_70__window_last_5m | 154 | 2980.0000 | 0.1935 | -740.0000 |
| team_winning_by_1_no_sot_against__no_goal | team_winning_by_1_no_sot_against__no_goal_65_90__cutoff_65__window_last_5m | 132 | 2960.0000 | 0.2242 | -440.0000 |
| opponent_no_recent_key_passes__no_goal | opponent_no_recent_key_passes__no_goal_70_90__cutoff_70__window_last_5m | 121 | 2920.0000 | 0.2413 | -620.0000 |

## Melhores variacoes por ROI

| strategy_family | variant_id | N_trades | profit_total | ROI | max_drawdown_abs |
| --- | --- | ---: | ---: | ---: | ---: |
| both_teams_cold_2of3__no_goal | both_teams_cold_2of3__no_goal_60_90__cutoff_60__window_last_10m | 25 | 1300.0000 | 0.5200 | -100.0000 |
| favorite_winning_by_1_opp_cold_2of3__no_goal | favorite_winning_by_1_opp_cold_2of3__no_goal_65_90__cutoff_65__window_last_10m | 36 | 1840.0000 | 0.5111 | -200.0000 |
| favorite_winning_by_1_opp_cold_2of3__no_goal | favorite_winning_by_1_opp_cold_2of3__no_goal_70_90__cutoff_70__window_last_15m | 38 | 1820.0000 | 0.4789 | -320.0000 |
| favorite_winning_by_1_opp_cold_2of3__no_goal | favorite_winning_by_1_opp_cold_2of3__no_goal_75_90__cutoff_75__window_last_15m | 42 | 1800.0000 | 0.4286 | -500.0000 |
| favorite_winning_by_1_opp_cold_2of3__no_goal | favorite_winning_by_1_opp_cold_2of3__no_goal_65_90__cutoff_65__window_last_5m | 56 | 2400.0000 | 0.4286 | -240.0000 |

## Melhor variacao equilibrada por familia

Formula usada:

```text
score_equilibrado = rank_profit_normalizado * 0.40 + rank_ROI_normalizado * 0.30 + rank_drawdown_normalizado * 0.20 + rank_N_normalizado * 0.10
```

Alerta interpretativo: este score e relativo dentro da familia. Ele nao aprova operacao e nao deve ser usado para comparar familias sem os demais estudos do roadmap.

## Alertas metodologicos

- `profit_total_soma_variacoes` nao deve ser tratado como lucro operacional real quando ha overlap alto.
- `profit_total_sem_somar_overlap` foi definido de forma conservadora como lucro da melhor variacao equilibrada da familia, para evitar soma indevida de oportunidades sobrepostas.
- Nenhuma variacao foi removida; classificacoes sao exploratorias.
- Familias com `overlap_max_fixture_pct >= 70%` foram marcadas com `FAMILIA_COM_ALTA_SOBREPOSICAO` e `NAO_SOMAR_LUCRO_DAS_VARIACOES`.
- `CAMPO_AUSENTE_TRADES_TEAM_ID_OU_TEAM_SIDE`.
- `EXISTEM_FAMILIAS_COM_ALTA_SOBREPOSICAO_NAO_SOMAR_LUCRO`.

## Parecer exploratorio

Este estudo organiza familias e variacoes para reduzir risco de duplicidade nas proximas frentes.

Ele nao aprova operacao final, nao descarta variacoes e nao deve ser usado como ranking operacional definitivo.

As proximas analises devem manter as variacoes disponiveis, mas considerar os alertas de overlap antes de somar lucro ou comparar estrategias como independentes.

## Artefatos

- CSV familias/variacoes: `C:\LateGoalResearch\data\processed\reports\agrupamento_por_familia_e_variacoes_v1\agrupamento_por_familia_e_variacoes_v1_serie_a_2025_tempos_expandidos.csv`
- CSV overlap: `C:\LateGoalResearch\data\processed\reports\agrupamento_por_familia_e_variacoes_v1\agrupamento_overlap_variacoes_v1_serie_a_2025_tempos_expandidos.csv`
- JSON: `C:\LateGoalResearch\data\processed\reports\agrupamento_por_familia_e_variacoes_v1\agrupamento_por_familia_e_variacoes_v1_serie_a_2025_tempos_expandidos.json`
