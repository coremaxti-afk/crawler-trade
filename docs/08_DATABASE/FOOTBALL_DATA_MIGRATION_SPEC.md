# FOOTBALL-DATA MIGRATION SPEC

## 1. Objetivo

Definir a especificacao futura de migration Football-Data para o projeto LateGoalResearch, sem criar migration executavel.

Este documento e exclusivamente documental. Ele nao implementa migration, nao altera PostgreSQL, nao cria schema real, nao cria importer, nao cria features, nao cria datasets, nao modela e nao executa importacao.

Objetivo da futura migration, se aprovada pelo CTO:

- criar estruturas de armazenamento Football-Data;
- preservar arquitetura staging-first;
- manter rastreabilidade por CSV e linha original;
- permitir importer futuro idempotente;
- evitar impacto em tabelas SofaScore existentes.

---

## 2. Escopo

Incluido:

- dependencia conceitual das tabelas futuras;
- ordem recomendada de criacao;
- estrategia de rollback;
- validacoes pos-migration;
- cuidados com PostgreSQL;
- criterios de aceite para uma future implementation.

Excluido:

- SQL executavel;
- migration real;
- alteracao de schema;
- alteracao de PostgreSQL;
- importer;
- carga de dados;
- features;
- datasets;
- modelagem;
- baseline;
- backtesting.

---

## 3. Dependencias

A future implementation de migration Football-Data depende de:

- PostgreSQL operacional.
- SQLAlchemy/config.database operacional.
- `matches_master` existente.
- `match_mapping` ou equivalente existente, quando aplicavel ao contrato oficial do projeto.
- `docs/08_DATABASE/FOOTBALL_DATA_SCHEMA_SPEC.md` aprovado.
- `docs/08_DATABASE/FOOTBALL_DATA_STORAGE_IMPORT_SPEC.md` aprovado.
- Decisao CTO explicita sobre FKs fisicas para tabelas oficiais.

A migration futura nao deve assumir que dados Football-Data ja foram importados.

A migration futura nao deve baixar CSV, ler CSV, popular staging, gerar mapping ou inserir odds.

---

## 4. Ordem de Criacao

Ordem obrigatoria recomendada:

1. `football_data_csv_files`
2. `football_data_staging_rows`
3. `football_data_match_mapping`
4. `football_data_odds`
5. indices
6. constraints unicas
7. FKs fisicas somente se aprovadas pelo CTO

### 4.1 football_data_csv_files

Criar `football_data_csv_files` primeiro porque a tabela de staging depende dela.

Funcao futura:

- registrar versoes de CSV Football-Data;
- preservar `source_hash`;
- controlar versionamento logico;
- permitir reprocessamento auditavel.

### 4.2 football_data_staging_rows

Criar `football_data_staging_rows` depois de `football_data_csv_files`.

Motivo:

- cada linha de staging deve apontar para a versao do CSV;
- grain conceitual: `source_hash + row_number`;
- `raw_row_json` deve preservar todas as colunas originais.

### 4.3 football_data_match_mapping

Criar `football_data_match_mapping` depois de staging.

Motivo:

- mapping depende de linha original preservada;
- mapping deve registrar `source_hash`, `row_number`, `sofascore_event_id` e `match_id`;
- linhas sem mapping confiavel devem permanecer rastreaveis.

### 4.4 football_data_odds

Criar `football_data_odds` depois de staging e mapping.

Motivo:

- odds definitivas dependem da linha original;
- odds definitivas dependem de mapping confiavel;
- nenhuma odd deve ser promovida sem vinculo explicito a `sofascore_event_id`.

### 4.5 Indices e Constraints

Indices e constraints unicas devem ser criados apos as tabelas.

A ordem fisica exata deve ser definida na future implementation, respeitando:

- dependencies entre tabelas;
- comportamento de unique constraints com `NULL`;
- custo de criacao de indices;
- compatibilidade com ambiente local/dev.

### 4.6 FKs Fisicas

FKs fisicas para `matches_master` ou tabela oficial de partidas devem ser criadas somente se aprovadas pelo CTO.

Risco:

- FKs fisicas podem aumentar integridade referencial;
- mas tambem podem dificultar staging, reprocessamento e tratamento de linhas sem mapping confiavel.

Recomendacao:

- FKs internas Football-Data podem ser avaliadas primeiro;
- FKs para tabelas oficiais devem ser decisao explicita de arquitetura.

---

## 5. Estrategia de Rollback

Rollback futuro deve remover estruturas na ordem inversa de dependencia:

1. `football_data_odds`
2. `football_data_match_mapping`
3. `football_data_staging_rows`
4. `football_data_csv_files`

### 5.1 Ambiente Local/Dev

Rollback deve ser seguro em ambiente local/dev quando nao houver dados reais relevantes.

Mesmo em ambiente local/dev, o rollback nao deve apagar:

- CSV bruto;
- arquivos versionados;
- dados SofaScore;
- dados H8;
- datasets ou reports ja existentes.

### 5.2 Ambiente com Dados Reais

