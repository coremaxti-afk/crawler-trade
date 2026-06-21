# ANALISE_REGIME_POR_FASE_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS

## 1. Objetivo

Estudo exploratorio para medir como direcoes de mercado, familias e variacoes se comportam em blocos cronologicos da temporada.
Nao e previsao futura, nao aprova operacao e nao define rodada ideal de entrada.

## 2. Reaproveitamento de Codigo

- Scripts semelhantes analisados: agrupamento_por_familia_e_variacoes_v1.py, validacao_preditiva_da_estrategia_v1.py, calc_strategy_drawdown.py.
- Funcoes/lógicas reaproveitadas: market_direction, make_variant_id, leitura automatica de CSV, drawdown por ordem temporal, max_losing_streak e normalizacao temporal por fixture_date_parsed/round/temporal_order_rank.
- Pontos com implementacao nova: divisao cronologica em fases 6 e 8, classificacao exploratoria por regime e consolidados por fase.

## 3. Fontes usadas

- Trades DD: `C:\LateGoalResearch\data\processed\reports\drawdown\strategy_drawdown_trades_serie_a_2025_tempos_expandidos.csv`
- Summary DD: `C:\LateGoalResearch\data\processed\reports\drawdown\strategy_drawdown_summary_serie_a_2025_tempos_expandidos.csv`
- Agrupamento por familia: `C:\LateGoalResearch\data\processed\reports\agrupamento_por_familia_e_variacoes_v1\agrupamento_por_familia_e_variacoes_v1_serie_a_2025_tempos_expandidos.csv`

## 4. Qualidade dos dados

- Total trades: `77661`
- Total fixtures: `380`
- Datas disponiveis: `2025-03-29 21:30:00 -> 2025-12-07 19:00:00`
- temporal_order_rank disponivel: `SIM`
- Campos presentes: `fixture_id, strategy_name, target, cutoff, window, market_type, settlement, profit, fixture_date_parsed, fixture_round, temporal_order_rank, league_label, season_label, season_id, league_id`
- Campos ausentes: `stake`
- `OVERLAP_ALTO_NAO_SOMAR_VARIACOES`
- `docs/00_AGENTS/GOVERNANCE_V2.md nao encontrado no workspace com este nome.`
- `docs/04_RESEARCH/FRENTES_DE_PESQUISA_PRE_RANKING_OPERACIONAL_FINAL_V1.md nao encontrado no workspace com este nome.`

## 5. Mapa das fases

| phase_count | phase_number | phase_start_round | phase_end_round | phase_start_date | phase_end_date | fixtures_na_fase |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | 1 | 1 | 64 | 2025-03-29 21:30:00 | 2025-05-03 21:30:00 | 64 |
| 6 | 2 | 65 | 127 | 2025-05-04 00:00:00 | 2025-07-16 23:00:00 | 63 |
| 6 | 3 | 128 | 190 | 2025-07-17 00:30:00 | 2025-08-23 19:00:00 | 63 |
| 6 | 4 | 191 | 254 | 2025-08-23 21:30:00 | 2025-10-04 21:30:00 | 64 |
| 6 | 5 | 255 | 317 | 2025-10-04 21:30:00 | 2025-11-07 00:30:00 | 63 |
| 6 | 6 | 318 | 380 | 2025-11-08 19:00:00 | 2025-12-07 19:00:00 | 63 |
| 8 | 1 | 1 | 48 | 2025-03-29 21:30:00 | 2025-04-20 21:30:00 | 48 |
| 8 | 2 | 49 | 95 | 2025-04-20 23:30:00 | 2025-05-25 19:00:00 | 47 |
| 8 | 3 | 96 | 143 | 2025-05-25 19:00:00 | 2025-07-23 22:30:00 | 48 |
| 8 | 4 | 144 | 190 | 2025-07-24 00:30:00 | 2025-08-23 19:00:00 | 47 |
| 8 | 5 | 191 | 238 | 2025-08-23 21:30:00 | 2025-09-28 19:00:00 | 48 |
| 8 | 6 | 239 | 285 | 2025-09-28 19:00:00 | 2025-10-21 00:30:00 | 47 |
| 8 | 7 | 286 | 333 | 2025-10-22 22:00:00 | 2025-11-19 22:30:00 | 48 |
| 8 | 8 | 334 | 380 | 2025-11-20 00:30:00 | 2025-12-07 19:00:00 | 47 |

