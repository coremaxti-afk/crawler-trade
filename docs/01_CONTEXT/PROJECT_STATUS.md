# PROJECT STATUS

## Estado Atual da Base

- Inventory SofaScore EPL: 381 partidas.
- Partidas importaveis: 380.
- Partida descartada da importacao atual: `12436452`.
- `matches_master`: 380 partidas.
- `match_statistics`: 380 partidas.
- `match_incidents`: 7647 registros.
- `match_graph`: 34861 pontos em 379 partidas.
- `match_shotmap`: 9883 finalizacoes em 380 partidas.
- `match_source_status`: 760 registros.
- Football-Data: 380 staging rows, 380 mappings e 34280 odds importadas localmente.

Ressalvas:

- `big_chances_home` possui 7 nulos.
- `big_chances_away` possui 7 nulos.
- `12437015` segue como `known_missing` para `graph.json`, HTTP 404 confirmado.
- Football-Data `opening_like` nao deve ser tratado automaticamente como opening odds oficial.
- Football-Data nao contem odds live/in-game.

---

## Concluido

- Estrutura documental do projeto consolidada.
- Understat integrado.
- FotMob integrado parcialmente.
- EPL 2024/2025 descoberta via SofaScore.
- Match Mapping criado.
- PostgreSQL e SQLAlchemy configurados.
- Tabelas principais SofaScore populadas.
- Dataset Analitico V1 gerado com 380 linhas e status APTO COM RESSALVAS.
- Target Audit concluido: `target_late_goal_75` com 189 positivos e 191 negativos.
- Validacao H1/H2 bloqueada por risco de data leakage.
- Validacao H3/H4 concluida.
- Baseline 1A Pre-Match H3/H4 executado e NAO APROVADO quantitativamente.
- Baseline In-Game V1 H6/H9 executado e NAO APROVADO quantitativamente.
- Discovery controlado SofaScore H8 executado.
- `graph` e `shotmap` coletados, auditados, armazenados e importados.
- Validacao Estatistica Inicial H8-A/H8-B executada.
- Feature Builder H8 V1 implementado e executado localmente.
- Dataset H8 V1 criado com join explicito do target e validation report APTO COM RESSALVAS.
- Baseline H8 V1 executado e NAO APROVADO quantitativamente.
- Discovery Football-Data EPL 2024/25 concluido com 380 partidas e odds historicas 1X2, Over/Under 2.5 e Asian Handicap.
- Match mapping Football-Data x SofaScore executado: 380/380 partidas pareadas, 100%, 0 conflitos de placar e 0 ambiguidades relevantes.
- Especificacao Football-Data Storage/Import criada e revisada pela area Data Engineer / Database.
- Specs documentais Football-Data Schema, Migration e Importer consolidadas em `docs/08_DATABASE/`.
- Football-Data Fase 1 implementada: migration, importer, dry-run, validacao e teste controlado em 5 linhas.
- Football-Data Fase 2 executada: importacao completa local das 380 partidas e validacao idempotente.

---

## H8 - Graph / Momentum / Shotmap

Documentos:

- `docs/03_SOURCES/SOFASCORE/ENDPOINT_DISCOVERY_20260605.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_ENDPOINT.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_AUDIT_20260606.md`
- `docs/03_SOURCES/SOFASCORE/SHOTMAP_ENDPOINT.md`
- `docs/08_DATABASE/H8_STORAGE_IMPORT_SPEC.md`
- `docs/04_RESEARCH/H8_FEATURE_CATALOG_V1.md`
- `docs/04_RESEARCH/H8_INITIAL_STATISTICAL_VALIDATION_RESULTS.md`
- `docs/04_RESEARCH/H8_FEATURE_BUILDER_SPEC.md`
- `docs/04_RESEARCH/H8_DATASET_BASELINE_RECOMMENDATION.md`
- `docs/04_RESEARCH/BASELINE_H8_V1_RESULTS.md`

---

## Odds Historicas - Football-Data

Documentos:

- `docs/03_SOURCES/ODDS/FOOTBALL_DATA_DISCOVERY_20260607.md`
- `docs/03_SOURCES/ODDS/FOOTBALL_DATA_MATCH_MAPPING_20260607.md`
- `docs/08_DATABASE/FOOTBALL_DATA_STORAGE_IMPORT_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_SCHEMA_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_MIGRATION_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_IMPORTER_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_PHASE1_IMPLEMENTATION_REPORT.md`
- `docs/08_DATABASE/FOOTBALL_DATA_PHASE2_FULL_IMPORT_REPORT.md`

Artefatos:

- `database/migrations/20260608_create_football_data_storage_tables.sql`
- `Importer/FootballData/football_data_importer.py`

Estado:

- Fonte avaliada: Football-Data.co.uk EPL 2024/25.
- CSV publico baixado e analisado: 380 partidas.
- Mercados importados: 1X2, Over/Under 2.5 e Asian Handicap.
- Odds closing presentes.
- Odds opening-like/pre-close preservadas como `opening_like`, sem assumir opening odds oficiais.
- Odds live ausentes.
- Match mapping com SofaScore: 380/380 partidas importaveis pareadas.
- Migration Football-Data aplicada localmente.
- Carga completa executada: 380 staging, 380 mappings, 34280 odds.
- Idempotencia validada: reexecucao com 0 inserts, 34280 updates e contagem final estavel.
- Duplicatas por grain: 0.
- Orfaos: 0.
- Odds invalidas: 0.
- `Max`, `MaxC`, `Avg` e `AvgC` preservados como agregadores distintos.
- Recomendacao atual: APTO PARA PROXIMA ETAPA DE DATA ENGINEER / QUANT RESEARCH.

---

## Status das Hipoteses

- H1 - BLOQUEADA por data leakage.
- H2 - BLOQUEADA por data leakage.
- H3 - MANTER COMO CANDIDATA, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H4 - MANTER COMO CANDIDATA FORTE, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H5 - NAO VALIDADA.
- H6 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.
- H7 - NAO VALIDADA COMO HIPOTESE INDEPENDENTE.
- H8 - BASELINE V1 EXECUTADO E NAO APROVADO quantitativamente.
- H9 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.

---

## Proximas Etapas

1. Quant Research revisar `docs/04_RESEARCH/BASELINE_H8_V1_RESULTS.md`.
2. PM decidir se H8 deve ser refinado, combinado com outras familias ou encerrado nesta formulacao.
3. Data Engineer / Quant Research revisar `docs/08_DATABASE/FOOTBALL_DATA_PHASE2_FULL_IMPORT_REPORT.md`.
4. Definir contrato de consumo das odds antes de criar dataset ou features.
5. Nao iniciar backtesting financeiro.
6. Nao iniciar producao.
7. Nao tratar `opening_like` como opening odds oficial sem auditoria metodologica.

---

## Status

EM EXECUCAO - H8 TEM DATASET E BASELINE CONTROLADO EXECUTADOS, MAS BASELINE H8 V1 FOI NAO APROVADO QUANTITATIVAMENTE. FOOTBALL-DATA FASE 2 FOI EXECUTADA LOCALMENTE COM 380 PARTIDAS, 34280 ODDS, 0 DUPLICATAS, 0 ORFAOS E 0 ODDS INVALIDAS. FEATURES, DATASETS, PRODUCAO E BACKTESTING SEGUEM BLOQUEADOS ATE NOVA AUTORIZACAO.
