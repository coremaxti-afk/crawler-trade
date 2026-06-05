# INITIAL STATISTICAL VALIDATION H6/H9

## Status

Validacao estatistica inicial executada.

Nenhuma modelagem foi iniciada. Nenhum banco, schema, crawler ou importer foi alterado.

---

## Escopo

Dataset usado:

- `LateGoalResearch/data/processed/datasets/late_goal_dataset_v1b_ingame.csv`
- `late_goal_dataset_v1b_ingame_metadata.json`
- `late_goal_dataset_v1b_ingame_validation_report.json`

Plano metodologico:

- `docs/04_RESEARCH/STATISTICAL_VALIDATION_PLAN.md`

Grain:

- 1 linha por `match_id + cutoff_minute`.

Cutoffs:

- 60, 65, 70, 75, 80.

Target:

- `target_goal_after_cutoff`: 1 se existe gol com minuto maior que `cutoff_minute`; 0 caso contrario.

Baseline geral:

- N: 1900
- Positivos: 1078
- Negativos: 822
- Taxa de target: 0.567368

---

## Metodologia

- Variaveis binarias foram comparadas com Fisher exact test em tabela 2x2.
- Variaveis com multiplos grupos foram avaliadas com teste qui-quadrado de independencia.
- Efeito observado em variaveis binarias: odds ratio do grupo 1 contra grupo 0 e diferenca da taxa do grupo 1 contra o baseline.
- Efeito observado em variaveis agrupadas: Cramer's V e maior diferenca absoluta de taxa contra o baseline.
- Recomendacao operacional: MANTER quando p-value < 0.05 e efeito absoluto >= 5 p.p.; OBSERVAR quando efeito >= 3 p.p. sem significancia forte ou com ressalva; DESCARTAR quando efeito e significancia forem fracos nesta amostra.

---

## Controles de Leakage

- Foram usadas apenas colunas construidas a partir de `match_incidents` com `minute <= cutoff_minute` para variaveis explicativas.
- O target foi calculado separadamente com eventos de gol depois do cutoff.
- `match_statistics` nao foi usado.
- Estatisticas full-match nao foram usadas.
- Eventos apos cutoff nao foram usados como variaveis explicativas.
- `red_cards_until_cutoff` e `yellow_cards_until_cutoff` nao foram usados porque estao nulos por design.

---

## H6 - Estado da Partida

Hipotese: o estado atual do placar altera a probabilidade de gols futuros.

### Resumo H6

| Variavel | N | Positivos | Negativos | Taxa baseline | Teste | p-value | Efeito observado | Recomendacao |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- | --- |
| `is_draw_until_cutoff` | 1900 | 1078 | 822 | 0.567368 | Fisher exact test | 0.205801 | OR=0.87145; diff grupo=1 vs baseline=-0.02503 | DESCARTAR |
| `home_leading_until_cutoff` | 1900 | 1078 | 822 | 0.567368 | Fisher exact test | 0.110669 | OR=1.162576; diff grupo=1 vs baseline=0.021534 | DESCARTAR |
| `away_leading_until_cutoff` | 1900 | 1078 | 822 | 0.567368 | Fisher exact test | 0.655687 | OR=0.955095; diff grupo=1 vs baseline=-0.00763 | DESCARTAR |
| `score_diff_home_until_cutoff` | 1900 | 1078 | 822 | 0.567368 | Chi-square test of independence | 0.00987 | Cramer's V=0.083688; max |diff|=0.085441 | MANTER |
| `total_goals_until_cutoff` | 1900 | 1078 | 822 | 0.567368 | Chi-square test of independence | 0.261339 | Cramer's V=0.04589; max |diff|=0.032632 | OBSERVAR |
| `time_since_last_goal_until_cutoff` | 1900 | 1078 | 822 | 0.567368 | Chi-square test of independence | 0.14835 | Cramer's V=0.059708; max |diff|=0.046001 | OBSERVAR |

### Detalhamento por Grupo H6

### `is_draw_until_cutoff`

Empate no cutoff contra qualquer nao-empate.

Teste usado: Fisher exact test. p-value: 0.205801. Recomendacao: **DESCARTAR**.

