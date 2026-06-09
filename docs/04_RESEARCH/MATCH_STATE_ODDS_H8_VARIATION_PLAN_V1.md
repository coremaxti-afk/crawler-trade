# MATCH_STATE_ODDS_H8_VARIATION_PLAN_V1

## Status

Plano metodologico de pesquisa.

Nao contem codigo.

Nao cria dataset.

Nao executa baseline.

Nao cria modelo.

Nao executa backtesting financeiro real.

Nao cria producao.

---

## 1. Objetivo

Explorar ao maximo os cenarios em que uma equipe esta vencendo por 1 gol, combinando:

- estado do placar;
- cutoff do jogo;
- favorito pre-jogo via odds 1X2;
- faixa simples de favoritismo;
- pressao recente H8/graph/shotmap;
- total de gols ate o cutoff;
- estrategias teoricas de Back Over +1 gol e Lay Over +1 gol.

A pergunta principal deixa de ser apenas:

```text
Qual padrao acerta mais?
```

E passa a ser:

```text
Qual padrao pode ter valor de mercado quando combinado com odd e direcao do trade?
```

---

## 2. Motivacao

Resultados anteriores mostraram que alguns estados de placar apresentam taxa alta de gol apos cutoff, por exemplo:

- visitante vencendo por 1 @60: 75.3% de gol apos 60;
- mandante vencendo por 1 @60: 70.9% de gol apos 60;
- visitante vencendo por 1 @70: 63.5% de gol apos 70;
- 3 gols no jogo @70: 63.9% de gol apos 70.

No entanto, taxa de gol nao e suficiente.

O mercado pode pagar melhor aos 70/75 minutos, entao um padrao com menor taxa pode ter EV melhor do que um padrao com maior taxa aos 60.

---

## 3. Catalogo de Faixas Simples de Favoritismo 1X2

Usar odds pre-jogo 1X2 closing.

Definicao do favorito:

```text
favorite_side = menor odd entre home, draw, away
```

Na pratica, para lado mandante/visitante:

```text
home_favorite = odd_home_close < odd_away_close AND odd_home_close < odd_draw_close
away_favorite = odd_away_close < odd_home_close AND odd_away_close < odd_draw_close
```

Faixas simples:

| Faixa | Regra pela odd do favorito | Interpretacao |
|---|---:|---|
| `favorite_strong` | `odd_favorite <= 1.60` | Favorito forte |
| `favorite_medium` | `1.61 <= odd_favorite <= 1.90` | Favorito medio |
| `favorite_light` | `1.91 <= odd_favorite <= 2.20` | Favorito leve |
| `balanced_game` | `odd_favorite > 2.20` | Jogo equilibrado / sem favorito claro |

Flags derivadas:

```text
home_strong_favorite
home_medium_favorite
home_light_favorite
away_strong_favorite
away_medium_favorite
away_light_favorite
balanced_game
```

---

## 4. Cutoffs Prioritarios

Prioridade:

1. `70` minutos
2. `60` minutos
3. `75` minutos
4. `65` minutos

Motivo:

- aos 60, taxa de gol e maior, mas odd tende menor;
- aos 70, taxa cai, mas preco pode melhorar;
- aos 75, odd pode melhorar ainda mais, mas tempo restante cai;
- aos 65 serve como ponto intermediario.

---

## 5. Targets a Gerar

Para cada cutoff:

```text
goal_after_cutoff
no_goal_after_cutoff
```

Para janelas especificas futuras:

```text
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
goal_70_90
no_goal_70_90
goal_75_85
no_goal_75_85
goal_75_90
no_goal_75_90
```

V1 pode iniciar com `goal_after_cutoff` e `no_goal_after_cutoff`, mas a pesquisa de trade deve caminhar para janelas fixas.

---

## 6. Estrategias Teoricas a Avaliar

### 6.1 Back Over +1 gol

Entrada teorica:

```text
Back Over +1 gol
```

Resultado simplificado:

```text
Se sai gol: lucro = stake * (odd_back - 1)
Se nao sai gol: prejuizo = stake
```

