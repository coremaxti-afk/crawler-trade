# Baseline In-Game V1 Results

Gerado em: 2026-06-05T02:29:18

## Resumo Executivo

Baseline In-Game V1 executado em rodada controlada com cutoff 75, features H6/H9 aprovadas, target `target_late_goal_75`, split temporal 60/20/20 sem shuffle, imputacao numerica por mediana fitada apenas no treino, codificacao categorica fitada apenas no treino, baseline nulo por prevalencia do treino e modelo treinado de regressao logistica.

Status operacional: `APTO COM RESSALVAS`.

Status dos criterios quantitativos: `NAO APROVADO`.

Resultado no teste:

- ROC-AUC Test: 0.5250
- PR-AUC Test: 0.5541
- Prevalencia Test: 0.5263
- ROC-AUC aprovado: False
- PR-AUC aprovado: False
- Brier contra nulo aprovado: False
- Log Loss contra nulo aprovado: False

## Objetivo

Avaliar se features in-game disponiveis ate o minuto 75 possuem sinal preditivo minimo para estimar a probabilidade de uma partida ter pelo menos um gol apos 75:00.

## Arquivos de Entrada

- `C:\LateGoalResearch\data\processed\datasets\late_goal_dataset_v1b_ingame.csv`
- `C:\LateGoalResearch\data\processed\datasets\late_goal_dataset_v1b_ingame_metadata.json`
- `C:\LateGoalResearch\data\processed\datasets\late_goal_dataset_v1b_ingame_validation_report.json`
- `C:\LateGoalResearch\data\processed\datasets\late_goal_dataset_v1.csv` usado somente para validar equivalencia do target, quando disponivel.

## Snapshot Oficial

- Cutoff: `75`
- Filtro aplicado: `cutoff_minute == 75`
- Features: informacoes ate `minute <= 75`
- Target operacional: `target_goal_after_cutoff` em cutoff 75
- Target final do experimento: `target_late_goal_75`

## Features Usadas

Features base:

- `score_diff_home_until_cutoff`
- `cards_until_cutoff`
- `substitutions_until_cutoff`
- `score_state_group`

Features apos codificacao:

- `score_diff_home_until_cutoff`
- `cards_until_cutoff`
- `substitutions_until_cutoff`
- `score_state_group_away_leading`
- `score_state_group_draw`
- `score_state_group_home_leading`

## Auditoria Anti-Leakage

- Whitelist oficial prevaleceu sobre blacklist: `true`.
- Target fora de X: `true`.
- Operational target fora de X: `true`.
- `match_statistics` full-match usado: `false`.
- Features pre-jogo usadas: `false`.
- xG/xGA/forecast usados: `false`.
- `score_state_group` foi derivado de `score_diff_home_until_cutoff` dentro do snapshot cutoff 75.

## Validacao do Snapshot

- Todas as linhas com `cutoff_minute = 75`: `True`.
- Uma linha por `match_id`: `True`.
- Equivalencia de target checada: `True`.
- Divergencias de target: `0`.

## Split Temporal

| Split | N | Data inicial | Data final | Pos | Neg | Prevalencia |
|---|---:|---|---|---:|---:|---:|
| train | 228 | 2024-08-16T19:00:00 | 2025-01-26T16:30:00 | 112 | 116 | 0.4912 |
| validation | 76 | 2025-01-26T19:00:00 | 2025-04-05T16:30:00 | 37 | 39 | 0.4868 |
| test | 76 | 2025-04-06T13:00:00 | 2025-05-25T15:00:00 | 40 | 36 | 0.5263 |

## Imputacao e Codificacao

- Numericas: mediana fitada apenas no treino.
- Categorica: OneHotEncoder fitado apenas no treino, com `handle_unknown=ignore`.
- Categorias de treino: `{'score_state_group': ['away_leading', 'draw', 'home_leading']}`.
- Medianas de treino: `{'score_diff_home_until_cutoff': 0.0, 'cards_until_cutoff': 3.0, 'substitutions_until_cutoff': 4.0}`.

## Baseline Nulo

Probabilidade constante aprendida no treino: `0.4912`.

## Metricas por Split

