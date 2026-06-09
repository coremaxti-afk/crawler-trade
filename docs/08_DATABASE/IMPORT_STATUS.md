# IMPORT STATUS

## Objetivo

Acompanhar o estado da importacao dos dados coletados para o PostgreSQL.

---

## Resumo Executivo Atual

Status geral da area Data Engineer / Database:

- SofaScore core importado e validado.
- Validacao leve pos-importacao SofaScore concluida.
- H8 Graph/Shotmap armazenado, importado e validado.
- Football-Data Phase 1 executada em amostra controlada.
- Football-Data Phase 2 executada com importacao completa das 380 partidas.
- Backtesting financeiro e producao seguem bloqueados.

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

## SofaScore Core

### Season Collector

Status:

Implementado.

Artefatos:

- `inventory.json`
- `rounds.json`
- `round_XX_events.json`

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
- Partida descartada da importacao atual: `12436452`.

Observacao:

- A partida `12436449` foi corrigida/coletada com os 3 JSONs core e esta importada.
- `lineups.json` e `h2h.json` seguem preservados como dados brutos complementares, mas nao foram importados nesta etapa.

---

## SofaScore Importer Core

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

Regras aplicadas:

- Usa `from config.database import engine`.
- Usa SQLAlchemy com `engine.begin()` e `sqlalchemy.text`.
- Classifica partidas em `full`, `core`, `incomplete` e `known_skipped`.
- Pula `KNOWN_SKIPPED_MATCH_IDS = {"12436452"}`.
- Importa apenas partidas full/core.
- Erro por partida nao interrompe todo o lote.
- Reexecucao nao duplica registros.

### Validacao Executada

Dry-run:

- full: 192
- core: 188
- importable: 380
- known_skipped: 1
- incomplete: 0
- missing: 0

Primeira importacao real:

- processed: 380
- inserted: 380
- updated: 0
- failed: 0
- known_skipped: 1

Segunda execucao / idempotencia:

- processed: 380
- inserted: 0
- updated: 380
- failed: 0
- known_skipped: 1

Validacao SQL final:

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

## Validacao Leve de Qualidade Pos-Importacao SofaScore

Status:

APTO COM RESSALVAS para inicio da fase Quant Research.

Script:

- `LateGoalResearch/Crawler/Sofascore/validate_sofascore_import_quality.py`

Relatorios gerados localmente:

- `data/reports/sofascore_import_quality_report.md`
- `data/reports/sofascore_import_quality_report.json`

Escopo:

- Validacao somente leitura.
- Uso de `config.database.engine`.
- Execucao apenas de consultas `SELECT`.
- Nenhuma alteracao em schema, dados brutos, importer, collectors, features ou modelagem.

Contagens validadas:

- `matches_master`: 380 / 380.
- `match_statistics`: 380 / 380.
- `match_incidents`: 7647 / 7647.

Incidentes por partida:

- Minimo: 12.
- Maximo: 30.
- Media: 20.1237.
- Mediana: 20.0.
- Partidas com 0 incidentes: 0.

Tipos de incidentes:

- Tipos nulos: 0.
- Tipos raros <= 3: 0.

Distribuicao:

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

Divergencias entre `matches_master` e `match_incidents`:

- Divergencias encontradas: 0.

`match_statistics`:

- Linhas: 380.
- Linhas vazias: 0.
- Partidas sem estatisticas: 0.

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

Conclusao:

A base SofaScore EPL importada esta tecnicamente apta para Quant Research com ressalvas documentadas. A principal ressalva e a existencia de 7 nulos em `big_chances_home` e 7 nulos em `big_chances_away`.

---

## H8 Graph / Shotmap Import

Status:

Implementado, importado e validado.

Documentos:

- `docs/08_DATABASE/H8_STORAGE_IMPORT_SPEC.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_AUDIT_20260606.md`
- `docs/03_SOURCES/SOFASCORE/SHOTMAP_ENDPOINT.md`

Tabelas populadas:

- `match_graph`
- `match_shotmap`
- `match_source_status`

Resultados:

- `match_graph`: 34861 pontos em 379 partidas.
- `match_shotmap`: 9883 finalizacoes em 380 partidas.
- `match_source_status`: 760 registros.
- Duplicatas em `match_graph`: 0.
- Duplicatas em `match_shotmap`: 0.
- Duplicatas em `match_source_status`: 0.

