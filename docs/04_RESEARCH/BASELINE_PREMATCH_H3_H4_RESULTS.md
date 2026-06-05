# Baseline 1 Pre-Match H3/H4 Results

Gerado em: 2026-06-05T01:44:41

## Resumo Executivo

Baseline 1A foi executado em rodada controlada com features pre-jogo H3/H4 aprovadas, target `target_late_goal_75`, split temporal 60/20/20 sem shuffle, imputacao por mediana fitada apenas no treino, baseline nulo por prevalencia do treino e modelo treinado de regressao logistica.

Status operacional do relatorio: `APTO COM RESSALVAS`.

Resultado no teste:

- ROC-AUC Test: 0.4910
- PR-AUC Test: 0.5364
- Prevalencia Test: 0.5263
- Criterio ROC-AUC Test > 0.55: False
- Criterio PR-AUC Test > prevalence_test + 0.03: False
- Status dos criterios: NAO APROVADO

## Objetivo

Avaliar se features historicas pre-jogo H3/H4 possuem sinal preditivo minimo para estimar a probabilidade de uma partida ter pelo menos um gol apos 75:00.

## Arquivos de Entrada

- `C:\LateGoalResearch\data\processed\features\historical_prematch_features_v1.csv`
- `C:\LateGoalResearch\data\processed\features\historical_prematch_features_v1_metadata.json`
- `C:\LateGoalResearch\data\processed\features\historical_prematch_features_v1_validation_report.json`
- `C:\LateGoalResearch\data\processed\datasets\late_goal_dataset_v1.csv`
- `C:\LateGoalResearch\data\processed\datasets\late_goal_dataset_v1_metadata.json`
- `C:\LateGoalResearch\data\processed\datasets\late_goal_dataset_v1_validation_report.json`

## Metodologia

- Unidade final: 1 linha por partida.
- Conversao: team-level para match-level, prefixando features do mandante com `home_` e visitante com `away_`.
- Target: `target_late_goal_75`.
- Split: temporal cronologico 60/20/20, sem shuffle.
- Imputacao: mediana fitada apenas no treino e aplicada a validation/test.
- Baseline nulo: probabilidade constante igual a prevalencia do target no treino.
- Modelo treinado: sklearn.pipeline.Pipeline(StandardScaler + LogisticRegression).
- Producao e backtesting financeiro: nao executados.

## Features Usadas

- `home_goals_for_avg_last_3`
- `home_goals_for_avg_last_10`
- `home_shots_on_target_for_avg_last_5`
- `home_shots_against_avg_last_5`
- `home_shots_on_target_against_avg_last_5`
- `home_big_chances_against_avg_last_5`
- `away_goals_for_avg_last_3`
- `away_goals_for_avg_last_10`
- `away_shots_on_target_for_avg_last_5`
- `away_shots_against_avg_last_5`
- `away_shots_on_target_against_avg_last_5`
- `away_big_chances_against_avg_last_5`

## Auditoria Anti-Leakage

- Whitelist oficial prevaleceu sobre blacklist: `true`.
- Total de colunas em X: 12.
- Target utilizado: `target_late_goal_75`.
- Todas as colunas de X vieram da whitelist: `True`.
- Achados do scanner em X: 8 achados tratados por precedencia da whitelist.
- Colunas removidas registradas no manifest: 4.

## Split Temporal

| Split | N | Data inicial | Data final | Pos | Neg | Prevalencia | History zero |
|---|---:|---|---|---:|---:|---:|---:|
| train | 228 | 2024-08-16T19:00:00 | 2025-01-26T16:30:00 | 112 | 116 | 0.4912 | 10 |
| validation | 76 | 2025-01-26T19:00:00 | 2025-04-05T16:30:00 | 37 | 39 | 0.4868 | 0 |
| test | 76 | 2025-04-06T13:00:00 | 2025-05-25T15:00:00 | 40 | 36 | 0.5263 | 0 |

## Observacoes sem Historico

Observacoes sem historico anterior foram mantidas no experimento principal e imputadas conforme regra aprovada.

- Train: 10
- Validation: 0
- Test: 0

## Imputacao

| Feature | Mediana treino | Nulos train antes/depois | Nulos validation antes/depois | Nulos test antes/depois |
|---|---:|---:|---:|---:|
| `home_goals_for_avg_last_3` | 1.3333 | 10/0 | 0/0 | 0/0 |
| `home_goals_for_avg_last_10` | 1.4000 | 10/0 | 0/0 | 0/0 |
| `home_shots_on_target_for_avg_last_5` | 4.6000 | 10/0 | 0/0 | 0/0 |
| `home_shots_against_avg_last_5` | 13.4000 | 10/0 | 0/0 | 0/0 |
| `home_shots_on_target_against_avg_last_5` | 4.4500 | 10/0 | 0/0 | 0/0 |
| `home_big_chances_against_avg_last_5` | 2.5500 | 10/0 | 0/0 | 0/0 |
| `away_goals_for_avg_last_3` | 1.3333 | 10/0 | 0/0 | 0/0 |
| `away_goals_for_avg_last_10` | 1.4000 | 10/0 | 0/0 | 0/0 |
| `away_shots_on_target_for_avg_last_5` | 4.7083 | 10/0 | 0/0 | 0/0 |
| `away_shots_against_avg_last_5` | 12.8000 | 10/0 | 0/0 | 0/0 |
| `away_shots_on_target_against_avg_last_5` | 4.6000 | 10/0 | 0/0 | 0/0 |
| `away_big_chances_against_avg_last_5` | 2.4500 | 10/0 | 0/0 | 0/0 |

