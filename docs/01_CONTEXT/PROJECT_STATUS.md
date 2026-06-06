# PROJECT STATUS

## Estado Atual da Base

- Inventory SofaScore EPL: 381 partidas.
- Pastas locais: 381.
- Partidas importaveis: 380.
- Partida descartada da importacao atual: `12436452`.
- `matches_master`: 380 partidas.
- `match_statistics`: 380 partidas.
- `match_incidents`: 7647 registros.
- Orfaos em `match_statistics`: 0.
- Orfaos em `match_incidents`: 0.

Ressalvas:

- `big_chances_home` possui 7 nulos.
- `big_chances_away` possui 7 nulos.
- `match_graph` ainda nao possui dados importados.
- Dados raw H8 (`graph.json` e `shotmap.json`) foram coletados, mas ainda nao possuem importer aprovado.

---

## Concluido

- Estrutura documental do projeto consolidada.
- Understat integrado.
- FotMob integrado parcialmente.
- EPL 2024/2025 descoberta via SofaScore com 381 partidas no inventory.
- Match Mapping criado.
- PostgreSQL configurado.
- SQLAlchemy configurado.
- Tabelas `match_mapping`, `matches_master`, `match_statistics`, `match_incidents` e `match_graph` criadas.
- Coleta SofaScore core/full auditada com 380 partidas importaveis.
- PostgreSQL populado com 380 partidas SofaScore importaveis.
- Dataset Analitico V1 gerado com 380 linhas e status APTO COM RESSALVAS.
- Target Audit concluido: `target_late_goal_75` com 189 positivos e 191 negativos.
- Validacao H1/H2 bloqueada por risco confirmado de data leakage.
- Validacao H3/H4 concluida.
- Baseline 1A Pre-Match H3/H4 implementado, executado e revisado como NAO APROVADO quantitativamente.
- Baseline In-Game V1 H6/H9 implementado, executado e revisado como NAO APROVADO quantitativamente.
- Discovery controlado SofaScore H8 executado.
- Endpoint `/graph` confirmado como fonte temporal de momentum.
- Endpoint `/shotmap` confirmado como fonte de finalizacoes temporais e espaciais.
- Coleta raw `graph.json` executada e auditada.
- Coleta raw `shotmap.json` executada e auditada.

---

## H8 - Graph / Momentum / Shotmap

Documentos:

- `docs/03_SOURCES/SOFASCORE/ENDPOINT_DISCOVERY_20260605.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_ENDPOINT.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_AUDIT_20260606.md`
- `docs/03_SOURCES/SOFASCORE/SHOTMAP_ENDPOINT.md`

Status:

- H8 e a frente ativa.
- `graph.json` foi coletado como artefato raw temporal de momentum/pressao.
- `shotmap.json` foi coletado como artefato raw de finalizacoes temporais/espaciais.
- Importer H8 ainda nao autorizado.
- Feature builder H8 ainda nao autorizado.
- Dataset/Baseline H8 ainda nao autorizados.

Auditoria `graph` atualizada:

- Inventory total: 381 partidas.
- Pastas locais: 381.
- Partidas importaveis: 380.
- `graph.json` validos: 379.
- `graph.json` faltantes totais na base importavel: 1.
- `graph.json` faltantes excluindo 404 conhecido: 0.
- `graph.json` invalidos: 0.
- `graphPoints` minimo: 91.
- `graphPoints` maximo: 92.
- Media de `graphPoints`: 91,98.
- Excecao tecnica conhecida: `12437015`, Crystal Palace x Liverpool FC, HTTP 404 no endpoint `/graph`.

Auditoria `shotmap`:

- Inventory total: 381 partidas.
- Pastas locais: 381.
- Partidas importaveis: 380.
- `shotmap.json` validos: 380.
- `shotmap.json` faltantes na base importavel: 0.
- `shotmap.json` invalidos: 0.
- Total de finalizacoes: 9.883.
- Media de finalizacoes por partida: 26,01.
- Partida conhecida como skip: `12436452`.

Interpretacao:

- `graph` e `shotmap` formam a base raw candidata para features H8.
- `shotmap` pode permitir, futuramente, xG acumulado ate cutoff, xG recente, volume de chutes, xGOT recente e qualidade das chances antes do cutoff.
- `graph` pode permitir, futuramente, momentum acumulado, momentum recente, pressao por janela e variacoes de dominio antes do cutoff.
- Nenhuma dessas features foi implementada ainda.
- Antes de importer/feature builder H8, e necessario definir regra explicita para `12437015` sem `graph.json`.

---

## Dataset Analitico V1

Status:

- Gerado.
- APTO COM RESSALVAS.

Resumo:

- Linhas: 380.
- Grain: 1 linha por partida.
- Target principal: `target_late_goal_75`.
- Target positivo: 189.
- Target negativo: 191.
- Duplicatas por `match_id`: 0.
- Duplicatas por `sofascore_event_id`: 0.

Colunas proibidas como features:

- `has_late_goal`
- `target_late_goal_75`
- `late_goal_count_75`
- `home_late_goal_count_75`
- `away_late_goal_count_75`
- `first_late_goal_minute_75`
- `home_goals`
- `away_goals`
- `total_goals`

Regra:

- Estatisticas finais da propria partida sao proibidas como preditores in-game.

---

## Status das Hipoteses

- H1 - BLOQUEADA por data leakage.
- H2 - BLOQUEADA por data leakage.
- H3 - MANTER COMO CANDIDATA, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H4 - MANTER COMO CANDIDATA FORTE, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H5 - NAO VALIDADA.
- H6 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.
- H7 - NAO VALIDADA COMO HIPOTESE INDEPENDENTE.
- H8 - FRENTE ATIVA: raw `graph` e `shotmap` coletados e auditados; pendente decisao de importer/feature spec.
- H9 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.

---

## Em Andamento

### Consolidacao H8

Proximos agentes provaveis:

- Data Engineer / Database.
- CTO.
- Quant Research / Data Science.

Objetivo:

Avaliar como importar e validar `graph.json` e `shotmap.json` antes de qualquer feature builder ou baseline H8.

---

## Proximas Etapas

1. Definir politica para `12437015` sem `graph.json`.
2. Validar estrutura de `graph.json` e `shotmap.json` para desenho futuro de importer.
3. Acionar Data Engineer / Database para avaliar armazenamento/importacao H8.
4. Acionar CTO se houver mudanca de schema ou nova estrutura de armazenamento.
5. Acionar Quant Research para especificar features H8 somente apos decisao de armazenamento/importacao.
6. Manter backtesting e producao bloqueados.

---

## Descobertas Recentes

- H3/H4 pre-jogo isoladas nao foram suficientes no Baseline 1A.
- H6/H9 melhoraram o baseline, mas nao aprovaram quantitativamente sem graph/momentum.
- `graph` foi confirmado como fonte temporal de momentum/pressao.
- `graph` possui 379/380 partidas importaveis cobertas e 1 excecao 404 conhecida.
- `shotmap` foi confirmado como fonte de finalizacoes temporais/espaciais.
- A cobertura `shotmap` esta fechada para as 380 partidas importaveis.
- A proxima decisao tecnica e sobre tratamento da excecao/importer/armazenamento H8, nao modelagem.
- Nenhum backtesting ou producao foi iniciado.
