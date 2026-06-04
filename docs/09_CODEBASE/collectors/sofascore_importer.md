# SOFASCORE IMPORTER

## Arquivo

Crawler/Sofascore/sofascore_importer.py

---

## Objetivo

Importar os JSONs coletados do SofaScore para o PostgreSQL.

Responsável por transformar dados brutos em registros estruturados nas tabelas analíticas do projeto.

---

## Status

Planejado.

Implementação ainda não iniciada.

---

## Entradas

### event.json

Dados gerais da partida.

### statistics.json

Estatísticas agregadas.

### incidents.json

Eventos da partida.

### lineups.json

Escalações.

### h2h.json

Histórico de confrontos.

---

## Tabelas Destino

### matches_master

Informações principais da partida.

### match_statistics

Estatísticas detalhadas.

### match_incidents

Timeline de eventos.

### match_graph

Momentum minuto a minuto.

---

## Fluxo Previsto

JSON Raw
↓
Validação
↓
Transformação
↓
PostgreSQL

---

## Requisitos

- PostgreSQL ativo.
- config/database.py configurado.
- JSONs previamente coletados.

---

## Próximas Evoluções

- Importação incremental.
- Reprocessamento seguro.
- Logs detalhados.
- Controle de duplicidade.

---

## Dependências

- SQLAlchemy
- PostgreSQL
- config/database.py