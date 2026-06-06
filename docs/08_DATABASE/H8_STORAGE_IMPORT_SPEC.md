# H8 STORAGE IMPORT SPEC — Graph / Momentum

Status: PRONTA PARA REVISÃO CTO

## Objetivo

Definir a especificação formal de armazenamento e importação futura dos artefatos H8 da fonte SofaScore:

- `graph.json`
- `shotmap.json`

Este documento é uma especificação técnica para revisão CTO.

Não autoriza implementação, migration, alteração de schema, importer, feature engineering, dataset, baseline ou modelagem.

---

## Escopo

Incluído nesta especificação:

- desenho lógico das tabelas H8;
- grain recomendado;
- campos mínimos;
- constraints mínimas;
- política para exceção conhecida;
- estratégia de importer futuro;
- idempotência;
- rastreabilidade raw;
- validações pós-importação;
- riscos de schema.

Fora do escopo:

- implementação de código;
- criação de migration;
- alteração de schema;
- criação de importer;
- criação de features H8;
- dataset analítico;
- baseline;
- modelagem;
- alteração de crawlers;
- alteração de dados brutos.

---

## Estado Atual H8

Coleta e auditoria H8 concluídas no escopo de Data Acquisition.

### Graph

- Partidas importáveis: 380.
- `graph.json` válidos: 379.
- `graph.json` faltantes totais na base importável: 1.
- `graph.json` faltantes excluindo exceção conhecida: 0.
- `graph.json` inválidos: 0.
- `graphPoints` mínimo: 91.
- `graphPoints` máximo: 92.
- Média de `graphPoints`: 91,98.

Exceção conhecida:

- `event_id`: `12437015`
- Partida: Crystal Palace x Liverpool FC
- Motivo: HTTP 404 no endpoint `/graph`

### Shotmap

- Partidas importáveis: 380.
- `shotmap.json` válidos: 380.
- Faltantes: 0.
- Inválidos: 0.
- Total de finalizações: 9.883.
- Média de finalizações por partida: 26,01.

---

## Decisão CTO Vigente

A exceção `12437015` deve seguir a Opção 2:

- manter a partida para features baseadas em `shotmap`, `incidents` e `statistics`;
- marcar `graph` como exceção conhecida;
- excluir apenas de features/datasets que exijam graph completo.

---

# 1. Tabela `match_graph`

## Objetivo

Armazenar os pontos de momentum do `graph.json` em formato granular e auditável.

## Grain

Uma linha por ponto do graph por partida.

Grain recomendado:

```text
sofascore_event_id + point_index
```

## Campos Mínimos

| Campo | Tipo sugerido | Obrigatório | Descrição |
|---|---|---:|---|
| `id` | bigserial / identity | sim | Chave técnica interna. |
| `match_id` | bigint / integer | sim | FK lógica para `matches_master.match_id`, se disponível no schema atual. |
| `sofascore_event_id` | bigint | sim | ID da partida no SofaScore. |
| `point_index` | integer | sim | Índice ordinal do ponto dentro de `graphPoints`, iniciado em 0 ou 1 conforme decisão de implementação. |
| `minute` | integer | sim | Minuto informado no payload. |
| `value` | numeric / integer | sim | Valor bruto de momentum informado no payload. |
| `raw_file_path` | text | sim | Caminho do arquivo raw usado na importação. |
| `raw_payload_hash` | text | sim | Hash do payload bruto do arquivo no momento da importação. |
| `imported_at` | timestamp with time zone | sim | Timestamp de importação. |
| `updated_at` | timestamp with time zone | sim | Timestamp da última atualização via upsert. |

## Constraints Mínimas

Recomendadas para revisão CTO:

```sql
UNIQUE (sofascore_event_id, point_index)
```

Constraints adicionais recomendadas:

```sql
CHECK (point_index >= 0)
CHECK (minute IS NOT NULL)
CHECK (value IS NOT NULL)
```

FK recomendada, se compatível com o schema atual:

```sql
FOREIGN KEY (match_id) REFERENCES matches_master(match_id)
```

## Observações

- Não calcular features nesta tabela.
- Não inverter sinal de momentum na importação.
- Não normalizar `value` na importação.
- Preservar granularidade original.
- Se o mesmo arquivo for reimportado, o upsert deve atualizar `minute`, `value`, `raw_file_path`, `raw_payload_hash` e `updated_at` sem duplicar linhas.

---

# 2. Tabela `match_shotmap`

## Objetivo

Armazenar finalizações do `shotmap.json` em formato granular, preservando dados temporais, espaciais e metadados mínimos necessários para auditoria.

