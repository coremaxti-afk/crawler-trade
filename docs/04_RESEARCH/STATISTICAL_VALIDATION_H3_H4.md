# Validacao Estatistica H3/H4 - Historical Pre-Match Features V1

Gerado em: 2026-06-04T23:27:40

## 1. Metodologia aplicada

Esta validacao usa o arquivo `historical_prematch_features_v1.csv` como fonte de features historicas pre-jogo e o `late_goal_dataset_v1.csv` apenas para anexar o target direcional. O join foi feito por `match_id`, preservando o grain de uma linha por time por partida.

O target usado foi `target_directional_late_goal_75`, derivado somente para este relatorio:

- linhas `is_home = 1`: `home_late_goal_count_75 > 0`;
- linhas `is_home = 0`: `away_late_goal_count_75 > 0`.

As linhas sem historico anterior foram removidas por feature quando a feature estava nula. Nenhum dataset existente foi alterado. Nenhum dado de partida futura, target, xG, forecast ou estatistica da propria partida foi usado como variavel explicativa. A validacao do Feature Builder V1 informa status `APTO` e `temporal_leakage_validation.mismatch_count = 0`.

Para cada feature, os valores foram agrupados em quartis quando possivel. Para cada grupo foram calculados N, positivos, negativos, taxa do target e diferenca contra o baseline da amostra valida da propria feature. O teste estatistico aplicado foi qui-quadrado para tabelas com mais de 2 grupos e Fisher exact apenas quando a tabela ficou 2x2. O tamanho de efeito reportado e Cramer's V para qui-quadrado ou odds ratio para Fisher.

Criterio de classificacao:

- MANTER: p-value < 0.05 e efeito absoluto maximo >= 5 p.p.;
- OBSERVAR: efeito absoluto maximo >= 3 p.p. ou p-value proximo de 0.05;
- DESCARTAR: efeito e significancia fracos nesta amostra.

## 2. Tamanho da amostra utilizada

- Linhas no feature set: 760
- Positivos direcionais: 214
- Negativos direcionais: 546
- Baseline direcional geral: 28.2%
- Partidas: 380
- Times: 20
- Linhas sem historico inicial esperadas: 20

## 3. Testes estatisticos executados

| Feature | N | Positivos | Negativos | Baseline | Teste | p-value | Efeito | Efeito max | Classificacao |
|---|---:|---:|---:|---:|---|---:|---:|---:|---|
| `goals_for_avg_last_3` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0421 | 0.105 | 6.1 p.p. | MANTER |
| `goals_for_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.1780 | 0.082 | 4.5 p.p. | OBSERVAR |
| `goals_for_avg_last_10` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0086 | 0.126 | 9.3 p.p. | MANTER |
| `shots_for_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.4959 | 0.057 | 3.5 p.p. | OBSERVAR |
| `shots_on_target_for_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0298 | 0.110 | 6.9 p.p. | MANTER |
| `big_chances_for_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.2660 | 0.073 | 4.9 p.p. | OBSERVAR |
| `goals_against_avg_last_3` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.2209 | 0.077 | 7.1 p.p. | OBSERVAR |
| `goals_against_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0821 | 0.095 | 7.7 p.p. | OBSERVAR |
| `goals_against_avg_last_10` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0944 | 0.093 | 6.4 p.p. | OBSERVAR |
| `shots_against_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0334 | 0.108 | 7.8 p.p. | MANTER |
| `shots_on_target_against_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0028 | 0.138 | 10.8 p.p. | MANTER |
| `big_chances_against_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0004 | 0.157 | 9.1 p.p. | MANTER |

## 4. Ranking preliminar das features

