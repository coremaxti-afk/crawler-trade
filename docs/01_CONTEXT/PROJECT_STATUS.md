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
- Odds Features V1: 380 linhas, 380 partidas unicas, status APTO.
- Dataset Odds V1: 380 linhas, 380 partidas unicas, target unido explicitamente, status APTO COM RESSALVAS.
- H8 Composite Pressure Score V1: 1520 linhas match_id + cutoff, 5040 resultados disponiveis, status exploratorio concluido.

Ressalvas:

- `big_chances_home` possui 7 nulos.
- `big_chances_away` possui 7 nulos.
- `12437015` segue como `known_missing` para `graph.json`, HTTP 404 confirmado.
- Football-Data `opening_like` nao deve ser tratado automaticamente como opening odds oficial.
- Football-Data nao contem odds live/in-game.
- Odds Features V1 usa closing odds sem timestamp individual; tratado como pre-match closing pela semantica da fonte.
- Dataset Odds V1 contem target para validacao supervisionada; X deve usar apenas `feature_columns_for_x`.
- H8 Composite Pressure Score V1 usa graph/momentum agregado da partida, nao pressao por equipe.
- H8 Composite Pressure Score V1 e exploratorio: nao autoriza baseline, modelo, backtesting financeiro real, producao ou trade.

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
- Odds Feature Builder V1 implementado e executado localmente com status APTO.
- Dataset Odds V1 criado com join explicito do `target_late_goal_75` e validation report APTO COM RESSALVAS.
- Odds Initial Statistical Validation concluida: odds pre-jogo isoladas nao apresentaram sinal forte para `target_late_goal_75`.
- Odds Interaction Validation V1 concluida: MANTER 0, OBSERVAR 1, DESCARTAR 11; odds encerradas como frente principal por enquanto.
- Match State + Odds + H8 Variation V1 concluida como exploratoria, com necessidade de verificar/corrigir JSONs vazios no GitHub.
- H8 Composite Pressure Score Results V1 concluido como exploratorio: 5040 resultados disponiveis; MANTER robusto 0; muitos sinais locais/micro-amostra, sem autorizacao para baseline/modelo/backtesting/producao.
- Issue #1 criada para `MARKET_PRICE_CASHOUT_SENSITIVITY_V1` e roadmap de correcao de artefatos/analise financeira exploratoria.

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
- `docs/04_RESEARCH/H8_COMPOSITE_PRESSURE_SCORE_RESULTS_V1.md`

Estado:

- Feature Builder H8 V1 executado.
- Dataset H8 V1 criado.
- Baseline H8 V1 executado e nao aprovado quantitativamente.
- Composite Pressure Score V1 executado conforme plano exploratorio.
- Scores compostos usam shotmap/xG + graph momentum agregado, com pesos fixos nao ajustados por target.
- Classes Composite Pressure V1: DESCARTAR_ESTATISTICO_LOCAL 3837, OBSERVAR 813, MICRO_AMOSTRA_REPLICAR 304, NAO_DISPONIVEL_V1 210, PROMISSOR_LOCAL 86.
- Melhor ranking @70 reportado tem N=2, logo deve ser tratado como micro-amostra/replicacao, nao como padrao robusto.
- Producao, trade, baseline novo, modelo e backtesting seguem bloqueados.

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
- `docs/04_RESEARCH/ODDS_DATASET_SPEC_V1.md`
- `docs/04_RESEARCH/ODDS_INITIAL_STATISTICAL_VALIDATION_RESULTS.md`
- `docs/04_RESEARCH/ODDS_INTERACTION_VALIDATION_RESULTS_V1.md`

Artefatos:

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
- Odds Features V1 geradas com 380 linhas e 1 linha por `match_id`.
- Cobertura Odds Features V1: 380/380 para 1X2, 380/380 para Over/Under 2.5 e 380/380 para ambos.
- Validation report Odds Features V1: APTO, 0 duplicatas, 0 odds invalidas, 0 probabilidades invalidas, 0 target columns e 0 Asian Handicap.
- Dataset Odds V1 gerado com 380 linhas e 1 linha por `match_id`.
- Target `target_late_goal_75` unido explicitamente: 191 negativos e 189 positivos.
- Validation report Dataset Odds V1: APTO COM RESSALVAS, 0 duplicatas, 0 target mismatches, 0 odds invalidas, 0 probabilidades invalidas, 0 Asian Handicap, 0 live/in-play e 0 full-match columns.
- Validacao estatistica inicial de odds isoladas: MANTER 0; OBSERVAR favorite_strength, match_balance e favorite_side=none_clear; DESCARTAR isolado implied_prob_over25_norm e over25_closing_strength.
- Odds Interaction Validation V1: unico sinal OBSERVAR foi `match_balance_high + shots_last_10m_high @60`, fraco e instavel; odds encerradas como frente principal por enquanto.

---

## Status das Hipoteses

- H1 - BLOQUEADA por data leakage.
- H2 - BLOQUEADA por data leakage.
- H3 - MANTER COMO CANDIDATA, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H4 - MANTER COMO CANDIDATA FORTE, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H5 - NAO VALIDADA.
- H6 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.
- H7 - NAO VALIDADA COMO HIPOTESE INDEPENDENTE.
- H8 - FRENTE EXPLORATORIA ATIVA; baseline V1 nao aprovado, Composite Pressure Score V1 gerou sinais locais/micro-amostra para replicacao, mas nenhum sinal robusto autorizado.
- H9 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.
- Odds Historicas - DATASET V1 E VALIDACOES CONCLUIDAS; odds isoladas e odds+H8 nao sustentam frente principal no momento.

---

## Proximas Etapas

1. Codex verificar/corrigir JSONs vazios de `MATCH_STATE_ODDS_H8_VARIATION_V1`.
2. Quant Research especificar `MARKET_PRICE_CASHOUT_SENSITIVITY_V1` com EV hold-to-loss, EV com cashout, ROI e break-even por janela.
3. Quant Research revisar `H8_COMPOSITE_PRESSURE_SCORE_RESULTS_V1.md` e selecionar quais sinais entram em replicacao multi-liga.
4. Data Science / Data Engineering especificar `H8_TEAM_SIDE_FEATURES_V1` para separar pressao por equipe.
5. Nao iniciar backtesting financeiro real.
6. Nao iniciar producao.
7. Nao usar odds live nao timestampadas.
8. Nao tratar sinais `PROMISSOR_LOCAL` ou `MICRO_AMOSTRA_REPLICAR` como estrategia operacional.

---

## Status

EM EXECUCAO - H8 E ODDS EVOLUIRAM PARA PESQUISA EXPLORATORIA DE PADROES, MERCADO E CASHOUT. BASELINES H3/H4, H6/H9 E H8 V1 NAO FORAM APROVADOS QUANTITATIVAMENTE. FOOTBALL-DATA FASE 2 E ODDS DATASET V1 FORAM CONCLUIDOS, MAS ODDS ISOLADAS E ODDS+H8 NAO SUSTENTARAM FRENTE PRINCIPAL. H8 COMPOSITE PRESSURE SCORE V1 GEROU SINAIS LOCAIS/MICRO-AMOSTRA, SEM AUTORIZACAO PARA MODELO, BASELINE, BACKTESTING, PRODUCAO OU TRADE REAL. PROXIMAS PRIORIDADES: CORRIGIR JSONS VAZIOS, ESPECIFICAR MARKET_PRICE_CASHOUT_SENSITIVITY_V1, REVISAR SINAIS PARA REPLICACAO MULTI-LIGA E CRIAR H8_TEAM_SIDE_FEATURES_V1.