| Grupo | N | Positivos | Negativos | Taxa target | Diff vs baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 1404 | 809 | 595 | 0.576211 | 0.008842 |
| 1 | 496 | 269 | 227 | 0.542339 | -0.02503 |

### `home_leading_until_cutoff`

Mandante vencendo no cutoff contra demais estados.

Teste usado: Fisher exact test. p-value: 0.110669. Recomendacao: **DESCARTAR**.

| Grupo | N | Positivos | Negativos | Taxa target | Diff vs baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 1107 | 611 | 496 | 0.551942 | -0.015426 |
| 1 | 793 | 467 | 326 | 0.588903 | 0.021534 |

### `away_leading_until_cutoff`

Visitante vencendo no cutoff contra demais estados.

Teste usado: Fisher exact test. p-value: 0.655687. Recomendacao: **DESCARTAR**.

| Grupo | N | Positivos | Negativos | Taxa target | Diff vs baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 1289 | 736 | 553 | 0.570985 | 0.003617 |
| 1 | 611 | 342 | 269 | 0.559738 | -0.00763 |

### `score_diff_home_until_cutoff`

Diferenca de placar pela perspectiva do mandante, agrupada em visitante +2, visitante +1, empate, mandante +1 e mandante +2.

Teste usado: Chi-square test of independence. p-value: 0.00987. Recomendacao: **MANTER**.

| Grupo | N | Positivos | Negativos | Taxa target | Diff vs baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| away_by_1 | 362 | 222 | 140 | 0.61326 | 0.045891 |
| away_by_2_plus | 249 | 120 | 129 | 0.481928 | -0.085441 |
| draw | 496 | 269 | 227 | 0.542339 | -0.02503 |
| home_by_1 | 486 | 285 | 201 | 0.58642 | 0.019051 |
| home_by_2_plus | 307 | 182 | 125 | 0.592834 | 0.025465 |

### `total_goals_until_cutoff`

Total de gols ja ocorridos no cutoff, agrupado em 0, 1, 2 e 3+.

Teste usado: Chi-square test of independence. p-value: 0.261339. Recomendacao: **OBSERVAR**.

| Grupo | N | Positivos | Negativos | Taxa target | Diff vs baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 200 | 120 | 80 | 0.6 | 0.032632 |
| 1 | 528 | 314 | 214 | 0.594697 | 0.027329 |
| 2 | 499 | 274 | 225 | 0.549098 | -0.01827 |
| 3+ | 673 | 370 | 303 | 0.549777 | -0.017591 |

### `time_since_last_goal_until_cutoff`

Tempo desde o ultimo gol ate o cutoff, incluindo grupo sem gol anterior.

Teste usado: Chi-square test of independence. p-value: 0.14835. Recomendacao: **OBSERVAR**.

| Grupo | N | Positivos | Negativos | Taxa target | Diff vs baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0-5 | 330 | 175 | 155 | 0.530303 | -0.037065 |
| 11-20 | 387 | 217 | 170 | 0.560724 | -0.006645 |
| 21+ | 749 | 444 | 305 | 0.59279 | 0.025422 |
| 6-10 | 234 | 122 | 112 | 0.521368 | -0.046001 |
| no_prior_goal | 200 | 120 | 80 | 0.6 | 0.032632 |

### Analise complementar de estado composto

O grupo `score_state_group` combina empate 0x0, empate com gols, lideranca simples e lideranca por 2+ gols. Ele nao substitui as variaveis solicitadas, mas ajuda a interpretar H6 sem perder granularidade do estado do placar.

| Variavel | N | Positivos | Negativos | Taxa baseline | Teste | p-value | Efeito observado | Recomendacao |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- | --- |
| `score_state_group` | 1900 | 1078 | 822 | 0.567368 | Chi-square test of independence | 0.003145 | Cramer's V=0.096916; max |diff|=0.085441 | MANTER |

### `score_state_group`

Estado composto do placar: 0x0, empate com gols, mandante/visitante vencendo por 1 ou por 2+.

Teste usado: Chi-square test of independence. p-value: 0.003145. Recomendacao: **MANTER**.

