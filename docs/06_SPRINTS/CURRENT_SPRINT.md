# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar a frente H8 com dados temporais de graph/momentum e shotmap, preparando a próxima fase de importação/feature engineering sem iniciar backtesting ou produção.

---

## Concluído

- [x] Criar collectors SofaScore.
- [x] Resolver robustez operacional do HTTP 403 com coleta core.
- [x] Coletar/auditar EPL SofaScore com 381 partidas no inventário.
- [x] Consolidar 380 partidas importáveis.
- [x] Implementar `sofascore_importer.py`.
- [x] Popular PostgreSQL com dados core SofaScore.
- [x] Validar idempotência do importer.
- [x] Validar integridade básica entre `matches_master`, `match_statistics` e `match_incidents`.
- [x] Executar validação leve de qualidade pós-importação.
- [x] Definir metodologia do Dataset Analítico V1.
- [x] Implementar Dataset Builder V1.
- [x] Gerar Dataset Analítico V1.
- [x] Executar Target Audit.
- [x] Validar estatisticamente H6/H9.
- [x] Bloquear H1/H2 por risco confirmado de data leakage.
- [x] Construir feature set histórico pré-jogo H3/H4.
- [x] Validar estatisticamente H3/H4.
- [x] Produzir e aprovar `FEATURE_CANDIDATE_SET_V1.md`.
- [x] Implementar e executar Baseline 1A Pre-Match H3/H4.
- [x] Revisar resultado quantitativo do Baseline 1A.
- [x] Produzir `BASELINE_INGAME_IMPLEMENTATION_SPEC.md`.
- [x] Implementar e executar Baseline In-Game V1.
- [x] Revisar resultado quantitativo do Baseline In-Game V1.
- [x] Encerrar a iteração de baselines sem graph/momentum como exploratória e não aprovada para backtesting/produção.
- [x] Executar discovery controlado de endpoints SofaScore.
- [x] Confirmar endpoint `/graph` como útil para H8.
- [x] Confirmar endpoint `/shotmap` como útil para H8.
- [x] Coletar `graph` com sucesso.

---

## Resultado dos Baselines Sem Graph

### Baseline 1A — Pre-Match H3/H4

Documento:

- `docs/04_RESEARCH/BASELINE_PREMATCH_H3_H4_RESULTS.md`

Status:

- Operacional: APTO COM RESSALVAS.
- Quantitativo: NÃO APROVADO.
- Decisão: não avançar para backtesting, produção ou sistema decisório.

### Baseline In-Game V1 — H6/H9

Documento:

- `docs/04_RESEARCH/BASELINE_INGAME_V1_RESULTS.md`

Status:

- Operacional: APTO COM RESSALVAS.
- Quantitativo: NÃO APROVADO.
- Decisão: não avançar para backtesting, produção ou sistema decisório.

Interpretação:

- O In-Game V1 melhorou em relação ao Pre-Match, mas ainda não atingiu os critérios mínimos.
- Os baselines atuais servem como benchmarks exploratórios, não como modelos candidatos.
- A próxima hipótese prioritária é que dados vivos de momentum/pressão e finalizações possam aumentar o sinal preditivo.

---

## Discovery SofaScore H8

Documentos:

- `docs/03_SOURCES/SOFASCORE/ENDPOINT_DISCOVERY_20260605.md`
- `docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_ENDPOINT.md`

Endpoints úteis confirmados:

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

Complementos possíveis:

- `lineups`
- `average-positions`
- `managers`

Endpoints não recomendados para insistência por tentativa de nomes:

- `/attacks`
- `/dangerous-attacks`
- `/possession`
- `/field-tilt`
- `/pressure`
- `/momentum`
- `/attack-momentum`

Decisão:

- Não insistir em endpoints não confirmados por tentativa de nomes.
- Priorizar H8 com `graph` + `shotmap` + `incidents` + `statistics`.

---

## Estado Atual da Coleta H8

### Graph

Status:

- Coletado com sucesso.

Interpretação:

- `graph` passa a ser o principal artefato temporal de momentum/pressão para H8.
- A próxima etapa será validar cobertura, estrutura e qualidade antes de importar/modelar.

### Shotmap

Status:

- Em coleta.

Interpretação:

- `shotmap` pode fornecer finalizações com minuto, acréscimo, `timeSeconds`, xG, xGOT e coordenadas.
- Pode permitir features como xG acumulado até cutoff, xG recente, volume de chutes e qualidade das chances antes do cutoff.

---

## Status das Hipóteses

- H1 — BLOQUEADA por data leakage.
- H2 — BLOQUEADA por data leakage.
- H3 — MANTER COMO CANDIDATA, mas Baseline 1A Pre-Match não aprovou no teste temporal.
- H4 — MANTER COMO CANDIDATA FORTE, mas Baseline 1A Pre-Match não aprovou no teste temporal.
- H5 — NÃO VALIDADA.
- H6 — VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph não aprovou quantitativamente.
- H7 — NÃO VALIDADA COMO HIPÓTESE INDEPENDENTE.
- H8 — FRENTE ATIVA: graph/momentum + shotmap.
- H9 — VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph não aprovou quantitativamente.

---

## Próxima Frente Oficial

Consolidação da coleta H8.

Objetivo:

Validar a cobertura e a qualidade dos dados `graph` e `shotmap` antes de planejar importer, feature builder ou novo baseline.

---

## Restrições Ativas

- Não avançar nenhum baseline atual para backtesting.
- Não usar nenhum baseline atual em produção.
- Não transformar nenhum baseline atual em sistema decisório.
- Não usar features bloqueadas.
- Não usar estatísticas finais da própria partida como preditores.
- Não usar xG/xGA/forecast sem comprovação temporal segura.
- Não usar eventos após cutoff como features in-game.
- Manter backtesting e produção bloqueados.
- Qualquer coleta adicional deve respeitar checkpoint, baixo volume, delays e validação operacional.

---

## Próximos Passos

- [ ] Finalizar coleta de `shotmap`.
- [ ] Auditar cobertura de `graph` por partida.
- [ ] Auditar cobertura de `shotmap` por partida.
- [ ] Validar estrutura e qualidade dos JSONs coletados.
- [ ] Acionar Data Engineer / Database para avaliar importer futuro de `graph` e `shotmap`.
- [ ] Acionar CTO se houver necessidade de nova arquitetura de armazenamento/importação.
- [ ] Só depois definir plano Quant para H8.

---

## Status

EM EXECUÇÃO — GRAPH COLETADO COM SUCESSO; SHOTMAP EM COLETA; H8 É A FRENTE ATIVA.
