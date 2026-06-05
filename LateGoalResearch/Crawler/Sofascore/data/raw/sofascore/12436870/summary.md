# SofaScore Endpoint Discovery - 12436870

## Escopo

Discovery controlado em uma unica partida da Premier League ja coletada localmente.

Nao altera banco, schema, importers, datasets, features, baselines, modelagem ou coletores existentes.

## Partida

- event_id: `12436870`
- home_team: Manchester United
- away_team: Fulham
- status: Ended

## Resultado Geral

- Endpoints planejados/testados: 20
- HTTP 403: nao

## Matriz de Endpoints

| Endpoint | Status | Classificacao | Resumo | Arquivo |
|---|---:|---|---|---|
| `graph` | 200 | useful | root_type=object; graph_points_count=92; has_minute_like_field=True; keys=graphPoints,overtimeLength,periodCount,periodTime | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\responses\graph.json` |
| `shotmap` | 200 | useful | root_type=object; shotmap_count=24; has_minute_like_field=True; keys=shotmap | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\responses\shotmap.json` |
| `statistics` | 200 | useful | root_type=object; statistics_count=3; has_minute_like_field=False; keys=statistics | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\responses\statistics.json` |
| `statistics_overall` | 404 | not_found |  | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\errors\statistics_overall.json` |
| `statistics_period_1` | 404 | not_found |  | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\errors\statistics_period_1.json` |
| `statistics_period_2` | 404 | not_found |  | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\errors\statistics_period_2.json` |
| `incidents` | 200 | useful | root_type=object; incidents_count=20; has_minute_like_field=True; keys=away,home,incidents | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\responses\incidents.json` |
| `lineups` | 200 | useful | root_type=object; has_minute_like_field=False; keys=away,confirmed,home,statisticalVersion | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\responses\lineups.json` |
| `lineups_confirmed` | 404 | not_found |  | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\errors\lineups_confirmed.json` |
| `player_statistics` | 404 | not_found |  | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\errors\player_statistics.json` |
| `players_statistics` | 404 | not_found |  | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\errors\players_statistics.json` |
| `heatmap` | 404 | not_found |  | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\errors\heatmap.json` |
| `average_positions` | 200 | useful | root_type=object; has_minute_like_field=True; keys=away,home,substitutions | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\responses\average_positions.json` |
| `momentum` | 404 | not_found |  | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\errors\momentum.json` |
| `attack_momentum` | 404 | not_found |  | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\errors\attack_momentum.json` |
| `win_probability` | 404 | not_found |  | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\errors\win_probability.json` |
| `votes` | 200 | useful | root_type=object; has_minute_like_field=False; keys=bothTeamsToScoreVote,firstTeamToScoreVote,vote,whoShouldHaveWonVote | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\responses\votes.json` |
| `details` | 404 | not_found |  | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\errors\details.json` |
| `best_players` | 200 | useful | root_type=object; has_minute_like_field=False; keys=bestAwayTeamPlayer,bestHomeTeamPlayer | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\responses\best_players.json` |
| `managers` | 200 | useful | root_type=object; has_minute_like_field=False; keys=awayManager,homeManager | `C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\endpoint_discovery\12436870\responses\managers.json` |

## Endpoints uteis

- `graph` -> root_type=object; graph_points_count=92; has_minute_like_field=True; keys=graphPoints,overtimeLength,periodCount,periodTime
- `shotmap` -> root_type=object; shotmap_count=24; has_minute_like_field=True; keys=shotmap
- `statistics` -> root_type=object; statistics_count=3; has_minute_like_field=False; keys=statistics
- `incidents` -> root_type=object; incidents_count=20; has_minute_like_field=True; keys=away,home,incidents
- `lineups` -> root_type=object; has_minute_like_field=False; keys=away,confirmed,home,statisticalVersion
- `average_positions` -> root_type=object; has_minute_like_field=True; keys=away,home,substitutions
- `votes` -> root_type=object; has_minute_like_field=False; keys=bothTeamsToScoreVote,firstTeamToScoreVote,vote,whoShouldHaveWonVote
- `best_players` -> root_type=object; has_minute_like_field=False; keys=bestAwayTeamPlayer,bestHomeTeamPlayer
- `managers` -> root_type=object; has_minute_like_field=False; keys=awayManager,homeManager

## Endpoints vazios

- Nenhum

## Endpoints inexistentes/404

- `statistics_overall` -> 
- `statistics_period_1` -> 
- `statistics_period_2` -> 
- `lineups_confirmed` -> 
- `player_statistics` -> 
- `players_statistics` -> 
- `heatmap` -> 
- `momentum` -> 
- `attack_momentum` -> 
- `win_probability` -> 
- `details` -> 

## Endpoints com texto nao JSON

- Nenhum

## Endpoints com erro

- Nenhum

## Endpoints bloqueados

- Nenhum

## Interpretacao Inicial

Endpoints com `has_minute_like_field=true`, listas temporais ou chaves como `graphPoints`, `incidents` ou `shotmap` devem ser revisados pelo Data Acquisition/CTO antes de qualquer decisao arquitetural.

Este discovery nao promove nenhum endpoint a fonte oficial e nao autoriza importer, feature engineering ou dataset H8.

## Restricoes Respeitadas

- Apenas 1 event_id foi usado.
- Lista fixa de ate 20 endpoints candidatos.
- Sem brute force ou variacoes infinitas.
- Sem paralelismo.
- Sem rotacao de IP ou bypass agressivo.
- Sem sobrescrever JSON valido existente.
