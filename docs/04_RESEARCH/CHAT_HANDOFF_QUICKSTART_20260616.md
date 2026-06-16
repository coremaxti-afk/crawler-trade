# CHAT_HANDOFF_QUICKSTART_20260616

## Projeto real

```text
C:\LateGoalResearch
```

Abrir o proximo chat diretamente nessa pasta para normalizar Git e commits.

## Mapas principais

```text
C:\LateGoalResearch\data\raw\sportmonks\league_season_map\league_last_3_seasons.json
C:\LateGoalResearch\data\raw\football_data\football_data_league_odds_map.csv
```

## Runners principais

SportMonks collector:

```text
C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py
```

Football-Data odds:

```text
C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py
```

Discovery V2:

```text
C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py
```

Drawdown:

```text
C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py
```

## Comandos prontos

LaLiga 2025/26:

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py --league-id 564 --season-id 25659
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py --league-id 564 --season-id 25659
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py --league-id 564 --season-id 25659
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py --league-id 564 --season-id 25659
```

LaLiga 2024/25:

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py --league-id 564 --season-id 23621
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py --league-id 564 --season-id 23621
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py --league-id 564 --season-id 23621
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py --league-id 564 --season-id 23621
```

## Ajustes importantes ja feitos

- `discovery_v2 editado` com tempos/targets expandidos.
- Aliases da LaLiga corrigidos; `missing_odds` caiu para `0`.
- CSVs ajustados para Excel PT-BR com `;` e `utf-8-sig`.
- Drawdown agora usa todas as estrategias por padrao, nao so Top 10.
- Targets com fim antes de `90` usam `CASHOUT_ESTIMADO`.

## Arquivos-chave gerados

Discovery LaLiga 25/26:

```text
C:\LateGoalResearch\data\processed\reports\sportmonks_team_side_strategy_discovery_summary_v2_la_liga_2025_26_tempos_expandidos.csv
C:\LateGoalResearch\data\processed\reports\sportmonks_team_side_strategy_discovery_entries_v2_la_liga_2025_26_tempos_expandidos.csv
C:\LateGoalResearch\docs\04_RESEARCH\SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V2_LA_LIGA_2025_26_TEMPOS_EXPANDIDOS.md
```

Drawdown LaLiga 25/26:

```text
C:\LateGoalResearch\data\processed\reports\strategy_drawdown_summary_la_liga_2025_26_tempos_expandidos.csv
C:\LateGoalResearch\data\processed\reports\strategy_drawdown_trades_la_liga_2025_26_tempos_expandidos.csv
```

## Referencias uteis

Handoff tecnico completo:

```text
C:\LateGoalResearch\docs\04_RESEARCH\CHAT_HANDOFF_TECHNICAL_SUMMARY_20260616.md
```

Guia consolidado dos runners:

```text
C:\LateGoalResearch\docs\04_RESEARCH\TUTORIAL SCRIPTS\RUNNERS_OPERACIONAIS_COLETA_E_DISCOVERY.md
```
