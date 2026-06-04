# TABLE MATCH_INCIDENTS

## Origem

SofaScore
/api/v1/event/{event_id}/incidents

## Objetivo

Armazenar a timeline dos eventos da partida.

## Relacionamento

match_id -> matches_master.match_id

## Campos Confirmados

- id
- sofascore_event_id
- minute
- incident_type
- is_home
- player_name
- home_score
- away_score
- match_id

## Eventos Esperados

- Goals
- Cards
- Substitutions
- Penalties
- VAR
- Match Periods