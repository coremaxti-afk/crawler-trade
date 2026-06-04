# PIPELINE

## Visão Geral

### Understat

Understat
↓
matches
team_match_stats

### FotMob

FotMob
↓
events_v2
↓
snapshots
↓
results

### SofaScore

SofaScore
↓
match_mapping
↓
matches_master
↓
match_statistics
match_incidents
match_graph

### Integração

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
Produção

## Princípios

- Dados brutos são preservados.
- Transformações são reproduzíveis.
- Cada etapa deve ser auditável.
- Nenhuma análise utiliza diretamente arquivos RAW.
- Priorizar integração multi-fonte.
