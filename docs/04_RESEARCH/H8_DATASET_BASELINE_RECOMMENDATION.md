# H8 DATASET AND BASELINE RECOMMENDATION

## Status

Documento metodologico Quant Research.

Nao contem codigo.

Nao cria dataset.

Nao cria modelo.

Nao executa baseline.

Nao altera PostgreSQL, schema, importer, crawler ou dados brutos.

---

## 1. Objetivo

Revisar metodologicamente o Feature Builder H8 V1 e definir se o projeto deve avançar para Dataset H8 V1 e Baseline H8 controlado.

Este documento consolida:

- revisao anti-leakage;
- decisao sobre avanço ou bloqueio;
- features recomendadas;
- tratamento de nulos e `known_missing`;
- riscos metodologicos;
- proposta de Dataset H8;
- proposta de Baseline H8;
- criterios de aceite para proxima tarefa Codex.

---

## 2. Fontes e Artefatos Revisados

Documentos:

- `docs/04_RESEARCH/H8_INITIAL_STATISTICAL_VALIDATION_RESULTS.md`
- `docs/04_RESEARCH/H8_FEATURE_BUILDER_SPEC.md`
- `docs/04_RESEARCH/H8_FEATURE_CATALOG_V1.md`

Implementacao e artefatos:

- `Analytics/FeatureBuilder/h8_feature_builder_v1.py`
- `data/processed/features/h8_features_v1.csv`
- `data/processed/features/h8_features_v1_metadata.json`
- `data/processed/features/h8_features_v1_validation_report.json`
- `data/processed/datasets/late_goal_dataset_v1.csv`

---

## 3. Estado Atual H8

A validacao estatistica inicial H8 foi executada usando registros com `minute <= cutoff` para construir features e `target_late_goal_75` como target.

Resumo da validacao:

- 36 combinacoes cutoff-feature avaliadas.
- 2 classificadas como MANTER.
- 27 classificadas como OBSERVAR.
- 7 classificadas como DESCARTAR.
- 0 classificadas como NAO TESTAVEL.

Features MANTER:

- `momentum_trend_last_10m` no cutoff 60.
- `shots_last_10m` no cutoff 60.

Melhor feature individual:

- `momentum_trend_last_10m` no cutoff 60.
- p-value: 0.0194.
- efeito maximo: 13.0 p.p.

Interpretacao Quant:

- H8 possui sinal exploratorio real.
- O sinal mais forte apareceu no cutoff 60, sugerindo valor operacional por antecedencia.
- Graph e Shotmap devem seguir separados na interpretacao e na auditoria.

---

## 4. Revisao do Feature Builder H8 V1

### 4.1 Grain

Grain aprovado:

```text
1 linha por match_id + cutoff_minute
```

Cutoffs gerados:

- 60
- 65
- 70
- 75

Resultado validado:

- linhas geradas: 1520.
- partidas unicas: 380.
- cutoffs presentes: 60, 65, 70, 75.
- cada cutoff possui 380 partidas.

Decisao Quant:

- Grain correto para Dataset H8 e Baseline H8 multi-cutoff controlado.

### 4.2 Cobertura

Graph:

- disponivel em 379 partidas.
- 1516 linhas com Graph disponivel.
- `event_id 12437015` conhecido como missing Graph.

Shotmap:

- disponivel em 380 partidas.
- 1520 linhas com Shotmap disponivel.

Decisao Quant:

- Cobertura suficiente para avancar.
- Ressalva Graph deve permanecer documentada e tratada explicitamente.

### 4.3 Whitelist

Features H8 V1 presentes na whitelist:

H8-A Graph:

- `momentum_last_5m_avg`
- `momentum_last_10m_avg`
- `momentum_trend_last_10m`
- `momentum_sum_until_cutoff`

H8-B Shotmap:

- `xg_last_5m`
- `xg_last_10m`
- `shots_last_5m`
- `shots_last_10m`
- `xg_sum_until_cutoff`

Decisao Quant:

- Whitelist adequada para Dataset H8 V1.
- Nenhuma feature fora da whitelist deve entrar em baseline H8 V1.

---

## 5. Revisao Anti-Leakage

O validation report do Feature Builder H8 V1 indica:

- `uses_only_minute_lte_cutoff = true`.
- `contains_target_columns = false`.
- `contains_full_time_score_columns = false`.
- `graph_and_shotmap_separated = true`.
- `whitelist_enforced = true`.

Conclusao:

- O Feature Builder H8 V1 respeita as regras centrais anti-leakage.

Ressalva metodologica:

- O feature set H8 nao possui target por design.
- Join com `target_late_goal_75` deve ser explicito e auditado no Dataset H8 V1.

Controles obrigatorios no proximo dataset:

