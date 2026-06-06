# H8 STORAGE IMPORT SPEC — Graph / Momentum

## Objetivo

Definir a especificação formal de armazenamento e importação futura dos artefatos H8 da fonte SofaScore:

- `graph.json`
- `shotmap.json`

Este documento é uma especificação técnica para revisão CTO.

Não autoriza implementação, migration, alteração de schema, importer, feature engineering, dataset, baseline ou modelagem.

---

## Escopo

Incluído nesta especificação:

- desenho lógico das tabelas H8;
- grain recomendado;
- campos mínimos;
- constraints mínimas;
- política para exceção conhecida;
- estratégia de importer futuro;
- idempotência;
- rastreabilidade raw;
- validações pós-importação;
- riscos de schema.

Fora do escopo:

- implementação de código;
- criação de migration;
- alteração de schema;
- criação de importer;
- criação de features H8;
- dataset analítico;
- baseline;
- modelagem;
- alteração de crawlers;
- alteração de dados brutos.

---

## Estado Atual H8

Coleta e auditoria H8 concluídas no escopo de Data Acquisition.

### Graph

- Partidas importáveis: 380.
- `graph.json` válidos: 379.
- `graph.json` faltantes totais na base importável: 1.
- `graph.json` faltantes excluindo exceção conhecida: 0.
- `graph.json` inválidos: 0.
- `graphPoints` mínimo: 91.
- `graphPoints` máximo: 92.
- Média de `graphPoints`: 91,98.

Exceção conhecida:

- `event_id`: `12437015`
- Partida: Crystal Palace x Liverpool FC
- Motivo: HTTP 404 no endpoint `/graph`

### Shotmap

- Partidas importáveis: 380.
- `shotmap.json` válidos: 380.
- Faltantes: 0.
- Inválidos: 0.
- Total de finalizações: 9.883.
- Média de finalizações por partida: 26,01.

---

## Decisão CTO Vigente

A exceção `12437015` deve seguir a Opção 2:

- manter a partida para features baseadas em `shotmap`, `incidents` e `statistics`;
- marcar `graph` como exceção conhecida;
- excluir apenas de features/datasets que exijam graph completo.

---

# 1. Tabela `match_graph`

## Objetivo

Armazenar os pontos de momentum do `graph.json` em formato granular e auditável.

## Grain

Uma linha por ponto do graph por partida.

Grain recomendado:

```text
sofascore_event_id + point_index
