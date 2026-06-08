# FOOTBALL-DATA PHASE 1 IMPLEMENTATION REPORT

## Objetivo

Registrar o resultado da Fase 1 Football-Data aprovada pelo CTO:

- migration controlada;
- importer controlado;
- `--dry-run`;
- teste em pequena amostra;
- validacoes de idempotencia, FK, contagens, rastreabilidade e integridade dos mercados.

Esta execucao nao criou features, datasets, modelagem, baseline, crawler ou carga completa das 380 partidas.

---

## Artefatos Implementados

- `database/migrations/20260608_create_football_data_storage_tables.sql`
- `Importer/FootballData/football_data_importer.py`

## Arquivos de Referencia

- `docs/08_DATABASE/FOOTBALL_DATA_STORAGE_IMPORT_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_SCHEMA_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_MIGRATION_SPEC.md`
- `docs/08_DATABASE/FOOTBALL_DATA_IMPORTER_SPEC.md`

---

## Resultado da Migration

Migration aplicada localmente no PostgreSQL.

Tabelas criadas:

- `football_data_csv_files`
- `football_data_staging_rows`
- `football_data_match_mapping`
- `football_data_odds`

Contagens imediatamente apos migration:

| Tabela | Registros |
|---|---:|
| `football_data_csv_files` | 0 |
| `football_data_staging_rows` | 0 |
| `football_data_match_mapping` | 0 |
| `football_data_odds` | 0 |

Resultado:

- Migration criou apenas estrutura.
- Nenhum dado foi importado pela migration.
- Nenhuma tabela SofaScore foi alterada.
- Nenhuma feature/dataset/modelagem foi criada.

### Decisao de FK

FKs fisicas criadas:

- `football_data_staging_rows.csv_file_id -> football_data_csv_files.id`
- `football_data_match_mapping.staging_row_id -> football_data_staging_rows.id`
- `football_data_match_mapping.match_id -> matches_master.match_id`
- `football_data_odds.staging_row_id -> football_data_staging_rows.id`
- `football_data_odds.mapping_id -> football_data_match_mapping.id`
- `football_data_odds.match_id -> matches_master.match_id`

Nao foi criada FK fisica em `sofascore_event_id`, porque `matches_master.sofascore_event_id` nao possui unique constraint no schema atual. O campo foi preservado e indexado para rastreabilidade.

---

## Resultado do Importer

Importer implementado em:

```text
Importer/FootballData/football_data_importer.py
```

Comandos suportados:

- `--dry-run`
- `--stage-only`
- `--map-only`
- `--odds-only`
- `--all`
- `--limit`

Regras implementadas:

- usa `config.database.engine`;
- nao cria `create_engine` proprio;
- nao hardcoda credenciais no importer;
- segue staging-first;
- calcula `source_hash`;
- preserva `raw_row_json`;
- faz mapping por times normalizados + placar + validacao de data;
- nao promove odds sem mapping confiavel;
- preserva `source_file`, `source_url`, `source_hash`, `row_number`, `source_column` e `source_column_semantics`;
- nao baixa CSV;
- nao cria features/datasets.

---

## Resultado do Dry-run

Comando executado:

```bash
python C:\LateGoalResearch\Importer\FootballData\football_data_importer.py --csv C:\LateGoalResearch\data\raw\football_data\england\premier_league_2024_2025\E0_2024_2025.csv --season 2024-2025 --competition EPL --dry-run --limit 5
```

Resultado:

| Item | Resultado |
|---|---:|
| Linhas processadas | 5 |
| Colunas detectadas | 120 |
| Mappings simulados | 5 mapped |
| Odds estimadas | 470 |
| Escritas no banco | 0 |

Odds estimadas por mercado:

| Mercado | Odds |
|---|---:|
| `match_odds_1x2` | 270 |
| `over_under_2_5` | 100 |
| `asian_handicap` | 100 |

Odds estimadas por tipo:

| Tipo | Odds |
|---|---:|
| `opening_like` | 165 |
| `closing` | 165 |
| `average` | 70 |
| `maximum` | 70 |

Validacao pos-dry-run:

- `football_data_csv_files`: 0
- `football_data_staging_rows`: 0
- `football_data_match_mapping`: 0
- `football_data_odds`: 0

Resultado: dry-run validado sem escrita.

---

## Teste Controlado em Pequena Amostra

Comando executado:

```bash
python C:\LateGoalResearch\Importer\FootballData\football_data_importer.py --csv C:\LateGoalResearch\data\raw\football_data\england\premier_league_2024_2025\E0_2024_2025.csv --season 2024-2025 --competition EPL --all --limit 5
```

Resultado apos importacao limpa da amostra:

| Item | Resultado |
|---|---:|
| Linhas processadas | 5 |
| Staging rows | 5 |
| Mapping rows | 5 |
| Unmapped rows | 0 |
| Odds rows | 470 |
| Failed rows | 0 |
| Invalid odds | 0 |
| Duplicatas por grain | 0 |
| Orfaos | 0 |

Mappings:

