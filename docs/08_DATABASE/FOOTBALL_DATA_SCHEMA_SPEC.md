# FOOTBALL-DATA SCHEMA SPEC

## Objetivo

Definir a especificacao tecnica futura de schema para armazenamento de odds historicas Football-Data no projeto LateGoalResearch.

Este documento e apenas especificacao. Nao autoriza implementacao, migration, alteracao de PostgreSQL, importer, features, datasets, modelagem ou execucao operacional.

---

## Escopo

Incluido:

- tabelas futuras;
- grain das tabelas;
- colunas minimas;
- PK;
- FK;
- constraints;
- indices;
- relacionamento com `match_id` e `sofascore_event_id`.

Fora do escopo:

- codigo;
- migration executavel;
- importer;
- feature engineering;
- dataset analitico;
- modelagem;
- backtesting;
- producao.

---

## Premissas

- Football-Data EPL 2024/25 possui 380 partidas pareadas com SofaScore.
- Taxa de pareamento Football-Data x SofaScore: 100%.
- Ambiguidades: 0.
- Conflitos de placar: 0.
- Conflitos de nomes foram resolvidos por dicionario explicito.
- Nenhum registro deve avancar para camada definitiva sem `sofascore_event_id` confiavel.
- `match_id` deve ser a chave interna do projeto quando disponivel.
- `sofascore_event_id` deve ser preservado para rastreabilidade e reconciliacao multi-fonte.

---

## Visao Geral do Modelo

Modelo futuro recomendado:

```text
football_data_csv_files
  -> football_data_staging_rows
  -> football_data_match_mapping
  -> football_data_odds
```

Objetivo:

- preservar CSV bruto;
- permitir staging-first;
- separar mapping de odds;
- manter rastreabilidade completa ate linha original;
- permitir reprocessamento idempotente por versao de CSV.

---

# 1. Tabela `football_data_csv_files`

## Objetivo

Registrar cada versao de CSV Football-Data processada ou disponivel para processamento.

## Grain

Uma linha por arquivo/versionamento de conteudo.

Grain conceitual:

```text
source_hash
```

## Colunas Minimas

- `id`
- `competition_code`
- `season`
- `source_name`
- `source_url`
- `source_file`
- `source_hash`
- `downloaded_at`
- `registered_at`
- `row_count`
- `notes`

## PK

- `id`

## Constraints

- `UNIQUE(source_hash)`
- `source_name` deve ser `football-data`
- `source_hash` nao deve ser nulo
- `source_file` nao deve ser nulo

## Indices Recomendados

- `idx_fd_csv_files_source_hash`
- `idx_fd_csv_files_competition_season`
- `idx_fd_csv_files_source_file`

## Observacoes

- `source_hash` deve ser calculado sobre o conteudo real do CSV.
- Arquivos com mesmo nome e hash diferente devem ser tratados como versoes distintas.
- Arquivos com nomes diferentes e mesmo hash podem ser tratados como duplicatas logicas.

---

# 2. Tabela `football_data_staging_rows`

## Objetivo

Preservar linhas originais do CSV Football-Data em staging, sem transformacao destrutiva.

## Grain

Uma linha por linha original do CSV por versao de arquivo.

Grain conceitual:

```text
source_hash + row_number
```

## Colunas Minimas

- `id`
- `csv_file_id`
- `source_hash`
- `row_number`
- `raw_row_json` JSONB
- `division`
- `match_date`
- `home_team_raw`
- `away_team_raw`
- `home_goals`
- `away_goals`
- `result_raw`
- `created_at`

## PK

- `id`

## FK

- `csv_file_id` -> `football_data_csv_files.id`

## Constraints

- `UNIQUE(source_hash, row_number)`
- `source_hash` nao deve ser nulo
- `row_number` nao deve ser nulo
- `raw_row_json` nao deve ser nulo

## Indices Recomendados

- `idx_fd_staging_source_hash_row_number`
- `idx_fd_staging_match_date`
- `idx_fd_staging_home_away_raw`
- `idx_fd_staging_csv_file_id`

## Observacoes

- `raw_row_json` deve preservar todas as colunas originais do CSV.
- Colunas derivadas em staging devem servir apenas para validacao/mapping.
- Linhas nao pareadas devem permanecer em staging.

---

# 3. Tabela `football_data_match_mapping`

## Objetivo

Registrar o mapping auditavel entre linha Football-Data, `sofascore_event_id` e `match_id`.

## Grain

Uma linha por linha de staging mapeada para uma partida oficial.

Grain conceitual:

```text
source_hash + row_number -> sofascore_event_id -> match_id
```

## Colunas Minimas

- `id`
- `staging_row_id`
- `source_hash`
- `row_number`
- `sofascore_event_id`
- `match_id`
- `mapping_status`
- `mapping_method`
- `home_team_normalized`
- `away_team_normalized`
- `score_check_status`
- `ambiguity_flag`
- `conflict_reason`
- `mapped_at`

## PK

- `id`

## FK

- `staging_row_id` -> `football_data_staging_rows.id`
- `match_id` -> tabela oficial de partidas do projeto, se FK fisica for aprovada pelo CTO
- `sofascore_event_id` -> `matches_master.sofascore_event_id`, se FK fisica for aprovada pelo CTO

## Constraints

- `UNIQUE(source_hash, row_number)`
- `sofascore_event_id` nao deve ser nulo para registros promovidos
- `mapping_status` deve distinguir, no minimo:
  - `mapped`
  - `unmapped`
  - `ambiguous`
  - `conflict`
  - `cancelled_or_postponed`