| Rank | Hipotese | Feature | Classificacao | p-value | Efeito max | Teste |
|---:|---|---|---|---:|---:|---|
| 1 | H4 | `shots_on_target_against_avg_last_5` | MANTER | 0.0028 | 10.8 p.p. | Qui-quadrado |
| 2 | H3 | `goals_for_avg_last_10` | MANTER | 0.0086 | 9.3 p.p. | Qui-quadrado |
| 3 | H4 | `big_chances_against_avg_last_5` | MANTER | 0.0004 | 9.1 p.p. | Qui-quadrado |
| 4 | H4 | `shots_against_avg_last_5` | MANTER | 0.0334 | 7.8 p.p. | Qui-quadrado |
| 5 | H3 | `shots_on_target_for_avg_last_5` | MANTER | 0.0298 | 6.9 p.p. | Qui-quadrado |
| 6 | H3 | `goals_for_avg_last_3` | MANTER | 0.0421 | 6.1 p.p. | Qui-quadrado |
| 7 | H4 | `goals_against_avg_last_5` | OBSERVAR | 0.0821 | 7.7 p.p. | Qui-quadrado |
| 8 | H4 | `goals_against_avg_last_3` | OBSERVAR | 0.2209 | 7.1 p.p. | Qui-quadrado |
| 9 | H4 | `goals_against_avg_last_10` | OBSERVAR | 0.0944 | 6.4 p.p. | Qui-quadrado |
| 10 | H3 | `big_chances_for_avg_last_5` | OBSERVAR | 0.2660 | 4.9 p.p. | Qui-quadrado |
| 11 | H3 | `goals_for_avg_last_5` | OBSERVAR | 0.1780 | 4.5 p.p. | Qui-quadrado |
| 12 | H3 | `shots_for_avg_last_5` | OBSERVAR | 0.4959 | 3.5 p.p. | Qui-quadrado |

## 5. H3 - Forca Ofensiva

| Feature | N | Positivos | Negativos | Baseline | Teste | p-value | Efeito | Efeito max | Classificacao |
|---|---:|---:|---:|---:|---|---:|---:|---:|---|
| `goals_for_avg_last_3` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0421 | 0.105 | 6.1 p.p. | MANTER |
| `goals_for_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.1780 | 0.082 | 4.5 p.p. | OBSERVAR |
| `goals_for_avg_last_10` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0086 | 0.126 | 9.3 p.p. | MANTER |
| `shots_for_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.4959 | 0.057 | 3.5 p.p. | OBSERVAR |
| `shots_on_target_for_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0298 | 0.110 | 6.9 p.p. | MANTER |
| `big_chances_for_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.2660 | 0.073 | 4.9 p.p. | OBSERVAR |

### Grupos H3

**`goals_for_avg_last_3`**

| Grupo | N | Positivos | Negativos | Taxa target | Dif. vs baseline |
|---|---:|---:|---:|---:|---:|
| (-0.001, 1.0] | 277 | 61 | 216 | 22.0% | -6.1 p.p. |
| (1.0, 1.333] | 139 | 43 | 96 | 30.9% | +2.8 p.p. |
| (1.333, 2.0] | 201 | 65 | 136 | 32.3% | +4.2 p.p. |
| (2.0, 4.667] | 123 | 39 | 84 | 31.7% | +3.6 p.p. |

**`goals_for_avg_last_5`**

| Grupo | N | Positivos | Negativos | Taxa target | Dif. vs baseline |
|---|---:|---:|---:|---:|---:|
| (-0.001, 1.0] | 229 | 54 | 175 | 23.6% | -4.5 p.p. |
| (1.0, 1.4] | 184 | 58 | 126 | 31.5% | +3.4 p.p. |
| (1.4, 1.8] | 145 | 38 | 107 | 26.2% | -1.9 p.p. |
| (1.8, 3.8] | 182 | 58 | 124 | 31.9% | +3.8 p.p. |

**`goals_for_avg_last_10`**

| Grupo | N | Positivos | Negativos | Taxa target | Dif. vs baseline |
|---|---:|---:|---:|---:|---:|
| (-0.001, 1.0] | 186 | 35 | 151 | 18.8% | -9.3 p.p. |
| (1.0, 1.4] | 186 | 57 | 129 | 30.6% | +2.5 p.p. |
| (1.4, 1.814] | 183 | 62 | 121 | 33.9% | +5.8 p.p. |
| (1.814, 3.0] | 185 | 54 | 131 | 29.2% | +1.1 p.p. |

**`shots_for_avg_last_5`**

