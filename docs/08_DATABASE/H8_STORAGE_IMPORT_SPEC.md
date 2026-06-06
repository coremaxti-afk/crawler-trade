# H8 STORAGE IMPORT SPEC — Graph / Momentum

Status: APROVADO COM AJUSTES CTO — PRONTO PARA PRÓXIMA DECISÃO PM/CTO.

---

## 1. Objetivo

Definir a especificação documental para armazenamento e importação futura dos artefatos H8 da fonte SofaScore:

- `graph.json`
- `shotmap.json`

A especificação descreve tabelas candidatas, grains, campos mínimos, constraints, política de exceção conhecida, estratégia futura de importer, idempotência, rastreabilidade raw, validações pós-importação e riscos de schema.

Este documento não implementa código nem altera o banco.

---

## 2. Escopo

Incluído neste documento:

- especificação de `match_graph`;
- especificação de `match_shotmap`;
- especificação de `match_source_status`;
- política para `event_id=12437015`;
- estratégia futura do importer H8;
- funções internas esperadas do importer futuro;
- regras de idempotência;
- rastreabilidade com `raw_file_path` e `raw_payload_hash`;
- validações pós-importação;
- riscos de schema.

Fora do escopo:

- código;
- migration;
- alteração de schema;
- criação de importer;
- criação de features;
- criação de dataset;
- baseline;
- modelagem;
- alteração de crawlers;
- alteração de dados brutos.

---

## 3. Estado Atual H8

A frente oficial atual é H8 — Graph / Momentum.

Coleta e auditoria H8 concluídas:

| Métrica | Valor |
|---|---:|
| Inventory total | 381 |
| Partidas importáveis | 380 |
| `graph.json` válidos | 379/380 |
| `graph.json` faltante conhecido | 1 |
| `shotmap.json` válidos | 380/380 |
| Total de finalizações `shotmap` | 9.883 |
| Média de finalizações por partida | 26,01 |

Exceção conhecida de graph:

| event_id | Partida | Problema |
|---:|---|---|
| 12437015 | Crystal Palace x Liverpool FC | HTTP 404 no endpoint `/graph` |

---

## 4. Decisão CTO Vigente

Veredito CTO: APROVADO COM AJUSTES.

Ajustes obrigatórios incorporados nesta especificação:

1. `match_graph` deve usar `momentum_value`, não `value`.
2. `momentum_value` representa o valor bruto de momentum do payload.
3. O sinal de `momentum_value` não deve ser normalizado, invertido ou transformado na importação.
4. `match_source_status` deve ter grain obrigatório:

```text
sofascore_event_id + source_name + artifact_name
```

5. `source_name` deve ser:

```text
sofascore
```

6. `artifact_name` deve ser:

```text
graph.json
shotmap.json
```

7. A exceção `12437015` deve ser registrada como `known_missing` para `graph.json`, com `http_status=404` e decisão operacional explícita.

---

## 5. Tabela `match_graph`

### Objetivo

Armazenar os pontos de momentum do `graph.json` em formato granular e auditável.

### Grain

Uma linha por ponto de momentum por partida.

Grain obrigatório:

```text
sofascore_event_id + point_index
```

### Campos Mínimos

| Campo | Tipo sugerido | Obrigatório | Descrição |
|---|---|---:|---|
| `sofascore_event_id` | bigint | sim | ID da partida no SofaScore. |
| `point_index` | integer | sim | Índice ordinal do item em `graphPoints`. |
| `minute` | integer | sim | Minuto informado no payload. |
| `momentum_value` | numeric | sim | Valor bruto de momentum do payload. |
| `source_name` | text | sim | Valor fixo esperado: `sofascore`. |
| `artifact_name` | text | sim | Valor fixo esperado: `graph.json`. |
| `raw_file_path` | text | sim | Caminho do arquivo raw usado na importação. |
| `raw_payload_hash` | text | sim | Hash do payload bruto do arquivo. |
| `imported_at` | timestamptz | sim | Timestamp da importação. |

Campos técnicos adicionais podem ser avaliados pelo CTO/Data Engineer, como `id`, `created_at` ou `updated_at`, mas não são exigidos por esta especificação documental.

### Constraint Obrigatória