## Indices Recomendados

- `idx_fd_mapping_sofascore_event_id`
- `idx_fd_mapping_match_id`
- `idx_fd_mapping_status`
- `idx_fd_mapping_source_hash_row_number`

## Observacoes

- Nenhuma odd deve ir para armazenamento definitivo sem mapping confiavel.
- Conflitos de nome devem ser resolvidos por dicionario explicito auditavel.
- Placar pode ser usado como validacao auxiliar, nao como unica identidade da partida.

---

# 4. Tabela `football_data_odds`

## Objetivo

Armazenar odds historicas Football-Data em formato granular e rastreavel.

## Grain

Uma linha por odd, por partida, mercado, selecao, tipo de odd, bookmaker/agregador e versao de origem.

Grain conceitual:

```text
sofascore_event_id + market + selection + odds_type + bookmaker_or_aggregator + source_hash
```

Para Asian Handicap, a linha de handicap tambem deve participar do grain:

```text
sofascore_event_id + market + selection + handicap_line + odds_type + bookmaker_or_aggregator + source_hash
```

## Colunas Minimas

- `id`
- `staging_row_id`
- `mapping_id`
- `match_id`
- `sofascore_event_id`
- `source_hash`
- `source_file`
- `source_url`
- `row_number`
- `market`
- `selection`
- `handicap_line`
- `odds_type`
- `bookmaker_or_aggregator`
- `odds_value`
- `source_column`
- `source_column_semantics`
- `is_closing`
- `is_opening_like`
- `is_average`
- `is_maximum`
- `imported_at`

## PK

- `id`

## FK

- `staging_row_id` -> `football_data_staging_rows.id`
- `mapping_id` -> `football_data_match_mapping.id`
- `match_id` -> tabela oficial de partidas do projeto, se FK fisica for aprovada pelo CTO
- `sofascore_event_id` -> `matches_master.sofascore_event_id`, se FK fisica for aprovada pelo CTO

## Constraints

- `odds_value` deve ser positivo quando informado
- `market` nao deve ser nulo
- `selection` nao deve ser nulo
- `odds_type` nao deve ser nulo
- `bookmaker_or_aggregator` nao deve ser nulo
- `source_hash` nao deve ser nulo
- `source_column` nao deve ser nulo

Constraint unica conceitual:

```text
UNIQUE(sofascore_event_id, market, selection, handicap_line, odds_type, bookmaker_or_aggregator, source_hash)
```

Observacao:

- Para mercados sem handicap, `handicap_line` pode ser nulo. O desenho fisico deve considerar como PostgreSQL trata `NULL` em unique constraints antes da migration.

## Indices Recomendados

- `idx_fd_odds_sofascore_event_id`
- `idx_fd_odds_match_id`
- `idx_fd_odds_market_selection`
- `idx_fd_odds_odds_type`
- `idx_fd_odds_bookmaker`
- `idx_fd_odds_source_hash`
- `idx_fd_odds_market_odds_type`

## Mercados Suportados Inicialmente

### Match Odds 1X2

- `market = match_odds_1x2`
- selecoes:
  - `home_win`
  - `draw`
  - `away_win`

### Over/Under 2.5

- `market = over_under_2_5`
- selecoes:
  - `over_2_5`
  - `under_2_5`

### Asian Handicap

- `market = asian_handicap`
- selecoes:
  - `home_handicap`
  - `away_handicap`
- `handicap_line` obrigatoria quando disponivel no CSV

## Tipos de Odds

- `closing`
- `opening_like`
- `average`
- `maximum`

## Semantica das Colunas

- Colunas com `C` devem ser tratadas como candidatas a closing odds conforme documentacao da fonte.
- Colunas sem `C` nao devem ser assumidas automaticamente como opening odds.
- Colunas sem `C` podem ser classificadas como `opening_like` apenas quando houver documentacao no importer/spec ou validacao de fonte.
- A semantica original da coluna Football-Data deve ser preservada em `source_column` e `source_column_semantics`.

---

## Relacionamento com `match_id` e `sofascore_event_id`

Recomendacao:

- `sofascore_event_id` deve ser obrigatorio para promocao a odds definitiva.
- `match_id` deve ser preenchido quando disponivel no banco oficial.
- `sofascore_event_id` garante reconciliacao multi-fonte.
- `match_id` garante integracao com datasets internos.

Fluxo:

```text
football_data_staging_rows
-> football_data_match_mapping
-> matches_master.sofascore_event_id
-> match_id
-> football_data_odds
```

---

## Riscos de Schema

- Unique constraint com `handicap_line` nulo precisa de desenho cuidadoso em PostgreSQL.
- Colunas sem `C` nao podem ser tratadas automaticamente como opening odds.
- Football-Data nao fornece live odds; nao usar como fonte in-game.
- Layout do CSV pode variar entre temporadas.
- Bookmakers/colunas podem ser removidos ou adicionados.
- Normalizacao excessiva antes do primeiro importer pode gerar overengineering.
- FK fisica pode ser util, mas deve ser avaliada contra a flexibilidade de staging e reprocessamento.

---

## Status da Especificacao

Status:

**PRONTA PARA FUTURA IMPLEMENTACAO PELO CODEX APOS APROVACAO CTO**

Esta especificacao nao cria schema, migration, importer, features, dataset ou modelagem.