Formula:

```text
EV_por_100 = P(gol) * ((odd_back - 1) * 100) - P(sem_gol) * 100
break_even = 1 / odd_back
```

### 6.2 Lay Over +1 gol

Entrada teorica:

```text
Lay Over +1 gol
```

Resultado simplificado:

```text
Se nao sai gol: lucro = stake_lay
Se sai gol: prejuizo = stake_lay * (odd_lay - 1)
```

Formula:

```text
responsabilidade = stake * (odd_lay - 1)
EV_por_100 = P(sem_gol) * 100 - P(gol) * responsabilidade
break_even_sem_gol = responsabilidade / (100 + responsabilidade)
```

---

## 7. Faixas de Odds para Sensibilidade

Para cada padrao, calcular EV teorico em faixas:

```text
1.30
1.40
1.50
1.60
1.70
1.80
1.90
2.00
2.20
```

Separar:

- EV Back Over;
- EV Lay Over;
- break-even Back;
- break-even Lay;
- ROI teorico por R$100;
- odd minima para Back Over ficar positiva;
- odd maxima para Lay Over ficar positiva.

---

# PARTE A — VARIACOES PRINCIPAIS: VISITANTE VENCENDO POR 1

## 8. Visitante vencendo por 1 — variacoes basicas

Testar em cutoffs 60, 65, 70, 75:

```text
away_winning_by_1
```

Com targets:

```text
goal_after_cutoff
no_goal_after_cutoff
```

---

## 9. Visitante vencendo por 1 + favoritismo pre-jogo

Testar:

```text
away_winning_by_1 + away_favorite
away_winning_by_1 + away_strong_favorite
away_winning_by_1 + away_medium_favorite
away_winning_by_1 + away_light_favorite
away_winning_by_1 + away_underdog
away_winning_by_1 + home_favorite
away_winning_by_1 + home_strong_favorite
away_winning_by_1 + home_medium_favorite
away_winning_by_1 + home_light_favorite
away_winning_by_1 + balanced_game
```

Interpretacoes esperadas:

- visitante favorito vencendo por 1 pode indicar superioridade confirmada;
- visitante underdog vencendo por 1 pode gerar pressao do mandante;
- mandante favorito perdendo por 1 pode gerar aceleracao ofensiva;
- jogo equilibrado com visitante vencendo por 1 pode manter jogo aberto.

---

## 10. Visitante vencendo por 1 + H8/pressao recente

Testar:

```text
away_winning_by_1 + shots_last_10m_high
away_winning_by_1 + shots_last_10m_low
away_winning_by_1 + xg_last_10m_high
away_winning_by_1 + xg_last_10m_low
away_winning_by_1 + momentum_trend_positive
away_winning_by_1 + momentum_trend_non_positive
away_winning_by_1 + momentum_last_10m_avg_high
away_winning_by_1 + momentum_last_10m_avg_low
away_winning_by_1 + hot_game_2of4
away_winning_by_1 + cold_game_2of4
```

---

## 11. Visitante vencendo por 1 + pressao do time perdendo

Se o dataset permitir separar por time, testar:

```text
away_winning_by_1 + home_losing_team_shots_last_10m_high
away_winning_by_1 + home_losing_team_xg_last_10m_high
away_winning_by_1 + home_losing_team_momentum_positive
away_winning_by_1 + home_losing_team_pressure_high
```

Se nao houver separacao por time no H8 atual, Codex deve reportar como `NAO DISPONIVEL V1` e nao improvisar.

---

## 12. Visitante vencendo por 1 + total de gols

Testar:

```text
away_winning_by_1 + total_goals_1
away_winning_by_1 + total_goals_2
away_winning_by_1 + total_goals_3
away_winning_by_1 + total_goals_4plus
away_winning_by_1 + total_goals_2_or_3
away_winning_by_1 + total_goals_3plus
```

Exemplos:

- `total_goals_1`: 0x1;
- `total_goals_3`: 1x2;
- `total_goals_3plus`: jogo mais aberto.

