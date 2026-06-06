# PROJECT STATUS

## Estado Atual da Base

- Inventory SofaScore EPL: 381 partidas.
- Pastas locais: 381.
- Partidas importaveis: 380.
- Partida descartada da importacao atual: `12436452`.
- `matches_master`: 380 partidas.
- `match_statistics`: 380 partidas.
- `match_incidents`: 7647 registros.
- `match_graph`: 34861 pontos em 379 partidas.
- `match_shotmap`: 9883 finalizacoes em 380 partidas.
- `match_source_status`: 760 registros.
- Orfaos em `match_statistics`: 0.
- Orfaos em `match_incidents`: 0.

Ressalvas:

- `big_chances_home` possui 7 nulos.
- `big_chances_away` possui 7 nulos.
- `12436452` segue como partida conhecida descartada da importacao SofaScore atual.
- `12437015` segue como `known_missing` para `graph.json`, HTTP 404 confirmado, mantendo a partida e excluindo apenas outputs que exigem Graph.

---

## Concluido

- Estrutura documental do projeto consolidada.
- Understat integrado.
- FotMob integrado parcialmente.
- EPL 2024/2025 descoberta via SofaScore com 381 partidas no inventory.
- Match Mapping criado.
- PostgreSQL configurado.
- SQLAlchemy configurado.
- Tabelas `match_mapping`, `matches_master`, `match_statistics`, `match_incidents`, `match_graph`, `match_shotmap` e `match_source_status` criadas.
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
- Schema/storage H8 implementado e importado para `match_graph`, `match_shotmap` e `match_source_status`.
- Catalogo metodologico H8 V1 concluido.
- Validacao Estatistica Inicial H8-A/H8-B executada.

---

## H8 - Graph / Momentum / Shotmap

Documentos:

- `docs/03_SOURCES/SOFASCORE/ENDPOINT_DISCOVERY_20260605.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_ENDPOINT.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_AUDIT_20260606.md`
- `docs/03_SOURCES/SOFASCORE/SHOTMAP_ENDPOINT.md`
- `docs/08_DATABASE/H8_STORAGE_IMPORT_SPEC.md`
- `docs/04_RESEARCH/H8_FEATURE_CATALOG_V1.md`
- `docs/04_RESEARCH/H8_INITIAL_STATISTICAL_VALIDATION_RESULTS.md`

Status:

- H8 e a frente ativa.
- `graph.json` foi coletado, auditado, armazenado e importado como artefato temporal de momentum/pressao.
- `shotmap.json` foi coletado, auditado, armazenado e importado como artefato de finalizacoes temporais/espaciais.
- `12437015` permanece como excecao tecnica conhecida para Graph.
- Validacao estatistica inicial H8 foi executada contra `target_late_goal_75` nos cutoffs 60, 65, 70 e 75.
- Feature Builder H8 ainda nao foi implementado.
- Dataset H8 permanente ainda nao foi criado.
- Baseline H8 ainda nao foi executado.
- Producao e backtesting financeiro continuam bloqueados.

Auditoria `graph`:

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

Validacao Estatistica Inicial H8:

- Testes executados: 36 combinacoes cutoff-feature.
- MANTER: 2.
- OBSERVAR: 27.
- DESCARTAR: 7.
- NAO TESTAVEL: 0.
- Melhor sinal: `momentum_trend_last_10m` no cutoff 60, p-value 0,0194, efeito maximo 13,0 p.p.
- Segundo sinal aprovado: `shots_last_10m` no cutoff 60, p-value 0,0492, efeito maximo 11,7 p.p.
- Graph e Shotmap seguem como familias complementares candidatas.

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
- H8 - VALIDADA INICIALMENTE: Graph e Shotmap possuem sinais candidatos; pendente Feature Builder H8 e decisao de proxima etapa.
- H9 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.

---

## Em Andamento

### Consolidacao H8

Proximos agentes provaveis:

- Quant Research / Data Science.
- Data Engineer / Database.
- CTO.

Objetivo:

Revisar a validacao estatistica inicial H8 e decidir se sera autorizado Feature Builder H8, Dataset H8 e/ou Baseline H8 controlado.

---

## Proximas Etapas

1. Revisar `docs/04_RESEARCH/H8_INITIAL_STATISTICAL_VALIDATION_RESULTS.md`.
2. Decidir quais features H8 classificadas como MANTER/OBSERVAR seguem para Feature Builder.
3. Se autorizado, implementar Feature Builder H8 com whitelist e auditoria anti-leakage.
4. Se autorizado, gerar Dataset H8 por cutoff.
5. Se autorizado, executar Baseline H8 controlado.
6. Manter backtesting financeiro e producao bloqueados.

---

## Descobertas Recentes

- H3/H4 pre-jogo isoladas nao foram suficientes no Baseline 1A.
- H6/H9 melhoraram o baseline, mas nao aprovaram quantitativamente sem graph/momentum.
- `graph` foi confirmado como fonte temporal de momentum/pressao.
- `graph` possui 379/380 partidas importaveis cobertas e 1 excecao 404 conhecida.
- `shotmap` foi confirmado como fonte de finalizacoes temporais/espaciais.
- A cobertura `shotmap` esta fechada para as 380 partidas importaveis.
- H8-A/H8-B apresentaram 2 sinais MANTER e 27 OBSERVAR na validacao univariada inicial.
- Nenhum backtesting ou producao foi iniciado.
