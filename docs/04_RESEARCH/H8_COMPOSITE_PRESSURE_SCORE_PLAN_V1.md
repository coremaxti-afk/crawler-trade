# H8_COMPOSITE_PRESSURE_SCORE_PLAN_V1

## Status

Prioridade maxima de pesquisa.

Documento metodologico.

Nao contem codigo.

Nao cria modelo.

Nao executa baseline.

Nao executa backtesting financeiro real.

Nao cria producao.

---

## 1. Objetivo

Criar e validar um ou mais scores compostos de pressao/calor do jogo combinando sinais H8 hoje separados, principalmente:

- shots nos ultimos minutos;
- xG nos ultimos minutos;
- graph/momentum nos ultimos minutos;
- tendencia do graph/momentum;
- possivelmente xGOT, se estiver disponivel e sem leakage.

A prioridade passa a ser sair de variaveis isoladas como:

```text
shots_last_10m_high
xg_last_10m_high
momentum_trend_positive
```

para variaveis compostas como:

```text
h8_pressure_score_last_10m
h8_hot_combo_last_10m
h8_attack_heat_last_10m
```

---

## 2. Motivacao

O H8 atual testa sinais separados. Isso ajuda, mas pode perder cenarios em que nenhum sinal isolado e forte o suficiente, enquanto a combinacao deles indica jogo quente.

Exemplo conceitual:

```text
shots_last_10m = medio
xg_last_10m = medio
momentum_trend = positivo
```

Isoladamente pode nao passar no filtro, mas junto pode indicar pressao real.

A prioridade de pesquisa agora e construir um indicador composto que responda:

```text
O jogo esta realmente esquentando?
```

E, em uma V2 por time:

```text
Quem esta esquentando o jogo?
```

---

## 3. Escopo V1

A V1 deve ser agregada do jogo, nao por equipe.

Usar apenas sinais disponiveis sem inferencia duvidosa por lado:

```text
shots_last_10m
xg_last_10m
momentum_last_10m_avg
momentum_trend_last_10m
```

Se disponivel e validado:

```text
xgot_last_10m
```

Nao usar ainda:

```text
graph por equipe via sinal do value
favorite_pressure_high
losing_team_pressure_high
```

Esses ficam para V2 apos validacao metodologica do direction/sign do graph.

---

## 4. Fontes Esperadas

### 4.1 shotmap

Pode alimentar:

```text
shots_last_10m
xg_last_10m
xgot_last_10m
big_chances_last_10m, se existir campo confiavel
```

### 4.2 graph

Pode alimentar:

```text
momentum_last_10m_avg
momentum_last_5m_avg
momentum_trend_last_10m
momentum_acceleration_last_10m
```

Na V1, usar graph como pressao agregada do jogo.

### 4.3 incidents

Pode alimentar contexto, mas nao deve substituir shotmap/graph para score principal.

Possiveis flags auxiliares:

```text
red_card_before_cutoff
goal_recent_before_cutoff
substitution_recent_before_cutoff
```

Apenas se ja forem usadas sem leakage e com timestamp ate cutoff.

---

## 5. Scores Compostos Propostos

## 5.1 Score A — Simple Hot Combo

Score binario simples:

```text
h8_hot_combo_10m_count =
  I(shots_last_10m_high)
+ I(xg_last_10m_high)
+ I(momentum_trend_positive)
```

Flags:

```text
h8_hot_combo_10m_1of3 = count >= 1
h8_hot_combo_10m_2of3 = count >= 2
h8_hot_combo_10m_3of3 = count == 3
```

Uso esperado:

```text
away_winning_by_1 + h8_hot_combo_10m_2of3
home_winning_by_1 + h8_hot_combo_10m_2of3
favorite_losing_by_1 + h8_hot_combo_10m_2of3
```

---

## 5.2 Score B — Weighted Pressure Score

Score continuo normalizado por cutoff:

```text
shots_z_cutoff = zscore(shots_last_10m dentro do cutoff)
xg_z_cutoff = zscore(xg_last_10m dentro do cutoff)
momentum_avg_z_cutoff = zscore(momentum_last_10m_avg dentro do cutoff)
momentum_trend_score = 1 se trend positivo, 0 se nao positivo
```

