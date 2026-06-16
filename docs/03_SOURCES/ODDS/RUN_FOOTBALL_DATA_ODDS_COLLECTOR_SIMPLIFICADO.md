# RUN_FOOTBALL_DATA_ODDS_COLLECTOR_SIMPLIFICADO

## Objetivo

Este runner baixa odds Football-Data usando apenas:

```text
--league-id
--season-id
```

Ele consulta os mapas locais do projeto para descobrir:

```text
codigo Football-Data
pais
league-label
temporada
source-type
```

## Script

```text
C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py
```

## Conferir sem baixar

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py `
  --league-id 564 `
  --season-id 25659 `
  --dry-run
```

## Baixar LaLiga 2025/26

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py `
  --league-id 564 `
  --season-id 25659
```

## Baixar LaLiga 2024/25

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py `
  --league-id 564 `
  --season-id 23621
```

## Forcar novo download

Se o arquivo ja existir e voce quiser baixar novamente:

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py `
  --league-id 564 `
  --season-id 25659 `
  --force
```

## Se der erro de liga indisponivel

Significa que a liga nao tem codigo Football-Data confirmado no mapa:

```text
C:\LateGoalResearch\data\raw\football_data\football_data_league_odds_map.csv
```

Nesse caso, a liga precisa de outra fonte de odds ou verificacao manual.