## 6. Resultado por direcao de mercado

| market_direction | phase_count | phase_number | N_fase | profit_fase | ROI_fase | max_drawdown_fase |
| --- | --- | --- | --- | --- | --- | --- |
| goal | 6 | 1 | 8681 | -103007.3764 | -0.1187 | -103007.3764 |
| no_goal | 6 | 1 | 3434 | 56082.5541 | 0.1633 | -11792.0012 |
| goal | 6 | 2 | 9096 | -115203.0866 | -0.1267 | -133687.6226 |
| no_goal | 6 | 2 | 2994 | 35593.2821 | 0.1189 | -18548.8197 |
| goal | 6 | 3 | 10358 | -49258.9420 | -0.0476 | -64985.2350 |
| no_goal | 6 | 3 | 3140 | 7360.2513 | 0.0234 | -17865.0838 |
| goal | 6 | 4 | 10288 | -211526.8540 | -0.2056 | -211526.8540 |
| no_goal | 6 | 4 | 3492 | 103338.0963 | 0.2959 | -11300.1462 |
| goal | 6 | 5 | 9672 | -64328.4816 | -0.0665 | -128396.2484 |
| no_goal | 6 | 5 | 3550 | 75609.7807 | 0.2130 | -15699.7441 |
| goal | 6 | 6 | 10218 | -68001.9235 | -0.0666 | -83187.9820 |
| no_goal | 6 | 6 | 2738 | 6687.7262 | 0.0244 | -28401.6860 |
| goal | 8 | 1 | 6337 | -60682.1205 | -0.0958 | -60998.7242 |
| no_goal | 8 | 1 | 2452 | 44205.6975 | 0.1803 | -11792.0012 |
| goal | 8 | 2 | 6512 | -101091.4555 | -0.1552 | -101231.1570 |
| no_goal | 8 | 2 | 2326 | 31153.5014 | 0.1339 | -12734.6817 |
| goal | 8 | 3 | 7174 | -77736.4707 | -0.1084 | -77736.4707 |
| no_goal | 8 | 3 | 2166 | 11023.1191 | 0.0509 | -31951.1042 |
| goal | 8 | 4 | 8112 | -27959.3583 | -0.0345 | -55099.2608 |
| no_goal | 8 | 4 | 2624 | 12653.7694 | 0.0482 | -17865.0838 |
| goal | 8 | 5 | 7723 | -178283.1861 | -0.2308 | -182645.3310 |
| no_goal | 8 | 5 | 2662 | 93298.3003 | 0.3505 | -11300.1462 |
| goal | 8 | 6 | 7260 | -57025.0477 | -0.0785 | -70362.5180 |
| no_goal | 8 | 6 | 2414 | 38104.1563 | 0.1578 | -9200.1614 |
| goal | 8 | 7 | 7757 | -70168.1968 | -0.0905 | -72125.4513 |
| no_goal | 8 | 7 | 2354 | 53685.6229 | 0.2281 | -15699.7441 |
| goal | 8 | 8 | 7438 | -38380.8285 | -0.0516 | -62335.3488 |
| no_goal | 8 | 8 | 2350 | 547.5236 | 0.0023 | -28401.6860 |

## 7. Top familias mais consistentes

