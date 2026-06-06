# PROJECT STATUS

## Estado Atual da Base

- Inventory SofaScore EPL: 381 partidas.
- Pastas locais: 381.
- Partidas importaveis: 380.
- Partida descartada da importacao atual: `12436452`.
- `matches_master`: 380 partidas.
- `match_statistics`: 380 partidas.
- `match_incidents`: 7647 registros.
- `match_graph`: 34861 pontos em 379 partidas.
- `match_shotmap`: 9883 finalizacoes em 380 partidas.
- `match_source_status`: 760 registros.
- Orfaos em `match_statistics`: 0.
- Orfaos em `match_incidents`: 0.

Ressalvas:

- `big_chances_home` possui 7 nulos.
- `big_chances_away` possui 7 nulos.
- `12436452` segue como partida conhecida descartada da importacao SofaScore atual.
- `12437015` segue como `known_missing` para `graph.json`, HTTP 404 confirmado, mantendo a partida e excluindo apenas outputs que exigem Graph.

---

## Concluido

- Estrutura documental do projeto consolidada.
- Understat integrado.
- FotMob integrado parcialmente.
- EPL 2024/2025 descoberta via SofaScore com 381 partidas no inventory.
- Match Mapping criado.
- PostgreSQL configurado.
- SQLAlchemy configurado.
- Tabelas `match_mapping`, `matches_master`, `match_statistics`, `match_incidents`, `match_graph`, `match_shotmap` e `match_source_status` criadas.
- Coleta SofaScore core/full auditada com 380 partidas importaveis.
- PostgreSQL populado com 380 partidas SofaScore importaveis.
- Dataset Analitico V1 gerado com 380 linhas e status APTO COM RESSALVAS.
- Target Audit concluido: `target_late_goal_75` com 189 positivos e 191 negativos.
- Validacao H1/H2 bloqueada por risco confirmado de data leakage.
- Validacao H3/H4 concluida.
- Baseline 1A Pre-Match H3/H4 implementado, executado e revisado como NAO APROVADO quantitativamente.
- Baseline In-Game V1 H6/H9 implementado, executado e revisado como NAO APROVADO quantitativamente.
- Discovery controlado SofaScore H8 executado.
- Endpoint `/graph` confirmado como fonte temporal de momentum.
- Endpoint `/shotmap` confirmado como fonte de finalizacoes temporais e espaciais.
- Coleta raw `graph.json` executada e auditada.
- Coleta raw `shotmap.json` executada e auditada.
- Schema/storage H8 implementado e importado para `match_graph`, `match_shotmap` e `match_source_status`.
- Catalogo metodologico H8 V1 concluido.
- Validacao Estatistica Inicial H8-A/H8-B executada.
- Feature Builder H8 V1 especificado, implementado e executado localmente.
- Dataset H8 V1 criado com join explicito do target e validation report APTO COM RESSALVAS.

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

Status:

- H8 e a frente ativa.
- `graph.json` foi coletado, auditado, armazenado e importado como artefato temporal de momentum/pressao.
- `shotmap.json` foi coletado, auditado, armazenado e importado como artefato de finalizacoes temporais/espaciais.
- `12437015` permanece como excecao tecnica conhecida para Graph.
- Validacao estatistica inicial H8 foi executada contra `target_late_goal_75` nos cutoffs 60, 65, 70 e 75.
- Feature Builder H8 V1 foi implementado em `Analytics/FeatureBuilder/h8_feature_builder_v1.py`.
- Feature Builder H8 V1 gerou `h8_features_v1` localmente com 1520 linhas e status APTO COM RESSALVAS.
- Dataset H8 V1 foi implementado em `Analytics/DatasetBuilder/h8_dataset_builder_v1.py`.
- Dataset H8 V1 foi gerado localmente com 1520 linhas, 380 partidas, 4 cutoffs e `target_late_goal_75` anexado.
- Baseline H8 ainda nao foi executado.
- Producao e backtesting financeiro continuam bloqueados.

Feature Builder H8 V1:

- Script: `Analytics/FeatureBuilder/h8_feature_builder_v1.py`.
- Spec: `docs/04_RESEARCH/H8_FEATURE_BUILDER_SPEC.md`.
- Grain: 1 linha por `match_id + cutoff_minute`.
- Cutoffs: 60, 65, 70 e 75.
- Linhas geradas localmente: 1520.
- Partidas unicas: 380.
- Graph disponivel: 379 partidas.
- Shotmap disponivel: 380 partidas.
- Status validation report: APTO COM RESSALVAS.
- Erros: 0.

