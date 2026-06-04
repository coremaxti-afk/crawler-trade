# TABLE MATCH_GRAPH

## Origem

SofaScore
/api/v1/event/{event_id}/graph

## Objetivo

Armazenar os pontos de momentum minuto a minuto.

## Relacionamento

match_id -> matches_master.match_id

## Campos Esperados

- minute
- value

## Status

Coleta ainda não implementada.

Observação:

A tabela foi criada antecipadamente para suportar:

- H8 Momentum e Pressão Temporal
- H5 Pressão Ofensiva In-Game

## Utilização

Modelagem temporal.
Análise de pressão ofensiva.
Identificação de cenários de gol tardio.