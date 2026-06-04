# DATA FLOW

## Fluxo Geral

### Understat

Understat API
↓
matches
↓
team_match_stats

### FotMob

FotMob API
↓
fotmob_raw_matches
↓
events_v2
↓
snapshots
↓
results

### SofaScore

SofaScore API
↓
match_mapping
↓
matches_master
↓
match_statistics
↓
match_incidents
↓
match_graph

## Integração Multi-Fonte

Todas as fontes
↓
Feature Engineering
↓
Dataset Analítico
↓
Pesquisa Quantitativa
↓
Modelagem
↓
Backtesting
↓
Operação

## Objetivo Final

Identificar padrões estatísticos capazes de antecipar gols tardios com valor operacional para trading esportivo.