1. `target_late_goal_75` so pode entrar como target, nunca em `X`.
2. `late_goal`, `goal_after`, `target`, `score final` e colunas equivalentes devem ser bloqueadas em features.
3. Features devem permanecer calculadas apenas com `minute <= cutoff`.
4. Para cada cutoff, a interpretacao deve deixar claro que o target e gol apos 75, nao gol apos o cutoff, salvo decisao metodologica futura diferente.

---

## 6. Decisao: Avancar ou Bloquear

Decisao Quant:

```text
APROVADO COM RESSALVAS PARA DATASET H8 V1
APROVADO COM RESSALVAS PARA PLANO DE BASELINE H8 CONTROLADO
```

Nao aprovado ainda para:

- producao;
- backtesting financeiro;
- automacao operacional;
- sistema decisorio.

Justificativa:

- H8 apresentou sinal estatistico exploratorio real.
- Feature Builder H8 V1 esta auditavel e passou nos checks anti-leakage.
- A cobertura e suficiente, com apenas 1 partida known_missing para Graph.
- O proximo passo natural e criar Dataset H8 V1 com join explicito de target e preparar baseline controlado.

---

## 7. Features Recomendadas para Dataset H8 V1

### 7.1 Recomendacao principal

Usar conjunto restrito:

```text
MANTER + OBSERVAR selecionadas
```

Nao usar apenas MANTER, porque isso deixaria o dataset restrito demais a duas features no cutoff 60.

Nao usar todas as OBSERVAR indiscriminadamente no primeiro baseline se o objetivo for evitar excesso de dimensionalidade.

### 7.2 Features obrigatorias no Dataset H8 V1

Graph:

- `momentum_trend_last_10m`
- `momentum_last_5m_avg`
- `momentum_last_10m_avg`

Shotmap:

- `shots_last_10m`
- `xg_last_10m`
- `xg_sum_until_cutoff`

### 7.3 Features opcionais para auditoria ou baseline expandido

Graph:

- `momentum_sum_until_cutoff`

Shotmap:

- `xg_last_5m`
- `shots_last_5m`

### 7.4 Features a evitar no primeiro Baseline H8

Evitar como preditores principais no primeiro baseline:

- features classificadas como DESCARTAR na maioria dos cutoffs;
- features com efeito fraco e baixa estabilidade.

Observacao:

- Nao remover fisicamente do dataset se ja estiverem no `h8_features_v1`; apenas controlar via whitelist no baseline.

---

## 8. Tratamento de `event_id 12437015` sem Graph

Regra recomendada:

- manter a partida no Dataset H8 V1;
- preservar `graph_known_missing = 1`;
- manter features Graph como nulas para esta partida;
- manter features Shotmap normalmente;
- nao imputar Graph antes do split;
- qualquer imputacao futura deve ser fitada somente no treino.

Para validacao estatistica:

- excluir a linha apenas das analises que dependem diretamente de Graph;
- manter nas analises Shotmap.

Para baseline H8:

- manter a linha no experimento principal;
- imputar Graph nulo usando estrategia fitada no treino ou usar pipeline capaz de lidar com nulos;
- reportar impacto de `graph_known_missing`.

Nao permitido:

- remover a partida silenciosamente;
- preencher Graph com 0 sem registrar;
- usar informacao do target para imputar.

---

## 9. Tratamento de Features Graph Nulas

Causas esperadas:

- Graph indisponivel para known_missing.
- Possivel janela sem pontos Graph, se ocorrer em alguma partida/cutoff.

Regra metodologica:

- nulos Graph devem ser preservados no feature set base;
- imputacao so deve ocorrer em etapa de dataset/modelagem;
- imputador deve ser ajustado somente no treino.

Recomendacao para Dataset H8 V1:

- incluir contadores de cobertura ja existentes:
  - `graph_available`
  - `graph_known_missing`
  - `graph_points_until_cutoff`
  - `graph_points_last_5m`
  - `graph_points_last_10m`

Recomendacao para Baseline H8:

- imputar Graph nulo com mediana do treino por feature;
- manter `graph_known_missing` apenas como coluna de auditoria, nao como feature preditiva no primeiro baseline;
- executar analise de sensibilidade removendo `event_id 12437015`, se autorizado.

---

## 10. Tratamento de Shotmap Zero

Regra:

- se nao houver finalizacao na janela, features de contagem devem ser 0;
- features de xG da janela devem ser 0;
- isso nao e missing, e sim ausencia real de finalizacoes.

Exemplos:

- `shots_last_5m = 0` quando nao houve finalizacao nos ultimos 5 minutos antes do cutoff.
- `xg_last_5m = 0` quando nao houve finalizacao nessa janela.

Nao imputar zeros de Shotmap.

Nao tratar zeros como nulos.

---

## 11. Proposta de Dataset H8 V1

Arquivo esperado:

- `data/processed/datasets/h8_dataset_v1.csv`
- `data/processed/datasets/h8_dataset_v1.parquet`
- `data/processed/datasets/h8_dataset_v1_metadata.json`
- `data/processed/datasets/h8_dataset_v1_validation_report.json`

Grain:

```text
1 linha por match_id + cutoff_minute
```

Linhas esperadas:

```text
380 partidas x 4 cutoffs = 1520 linhas
```

Fonte de features:

- `data/processed/features/h8_features_v1.csv`

Fonte de target:

- `data/processed/datasets/late_goal_dataset_v1.csv`

Target oficial:

- `target_late_goal_75`

Colunas obrigatorias:

Identificacao:

- `match_id`
- `sofascore_event_id`
- `league`
- `season`
- `match_date`
- `home_team`
- `away_team`
- `cutoff_minute`

Cobertura:

- `graph_available`
- `graph_known_missing`
- `shotmap_available`
- `graph_points_until_cutoff`
- `graph_points_last_5m`
- `graph_points_last_10m`
- `shots_until_cutoff`

Features H8:

- `momentum_last_5m_avg`
- `momentum_last_10m_avg`
- `momentum_trend_last_10m`
- `momentum_sum_until_cutoff`
- `xg_last_5m`
- `xg_last_10m`
- `shots_last_5m`
- `shots_last_10m`
- `xg_sum_until_cutoff`

Target:

- `target_late_goal_75`

Observacao importante:

- Como `target_late_goal_75` e fixo por partida, ele sera repetido nos quatro cutoffs da mesma partida.
- Em baseline multi-cutoff, o split temporal deve ser feito por `match_id`, nao por linha, para evitar a mesma partida em splits diferentes.

---

## 12. Proposta de Baseline H8 Controlado

### 12.1 Tipo

Baseline H8 inicial:

- In-Game H8 Only.

Nao misturar ainda com:

- H3/H4 pre-jogo;
- H6/H9 eventos/placar;
- H1/H2;
- H8 features fora da whitelist.

### 12.2 Target

Target:

- `target_late_goal_75`.

Ressalva:

- Para cutoffs 60/65/70, o target continua sendo gol apos 75, nao gol apos o cutoff.
- Isso significa que os cutoffs medem antecedencia operacional para o mesmo evento tardio.

### 12.3 Cutoffs

Primeiro baseline H8 recomendado:

- avaliar cutoffs separadamente: 60, 65, 70, 75.

Nao recomendado no primeiro baseline:

- treinar um unico modelo misturando todos os cutoffs.

Motivo:

- misturar cutoffs aumenta dependencia entre linhas da mesma partida e pode inflar amostra artificialmente.

Desenho recomendado:

- Baseline H8-60.
- Baseline H8-65.
- Baseline H8-70.
- Baseline H8-75.

Cada um com 380 linhas, uma por partida.

### 12.4 Features permitidas por baseline

Baseline H8 restrito inicial:

- `momentum_trend_last_10m`
- `shots_last_10m`
- `momentum_last_5m_avg`
- `xg_last_10m`
- `xg_sum_until_cutoff`

Baseline H8 expandido, somente se aprovado:

- adicionar `momentum_last_10m_avg`
- adicionar `momentum_sum_until_cutoff`
- adicionar `xg_last_5m`
- adicionar `shots_last_5m`

Recomendacao Quant:

- comecar pelo baseline restrito para reduzir dimensionalidade e overfitting.

### 12.5 Split temporal

Split:

- 60% treino.
- 20% validacao.
- 20% teste.

Regra:

- ordenar por `match_date`.
- split por `match_id`.
- sem shuffle.
- sem stratification.
- sem balanceamento artificial.

Com 380 partidas:

- treino: 228.
- validacao: 76.
- teste: 76.

Se cutoffs forem avaliados separadamente:

- cada cutoff deve usar a mesma lista de `match_id` em treino/validacao/teste.

### 12.6 Baseline nulo

Baseline nulo obrigatorio:

- probabilidade constante igual a prevalencia do target no treino.

Calculo:

- feito por cutoff/modelo, mas a prevalencia tende a ser igual se a amostra de partidas for a mesma.

Comparar modelo vs nulo em:

- ROC-AUC;
- PR-AUC;
- Brier Score;
- Log Loss;
- Lift@Top20%.

### 12.7 Metricas obrigatorias

Metricas principais:

- ROC-AUC Test.
- PR-AUC Test.

Metricas secundarias:

- Brier Score.
- Log Loss.
- Lift@Top20%.
- Calibration by bins.

Comparacoes obrigatorias:

- modelo vs baseline nulo;
- cutoff 60 vs 65 vs 70 vs 75;
- Graph-only vs Shotmap-only, se aprovado;
- feature importance apenas como diagnostico, sem interpretacao causal.

### 12.8 Criterios minimos de aprovacao