Em ambiente com dados reais, rollback deve exigir confirmacao explicita.

Antes do rollback, deve-se registrar:

- tabelas afetadas;
- contagem de registros por tabela;
- source_hashes existentes;
- risco de perda de staging/mapping/odds.

### 5.3 Regras de Preservacao

Rollback nao deve apagar CSV bruto.

Rollback nao deve apagar arquivos versionados.

Rollback nao deve apagar dados SofaScore.

Rollback nao deve alterar `matches_master`, `match_statistics`, `match_incidents`, `match_graph`, `match_shotmap` ou qualquer tabela nao Football-Data.

---

## 6. Validacoes Pos-Migration

A future implementation deve executar validacoes estruturais apos migration.

Validacoes obrigatorias:

- verificar existencia das 4 tabelas;
- verificar constraints unicas;
- verificar indices;
- verificar colunas obrigatorias;
- verificar tipo JSONB em `raw_row_json`;
- verificar tipo numerico/decimal adequado para `odds_value`;
- verificar que `source_hash` comporta SHA-256;
- verificar que nenhuma tabela foi populada pela migration;
- verificar que a migration nao criou features;
- verificar que a migration nao criou datasets;
- verificar que a migration nao alterou tabelas SofaScore;
- verificar que importers existentes continuam intactos.

### 6.1 Tabelas Esperadas

Tabelas futuras esperadas:

- `football_data_csv_files`;
- `football_data_staging_rows`;
- `football_data_match_mapping`;
- `football_data_odds`.

### 6.2 Constraints Esperadas

Constraints conceituais esperadas:

- `football_data_csv_files`: `UNIQUE(source_hash)`;
- `football_data_staging_rows`: `UNIQUE(source_hash, row_number)`;
- `football_data_match_mapping`: `UNIQUE(source_hash, row_number)`;
- `football_data_odds`: unique por grain aprovado.

Observacao:

- O desenho fisico de unique para `football_data_odds` deve considerar `handicap_line NULL`.

### 6.3 Resultado Esperado

A migration futura deve criar apenas estrutura.

Resultado pos-migration esperado:

- 4 tabelas criadas;
- 0 registros importados;
- 0 features criadas;
- 0 datasets criados;
- 0 alteracoes em tabelas SofaScore;
- 0 execucoes de importer.

---

## 7. Cuidados com PostgreSQL

### 7.1 Unique com handicap_line NULL

PostgreSQL trata `NULL` em unique constraints de forma especial.

Como `handicap_line` participa do grain para Asian Handicap, mas pode ser nulo para mercados 1X2 e Over/Under, o desenho fisico deve ser decidido com cuidado.

Opcoes futuras a avaliar pelo CTO:

- unique parcial por mercado;
- coluna normalizada auxiliar para grain;
- uso de expressao controlada;
- separacao fisica por mercado, se aprovado;
- outra abordagem compativel com a arquitetura do projeto.

Esta especificacao nao escolhe implementacao fisica.

### 7.2 JSONB para raw_row_json

`raw_row_json` deve usar JSONB para preservar todas as colunas originais do CSV.

Esse campo nao deve substituir colunas normalizadas minimas usadas para validacao e mapping.

### 7.3 Numeric/Decimal para odds_value

`odds_value` deve usar tipo numerico/decimal adequado para odds.

A future implementation deve evitar perda de precisao por tipo inadequado.

### 7.4 source_hash

`source_hash` deve ter tamanho compativel com SHA-256.

A future implementation deve definir tamanho fisico suficiente e consistente entre as quatro tabelas.

### 7.5 Timestamps

Timestamps devem usar timezone se o padrao do projeto permitir.

Campos como `downloaded_at`, `registered_at`, `created_at`, `mapped_at` e `imported_at` devem seguir convencao unica.

### 7.6 Enums e Flexibilidade

Nao criar enum rigido cedo demais se houver risco de mudanca de layout.

Campos como `market`, `selection`, `odds_type`, `mapping_status` e `bookmaker_or_aggregator` devem equilibrar:

- integridade;
- flexibilidade de fonte;
- facilidade de reprocessamento;
- evolucao entre temporadas.

---

## 8. Criterios de Aceite

A future implementation de migration sera aceitavel se:

- criar apenas estrutura;
- nao importar dados;
- nao criar features;
- nao criar datasets;
- nao alterar tabelas SofaScore;
- nao quebrar importers existentes;
- documentar rollback;
- permitir validacao pos-migration com consultas simples;
- respeitar staging-first;
- preservar rastreabilidade por `source_hash` e `row_number`;
- nao criar FKs fisicas para tabelas oficiais sem aprovacao CTO;
- tratar explicitamente o risco de `handicap_line NULL`.

---

## 9. Status da Especificacao

Status:

**PRONTA PARA FUTURA IMPLEMENTACAO PELO CODEX APOS APROVACAO CTO**

Esta especificacao nao cria schema, migration, importer, features, dataset, modelagem, SQL executavel ou alteracao de PostgreSQL.