## Baseline Nulo

Probabilidade constante aprendida no treino: 0.4912

O baseline nulo foi avaliado em train/validation/test com ROC-AUC, PR-AUC, Brier Score e Log Loss.

## Metricas por Split

| Split | Modelo | N | Pos | Neg | Prev | ROC-AUC | PR-AUC | Brier | Log Loss | Lift@20% |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | Baseline nulo | 228 | 112 | 116 | 0.4912 | 0.5000 | 0.4912 | 0.2499 | 0.6930 | 1.1064 |
| train | Regressao logistica | 228 | 112 | 116 | 0.4912 | 0.6178 | 0.5984 | 0.2406 | 0.6743 | 1.3276 |
| validation | Baseline nulo | 76 | 37 | 39 | 0.4868 | 0.5000 | 0.4868 | 0.2498 | 0.6928 | 1.4122 |
| validation | Regressao logistica | 76 | 37 | 39 | 0.4868 | 0.5191 | 0.5196 | 0.2604 | 0.7161 | 1.2838 |
| test | Baseline nulo | 76 | 40 | 36 | 0.5263 | 0.5000 | 0.5263 | 0.2505 | 0.6942 | 0.9500 |
| test | Regressao logistica | 76 | 40 | 36 | 0.5263 | 0.4910 | 0.5364 | 0.2594 | 0.7122 | 1.1875 |

## Comparacao Modelo vs Baseline Nulo

Valores negativos em Brier/LogLoss indicam melhora probabilistica do modelo contra o baseline nulo.

| Split | Delta Brier modelo-nulo | Delta LogLoss modelo-nulo | Delta ROC-AUC | Delta PR-AUC |
|---|---:|---:|---:|---:|
| train | -0.0093 | -0.0187 | 0.1178 | 0.1072 |
| validation | 0.0105 | 0.0232 | 0.0191 | 0.0328 |
| test | 0.0089 | 0.0180 | -0.0090 | 0.0100 |

## Calibration by Bins

A calibracao por bins esta registrada em `C:\LateGoalResearch\data\processed\reports\baseline_1_prematch_metrics.json` para train, validation e test, tanto para baseline nulo quanto para modelo treinado.

## Lift@Top20%

Lift@Top20% esta reportado na tabela de metricas e detalhado em `C:\LateGoalResearch\data\processed\reports\baseline_1_prematch_metrics.json`.

## Decisao Final

Status dos criterios quantitativos: `NAO APROVADO`.

Status operacional do artefato: `APTO COM RESSALVAS`.

Interpretacao: este resultado e uma primeira execucao controlada para revisao do Quant Research e PM. Nao autoriza producao, automacao operacional, backtesting financeiro ou uso como sistema decisorio.

## Limitacoes

- Amostra de uma unica temporada EPL com teste de aproximadamente 20% das partidas.
- Observacoes nao sao totalmente independentes, pois clubes aparecem repetidamente.
- Modelo simples e exploratorio; nao ha validacao multi-temporada.
- Features H6/H9 in-game continuam fora do Baseline 1.
- Baseline 1B com features diff nao foi executado.
- Nenhuma calibracao operacional ou threshold decisorio foi aprovado.

## Recomendacoes

1. Quant Research deve revisar ROC-AUC Test, PR-AUC Test e comparacao contra baseline nulo.
2. PM deve decidir se o resultado e suficiente para nova iteracao metodologica ou se deve permanecer como referencia exploratoria.
3. Nao avancar para producao nem backtesting financeiro.
4. Considerar validacao temporal mais robusta quando houver mais temporadas.
5. Avaliar Baseline 1B somente se PM/CTO autorizarem explicitamente.

## Artefatos Gerados

- `C:\LateGoalResearch\data\processed\baseline\baseline_1_prematch_dataset.csv`
- `C:\LateGoalResearch\data\processed\baseline\baseline_1_prematch_train.csv`
- `C:\LateGoalResearch\data\processed\baseline\baseline_1_prematch_validation.csv`
- `C:\LateGoalResearch\data\processed\baseline\baseline_1_prematch_test.csv`
- `C:\LateGoalResearch\data\processed\reports\baseline_1_prematch_feature_manifest.json`
- `C:\LateGoalResearch\data\processed\reports\baseline_1_prematch_split_report.json`
- `C:\LateGoalResearch\data\processed\reports\baseline_1_prematch_imputation_report.json`
- `C:\LateGoalResearch\data\processed\reports\baseline_1_prematch_metrics.json`
- `C:\LateGoalResearch\data\processed\reports\baseline_1_prematch_validation_report.json`
- `C:\LateGoalResearch\data\processed\models\baseline_1_prematch_model.pkl`