## Grain

Uma linha por finalização por partida.

Grain recomendado:

```text
sofascore_event_id + shot_index
```

`shot_index` deve representar a posição ordinal da finalização na lista bruta do payload.

## Campos Mínimos

| Campo | Tipo sugerido | Obrigatório | Descrição |
|---|---|---:|---|
| `id` | bigserial / identity | sim | Chave técnica interna. |
| `match_id` | bigint / integer | sim | FK lógica para `matches_master.match_id`, se disponível no schema atual. |
| `sofascore_event_id` | bigint | sim | ID da partida no SofaScore. |
| `shot_index` | integer | sim | Índice ordinal da finalização dentro do payload. |
| `minute` | integer | não | Minuto da finalização, quando disponível. |
| `added_time` | integer | não | Acréscimo, quando disponível. |
| `time_seconds` | integer | não | Tempo em segundos, quando disponível. |
| `team_id` | bigint | não | ID do time no SofaScore, quando disponível. |
| `team_name` | text | não | Nome do time, quando disponível. |
| `player_id` | bigint | não | ID do jogador no SofaScore, quando disponível. |
| `player_name` | text | não | Nome do jogador, quando disponível. |
| `shot_type` | text | não | Tipo da finalização, quando disponível. |
| `situation` | text | não | Situação/contexto da finalização, quando disponível. |
| `body_part` | text | não | Parte do corpo, quando disponível. |
| `goal_mouth_location` | text | não | Localização na boca do gol, quando disponível. |
| `xg` | numeric | não | Expected Goals bruto do SofaScore, quando disponível. |
| `xgot` | numeric | não | Expected Goals on Target bruto, quando disponível. |
| `is_goal` | boolean | não | Indicador derivado somente do próprio shot item, se existir campo inequívoco no payload. |
| `player_coordinates` | jsonb | não | Coordenadas brutas do jogador/finalização. |
| `goal_mouth_coordinates` | jsonb | não | Coordenadas brutas da boca do gol. |
| `draw` | jsonb | não | Objeto bruto `draw`, quando disponível. |
| `raw_shot` | jsonb | sim | Objeto bruto completo da finalização. |
| `raw_file_path` | text | sim | Caminho do arquivo raw usado na importação. |
| `raw_payload_hash` | text | sim | Hash do payload bruto do arquivo no momento da importação. |
| `imported_at` | timestamp with time zone | sim | Timestamp de importação. |
| `updated_at` | timestamp with time zone | sim | Timestamp da última atualização via upsert. |

## Constraints Mínimas

Recomendadas para revisão CTO:

```sql
UNIQUE (sofascore_event_id, shot_index)
```

Constraints adicionais recomendadas:

```sql
CHECK (shot_index >= 0)
```

FK recomendada, se compatível com o schema atual:

```sql
FOREIGN KEY (match_id) REFERENCES matches_master(match_id)
```

## Observações

- `raw_shot` deve preservar o objeto completo de cada finalização.
- Campos estruturados como `xg`, `xgot`, `minute` e coordenadas devem ser extraídos apenas para facilitar consulta e validação.
- Não criar features nesta tabela.
- Não calcular janelas temporais nesta tabela.
- Não inferir valores ausentes a partir de outros arquivos.
- Não usar estatísticas finais da partida para preencher shotmap.

---

# 3. Tabela `match_source_status`

## Objetivo

Registrar o status por partida e por fonte raw H8, permitindo rastrear cobertura, exceções conhecidas, arquivos faltantes, hashes e disponibilidade para importação futura.

## Grain

Uma linha por partida por fonte.

Grain recomendado:

```text
sofascore_event_id + source_name
```

Valores iniciais de `source_name`:

- `graph`
- `shotmap`

## Campos Mínimos

| Campo | Tipo sugerido | Obrigatório | Descrição |
|---|---|---:|---|
| `id` | bigserial / identity | sim | Chave técnica interna. |
| `match_id` | bigint / integer | sim | FK lógica para `matches_master.match_id`, se disponível no schema atual. |
| `sofascore_event_id` | bigint | sim | ID da partida no SofaScore. |
| `source_name` | text | sim | Nome da fonte: `graph` ou `shotmap`. |
| `status` | text | sim | Status operacional da fonte para a partida. |
| `raw_file_path` | text | não | Caminho do arquivo raw, se existir. |
| `raw_payload_hash` | text | não | Hash do payload bruto, se existir. |
| `records_count` | integer | não | Quantidade de registros granulares esperados/importados. |
| `known_missing_reason` | text | não | Motivo de ausência conhecida, quando aplicável. |
| `last_checked_at` | timestamp with time zone | sim | Timestamp da última verificação/importação. |
| `imported_at` | timestamp with time zone | não | Timestamp da importação, quando aplicável. |
| `updated_at` | timestamp with time zone | sim | Timestamp da última atualização via upsert. |

