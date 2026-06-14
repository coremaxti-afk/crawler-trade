# SPORTMONKS_SEASON_COMPARISON_2024_25_VS_2025_26_V1

## Status

```text
APROVADO COM RESSALVAS
```

Este documento registra o parecer comparativo entre as entregas SportMonks Team-Side Strategy Discovery da EPL 2024/25 e EPL 2025/26.

---

## Resumo Executivo

A temporada EPL 2024/25 fortaleceu a leitura estatistica encontrada na EPL 2025/26.

A principal conclusao e que a frente SportMonks nao deve ser vista apenas como descoberta de estrategias Under. A comparacao entre temporadas mostrou que a familia Over, especialmente Back Over tardio, pode ser mais interessante operacionalmente por causa do payoff maior das odds.

Veredito:

```text
APROVADO COM RESSALVAS, COM FOCO EM PLAYBOOKS OPERACIONAIS
```

---

## Comparacao Geral

### EPL 2025/26

Principais achados:

- `home_winning_by_1_visitor_pressing` em 75 -> goal_75_90;
- `favorite_winning_by_1_opp_cold_2of3` em cenarios no-goal;
- `team_winning_by_1_opp_cold_2of3` em cenarios no-goal;
- `both_teams_cold_2of3` em cenarios no-goal.

### EPL 2024/25

A entrega 2024/25 aumentou o volume de estrategias promissoras e confirmou familias da 2025/26.

Resumo reportado:

```text
411 combos avaliados
25 PROMISSOR
233 OBSERVACAO
153 DESCARTADO
```

---

## Estrategias Confirmadas Entre Temporadas

### 1. home_winning_by_1_visitor_pressing

Na EPL 2025/26:

```text
75 -> goal_75_90
N=36
acerto=63.9%
diff=+16.8 pp
p=0.041
```

Na EPL 2024/25:

```text
75 -> goal_75_90
N=55
acerto=60.0%
diff=+12.4 pp
p=0.068
```

Parecer:

```text
Muito promissora para Back Over 75.
```

Esta e uma das estrategias mais importantes para avaliacao operacional pelo Agente 06, porque combina taxa razoavel com odds tardias potencialmente altas.

---

### 2. favorite_winning_by_1_opp_cold_2of3

Na EPL 2025/26:

```text
65 -> no_goal_65_80
N=32
acerto=81.3%
diff=+14.7 pp
p=0.085
```

Na EPL 2024/25:

```text
65 -> no_goal_65_90
N=40
acerto=55.0%
diff=+17.1 pp
p=0.0287
```

Parecer:

```text
A logica se confirma, mas o melhor target muda por temporada.
```

Em 2024/25 aparece mais como Under Hold ate o fim; em 2025/26 aparece forte em janela curta 65-80.

---

### 3. team_winning_by_1_opp_cold_2of3

Na EPL 2024/25:

```text
65 -> no_goal_65_90
N=55
acerto=54.5%
diff=+16.7 pp
p=0.0095
```

Parecer:

```text
Estatisticamente forte, mas precisa avaliacao operacional.
```

A taxa absoluta e baixa para Under Hold, entao a viabilidade depende de odds e break-even.

---

## Novas Frentes Fortes em 2024/25

### 1. favorite_losing_pressure_high_2of3

```text
60 -> goal_60_75
N=32
acerto=53.1%
diff=+17.9 pp
p=0.0374
```

Parecer:

```text
Excelente candidata para Back Over 60-75.
```

Logica operacional:

```text
Favorito perdendo e pressionando.
```

---

### 2. underdog_winning_favorite_pressing_2of3

```text
60 -> goal_60_75
N=32
acerto=53.1%
diff=+17.9 pp
p=0.0374
```

Parecer:

```text
Leitura inversa da estrategia anterior.
```

Logica operacional:

```text
Azarao vencendo + favorito pressionando.
```

---

### 3. big_chances_recent

Exemplos reportados:

```text
60 -> goal_60_75
N=41
acerto=51.2%
diff=+16.0 pp
p=0.0423
```

```text
70 -> goal_70_85
N=100
acerto=48.0%
diff=+11.2 pp
p=0.0145
```

Parecer:

```text
Uma das frentes Over mais robustas por volume.
```

Deve ser encaminhada ao Agente 06 para avaliacao de EV, break-even e sensibilidade a odds.

---

## Familias Principais Consolidadas

### 1. Back Over tardio

```text
home_winning_by_1_visitor_pressing 75 -> 90
```

Prioridade operacional alta.

---

### 2. Back Over de pressao

```text
favorite_losing_pressure_high_2of3
underdog_winning_favorite_pressing_2of3
big_chances_recent
```

Prioridade operacional alta.

---

### 3. Under Hold

```text
favorite_winning_by_1_opp_cold_2of3
team_winning_by_1_opp_cold_2of3
both_teams_cold_2of3
```

Prioridade operacional media/alta, dependendo de odds e janela.

---

## Ranking Recomendado para Proxima Avaliacao Operacional

1. `home_winning_by_1_visitor_pressing` 75 -> goal_75_90
2. `favorite_losing_pressure_high_2of3` 60 -> goal_60_75
3. `underdog_winning_favorite_pressing_2of3` 60 -> goal_60_75
4. `big_chances_recent` 70 -> goal_70_85
5. `favorite_winning_by_1_opp_cold_2of3` 65 -> no_goal_65_90
6. `team_winning_by_1_opp_cold_2of3` 65 -> no_goal_65_90
7. `both_teams_cold_2of3` 60 -> no_goal_60_80 / no_goal_60_90

---

## Decisao Operacional

A comparacao 24/25 vs 25/26 sugere que:

```text
A linha Over pode ser mais promissora financeiramente que a linha Under.
```

Motivo:

```text
Taxas de 48% a 64% em janelas tardias podem ser muito lucrativas se as odds forem altas.
```

Portanto, as proximas avaliacoes do Agente 06 devem priorizar:

```text
Back Over 75
Back Over 70-85
Back Over 60-75 com favorito pressionando
```

---

## Ressalvas

- Odds live historicas timestampadas continuam fora de escopo.
- Simulacoes devem usar odds medias observadas do projeto.
- Simulacoes devem ser marcadas como ESTIMATIVA OPERACIONAL.
- Nao e backtesting financeiro real.
- Nenhuma estrategia deve ser promovida para robo, producao ou trade real.

---

## Proxima Frente Recomendada

```text
SPORTMONKS_OPERATIONAL_PLAYBOOKS_V1
```

Objetivo:

Transformar as familias confirmadas em playbooks operacionais com:

- regra de entrada;
- mercado sugerido;
- janela;
- odds minima estimada;
- EV estimado;
- criterio de saida;
- veredito do Agente 06.

---

## Documentos Relacionados

- docs/04_RESEARCH/SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V1.md
- docs/04_RESEARCH/SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V2.md
- docs/04_RESEARCH/SPORTMONKS_OPERATIONAL_ACTION_PLAN_V1.md
- docs/00_AGENTS/GOVERNANCE_V2.md
- docs/00_AGENTS/CHAIN_OF_COMMAND.md