| Status | Registros |
|---|---:|
| `mapped` | 5 |

Odds por mercado:

| Mercado | Odds |
|---|---:|
| `match_odds_1x2` | 270 |
| `over_under_2_5` | 100 |
| `asian_handicap` | 100 |

Odds por tipo:

| Tipo | Odds |
|---|---:|
| `opening_like` | 165 |
| `closing` | 165 |
| `average` | 70 |
| `maximum` | 70 |

Bookmakers/agregadores:

| Bookmaker/agregador | Odds |
|---|---:|
| `B365` | 70 |
| `BFE` | 70 |
| `Avg` | 35 |
| `AvgC` | 35 |
| `Max` | 35 |
| `MaxC` | 35 |
| `P` | 40 |
| `1XB` | 30 |
| `BF` | 30 |
| `BW` | 30 |
| `PS` | 30 |
| `WH` | 30 |

---

## Resultado da Idempotencia

A mesma amostra foi reexecutada apos a importacao controlada.

Resultado da reexecucao:

| Item | Resultado |
|---|---:|
| Linhas processadas | 5 |
| Staging rows | 5 |
| Mapping rows | 5 |
| Odds inserted | 0 |
| Odds updated | 470 |
| Odds rows totais | 470 |
| Duplicate odds grain | 0 |
| Orphan odds | 0 |

Conclusao:

- reexecucao nao duplicou CSV file;
- reexecucao nao duplicou staging;
- reexecucao nao duplicou mapping;
- reexecucao nao duplicou odds;
- grain aprovado funcionou para a amostra.

---

## Resultado da Validacao

Validacoes executadas com consultas `SELECT`.

### Contagens

| Tabela | Registros |
|---|---:|
| `football_data_csv_files` | 1 |
| `football_data_staging_rows` | 5 |
| `football_data_match_mapping` | 5 |
| `football_data_odds` | 470 |

### Integridade FK / Orfaos

| Validacao | Resultado |
|---|---:|
| staging sem csv_file | 0 |
| mapping sem staging | 0 |
| odds sem mapping ou staging | 0 |
| odds sem match em `matches_master` | 0 |

### Integridade de Mercado

| Validacao | Resultado |
|---|---:|
| odds invalidas (`odds_value <= 0`) | 0 |
| duplicatas por grain | 0 |
| mercados importados | 3 |
| tipos de odds importados | 4 |

---

## Problemas Encontrados e Solucoes

### 1. Colisao inicial de grain para `Max/Avg` e `MaxC/AvgC`

Durante o primeiro teste controlado, `Max/Avg` e `MaxC/AvgC` colidiram no grain porque ambos eram classificados com `bookmaker_or_aggregator = Max/Avg` e `odds_type = maximum/average`.

Impacto:

- a amostra inicial ficou com menos linhas de odds que o esperado;
- valores closing de max/avg poderiam sobrescrever valores nao-C.

Solucao aplicada:

- preservar `MaxC` e `AvgC` como agregadores distintos de `Max` e `Avg`;
- manter `odds_type = maximum/average`;
- preservar flags `is_closing`, `is_average` e `is_maximum`;
- limpar apenas os registros Football-Data de teste do `source_hash` da amostra;
- reexecutar a amostra limpa.

Resultado apos correcao:

- 470 odds na amostra de 5 linhas;
- 0 duplicatas por grain;
- idempotencia validada.

### 2. FK fisica em `sofascore_event_id`

Nao foi criada FK fisica para `sofascore_event_id`, pois `matches_master.sofascore_event_id` nao possui unique constraint no banco atual.

Solucao:

- criar FKs fisicas por `match_id`;
- preservar e indexar `sofascore_event_id`;
- registrar essa decisao para revisao CTO.

---

## Restricoes Respeitadas

- Nao foram criadas features.
- Nao foram criados datasets.
- Nao foi executada modelagem.
- Nao foi executado baseline.
- Nao foi alterado crawler.
- Nao foi alterado SofaScore.
- Nao foi alterado dado bruto.
- Nao foi executada importacao completa das 380 partidas.
- Foi executada apenas amostra controlada de 5 linhas.

---

## Recomendacao

Recomendacao: **APTO PARA REVISAO CTO DA CARGA COMPLETA**.

Antes de autorizar a importacao completa das 380 partidas, recomenda-se CTO revisar:

1. Decisao de nao criar FK fisica em `sofascore_event_id`.
2. Uso de `handicap_line_key` para resolver unique com `NULL`.
3. Tratamento de `MaxC` e `AvgC` como agregadores distintos no grain.
4. Resultado da amostra controlada: 5/5 mapped, 470 odds, 0 duplicatas, 0 orfaos.

Se aprovado, proximo passo operacional:

```bash
python C:\LateGoalResearch\Importer\FootballData\football_data_importer.py --csv C:\LateGoalResearch\data\raw\football_data\england\premier_league_2024_2025\E0_2024_2025.csv --season 2024-2025 --competition EPL --all
```

Esse comando ainda nao foi executado nesta fase.
