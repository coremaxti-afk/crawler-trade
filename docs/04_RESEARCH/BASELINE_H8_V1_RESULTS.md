# Baseline H8 V1 Results

Gerado em: 2026-06-06T20:23:54

## Resumo Executivo

Baseline H8 V1 executado em rodada controlada, avaliando cada cutoff separadamente: 60, 65, 70 e 75.

Status operacional: `APTO COM RESSALVAS`.

Melhor cutoff no ranking principal: `60`.

Metricas do melhor cutoff no teste:

- ROC-AUC Test: 0.5076
- PR-AUC Test: 0.5232
- Delta Brier modelo-nulo: 0.0155
- Delta LogLoss modelo-nulo: 0.0345
- Lift@Top20% Test: 0.9500
- Melhor feature: `momentum_last_10m_avg`
- Melhor grupo: `Graph`

## Gate do Validation Report

Todos os pontos obrigatorios foram confirmados antes da execucao:

- target_late_goal_75_unido_corretamente: `True`
- ausencia_target_derived_features: `True`
- ausencia_full_match: `True`
- ausencia_placar_final: `True`
- graph_known_missing_preservado: `True`
- duplicatas_match_cutoff_zero: `True`

## Metodologia

- Dataset: `data/processed/datasets/late_goal_dataset_h8_v1.csv`.
- Target: `target_late_goal_75`.
- Features: somente whitelist H8.
- Cutoffs avaliados separadamente: 60, 65, 70, 75.
- Split: temporal por `match_id`, 60/20/20, sem shuffle.
- Imputacao: mediana fitada apenas no treino dentro de cada cutoff.
- Escala: StandardScaler fitado apenas no treino dentro de cada cutoff.
- Modelo: regressao logistica controlada.
- Baseline nulo: probabilidade constante igual a prevalencia do treino em cada cutoff.

## Features Usadas

- `momentum_last_5m_avg`
- `momentum_last_10m_avg`
- `momentum_trend_last_10m`
- `momentum_sum_until_cutoff`
- `xg_last_5m`
- `xg_last_10m`
- `shots_last_5m`
- `shots_last_10m`
- `xg_sum_until_cutoff`

## Auditoria Anti-Leakage

- Nenhuma feature H3/H4/H6/H9 foi usada.
- Nenhuma feature target-derived foi usada em X.
- Nenhum placar final foi usado.
- Nenhuma estatistica full-match foi usada.
- Features H8 vieram do Dataset H8 V1, herdando a regra `minute <= cutoff`.
- Backtesting financeiro: nao executado.
- Producao: nao criada.

## Metricas por Cutoff e Split

| Cutoff | Split | Modelo | N | Pos | Neg | Prev | ROC-AUC | PR-AUC | Brier | Log Loss | Lift@20% |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 60 | train | Nulo | 228 | 112 | 116 | 0.4912 | 0.5000 | 0.4912 | 0.2499 | 0.6930 | 1.1064 |
| 60 | train | Modelo | 228 | 112 | 116 | 0.4912 | 0.6084 | 0.6191 | 0.2401 | 0.6728 | 1.3719 |
| 60 | validation | Nulo | 76 | 37 | 39 | 0.4868 | 0.5000 | 0.4868 | 0.2498 | 0.6928 | 1.4122 |
| 60 | validation | Modelo | 76 | 37 | 39 | 0.4868 | 0.4837 | 0.4857 | 0.2633 | 0.7209 | 0.8986 |
| 60 | test | Nulo | 76 | 40 | 36 | 0.5263 | 0.5000 | 0.5263 | 0.2505 | 0.6942 | 0.9500 |
| 60 | test | Modelo | 76 | 40 | 36 | 0.5263 | 0.5076 | 0.5232 | 0.2660 | 0.7287 | 0.9500 |
| 65 | train | Nulo | 228 | 112 | 116 | 0.4912 | 0.5000 | 0.4912 | 0.2499 | 0.6930 | 1.1064 |
| 65 | train | Modelo | 228 | 112 | 116 | 0.4912 | 0.5744 | 0.5957 | 0.2435 | 0.6796 | 1.3276 |
| 65 | validation | Nulo | 76 | 37 | 39 | 0.4868 | 0.5000 | 0.4868 | 0.2498 | 0.6928 | 1.4122 |
| 65 | validation | Modelo | 76 | 37 | 39 | 0.4868 | 0.5010 | 0.5021 | 0.2532 | 0.6995 | 0.8986 |
| 65 | test | Nulo | 76 | 40 | 36 | 0.5263 | 0.5000 | 0.5263 | 0.2505 | 0.6942 | 0.9500 |
| 65 | test | Modelo | 76 | 40 | 36 | 0.5263 | 0.4299 | 0.4771 | 0.2705 | 0.7357 | 0.8313 |
| 70 | train | Nulo | 228 | 112 | 116 | 0.4912 | 0.5000 | 0.4912 | 0.2499 | 0.6930 | 1.1064 |
| 70 | train | Modelo | 228 | 112 | 116 | 0.4912 | 0.5864 | 0.5858 | 0.2432 | 0.6796 | 1.2834 |
| 70 | validation | Nulo | 76 | 37 | 39 | 0.4868 | 0.5000 | 0.4868 | 0.2498 | 0.6928 | 1.4122 |
| 70 | validation | Modelo | 76 | 37 | 39 | 0.4868 | 0.5038 | 0.4885 | 0.2633 | 0.7209 | 0.7703 |
| 70 | test | Nulo | 76 | 40 | 36 | 0.5263 | 0.5000 | 0.5263 | 0.2505 | 0.6942 | 0.9500 |
| 70 | test | Modelo | 76 | 40 | 36 | 0.5263 | 0.4903 | 0.5378 | 0.2609 | 0.7158 | 0.9500 |
| 75 | train | Nulo | 228 | 112 | 116 | 0.4912 | 0.5000 | 0.4912 | 0.2499 | 0.6930 | 1.1064 |
| 75 | train | Modelo | 228 | 112 | 116 | 0.4912 | 0.5989 | 0.6378 | 0.2406 | 0.6736 | 1.3276 |
| 75 | validation | Nulo | 76 | 37 | 39 | 0.4868 | 0.5000 | 0.4868 | 0.2498 | 0.6928 | 1.4122 |
| 75 | validation | Modelo | 76 | 37 | 39 | 0.4868 | 0.4761 | 0.4954 | 0.2622 | 0.7188 | 0.8986 |
| 75 | test | Nulo | 76 | 40 | 36 | 0.5263 | 0.5000 | 0.5263 | 0.2505 | 0.6942 | 0.9500 |
| 75 | test | Modelo | 76 | 40 | 36 | 0.5263 | 0.4521 | 0.4899 | 0.2686 | 0.7315 | 0.7125 |

