# CURRENT SPRINT

## Sprint Atual

Objetivo:

Encerrar a iteração de baselines sem graph/momentum e abrir a frente de coleta/análise de graph para testar H8 — Momentum e Pressão Temporal.

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

---

## Resultado dos Baselines Sem Graph

### Baseline 1A — Pre-Match H3/H4

Documento:

- `docs/04_RESEARCH/BASELINE_PREMATCH_H3_H4_RESULTS.md`

Status:

- Operacional: APTO COM RESSALVAS.
- Quantitativo: NÃO APROVADO.
- Decisão: não avançar para backtesting, produção ou sistema decisório.

Métricas no teste:

- ROC-AUC Test: 0.4910.
- PR-AUC Test: 0.5364.
- Prevalência Test: 0.5263.
- PR-AUC mínimo exigido: 0.5563.

### Baseline In-Game V1 — H6/H9

Documento:

- `docs/04_RESEARCH/BASELINE_INGAME_V1_RESULTS.md`

Status:

- Operacional: APTO COM RESSALVAS.
- Quantitativo: NÃO APROVADO.
- Decisão: não avançar para backtesting, produção ou sistema decisório.

Métricas no teste:

- ROC-AUC Test: 0.5250.
- PR-AUC Test: 0.5541.
- Prevalência Test: 0.5263.
- PR-AUC requerido: 0.5563.
- Brier modelo: 0.2525 vs nulo 0.2505.
- Log Loss modelo: 0.6983 vs nulo 0.6942.

Interpretação:

- O In-Game V1 melhorou em relação ao Pre-Match, mas ainda não atingiu os critérios mínimos.
- O PR-AUC ficou próximo do mínimo, mas falhou por pequena margem.
- A qualidade probabilística piorou contra o baseline nulo.
- Os baselines atuais servem como benchmarks exploratórios, não como modelos candidatos.

---

## Decisão PM

A iteração de baselines sem graph/momentum está encerrada.

Motivo:

- Os baselines sem graph não foram aprovados quantitativamente.
- A hipótese do PM é que dados ao vivo/momentum podem ser mais relevantes para gols tardios.
- A próxima frente oficial passa a ser buscar/coletar graph/momentum para testar H8.

---

## Status das Hipóteses

- H1 — BLOQUEADA por data leakage.
- H2 — BLOQUEADA por data leakage.
- H3 — MANTER COMO CANDIDATA, mas Baseline 1A Pre-Match não aprovou no teste temporal.
- H4 — MANTER COMO CANDIDATA FORTE, mas Baseline 1A Pre-Match não aprovou no teste temporal.
- H5 — NÃO VALIDADA.
- H6 — VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph não aprovou quantitativamente.
- H7 — NÃO VALIDADA COMO HIPÓTESE INDEPENDENTE.
- H8 — PRÓXIMA FRENTE: graph/momentum.
- H9 — VALIDADA INICIALMENTE, mas Baseline In-Game V1 sem graph não aprovou quantitativamente.

---

## Próxima Frente Oficial

Graph / Momentum — H8.

Objetivo:

Investigar se dados temporais de pressão/momentum ao vivo melhoram a previsão de gols tardios.

Escopo inicial esperado:

- identificar endpoint/artefato `graph` ou equivalente;
- validar disponibilidade para partidas já coletadas;
- estimar custo em requests;
- definir estratégia segura de coleta;
- documentar estrutura dos dados;
- avaliar como transformar graph/momentum em features sem leakage.

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
- Qualquer coleta graph/momentum deve respeitar checkpoint, baixo volume, delays e validação operacional.

---

## Próximos Passos

- [ ] Acionar Data Acquisition Engineer para avaliar graph/momentum.
- [ ] Identificar endpoint e formato do graph.
- [ ] Executar teste controlado em amostra mínima.
- [ ] Documentar viabilidade operacional.
- [ ] Acionar CTO se houver necessidade de nova arquitetura de armazenamento/importação.
- [ ] Só depois definir plano Quant para H8.

---

## Status

EM EXECUÇÃO — BASELINES SEM GRAPH ENCERRADOS COMO EXPLORATÓRIOS; PRÓXIMA FRENTE: GRAPH/MOMENTUM H8.
