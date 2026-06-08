# FOOTBALL-DATA IMPORTER SPEC

## 1. Objetivo

Definir a especificacao futura do importer Football-Data para o projeto LateGoalResearch, sem criar importer.

Este documento e exclusivamente documental. Ele nao implementa codigo, nao cria migration, nao altera schema, nao altera PostgreSQL, nao importa dados, nao cria features, nao cria datasets, nao modela e nao executa baseline.

Objetivo do importer futuro, se aprovado pelo CTO:

- importar CSV Football-Data de forma staging-first;
- preservar rastreabilidade completa por arquivo, hash, linha e coluna original;
- construir mapping confiavel Football-Data x SofaScore;
- armazenar odds historicas apenas para linhas com mapping confiavel;
- ser idempotente e reexecutavel;
- permitir dry-run sem escrita no banco.

---

## 2. Escopo

Incluido:

- arquitetura sugerida;
- comandos previstos;
- fluxo de importacao;
- idempotencia;
- dry-run;
- rastreabilidade;
- versionamento de CSV;
- tratamento de erros;
- validacoes pos-importacao;
- logs e resumo final;
- restricoes e criterios de aceite.

Excluido:

- implementacao real;
- codigo Python;
- migration;
- schema;
- alteracao de PostgreSQL;
- download de CSV;
- features;
- datasets;
- modelagem;
- baseline;
- backtesting;
- producao.

---

## 3. Arquitetura

Local sugerido para future implementation:

```text
LateGoalResearch/Importer/FootballData/football_data_importer.py
```

Regras obrigatorias para future implementation:

- usar `config.database.engine`;
- nao criar `create_engine` novo;
- nao hardcodar credenciais;
- usar SQLAlchemy `text` / `engine.begin`;
- seguir arquitetura staging-first;
- nao baixar CSV;
- nao alterar crawlers;
- nao alterar SofaScore;
- nao alterar dados brutos;
- nao criar features/datasets.

### 3.1 Funcoes Internas Sugeridas

Funcoes sugeridas para future implementation:

- `register_csv_file()`;
- `import_staging_rows()`;
- `build_match_mapping()`;
- `import_odds()`;
- `validate_import()`;
- `write_summary()`.

### 3.2 Responsabilidades das Funcoes

#### register_csv_file()

Responsavel por:

- receber caminho do CSV;
- calcular `source_hash`;
- registrar ou reconhecer versao em `football_data_csv_files`;
- preservar `source_file`, `source_url`, `competition_code`, `season` e `row_count`;
- respeitar idempotencia por `source_hash`.

#### import_staging_rows()

Responsavel por:

- ler CSV bruto;
- preservar todas as colunas em `raw_row_json`;
- preencher colunas minimas de validacao/mapping;
- gravar staging por `source_hash + row_number`;
- nao descartar linhas sem mapping;
- nao transformar odds em features.

#### build_match_mapping()

Responsavel por:

- aplicar dicionario explicito de nomes de times;
- parear linhas com SofaScore/matches_master;
- registrar `sofascore_event_id` e `match_id` quando confiaveis;
- registrar status para linhas `mapped`, `unmapped`, `ambiguous`, `conflict` ou `cancelled_or_postponed`;
- bloquear promocao de linhas ambiguas ou conflitantes.

#### import_odds()

Responsavel por:

- extrair odds por mercado suportado;
- preservar `source_column` e `source_column_semantics`;
- classificar `odds_type` sem inferencia indevida;
- preservar `handicap_line` exatamente como fornecida;
- gravar apenas odds de linhas com mapping confiavel;
- nao inferir odds ausentes.

#### validate_import()

Responsavel por:

- comparar total de linhas CSV vs staging;
- validar mappings por status;
- validar odds por mercado/tipo/bookmaker;
- detectar duplicatas por grain;
- detectar odds invalidas;
- registrar inconsistencias.

#### write_summary()

Responsavel por:

- emitir resumo final em log/console/arquivo, conforme padrao futuro aprovado;
- consolidar contagens;
- listar falhas por linha;
- registrar `source_hash`, `source_file`, inicio e fim da execucao.

---

## 4. Comandos Previstos

Comandos previstos para future implementation:

```bash
python football_data_importer.py --csv <path> --season 2024-2025 --competition EPL --dry-run
```

```bash
python football_data_importer.py --csv <path> --season 2024-2025 --competition EPL --stage-only
```

```bash
python football_data_importer.py --csv <path> --season 2024-2025 --competition EPL --map-only
```

```bash
python football_data_importer.py --csv <path> --season 2024-2025 --competition EPL --odds-only
```

```bash
python football_data_importer.py --csv <path> --season 2024-2025 --competition EPL --all
```

### 4.1 dry-run

Executa validacoes e simulacoes sem escrita no banco.

### 4.2 stage-only

Executa apenas registro de CSV e staging, se aprovado na future implementation.

### 4.3 map-only

Executa apenas mapping para linhas ja presentes em staging, se aprovado na future implementation.

### 4.4 odds-only

