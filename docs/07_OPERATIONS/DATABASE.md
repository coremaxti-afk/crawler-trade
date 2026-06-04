# DATABASE

## Banco Principal

PostgreSQL

---

## Objetivos

- Centralizar dados das fontes.
- Construir dataset integrado.
- Disponibilizar dados para análise quantitativa.
- Servir como camada única para Feature Engineering.

---

## Estado Atual

### Configuração

- PostgreSQL configurado.
- SQLAlchemy configurado.
- config/database.py ativo.

### Tabelas Principais

- matches_master
- match_statistics
- match_incidents
- match_graph

---

## Fontes Integradas

### Understat

Status:
Operacional

### SofaScore

Status:
Coleta operacional

### FotMob

Status:
Parcial

---

## Próximo Marco

Implementar:

sofascore_importer.py

Objetivo:

Popular PostgreSQL com os JSONs coletados do SofaScore.

---

## Status

Banco operacional.
Modelagem em evolução.