O baseline H8 so deve ser aprovado se, no teste temporal:

1. `ROC-AUC Test > 0.55`.
2. `PR-AUC Test > prevalence_test + 0.03`.
3. Brier Score do modelo <= Brier Score do baseline nulo, ou ressalva explicita.
4. Log Loss do modelo <= Log Loss do baseline nulo, ou ressalva explicita.
5. Nenhuma feature proibida foi usada.
6. Split temporal por match_id foi respeitado.
7. Imputacao foi fitada apenas no treino.
8. Cada cutoff foi avaliado separadamente.

Se ROC/PR falharem:

- status: `NAO APROVADO`.

Se ROC/PR passarem mas Brier/Log Loss piorarem:

- status: `APTO COM RESSALVAS`.

Se todos passarem:

- status: `APROVADO`.

---

## 13. Riscos Metodologicos

### Risco 1 - Target fixo por partida em multiplos cutoffs

Como o target e repetido para 60/65/70/75, misturar cutoffs no mesmo treino cria dependencia entre linhas.

Mitigacao:

- avaliar cada cutoff separadamente no primeiro baseline H8.

### Risco 2 - Sinal exploratorio univariado nao garante ganho multivariado

A validacao H8 inicial foi univariada.

Mitigacao:

- usar baseline restrito e simples;
- nao interpretar features como causalidade;
- comparar contra baseline nulo.

### Risco 3 - Graph momentum sem direcionalidade de time

O validation report alerta que o feature set e match-level e o sinal do momentum foi preservado como importado.

Mitigacao:

- nao inverter sinal sem nova especificacao;
- tratar Graph como momentum global/importado;
- documentar interpretacao.

### Risco 4 - known_missing Graph

Uma partida sem Graph pode afetar modelos com features Graph.

Mitigacao:

- manter partida;
- imputar apenas apos split;
- reportar impacto.

### Risco 5 - Overfitting por amostra pequena

Cada cutoff tem 380 partidas.

Mitigacao:

- modelo simples;
- poucas features;
- sem busca extensa de hiperparametros;
- teste usado apenas uma vez.

---

## 14. Criterios de Aceite para Proximo Codex Developer

A proxima tarefa Codex so deve ser autorizada se PM/CTO aprovarem.

### 14.1 Dataset H8 V1

Codex deve produzir:

- `data/processed/datasets/h8_dataset_v1.csv`
- `data/processed/datasets/h8_dataset_v1.parquet`
- `data/processed/datasets/h8_dataset_v1_metadata.json`
- `data/processed/datasets/h8_dataset_v1_validation_report.json`

Criterios de aceite:

- 1520 linhas.
- 380 partidas unicas.
- cutoffs 60/65/70/75 presentes.
- 380 linhas por cutoff.
- target `target_late_goal_75` anexado corretamente.
- nenhuma duplicata `match_id + cutoff_minute`.
- nenhuma feature fora da whitelist H8.
- nenhuma coluna target-derived em `X`.
- Graph known_missing preservado para `12437015`.
- Shotmap zeros preservados como zeros, nao nulos.
- validation report com status `APTO` ou `APTO COM RESSALVAS`.

### 14.2 Baseline H8

Somente apos Dataset H8 V1 aprovado.

Criterios de aceite:

- cutoffs avaliados separadamente.
- split temporal por `match_id`.
- mesma lista de partidas em treino/validacao/teste para todos os cutoffs.
- baseline nulo reportado.
- metricas por cutoff.
- comparacao com baseline nulo.
- comparacao entre cutoffs.
- Brier e Log Loss reportados.
- Lift@Top20% reportado.
- Calibration by bins reportada.
- relatorio final em `docs/04_RESEARCH/BASELINE_H8_RESULTS.md`.

Restrições:

- nao criar producao;
- nao executar backtesting;
- nao alterar PostgreSQL;
- nao alterar schema;
- nao alterar importer;
- nao alterar crawler;
- nao alterar dados brutos;
- nao usar dados pos-cutoff;
- nao usar features fora da whitelist H8 aprovada.

---

## 15. Recomendacao Final

Decisao Quant:

```text
AVANCAR PARA DATASET H8 V1
```

Com ressalvas:

- Baseline H8 so deve ocorrer apos Dataset H8 V1 aprovado.
- Primeiro baseline H8 deve avaliar cutoffs separadamente.
- Comecar com baseline restrito, usando as features de maior valor esperado.
- Nao misturar H8 com H3/H4/H6/H9 ainda.
- Nao avancar para backtesting ou producao antes de criterios minimos em teste temporal.

Proxima etapa recomendada:

1. PM aprovar Dataset H8 V1.
2. CTO revisar escopo tecnico.
3. Codex implementar Dataset H8 V1 com join explicito de target.
4. Quant revisar validation report.
5. Apenas depois planejar/autorizar Baseline H8.
