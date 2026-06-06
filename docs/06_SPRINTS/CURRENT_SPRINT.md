# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar a frente H8 com dados temporais de graph/momentum e shotmap, preparando a proxima fase de importacao/feature engineering sem iniciar backtesting ou producao.

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

---

## Documentos H8

- `docs/03_SOURCES/SOFASCORE/ENDPOINT_DISCOVERY_20260605.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_ENDPOINT.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_AUDIT_20260606.md`
- `docs/03_SOURCES/SOFASCORE/SHOTMAP_ENDPOINT.md`

---

## Estado Atual da Coleta H8

### Graph

Status:

- Coletado e auditado com ressalva tecnica conhecida.

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
- Excecao conhecida: `12437015`, Crystal Palace x Liverpool FC, HTTP 404 no endpoint `/graph`.

Interpretacao:

- `graph` continua sendo o principal artefato temporal de momentum/pressao para H8.
- A cobertura esta efetivamente fechada, exceto por uma excecao tecnica conhecida.
- Antes de importer/feature builder/baseline H8, e preciso definir regra explicita para `12437015`.

### Shotmap

Status:

- Coletado e auditado com sucesso.

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

---

## Base Candidata para H8

- `graph`
- `shotmap`
- `incidents`
- `statistics`

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
- H8 - FRENTE ATIVA: graph/momentum + shotmap coletados e auditados; pendente decisao de importer/feature spec.
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
- Nao implementar importer H8 sem aprovacao explicita.
- Nao alterar schema para H8 sem aprovacao explicita do CTO/Data Engineer.

---

## Proximos Passos

- [ ] Definir politica de tratamento para `12437015` sem `graph.json`.
- [ ] Validar estrutura conjunta de `graph` e `shotmap` para desenho futuro de importer.
- [ ] Acionar Data Engineer / Database para avaliar importer futuro de `graph` e `shotmap`.
- [ ] Acionar CTO se houver necessidade de nova arquitetura de armazenamento/importacao.
- [ ] So depois definir plano Quant para H8.

---

## Status

EM EXECUCAO - SHOTMAP AUDITADO COM 380/380 PARTIDAS IMPORTAVEIS COBERTAS; GRAPH AUDITADO COM 379/380 PARTIDAS IMPORTAVEIS COBERTAS E 1 EXCECAO 404 CONHECIDA (`12437015`); H8 SEGUE COMO FRENTE ATIVA, SEM IMPORTER/FEATURES/BASELINE AUTORIZADOS AINDA.