| strategy_family | phase_count | consistencia_por_fase | profit_total | ROI_total | classificacao_exploratoria |
| --- | --- | --- | --- | --- | --- |
| opponent_no_big_chances__no_goal | 6 | 1.0000 | 76259.7639 | 0.1455 | CONSISTENTE_MULTI_FASE |
| opponent_no_big_chances__no_goal | 8 | 1.0000 | 76259.7639 | 0.1455 | CONSISTENTE_MULTI_FASE |
| team_winning_by_1_no_sot_against__no_goal | 8 | 1.0000 | 51407.3378 | 0.1273 | CONSISTENTE_MULTI_FASE |
| opponent_no_recent_key_passes__no_goal | 6 | 1.0000 | 40164.2507 | 0.1418 | CONSISTENTE_MULTI_FASE |
| opponent_no_recent_key_passes__no_goal | 8 | 1.0000 | 40164.2507 | 0.1418 | CONSISTENTE_MULTI_FASE |
| favorite_winning_by_1_opp_cold_2of3__no_goal | 6 | 1.0000 | 38886.9540 | 0.2392 | CONSISTENTE_MULTI_FASE |
| favorite_winning_by_1_opp_cold_2of3__no_goal | 8 | 1.0000 | 38886.9540 | 0.2392 | CONSISTENTE_MULTI_FASE |
| team_winning_by_1_opp_cold_2of3__no_goal | 6 | 1.0000 | 38126.4377 | 0.1574 | CONSISTENTE_MULTI_FASE |
| team_winning_by_1_opp_cold_2of3__no_goal | 8 | 0.8750 | 38126.4377 | 0.1574 | CONSISTENTE_MULTI_FASE |
| team_winning_by_1_low_dangerous_attacks_against__no_goal | 8 | 0.8750 | 12249.2019 | 0.0931 | CONSISTENTE_MULTI_FASE |
| team_winning_by_1_no_sot_against__no_goal | 6 | 0.8333 | 51407.3378 | 0.1273 | CONSISTENTE_MULTI_FASE |
| both_teams_cold_2of3__no_goal | 6 | 0.8333 | 27577.7444 | 0.1472 | CONSISTENTE_MULTI_FASE |
| both_teams_cold_2of3__no_goal | 8 | 0.7500 | 27577.7444 | 0.1472 | CONSISTENTE_MULTI_FASE |
| team_winning_by_1_low_dangerous_attacks_against__no_goal | 6 | 0.6667 | 12249.2019 | 0.0931 | INSTAVEL_POR_FASE |
| away_winning_by_1_home_pressing__goal | 6 | 0.3333 | -12388.4460 | -0.0725 | NEGATIVA_MULTI_FASE |
| favorite_losing_pressure_high_2of3__goal | 6 | 0.3333 | -13149.9066 | -0.0764 | NEGATIVA_MULTI_FASE |
| underdog_winning_favorite_pressing_2of3__goal | 6 | 0.3333 | -13149.9066 | -0.0764 | NEGATIVA_MULTI_FASE |
| away_winning_by_1_home_pressing__goal | 8 | 0.2500 | -12388.4460 | -0.0725 | NEGATIVA_MULTI_FASE |
| favorite_losing_pressure_high_2of3__goal | 8 | 0.2500 | -13149.9066 | -0.0764 | NEGATIVA_MULTI_FASE |
| underdog_winning_favorite_pressing_2of3__goal | 8 | 0.2500 | -13149.9066 | -0.0764 | NEGATIVA_MULTI_FASE |

## 8. Familias dependentes de regime

