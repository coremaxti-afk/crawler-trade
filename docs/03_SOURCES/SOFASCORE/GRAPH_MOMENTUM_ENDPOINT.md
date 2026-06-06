# SofaScore Graph / Momentum Endpoint

Status: ENDPOINT CONFIRMADO; COLETA AUDITADA COM RESSALVA TECNICA CONHECIDA

Frente relacionada: H8 - Graph / Momentum / Shotmap

Documento de auditoria completa:

```text
docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_AUDIT_20260606.md
```

---

## Objetivo

Registrar oficialmente o endpoint SofaScore de graph/momentum para uso futuro na frente H8.

Este documento registra descoberta, orientacao operacional e resultado resumido da auditoria de cobertura.

Nao autoriza implementacao de importer, features, baseline, modelagem, backtesting ou producao.

---

## Endpoint

```text
https://www.sofascore.com/api/v1/event/{event_id}/graph
```

Exemplo validado:

```text
https://www.sofascore.com/api/v1/event/12436874/graph
```

---

## Payload Observado

```json
{
  "graphPoints": [
    {"minute": 1, "value": 3},
    {"minute": 2, "value": 20},
    {"minute": 3, "value": 5},
    {"minute": 4, "value": 6},
    {"minute": 5, "value": 18},
    {"minute": 6, "value": -13},
    {"minute": 7, "value": -26}
  ]
}
```

---

## Interpretacao Inicial

Cada item em `graphPoints` contem:

- `minute`: minuto da partida;
- `value`: valor de momentum observado para aquele minuto.

Valores positivos e negativos parecem representar variacao relativa de dominio/momentum entre as equipes.

A semantica exata do sinal deve ser validada antes de qualquer feature engineering oficial.

---

## Estrutura Raw

JSON bruto salvo em:

```text
data/raw/sofascore/premier_league_61627/matches/{event_id}/graph.json
```

---

## Validacao Minima do Payload

Um `graph.json` deve ser considerado valido se:

- for JSON parseavel;
- contiver a chave `graphPoints`;
- `graphPoints` for uma lista;
- cada item tiver `minute` e `value`;
- `minute` for numerico ou conversivel para numero;
- `value` for numerico ou conversivel para numero.

Payload vazio ou ausente deve ser registrado, nao inferido.

---

## Resultado do Spike Inicial

Data de registro: 2026-06-05

Coletores utilizados:

```text
LateGoalResearch/Crawler/Sofascore/h8_graph_momentum_collector.py
LateGoalResearch/Crawler/Sofascore/h8_graph_momentum_collector_playwright.py
```

Partidas testadas no spike controlado:

| Ordem | event_id | Partida | target_late_goal_75 | Status Playwright | graphPoints |
|---:|---:|---|---:|---|---:|
| 1 | 12436870 | Manchester United x Fulham | 1 | JSON valido | 92 |
| 2 | 12436873 | Everton x Brighton & Hove Albion | 1 | JSON valido | 92 |
| 3 | 12436875 | Nottingham Forest x Bournemouth | 1 | JSON valido | 92 |
| 4 | 12436871 | Ipswich Town x Liverpool FC | 0 | JSON valido | 92 |
| 5 | 12436872 | Arsenal x Wolverhampton | 0 | JSON valido | 92 |

Resumo operacional do spike:

- Partidas planejadas: 5.
- Partidas coletadas via Playwright com sessao aquecida: 5.
- JSONs validos retornados: 5.
- `graphPoints` observado: sim, em 5/5 partidas.
- `graph_points_count`: 92 em todas as 5 partidas.
- HTTP 403 na execucao Playwright: nao.
- Criterio de 80% de validade: atingido, com 100% de validade no spike.

Observacao operacional:

O coletor inicial baseado em `urllib` retornou HTTP 403 para `event_id=12436870` em tentativas anteriores. A variante Playwright com browser/sessao aquecida coletou as partidas com sucesso. Portanto, o endpoint esta acessivel, mas depende de contexto de navegador/sessao para a coleta controlada.

---

## Auditoria de Cobertura Atualizada - 2026-06-06

Documento detalhado:

```text
docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_AUDIT_20260606.md
```

Resumo:

| Metrica | Valor |
|---|---:|
| Inventory total | 381 |
| Pastas locais | 381 |
| Partidas importaveis | 380 |
| `graph.json` validos | 379 |
| `graph.json` faltantes totais na base importavel | 1 |
| `graph.json` faltantes excluindo 404 conhecido | 0 |
| `graph.json` invalidos | 0 |
| Minimo de `graphPoints` | 91 |
| Maximo de `graphPoints` | 92 |
| Media de `graphPoints` | 91,98 |

Excecao conhecida:

| event_id | Rodada | Partida | Status |
|---:|---:|---|---|
| 12437015 | 7 | Crystal Palace x Liverpool FC | HTTP 404 confirmado no endpoint `/graph` |

---

## Status Final da Fonte Graph

Status: APTO COM RESSALVA TECNICA CONHECIDA.

Conclusao:

- O endpoint `/graph` e fonte candidata forte para H8.
- Os arquivos validos apresentam estrutura consistente.
- A cobertura esta fechada para todas as partidas importaveis exceto `12437015`, que retorna HTTP 404.
- Antes de importer, feature builder ou baseline H8, o projeto deve definir regra explicita para a excecao `12437015`.

---

## Restricoes

- Nao alterar schema.
- Nao implementar importer.
- Nao criar features H8 ainda.
- Nao criar dataset novo.
- Nao executar baseline.
- Nao fazer modelagem.
- Nao misturar coleta graph com features.
- Nao alterar estrutura dos JSONs existentes.
- Nao iniciar backtesting.
- Nao iniciar producao.

---

## Proximo Passo Recomendado

Decidir, com PM/Data Acquisition/CTO/Data Engineer, a politica para `12437015`:

1. excluir apenas das features H8 baseadas em graph;
2. manter a partida para features baseadas em shotmap/incidents/statistics;
3. ou excluir a partida de datasets H8 que exijam graph completo.

Somente depois disso deve ser planejado qualquer importer ou feature engineering H8.