Score:

```text
h8_pressure_score_10m =
  0.30 * shots_z_cutoff
+ 0.35 * xg_z_cutoff
+ 0.20 * momentum_avg_z_cutoff
+ 0.15 * momentum_trend_score
```

Criar buckets por cutoff:

```text
h8_pressure_score_10m_top25
h8_pressure_score_10m_top33
h8_pressure_score_10m_top50
h8_pressure_score_10m_bottom25
```

Observacao:

Os pesos acima sao proposta inicial, nao otimizados por target. Nao ajustar pesos usando o resultado do target nesta V1 para evitar overfitting.

---

## 5.3 Score C — Shotmap Quality Combo

Foco apenas em shotmap:

```text
h8_shot_quality_score_10m =
  0.45 * shots_z_cutoff
+ 0.55 * xg_z_cutoff
```

Se xGOT existir:

```text
h8_shot_quality_score_10m_xgot =
  0.35 * shots_z_cutoff
+ 0.40 * xg_z_cutoff
+ 0.25 * xgot_z_cutoff
```

Buckets:

```text
h8_shot_quality_top25
h8_shot_quality_top33
h8_shot_quality_bottom25
```

---

## 5.4 Score D — Graph Momentum Combo

Foco apenas em graph:

```text
h8_graph_momentum_score_10m =
  0.60 * momentum_avg_z_cutoff
+ 0.40 * momentum_trend_score
```

Opcional:

```text
momentum_acceleration_last_10m
```

se ja existir ou puder ser criado sem leakage.

---

## 5.5 Score E — Conservative Hot Signal

Sinal conservador para evitar ruidos:

```text
h8_conservative_hot_10m =
  shots_last_10m_high
  AND xg_last_10m_high
  AND momentum_trend_positive
```

Esperado ter N menor, mas efeito possivelmente maior.

---

## 5.6 Score F — Pressure Without Shots Trap

Capturar jogo com graph subindo, mas sem finalizacao alta:

```text
h8_graph_only_pressure_10m =
  momentum_trend_positive
  AND shots_last_10m_low
```

Motivo:

Em resultados recentes apareceu padrao curioso como:

```text
away_winning_by_1 + shots_last_10m_low
```

com taxa boa em algumas janelas. Isso pode indicar pressao territorial sem volume de chute, ou ruido. Deve ser testado separadamente.

---

## 6. Variacoes Prioritarias para Teste

### 6.1 Com visitante vencendo por 1

```text
away_winning_by_1 + h8_hot_combo_10m_2of3
away_winning_by_1 + h8_hot_combo_10m_3of3
away_winning_by_1 + h8_pressure_score_10m_top25
away_winning_by_1 + h8_pressure_score_10m_top33
away_winning_by_1 + h8_shot_quality_top25
away_winning_by_1 + h8_graph_momentum_top25
away_winning_by_1 + h8_graph_only_pressure_10m
away_winning_by_1 + h8_conservative_hot_10m
```

### 6.2 Com mandante vencendo por 1

```text
home_winning_by_1 + h8_hot_combo_10m_2of3
home_winning_by_1 + h8_hot_combo_10m_3of3
home_winning_by_1 + h8_pressure_score_10m_top25
home_winning_by_1 + h8_pressure_score_10m_top33
home_winning_by_1 + h8_shot_quality_top25
home_winning_by_1 + h8_graph_momentum_top25
home_winning_by_1 + h8_graph_only_pressure_10m
home_winning_by_1 + h8_conservative_hot_10m
```

### 6.3 Com favorito perdendo por 1

```text
favorite_losing_by_1 + h8_hot_combo_10m_2of3
favorite_losing_by_1 + h8_pressure_score_10m_top25
favorite_losing_by_1 + h8_shot_quality_top25
favorite_losing_by_1 + h8_graph_momentum_top25
favorite_losing_by_1 + h8_conservative_hot_10m
```

### 6.4 Com favorito vencendo por 1

