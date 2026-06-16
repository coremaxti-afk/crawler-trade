# RUN_SPORTMONKS_FULL_SEASON_COLLECTOR_SIMPLIFICADO

## Objetivo

Runner simplificado para coletar dados SportMonks por temporada.

Na maioria dos casos, basta informar:

```text
--season-id
```

Por seguranca, tambem e possivel informar:

```text
--league-id
--season-id
```

Se algum `season_id` for ambiguo, o runner vai pedir `--league-id`.

## Script

```text
C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py
```

## Conferir sem coletar

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py `
  --season-id 25659 `
  --dry-run
```

## Coletar H8 da LaLiga 2025/26

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py `
  --league-id 564 `
  --season-id 25659
```

O padrao e:

```text
--categories h8
```

## Coletar todas as categorias

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py `
  --league-id 564 `
  --season-id 25659 `
  --categories all
```

## Teste com poucos jogos

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py `
  --league-id 564 `
  --season-id 25659 `
  --fixture-limit 3 `
  --max-requests 50
```

## Forcar recoleta

Use apenas se quiser sobrescrever JSONs ja existentes:

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py `
  --league-id 564 `
  --season-id 25659 `
  --force
```

## Saida

A coleta salva em:

```text
C:\LateGoalResearch\data\raw\sportmonks\full_collection\<pais>_<liga>_league_<league_id>_season_<season_id>_<season_label>
```

Exemplo:

```text
C:\LateGoalResearch\data\raw\sportmonks\full_collection\spain_la_liga_league_564_season_25659_2025_2026
```

## Ordem recomendada com os outros runners

1. Coletar SportMonks:

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py --league-id 564 --season-id 25659
```

2. Baixar odds Football-Data:

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py --league-id 564 --season-id 25659
```

3. Rodar discovery V2:

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py --league-id 564 --season-id 25659
```

4. Rodar drawdown:

```powershell
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py --league-id 564 --season-id 25659
```
