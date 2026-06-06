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

Ressalvas:

- `big_chances_home` possui 7 nulos.
- `big_chances_away` possui 7 nulos.
- `12437015` segue como `known_missing` para `graph.json`, HTTP 404 confirmado.

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

Artefatos:

- `Analytics/FeatureBuilder/h8_feature_builder_v1.py`
- `Analytics/DatasetBuilder/h8_dataset_builder_v1.py`
- `Analytics/BaselineH8/run_baseline_h8_v1.py`
- `data/processed/datasets/late_goal_dataset_h8_v1_metadata.json`
- `data/processed/datasets/late_goal_dataset_h8_v1_validation_report.json`
- `data/processed/reports/baseline_h8_v1_validation_report.json`
- `data/processed/reports/baseline_h8_v1_metrics_summary.json`

### Feature Builder H8 V1

- Grain: 1 linha por `match_id + cutoff_minute`.
- Cutoffs: 60, 65, 70 e 75.
- Linhas: 1520.
- Partidas unicas: 380.
- Graph disponivel: 379 partidas.
- Shotmap disponivel: 380 partidas.
- Validation status: APTO COM RESSALVAS.
- Erros: 0.

### Dataset H8 V1

- Linhas: 1520.
- Partidas unicas: 380.
- Cutoffs: 60, 65, 70 e 75.
- Target: `target_late_goal_75`.
- `match_id + cutoff_minute` duplicados: 0.
- Target mismatches: 0.
- Graph known_missing rows: 4.
- Shotmap available rows: 1520.
- Validation status: APTO COM RESSALVAS.
- Erros: 0.

### Baseline H8 V1

Gate confirmado antes da execucao:

- `target_late_goal_75` unido corretamente.
- Ausencia de target-derived features.
- Ausencia de colunas full-match.
- Ausencia de placar final.
- `graph_known_missing` preservado.
- 0 duplicatas `match_id + cutoff_minute`.

Resultado:

- Cutoffs avaliados separadamente: 60, 65, 70 e 75.
- Split temporal por `match_id`, 60/20/20, sem shuffle.
- Baseline nulo executado.
- Features usadas: somente whitelist H8.
- Melhor cutoff: 60.
- ROC-AUC Test melhor cutoff: 0,5076.
- PR-AUC Test melhor cutoff: 0,5232.
- Delta Brier Test: +0,0155 contra o nulo.
- Delta LogLoss Test: +0,0345 contra o nulo.
- Melhor feature do melhor cutoff: `momentum_last_10m_avg`.
- Melhor grupo do melhor cutoff: Graph.
- Decisao quantitativa: NAO APROVADO.

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
3. Nao iniciar backtesting financeiro.
4. Nao iniciar producao.
5. Nao combinar H8 com H3/H4/H6/H9 sem aprovacao explicita.

---

## Status

EM EXECUCAO - H8 TEM DATASET E BASELINE CONTROLADO EXECUTADOS, MAS BASELINE H8 V1 FOI NAO APROVADO QUANTITATIVAMENTE. PRODUCAO E BACKTESTING SEGUEM BLOQUEADOS.
