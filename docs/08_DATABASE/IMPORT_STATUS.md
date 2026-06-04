# IMPORT STATUS

## Objetivo

Acompanhar o estado da importação dos dados coletados para o PostgreSQL.

---

## Understat

Status:
Operacional

Origem:
Understat

Destino:
matches_master

Dados disponíveis:

- Match ID
- Liga
- Temporada
- Data
- Times
- Placar
- xG
- Forecast
- PPDA
- Deep
- xGA

---

## SofaScore

### Season Collector

Status:
Implementado

Artefatos:

- inventory.json
- rounds.json
- round_XX_events.json

---

### Match Collector

Status:
Implementado

Artefatos:

- event.json
- statistics.json
- incidents.json
- lineups.json
- h2h.json

---

### Importer

Status:
Não iniciado

Script previsto:

sofascore_importer.py

---

## Tabelas PostgreSQL

### matches_master

Status:
Pronta

---

### match_statistics

Status:
Pronta

---

### match_incidents

Status:
Pronta

---

### match_graph

Status:
Estrutura pronta

Observação:
Coleta do endpoint graph ainda não implementada.

---

## Estado Atual do Projeto

Temporadas descobertas:

- Premier League 2024/25

Partidas coletadas:

- 50+

JSONs coletados:

- 250+

---

## Próximo Marco

Implementar:

sofascore_importer.py

Objetivo:

Importar dados SofaScore para:

- matches_master
- match_statistics
- match_incidents
- match_graph

---

## Bloqueios Conhecidos

### HTTP 403 SofaScore

Situação observada:

- coleta funcional
- bloqueio após grande volume de requisições

Hipóteses:

- rate limiting
- session limiting
- IP limiting

Status:
Em investigação