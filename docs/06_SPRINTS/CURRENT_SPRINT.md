# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar a pesquisa exploratoria de H8, Odds, Match State e protocolos dinamicos de trade teorico, mantendo bloqueados producao, robo, trade real, modelo, baseline preditivo e backtesting real com odds live. Separar claramente taxa estatistica, EV teorico, EV com cashout e operacionalidade real.

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
- [x] Validar idempotencia, FKs, contagens, rastreabilidade e mercados na Fase 1.
- [x] Documentar resultado em `FOOTBALL_DATA_PHASE1_IMPLEMENTATION_REPORT.md`.
- [x] Executar importacao completa Football-Data das 380 partidas.
- [x] Reexecutar importacao completa para validar idempotencia.
- [x] Validar contagens finais, orfaos, duplicatas, odds invalidas e agregadores.
- [x] Documentar resultado em `FOOTBALL_DATA_PHASE2_FULL_IMPORT_REPORT.md`.
- [x] Implementar e executar Odds Feature Builder V1.
- [x] Gerar features odds V1, metadata e validation report com status APTO.
- [x] Criar Dataset Odds V1 com join explicito do target.
- [x] Gerar metadata e validation report do Dataset Odds V1 com status APTO COM RESSALVAS.
- [x] Executar Odds Initial Statistical Validation: odds pre-jogo isoladas sem sinal forte para `target_late_goal_75`.
- [x] Executar Odds Interaction Validation V1: MANTER 0, OBSERVAR 1, DESCARTAR 11; odds encerradas como frente principal por enquanto.
- [x] Criar `MATCH_STATE_ODDS_H8_VARIATION_PLAN_V1.md`.
- [x] Executar `MATCH_STATE_ODDS_H8_VARIATION_V1` como exploracao controlada.
- [x] Criar classificacao metodologica para micro-amostras e replicacao multi-liga.
- [x] Criar issue #1 `MARKET_PRICE_CASHOUT_SENSITIVITY_V1`.
- [x] Executar `H8_COMPOSITE_PRESSURE_SCORE_RESULTS_V1` como exploracao de scores compostos agregados.
- [x] Criar issue #2 `DYNAMIC_TRADE_PROTOCOL_VALIDATION_V2` para expansao controlada.

---

## Documentos H8 / Match State / Trade Exploratorio

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
- `docs/04_RESEARCH/MATCH_STATE_ODDS_H8_VARIATION_PLAN_V1.md`
- `docs/04_RESEARCH/MATCH_STATE_ODDS_H8_VARIATION_RESULTS_V1.md`
- `docs/04_RESEARCH/MULTI_LEAGUE_REPLICATION_CLASSIFICATION_V1.md`
- `docs/04_RESEARCH/H8_COMPOSITE_PRESSURE_SCORE_RESULTS_V1.md`
- `docs/04_RESEARCH/DYNAMIC_TRADE_PROTOCOL_VALIDATION_RESULTS_V1.md`

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
- `docs/08_DATABASE/FOOTBALL_DATA_PHASE2_FULL_IMPORT_REPORT.md`
- `docs/04_RESEARCH/ODDS_DATASET_SPEC_V1.md`
- `docs/04_RESEARCH/ODDS_INITIAL_STATISTICAL_VALIDATION_RESULTS.md`
- `docs/04_RESEARCH/ODDS_INTERACTION_VALIDATION_RESULTS_V1.md`

---

## Artefatos Football-Data

- `database/migrations/20260608_create_football_data_storage_tables.sql`
- `Importer/FootballData/football_data_importer.py`
- `Analytics/FeatureBuilder/odds_feature_builder_v1.py`
- `Analytics/DatasetBuilder/odds_dataset_builder_v1.py`
- `data/processed/features/odds_features_v1.csv`
- `data/processed/features/odds_features_v1.parquet`
- `data/processed/features/odds_features_v1_metadata.json`
- `data/processed/features/odds_features_v1_validation_report.json`
- `data/processed/datasets/late_goal_dataset_odds_v1.csv`
- `data/processed/datasets/late_goal_dataset_odds_v1.parquet`
- `data/processed/datasets/late_goal_dataset_odds_v1_metadata.json`
- `data/processed/datasets/late_goal_dataset_odds_v1_validation_report.json`

---

## Estado Atual H8

- Feature Builder H8 V1 executado.
- Dataset H8 V1 criado.
- Baseline H8 V1 executado.
- Decisao quantitativa baseline: NAO APROVADO.
- Composite Pressure Score V1 executado com 5040 resultados disponiveis.
- Composite Pressure Score V1 gerou sinais locais e micro-amostras, mas nenhum padrao robusto autorizado.
- O H8 atual mede pressao agregada da partida, nao pressao por equipe.
- Proxima evolucao tecnica relevante: `H8_TEAM_SIDE_FEATURES_V1`.
- Producao, trade real, modelo e backtesting real seguem bloqueados.