```text
favorite_winning_by_1 + h8_pressure_score_10m_bottom25
favorite_winning_by_1 + h8_shot_quality_bottom25
favorite_winning_by_1 + h8_graph_momentum_bottom25
favorite_winning_by_1 + h8_cold_combo_10m_2of3
```

---

## 7. Cold Combo

Criar tambem score frio para Lay Over / Back Under:

```text
h8_cold_combo_10m_count =
  I(shots_last_10m_low)
+ I(xg_last_10m_low)
+ I(momentum_trend_non_positive)
```

Flags:

```text
h8_cold_combo_10m_2of3 = count >= 2
h8_cold_combo_10m_3of3 = count == 3
```

Testar:

```text
home_winning_by_1 + h8_cold_combo_10m_2of3
away_winning_by_1 + h8_cold_combo_10m_2of3
favorite_winning_by_1 + h8_cold_combo_10m_2of3
team_winning_by_1 + h8_cold_combo_10m_2of3
```

---

## 8. Cutoffs e Janelas

Cutoffs:

```text
60
65
70
75
80, se disponivel
```

Prioridade:

```text
70
75
65
60
80
```

Targets:

```text
goal_after_cutoff
no_goal_after_cutoff
goal_60_70
no_goal_60_70
goal_60_75
no_goal_60_75
goal_65_75
no_goal_65_75
goal_65_80
no_goal_65_80
goal_70_80
no_goal_70_80
goal_70_85
no_goal_70_85
goal_75_85
no_goal_75_85
goal_75_90
no_goal_75_90
```

---

## 9. Analise Financeira Teorica

Usar odds medias travadas definidas pelo usuario:

```text
60 -> 1.30
65 -> 1.50
70 -> 1.70
75 -> 2.00
80 -> 2.40
```

Para cashout, quando houver janela com fechamento conhecido:

```text
saida_85 -> 2.90
```

Calcular:

```text
back_over_hold_ev
back_over_cashout_ev
lay_over_hold_ev
lay_over_cashout_ev, se formula operacional estiver definida
break_even_sem_cashout
break_even_com_cashout
roi_hold
roi_cashout
```

Para Back Over com cashout:

```text
stake_hedge = stake_entrada * odd_entrada / odd_saida
loss_cashout = stake_entrada - stake_hedge
profit_if_goal = stake_entrada * (odd_entrada - 1)
EV = P(gol) * profit_if_goal - P(no_goal) * loss_cashout
```

Exemplo ja validado conceitualmente:

```text
entrada @70 = 1.70
saida @85 = 2.90
stake = 100
loss_cashout = 100 - (100 * 1.70 / 2.90) = 41.38
break_even = 41.38 / (70 + 41.38) = 37.15%
```

---

## 10. Saidas Esperadas

Gerar:

```text
data/processed/reports/h8_composite_pressure_score_v1_report.json
data/processed/reports/h8_composite_pressure_score_v1_metrics.json
docs/04_RESEARCH/H8_COMPOSITE_PRESSURE_SCORE_RESULTS_V1.md
```

O markdown deve conter:

1. Resumo executivo.
2. Definicao dos scores.
3. Validacao anti-leakage.
4. Ranking estatistico.
5. Ranking financeiro sem cashout.
6. Ranking financeiro com cashout.
7. Comparacao contra features isoladas.
8. Padroes para Back Over.
9. Padroes para Lay Over / Back Under.
10. Candidatos para replicacao multi-liga.
11. Limitacoes.
12. Proximas etapas.

---

## 11. Regras Anti-Leakage

- Usar somente eventos ate o cutoff.
- Nao usar placar final como feature.
- Nao usar gols futuros como feature.
- Nao ajustar pesos usando o target desta mesma validacao.
- Nao usar odds live nao timestampadas.
- Nao inferir pressao por time via graph sem validacao previa.
- Toda feature deve indicar explicitamente a janela temporal usada.

---

## 12. Prompt para Codex