Excecao conhecida:

- `sofascore_event_id = 12437015`
- Partida: Crystal Palace x Liverpool FC
- Artefato: `graph.json`
- Status: `known_missing`
- HTTP status: 404
- Decisao: `keep_match_exclude_graph_required_outputs`
- Linhas em `match_graph` para `12437015`: 0.

Observacoes:

- `match_graph` usa `momentum_value` como valor bruto de momentum do payload.
- O sinal de `momentum_value` nao foi normalizado, invertido ou transformado na importacao.
- `shotmap` foi preservado como dado bruto granular de finalizacoes, sem virar feature nesta etapa.

Conclusao:

H8 storage/importer esta aprovado para consumo posterior por etapas explicitamente autorizadas. A excecao `12437015` deve permanecer documentada e ser excluida apenas de features/datasets que exijam graph completo.

---

## Football-Data Storage / Import

### Documentacao Tecnica

Documentos consolidados:

- `docs/08_DATABASE/FOOTBALL_DATA_STORAGE_IMPORT_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_SCHEMA_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_MIGRATION_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_IMPORTER_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_PHASE1_IMPLEMENTATION_REPORT.md`
- `docs/08_DATABASE/FOOTBALL_DATA_PHASE2_FULL_IMPORT_REPORT.md`

### Phase 1 - Amostra Controlada

Status:

Executada e validada.

Artefatos implementados:

- `database/migrations/20260608_create_football_data_storage_tables.sql`
- `Importer/FootballData/football_data_importer.py`

Migration:

- Aplicada localmente.
- Criou apenas estrutura.
- Nenhum dado foi importado pela migration.
- Nenhuma tabela SofaScore foi alterada.
- Nenhuma feature, dataset ou modelagem foi criada.

Tabelas criadas:

- `football_data_csv_files`
- `football_data_staging_rows`
- `football_data_match_mapping`
- `football_data_odds`

Importer:

- Usa `config.database.engine`.
- Nao cria `create_engine` proprio.
- Nao hardcoda credenciais.
- Segue staging-first.
- Calcula `source_hash`.
- Preserva `raw_row_json`.
- Faz mapping por times normalizados + placar + validacao de data.
- Nao promove odds sem mapping confiavel.
- Preserva `source_file`, `source_url`, `source_hash`, `row_number`, `source_column` e `source_column_semantics`.
- Nao baixa CSV.
- Nao cria features/datasets.

Amostra controlada:

- Linhas processadas: 5.
- Staging rows: 5.
- Mapping rows: 5.
- Unmapped rows: 0.
- Odds rows: 470.
- Failed rows: 0.
- Invalid odds: 0.
- Duplicatas por grain: 0.
- Orfaos: 0.

Idempotencia da amostra:

- Odds inserted no rerun: 0.
- Odds updated no rerun: 470.
- Odds rows totais: 470.
- Duplicate odds grain: 0.
- Orphan odds: 0.

Decisoes tecnicas registradas:

- `Max` e `MaxC` preservados como agregadores distintos.
- `Avg` e `AvgC` preservados como agregadores distintos.
- FK fisica por `match_id`.
- `sofascore_event_id` preservado e indexado, sem FK fisica, porque `matches_master.sofascore_event_id` nao possui unique constraint no schema atual.
- `handicap_line_key` usado para resolver unique com `NULL`.

### Phase 2 - Importacao Completa

Status:

Executada e validada.

CSV bruto:

- `data/raw/football_data/england/premier_league_2024_2025/E0_2024_2025.csv`

Source hash:

```text
d0c8ce4a96d886cf60cf101f570f4a3893844226f91c7bd769eb568c49edbfa4
```

Resultado da carga completa:

- processed_rows: 380.
- staged_rows: 380.
- mapped_rows: 380.
- unmapped_rows: 0.
- odds_inserted: 33810.
- odds_updated: 470.
- failed_rows: 0.
- rows_without_mapping: 0.
- rows_not_mapped: 0.
- odds_rows finais: 34280.

Resultado da idempotencia:

- Reexecucao com o mesmo comando.
- processed_rows: 380.
- staged_rows: 380.
- mapped_rows: 380.
- unmapped_rows: 0.
- odds_inserted: 0.
- odds_updated: 34280.
- failed_rows: 0.
- odds_rows finais: 34280.

