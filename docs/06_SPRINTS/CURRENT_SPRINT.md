# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar H8 de coleta/importacao ate Dataset e Baseline controlado, sem iniciar producao, automacao operacional ou backtesting financeiro. Registrar e validar fontes auxiliares de odds historicas de forma controlada, sem promover carga completa, features, datasets ou producao sem aprovacao.

---

## Concluido

- [x] Executar discovery controlado de endpoints SofaScore.
- [x] Confirmar endpoint `/graph` como util para H8.
- [x] Confirmar endpoint `/shotmap` como util para H8.
- [x] Coletar `graph` e auditar cobertura.
- [x] Coletar `shotmap` e auditar cobertura.
- [x] Especificar storage/import H8.
- [x] Implementar schema/storage H8.
- [x] Implementar e executar importer H8.
- [x] Registrar `12437015` como known_missing para Graph HTTP 404.
- [x] Completar catalogo metodologico H8 V1.
- [x] Executar Validacao Estatistica Inicial H8-A/H8-B.
- [x] Especificar Feature Builder H8 V1.
- [x] Implementar e executar Feature Builder H8 V1.
- [x] Criar Dataset H8 V1 com join explicito do target.
- [x] Confirmar validation report do Dataset H8 V1 antes do baseline.
- [x] Executar Baseline H8 V1 controlado.
- [x] Documentar resultado do Baseline H8 V1.
- [x] Executar discovery Football-Data EPL 2024/25 para odds historicas.
- [x] Executar match mapping exploratorio Football-Data x SofaScore com 380/380 partidas pareadas.
- [x] Criar e revisar especificacao Football-Data Storage/Import.
- [x] Consolidar `FOOTBALL_DATA_SCHEMA_SPEC.md`.
- [x] Criar `FOOTBALL_DATA_MIGRATION_SPEC.md`.
- [x] Criar `FOOTBALL_DATA_IMPORTER_SPEC.md`.
- [x] Implementar migration Football-Data Fase 1.
- [x] Implementar importer Football-Data Fase 1.
- [x] Executar dry-run Football-Data com 5 linhas.
- [x] Executar teste controlado Football-Data com 5 linhas.
- [x] Validar idempotencia, FKs, contagens, rastreabilidade e mercados.
- [x] Documentar resultado em `FOOTBALL_DATA_PHASE1_IMPLEMENTATION_REPORT.md`.

---

## Documentos H8

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

## Documentos Odds Historicas

- `docs/03_SOURCES/ODDS/FOOTBALL_DATA_DISCOVERY_20260607.md`
- `docs/03_SOURCES/ODDS/FOOTBALL_DATA_MATCH_MAPPING_20260607.md`
- `docs/03_SOURCES/ODDS/ODDSPORTAL_DISCOVERY_20260607.md`
- `docs/08_DATABASE/FOOTBALL_DATA_STORAGE_IMPORT_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_SCHEMA_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_MIGRATION_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_IMPORTER_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_PHASE1_IMPLEMENTATION_REPORT.md`

---

## Artefatos Football-Data

- `database/migrations/20260608_create_football_data_storage_tables.sql`
- `Importer/FootballData/football_data_importer.py`

---

## Estado Atual H8

- Feature Builder H8 V1 executado.
- Dataset H8 V1 criado.
- Baseline H8 V1 executado.
- Decisao quantitativa: NAO APROVADO.
- Producao e backtesting seguem bloqueados.

---

## Estado Atual Odds Historicas

### Football-Data EPL 2024/25

- CSV publico analisado: 380 partidas.
- Mercados encontrados: 1X2, Over/Under 2.5 e Asian Handicap.
- Odds closing presentes.
- Odds opening-like/pre-close preservadas como `opening_like`, sem assumir opening odds oficiais.
- Odds live ausentes.
- Match mapping com SofaScore: 380/380 partidas importaveis pareadas.
- Taxa de pareamento: 100%.
- Conflitos de placar: 0.
- Ambiguidades relevantes: 0.
- Migration Football-Data aplicada localmente.
- Dry-run com 5 linhas: 5 mapped, 470 odds estimadas, 0 escritas.
- Teste controlado: 5 staging, 5 mapping, 470 odds, 0 duplicatas, 0 orfaos.
- Idempotencia: reexecucao com 0 inserts, 470 updates, 470 odds totais.
- Recomendacao: APTO PARA REVISAO CTO DA CARGA COMPLETA.
- Carga completa das 380 partidas ainda bloqueada.

---

## Restricoes Ativas

- Nao iniciar backtesting financeiro.
- Nao iniciar producao.
- Nao transformar nenhum baseline em sistema decisorio.
- Nao combinar H8 com H3/H4/H6/H9 sem aprovacao explicita.
- Nao usar features fora de whitelist aprovada.
- Nao usar eventos apos cutoff como features.
- Nao executar carga completa Football-Data sem aprovacao CTO.
- Nao criar features Football-Data.
- Nao criar dataset Football-Data.

---

## Proximos Passos

- [ ] Quant Research revisar `docs/04_RESEARCH/BASELINE_H8_V1_RESULTS.md`.
- [ ] PM decidir se H8 deve ser refinado, combinado com outras familias ou pausado nesta formulacao.
- [ ] CTO revisar `docs/08_DATABASE/FOOTBALL_DATA_PHASE1_IMPLEMENTATION_REPORT.md`.
- [ ] CTO decidir se autoriza carga completa Football-Data das 380 partidas.
- [ ] Manter backtesting e producao bloqueados.

---

## Status

EM EXECUCAO - H8 COMPLETO ATE BASELINE CONTROLADO. BASELINE H8 V1 NAO APROVADO QUANTITATIVAMENTE. FOOTBALL-DATA FASE 1 IMPLEMENTADA E VALIDADA EM AMOSTRA CONTROLADA DE 5 LINHAS. CARGA COMPLETA, DATASETS, FEATURES, PRODUCAO E BACKTESTING SEGUEM BLOQUEADOS ATE APROVACAO CTO.