## Status Permitidos

Valores recomendados para `status`:

- `available`
- `imported`
- `missing`
- `known_missing`
- `invalid_raw`
- `skipped`

## Constraints Mínimas

```sql
UNIQUE (sofascore_event_id, source_name)
CHECK (source_name IN ('graph', 'shotmap'))
CHECK (status IN ('available', 'imported', 'missing', 'known_missing', 'invalid_raw', 'skipped'))
```

FK recomendada, se compatível com o schema atual:

```sql
FOREIGN KEY (match_id) REFERENCES matches_master(match_id)
```

---

# 4. Política para `event_id=12437015`

## Contexto

A partida `12437015`, Crystal Palace x Liverpool FC, retorna HTTP 404 no endpoint:

```text
https://www.sofascore.com/api/v1/event/12437015/graph
```

A ausência de `graph.json` deve ser tratada como exceção técnica conhecida, não como falha aberta de coleta.

## Política Recomendada

Registrar em `match_source_status`:

| Campo | Valor |
|---|---|
| `sofascore_event_id` | `12437015` |
| `source_name` | `graph` |
| `status` | `known_missing` |
| `known_missing_reason` | `graph.json HTTP 404 confirmed` |
| `raw_file_path` | `NULL` |
| `raw_payload_hash` | `NULL` |
| `records_count` | `0` |

Regras:

- A partida permanece válida para `shotmap`, `incidents` e `statistics`.
- A partida deve ser excluída apenas de features/datasets que exijam graph completo.
- Não tentar contornos agressivos para obter esse graph.
- Não criar payload sintético para substituir `graph.json`.
- Não imputar graph sem aprovação metodológica explícita do Quant Research e CTO.

---

# 5. Estratégia Futura do `h8_importer.py`

## Local Sugerido

```text
LateGoalResearch/Crawler/Sofascore/h8_importer.py
```

## Objetivo

Importar `graph.json` e `shotmap.json` brutos para PostgreSQL de forma idempotente, auditável e retomável.

## CLI Recomendada

```bash
python LateGoalResearch/Crawler/Sofascore/h8_importer.py --graph
python LateGoalResearch/Crawler/Sofascore/h8_importer.py --shotmap
python LateGoalResearch/Crawler/Sofascore/h8_importer.py --all
python LateGoalResearch/Crawler/Sofascore/h8_importer.py --all --dry-run
```

Parâmetros mínimos:

- `--graph`: importar apenas `graph.json`.
- `--shotmap`: importar apenas `shotmap.json`.
- `--all`: importar graph, shotmap e status das fontes.
- `--dry-run`: validar arquivos e imprimir plano sem escrever no banco.

## Conexão

O importer futuro deve usar exclusivamente:

```python
from config.database import engine
```

Não criar outro `create_engine`.

## Funções Recomendadas

### `import_graph()`

Responsabilidades:

- localizar `graph.json` nas pastas de partidas;
- validar payload mínimo;
- resolver `match_id` a partir de `matches_master`;
- calcular `raw_payload_hash`;
- inserir/upsert uma linha por `graphPoint` em `match_graph`;
- registrar fonte em `match_source_status`;
- tratar `12437015` como `known_missing`.

### `import_shotmap()`

Responsabilidades:

- localizar `shotmap.json` nas pastas de partidas;
- validar payload mínimo;
- resolver `match_id` a partir de `matches_master`;
- calcular `raw_payload_hash`;
- inserir/upsert uma linha por finalização em `match_shotmap`;
- preservar o objeto bruto da finalização em `raw_shot`;
- registrar fonte em `match_source_status`.

### `import_source_status()`

Responsabilidades:

- registrar status por partida/fonte;
- marcar arquivos presentes e válidos como `available` ou `imported`;
- marcar ausências inesperadas como `missing`;
- marcar `12437015` + `graph` como `known_missing`;
- registrar `raw_file_path`, `raw_payload_hash`, `records_count` e timestamps.

---

# 6. Idempotência

## Regra Geral

O importer futuro deve poder rodar repetidamente sem duplicar registros.

Estratégia recomendada:

```sql
INSERT ... ON CONFLICT DO UPDATE
```

Conflitos esperados:

