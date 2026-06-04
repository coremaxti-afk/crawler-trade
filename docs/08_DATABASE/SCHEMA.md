# DATABASE SCHEMA

## Estado Atual

### Implementado

- matches_master
- match_statistics
- match_incidents
- match_graph

### Em Desenvolvimento

- sofascore_importer.py

### Planejado

- analytics_dataset_builder.py
- feature_builder.py

---

## Core Tables

### matches
Fonte principal Understat.

### team_match_stats
Estatísticas avançadas por equipe e partida.

### events_v2
Eventos detalhados oriundos do FotMob.

### snapshots
Snapshots minuto a minuto gerados pelo snapshot_builder_v2.py.

### results
Tabela de targets para treinamento dos modelos de gols tardios.

## SofaScore Layer

### matches_master
Tabela mestre de integração entre Understat, FotMob e SofaScore.

### match_statistics
Estatísticas agregadas da partida.

### match_incidents
Incidentes da partida (gols, cartões, substituições etc).

### match_graph
Dados de momentum minuto a minuto do SofaScore.

### match_mapping
Mapeamento entre IDs das diferentes fontes de dados.

## Staging

### fotmob_raw_matches
Armazenamento bruto de payloads FotMob.