| strategy_family | phase_count | pct_lucro_melhor_fase | profit_total | ROI_total | classificacao_exploratoria |
| --- | --- | --- | --- | --- | --- |
| team_winning_by_1_low_dangerous_attacks_against__no_goal | 6 | 0.4797 | 12249.2019 | 0.0931 | INSTAVEL_POR_FASE |
| both_teams_cold_2of3__no_goal | 6 | 0.4644 | 27577.7444 | 0.1472 | CONSISTENTE_MULTI_FASE |
| team_winning_by_1_no_sot_against__no_goal | 6 | 0.4406 | 51407.3378 | 0.1273 | CONSISTENTE_MULTI_FASE |
| team_winning_by_1_low_dangerous_attacks_against__no_goal | 8 | 0.4225 | 12249.2019 | 0.0931 | CONSISTENTE_MULTI_FASE |
| team_winning_by_1_no_sot_against__no_goal | 8 | 0.4151 | 51407.3378 | 0.1273 | CONSISTENTE_MULTI_FASE |
| both_teams_cold_2of3__no_goal | 8 | 0.4125 | 27577.7444 | 0.1472 | CONSISTENTE_MULTI_FASE |
| opponent_no_big_chances__no_goal | 6 | 0.4029 | 76259.7639 | 0.1455 | CONSISTENTE_MULTI_FASE |
| team_winning_by_1_opp_cold_2of3__no_goal | 6 | 0.3684 | 38126.4377 | 0.1574 | CONSISTENTE_MULTI_FASE |
| opponent_no_big_chances__no_goal | 8 | 0.3521 | 76259.7639 | 0.1455 | CONSISTENTE_MULTI_FASE |
| opponent_no_recent_key_passes__no_goal | 6 | 0.3470 | 40164.2507 | 0.1418 | CONSISTENTE_MULTI_FASE |
| team_winning_by_1_opp_cold_2of3__no_goal | 8 | 0.3411 | 38126.4377 | 0.1574 | CONSISTENTE_MULTI_FASE |
| favorite_winning_by_1_opp_cold_2of3__no_goal | 6 | 0.3117 | 38886.9540 | 0.2392 | CONSISTENTE_MULTI_FASE |
| opponent_no_recent_key_passes__no_goal | 8 | 0.3102 | 40164.2507 | 0.1418 | CONSISTENTE_MULTI_FASE |
| favorite_winning_by_1_opp_cold_2of3__no_goal | 8 | 0.2945 | 38886.9540 | 0.2392 | CONSISTENTE_MULTI_FASE |
| away_winning_by_1_home_pressing__goal | 6 | 0.0000 | -12388.4460 | -0.0725 | NEGATIVA_MULTI_FASE |
| away_winning_by_1_home_pressing__goal | 8 | 0.0000 | -12388.4460 | -0.0725 | NEGATIVA_MULTI_FASE |
| favorite_losing_pressure_high_2of3__goal | 6 | 0.0000 | -13149.9066 | -0.0764 | NEGATIVA_MULTI_FASE |
| underdog_winning_favorite_pressing_2of3__goal | 6 | 0.0000 | -13149.9066 | -0.0764 | NEGATIVA_MULTI_FASE |
| favorite_losing_pressure_high_2of3__goal | 8 | 0.0000 | -13149.9066 | -0.0764 | NEGATIVA_MULTI_FASE |
| underdog_winning_favorite_pressing_2of3__goal | 8 | 0.0000 | -13149.9066 | -0.0764 | NEGATIVA_MULTI_FASE |

## 9. Melhor fase por familia

| strategy_family | phase_count | melhor_fase | profit_melhor_fase | ROI_melhor_fase |
| --- | --- | --- | --- | --- |
| opponent_no_big_chances__no_goal | 6 | 4 | 30726.1164 | 0.3036 |
| opponent_no_big_chances__no_goal | 8 | 5 | 26851.7042 | 0.3580 |
| team_winning_by_1_no_sot_against__no_goal | 6 | 4 | 22647.7505 | 0.2957 |
| team_winning_by_1_no_sot_against__no_goal | 8 | 5 | 21341.2671 | 0.3838 |
| team_winning_by_1_opp_cold_2of3__no_goal | 6 | 4 | 14046.3570 | 0.3001 |
| opponent_no_recent_key_passes__no_goal | 6 | 4 | 13938.0034 | 0.2844 |
| team_winning_by_1_opp_cold_2of3__no_goal | 8 | 5 | 13003.4938 | 0.3673 |
| both_teams_cold_2of3__no_goal | 6 | 1 | 12807.5267 | 0.2737 |
| opponent_no_recent_key_passes__no_goal | 8 | 5 | 12458.2912 | 0.3480 |
| favorite_winning_by_1_opp_cold_2of3__no_goal | 6 | 5 | 12120.0061 | 0.4179 |
| favorite_winning_by_1_opp_cold_2of3__no_goal | 8 | 5 | 11452.0043 | 0.3922 |
| both_teams_cold_2of3__no_goal | 8 | 2 | 11374.5126 | 0.2562 |
| team_winning_by_1_low_dangerous_attacks_against__no_goal | 6 | 5 | 5875.6838 | 0.2490 |
| team_winning_by_1_low_dangerous_attacks_against__no_goal | 8 | 5 | 5175.2543 | 0.2614 |
| home_winning_by_1_visitor_pressing__goal | 6 | 3 | 4026.6941 | 0.0873 |
| home_winning_by_1_visitor_pressing__goal | 8 | 4 | 3914.3177 | 0.1027 |
| away_winning_by_1_home_pressing__goal | 8 | 2 | 3381.6778 | 0.2663 |
| favorite_losing_pressure_high_2of3__goal | 8 | 2 | 2645.7189 | 0.1825 |
| underdog_winning_favorite_pressing_2of3__goal | 8 | 2 | 2645.7189 | 0.1825 |
| away_winning_by_1_home_pressing__goal | 6 | 5 | 2612.6383 | 0.0954 |