Dataset H8 V1:

- Script: `Analytics/DatasetBuilder/h8_dataset_builder_v1.py`.
- Output local: `data/processed/datasets/late_goal_dataset_h8_v1.csv`.
- Output local: `data/processed/datasets/late_goal_dataset_h8_v1.parquet`.
- Metadata: `data/processed/datasets/late_goal_dataset_h8_v1_metadata.json`.
- Validation report: `data/processed/datasets/late_goal_dataset_h8_v1_validation_report.json`.
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

Validacao Estatistica Inicial H8:

- Testes executados: 36 combinacoes cutoff-feature.
- MANTER: 2.
- OBSERVAR: 27.
- DESCARTAR: 7.
- NAO TESTAVEL: 0.
- Melhor sinal: `momentum_trend_last_10m` no cutoff 60, p-value 0,0194, efeito maximo 13,0 p.p.
- Segundo sinal aprovado: `shots_last_10m` no cutoff 60, p-value 0,0492, efeito maximo 11,7 p.p.
- Graph e Shotmap seguem como familias complementares candidatas.

---

## Dataset Analitico V1

Status:

- Gerado.
- APTO COM RESSALVAS.

Resumo:

- Linhas: 380.
- Grain: 1 linha por partida.
- Target principal: `target_late_goal_75`.
- Target positivo: 189.
- Target negativo: 191.
- Duplicatas por `match_id`: 0.
- Duplicatas por `sofascore_event_id`: 0.

Colunas proibidas como features:

- `has_late_goal`
- `target_late_goal_75`
- `late_goal_count_75`
- `home_late_goal_count_75`
- `away_late_goal_count_75`
- `first_late_goal_minute_75`
- `home_goals`
- `away_goals`
- `total_goals`

Regra:

- Estatisticas finais da propria partida sao proibidas como preditores in-game.

---

## Status das Hipoteses

- H1 - BLOQUEADA por data leakage.
- H2 - BLOQUEADA por data leakage.
- H3 - MANTER COMO CANDIDATA, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H4 - MANTER COMO CANDIDATA FORTE, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H5 - NAO VALIDADA.
- H6 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.
- H7 - NAO VALIDADA COMO HIPOTESE INDEPENDENTE.
- H8 - DATASET V1 IMPLEMENTADO: pendente decisao de Baseline H8.
- H9 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.

---

## Em Andamento

### Consolidacao H8

Proximos agentes provaveis:

- Quant Research / Data Science.
- PM.
- CTO, se houver nova mudanca metodologica ou arquitetura.

Objetivo:

Revisar o Dataset H8 V1 e decidir se sera autorizado Baseline H8 controlado.

---

## Proximas Etapas

1. Revisar `Analytics/DatasetBuilder/h8_dataset_builder_v1.py`.
2. Revisar `data/processed/datasets/late_goal_dataset_h8_v1_metadata.json`.
3. Revisar `data/processed/datasets/late_goal_dataset_h8_v1_validation_report.json`.
4. Decidir se Baseline H8 controlado sera autorizado.
5. Se autorizado, implementar Baseline H8 sem backtesting financeiro e sem producao.
6. Manter backtesting financeiro e producao bloqueados.

---

## Descobertas Recentes

- H3/H4 pre-jogo isoladas nao foram suficientes no Baseline 1A.
- H6/H9 melhoraram o baseline, mas nao aprovaram quantitativamente sem graph/momentum.
- `graph` foi confirmado como fonte temporal de momentum/pressao.
- `graph` possui 379/380 partidas importaveis cobertas e 1 excecao 404 conhecida.
- `shotmap` foi confirmado como fonte de finalizacoes temporais/espaciais.
- A cobertura `shotmap` esta fechada para as 380 partidas importaveis.
- H8-A/H8-B apresentaram 2 sinais MANTER e 27 OBSERVAR na validacao univariada inicial.
- Feature Builder H8 V1 produziu 1520 linhas com validacao anti-leakage sem erros.
- Dataset H8 V1 anexou `target_late_goal_75` explicitamente e preservou whitelist/known_missing.
- Nenhum backtesting ou producao foi iniciado.