Executa apenas promocao de odds para linhas ja mapeadas com confianca, se aprovado na future implementation.

### 4.5 all

Executa fluxo completo:

```text
register_csv_file
-> import_staging_rows
-> build_match_mapping
-> import_odds
-> validate_import
-> write_summary
```

---

## 5. Fluxo de Importacao

Fluxo futuro recomendado:

1. Ler CSV bruto.
2. Calcular `source_hash`.
3. Registrar CSV em `football_data_csv_files`.
4. Inserir/preservar linhas em `football_data_staging_rows`.
5. Aplicar dicionario de nomes de times.
6. Parear com SofaScore/`matches_master`.
7. Registrar mapping em `football_data_match_mapping`.
8. Extrair odds por mercado.
9. Inserir odds definitivas em `football_data_odds`.
10. Executar validacoes.
11. Gerar resumo.

### 5.1 Leitura do CSV

O importer futuro deve receber o CSV local por argumento.

Nao deve baixar CSV automaticamente.

Nao deve sobrescrever CSV bruto.

### 5.2 Calculo de source_hash

`source_hash` deve ser calculado sobre o conteudo real do arquivo.

Esse hash identifica versao de conteudo, nao apenas caminho ou nome do arquivo.

### 5.3 Staging

Staging deve preservar linha original completa em `raw_row_json`.

Grain de staging:

```text
source_hash + row_number
```

### 5.4 Mapping

Mapping deve ser explicito.

Nenhuma linha deve ser promovida para odds definitivas sem `sofascore_event_id` confiavel.

### 5.5 Extracao de Odds

Mercados iniciais esperados:

- `match_odds_1x2`;
- `over_under_2_5`;
- `asian_handicap`.

Tipos iniciais esperados:

- `closing`;
- `opening_like`;
- `average`;
- `maximum`.

O importer futuro deve preservar a semantica original da coluna Football-Data.

---

## 6. Idempotencia

O importer futuro deve ser idempotente.

Reexecucao com o mesmo CSV nao pode duplicar registros.

Novo `source_hash` deve criar nova versao.

### 6.1 CSV File

Estrategia futura:

- `ON CONFLICT(source_hash) DO UPDATE` ou `DO NOTHING`, conforme decisao CTO.

A decisao deve considerar se metadados como `registered_at`, `notes` ou `row_count` podem ser atualizados em reexecucao.

### 6.2 Staging

Estrategia futura:

- `ON CONFLICT(source_hash, row_number) DO UPDATE`.

Objetivo:

- preservar linha original;
- permitir reprocessamento seguro;
- corrigir metadados se necessario;
- nao duplicar staging.

### 6.3 Mapping

Estrategia futura:

- `ON CONFLICT(source_hash, row_number) DO UPDATE`.

Objetivo:

- permitir atualizar mapping_status;
- registrar resolucao de ambiguidade;
- preservar historico por versao de CSV.

### 6.4 Odds

Estrategia futura:

- `ON CONFLICT(grain aprovado) DO UPDATE`.

Grain aprovado depende do desenho fisico CTO.

Grain conceitual:

```text
sofascore_event_id + market + selection + odds_type + bookmaker_or_aggregator + source_hash
```

Para Asian Handicap:

```text
sofascore_event_id + market + selection + handicap_line + odds_type + bookmaker_or_aggregator + source_hash
```

A future implementation deve tratar `handicap_line NULL` de forma compativel com PostgreSQL.

---

## 7. Dry-run

Dry-run deve executar sem escrita no banco.

Dry-run deve:

- calcular `source_hash`;
- contar linhas;
- validar colunas;
- simular mapping;
- estimar odds extraidas;
- identificar colunas inesperadas;
- identificar colunas obrigatorias ausentes;
- reportar possiveis conflitos de nome/placar;
- reportar potencial de odds por mercado/tipo;
- gerar resumo sem persistencia.

Dry-run nao deve:

- inserir CSV file;
- inserir staging;
- inserir mapping;
- inserir odds;
- alterar PostgreSQL;
- criar arquivos derivados obrigatorios;
- criar features/datasets.

---

## 8. Rastreabilidade

Todo registro final futuro deve preservar:

- `source_file`;
- `source_url`;
- `source_hash`;
- `row_number`;
- `source_column`;
- `source_column_semantics`;
- `imported_at`.

### 8.1 source_column

`source_column` deve conter o nome exato da coluna Football-Data usada para gerar a odd.

### 8.2 source_column_semantics

`source_column_semantics` deve registrar a interpretacao aplicada.

Regras:

- colunas com `C` podem ser candidatas a closing odds conforme documentacao da fonte;
- colunas sem `C` nao devem ser assumidas automaticamente como opening odds;
- colunas sem `C` so podem ser `opening_like` com documentacao/validacao;
- semantica original deve ser preservada.

### 8.3 Linha Original

Cada odd deve ser rastreavel ate:

```text
football_data_odds
-> football_data_match_mapping
-> football_data_staging_rows
-> football_data_csv_files
-> CSV bruto
```