---

## 13. Visitante vencendo por 1 + odds balance

Testar:

```text
away_winning_by_1 + match_balance_high
away_winning_by_1 + match_balance_low
away_winning_by_1 + favorite_strength_high
away_winning_by_1 + favorite_strength_low
```

---

# PARTE B — VARIACOES PRINCIPAIS: MANDANTE VENCENDO POR 1

## 14. Mandante vencendo por 1 — variacoes basicas

Testar em cutoffs 60, 65, 70, 75:

```text
home_winning_by_1
```

Com targets:

```text
goal_after_cutoff
no_goal_after_cutoff
```

---

## 15. Mandante vencendo por 1 + favoritismo pre-jogo

Testar:

```text
home_winning_by_1 + home_favorite
home_winning_by_1 + home_strong_favorite
home_winning_by_1 + home_medium_favorite
home_winning_by_1 + home_light_favorite
home_winning_by_1 + home_underdog
home_winning_by_1 + away_favorite
home_winning_by_1 + away_strong_favorite
home_winning_by_1 + away_medium_favorite
home_winning_by_1 + away_light_favorite
home_winning_by_1 + balanced_game
```

Interpretacoes esperadas:

- mandante favorito vencendo por 1 pode controlar o jogo;
- mandante underdog vencendo por 1 pode sofrer pressao;
- visitante favorito perdendo por 1 pode gerar aceleracao ofensiva;
- jogo equilibrado pode manter troca ofensiva.

---

## 16. Mandante vencendo por 1 + H8/pressao recente

Testar:

```text
home_winning_by_1 + shots_last_10m_high
home_winning_by_1 + shots_last_10m_low
home_winning_by_1 + xg_last_10m_high
home_winning_by_1 + xg_last_10m_low
home_winning_by_1 + momentum_trend_positive
home_winning_by_1 + momentum_trend_non_positive
home_winning_by_1 + momentum_last_10m_avg_high
home_winning_by_1 + momentum_last_10m_avg_low
home_winning_by_1 + hot_game_2of4
home_winning_by_1 + cold_game_2of4
```

---

## 17. Mandante vencendo por 1 + pressao do visitante perdendo

Se o dataset permitir separar por time, testar:

```text
home_winning_by_1 + away_losing_team_shots_last_10m_high
home_winning_by_1 + away_losing_team_xg_last_10m_high
home_winning_by_1 + away_losing_team_momentum_positive
home_winning_by_1 + away_losing_team_pressure_high
```

Se nao houver separacao por time no H8 atual, Codex deve reportar como `NAO DISPONIVEL V1`.

---

## 18. Mandante vencendo por 1 + total de gols

Testar:

```text
home_winning_by_1 + total_goals_1
home_winning_by_1 + total_goals_2
home_winning_by_1 + total_goals_3
home_winning_by_1 + total_goals_4plus
home_winning_by_1 + total_goals_2_or_3
home_winning_by_1 + total_goals_3plus
```

---

## 19. Mandante vencendo por 1 + odds balance

Testar:

```text
home_winning_by_1 + match_balance_high
home_winning_by_1 + match_balance_low
home_winning_by_1 + favorite_strength_high
home_winning_by_1 + favorite_strength_low
```

---

# PARTE C — VARIACOES SIMETRICAS E DERIVADAS

## 20. Time vencendo por 1, independente do lado

Testar:

```text
team_winning_by_1
team_winning_by_1 + favorite_winning_by_1
team_winning_by_1 + underdog_winning_by_1
team_winning_by_1 + favorite_losing_by_1
team_winning_by_1 + favorite_pressure_high
team_winning_by_1 + losing_team_pressure_high
team_winning_by_1 + total_goals_1
team_winning_by_1 + total_goals_3plus
team_winning_by_1 + shots_last_10m_high
team_winning_by_1 + shots_last_10m_low
```

---

## 21. Favorito perdendo por 1

Testar:

```text
favorite_losing_by_1
favorite_losing_by_1 + favorite_strong
favorite_losing_by_1 + favorite_medium
favorite_losing_by_1 + favorite_light
favorite_losing_by_1 + shots_last_10m_high
favorite_losing_by_1 + xg_last_10m_high
favorite_losing_by_1 + momentum_trend_positive
favorite_losing_by_1 + total_goals_1
favorite_losing_by_1 + total_goals_3plus
```

---

## 22. Underdog vencendo por 1

Testar:

```text
underdog_winning_by_1
underdog_winning_by_1 + favorite_strong
underdog_winning_by_1 + favorite_medium
underdog_winning_by_1 + favorite_pressure_high
underdog_winning_by_1 + shots_last_10m_high
underdog_winning_by_1 + total_goals_3plus
```

---

# PARTE D — PRIORIDADES DE EXECUCAO

## 23. Prioridade 1 — Exploracao principal @70

Executar primeiro:

```text
away_winning_by_1 @70 + away_favorite
away_winning_by_1 @70 + away_underdog
away_winning_by_1 @70 + home_favorite
away_winning_by_1 @70 + shots_last_10m_high
away_winning_by_1 @70 + momentum_trend_positive
away_winning_by_1 @70 + total_goals_3
away_winning_by_1 @70 + total_goals_3plus
away_winning_by_1 @70 + match_balance_high
home_winning_by_1 @70 + home_favorite
home_winning_by_1 @70 + home_underdog
home_winning_by_1 @70 + away_favorite
home_winning_by_1 @70 + shots_last_10m_high
home_winning_by_1 @70 + momentum_trend_positive
home_winning_by_1 @70 + total_goals_3
home_winning_by_1 @70 + total_goals_3plus
home_winning_by_1 @70 + match_balance_high
favorite_losing_by_1 @70
underdog_winning_by_1 @70
team_winning_by_1 @70 + shots_last_10m_high
team_winning_by_1 @70 + low_pressure_last_10m
```

---

## 24. Prioridade 2 — Comparacao @60 vs @75

Executar as mesmas familias em:

```text
cutoff 60
cutoff 75
```

Motivo:

- 60 mede taxa alta, odd possivelmente baixa;
- 75 mede taxa menor, odd possivelmente maior;
- comparar EV por faixa de odd.

---

## 25. Prioridade 3 — Janelas curtas

Depois do ranking geral, testar:

```text
goal_70_80
no_goal_70_80
goal_70_85
no_goal_70_85
goal_75_85
no_goal_75_85
```

Isto e mais proximo de trade real do que `goal_after_cutoff` ate o fim.

---

# PARTE E — SAIDA ESPERADA

## 26. Tabela estatistica esperada

Para cada variacao:

| Campo | Descricao |
|---|---|
| `variation_name` | Nome padronizado da variacao |
| `cutoff` | Minuto do cutoff |
| `target` | Target usado |
| `N` | Amostra |
| `pos` | Gols ou no-gols conforme target |
| `neg` | Complemento |
| `rate` | Taxa observada |
| `baseline_cutoff` | Taxa media do target no cutoff |
| `diff_pp` | Diferenca em pontos percentuais |
| `odds_ratio` | OR vs resto |
| `ci95` | Intervalo de confianca |
| `p_value` | Fisher exact test |
| `class` | PROMISSOR / OBSERVAR / DESCARTAR |
| `market_note` | Back Over / Lay Over / cuidado |

---

## 27. Tabela EV esperada

Para cada variacao e cada odd simulada:

| Campo | Descricao |
|---|---|
| `variation_name` | Nome da variacao |
| `cutoff` | Cutoff |
| `N` | Amostra |
| `p_goal` | Probabilidade observada de gol |
| `p_no_goal` | Probabilidade observada de no-goal |
| `odd` | Odd simulada |
| `back_over_ev_per_100` | EV Back Over por R$100 |
| `lay_over_ev_per_100` | EV Lay Over por R$100 |
| `back_over_roi` | ROI Back Over |
| `lay_over_roi` | ROI Lay Over |
| `back_break_even` | Break-even Back |
| `lay_break_even_no_goal` | Break-even Lay |
| `preferred_side` | Back Over / Lay Over / Neutro |