| Grupo | N | Positivos | Negativos | Taxa target | Diff vs baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| away_leading_by_1 | 362 | 222 | 140 | 0.61326 | 0.045891 |
| away_leading_by_2_plus | 249 | 120 | 129 | 0.481928 | -0.085441 |
| draw_0_0 | 200 | 120 | 80 | 0.6 | 0.032632 |
| draw_with_goals | 296 | 149 | 147 | 0.503378 | -0.06399 |
| home_leading_by_1 | 486 | 285 | 201 | 0.58642 | 0.019051 |
| home_leading_by_2_plus | 307 | 182 | 125 | 0.592834 | 0.025465 |

### Interpretacao H6

- `score_diff_home_until_cutoff` apresentou associacao estatisticamente significativa com o target e efeito relevante. Recomenda-se manter para a proxima etapa exploratoria.
- `score_state_group` tambem apresentou sinal significativo, sugerindo que o estado composto do placar e mais informativo que flags isoladas.
- `is_draw_until_cutoff`, `home_leading_until_cutoff` e `away_leading_until_cutoff` isoladas nao apresentaram evidencia suficiente nesta amostra.
- `total_goals_until_cutoff` e `time_since_last_goal_until_cutoff` devem ser observadas: nao passaram como sinal forte, mas exibem diferencas de taxa em alguns grupos.

---

## H9 - Eventos Alteram Probabilidade

Hipotese: eventos recentes alteram a probabilidade de gol futuro.

### Resumo H9

| Variavel | N | Positivos | Negativos | Taxa baseline | Teste | p-value | Efeito observado | Recomendacao |
| --- | ---: | ---: | ---: | ---: | --- | ---: | --- | --- |
| `goal_last_5m_until_cutoff` | 1900 | 1078 | 822 | 0.567368 | Fisher exact test | 0.399569 | OR=0.893517; diff grupo=1 vs baseline=-0.023509 | DESCARTAR |
| `goal_last_10m_until_cutoff` | 1900 | 1078 | 822 | 0.567368 | Fisher exact test | 0.079035 | OR=0.834321; diff grupo=1 vs baseline=-0.032264 | OBSERVAR |
| `cards_until_cutoff` | 1900 | 1078 | 822 | 0.567368 | Chi-square test of independence | 0.003972 | Cramer's V=0.083765; max |diff|=0.058981 | MANTER |
| `substitutions_until_cutoff` | 1900 | 1078 | 822 | 0.567368 | Chi-square test of independence | 0 | Cramer's V=0.14091; max |diff|=0.122287 | MANTER |

### Detalhamento por Grupo H9

### `goal_last_5m_until_cutoff`

Houve gol nos 5 minutos anteriores ao cutoff.

Teste usado: Fisher exact test. p-value: 0.399569. Recomendacao: **DESCARTAR**.

| Grupo | N | Positivos | Negativos | Taxa target | Diff vs baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 1615 | 923 | 692 | 0.571517 | 0.004149 |
| 1 | 285 | 155 | 130 | 0.54386 | -0.023509 |

### `goal_last_10m_until_cutoff`

Houve gol nos 10 minutos anteriores ao cutoff.

Teste usado: Fisher exact test. p-value: 0.079035. Recomendacao: **OBSERVAR**.

| Grupo | N | Positivos | Negativos | Taxa target | Diff vs baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 1373 | 796 | 577 | 0.579752 | 0.012384 |
| 1 | 527 | 282 | 245 | 0.535104 | -0.032264 |

### `cards_until_cutoff`

Quantidade de cartoes registrados ate o cutoff, sem distinguir cor.

Teste usado: Chi-square test of independence. p-value: 0.003972. Recomendacao: **MANTER**.

| Grupo | N | Positivos | Negativos | Taxa target | Diff vs baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 182 | 110 | 72 | 0.604396 | 0.037027 |
| 1 | 288 | 166 | 122 | 0.576389 | 0.00902 |
| 2 | 463 | 290 | 173 | 0.62635 | 0.058981 |
| 3+ | 967 | 512 | 455 | 0.529473 | -0.037896 |

### `substitutions_until_cutoff`

Quantidade de substituicoes registradas ate o cutoff.

Teste usado: Chi-square test of independence. p-value: 0. Recomendacao: **MANTER**.

