# RUN_STRATEGY_DISCOVERY_V2_SIMPLIFICADO

## Objetivo

Este wrapper simplifica a execucao do discovery V2.

Antes, era necessario informar manualmente:

```text
--sportmonks-root
--football-data-csv
--season-label
--summary-csv
--entries-csv
--report-md
```

Agora basta informar:

```text
--league-id
--season-id
```

O script resolve o restante usando os mapas locais do projeto.

## Script

```text
C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py
```

## Conferir antes de executar

Use `--dry-run`:

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py `
  --league-id 564 `
  --season-id 25659 `
  --dry-run
```

## Executar LaLiga 2025/26

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py `
  --league-id 564 `
  --season-id 25659
```

## Executar LaLiga 2024/25

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py `
  --league-id 564 `
  --season-id 23621
```

## Executar Premier League 2025/26

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py `
  --league-id 8 `
  --season-id 25583
```

## O que ele usa por baixo

Mapa SportMonks:

```text
C:\LateGoalResearch\data\raw\sportmonks\league_season_map\league_last_3_seasons.json
```

Mapa Football-Data:

```text
C:\LateGoalResearch\data\raw\football_data\football_data_league_odds_map.csv
```

Coletas SportMonks:

```text
C:\LateGoalResearch\data\raw\sportmonks\full_collection\...
```

CSVs Football-Data:

```text
C:\LateGoalResearch\data\raw\football_data\...
```

## Se der erro de Football-Data nao encontrado

Significa que a liga esta no mapa, mas o CSV da temporada ainda nao foi baixado.

Baixe com:

```powershell
python C:\LateGoalResearch\Crawler\FootballData\football_data_odds_collector.py `
  --league-code SP1 `
  --country spain `
  --league-label la_liga `
  --season 2025_2026
```

Troque `league-code`, `country`, `league-label` e `season` conforme o arquivo:

```text
C:\LateGoalResearch\data\raw\football_data\football_data_league_odds_map.csv
```

## Observacao

O wrapper nao altera regra, threshold, estrategia ou calculo. Ele apenas monta caminhos e chama o discovery V2.
