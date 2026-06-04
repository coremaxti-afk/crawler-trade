# TABLE EVENTS_V2

## Origem

FotMob

## Objetivo

Armazenar eventos detalhados da partida.

## Principais Campos

- minute
- minute_added
- event_type
- team_id
- player_name
- xg
- is_on_target
- shot_type
- situation

## Papel Arquitetural

FotMob Events
→ Snapshot Builder
→ Snapshots
→ Modelagem