Contagens finais:

- `football_data_csv_files`: 1.
- `football_data_staging_rows`: 380.
- `football_data_match_mapping`: 380.
- `football_data_odds`: 34280.

Validacao de integridade:

- duplicate_staging_grain: 0.
- duplicate_mapping_grain: 0.
- duplicate_odds_grain: 0.
- staging_without_csv: 0.
- mapping_without_staging: 0.
- mapping_without_match_master: 0.
- odds_without_mapping_or_staging: 0.
- odds_without_match_master: 0.
- invalid_odds (`odds_value <= 0`): 0.

Distribuicao por mercado:

- `match_odds_1x2`: 19098.
- `over_under_2_5`: 7582.
- `asian_handicap`: 7600.

Distribuicao por tipo de odds:

- `opening_like`: 11802.
- `closing`: 11838.
- `average`: 5320.
- `maximum`: 5320.

Bookmakers/agregadores:

- `B365`: 5320.
- `BFE`: 5314.
- `P`: 3028.
- `Avg`: 2660.
- `AvgC`: 2660.
- `Max`: 2660.
- `MaxC`: 2660.
- `PS`: 2280.
- `BF`: 2277.
- `1XB`: 2253.
- `WH`: 1734.
- `BW`: 1434.

Semantica das colunas:

- `football_data_non_c_column_preserved_as_opening_like_candidate`: 11802.
- `football_data_c_column_candidate_closing`: 11838.
- `football_data_average_odds`: 5320.
- `football_data_maximum_odds`: 5320.

Observacoes:

- Colunas sem `C` foram preservadas como `opening_like`, sem assumir opening odds oficiais.
- Football-Data continua nao sendo fonte live/in-game.
- `Max/MaxC` e `Avg/AvgC` foram preservados como agregadores distintos.

Conclusao:

Football-Data esta importado, validado e apto para proxima etapa autorizada de Data Engineer / Quant Research. Ainda nao foram criadas features, datasets, modelagem, baseline financeiro, backtesting ou producao.

---

## Tabelas PostgreSQL - Estado Atual

### matches_master

Status:

Populada com 380 partidas SofaScore EPL importaveis.

Origem principal:

- `event.json`

### match_statistics

Status:

Populada com 380 registros de estatisticas agregadas.

Origem principal:

- `statistics.json`

### match_incidents

Status:

Populada com 7647 incidentes.

Origem principal:

- `incidents.json`

### match_graph

Status:

Populada com 34861 pontos de graph em 379 partidas.

Origem principal:

- `graph.json`

### match_shotmap

Status:

Populada com 9883 finalizacoes em 380 partidas.

Origem principal:

- `shotmap.json`

### match_source_status

Status:

Populada com 760 registros de cobertura/status de artefatos SofaScore H8.

### football_data_csv_files

Status:

Populada com 1 versao de CSV Football-Data EPL 2024/25.

### football_data_staging_rows

Status:

Populada com 380 linhas staging Football-Data EPL 2024/25.

### football_data_match_mapping

Status:

Populada com 380 mappings Football-Data x SofaScore.

### football_data_odds

Status:

Populada com 34280 odds Football-Data EPL 2024/25.

---

## Restricoes Ativas

- Nao iniciar backtesting financeiro sem aprovacao explicita.
- Nao iniciar producao.
- Nao transformar baseline em sistema decisorio.
- Nao usar Football-Data como fonte live/in-game.
- Nao assumir colunas `opening_like` como opening odds oficiais sem auditoria adicional.
- Nao criar features/datasets adicionais sem autorizacao da frente responsavel.

---

## Proximo Marco

Proximas etapas possiveis, sob nova autorizacao:

1. Revisar contrato de consumo das odds por Quant Research.
2. Definir quais odds podem ser usadas como pre-match sem leakage.
3. Auditar `opening_like` antes de uso como proxy de opening odds.
4. Criar plano de dataset odds-aware, sem leakage.
5. Manter backtesting financeiro e producao bloqueados ate nova aprovacao.

---

## Status

ATUALIZADO - SofaScore core, H8 Graph/Shotmap e Football-Data EPL 2024/25 estao importados e validados nos limites documentados. A area de banco esta pronta para proxima decisao de consumo analitico, mantendo bloqueios de producao e backtesting financeiro.