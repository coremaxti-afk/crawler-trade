# TABLE MATCHES_MASTER

## Objetivo

Tabela mestre de identificação das partidas do projeto.

## Chave Primária

match_id

## Campos Principais

- match_id
- understat_match_id
- sofascore_event_id
- league
- season
- match_date
- home_team
- away_team
- home_goals
- away_goals
- home_xg
- away_xg
- forecast_home
- forecast_draw
- forecast_away

## Papel Arquitetural

Esta tabela funciona como camada central de integração entre Understat, FotMob e SofaScore.

## Relacionamentos

matches_master
├── match_statistics
├── match_incidents
└── match_graph
