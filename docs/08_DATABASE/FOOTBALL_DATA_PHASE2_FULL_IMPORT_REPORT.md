# FOOTBALL-DATA PHASE 2 FULL IMPORT REPORT

## Objetivo

Registrar a execucao da Fase 2 Football-Data:

- importacao completa local das 380 partidas Football-Data;
- reexecucao para validacao de idempotencia;
- validacoes finais de contagens, FKs, orfaos, duplicatas, odds invalidas e preservacao de agregadores.

Esta fase nao criou features, datasets, modelagem, baseline, backtesting, crawlers ou alteracoes de dados brutos.

---

## Artefatos Usados

- Importer: `Importer/FootballData/football_data_importer.py`
- CSV bruto: `data/raw/football_data/england/premier_league_2024_2025/E0_2024_2025.csv`
- Migration ja aprovada: `database/migrations/20260608_create_football_data_storage_tables.sql`

Source hash:

```text
d0c8ce4a96d886cf60cf101f570f4a3893844226f91c7bd769eb568c49edbfa4
```

---

## Execucao da Importacao Completa

Comando executado:

```bash
python C:\LateGoalResearch\Importer\FootballData\football_data_importer.py --csv C:\LateGoalResearch\data\raw\football_data\england\premier_league_2024_2025\E0_2024_2025.csv --season 2024-2025 --competition EPL --all
```

Resultado:

| Item | Resultado |
|---|---:|
| processed_rows | 380 |
| staged_rows | 380 |
| mapped_rows | 380 |
| unmapped_rows | 0 |
| odds_inserted | 33810 |
| odds_updated | 470 |
| failed_rows | 0 |
| rows_without_mapping | 0 |
| rows_not_mapped | 0 |
| odds_rows finais | 34280 |

Observacao:

- `470` odds ja existiam da amostra controlada da Fase 1 e foram atualizadas.
- `33810` odds foram inseridas na carga completa.

---

## Resultado da Idempotencia

A importacao completa foi reexecutada com o mesmo comando.

Resultado da reexecucao:

| Item | Resultado |
|---|---:|
| processed_rows | 380 |
| staged_rows | 380 |
| mapped_rows | 380 |
| unmapped_rows | 0 |
| odds_inserted | 0 |
| odds_updated | 34280 |
| failed_rows | 0 |
| odds_rows finais | 34280 |

Conclusao:

- reexecucao nao duplicou CSV file;
- reexecucao nao duplicou staging;
- reexecucao nao duplicou mapping;
- reexecucao nao duplicou odds;
- contagem final permaneceu estavel em `34280` odds.

---

## Contagens Finais

| Tabela | Registros |
|---|---:|
| `football_data_csv_files` | 1 |
| `football_data_staging_rows` | 380 |
| `football_data_match_mapping` | 380 |
| `football_data_odds` | 34280 |

Mapping:

| Status | Registros |
|---|---:|
| `mapped` | 380 |

---

## Validacao de Integridade

| Validacao | Resultado |
|---|---:|
| duplicate_staging_grain | 0 |
| duplicate_mapping_grain | 0 |
| duplicate_odds_grain | 0 |
| staging_without_csv | 0 |
| mapping_without_staging | 0 |
| mapping_without_match_master | 0 |
| odds_without_mapping_or_staging | 0 |
| odds_without_match_master | 0 |
| invalid_odds (`odds_value <= 0`) | 0 |

Resultado:

- 0 duplicatas.
- 0 orfaos.
- 0 odds invalidas.
- 380 mappings validos.
- 380 partidas em staging.

---

## Integridade dos Mercados

Odds por mercado:

| Mercado | Odds |
|---|---:|
| `match_odds_1x2` | 19098 |
| `over_under_2_5` | 7582 |
| `asian_handicap` | 7600 |

Odds por tipo:

| Tipo | Odds |
|---|---:|
| `opening_like` | 11802 |
| `closing` | 11838 |
| `average` | 5320 |
| `maximum` | 5320 |

Bookmakers/agregadores:

| Bookmaker/agregador | Odds |
|---|---:|
| `B365` | 5320 |
| `BFE` | 5314 |
| `P` | 3028 |
| `Avg` | 2660 |
| `AvgC` | 2660 |
| `Max` | 2660 |
| `MaxC` | 2660 |
| `PS` | 2280 |
| `BF` | 2277 |
| `1XB` | 2253 |
| `WH` | 1734 |
| `BW` | 1434 |

---

## Preservacao de Max/Avg e MaxC/AvgC

Validacao especifica:

| Agregador | Odds |
|---|---:|
| `Avg` | 2660 |
| `AvgC` | 2660 |
| `Max` | 2660 |
| `MaxC` | 2660 |

Resultado:

- `Max` e `MaxC` foram preservados como agregadores distintos.
- `Avg` e `AvgC` foram preservados como agregadores distintos.
- Nao houve colisao de grain.

---

## Semantica das Colunas

| source_column_semantics | Odds |
|---|---:|
| `football_data_non_c_column_preserved_as_opening_like_candidate` | 11802 |
| `football_data_c_column_candidate_closing` | 11838 |
| `football_data_average_odds` | 5320 |
| `football_data_maximum_odds` | 5320 |

Observacao:

- Colunas sem `C` foram preservadas como `opening_like`, sem assumir opening odds oficiais.
- Football-Data continua nao sendo fonte live/in-game.

---

## Problemas Encontrados

Nenhum problema novo foi encontrado na Fase 2.

O problema de colisao `Max/Avg` vs `MaxC/AvgC`, identificado na Fase 1, permaneceu corrigido durante a carga completa.

---

## Restricoes Respeitadas

- Nenhuma feature criada.
- Nenhum dataset criado.
- Nenhuma modelagem executada.
- Nenhum backtesting executado.
- Nenhum crawler alterado.
- Nenhum dado bruto alterado.
- Nenhuma alteracao de schema alem da migration ja aprovada.

---

## Recomendacao

Recomendacao: **APTO PARA PROXIMA ETAPA DE DATA ENGINEER / QUANT RESEARCH**.

Possiveis proximas etapas, sob nova autorizacao:

1. Validar contrato de consumo das odds por pesquisa.
2. Criar plano de dataset odds-aware, sem leakage.
3. Definir quais odds podem ser usadas como pre-match.
4. Auditar `opening_like` antes de qualquer uso como proxy de opening odds.
5. Manter proibido backtesting financeiro ate nova aprovacao.
