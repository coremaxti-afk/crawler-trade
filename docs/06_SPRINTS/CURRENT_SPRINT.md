# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar o primeiro conjunto mínimo de features candidatas do LateGoalResearch e preparar a transição controlada para planejamento de baseline, sem iniciar modelagem ou backtesting.

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

---

## Estado Atual

Documento aprovado:

- `docs/04_RESEARCH/FEATURE_CANDIDATE_SET_V1.md`

Commit:

- `2e94f3dc2b00480bbbe5582f7b9fa91d4e533f14`

Status:

- APROVADO pelo PM.

---

## Status das Hipóteses

- H1 — BLOQUEADA por data leakage.
- H2 — BLOQUEADA por data leakage.
- H3 — MANTER COMO CANDIDATA.
- H4 — MANTER COMO CANDIDATA FORTE.
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

- Não iniciar modelagem ainda.
- Não executar baseline sem plano aprovado.
- Não executar backtesting.
- Não usar features bloqueadas.
- Manter separação entre bloco pré-jogo e bloco in-game.
- Não usar estatísticas finais da própria partida como preditores.
- Não usar xG/xGA/forecast sem comprovação temporal segura.

---

## Próxima Frente Oficial

Baseline Preparation.

Objetivo:

Produzir um plano formal de experimento antes de qualquer treino ou baseline executável.

Documento esperado:

- `docs/04_RESEARCH/BASELINE_EXPERIMENT_PLAN.md`

Conteúdo esperado:

- dataset a ser usado;
- features permitidas;
- features proibidas;
- separação pré-jogo vs in-game;
- split temporal;
- métricas;
- critérios de sucesso;
- regras anti-leakage;
- escopo do primeiro baseline.

---

## Próximos Passos

- [ ] Acionar CTO para revisar a transição para baseline.
- [ ] Acionar Quant Research para desenhar `BASELINE_EXPERIMENT_PLAN.md`.
- [ ] Só após aprovação do plano, preparar tarefa controlada para Codex.
- [ ] Manter modelagem bloqueada até aprovação formal do plano.

---

## Status

EM EXECUÇÃO — FEATURE_CANDIDATE_SET_V1 APROVADO; PRÓXIMA FRENTE: BASELINE PREPARATION.