| Grupo | N | Positivos | Negativos | Taxa target | Diff vs baseline |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 184 | 120 | 64 | 0.652174 | 0.084805 |
| 1 | 203 | 140 | 63 | 0.689655 | 0.122287 |
| 2 | 275 | 178 | 97 | 0.647273 | 0.079904 |
| 3+ | 1238 | 640 | 598 | 0.516963 | -0.050406 |

### Interpretacao H9

- `cards_until_cutoff` apresentou associacao estatisticamente significativa. Como a cor do cartao nao esta disponivel, o sinal deve ser tratado como proxy agregada de tensao/eventos disciplinares.
- `substitutions_until_cutoff` apresentou o efeito mais forte entre as variaveis H9 testadas, mas exige cautela porque substituicoes aumentam mecanicamente com o tempo e podem carregar efeito de cutoff.
- `goal_last_10m_until_cutoff` ficou em zona de observacao, com p-value proximo mas acima de 0.05.
- `goal_last_5m_until_cutoff` nao apresentou evidencia suficiente nesta amostra inicial.

---

## Recomendacoes por Feature

| Hipotese | Feature | Recomendacao | Motivo |
| --- | --- | --- | --- |
| H6 | `is_draw_until_cutoff` | DESCARTAR | p=0.205801; OR=0.87145; diff=-0.02503 |
| H6 | `home_leading_until_cutoff` | DESCARTAR | p=0.110669; OR=1.162576; diff=0.021534 |
| H6 | `away_leading_until_cutoff` | DESCARTAR | p=0.655687; OR=0.955095; diff=-0.00763 |
| H6 | `score_diff_home_until_cutoff` | MANTER | p=0.00987; V=0.083688; max diff=0.085441 |
| H6 | `total_goals_until_cutoff` | OBSERVAR | p=0.261339; V=0.04589; max diff=0.032632 |
| H6 | `time_since_last_goal_until_cutoff` | OBSERVAR | p=0.14835; V=0.059708; max diff=0.046001 |
| H6 | `score_state_group` | MANTER | p=0.003145; V=0.096916; max diff=0.085441 |
| H9 | `goal_last_5m_until_cutoff` | DESCARTAR | p=0.399569; OR=0.893517; diff=-0.023509 |
| H9 | `goal_last_10m_until_cutoff` | OBSERVAR | p=0.079035; OR=0.834321; diff=-0.032264 |
| H9 | `cards_until_cutoff` | MANTER | p=0.003972; V=0.083765; max diff=0.058981 |
| H9 | `substitutions_until_cutoff` | MANTER | p=0; V=0.14091; max diff=0.122287 |

---

## Limitacoes

- A amostra possui apenas uma temporada EPL e 1900 linhas derivadas de 380 partidas por 5 cutoffs; as linhas por cutoff nao sao independentes no sentido forte, pois uma mesma partida aparece cinco vezes.
- Os testes medem associacao estatistica, nao capacidade preditiva fora da amostra.
- `substitutions_until_cutoff` pode refletir parcialmente o efeito do tempo/cutoff, ja que substituicoes se acumulam ao longo da partida.
- `cards_until_cutoff` nao separa amarelos de vermelhos porque a importacao atual nao preserva a cor do cartao.
- `time_since_last_goal_until_cutoff` possui grupo sem gol anterior, que deve ser interpretado separadamente de intervalos numericos.
- Nenhuma correcao formal para multiplos testes foi aplicada nesta rodada inicial; resultados devem ser tratados como triagem estatistica.

---

## Conclusao

H6 possui sinal inicial principalmente quando o estado do placar e representado por diferenca/estado composto, nao por flags isoladas simples.

H9 possui sinal inicial em `cards_until_cutoff` e `substitutions_until_cutoff`, com ressalvas metodologicas importantes. `goal_last_10m_until_cutoff` deve permanecer em observacao; `goal_last_5m_until_cutoff` deve ser descartada nesta forma inicial.

A proxima etapa recomendada e revisar esses achados com Quant Research, decidir quais variaveis entram no catalogo exploratorio e somente depois discutir feature engineering formal. Nenhuma modelagem deve ser iniciada com base apenas neste relatorio.
