# SPORTMONKS_2024_25_VS_2025_26_COMPARATIVE_STRATEGY_NOTES_V1

## Status

```text
NOTAS DE PESQUISA PARA LAPIDACAO FUTURA
```

Este documento registra a comparação qualitativa entre a entrega SportMonks EPL 2024/25 e a frente EPL 2025/26 para uso futuro na lapidação das estratégias.

Não representa produção, robô, trade real ou backtesting financeiro real.

---

## Parecer Executivo

```text
APROVADO COM RESSALVAS, MAS MAIS FORTE QUE A V1 ISOLADA
```

A temporada EPL 2024/25 confirmou várias famílias observadas na EPL 2025/26 e revelou novas frentes promissoras de Over.

A leitura geral é que a frente SportMonks ganhou força porque agora existem sinais repetidos em temporadas diferentes.

---

## Resultado Geral 2024/25

A entrega EPL 2024/25 reportou:

```text
411 combos avaliados
25 PROMISSOR
233 OBSERVACAO
153 DESCARTADO
```

Comparado com a 2025/26, a 2024/25 trouxe:

- mais volume;
- mais variedade;
- mais confirmações de famílias estratégicas;
- novas frentes de Back Over com pressão.

---

# Estratégias Confirmadas Entre Temporadas

## 1. home_winning_by_1_visitor_pressing

Na EPL 2025/26, já era a principal candidata Over:

```text
cutoff 75
target goal_75_90
N = 36
acerto = 63.9%
diff = +16.8 pp
p = 0.041
```

Na EPL 2024/25 apareceu novamente:

```text
cutoff 75
target goal_75_90
N = 55
acerto = 60.0%
diff = +12.4 pp
p = 0.068
```

Parecer:

```text
Muito promissora.
Uma das principais candidatas para Back Over 75.
```

Interpretação operacional:

```text
Mandante vencendo por 1, mas visitante pressionando no fim.
```

Essa família deve ser priorizada para playbook operacional.

---

## 2. favorite_winning_by_1_opp_cold_2of3

Na EPL 2025/26, apareceu forte em janela curta:

```text
cutoff 65
target no_goal_65_80
N = 32
acerto = 81.3%
diff = +14.7 pp
p = 0.085
```

Na EPL 2024/25 apareceu forte em hold:

```text
cutoff 65
target no_goal_65_90
N = 40
acerto = 55.0%
diff = +17.1 pp
p = 0.0287
```

Parecer:

```text
Confirma a lógica favorita + adversário frio.
Mas o melhor target varia por temporada.
```

Interpretação:

```text
Na 2025/26 pareceu mais forte em janela curta 65-80.
Na 2024/25 apareceu como Under Hold até o fim.
```

Precisa lapidação antes de virar playbook final.

---

## 3. team_winning_by_1_opp_cold_2of3

Na EPL 2025/26 já era uma frente forte de no-goal curto.

Na EPL 2024/25 apareceu como:

```text
cutoff 65
target no_goal_65_90
N = 55
acerto = 54.5%
diff = +16.7 pp
p = 0.0095
```

Parecer:

```text
Estatisticamente forte.
Operacionalmente depende de odds e avaliação do Agente 06.
```

Ressalva:

```text
A taxa absoluta é baixa para Under Hold, mas pode ser aceitável dependendo da odd e do payoff.
```

---

# Novas Frentes Fortes em 2024/25

## 1. favorite_losing_pressure_high_2of3

Resultado:

```text
cutoff 60
target goal_60_75
N = 32
acerto = 53.1%
diff = +17.9 pp
p = 0.0374
```

Parecer:

```text
Excelente descoberta.
Favorito perdendo e pressionando parece candidato forte para Back Over 60-75.
```

Interpretação:

```text
Quando o favorito está atrás no placar e gera pressão alta, o mercado de Over em janela curta pode ser mais valioso que estratégias Under de alta taxa.
```

---

## 2. underdog_winning_favorite_pressing_2of3

Resultado:

```text
cutoff 60
target goal_60_75
N = 32
acerto = 53.1%
diff = +17.9 pp
p = 0.0374
```

Parecer:

```text
Muito forte e operacionalmente lógica.
```

Interpretação:

```text
É a leitura inversa da anterior: azarão vencendo e favorito pressionando.
```

Essa família deve ser avaliada junto com favorite_losing_pressure_high_2of3, pois podem representar o mesmo fenômeno por nomenclaturas diferentes.

---

## 3. big_chances_recent

Apareceu em múltiplos targets:

```text
cutoff 60
target goal_60_75
N = 41
acerto = 51.2%
diff = +16.0 pp
p = 0.0423
```

E também:

```text
cutoff 70
target goal_70_85
N = 100
acerto = 48.0%
diff = +11.2 pp
p = 0.0145
```

Parecer:

```text
Uma das frentes mais robustas por volume.
Deve ser enviada ao Agente 06.
```

Interpretação:

```text
Big chances recentes podem ser um sinal simples e forte para Back Over em janela curta.
```

---

# Famílias Estratégicas Prioritárias

## 1. Back Over Tardio

Principal estratégia:

```text
home_winning_by_1_visitor_pressing
75 -> goal_75_90
```

Motivo:

- confirmou em duas temporadas;
- odds no minuto 75 tendem a ser mais altas;
- taxa de acerto não precisa ser tão alta para EV positivo.

---

## 2. Back Over de Pressão

Estratégias:

```text
favorite_losing_pressure_high_2of3
underdog_winning_favorite_pressing_2of3
big_chances_recent
```

Motivo:

- pressão real por lado/time;
- bom diff vs baseline;
- boa lógica operacional;
- payoff potencialmente interessante.

---

## 3. Under Hold / No Goal

Estratégias:

```text
favorite_winning_by_1_opp_cold_2of3
team_winning_by_1_opp_cold_2of3
both_teams_cold_2of3
```

Motivo:

- confirma a linha histórica de jogo frio;
- precisa de avaliação de odds porque taxa absoluta pode variar bastante por target;
- mais adequada para hold ou janela longa que para cashout curto.

---

# Prioridade Recomendada para Lapidação

Ordem sugerida:

```text
1. home_winning_by_1_visitor_pressing 75 -> goal_75_90
2. favorite_losing_pressure_high_2of3 60 -> goal_60_75
3. underdog_winning_favorite_pressing_2of3 60 -> goal_60_75
4. big_chances_recent 70 -> goal_70_85
5. favorite_winning_by_1_opp_cold_2of3 65 -> no_goal_65_90
```

---

# Pontos para Lapidação Futura

## 1. Consolidar nomenclaturas equivalentes

Possível equivalência:

```text
favorite_losing_pressure_high_2of3
underdog_winning_favorite_pressing_2of3
```

Ambas podem representar o mesmo cenário:

```text
favorito perdendo + pressionando
```

## 2. Separar home/away

Especialmente em:

```text
home_winning_by_1_visitor_pressing
```

Verificar se o efeito vem de:

- mandante recuando;
- visitante pressionando;
- viés de jogo em casa;
- placar de 1 gol.

## 3. Testar estabilidade de cutoff

Comparar:

- 60 vs 65;
- 70 vs 75;
- 75 vs 80, se houver dados;
- janelas 5m, 10m e 15m.

## 4. Enviar ao Agente 06

Todas as famílias acima devem passar pelo Agente 06, pois:

```text
Taxa estatística alta nao implica lucro.
Taxa estatística baixa pode ser lucrativa se a odd for alta.
```

---

# Decisão Atual

```text
MANTER COMO FRENTE PRIORITÁRIA PARA LAPIDAÇÃO
```

Não avançar para:

- robô;
- produção;
- trade real;
- backtesting financeiro real.

Próxima fase recomendada:

```text
SPORTMONKS_OPERATIONAL_PLAYBOOKS_V1
```

Objetivo:

```text
Transformar as famílias confirmadas em playbooks operacionais estimados com odds médias e avaliação do Agente 06.
```