```sql
UNIQUE (sofascore_event_id, point_index)
```

### Observações

- Não usar `match_graph.value`.
- Todas as referências ao valor de momentum devem usar `match_graph.momentum_value`.
- `momentum_value` é bruto, sem normalização, inversão ou transformação de sinal.
- Não usar `minute` como chave única, pois pode haver variações, acréscimos ou colisões futuras.
- Não calcular features dentro de `match_graph`.
- Não inferir dados ausentes.
- Não criar linha sintética para `event_id=12437015`.

---

## 6. Tabela `match_shotmap`

### Objetivo

Armazenar as finalizações do `shotmap.json` em formato granular e auditável, preservando dados temporais, espaciais e metadados mínimos relevantes.

### Grain

Uma linha por finalização por partida.

Grain obrigatório:

```text
sofascore_event_id + shot_index
```

`shot_index` representa o índice ordinal da finalização dentro do payload bruto.

### Campos Mínimos

| Campo | Tipo sugerido | Obrigatório | Descrição |
|---|---|---:|---|
| `sofascore_event_id` | bigint | sim | ID da partida no SofaScore. |
| `shot_index` | integer | sim | Índice ordinal da finalização no payload. |
| `minute` | integer | não | Minuto da finalização. |
| `added_time` | integer | não | Acréscimo da finalização, quando disponível. |
| `time_seconds` | integer | não | Tempo em segundos, quando disponível. |
| `team_id` | bigint | não | ID do time, quando disponível. |
| `team_name` | text | não | Nome do time, quando disponível. |
| `player_id` | bigint | não | ID do jogador, quando disponível. |
| `player_name` | text | não | Nome do jogador, quando disponível. |
| `shot_type` | text | não | Tipo da finalização. |
| `goal_mouth_location` | text | não | Localização na boca do gol. |
| `xg` | numeric | não | xG bruto do SofaScore. |
| `xgot` | numeric | não | xGOT bruto do SofaScore. |
| `player_coordinates_json` | jsonb | não | Coordenadas brutas do jogador/finalização. |
| `goal_mouth_coordinates_json` | jsonb | não | Coordenadas brutas da boca do gol. |
| `draw_json` | jsonb | não | Objeto bruto `draw`, quando disponível. |
| `source_name` | text | sim | Valor fixo esperado: `sofascore`. |
| `artifact_name` | text | sim | Valor fixo esperado: `shotmap.json`. |
| `raw_file_path` | text | sim | Caminho do arquivo raw usado na importação. |
| `raw_payload_hash` | text | sim | Hash do payload bruto do arquivo. |
| `imported_at` | timestamptz | sim | Timestamp da importação. |

Campos adicionais, como `raw_shot_json`, podem ser avaliados pelo CTO/Data Engineer se houver necessidade de preservar o item bruto completo por linha. Esta especificação mínima já preserva rastreabilidade via `raw_file_path` e `raw_payload_hash`.

### Constraint Obrigatória

```sql
UNIQUE (sofascore_event_id, shot_index)
```

### Observações

- Não misturar `shotmap` em `match_incidents`.
- Não normalizar excessivamente o shotmap nesta fase.
- Não criar features dentro de `match_shotmap`.
- Não calcular janelas temporais nessa tabela.
- Não preencher campos ausentes a partir de `statistics`, `incidents` ou outras fontes.
- Não usar `minute` como chave única.

---

## 7. Tabela `match_source_status`

### Objetivo

Registrar cobertura, exceções conhecidas e status por artefato bruto, permitindo auditoria de disponibilidade por partida e por fonte.

### Grain

Grain obrigatório:

```text
sofascore_event_id + source_name + artifact_name
```

### Valores Padronizados

`source_name`:

```text
sofascore
```

`artifact_name`:

```text
graph.json
shotmap.json
```

### Campos Mínimos