## 10. Pior fase por familia

| strategy_family | phase_count | pior_fase | profit_pior_fase | ROI_pior_fase |
| --- | --- | --- | --- | --- |
| corners_recent_high__goal | 6 | 4 | -43017.9993 | -0.2041 |
| shots_on_target_recent__goal | 6 | 4 | -36061.2874 | -0.2134 |
| dangerous_attacks_accelerating__goal | 6 | 4 | -34545.3168 | -0.2206 |
| corners_recent_high__goal | 8 | 5 | -33882.9140 | -0.2061 |
| key_passes_recent_high__goal | 6 | 4 | -33172.2317 | -0.1995 |
| key_passes_recent_high__goal | 8 | 5 | -29595.1980 | -0.2301 |
| shots_on_target_recent__goal | 8 | 5 | -28537.1825 | -0.2281 |
| dangerous_attacks_accelerating__goal | 8 | 5 | -27586.3920 | -0.2308 |
| big_chances_recent__goal | 8 | 2 | -17156.8570 | -0.3452 |
| big_chances_recent__goal | 6 | 4 | -14826.6403 | -0.1635 |
| team_losing_pressure_high_2of3__goal | 6 | 4 | -14773.8161 | -0.2466 |
| team_losing_pressure_high_2of3__goal | 8 | 5 | -13844.0029 | -0.2908 |
| favorite_drawing_pressure_high_2of3__goal | 8 | 2 | -9610.3559 | -0.2150 |
| home_winning_by_1_visitor_pressing__goal | 6 | 4 | -9456.0006 | -0.2814 |
| favorite_drawing_pressure_high_2of3__goal | 6 | 2 | -9053.7537 | -0.1943 |
| favorite_losing_pressure_high_2of3__goal | 8 | 5 | -8790.0492 | -0.3268 |
| underdog_winning_favorite_pressing_2of3__goal | 8 | 5 | -8790.0492 | -0.3268 |
| away_winning_by_1_home_pressing__goal | 6 | 4 | -7676.7677 | -0.2132 |
| favorite_losing_pressure_high_2of3__goal | 6 | 4 | -7359.5401 | -0.2121 |
| underdog_winning_favorite_pressing_2of3__goal | 6 | 4 | -7359.5401 | -0.2121 |

## 11. Over/Goal por fase

| market_direction | phase_count | phase_number | profit_fase | ROI_fase | max_drawdown_fase |
| --- | --- | --- | --- | --- | --- |
| goal | 6 | 1 | -103007.3764 | -0.1187 | -103007.3764 |
| goal | 6 | 2 | -115203.0866 | -0.1267 | -133687.6226 |
| goal | 6 | 3 | -49258.9420 | -0.0476 | -64985.2350 |
| goal | 6 | 4 | -211526.8540 | -0.2056 | -211526.8540 |
| goal | 6 | 5 | -64328.4816 | -0.0665 | -128396.2484 |
| goal | 6 | 6 | -68001.9235 | -0.0666 | -83187.9820 |
| goal | 8 | 1 | -60682.1205 | -0.0958 | -60998.7242 |
| goal | 8 | 2 | -101091.4555 | -0.1552 | -101231.1570 |
| goal | 8 | 3 | -77736.4707 | -0.1084 | -77736.4707 |
| goal | 8 | 4 | -27959.3583 | -0.0345 | -55099.2608 |
| goal | 8 | 5 | -178283.1861 | -0.2308 | -182645.3310 |
| goal | 8 | 6 | -57025.0477 | -0.0785 | -70362.5180 |
| goal | 8 | 7 | -70168.1968 | -0.0905 | -72125.4513 |
| goal | 8 | 8 | -38380.8285 | -0.0516 | -62335.3488 |

