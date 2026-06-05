# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar o primeiro conjunto mínimo de features candidatas do LateGoalResearch, registrar o resultado do Baseline 1A e executar de forma controlada o Baseline In-Game V1, sem iniciar backtesting ou produção.

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
- [x] Produzir `BASELINE_EXPERIMENT_PLAN.md`.
- [x] Produzir e revisar `BASELINE_IMPLEMENTATION_SPEC.md`.
- [x] Implementar e executar Baseline 1A Pre-Match H3/H4.
- [x] Revisar resultado quantitativo do Baseline 1A.
- [x] Produzir `BASELINE_INGAME_IMPLEMENTATION_SPEC.md`.
- [x] Aprovar Baseline In-Game V1 para implementação controlada.

---

## Estado Atual

### Baseline 1A — Pre-Match H3/H4

Resultado:

- Documento: `docs/04_RESEARCH/BASELINE_PREMATCH_H3_H4_RESULTS.md`
- Operacional: APTO COM RESSALVAS.
- Quantitativo: NÃO APROVADO.
- Decisão: não avançar para backtesting, produção ou sistema decisório.

Métricas no teste:

- ROC-AUC Test: 0.4910.
- PR-AUC Test: 0.5364.
- Prevalência Test: 0.5263.
- PR-AUC mínimo exigido: 0.5563.
- Brier modelo vs baseline nulo: piorou +0.0089.
- Log Loss modelo vs baseline nulo: piorou +0.0180.

Interpretação:

- H3/H4 pré-jogo isoladas não sustentaram um baseline preditivo útil no teste temporal.
- O pipeline foi validado, mas o experimento falhou quantitativamente.

### Baseline In-Game V1 — H6/H9

Status:

- Aprovado para implementação controlada.

Documento aprovado:

- `docs/04_RESEARCH/BASELINE_INGAME_IMPLEMENTATION_SPEC.md`

Commit:

- `31db699a2e80c2ed11fed4672db8a785ce2b65b2`

Configuração aprovada:

- Target: `target_late_goal_75`.
- Cutoff: 75 minutos.
- Tipo: in-game snapshot.
- Features permitidas:
  - `score_diff_home_until_cutoff`
  - `score_state_group`
  - `cards_until_cutoff`
  - `substitutions_until_cutoff`

Proibições:

- H1/H2/H8.
- xG/xGA/forecast.
- eventos após cutoff.
- target-derived features.
- estatísticas full-match.
- produção, automação operacional e backtesting financeiro.

Plano futuro documentado:

- Baseline In-Game V2 com cutoffs 60, 65, 70 e 75 para medir trade-off entre antecedência operacional e ganho informacional.

---

## Status das Hipóteses

- H1 — BLOQUEADA por data leakage.
- H2 — BLOQUEADA por data leakage.
- H3 — MANTER COMO CANDIDATA, mas Baseline 1A Pre-Match não aprovou no teste temporal.
- H4 — MANTER COMO CANDIDATA FORTE, mas Baseline 1A Pre-Match não aprovou no teste temporal.
- H5 — NÃO VALIDADA.
- H6 — VALIDADA INICIALMENTE e autorizada para Baseline In-Game V1.
- H7 — NÃO VALIDADA COMO HIPÓTESE INDEPENDENTE.
- H8 — BLOQUEADA/PENDENTE de graph/momentum.
- H9 — VALIDADA INICIALMENTE e autorizada para Baseline In-Game V1.

---

## Restrições Ativas

- Não avançar o Baseline 1A para backtesting.
- Não usar o Baseline 1A em produção.
- Não transformar o Baseline 1A em sistema decisório.
- Não usar features bloqueadas.
- Não usar estatísticas finais da própria partida como preditores.
- Não usar xG/xGA/forecast sem comprovação temporal segura.
- Não usar eventos após cutoff como features in-game.
- Manter backtesting e produção bloqueados.
- Qualquer nova iteração de baseline precisa de autorização do PM/CTO.

---

## Próxima Frente Oficial

Implementação controlada do Baseline In-Game V1.

Próximo agente:

- Codex Developer.

Objetivo:

Executar o Baseline In-Game V1 conforme `BASELINE_INGAME_IMPLEMENTATION_SPEC.md`, gerar relatório completo e retornar para revisão do Quant Research e do PM.

---

## Próximos Passos

- [ ] Acionar Codex para implementar o Baseline In-Game V1.
- [ ] Gerar relatório com métricas train/validation/test.
- [ ] Comparar contra baseline nulo.
- [ ] Auditar features utilizadas em X.
- [ ] Enviar resultado ao Quant Research para revisão.
- [ ] Manter backtesting e produção bloqueados.

---

## Status

EM EXECUÇÃO — BASELINE 1A NÃO APROVADO; BASELINE IN-GAME V1 APROVADO PARA IMPLEMENTAÇÃO CONTROLADA.
