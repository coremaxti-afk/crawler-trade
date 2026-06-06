# SofaScore Shotmap Endpoint

Status: COLETA CONCLUIDA E AUDITADA

Frente relacionada: H8 - Graph / Momentum / Shotmap

Data de registro: 2026-06-06

---

## Objetivo

Registrar oficialmente o endpoint SofaScore de `shotmap`, a estrategia de coleta controlada e o resultado da auditoria local apos a coleta da Premier League 2024/25.

Este documento registra fonte bruta e cobertura operacional.

Nao autoriza importer, schema, feature engineering, dataset, baseline, modelagem, backtesting ou producao.

---

## Endpoint

```text
https://www.sofascore.com/api/v1/event/{event_id}/shotmap
```

Exemplo validado:

```text
https://www.sofascore.com/api/v1/event/12436870/shotmap
```

---

## Utilidade Esperada para H8

O endpoint `shotmap` retorna finalizacoes da partida com dados temporais e espaciais.

Campos observados ou monitorados pelo coletor:

- `minute`
- `time`
- `addedTime`
- `timeSeconds`
- `xg`
- `xgot`
- `player`
- `team`
- `shotType`
- `goalMouthLocation`
- `playerCoordinates`
- `goalMouthCoordinates`
- `draw`

Potencial analitico futuro:

- volume de finalizacoes ate cutoff;
- xG acumulado ate cutoff;
- xG recente;
- xGOT recente;
- qualidade das chances antes do cutoff;
- localizacao das finalizacoes;
- pressao ofensiva por finalizacoes em janelas recentes.

Esses usos dependem de importer e feature builder futuros, ainda nao autorizados neste documento.

---

## Script de Coleta

Script implementado:

```text
LateGoalResearch/Crawler/Sofascore/h8_shotmap_collector.py
```

Commits relacionados:

```text
29ee0bb4cf0586bac82f4dab19b8441a52857734 - cria coletor shotmap H8
4ed6084f369e662ee963ba89305c7c5cb3b43bec - adiciona start-index ao coletor shotmap H8
5521925a0a9345e46cdfedbd2a86807217e628e6 - permite coletar shotmap sem limite
```

---

## Estrutura Raw

Cada resposta bruta foi salva em:

```text
data/raw/sofascore/premier_league_61627/matches/{event_id}/shotmap.json
```

Log auditavel:

```text
data/raw/sofascore/premier_league_61627/collection_log_shotmap.jsonl
```

---

## Regras Operacionais Implementadas

- Ler `inventory.json`.
- Processar apenas partidas ja existentes localmente em `matches/{event_id}/`.
- Nao sobrescrever `shotmap.json` valido existente.
- Se `shotmap.json` existir e for invalido, mover para `_invalid_json_backup` antes de nova coleta.
- Registrar cada tentativa em `collection_log_shotmap.jsonl`.
- Parar imediatamente em HTTP 403.
- Usar Playwright com navegador e warmup manual quando necessario.
- Usar checkpoint por arquivo.
- Usar delay, jitter, backoff e `max_retries`.
- Nao executar em paralelo.
- Nao alterar coletores v2/v3.
- Nao alterar banco, schema, importer, dataset, features ou baseline.

---

## Parametros CLI

Parametros relevantes:

```text
--limit
--start-index
--dry-run
--request-delay
--match-delay
--jitter
--backoff
--max-retries
--headed
--manual-warmup
--storage-state
```

Sem limite:

```text
--limit 0
```

A partir de uma posicao do inventario:

```text
--start-index 31
```

---

## Comando de Coleta Final

Comando usado para coletar os jogos restantes apos os 30 iniciais:

```bash
python C:\LateGoalResearch\Crawler\Sofascore\h8_shotmap_collector.py --limit 0 --start-index 31 --headed --manual-warmup --request-delay 5 --match-delay 8 --jitter 2 --backoff 120 --max-retries 1
```

Observacao:

A reducao operacional de delays foi usada para aproximar a coleta de cerca de 4 jogos por minuto, mantendo execucao sequencial, jitter, backoff e parada em HTTP 403.

---

## Resultado da Coleta Final

Resumo informado ao fim da execucao final:

```text
processed=302
successes=301
skipped=1
failures=0
blocked_403=False
```

Interpretacao:

- A coleta final foi concluida sem falhas.
- Nao houve HTTP 403 durante a execucao final.
- O `skipped=1` correspondeu a um `shotmap.json` valido ja existente.

Partida pulada por checkpoint:

| event_id | Partida | Motivo | Finalizacoes |
|---:|---|---|---:|
| 12437032 | Liverpool FC x Chelsea | `skip_existing_valid` | 21 |

---

## Auditoria Local de Cobertura

Auditoria executada sobre:

```text
C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\premier_league_61627\inventory.json
C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\premier_league_61627\matches\
C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\premier_league_61627\collection_log_shotmap.jsonl
```

Resultado:

| Metrica | Valor |
|---|---:|
| Inventory total | 381 |
| Pastas locais | 381 |
| Partidas conhecidas como skip | 1 |
| `shotmap.json` validos | 380 |
| `shotmap.json` faltantes, excluindo skip conhecido | 0 |
| `shotmap.json` invalidos | 0 |
| Partidas validas com 0 finalizacoes | 0 |
| Total de finalizacoes | 9.883 |
| Minimo de finalizacoes por partida | 13 |
| Maximo de finalizacoes por partida | 48 |
| Media de finalizacoes por partida | 26,01 |
| Linhas no log | 383 |
| Sucessos registrados no log | 380 |
| Falhas registradas no log | 0 |

Skip conhecido:

| event_id | Rodada | Partida | Status |
|---:|---:|---|---|
| 12436452 | 15 | Everton x Liverpool FC | skip conhecido / fora da base importavel atual |

Registros antigos de 403:

| event_id | Resultado | Observacao |
|---:|---|---|
| 12436870 | `blocked_403` | Registro antigo de tentativa anterior, nao ocorreu na coleta final |
| 12436870 | `blocked_403` | Registro antigo de tentativa anterior, nao ocorreu na coleta final |

---

## Top 10 Partidas por Numero de Finalizacoes

| event_id | Rodada | Partida | Finalizacoes |
|---:|---:|---|---:|
| 12436609 | 32 | Chelsea x Ipswich Town | 48 |
| 12436440 | 22 | Brentford x Liverpool FC | 48 |
| 12436465 | 16 | Bournemouth x West Ham United | 45 |
| 12436590 | 37 | Brighton & Hove Albion x Liverpool FC | 43 |
| 12436985 | 6 | Arsenal x Leicester City | 41 |
| 12436462 | 15 | Ipswich Town x Bournemouth | 40 |
| 12437036 | 8 | Nottingham Forest x Crystal Palace | 40 |
| 12436436 | 21 | Brentford x Manchester City | 39 |
| 12436966 | 14 | Leicester City x West Ham United | 39 |
| 12436908 | 3 | Brentford x Southampton | 38 |

---

## Status Final da Fonte Shotmap

Status: APTO PARA PROXIMA AVALIACAO TECNICA.

Conclusao:

- A cobertura `shotmap` esta fechada para as 380 partidas importaveis.
- A partida `12436452` permanece como skip conhecido.
- Nao ha pendencias de JSON faltante ou invalido para a base importavel atual.
- A fonte pode ser considerada candidata forte para importer/feature builder H8 futuro.

---

## Recomendacao

Proximo passo recomendado:

- Acionar Data Engineer / Database para avaliar desenho de importer futuro de `graph.json` e `shotmap.json`.
- Acionar Quant Research / Data Science para definir especificacao metodologica de features H8 somente depois da avaliacao de armazenamento/importacao.

Manter bloqueado ate nova aprovacao:

- importer H8;
- alteracao de schema;
- feature builder H8;
- dataset H8;
- baseline H8;
- modelagem;
- backtesting;
- producao.