| Grupo | N | Positivos | Negativos | Taxa target | Dif. vs baseline |
|---|---:|---:|---:|---:|---:|
| (10.65, 12.8] | 194 | 52 | 142 | 26.8% | -1.3 p.p. |
| (12.8, 15.0] | 193 | 61 | 132 | 31.6% | +3.5 p.p. |
| (15.0, 24.0] | 168 | 49 | 119 | 29.2% | +1.1 p.p. |
| (2.999, 10.65] | 185 | 46 | 139 | 24.9% | -3.2 p.p. |

**`shots_on_target_for_avg_last_5`**

| Grupo | N | Positivos | Negativos | Taxa target | Dif. vs baseline |
|---|---:|---:|---:|---:|---:|
| (0.999, 3.6] | 198 | 42 | 156 | 21.2% | -6.9 p.p. |
| (3.6, 4.4] | 175 | 53 | 122 | 30.3% | +2.2 p.p. |
| (4.4, 5.4] | 201 | 55 | 146 | 27.4% | -0.7 p.p. |
| (5.4, 9.0] | 166 | 58 | 108 | 34.9% | +6.8 p.p. |

**`big_chances_for_avg_last_5`**

| Grupo | N | Positivos | Negativos | Taxa target | Dif. vs baseline |
|---|---:|---:|---:|---:|---:|
| (-0.001, 1.8] | 215 | 50 | 165 | 23.3% | -4.9 p.p. |
| (1.8, 2.4] | 168 | 51 | 117 | 30.4% | +2.2 p.p. |
| (2.4, 3.2] | 186 | 53 | 133 | 28.5% | +0.4 p.p. |
| (3.2, 6.0] | 171 | 54 | 117 | 31.6% | +3.5 p.p. |

### Conclusao H3

Na amostra atual, features ofensivas com sinal mais forte foram: `goals_for_avg_last_3`, `goals_for_avg_last_10`, `shots_on_target_for_avg_last_5`, `goals_for_avg_last_5`, `shots_for_avg_last_5`, `big_chances_for_avg_last_5`. A recomendacao e manter apenas as classificadas como MANTER para a proxima etapa e carregar as classificadas como OBSERVAR em uma lista de monitoramento estatistico, sem usa-las ainda como evidencia conclusiva.

## 6. H4 - Fragilidade Defensiva