| Campo | Tipo sugerido | Obrigatório | Descrição |
|---|---|---:|---|
| `sofascore_event_id` | bigint | sim | ID da partida no SofaScore. |
| `source_name` | text | sim | Fonte do artefato. Valor esperado: `sofascore`. |
| `artifact_name` | text | sim | Nome do artefato bruto: `graph.json` ou `shotmap.json`. |
| `status` | text | sim | Status do artefato. |
| `http_status` | integer | não | Código HTTP associado, quando aplicável. |
| `decision` | text | não | Decisão operacional/metodológica aplicada. |
| `reason` | text | não | Motivo detalhado do status/decisão. |
| `raw_file_path` | text | não | Caminho do arquivo bruto, se existir. |
| `checked_at` | timestamptz | sim | Timestamp da verificação/importação. |

Campos adicionais como `raw_payload_hash`, `records_count`, `imported_at` ou `updated_at` podem ser avaliados pelo CTO/Data Engineer, mas a constraint de grain deve permanecer com `artifact_name`.

### Constraint Obrigatória

```sql
UNIQUE (sofascore_event_id, source_name, artifact_name)
```

### Status Recomendados

- `available`
- `imported`
- `known_missing`
- `missing`
- `invalid_raw`
- `skipped`

---

## 8. Política para `event_id=12437015`

### Contexto

A partida `12437015`, Crystal Palace x Liverpool FC, retorna HTTP 404 no endpoint:

```text
https://www.sofascore.com/api/v1/event/12437015/graph
```

Essa ausência deve ser tratada como exceção técnica conhecida.

### Registro Obrigatório em `match_source_status`

| Campo | Valor |
|---|---|
| `sofascore_event_id` | `12437015` |
| `source_name` | `sofascore` |
| `artifact_name` | `graph.json` |
| `status` | `known_missing` |
| `http_status` | `404` |
| `decision` | `keep_match_exclude_graph_required_outputs` |
| `reason` | `HTTP 404 confirmado no endpoint /graph` |
| `raw_file_path` | `NULL` |

### Política Operacional

- Manter a partida para `shotmap`, `incidents` e `statistics`.
- Excluir a partida apenas de outputs que exijam `graph.json` completo.
- Não gerar `graph.json` sintético.
- Não imputar graph sem aprovação metodológica explícita.
- Não fazer bypass agressivo ou tentativa de contorno para HTTP 404.
- Não criar linhas em `match_graph` para `12437015`.

---

## 9. Estratégia de Importer Futuro

### Local Sugerido

Não usar:

```text
LateGoalResearch/Crawler/Sofascore/h8_importer.py
```

Usar preferencialmente:

```text
LateGoalResearch/Importer/Sofascore/h8_importer.py
```

Se já houver padrão oficial existente de importers no projeto, seguir esse padrão.

### Comandos Esperados

```bash
python LateGoalResearch/Importer/Sofascore/h8_importer.py --graph
python LateGoalResearch/Importer/Sofascore/h8_importer.py --shotmap
python LateGoalResearch/Importer/Sofascore/h8_importer.py --all
python LateGoalResearch/Importer/Sofascore/h8_importer.py --dry-run
```

### Funções Internas Esperadas

```python
import_graph()
import_shotmap()
import_source_status()
```

### Responsabilidades de `import_graph()`

- Ler `graph.json` bruto.
- Validar `graphPoints`.
- Criar uma linha por ponto em `match_graph`.
- Usar `momentum_value` para armazenar o valor bruto de momentum.
- Não usar coluna `value`.
- Não transformar o sinal.
- Registrar `source_name='sofascore'`.
- Registrar `artifact_name='graph.json'`.
- Registrar `raw_file_path` e `raw_payload_hash`.
- Pular `12437015` para `match_graph` e registrar status via `import_source_status()`.

### Responsabilidades de `import_shotmap()`

- Ler `shotmap.json` bruto.
- Criar uma linha por finalização em `match_shotmap`.
- Registrar campos temporais, espaciais e xG/xGOT quando disponíveis.
- Registrar `source_name='sofascore'`.
- Registrar `artifact_name='shotmap.json'`.
- Registrar `raw_file_path` e `raw_payload_hash`.
- Não criar features.
- Não misturar dados com `match_incidents`.

### Responsabilidades de `import_source_status()`

- Registrar cobertura por `sofascore_event_id + source_name + artifact_name`.
- Marcar `graph.json` disponível/importado.
- Marcar `shotmap.json` disponível/importado.
- Registrar `12437015 + graph.json` como `known_missing`.
- Registrar `http_status`, `decision`, `reason`, `raw_file_path` e `checked_at`.

