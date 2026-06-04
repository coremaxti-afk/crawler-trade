# sofascore_collector.py

## Tipo

Collector

## Importância

CRÍTICA

## Objetivo

Coletar os endpoints principais de uma única partida.

## Endpoints

- event
- statistics
- incidents
- lineups
- h2h

## Estrutura de Saída

/event_id/
- event.json
- statistics.json
- incidents.json
- lineups.json
- h2h.json

## Observação

Necessita futura evolução para incluir graph.json.

## Status

Ativo
