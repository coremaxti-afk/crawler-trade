# IMPORT STATUS

## Objetivo

Acompanhar o estado da importacao dos dados coletados para o PostgreSQL.

---

## Understat

Status:
Operacional.

Destino atual:

- `matches_master`, via integracao/mapeamento especifico da fonte.

Dados disponiveis:

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
Implementado.

Artefatos:

- `inventory.json`
- `rounds.json`
- `round_XX_events.json`

---

### Match Collectors

Status:
Implementados e validados operacionalmente.

Scripts relevantes:

- `LateGoalResearch/Crawler/Sofascore/v2_sofascore_match_collector.py`
- `LateGoalResearch/Crawler/Sofascore/v3_sofascore_match_collector.py`

Perfis de coleta:

- Full: `event.json`, `statistics.json`, `incidents.json`, `lineups.json`, `h2h.json`
- Core: `event.json`, `statistics.json`, `incidents.json`

Estado local auditado:

- Total no inventory: 381 partidas.
- Total de pastas locais: 381.
- Partidas full: 192.
- Partidas core: 188.
- Total importavel: 380.
- Partidas faltantes: 0.
- Partidas incompletas relevantes para importacao atual: 1.
- Partida descartada da importacao atual: `12436452`.

Observacao:

- A partida `12436449` foi corrigida/coletada com os 3 JSONs core e esta importada.
- `lineups.json` e `h2h.json` seguem preservados como dados brutos complementares, mas nao foram importados nesta etapa.

---

## SofaScore Importer

Status:
Implementado e executado.

Script:

- `LateGoalResearch/Crawler/Sofascore/sofascore_importer.py`

Commit:

- `84e641f` - Implementa importer SofaScore core

Escopo da importacao:

- `matches_master`
- `match_statistics`
- `match_incidents`

Fora do escopo desta etapa:

- `match_graph`
- `lineups.json`
- `h2h.json`
- features H1-H9
- dataset analitico
- modelagem

Regras aplicadas:

- Usa `from config.database import engine`.
- Usa SQLAlchemy com `engine.begin()` e `sqlalchemy.text`.
- Classifica partidas em `full`, `core`, `incomplete` e `known_skipped`.
- Pula `KNOWN_SKIPPED_MATCH_IDS = {"12436452"}`.
- Importa apenas partidas full/core.
- Erro por partida nao interrompe todo o lote.
- Reexecucao nao duplica registros.

---

## Validacao Executada

### Dry-run

Resultado:

- full: 192
- core: 188
- importable: 380
- known_skipped: 1
- incomplete: 0
- missing: 0

### Primeira importacao real

Resultado:

- processed: 380
- inserted: 380
- updated: 0
- failed: 0
- known_skipped: 1

### Segunda execucao / idempotencia

Resultado:

- processed: 380
- inserted: 0
- updated: 380
- failed: 0
- known_skipped: 1

### Banco apos importacao

- `matches_master`: 380 eventos distintos.
- `match_statistics`: 380 eventos distintos.
- `match_incidents`: 7647 registros, cobrindo 380 eventos.
- Registros para `12436452`: 0.
- Orfaos em `match_statistics`: 0.
- Orfaos em `match_incidents`: 0.
- Partidas importadas sem estatisticas: 0.

---

## Tabelas PostgreSQL

### matches_master

Status:
Populada com 380 partidas SofaScore EPL importaveis.

Origem principal:

- `event.json`

---

### match_statistics

Status:
Populada com 380 registros de estatisticas agregadas.

Origem principal:

- `statistics.json`

---

### match_incidents

Status:
Populada com 7647 incidentes.

Origem principal:

- `incidents.json`

---

### match_graph

Status:
Nao populada nesta etapa.

Motivo:

- Nenhum `graph.json` ou fonte equivalente foi coletado/importado ainda.

---

## Proximo Marco

Preparar a proxima etapa de engenharia de dados:

1. Validar amostras importadas por coluna.
2. Revisar qualidade dos dados em `match_statistics` e `match_incidents`.
3. Definir, com CTO/Data Engineer, se o proximo passo sera importacao complementar, graph ou inicio de catalogo de features.
4. Manter `12436452` fora da importacao atual ate nova decisao.