```text
Voce e o agente Codex do projeto LateGoalResearch / Crawler-Trade.

Prioridade maxima: implementar validacao exploratoria H8_COMPOSITE_PRESSURE_SCORE_V1 conforme docs/04_RESEARCH/H8_COMPOSITE_PRESSURE_SCORE_PLAN_V1.md.

Escopo:
- Nao criar modelo.
- Nao executar baseline preditivo.
- Nao fazer backtesting financeiro real.
- Nao alterar crawlers.
- Nao alterar schema de banco.
- Nao usar odds live.
- Apenas gerar features exploratorias, relatorios JSON e markdown de resultados.

Objetivo:
Criar e avaliar scores compostos de pressao/calor juntando shots, xG e graph/momentum, em vez de testar apenas variaveis isoladas.

Implementar scores:
1. h8_hot_combo_10m_count = I(shots_last_10m_high) + I(xg_last_10m_high) + I(momentum_trend_positive)
2. h8_hot_combo_10m_1of3 / 2of3 / 3of3
3. h8_cold_combo_10m_count = I(shots_last_10m_low) + I(xg_last_10m_low) + I(momentum_trend_non_positive)
4. h8_cold_combo_10m_2of3 / 3of3
5. h8_pressure_score_10m = 0.30*shots_z_cutoff + 0.35*xg_z_cutoff + 0.20*momentum_avg_z_cutoff + 0.15*momentum_trend_score
6. h8_pressure_score_10m_top25/top33/top50/bottom25
7. h8_shot_quality_score_10m = 0.45*shots_z_cutoff + 0.55*xg_z_cutoff
8. h8_shot_quality_top25/top33/bottom25
9. h8_graph_momentum_score_10m = 0.60*momentum_avg_z_cutoff + 0.40*momentum_trend_score
10. h8_graph_momentum_top25/top33/bottom25
11. h8_conservative_hot_10m = shots_last_10m_high AND xg_last_10m_high AND momentum_trend_positive
12. h8_graph_only_pressure_10m = momentum_trend_positive AND shots_last_10m_low

Avaliar combinacoes com:
- away_winning_by_1
- home_winning_by_1
- team_winning_by_1
- favorite_losing_by_1
- favorite_winning_by_1
- underdog_winning_by_1
- total_goals_3
- total_goals_3plus

Cutoffs:
- 60
- 65
- 70
- 75
- 80 se disponivel

Targets:
- goal_after_cutoff
- no_goal_after_cutoff
- goal_60_70 / no_goal_60_70
- goal_60_75 / no_goal_60_75
- goal_65_75 / no_goal_65_75
- goal_65_80 / no_goal_65_80
- goal_70_80 / no_goal_70_80
- goal_70_85 / no_goal_70_85
- goal_75_85 / no_goal_75_85
- goal_75_90 / no_goal_75_90

Calcular estatisticas:
- N
- pos
- neg
- rate
- baseline por cutoff/target
- diff_pp
- odds_ratio
- IC95
- p_value Fisher bicaudal
- classe usando MULTI_LEAGUE_REPLICATION_CLASSIFICATION_V1

Calcular financeiro teorico:
Usar odds medias travadas:
- 60 = 1.30
- 65 = 1.50
- 70 = 1.70
- 75 = 2.00
- 80 = 2.40

Para cashout em janelas que terminam aos 85, usar saida_85 = 2.90.

Calcular:
- back_over_hold_ev_per_100
- back_over_cashout_ev_per_100 quando houver odd de saida
- lay_over_hold_ev_per_100
- roi_hold
- roi_cashout
- break_even_hold
- break_even_cashout
- preferred_side

Gerar arquivos:
- data/processed/reports/h8_composite_pressure_score_v1_report.json
- data/processed/reports/h8_composite_pressure_score_v1_metrics.json
- docs/04_RESEARCH/H8_COMPOSITE_PRESSURE_SCORE_RESULTS_V1.md

Regras:
- Nao inferir pressao por time via graph nesta V1.
- Graph deve ser usado apenas como momentum agregado da partida.
- Se alguma feature necessaria nao existir, reportar NAO_DISPONIVEL_V1.
- Nao esconder resultados ruins.
- Reportar todos os testes.
```

---

## 13. Decisao Final

```text
APROVADO COMO PRIORIDADE MAXIMA DE PESQUISA
```

Proxima etapa recomendada:

```text
Executar H8_COMPOSITE_PRESSURE_SCORE_V1 via Codex.
```