## Comparacao Contra Baseline Nulo

Valores negativos em Brier/LogLoss indicam melhora do modelo contra o nulo.

| Cutoff | Split | Delta ROC-AUC | Delta PR-AUC | Delta Brier | Delta Log Loss | Delta Lift@20% |
|---:|---|---:|---:|---:|---:|---:|
| 60 | train | 0.1084 | 0.1278 | -0.0099 | -0.0202 | 0.2655 |
| 60 | validation | -0.0163 | -0.0012 | 0.0135 | 0.0280 | -0.5135 |
| 60 | test | 0.0076 | -0.0031 | 0.0155 | 0.0345 | 0.0000 |
| 65 | train | 0.0744 | 0.1045 | -0.0065 | -0.0134 | 0.2213 |
| 65 | validation | 0.0010 | 0.0153 | 0.0033 | 0.0066 | -0.5135 |
| 65 | test | -0.0701 | -0.0492 | 0.0200 | 0.0415 | -0.1188 |
| 70 | train | 0.0864 | 0.0946 | -0.0067 | -0.0134 | 0.1770 |
| 70 | validation | 0.0038 | 0.0017 | 0.0135 | 0.0281 | -0.6419 |
| 70 | test | -0.0097 | 0.0115 | 0.0103 | 0.0216 | 0.0000 |
| 75 | train | 0.0989 | 0.1465 | -0.0093 | -0.0193 | 0.2213 |
| 75 | validation | -0.0239 | 0.0085 | 0.0123 | 0.0259 | -0.5135 |
| 75 | test | -0.0479 | -0.0365 | 0.0181 | 0.0372 | -0.2375 |

## Ranking dos Cutoffs

| Rank | Cutoff | ROC-AUC Test | PR-AUC Test | Delta Brier Test | Delta LogLoss Test | Lift@20% Test | Melhor Feature | Melhor Grupo |
|---:|---:|---:|---:|---:|---:|---:|---|---|
| 1 | 60 | 0.5076 | 0.5232 | 0.0155 | 0.0345 | 0.9500 | `momentum_last_10m_avg` | Graph |
| 2 | 70 | 0.4903 | 0.5378 | 0.0103 | 0.0216 | 0.9500 | `xg_last_5m` | Shotmap |
| 3 | 75 | 0.4521 | 0.4899 | 0.0181 | 0.0372 | 0.7125 | `xg_last_10m` | Shotmap |
| 4 | 65 | 0.4299 | 0.4771 | 0.0200 | 0.0415 | 0.8313 | `xg_last_10m` | Shotmap |

## Melhor Feature e Grupo

- Melhor feature geral: `momentum_last_10m_avg`.
- Melhor grupo geral: `Graph`.

## Recomendacao Final

Decisao quantitativa inicial: `NAO APROVADO`.

Motivo: o melhor cutoff foi 60, mas o ROC-AUC Test ficou em 0.5076, o PR-AUC Test ficou em 0.5232, e o modelo piorou o baseline nulo em Brier (0.0155) e LogLoss (0.0345) no teste.

Baseline H8 V1 deve ser tratado como experimento controlado de pesquisa. O resultado nao autoriza producao, automacao operacional ou backtesting financeiro.