| Split | Modelo | N | Pos | Neg | Prev | ROC-AUC | PR-AUC | Brier | Log Loss | Lift@20% |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| train | null_baseline | 228 | 112 | 116 | 0.4912 | 0.5000 | 0.4912 | 0.2499 | 0.6930 | 1.1064 |
| train | trained_model | 228 | 112 | 116 | 0.4912 | 0.5444 | 0.4936 | 0.2466 | 0.6863 | 0.9293 |
| validation | null_baseline | 76 | 37 | 39 | 0.4868 | 0.5000 | 0.4868 | 0.2498 | 0.6928 | 1.4122 |
| validation | trained_model | 76 | 37 | 39 | 0.4868 | 0.4771 | 0.5677 | 0.2597 | 0.7128 | 1.1554 |
| test | null_baseline | 76 | 40 | 36 | 0.5263 | 0.5000 | 0.5263 | 0.2505 | 0.6942 | 0.9500 |
| test | trained_model | 76 | 40 | 36 | 0.5263 | 0.5250 | 0.5541 | 0.2525 | 0.6983 | 1.1875 |

## Comparacao Modelo vs Baseline Nulo

Valores negativos em Brier/LogLoss indicam melhora probabilistica do modelo contra o baseline nulo.

| Split | Delta Brier modelo-nulo | Delta LogLoss modelo-nulo | Delta ROC-AUC | Delta PR-AUC | Delta Lift@20% |
|---|---:|---:|---:|---:|---:|
| train | -0.0033 | -0.0067 | 0.0444 | 0.0024 | -0.1770 |
| validation | 0.0098 | 0.0200 | -0.0229 | 0.0809 | -0.2568 |
| test | 0.0019 | 0.0041 | 0.0250 | 0.0278 | 0.2375 |

## Comparacao Externa com Baseline 1A

Referencia externa aprovada:

- Baseline 1A ROC-AUC Test: 0.4910
- Baseline 1A PR-AUC Test: 0.5364

Comparacao direta e apenas contextual, pois Baseline 1A e pre-jogo e Baseline In-Game V1 usa informacao disponivel aos 75 minutos.

## Calibration by Bins

A calibracao por bins esta registrada em `C:\LateGoalResearch\data\processed\reports\baseline_ingame_v1_metrics.json` para train, validation e test, tanto para baseline nulo quanto para modelo treinado.

## Decisao Final

Status dos criterios quantitativos: `NAO APROVADO`.

Status operacional do artefato: `APTO COM RESSALVAS`.

Esta execucao nao autoriza producao, automacao operacional, backtesting financeiro ou uso como sistema decisorio.

## Limitacoes

- Amostra de uma unica temporada EPL.
- Modelo simples e exploratorio.
- `score_state_group` precisou ser derivado operacionalmente porque a coluna nao estava materializada no dataset V1B.
- Apenas cutoff 75 foi avaliado; comparacao de cutoffs 60/65/70/75 permanece fora do V1.
- Nenhum threshold decisorio foi aprovado.

## Recomendacoes

1. Quant Research deve revisar ROC-AUC Test, PR-AUC Test e comparacao contra baseline nulo.
2. PM deve decidir se o resultado autoriza nova iteracao metodologica.
3. Nao avancar para producao nem backtesting financeiro.
4. Se aprovado futuramente, planejar Baseline In-Game V2 para comparar cutoffs.

## Artefatos Gerados

- `C:\LateGoalResearch\data\processed\baseline_ingame\baseline_ingame_v1_dataset.csv`
- `C:\LateGoalResearch\data\processed\baseline_ingame\baseline_ingame_v1_train.csv`
- `C:\LateGoalResearch\data\processed\baseline_ingame\baseline_ingame_v1_validation.csv`
- `C:\LateGoalResearch\data\processed\baseline_ingame\baseline_ingame_v1_test.csv`
- `C:\LateGoalResearch\data\processed\reports\baseline_ingame_v1_feature_manifest.json`
- `C:\LateGoalResearch\data\processed\reports\baseline_ingame_v1_split_report.json`
- `C:\LateGoalResearch\data\processed\reports\baseline_ingame_v1_preprocessing_report.json`
- `C:\LateGoalResearch\data\processed\reports\baseline_ingame_v1_metrics.json`
- `C:\LateGoalResearch\data\processed\reports\baseline_ingame_v1_validation_report.json`
