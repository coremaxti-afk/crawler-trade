# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar o primeiro conjunto mínimo de features candidatas do LateGoalResearch, planejar e executar de forma controlada o primeiro baseline exploratório, sem iniciar backtesting ou produção.

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

---

## Estado Atual

Documento de features aprovado:

- `docs/04_RESEARCH/FEATURE_CANDIDATE_SET_V1.md`

Plano de baseline:

- `docs/04_RESEARCH/BASELINE_EXPERIMENT_PLAN.md`

Especificação operacional:

- `docs/04_RESEARCH/BASELINE_IMPLEMENTATION_SPEC.md`

Resultado do baseline:

- `docs/04_RESEARCH/BASELINE_PREMATCH_H3_H4_RESULTS.md`

Status do Baseline 1A:

- Operacional: APTO COM RESSALVAS.
- Quantitativo: NAO APROVADO.
- Decisão Quant: não avançar para backtesting, produção ou sistema decisório.

---

## Resultado Quantitativo do Baseline 1A

Dataset:

- 380 partidas.
- Split temporal: 228 treino / 76 validação / 76 teste.
- Target: `target_late_goal_75`.
- Features finais em `X`: 12.

Teste:

- ROC-AUC Test: 0.4910.
- PR-AUC Test: 0.5364.
- Prevalência Test: 0.5263.
- PR-AUC mínimo exigido: 0.5563.
- Brier modelo vs baseline nulo: piorou +0.0089.
- Log Loss modelo vs baseline nulo: piorou +0.0180.

Critérios:

- ROC-AUC Test > 0.55: FALHOU.
- PR-AUC Test > prevalence_test + 0.03: FALHOU.

Interpretação:

- O ganho em treino não sustentou em validação/teste.
- O baseline nulo foi superior em qualidade probabilística no teste.
- O artefato permanece útil como referência exploratória controlada, mas não autoriza avanço metodológico.

---

## Status das Hipóteses

- H1 — BLOQUEADA por data leakage.
- H2 — BLOQUEADA por data leakage.
- H3 — MANTER COMO CANDIDATA, mas Baseline 1A Pre-Match não aprovou no teste temporal.
- H4 — MANTER COMO CANDIDATA FORTE, mas Baseline 1A Pre-Match não aprovou no teste temporal.
- H5 — NÃO VALIDADA.
- H6 — VALIDADA INICIALMENTE.
- H7 — NÃO VALIDADA COMO HIPÓTESE INDEPENDENTE.
- H8 — BLOQUEADA/PENDENTE de graph/momentum.
- H9 — VALIDADA INICIALMENTE.

---

## Conjunto Mínimo de Features Candidatas V1

### Pré-jogo

- `goals_for_avg_last_3`
- `goals_for_avg_last_10`
- `shots_on_target_for_avg_last_5`
- `shots_against_avg_last_5`
- `shots_on_target_against_avg_last_5`
- `big_chances_against_avg_last_5`

### In-game

- `score_diff_home_until_cutoff`
- `score_state_group`
- `cards_until_cutoff`
- `substitutions_until_cutoff`

---

## Restrições Ativas

- Não avançar o Baseline 1A para backtesting.
- Não usar o Baseline 1A em produção.
- Não transformar o Baseline 1A em sistema decisório.
- Não usar features bloqueadas.
- Manter separação entre bloco pré-jogo e bloco in-game.
- Não usar estatísticas finais da própria partida como preditores.
- Não usar xG/xGA/forecast sem comprovação temporal segura.
- Qualquer nova iteração de baseline precisa de autorização do PM/CTO.

---

## Próxima Frente Oficial

A definir pelo PM.

Opções candidatas:

1. Revisar formulação do baseline pré-jogo.
2. Avaliar Baseline 1B com diferenças home-away, se PM/CTO autorizarem.
3. Planejar baseline in-game separado com H6/H9.
4. Aguardar ampliação multi-temporada antes de nova modelagem.

---

## Próximos Passos

- [ ] PM decidir a próxima frente oficial.
- [ ] Se houver nova iteração, CTO revisar escopo técnico antes de Codex.
- [ ] Quant Research desenhar novo plano metodológico antes de implementação.
- [ ] Manter backtesting e produção bloqueados.

---

## Status

EM EXECUÇÃO — BASELINE 1A EXECUTADO; RESULTADO QUANTITATIVO NAO APROVADO; PROXIMA FRENTE DEPENDE DO PM.