## 12. No Goal/Lay Over por fase

| market_direction | phase_count | phase_number | profit_fase | ROI_fase | max_drawdown_fase |
| --- | --- | --- | --- | --- | --- |
| no_goal | 6 | 1 | 56082.5541 | 0.1633 | -11792.0012 |
| no_goal | 6 | 2 | 35593.2821 | 0.1189 | -18548.8197 |
| no_goal | 6 | 3 | 7360.2513 | 0.0234 | -17865.0838 |
| no_goal | 6 | 4 | 103338.0963 | 0.2959 | -11300.1462 |
| no_goal | 6 | 5 | 75609.7807 | 0.2130 | -15699.7441 |
| no_goal | 6 | 6 | 6687.7262 | 0.0244 | -28401.6860 |
| no_goal | 8 | 1 | 44205.6975 | 0.1803 | -11792.0012 |
| no_goal | 8 | 2 | 31153.5014 | 0.1339 | -12734.6817 |
| no_goal | 8 | 3 | 11023.1191 | 0.0509 | -31951.1042 |
| no_goal | 8 | 4 | 12653.7694 | 0.0482 | -17865.0838 |
| no_goal | 8 | 5 | 93298.3003 | 0.3505 | -11300.1462 |
| no_goal | 8 | 6 | 38104.1563 | 0.1578 | -9200.1614 |
| no_goal | 8 | 7 | 53685.6229 | 0.2281 | -15699.7441 |
| no_goal | 8 | 8 | 547.5236 | 0.0023 | -28401.6860 |

## 13. Alertas metodologicos

- Estudo exploratorio: nao usar como previsao futura.
- Nao somar lucro de variacoes com sobreposicao alta como se fossem independentes.
- Fase forte isolada pode indicar concentracao de lucro e dependencia de regime.
- Mudanca de regime historica nao equivale a confirmacao operacional futura.

## 14. Parecer exploratorio

- Mercado Goal muda de regime: `NAO_EVIDENTE`
- Mercado No Goal muda de regime: `NAO_EVIDENTE`
- Familias mais consistentes identificadas: `13`
- Familias regime dependentes identificadas: `0`
- Existe fase claramente favoravel para Over: `NAO_EVIDENTE`
- Existe fase claramente favoravel para Under/No Goal: `SIM`

## Artefatos

- `C:\LateGoalResearch\data\processed\reports\analise_regime_por_fase_v1\analise_regime_por_fase_v1_phase6_serie_a_2025_tempos_expandidos.csv`
- `C:\LateGoalResearch\data\processed\reports\analise_regime_por_fase_v1\analise_regime_por_fase_v1_phase8_serie_a_2025_tempos_expandidos.csv`
- `C:\LateGoalResearch\data\processed\reports\analise_regime_por_fase_v1\analise_regime_por_fase_v1_resumo_familias_serie_a_2025_tempos_expandidos.csv`
- `C:\LateGoalResearch\data\processed\reports\analise_regime_por_fase_v1\analise_regime_por_fase_v1_resumo_variacoes_serie_a_2025_tempos_expandidos.csv`
- `C:\LateGoalResearch\data\processed\reports\analise_regime_por_fase_v1\analise_regime_por_fase_v1_resumo_market_direction_serie_a_2025_tempos_expandidos.csv`
- `C:\LateGoalResearch\data\processed\reports\analise_regime_por_fase_v1\analise_regime_por_fase_v1_mapa_fases_serie_a_2025_tempos_expandidos.csv`
- `C:\LateGoalResearch\data\processed\reports\analise_regime_por_fase_v1\analise_regime_por_fase_v1_serie_a_2025_tempos_expandidos.json`
- `C:\LateGoalResearch\docs\04_RESEARCH\analise_regime_por_fase_v1\ANALISE_REGIME_POR_FASE_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md`
- `C:\LateGoalResearch\docs\04_RESEARCH\analise_regime_por_fase_v1\COMO_EXECUTAR_ANALISE_REGIME_POR_FASE_V1.md`