---

## 10. Idempotência

O importer futuro deve ser retomável e seguro para múltiplas execuções.

Estratégia obrigatória:

```sql
INSERT ... ON CONFLICT DO UPDATE
```

Conflitos:

```sql
-- match_graph
ON CONFLICT (sofascore_event_id, point_index)

-- match_shotmap
ON CONFLICT (sofascore_event_id, shot_index)

-- match_source_status
ON CONFLICT (sofascore_event_id, source_name, artifact_name)
```

Regras:

- Não duplicar linhas.
- Preservar e atualizar `raw_file_path` e `raw_payload_hash` conforme o arquivo bruto usado.
- Atualizar campos estruturados quando o payload bruto mudar.
- Não apagar registros sem aprovação explícita.
- Não truncar tabelas.
- Não alterar arquivos raw.

---

## 11. Rastreabilidade Raw

Toda linha importada deve permitir rastrear o arquivo bruto de origem.

Campos obrigatórios nos registros granulares:

- `raw_file_path`
- `raw_payload_hash`

Campo obrigatório em status:

- `raw_file_path`, quando houver arquivo bruto.

Hash recomendado:

```text
SHA-256 do conteúdo bruto do arquivo JSON
```

Regras:

- O hash deve ser calculado sobre o arquivo bruto inteiro.
- O hash não deve ser calculado sobre payload transformado.
- O caminho deve apontar para a estrutura raw local padronizada:

```text
data/raw/sofascore/premier_league_61627/matches/{event_id}/graph.json
data/raw/sofascore/premier_league_61627/matches/{event_id}/shotmap.json
```

---

## 12. Validações Pós-Importação

Validações obrigatórias após importer futuro:

### Cobertura Graph

- Esperado: 379 `graph.json` válidos importados.
- Esperado: 1 `known_missing` para `graph.json`.
- `12437015` não deve ter linhas em `match_graph`.
- `12437015` deve existir em `match_source_status` como `known_missing`.

### Cobertura Shotmap

- Esperado: 380 `shotmap.json` válidos importados.
- Zero inválidos importados.

### Integridade

- Duplicatas por `match_graph(sofascore_event_id, point_index)`: 0.
- Duplicatas por `match_shotmap(sofascore_event_id, shot_index)`: 0.
- Duplicatas por `match_source_status(sofascore_event_id, source_name, artifact_name)`: 0.
- Órfãos contra `matches_master`: 0.

### Cobertura por Status

Relatório obrigatório por:

```text
source_name + artifact_name + status
```

Exemplo esperado:

| source_name | artifact_name | status | esperado |
|---|---|---|---:|
| sofascore | graph.json | imported/available | 379 |
| sofascore | graph.json | known_missing | 1 |
| sofascore | shotmap.json | imported/available | 380 |

---

## 13. Riscos de Schema

Riscos e decisões preventivas:

- Não usar `minute` como chave única em `match_graph` ou `match_shotmap`.
- Não misturar `shotmap` em `match_incidents`.
- Não normalizar `shotmap` excessivamente agora.
- Não tornar `graph` obrigatório para toda partida importável.
- Não criar schema orientado a features nesta etapa.
- Manter rastreabilidade raw como requisito central.
- Não usar `match_graph.value`; usar apenas `match_graph.momentum_value`.
- Não transformar o sinal de `momentum_value` durante importação.
- Não bloquear a partida `12437015` para artefatos que não dependem de graph.

---

## 14. Status da Especificação

Documento reconstruído integralmente conforme parecer CTO.

Critérios atendidos:

- Documento completo até Status da Especificação.
- Sem referência a `match_graph.value` como campo válido.
- Campo oficial de graph definido como `match_graph.momentum_value`.
- `match_source_status` com grain `sofascore_event_id + source_name + artifact_name`.
- `source_name` definido como `sofascore`.
- `artifact_name` definido como `graph.json` ou `shotmap.json`.
- Caminho futuro do importer definido fora de `Crawler/Sofascore`.
- Política para `12437015` definida como `known_missing` com HTTP 404.

Status: APROVADO COM AJUSTES CTO — PRONTO PARA PRÓXIMA DECISÃO PM/CTO.
