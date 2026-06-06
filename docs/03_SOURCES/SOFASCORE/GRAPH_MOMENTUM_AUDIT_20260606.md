# SofaScore Graph / Momentum Audit - 2026-06-06

## Objetivo

Registrar a auditoria local atualizada da cobertura de `graph.json` da Premier League 2024/25 para a frente H8 - Graph / Momentum / Shotmap.

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

## Resultado Geral Atualizado

| Metrica | Valor |
|---|---:|
| Inventory total | 381 |
| Pastas locais | 381 |
| Partidas importaveis | 380 |
| Partidas conhecidas como skip de importacao | 1 |
| `graph.json` validos | 379 |
| `graph.json` faltantes totais na base importavel | 1 |
| `graph.json` faltantes excluindo 404 conhecido | 0 |
| `graph.json` invalidos | 0 |
| Minimo de `graphPoints` | 91 |
| Maximo de `graphPoints` | 92 |
| Media de `graphPoints` | 91,98 |

Interpretacao:

- A cobertura `graph` foi praticamente fechada para a base importavel.
- Existem 379 partidas importaveis com `graph.json` valido.
- A unica partida importavel sem `graph.json` e `12437015`, com HTTP 404 confirmado.
- Nao foram encontrados `graph.json` invalidos.
- Os arquivos validos possuem estrutura consistente, com 91 ou 92 pontos.

---

## Excecao Conhecida: HTTP 404

| event_id | Rodada | Partida | Status |
|---:|---:|---|---|
| 12437015 | 7 | Crystal Palace x Liverpool FC | HTTP 404 confirmado no endpoint `/graph` |

Interpretacao:

- O endpoint `https://www.sofascore.com/api/v1/event/12437015/graph` retorna HTTP 404.
- Nao ha muito a corrigir via coleta neste caso sem mudar fonte, endpoint ou regra metodologica.
- A partida deve ser tratada como excecao tecnica conhecida para `graph`.

---

## Skip Conhecido de Importacao

| event_id | Rodada | Partida | Status |
|---:|---:|---|---|
| 12436452 | 15 | Everton x Liverpool FC | skip conhecido / fora da base importavel atual |

---

## Distribuicao de Pontos

| graph_points_count | Partidas |
|---:|---:|
| 91 | 7 |
| 92 | 372 |

Interpretacao:

- A distribuicao e consistente para dados minuto-a-minuto.
- A diferenca entre 91 e 92 pontos deve ser tratada como variacao operacional normal ate investigacao posterior.
- Nenhum arquivo valido tem lista vazia.

---

## Evolucao da Cobertura

Auditoria anterior:

- `graph.json` validos: 371.
- Faltantes na base importavel: 9.

Auditoria atualizada apos coleta manual dos links faltantes:

- `graph.json` validos: 379.
- Faltantes na base importavel: 1.
- Faltante restante: `12437015`, HTTP 404 confirmado.

---

## Status Final da Fonte Graph

Status: APTO COM RESSALVA TECNICA CONHECIDA.

Conclusao:

- `graph.json` esta disponivel e valido para 379 das 380 partidas importaveis.
- A unica ausencia restante e `12437015`, por HTTP 404 confirmado.
- A fonte e candidata forte para H8.
- Antes de importer/feature builder/baseline H8, o projeto deve definir regra explicita para a excecao `12437015`.

---

## Recomendacao

Antes de qualquer importer ou feature builder H8:

1. Registrar `12437015` como excecao tecnica conhecida para `graph`.
2. Definir politica metodologica para a partida sem `graph.json`:
   - excluir apenas das features H8 baseadas em graph;
   - manter para features H8 baseadas em shotmap/incidents/statistics;
   - ou excluir a partida de datasets H8 que exijam graph completo.
3. Nao tentar contornos agressivos para o HTTP 404.
4. Acionar Data Engineer / Database e CTO antes de qualquer alteracao de schema/importer.
5. Acionar Quant Research somente apos a regra de cobertura/excecao ser aprovada.

Manter bloqueado:

- importer H8;
- alteracao de schema;
- feature builder H8;
- dataset H8;
- baseline H8;
- modelagem;
- backtesting;
- producao.