- `match_graph`: `ON CONFLICT (sofascore_event_id, point_index)`
- `match_shotmap`: `ON CONFLICT (sofascore_event_id, shot_index)`
- `match_source_status`: `ON CONFLICT (sofascore_event_id, source_name)`

Campos atualizáveis no upsert:

- valores estruturados extraídos do payload;
- `raw_file_path`;
- `raw_payload_hash`;
- `records_count`;
- `status`;
- `known_missing_reason`;
- `updated_at`.

O importer não deve:

- apagar registros sem aprovação;
- truncar tabelas;
- sobrescrever dados raw;
- criar payload sintético;
- alterar JSON bruto.

---

# 7. Rastreabilidade Raw

Toda linha importada deve permitir rastrear o arquivo que originou o registro.

Campos obrigatórios para rastreabilidade:

- `raw_file_path`
- `raw_payload_hash`
- `imported_at`
- `updated_at`

Hash recomendado:

```text
SHA-256 do conteúdo bruto do arquivo JSON
```

Regras:

- O hash deve ser calculado sobre o arquivo bruto inteiro, antes de qualquer parsing transformacional.
- O caminho deve apontar para a localização local padronizada em `data/raw/sofascore/premier_league_61627/matches/{event_id}/`.
- Se o arquivo mudar, o próximo upsert deve atualizar `raw_payload_hash` e `updated_at`.

---

# 8. Validações Pós-Importação

## Validações de Cobertura

Consultas esperadas após importação futura:

- total de partidas em `matches_master`;
- total de partidas com status `graph=imported`;
- total de partidas com status `graph=known_missing`;
- total de partidas com status `shotmap=imported`;
- partidas com fonte `missing` inesperada;
- partidas com fonte `invalid_raw`.

Expectativa inicial:

- `graph=imported`: 379.
- `graph=known_missing`: 1 (`12437015`).
- `shotmap=imported`: 380.

## Validações de Integridade

- Nenhum `match_graph.match_id` órfão.
- Nenhum `match_shotmap.match_id` órfão.
- Nenhum `match_source_status.match_id` órfão.
- Nenhuma duplicidade por `(sofascore_event_id, point_index)`.
- Nenhuma duplicidade por `(sofascore_event_id, shot_index)`.
- Nenhuma duplicidade por `(sofascore_event_id, source_name)`.

## Validações de Qualidade Graph

- `graphPoints` por partida entre 91 e 92, exceto exceções futuras documentadas.
- `minute` não nulo.
- `value` não nulo.
- `point_index` sequencial por partida.

## Validações de Qualidade Shotmap

- total esperado aproximado: 9.883 finalizações.
- nenhuma partida importável sem status `shotmap=imported`.
- `shot_index` sequencial por partida.
- `raw_shot` não nulo.
- `raw_payload_hash` não nulo.

---

# 9. Riscos de Schema

## Risco 1 — Tabela `match_graph` já existir

O projeto já possui tabela `match_graph` criada anteriormente. Antes de qualquer migration, o CTO/Data Engineer deve verificar:

- colunas existentes;
- constraints existentes;
- compatibilidade com o grain proposto;
- necessidade real de alterar ou criar nova tabela.

## Risco 2 — Granularidade

Se `match_graph` existente tiver grain diferente, não adaptar importer sem decisão CTO.

## Risco 3 — Tipos de Dados

Campos `xg`, `xgot`, coordenadas e objetos aninhados podem variar por payload.

Recomendação:

- usar `jsonb` para objetos brutos/aninhados;
- usar campos estruturados apenas para valores estáveis e claramente presentes.

## Risco 4 — Exceção `12437015`

A ausência de graph para `12437015` deve ser explicitamente modelada no status da fonte para evitar falsa falha de importação.

## Risco 5 — Leakage Futuro

As tabelas H8 armazenam dados brutos da partida inteira. Feature builders futuros devem respeitar cutoff temporal e não usar eventos após cutoff.

Esta especificação não autoriza features.

---

# 10. Status Final

Status: PRONTA PARA REVISÃO CTO.

Resumo:

- `match_graph` especificada.
- `match_shotmap` especificada.
- `match_source_status` especificada.
- Exceção `12437015` definida como `known_missing` para graph HTTP 404.
- Estratégia futura de `h8_importer.py` definida.
- Idempotência definida com `INSERT ... ON CONFLICT DO UPDATE`.
- Rastreabilidade definida com `raw_file_path` e `raw_payload_hash`.
- Validações pós-importação definidas.
- Riscos de schema documentados.

Próximo passo:

- CTO/Data Engineer revisar e aprovar, ajustar ou rejeitar a especificação antes de qualquer implementação.
