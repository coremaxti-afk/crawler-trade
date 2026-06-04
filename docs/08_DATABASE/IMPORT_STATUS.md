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
Implementado, executado e aprovado em validacao SQL.

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

### Validacao SQL antes do rerun final

Consultas executadas:

```sql
SELECT COUNT(*) FROM matches_master;
SELECT COUNT(*) FROM match_statistics;
SELECT COUNT(*) FROM match_incidents;
```

Resultado:

- `matches_master`: 380
- `match_statistics`: 380
- `match_incidents`: 7647

Duplicatas por `sofascore_event_id`:

- `matches_master`: 0 grupos duplicados.
- `match_statistics`: 0 grupos duplicados.

Skip conhecido:

- `matches_master` com `sofascore_event_id = 12436452`: 0.
- `match_statistics` com `sofascore_event_id = 12436452`: 0.
- `match_incidents` com `sofascore_event_id = 12436452`: 0.

Integridade basica:

- Orfaos em `match_statistics`: 0.
- Orfaos em `match_incidents`: 0.

### Rerun final do importer

Resultado:

- processed: 380
- inserted: 0
- updated: 380
- failed: 0
- known_skipped: 1

Interpretacao:

- As 380 partidas importaveis ja existiam no banco.
- O importer atualiza registros existentes de forma idempotente.
- O comportamento `updated: 380` e esperado no rerun, pois a rotina atual executa update para eventos ja existentes, mesmo quando nao ha diferenca material de dados.
- Isso nao gerou aumento de registros nem duplicatas.

### Validacao SQL apos rerun final

Resultado:

- `matches_master`: 380
- `match_statistics`: 380
- `match_incidents`: 7647
- Duplicatas em `matches_master`: 0.
- Duplicatas em `match_statistics`: 0.
- Registros para `12436452`: 0 nas tres tabelas.
- Orfaos em `match_statistics`: 0.
- Orfaos em `match_incidents`: 0.

Conclusao:

A importacao SofaScore core esta aprovada pelos criterios atuais: `failed = 0`, `known_skipped = 1`, sem duplicatas, sem crescimento indevido apos rerun e com as tres tabelas alvo populadas conforme esperado.

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

---

## Validação Leve de Qualidade Pós-Importação

Status:

APTO COM RESSALVAS para início da fase Quant Research.

Script:

- `LateGoalResearch/Crawler/Sofascore/validate_sofascore_import_quality.py`

Relatórios gerados localmente:

- `data/reports/sofascore_import_quality_report.md`
- `data/reports/sofascore_import_quality_report.json`

Escopo:

- Validação somente leitura.
- Uso de `config.database.engine`.
- Execução apenas de consultas `SELECT`.
- Nenhuma alteração em schema, dados brutos, importer, collectors, features ou modelagem.

Contagens validadas:

- `matches_master`: 380 / 380.
- `match_statistics`: 380 / 380.
- `match_incidents`: 7647 / 7647.

Incidentes por partida:

- Mínimo: 12.
- Máximo: 30.
- Média: 20.1237.
- Mediana: 20.0.
- Partidas com 0 incidentes: 0.

Tipos de incidentes:

- Tipos nulos: 0.
- Tipos raros <= 3: 0.

Distribuição:

- `substitution`: 3211.
- `card`: 1681.
- `goal`: 1115.
- `period`: 760.
- `injuryTime`: 755.
- `varDecision`: 111.
- `inGamePenalty`: 14.

Partidas sem incidentes de gol:

- Total: 16.
- Partidas sem gol nos incidentes mas com placar com gols no `matches_master`: 0.

Divergências entre `matches_master` e `match_incidents`:

- Divergências encontradas: 0.

`match_statistics`:

- Linhas: 380.
- Linhas vazias: 0.
- Partidas sem estatísticas: 0.

Campos nulos:

- `possession_home`: 0.
- `possession_away`: 0.
- `shots_home`: 0.
- `shots_away`: 0.
- `shots_on_target_home`: 0.
- `shots_on_target_away`: 0.
- `corners_home`: 0.
- `corners_away`: 0.
- `big_chances_home`: 7.
- `big_chances_away`: 7.
- `xg_home`: 0.
- `xg_away`: 0.

Conclusão:

A base SofaScore EPL importada está tecnicamente apta para iniciar Quant Research com ressalvas documentadas. A principal ressalva é a existência de 7 nulos em `big_chances_home` e 7 nulos em `big_chances_away`. Não foram encontradas divergências de placar, partidas sem incidentes, estatísticas ausentes, duplicatas ou órfãos. `match_graph` permanece fora do escopo até coleta/importação de `graph.json` ou fonte equivalente.