| Feature | N | Positivos | Negativos | Baseline | Teste | p-value | Efeito | Efeito max | Classificacao |
|---|---:|---:|---:|---:|---|---:|---:|---:|---|
| `goals_against_avg_last_3` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.2209 | 0.077 | 7.1 p.p. | OBSERVAR |
| `goals_against_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0821 | 0.095 | 7.7 p.p. | OBSERVAR |
| `goals_against_avg_last_10` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0944 | 0.093 | 6.4 p.p. | OBSERVAR |
| `shots_against_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0334 | 0.108 | 7.8 p.p. | MANTER |
| `shots_on_target_against_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0028 | 0.138 | 10.8 p.p. | MANTER |
| `big_chances_against_avg_last_5` | 740 | 208 | 532 | 28.1% | Qui-quadrado | 0.0004 | 0.157 | 9.1 p.p. | MANTER |

### Grupos H4

**`goals_against_avg_last_3`**

| Grupo | N | Positivos | Negativos | Taxa target | Dif. vs baseline |
|---|---:|---:|---:|---:|---:|
| (-0.001, 1.0] | 307 | 89 | 218 | 29.0% | +0.9 p.p. |
| (1.0, 1.333] | 107 | 33 | 74 | 30.8% | +2.7 p.p. |
| (1.333, 2.0] | 188 | 57 | 131 | 30.3% | +2.2 p.p. |
| (2.0, 4.0] | 138 | 29 | 109 | 21.0% | -7.1 p.p. |

**`goals_against_avg_last_5`**

| Grupo | N | Positivos | Negativos | Taxa target | Dif. vs baseline |
|---|---:|---:|---:|---:|---:|
| (-0.001, 1.0] | 233 | 71 | 162 | 30.5% | +2.4 p.p. |
| (1.0, 1.4] | 178 | 54 | 124 | 30.3% | +2.2 p.p. |
| (1.4, 1.8] | 153 | 47 | 106 | 30.7% | +2.6 p.p. |
| (1.8, 4.0] | 176 | 36 | 140 | 20.5% | -7.7 p.p. |

**`goals_against_avg_last_10`**

| Grupo | N | Positivos | Negativos | Taxa target | Dif. vs baseline |
|---|---:|---:|---:|---:|---:|
| (-0.001, 1.1] | 208 | 64 | 144 | 30.8% | +2.7 p.p. |
| (1.1, 1.4] | 201 | 65 | 136 | 32.3% | +4.2 p.p. |
| (1.4, 1.778] | 147 | 39 | 108 | 26.5% | -1.6 p.p. |
| (1.778, 4.0] | 184 | 40 | 144 | 21.7% | -6.4 p.p. |

**`shots_against_avg_last_5`**

| Grupo | N | Positivos | Negativos | Taxa target | Dif. vs baseline |
|---|---:|---:|---:|---:|---:|
| (10.4, 12.6] | 184 | 66 | 118 | 35.9% | +7.8 p.p. |
| (12.6, 15.2] | 186 | 46 | 140 | 24.7% | -3.4 p.p. |
| (15.2, 25.8] | 181 | 42 | 139 | 23.2% | -4.9 p.p. |
| (2.999, 10.4] | 189 | 54 | 135 | 28.6% | +0.5 p.p. |

**`shots_on_target_against_avg_last_5`**

| Grupo | N | Positivos | Negativos | Taxa target | Dif. vs baseline |
|---|---:|---:|---:|---:|---:|
| (0.999, 3.6] | 216 | 71 | 145 | 32.9% | +4.8 p.p. |
| (3.6, 4.4] | 174 | 57 | 117 | 32.8% | +4.7 p.p. |
| (4.4, 5.4] | 182 | 51 | 131 | 28.0% | -0.1 p.p. |
| (5.4, 8.8] | 168 | 29 | 139 | 17.3% | -10.8 p.p. |

**`big_chances_against_avg_last_5`**

| Grupo | N | Positivos | Negativos | Taxa target | Dif. vs baseline |
|---|---:|---:|---:|---:|---:|
| (-0.001, 1.8] | 218 | 53 | 165 | 24.3% | -3.8 p.p. |
| (1.8, 2.4] | 183 | 64 | 119 | 35.0% | +6.9 p.p. |
| (2.4, 3.0] | 155 | 56 | 99 | 36.1% | +8.0 p.p. |
| (3.0, 6.6] | 184 | 35 | 149 | 19.0% | -9.1 p.p. |

### Conclusao H4

Na amostra atual, features defensivas com sinal mais forte foram: `shots_against_avg_last_5`, `shots_on_target_against_avg_last_5`, `big_chances_against_avg_last_5`, `goals_against_avg_last_3`, `goals_against_avg_last_5`, `goals_against_avg_last_10`. A interpretacao deve permanecer conservadora: as features sao historicas e pre-jogo, mas ainda foram avaliadas de forma univariada, sem controle por adversario, mando, calendario ou dependencia entre linhas da mesma partida.

## 7. Limitacoes

- Cada partida contribui com duas linhas, uma por time; portanto as observacoes nao sao totalmente independentes.
- A validacao e univariada e nao substitui modelagem, backtest ou validacao temporal.
- As features de shots e big chances usam estatisticas full-match de partidas anteriores, o que e metodologicamente aceitavel como historico pre-jogo, mas nao deve ser confundido com informacao disponivel durante a partida atual.
- O target direcional foi derivado apenas em memoria para este relatorio; nenhum dataset foi modificado.
- Quartis podem perder granularidade quando a feature tem muitos empates ou poucos valores distintos.

## 8. Recomendacoes para proxima etapa

1. Encaminhar as features classificadas como MANTER para avaliacao multivariada futura, ainda sem iniciar modelagem de producao.
2. Manter features OBSERVAR como candidatas condicionais para validacao temporal ou combinacao com H6/H9.
3. Descartar temporariamente features DESCARTAR nesta amostra, salvo se o Quant Research solicitar reavaliacao com outro target ou janela temporal.
4. Em qualquer etapa posterior, preservar separacao temporal e usar somente historico anterior ao kickoff.
5. Antes de modelagem, criar desenho de validacao temporal por rodada/data para reduzir risco de overfitting e dependencia entre linhas.
