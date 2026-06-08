# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar H8 de coleta/importacao ate Dataset e Baseline controlado, sem iniciar producao, automacao operacional ou backtesting financeiro. Registrar discoveries auxiliares de fontes quando concluirem etapa exploratoria, sem promover importer, schema ou producao sem aprovacao.

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
- [x] Aprovar especificacao Football-Data pela area Data Engineer / Database.

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

---

## Estado Atual H8

### Feature Builder H8 V1

- Script: `Analytics/FeatureBuilder/h8_feature_builder_v1.py`.
- Linhas: 1520.
- Partidas unicas: 380.
- Cutoffs: 60, 65, 70 e 75.
- Graph disponivel: 379 partidas.
- Shotmap disponivel: 380 partidas.
- Validation status: APTO COM RESSALVAS.

### Dataset H8 V1

- Script: `Analytics/DatasetBuilder/h8_dataset_builder_v1.py`.
- Linhas: 1520.
- Partidas unicas: 380.
- Target anexado: `target_late_goal_75`.
- `match_id + cutoff_minute` duplicados: 0.
- Target mismatches: 0.
- Graph known_missing rows: 4.
- Shotmap available rows: 1520.
- Validation status: APTO COM RESSALVAS.

### Baseline H8 V1

- Script: `Analytics/BaselineH8/run_baseline_h8_v1.py`.
- Relatorio: `docs/04_RESEARCH/BASELINE_H8_V1_RESULTS.md`.
- Cutoffs avaliados separadamente: 60, 65, 70 e 75.
- Split temporal por `match_id`, 60/20/20, sem shuffle.
- Baseline nulo executado.
- Features usadas: somente whitelist H8.
- Melhor cutoff: 60.
- ROC-AUC Test melhor cutoff: 0,5076.
- PR-AUC Test melhor cutoff: 0,5232.
- Delta Brier Test: +0,0155 contra o nulo.
- Delta LogLoss Test: +0,0345 contra o nulo.
- Melhor feature: `momentum_last_10m_avg`.
- Melhor grupo: Graph.
- Decisao quantitativa: NAO APROVADO.

---

## Estado Atual Odds Historicas

### Football-Data EPL 2024/25

- CSV publico analisado: 380 partidas.
- Mercados encontrados: 1X2, Over/Under 2.5 e Asian Handicap.
- Odds closing presentes.
- Odds opening-like/pre-close presentes em colunas Pinnacle/closing sequence.
- Odds live ausentes.
- Match mapping com SofaScore: 380/380 partidas importaveis pareadas.
- Taxa de pareamento: 100%.
- Conflitos de placar: 0.
- Ambiguidades relevantes: 0.
- Especificacao Storage/Import criada em `docs/08_DATABASE/FOOTBALL_DATA_STORAGE_IMPORT_SPEC.md`.
- Parecer Data Engineer / Database: APROVADO.
- Pronto para decisao CTO sobre futura implementacao de schema, migration e importer.

---

## Restricoes Ativas

- Nao iniciar backtesting financeiro.
- Nao iniciar producao.
- Nao transformar nenhum baseline em sistema decisorio.
- Nao combinar H8 com H3/H4/H6/H9 sem aprovacao explicita.
- Nao usar features fora de whitelist aprovada.
- Nao usar eventos apos cutoff como features.
- Nao criar importer Football-Data sem aprovacao CTO.
- Nao alterar schema para odds sem aprovacao CTO.

---

## Proximos Passos

- [ ] Quant Research revisar `docs/04_RESEARCH/BASELINE_H8_V1_RESULTS.md`.
- [ ] PM decidir se H8 deve ser refinado, combinado com outras familias ou pausado nesta formulacao.
- [ ] CTO decidir se autoriza schema Football-Data.
- [ ] CTO decidir se autoriza migration Football-Data.
- [ ] CTO decidir se autoriza importer Football-Data.
- [ ] Manter backtesting e producao bloqueados.

---

## Status

EM EXECUCAO - H8 COMPLETO ATE BASELINE CONTROLADO. BASELINE H8 V1 NAO APROVADO QUANTITATIVAMENTE. FOOTBALL-DATA TEM DISCOVERY, MATCH MAPPING E STORAGE/IMPORT SPEC APROVADOS PELA AREA DATA ENGINEER PARA FUTURA DECISAO CTO SOBRE SCHEMA, MIGRATION E IMPORTER. PROXIMA DECISAO E ARQUITETURAL/DE DADOS, NAO OPERACIONAL.