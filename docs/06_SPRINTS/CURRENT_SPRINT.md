# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar a frente H8 com dados temporais de graph/momentum e shotmap, passando da coleta/importacao para validacao estatistica inicial sem iniciar producao, automacao operacional ou backtesting financeiro.

---

## Concluido

- [x] Executar discovery controlado de endpoints SofaScore.
- [x] Confirmar endpoint `/graph` como util para H8.
- [x] Confirmar endpoint `/shotmap` como util para H8.
- [x] Coletar `graph` com sucesso operacional.
- [x] Auditar cobertura `graph` da base EPL importavel.
- [x] Coletar `shotmap` com sucesso.
- [x] Auditar cobertura `shotmap` da base EPL importavel.
- [x] Documentar API-Football e SofaScore discovery.
- [x] Documentar auditoria final de `graph` e `shotmap`.
- [x] Especificar storage/import H8.
- [x] Implementar schema/storage H8.
- [x] Implementar e executar importer H8.
- [x] Registrar `12437015` como known_missing para Graph HTTP 404.
- [x] Completar catalogo metodologico H8 V1.
- [x] Executar Validacao Estatistica Inicial H8-A/H8-B.

---

## Documentos H8

- `docs/03_SOURCES/SOFASCORE/ENDPOINT_DISCOVERY_20260605.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_ENDPOINT.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_AUDIT_20260606.md`
- `docs/03_SOURCES/SOFASCORE/SHOTMAP_ENDPOINT.md`
- `docs/08_DATABASE/H8_STORAGE_IMPORT_SPEC.md`
- `docs/04_RESEARCH/H8_FEATURE_CATALOG_V1.md`
- `docs/04_RESEARCH/H8_INITIAL_STATISTICAL_VALIDATION_RESULTS.md`

---

## Estado Atual da Coleta e Importacao H8

### Graph

Status:

- Coletado, auditado, armazenado e importado com ressalva tecnica conhecida.

Auditoria atualizada:

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
- Registros importados em `match_graph`: 34.861.
- Excecao conhecida: `12437015`, Crystal Palace x Liverpool FC, HTTP 404 no endpoint `/graph`.

Interpretacao:

- `graph` continua sendo o principal artefato temporal de momentum/pressao para H8.
- A cobertura esta efetivamente fechada, exceto por uma excecao tecnica conhecida.
- Outputs que exigem Graph devem excluir `12437015` ou tratar explicitamente como known_missing.

### Shotmap

Status:

- Coletado, auditado, armazenado e importado com sucesso.

Auditoria:

- Inventory total: 381 partidas.
- Pastas locais: 381.
- Partidas importaveis: 380.
- `shotmap.json` validos: 380.
- Faltantes na base importavel: 0.
- Invalidos: 0.
- Partida conhecida como skip: `12436452`.
- Total de finalizacoes: 9.883.
- Media de finalizacoes por partida: 26,01.
- HTTP 403 na coleta final: nao.
- Registros importados em `match_shotmap`: 9.883.

### Source Status

- Registros em `match_source_status`: 760.
- `12437015` registrado como `known_missing` para `graph.json`, HTTP 404.

---

## Validacao Estatistica Inicial H8

Status:

- Executada.
- Sem criacao de modelo.
- Sem baseline.
- Sem alteracao de schema/importer/crawler/dados brutos.

Resumo:

- Target: `target_late_goal_75`.
- Cutoffs: 60, 65, 70 e 75.
- Testes avaliados: 36 combinacoes cutoff-feature.
- MANTER: 2.
- OBSERVAR: 27.
- DESCARTAR: 7.
- NAO TESTAVEL: 0.

Melhores sinais:

- `momentum_trend_last_10m`, cutoff 60: MANTER, p-value 0,0194, efeito maximo 13,0 p.p.
- `shots_last_10m`, cutoff 60: MANTER, p-value 0,0492, efeito maximo 11,7 p.p.

Interpretacao:

- Graph e Shotmap devem seguir como familias complementares.
- A validacao e exploratoria/univariada e nao autoriza producao nem backtesting.
- Proxima etapa depende de aprovacao para Feature Builder H8 e eventual Dataset/Baseline H8.

---

## Base Candidata para H8

- `graph`
- `shotmap`
- `incidents`
- `statistics`, apenas quando houver controle temporal seguro e aprovacao explicita

Complementos possiveis:

- `lineups`
- `average-positions`
- `managers`

Endpoints nao recomendados para insistencia por tentativa de nomes:

- `/attacks`
- `/dangerous-attacks`
- `/possession`
- `/field-tilt`
- `/pressure`
- `/momentum`
- `/attack-momentum`

---

## Status das Hipoteses

- H1 - BLOQUEADA por data leakage.
- H2 - BLOQUEADA por data leakage.
- H3 - MANTER COMO CANDIDATA, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H4 - MANTER COMO CANDIDATA FORTE, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H5 - NAO VALIDADA.
- H6 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.
- H7 - NAO VALIDADA COMO HIPOTESE INDEPENDENTE.
- H8 - VALIDADA INICIALMENTE: Graph/Shotmap possuem sinais candidatos; pendente decisao para Feature Builder/Dataset/Baseline H8.
- H9 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.

---

## Restricoes Ativas

- Nao avancar nenhum baseline atual para backtesting.
- Nao usar nenhum baseline atual em producao.
- Nao transformar nenhum baseline atual em sistema decisorio.
- Nao usar features bloqueadas.
- Nao usar estatisticas finais da propria partida como preditores.
- Nao usar xG/xGA/forecast sem comprovacao temporal segura.
- Nao usar eventos apos cutoff como features in-game.
- Manter backtesting e producao bloqueados.
- Nao implementar Feature Builder H8 sem aprovacao explicita.
- Nao criar Dataset H8 permanente sem aprovacao explicita.
- Nao executar Baseline H8 sem aprovacao explicita.

---

## Proximos Passos

- [ ] Revisar `docs/04_RESEARCH/H8_INITIAL_STATISTICAL_VALIDATION_RESULTS.md`.
- [ ] Definir com Quant Research quais features H8 MANTER/OBSERVAR seguem.
- [ ] Solicitar aprovacao PM/CTO antes de Feature Builder H8.
- [ ] Se aprovado, implementar Feature Builder H8 com whitelist e auditoria anti-leakage.
- [ ] Se aprovado, gerar Dataset H8 por cutoff.
- [ ] Se aprovado, executar Baseline H8 controlado.
- [ ] Manter backtesting e producao bloqueados.

---

## Status

EM EXECUCAO - H8 COLETADO, AUDITADO, IMPORTADO E VALIDADO ESTATISTICAMENTE EM RODADA INICIAL. GRAPH: 379/380 PARTIDAS IMPORTAVEIS COBERTAS COM 1 EXCECAO 404 CONHECIDA (`12437015`). SHOTMAP: 380/380 PARTIDAS IMPORTAVEIS COBERTAS. VALIDACAO H8-A/H8-B: 2 FEATURES MANTER, 27 OBSERVAR, 7 DESCARTAR. PROXIMA DECISAO: FEATURE BUILDER/DATASET/BASELINE H8, AINDA SEM PRODUCAO OU BACKTESTING.
