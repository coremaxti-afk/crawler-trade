# PROJECT STATUS

## Etapas do Projeto

1. Organizacao
2. Inventario das Fontes
3. Coleta Bruta
4. Banco de Dados
5. Integracao Multi-Fonte
6. Catalogo de Features
7. Engenharia de Features
8. Definicao do Alvo
9. Dataset Analitico
10. Pesquisa Quantitativa
11. Modelagem
12. Producao

---

## Concluido

- Estrutura documental do projeto consolidada.
- Governanca de agentes criada em `docs/00_AGENTS/AGENT_COORDINATION.md`.
- Perfil do PM criado em `docs/00_AGENTS/PM_PROFILE.md`.
- Documento base de hipoteses criado em `docs/04_RESEARCH/ACTIVE/LATE_GOAL_HYPOTHESES.md`.
- Understat integrado.
- FotMob integrado parcialmente.
- EPL 2024/2025 descoberta via SofaScore com 381 partidas no inventory.
- Match Mapping criado.
- PostgreSQL configurado.
- SQLAlchemy configurado.
- Tabelas `match_mapping`, `matches_master`, `match_statistics`, `match_incidents` e `match_graph` criadas.
- Coleta SofaScore core/full auditada com 380 partidas importaveis.
- `sofascore_importer.py` implementado no commit `84e641f`.
- PostgreSQL populado com 380 partidas SofaScore importaveis.
- Idempotencia do importer validada.
- Validacao leve de qualidade concluida com status: APTO COM RESSALVAS.
- Dataset Builder V1 implementado no commit `1a1404e09079f2a1a7958ae948fefdc667872a50`.
- Dataset Analitico V1 gerado com 380 linhas e status APTO COM RESSALVAS.
- Target Audit concluido: `target_late_goal_75` com 189 positivos e 191 negativos.
- Validacao Estatistica Inicial H6/H9 concluida e revisada pelo Quant Research.
- Validacao H1/H2 bloqueada por risco confirmado de data leakage.
- Feature set historico pre-jogo `historical_prematch_features_v1` criado e validado para H3/H4.
- Validacao Estatistica H3/H4 concluida.
- `FEATURE_CANDIDATE_SET_V1.md` aprovado.
- `BASELINE_EXPERIMENT_PLAN.md` aprovado.
- `BASELINE_IMPLEMENTATION_SPEC.md` aprovado.
- Baseline 1A Pre-Match H3/H4 implementado, executado e revisado.
- Baseline 1A registrado como operacionalmente apto, mas quantitativamente NAO APROVADO.
- `BASELINE_INGAME_IMPLEMENTATION_SPEC.md` produzido e aprovado para implementacao controlada.

---

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
- `match_graph` ainda nao possui dados coletados/importados.

---

## Dataset Analitico V1

Status:

- Gerado.
- APTO COM RESSALVAS.

Script:

- `LateGoalResearch/Analytics/DatasetBuilder/dataset_builder_v1.py`

Artefatos locais:

- `data/processed/datasets/late_goal_dataset_v1.csv`
- `data/processed/datasets/late_goal_dataset_v1.parquet`
- `data/processed/datasets/late_goal_dataset_v1_metadata.json`
- `data/processed/datasets/late_goal_dataset_v1_validation_report.json`

Resumo:

- Linhas: 380.
- Grain: 1 linha por partida.
- Target principal: `target_late_goal_75`.
- Alias operacional: `has_late_goal`.
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

- H1 — BLOQUEADA por data leakage.
- H2 — BLOQUEADA por data leakage.
- H3 — MANTER COMO CANDIDATA, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H4 — MANTER COMO CANDIDATA FORTE, mas Baseline 1A Pre-Match nao aprovou no teste temporal.
- H5 — NAO VALIDADA.
- H6 — VALIDADA INICIALMENTE e autorizada para Baseline In-Game V1.
- H7 — NAO VALIDADA COMO HIPOTESE INDEPENDENTE.
- H8 — BLOQUEADA/PENDENTE de graph/momentum.
- H9 — VALIDADA INICIALMENTE e autorizada para Baseline In-Game V1.

---

## Baseline 1A — Pre-Match H3/H4

Documento:

- `docs/04_RESEARCH/BASELINE_PREMATCH_H3_H4_RESULTS.md`

Status:

- Operacional: APTO COM RESSALVAS.
- Quantitativo: NAO APROVADO.
- Decisao: nao avancar para backtesting, producao ou sistema decisorio.

Resultado no teste:

- ROC-AUC Test: 0.4910.
- PR-AUC Test: 0.5364.
- Prevalencia Test: 0.5263.
- PR-AUC minimo exigido: 0.5563.
- Brier modelo vs baseline nulo: piorou +0.0089.
- Log Loss modelo vs baseline nulo: piorou +0.0180.

Interpretacao:

- O pipeline foi validado.
- A implementacao respeitou split temporal, imputacao e auditoria anti-leakage.
- As features pre-jogo H3/H4 isoladas nao sustentaram um baseline preditivo util no teste temporal.

---

## Baseline In-Game V1 — H6/H9

Documento aprovado:

- `docs/04_RESEARCH/BASELINE_INGAME_IMPLEMENTATION_SPEC.md`

Commit:

- `31db699a2e80c2ed11fed4672db8a785ce2b65b2`

Status:

- APROVADO para implementacao controlada.

Configuracao:

- Target: `target_late_goal_75`.
- Cutoff: 75 minutos.
- Tipo: in-game snapshot.

Features permitidas:

- `score_diff_home_until_cutoff`
- `score_state_group`
- `cards_until_cutoff`
- `substitutions_until_cutoff`

Proibido:

- H1/H2/H8.
- xG/xGA/forecast.
- eventos apos cutoff.
- target-derived features.
- estatisticas full-match.
- producao, automacao operacional e backtesting financeiro.

Plano futuro:

- Baseline In-Game V2 com cutoffs 60, 65, 70 e 75 para medir trade-off entre antecedencia operacional e ganho informacional.

---

## Em Andamento

### Implementacao Controlada do Baseline In-Game V1

Proximo agente:

- Codex Developer.

Objetivo:

Executar o Baseline In-Game V1 conforme `BASELINE_INGAME_IMPLEMENTATION_SPEC.md`, gerar relatorio completo e retornar para revisao do Quant Research e PM.

---

## Proximas Etapas

1. Codex implementar o Baseline In-Game V1.
2. Gerar relatorio com metricas train/validation/test.
3. Comparar contra baseline nulo.
4. Auditar features utilizadas em X.
5. Enviar resultado ao Quant Research para revisao.
6. Manter backtesting e producao bloqueados.

---

## Descobertas Recentes

- H3/H4 pre-jogo isoladas nao foram suficientes no Baseline 1A.
- H6/H9 sao a frente in-game prioritaria por terem apresentado sinal estatistico inicial.
- O projeto deve tratar o Baseline 1A como referencia exploratoria, nao como modelo candidato.
- O proximo teste controlado sera o Baseline In-Game V1 no cutoff 75.
- Nenhum backtesting ou producao foi iniciado.
- `match_graph` segue pendente porque ainda nao ha `graph.json` coletado.