---

# PARTE F — CRITERIOS DE CLASSIFICACAO

## 28. Classificacao estatistica

### PROMISSOR

```text
N >= 40
diff >= +8 p.p.
OR > 1.50
p-value < 0.10
sem concentracao extrema
```

### OBSERVAR

```text
N >= 25
diff >= +4 p.p. ou edge operacional forte
OR > 1.20 ou EV teorico positivo em odds plausiveis
```

### DESCARTAR

```text
N pequeno demais
diff fraca
p-value fraco
sem EV teorico em odds plausiveis
```

---

## 29. Classificacao de mercado

Separar do criterio estatistico.

### EV_POSITIVO_TEORICO

Variacao que, em odds plausiveis, tem EV positivo para Back Over ou Lay Over.

### EV_DEPENDE_PRECO

Variacao com taxa interessante, mas que precisa de odd minima/maxima especifica.

### EV_NEGATIVO

Variacao que nao fica positiva em odds plausiveis.

---

# PARTE G — PROMPT PARA CODEX

## 30. Prompt sugerido para execucao

```text
Voce e o agente Codex do projeto LateGoalResearch.

Tarefa: implementar validacao exploratoria MATCH_STATE_ODDS_H8_VARIATION_V1 conforme o documento docs/04_RESEARCH/MATCH_STATE_ODDS_H8_VARIATION_PLAN_V1.md.

Escopo:
- Nao alterar banco de dados.
- Nao alterar schema.
- Nao alterar crawlers.
- Nao criar modelo.
- Nao executar baseline.
- Nao fazer backtesting financeiro real.
- Apenas gerar datasets/report exploratorios e markdown de resultados.

Entradas esperadas:
- dataset in-game com score ate cutoffs 60/65/70/75;
- dataset H8 com features por cutoff;
- odds_features_v1 com odds 1X2 closing e favorite_side/favorite_strength/match_balance;
- targets goal_after_cutoff/no_goal_after_cutoff derivados sem leakage.

Implementar:
1. Catalogar faixa simples de favorito:
   - favorite_strong: odd_favorite <= 1.60
   - favorite_medium: 1.61 <= odd_favorite <= 1.90
   - favorite_light: 1.91 <= odd_favorite <= 2.20
   - balanced_game: odd_favorite > 2.20
2. Criar flags home_favorite, away_favorite, home/away strong/medium/light favorite.
3. Criar flags home_winning_by_1, away_winning_by_1, team_winning_by_1, favorite_losing_by_1, underdog_winning_by_1.
4. Criar variacoes listadas no plano, priorizando cutoff 70 e depois 60/75.
5. Para cada variacao calcular N, pos, neg, taxa, baseline cutoff, diff, OR, IC95, p-value e classificacao.
6. Calcular EV teorico para Back Over e Lay Over por R$100 nas odds: 1.30, 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.20.
7. Gerar reports:
   - data/processed/reports/match_state_odds_h8_variation_v1_report.json
   - data/processed/reports/match_state_odds_h8_variation_v1_metrics.json
   - docs/04_RESEARCH/MATCH_STATE_ODDS_H8_VARIATION_RESULTS_V1.md

Regras anti-leakage:
- usar somente informacoes ate o cutoff nas features de jogo;
- odds permitidas apenas pre-game closing 1X2;
- nao usar odds live;
- nao usar placar final como feature;
- target somente como resposta;
- se feature por time nao existir, reportar como NAO DISPONIVEL V1, sem improvisar.
```

---

## 31. Decisao Final deste Plano

```text
APROVADO COMO PLANO METODOLOGICO DE PESQUISA
```

Nao autoriza:

- trade real;
- modelo;
- baseline;
- backtesting financeiro real;
- automacao;
- producao.

Proxima etapa recomendada:

```text
Executar MATCH_STATE_ODDS_H8_VARIATION_V1 via Codex.
```
