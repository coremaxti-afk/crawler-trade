# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar a frente H8 com dados temporais de graph/momentum e shotmap, preparando a proxima fase de importacao/feature engineering sem iniciar backtesting ou producao.

---

## Concluido

- [x] Criar collectors SofaScore.
- [x] Resolver robustez operacional do HTTP 403 com coleta core.
- [x] Coletar/auditar EPL SofaScore com 381 partidas no inventario.
- [x] Consolidar 380 partidas importaveis.
- [x] Implementar `sofascore_importer.py`.
- [x] Popular PostgreSQL com dados core SofaScore.
- [x] Validar idempotencia do importer.
- [x] Validar integridade basica entre `matches_master`, `match_statistics` e `match_incidents`.
- [x] Executar validacao leve de qualidade pos-importacao.
- [x] Definir metodologia do Dataset Analitico V1.
- [x] Implementar Dataset Builder V1.
- [x] Gerar Dataset Analitico V1.
- [x] Executar Target Audit.
- [x] Validar estatisticamente H6/H9.
- [x] Bloquear H1/H2 por risco confirmado de data leakage.
- [x] Construir feature set historico pre-jogo H3/H4.
- [x] Validar estatisticamente H3/H4.
- [x] Produzir e aprovar `FEATURE_CANDIDATE_SET_V1.md`.
- [x] Implementar e executar Baseline 1A Pre-Match H3/H4.
- [x] Revisar resultado quantitativo do Baseline 1A.
- [x] Produzir `BASELINE_INGAME_IMPLEMENTATION_SPEC.md`.
- [x] Implementar e executar Baseline In-Game V1.
- [x] Revisar resultado quantitativo do Baseline In-Game V1.
- [x] Encerrar a iteracao de baselines sem graph/momentum como exploratoria e nao aprovada para backtesting/producao.
- [x] Executar discovery controlado de endpoints SofaScore.
- [x] Confirmar endpoint `/graph` como util para H8.
- [x] Confirmar endpoint `/shotmap` como util para H8.
- [x] Coletar `graph` com sucesso parcial.
- [x] Auditar cobertura `graph` da base EPL importavel.
- [x] Coletar `shotmap` com sucesso.
- [x] Auditar cobertura `shotmap` da base EPL importavel.

---

## Resultado dos Baselines Sem Graph

### Baseline 1A - Pre-Match H3/H4

Documento:

- `docs/04_RESEARCH/BASELINE_PREMATCH_H3_H4_RESULTS.md`

Status:

- Operacional: APTO COM RESSALVAS.
- Quantitativo: NAO APROVADO.
- Decisao: nao avancar para backtesting, producao ou sistema decisorio.

### Baseline In-Game V1 - H6/H9

Documento:

- `docs/04_RESEARCH/BASELINE_INGAME_V1_RESULTS.md`

Status:

- Operacional: APTO COM RESSALVAS.
- Quantitativo: NAO APROVADO.
- Decisao: nao avancar para backtesting, producao ou sistema decisorio.

Interpretacao:

- O In-Game V1 melhorou em relacao ao Pre-Match, mas ainda nao atingiu os criterios minimos.
- Os baselines atuais servem como benchmarks exploratorios, nao como modelos candidatos.
- A proxima hipotese prioritaria e que dados vivos de momentum/pressao e finalizacoes possam aumentar o sinal preditivo.

---

## Discovery SofaScore H8

Documentos:

- `docs/03_SOURCES/SOFASCORE/ENDPOINT_DISCOVERY_20260605.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_ENDPOINT.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_AUDIT_20260606.md`
- `docs/03_SOURCES/SOFASCORE/SHOTMAP_ENDPOINT.md`

Endpoints uteis confirmados:

- `/graph`
- `/shotmap`
- `/statistics`
- `/incidents`
- `/lineups`
- `/average-positions`
- `/managers`

Base candidata para H8:

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

Decisao:

- Nao insistir em endpoints nao confirmados por tentativa de nomes.
- Priorizar H8 com `graph` + `shotmap` + `incidents` + `statistics`.

---

## Estado Atual da Coleta H8

### Graph

Status:

- Coletado e auditado com ressalvas.

Auditoria:

- Inventory total: 381 partidas.
- Pastas locais: 381.
- Partidas importaveis: 380.
- `graph.json` validos: 371.
- `graph.json` faltantes na base importavel: 9.
- `graph.json` invalidos: 0.
- Validos com 0 pontos: 0.
- `graphPoints` minimo: 91.
- `graphPoints` maximo: 92.
- Media de `graphPoints`: 91,98.
- Partida conhecida como skip: `12436452`.

Faltantes:

- `12436884` - Bournemouth x Newcastle United.
- `12436904` - Wolverhampton x Chelsea.
- `12436908` - Brentford x Southampton.
- `12436912` - Everton x Bournemouth.
- `12436927` - West Ham United x Manchester City.
- `12436923` - Newcastle United x Tottenham Hotspur.
- `12436949` - Southampton x Manchester United.
- `12436938` - Crystal Palace x Leicester City.
- `12437015` - Crystal Palace x Liverpool FC.

Documento:

- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_AUDIT_20260606.md`

Interpretacao:

- `graph` continua sendo o principal artefato temporal de momentum/pressao para H8.
- A cobertura atual e alta, mas nao esta fechada para as 380 partidas importaveis.
- Antes de importer/feature builder/baseline H8, e preciso decidir a regra para as 9 partidas faltantes.

### Shotmap

Status:

- Coletado e auditado com sucesso.

Auditoria:

- Inventory total: 381 partidas.
- Pastas locais: 381.
- `shotmap.json` validos: 380.
- Faltantes na base importavel: 0.
- Invalidos: 0.
- Partida conhecida como skip: `12436452`.
- Total de finalizacoes: 9.883.
- Media de finalizacoes por partida: 26,01.
- HTTP 403 na coleta final: nao.

Documento:

- `docs/03_SOURCES/SOFASCORE/SHOTMAP_ENDPOINT.md`

Interpretacao:

- `shotmap` fornece finalizacoes com minuto, acrescimo, `timeSeconds`, xG, xGOT e coordenadas.
- A cobertura esta fechada para as 380 partidas importaveis.
- Pode permitir features futuras como xG acumulado ate cutoff, xG recente, volume de chutes e qualidade das chances antes do cutoff.
- Importer, feature builder e baseline H8 continuam bloqueados ate nova aprovacao.

---

## Status das Hipoteses

- H1 - BLOQUEADA por data leakage.
- H2 - BLOQUEADA por data leakage.
- H3 - MANTER COMO CANDIDATA, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H4 - MANTER COMO CANDIDATA FORTE, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H5 - NAO VALIDADA.
- H6 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.
- H7 - NAO VALIDADA COMO HIPOTESE INDEPENDENTE.
- H8 - FRENTE ATIVA: graph/momentum + shotmap coletados; graph com 9 faltantes; pendente decisao de cobertura/importer/feature spec.
- H9 - VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph nao aprovou quantitativamente.

---

## Proxima Frente Oficial

Consolidacao tecnica da H8.

Objetivo:

Validar a cobertura e a qualidade dos dados `graph` e `shotmap` antes de planejar importer, feature builder ou novo baseline.

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
- Qualquer coleta adicional deve respeitar checkpoint, baixo volume, delays e validacao operacional.
- Nao implementar importer H8 sem aprovacao explicita.
- Nao alterar schema para H8 sem aprovacao explicita do CTO/Data Engineer.

---

## Proximos Passos

- [ ] Decidir se sera feita nova coleta controlada para os 9 `graph.json` faltantes.
- [ ] Definir politica de tratamento para partidas sem `graph.json`.
- [ ] Validar estrutura conjunta de `graph` e `shotmap` para desenho futuro de importer.
- [ ] Acionar Data Engineer / Database para avaliar importer futuro de `graph` e `shotmap`.
- [ ] Acionar CTO se houver necessidade de nova arquitetura de armazenamento/importacao.
- [ ] So depois definir plano Quant para H8.

---

## Status

EM EXECUCAO - SHOTMAP AUDITADO COM 380/380 PARTIDAS IMPORTAVEIS COBERTAS; GRAPH AUDITADO COM 371/380 PARTIDAS IMPORTAVEIS COBERTAS E 9 FALTANTES; H8 SEGUE COMO FRENTE ATIVA, SEM IMPORTER/FEATURES/BASELINE AUTORIZADOS AINDA.
