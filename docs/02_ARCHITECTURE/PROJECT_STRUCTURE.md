# PROJECT STRUCTURE

## Visão Geral

O projeto está organizado para separar documentação, coleta de dados, armazenamento, pesquisa quantitativa e modelagem.

## Estrutura Principal

```text
LateGoalResearch/
├── Crawler/
├── Database/
├── Analytics/
├── Exports/
└── Config/

/docs
├── 00_AGENTS
├── 01_CONTEXT
├── 02_ARCHITECTURE
├── 03_SOURCES
├── 04_RESEARCH
├── 05_FEATURES
├── 06_SPRINTS
├── 07_OPERATIONS
├── 08_DATABASE
└── 09_CODEBASE
```

## Crawler

Responsável pela coleta de dados.

Fontes:

- Understat
- FotMob
- SofaScore

## Database

Responsável pelo armazenamento consolidado.

Principais tabelas:

- matches
- team_match_stats
- snapshots
- results
- match_mapping
- matches_master
- match_statistics
- match_incidents
- match_graph

## Analytics

Responsável por:

- Feature Engineering
- Pesquisa Quantitativa
- Backtesting
- Modelagem

## Documentação

Toda documentação oficial do projeto está centralizada na pasta docs.
