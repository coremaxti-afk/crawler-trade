# snapshot_builder_v2.py

## Tipo

Analytics / Snapshot Builder

## Importância

CRÍTICA

## Objetivo

Construir snapshots minuto a minuto de uma partida para uso em modelos preditivos de gols tardios.

## Entradas

### Banco de Dados

- events_v2

### Arquivos

- matchdetails.json

## Features Geradas por Minuto

- minute
- home_score
- away_score
- home_xg
- away_xg
- home_shots
- away_shots
- home_sot
- away_sot
- momentum

## Saída

Tabela:

snapshots

## Papel Arquitetural

Eventos
→ Snapshot Minuto a Minuto
→ Feature Engineering
→ Modelo Late Goal

## Observações

Este é um dos componentes centrais do projeto.