---

## Estado Atual Odds Historicas

### Football-Data EPL 2024/25

- CSV publico analisado: 380 partidas.
- Mercados importados: 1X2, Over/Under 2.5 e Asian Handicap.
- Odds closing presentes.
- Odds opening-like/pre-close preservadas como `opening_like`, sem assumir opening odds oficiais.
- Odds live ausentes.
- Match mapping com SofaScore: 380/380 partidas importaveis pareadas.
- Taxa de pareamento: 100%.
- Conflitos de placar: 0.
- Ambiguidades relevantes: 0.
- Football-Data staging rows: 380.
- Football-Data mappings: 380.
- Football-Data odds: 34280.
- Duplicatas por grain: 0.
- Orfaos: 0.
- Odds invalidas: 0.
- Idempotencia: reexecucao com 0 inserts, 34280 updates e contagem final estavel.
- `Max`, `MaxC`, `Avg` e `AvgC` preservados como agregadores distintos.
- Odds Features V1: 380 linhas, 380 partidas unicas, 1 linha por `match_id`.
- Cobertura Odds Features V1: 100% para 1X2 e Over/Under 2.5.
- Validation report Odds Features V1: APTO.
- Dataset Odds V1: 380 linhas, 380 partidas unicas, 1 linha por `match_id`.
- Target `target_late_goal_75`: 191 negativos e 189 positivos.
- Validation report Dataset Odds V1: APTO COM RESSALVAS.
- Nenhum target-derived feature em X, placar final, odds live/in-play ou Asian Handicap incluido nas features V1.
- Odds isoladas e Odds+H8 nao sustentam frente principal no momento.

---

## Issues Ativas

- Issue #1: `MARKET_PRICE_CASHOUT_SENSITIVITY_V1` — roadmap de pesquisa, correcao de artefatos e analise financeira/cashout teorica.
- Issue #2: `DYNAMIC_TRADE_PROTOCOL_VALIDATION_V2` — expansao controlada dos testes dinamicos.

---

## Restricoes Ativas

- Nao criar robo.
- Nao iniciar trade real.
- Nao iniciar backtesting financeiro real.
- Nao iniciar producao.
- Nao transformar nenhum resultado exploratorio em sistema decisorio.
- Nao usar odds live se nao existirem com timestamp historico confiavel.
- Nao tratar odds medias fixas como precos historicos reais.
- Nao otimizar por p-hacking.
- Nao usar features fora de whitelist aprovada.
- Nao usar eventos apos cutoff como features.
- Nao usar placar final como feature.
- Nao tratar `opening_like` como opening odds oficial sem auditoria metodologica.

---

## Proximos Passos

- [ ] Codex verificar/corrigir JSONs vazios de `MATCH_STATE_ODDS_H8_VARIATION_V1`.
- [ ] Quant Research produzir/revisar `DYNAMIC_TRADE_PROTOCOL_EXPANSION_PLAN_V1.md` antes da Validation V2.
- [ ] Executar `DYNAMIC_TRADE_PROTOCOL_VALIDATION_V2` somente apos plano aprovado.
- [ ] Quant Research especificar `MARKET_PRICE_CASHOUT_SENSITIVITY_V1` com EV hold-to-loss, EV com cashout, ROI e break-even por janela.
- [ ] Quant Research revisar `H8_COMPOSITE_PRESSURE_SCORE_RESULTS_V1.md` e selecionar sinais para replicacao multi-liga.
- [ ] Data Science / Data Engineering especificar `H8_TEAM_SIDE_FEATURES_V1`.
- [ ] Manter backtesting real, producao, robo e trade real bloqueados.

---

## Status

EM EXECUCAO - A PESQUISA AVANCOU PARA PADROES EXPLORATORIOS DE MERCADO E PROTOCOLOS DINAMICOS COM ODDS MEDIAS FIXAS. H8 BASELINE V1 NAO FOI APROVADO, ODDS ISOLADAS NAO SUSTENTARAM FRENTE PRINCIPAL, MAS H8 COMPOSITE PRESSURE E DYNAMIC TRADE PROTOCOL V1 GERARAM SINAIS EXPLORATORIOS QUE JUSTIFICAM EXPANSAO CONTROLADA. PROXIMAS PRIORIDADES: CORRIGIR JSONS VAZIOS, CRIAR/REVISAR EXPANSION PLAN V1, EXECUTAR VALIDATION V2 COM CONTROLE DE P-HACKING, ESPECIFICAR CASHOUT SENSITIVITY E AVANCAR H8_TEAM_SIDE_FEATURES_V1. PRODUCAO, ROBO, TRADE REAL, MODELO E BACKTESTING REAL PERMANECEM BLOQUEADOS.
