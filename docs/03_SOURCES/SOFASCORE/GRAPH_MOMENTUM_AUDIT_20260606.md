# SofaScore Graph / Momentum Audit - 2026-06-06

## Objetivo

Registrar a auditoria local da cobertura de `graph.json` da Premier League 2024/25 para a frente H8 - Graph / Momentum / Shotmap.

Este documento registra apenas cobertura e qualidade de dados brutos.

Nao autoriza importer, alteracao de schema, feature engineering, dataset, baseline, modelagem, backtesting ou producao.

---

## Fonte Auditada

Inventario:

```text
C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\premier_league_61627\inventory.json
```

Pastas de partidas:

```text
C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\premier_league_61627\matches\{event_id}\graph.json
```

Logs verificados:

```text
C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\premier_league_61627\collection_log_graph.jsonl
C:\LateGoalResearch\Crawler\Sofascore\data\raw\sofascore\premier_league_61627\collection_log_graph_playwright.jsonl
```

---

## Criterio de Validade

Um `graph.json` foi considerado valido quando:

- o arquivo existe;
- o JSON e parseavel;
- possui a chave `graphPoints`;
- `graphPoints` e uma lista;
- cada item possui `minute` e `value`;
- `minute` e `value` nao estao nulos.

---

## Resultado Geral

| Metrica | Valor |
|---|---:|
| Inventory total | 381 |
| Pastas locais | 381 |
| Partidas conhecidas como skip | 1 |
| `graph.json` validos | 371 |
| `graph.json` faltantes na base importavel | 9 |
| `graph.json` invalidos | 0 |
| Validos com 0 pontos | 0 |
| Minimo de `graphPoints` | 91 |
| Maximo de `graphPoints` | 92 |
| Media de `graphPoints` | 91,98 |

Interpretacao:

- A cobertura `graph` e alta, mas ainda nao esta fechada para as 380 partidas importaveis.
- Existem 371 partidas importaveis com `graph.json` valido.
- Existem 9 partidas importaveis ainda sem `graph.json`.
- Nao foram encontrados `graph.json` invalidos.
- Os arquivos validos possuem estrutura consistente, com 91 ou 92 pontos.

---

## Partidas Faltantes

| event_id | Rodada | Partida |
|---:|---:|---|
| 12436884 | 2 | Bournemouth x Newcastle United |
| 12436904 | 2 | Wolverhampton x Chelsea |
| 12436908 | 3 | Brentford x Southampton |
| 12436912 | 3 | Everton x Bournemouth |
| 12436927 | 3 | West Ham United x Manchester City |
| 12436923 | 3 | Newcastle United x Tottenham Hotspur |
| 12436949 | 4 | Southampton x Manchester United |
| 12436938 | 4 | Crystal Palace x Leicester City |
| 12437015 | 7 | Crystal Palace x Liverpool FC |

Observacao:

- `12437015` aparece nos logs com HTTP 404 em duas tentativas Playwright.
- As demais partidas aparecem como faltantes locais e podem exigir nova coleta controlada, caso o PM/Data Acquisition autorize.

---

## Skip Conhecido

| event_id | Rodada | Partida | Status |
|---:|---:|---|---|
| 12436452 | 15 | Everton x Liverpool FC | skip conhecido / fora da base importavel atual |

---

## Distribuicao de Pontos

| graph_points_count | Partidas |
|---:|---:|
| 91 | 7 |
| 92 | 364 |

Interpretacao:

- A distribuicao e consistente para dados minuto-a-minuto.
- A diferenca entre 91 e 92 pontos deve ser tratada como variacao operacional normal ate investigacao posterior.
- Nenhum arquivo valido tem lista vazia.

---

## Logs de Coleta

Arquivos de log encontrados:

| Log | Tamanho aproximado | Observacao |
|---|---:|---|
| `collection_log_graph.jsonl` | 741 bytes | Tentativas iniciais baseadas em coletor nao Playwright |
| `collection_log_graph_playwright.jsonl` | 90.397 bytes | Coleta principal via Playwright |

Resumo dos logs:

| Metrica | Valor |
|---|---:|
| Arquivos de log | 2 |
| Linhas de log | 410 |
| Sucessos registrados | 371 |
| Skips registrados | 34 |
| Falhas registradas | 2 |
| Bloqueios HTTP 403 registrados | 3 |

Falhas/bloqueios registrados:

| timestamp | event_id | resultado | status_code | erro | log |
|---|---:|---|---:|---|---|
| 2026-06-05T12:57:30.863371+00:00 | 12436870 | blocked_403 | 403 | HTTP Error 403: Forbidden | `collection_log_graph.jsonl` |
| 2026-06-05T13:00:11.917928+00:00 | 12436870 | blocked_403 | 403 | HTTP Error 403: Forbidden | `collection_log_graph.jsonl` |
| 2026-06-05T13:04:38.745087+00:00 | 12436870 | blocked_403 | 403 | HTTP Error 403: Forbidden | `collection_log_graph.jsonl` |
| 2026-06-05T14:11:14.216620+00:00 | 12437015 | failed | 404 | HTTP 404 | `collection_log_graph_playwright.jsonl` |
| 2026-06-05T14:49:17.576475+00:00 | 12437015 | failed | 404 | HTTP 404 | `collection_log_graph_playwright.jsonl` |

Interpretacao operacional:

- Os HTTP 403 ocorreram na fase inicial com coletor nao Playwright e foram superados posteriormente com Playwright/sessao aquecida.
- O HTTP 404 em `12437015` persistiu em duas tentativas registradas.
- A coleta principal via Playwright foi majoritariamente bem-sucedida, mas nao completou 100% da base importavel.

---

## Status Final da Fonte Graph

Status: APTO COM RESSALVAS.

Conclusao:

- `graph.json` esta disponivel e valido para 371 partidas importaveis.
- A cobertura atual equivale a 371/380 partidas importaveis.
- Ainda existem 9 partidas importaveis sem `graph.json`.
- A fonte e candidata forte para H8, mas ainda requer decisao sobre tratamento dos faltantes antes de importer/feature builder/baseline.

---

## Recomendacao

Antes de qualquer importer ou feature builder H8:

1. Decidir se sera feita nova coleta controlada para as 9 partidas faltantes.
2. Tratar `12437015` separadamente, pois retornou HTTP 404 em duas tentativas.
3. Definir politica para partidas sem `graph.json`:
   - excluir de features H8 graph;
   - imputar apenas se metodologicamente aprovado;
   - manter apenas features `shotmap`/`incidents` para esses jogos;
   - ou exigir cobertura completa antes de avançar.
4. Acionar Data Engineer / Database e CTO antes de qualquer alteracao de schema/importer.
5. Acionar Quant Research somente apos a regra de cobertura/faltantes ser aprovada.

Manter bloqueado:

- importer H8;
- alteracao de schema;
- feature builder H8;
- dataset H8;
- baseline H8;
- modelagem;
- backtesting;
- producao.
