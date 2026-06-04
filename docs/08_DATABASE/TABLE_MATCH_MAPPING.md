# TABLE MATCH_MAPPING

## Objetivo

Realizar a correspondência entre IDs das diferentes fontes de dados.

## Campos Principais

- understat_match_id
- sofascore_event_id
- league
- season
- home_team
- away_team
- match_date

## Papel Arquitetural

Understat Match
↓
Match Mapping
↓
SofaScore Event

## Importância

CRÍTICA

Esta tabela é a base da integração multi-fonte do projeto.
