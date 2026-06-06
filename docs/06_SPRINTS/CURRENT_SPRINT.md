# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar a frente H8 com dados temporais de graph/momentum e shotmap, passando da coleta/importacao para feature engineering e Dataset H8 auditavel sem iniciar producao, automacao operacional ou backtesting financeiro.

---

## Concluido

- [x] Executar discovery controlado de endpoints SofaScore.
- [x] Confirmar endpoint `/graph` como util para H8.
- [x] Confirmar endpoint `/shotmap` como util para H8.
- [x] Coletar `graph` com sucesso operacional.
- [x] Auditar cobertura `graph` da base EPL importavel.
- [x] Coletar `shotmap` com sucesso.
- [x] Auditar cobertura `shotmap` da base EPL importavel.
- [x] Documentar API-Football e SofaScore discovery.
- [x] Documentar auditoria final de `graph` e `shotmap`.
- [x] Especificar storage/import H8.
- [x] Implementar schema/storage H8.
- [x] Implementar e executar importer H8.
- [x] Registrar `12437015` como known_missing para Graph HTTP 404.
- [x] Completar catalogo metodologico H8 V1.
- [x] Executar Validacao Estatistica Inicial H8-A/H8-B.
- [x] Especificar Feature Builder H8 V1.
- [x] Implementar Feature Builder H8 V1.
- [x] Executar Feature Builder H8 V1 localmente.
- [x] Criar Dataset H8 V1 com join explicito do target.

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

---

## Estado Atual H8

### Graph

- Coletado, auditado, armazenado, importado e usado no Feature Builder H8 V1.
- Registros importados em `match_graph`: 34.861.
- Cobertura: 379/380 partidas importaveis.
- Excecao conhecida: `12437015`, Crystal Palace x Liverpool FC, HTTP 404 no endpoint `/graph`.

### Shotmap

- Coletado, auditado, armazenado, importado e usado no Feature Builder H8 V1.
- Registros importados em `match_shotmap`: 9.883.
- Cobertura: 380/380 partidas importaveis.

### Feature Builder H8 V1

- Script: `Analytics/FeatureBuilder/h8_feature_builder_v1.py`.
- Output local: `data/processed/features/h8_features_v1.csv`.
- Output local: `data/processed/features/h8_features_v1.parquet`.
- Output local: `data/processed/features/h8_features_v1_metadata.json`.
- Output local: `data/processed/features/h8_features_v1_validation_report.json`.
- Linhas: 1520.
- Partidas unicas: 380.
- Cutoffs: 60, 65, 70 e 75.
- Validation status: APTO COM RESSALVAS.
- Erros: 0.

### Dataset H8 V1

- Script: `Analytics/DatasetBuilder/h8_dataset_builder_v1.py`.
- Output local: `data/processed/datasets/late_goal_dataset_h8_v1.csv`.
- Output local: `data/processed/datasets/late_goal_dataset_h8_v1.parquet`.
- Metadata: `data/processed/datasets/late_goal_dataset_h8_v1_metadata.json`.
- Validation report: `data/processed/datasets/late_goal_dataset_h8_v1_validation_report.json`.
- Linhas: 1520.
- Partidas unicas: 380.
- Cutoffs: 60, 65, 70 e 75.
- Target anexado: `target_late_goal_75`.
- `match_id + cutoff_minute` duplicados: 0.
- Target mismatches: 0.
- Graph known_missing rows: 4.
- Shotmap available rows: 1520.
- Validation status: APTO COM RESSALVAS.
- Erros: 0.

---

## Validacao Estatistica Inicial H8

- Target: `target_late_goal_75`.
- Cutoffs: 60, 65, 70 e 75.
- Testes avaliados: 36 combinacoes cutoff-feature.
- MANTER: 2.
- OBSERVAR: 27.
- DESCARTAR: 7.
- NAO TESTAVEL: 0.

Melhores sinais:

- `momentum_trend_last_10m`, cutoff 60: MANTER, p-value 0,0194, efeito maximo 13,0 p.p.
- `shots_last_10m`, cutoff 60: MANTER, p-value 0,0492, efeito maximo 11,7 p.p.

---

## Status das Hipoteses

- H1 - BLOQUEADA por data leakage.
- H2 - BLOQUEADA por data leakage.
- H3 - MANTER COMO CANDIDATA, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H4 - MANTER COMO CANDIDATA FORTE, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H5 - NAO VALIDADA.
- H6 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.
- H7 - NAO VALIDADA COMO HIPOTESE INDEPENDENTE.
- H8 - DATASET V1 IMPLEMENTADO; pendente decisao para Baseline H8.
- H9 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.

---

## Restricoes Ativas

- Nao avancar nenhum baseline atual para backtesting.
- Nao usar nenhum baseline atual em producao.
- Nao transformar nenhum baseline atual em sistema decisorio.
- Nao usar features bloqueadas.
- Nao usar estatisticas finais da propria partida como preditores.
- Nao usar xG/xGA/forecast sem comprovacao temporal segura.
- Nao usar eventos apos cutoff como features in-game.
- Manter backtesting e producao bloqueados.
- Nao executar Baseline H8 sem aprovacao explicita.

---

## Proximos Passos

- [ ] Revisar `Analytics/DatasetBuilder/h8_dataset_builder_v1.py`.
- [ ] Revisar metadata e validation report do Dataset H8 V1.
- [ ] Decidir se Baseline H8 controlado sera autorizado.
- [ ] Se aprovado, implementar Baseline H8 sem backtesting financeiro e sem producao.
- [ ] Manter backtesting e producao bloqueados.

---

## Status

EM EXECUCAO - H8 COLETADO, AUDITADO, IMPORTADO, VALIDADO ESTATISTICAMENTE, COM FEATURE BUILDER V1 E DATASET H8 V1 IMPLEMENTADOS. DATASET H8 V1 LOCAL GERADO COM 1520 LINHAS, 380 PARTIDAS, 4 CUTOFFS E TARGET ANEXADO. PROXIMA DECISAO: BASELINE H8, AINDA SEM PRODUCAO OU BACKTESTING.