---

## 9. Versionamento de CSV

CSV bruto nunca deve ser sobrescrito.

`source_hash` identifica versao.

Reprocessamento de versao antiga deve ser possivel.

Mudanca no mesmo arquivo publico deve gerar novo `source_hash`.

O importer futuro deve registrar:

- `source_file`;
- `source_url`;
- `source_hash`;
- `season`;
- `competition_code`;
- `row_count`;
- momento de registro/processamento.

---

## 10. Tratamento de Erros

### 10.1 Erros por Linha

Erros por linha nao devem interromper lote inteiro.

A linha com erro deve ser registrada com status ou log claro.

### 10.2 Linhas sem Mapping

Linhas sem mapping confiavel ficam em staging/mapping com status apropriado.

Nao devem ser promovidas para odds definitivas.

### 10.3 Odds Ausentes

Odds ausentes nao devem ser inferidas.

Ausencia deve ser registrada como ausencia, nao como zero.

### 10.4 Colunas Inesperadas

Colunas inesperadas devem ser logadas.

Nao devem interromper importacao se colunas obrigatorias estiverem presentes e a linha puder ser preservada em staging.

### 10.5 Colunas Obrigatorias Ausentes

Colunas obrigatorias ausentes devem falhar validacao estrutural.

Dry-run deve detectar isso antes de qualquer escrita.

### 10.6 Conflito de Placar

Conflito de placar deve bloquear promocao para odds definitivas.

A linha deve ser registrada como `conflict` ou status equivalente.

### 10.7 Ambiguidade

Ambiguidade deve bloquear promocao para odds definitivas daquela linha.

A linha deve permanecer auditavel para revisao manual.

---

## 11. Validacoes Pos-Importacao

Validacoes obrigatorias futuras:

- total de linhas CSV vs staging;
- total de mappings;
- mappings por status: `mapped`, `unmapped`, `ambiguous`, `conflict`, `cancelled_or_postponed`;
- total de partidas pareadas;
- total de odds por mercado;
- total de odds por `odds_type`;
- total de odds por `bookmaker_or_aggregator`;
- duplicatas por grain;
- `odds_value <= 0`;
- registros orfaos;
- `source_hash` consistente;
- 380/380 partidas esperadas para EPL 2024/25, se aplicavel.

### 11.1 Validacao de Cobertura EPL 2024/25

Para EPL 2024/25, o resultado esperado do mapping exploratorio e:

- Football-Data: 380 partidas;
- SofaScore importaveis: 380 partidas;
- pareadas: 380;
- taxa de pareamento: 100%;
- conflitos de placar: 0;
- ambiguidades relevantes: 0.

Qualquer divergencia futura deve ser reportada.

### 11.2 Validacao de Odds

A validacao de odds deve reportar, no minimo:

- mercado 1X2;
- Over/Under 2.5;
- Asian Handicap;
- closing;
- opening_like;
- average;
- maximum;
- bookmakers/agregadores;
- colunas ignoradas;
- odds invalidas.

---

## 12. Logs e Resumo Final

Resumo final futuro deve conter:

- `processed_rows`;
- `staged_rows`;
- `mapped_rows`;
- `unmapped_rows`;
- `odds_inserted`;
- `odds_updated`;
- `failed_rows`;
- `source_hash`;
- `source_file`;
- `started_at`;
- `finished_at`.

Logs devem informar:

- inicio e fim da execucao;
- arquivo processado;
- hash calculado;
- colunas encontradas;
- linhas processadas;
- status de mapping;
- odds extraidas por mercado;
- erros por linha;
- resumo final.

---

## 13. Restricoes

Future implementation nao deve:

- criar features;
- criar datasets;
- modelar;
- executar baseline;
- baixar CSV;
- alterar crawlers;
- alterar SofaScore;
- alterar dados brutos;
- alterar schema sem aprovacao CTO;
- criar `create_engine` proprio;
- hardcodar credenciais;
- inferir odds ausentes;
- promover linha sem mapping confiavel;
- tratar Football-Data como fonte live/in-game.

---

## 14. Criterios de Aceite

Future implementation sera aceitavel se:

- usar `config.database.engine`;
- seguir staging-first;
- ser idempotente;
- possuir dry-run sem escrita;
- preservar rastreabilidade;
- registrar erros por linha;
- nao duplicar registros;
- nao promover linha sem mapping confiavel;
- nao inferir odds ausentes;
- nao criar features;
- nao criar datasets;
- nao modelar;
- nao executar baseline;
- nao baixar CSV;
- nao alterar crawlers;
- nao alterar SofaScore;
- validar 380/380 partidas esperadas para EPL 2024/25 quando aplicavel;
- gerar logs claros e resumo final.

---

## 15. Status da Especificacao

Status:

**PRONTA PARA FUTURA IMPLEMENTACAO PELO CODEX APOS APROVACAO CTO**

Esta especificacao nao cria importer, codigo, migration, schema, features, dataset, modelagem, importacao ou alteracao de PostgreSQL.
