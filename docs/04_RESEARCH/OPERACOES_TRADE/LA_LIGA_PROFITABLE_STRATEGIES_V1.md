# LA_LIGA_PROFITABLE_STRATEGIES_V1

## Objetivo

Registrar as estrategias lucrativas encontradas na La Liga para futura lapidacao em playbooks operacionais.

Este documento pertence ao escopo do agente:

```text
06 - Trade Operations Quant
```

## Status

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
NAO E BACKTESTING FINANCEIRO REAL
NAO E PRODUCAO
```

## Curva oficial de odds usada

```text
60 = 1.40
65 = 1.60
70 = 1.80
75 = 2.00
80 = 2.45
85 = 3.35
```

## Premissas

```text
stake = 100
commission = 0
slippage = 0
spread = 0
liquidez = nao considerada
odds live timestampadas = nao disponiveis
```

## Regras operacionais

```text
Target goal_* = Back Over
Target no_goal_* = Lay Over / Under Hold
```

```text
janela terminada em 90 = HOLD_FINAL
janela terminada antes de 90 = CASHOUT_ESTIMADO
```

## Back Over — estrategias lucrativas

### 1. favorite_drawing_pressure_high_2of3

Leitura:

```text
Favorito empatando + pressao alta = sinal forte de gol.
Principal candidato de Back Over na La Liga.
```

| Entrada | Target | Janela | N | Strike | Diff | p-value | Tipo | Lucro estimado | ROI | EV/trade | Break-even |
|---:|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 60 | `goal_60_75` | last_10m | 59 | 50.8% | +15.8 pp | 0.010 | Back Over CASHOUT_ESTIMADO | +330.0 | +5.6% | +5.6 | 42.9% |
| 60 | `goal_60_80` | last_10m | 59 | 55.9% | +14.9 pp | 0.019 | Back Over CASHOUT_ESTIMADO | +205.7 | +3.5% | +3.5 | 51.7% |
| 65 | `goal_65_80` | last_10m | 55 | 45.5% | +14.1 pp | 0.023 | Back Over CASHOUT_ESTIMADO | +459.2 | +8.3% | +8.3 | 36.6% |

Melhor recorte financeiro:

```text
favorite_drawing_pressure_high_2of3 | 65 | goal_65_80
```

### 2. away_winning_by_1_home_pressing

Leitura:

```text
Visitante vencendo por 1 + mandante pressionando.
Versao invertida da logica home_winning_by_1_visitor_pressing.
```

| Entrada | Target | Janela | N | Strike | Diff | p-value | Tipo | Lucro estimado | ROI | EV/trade | Break-even |
|---:|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 70 | `goal_70_90` | last_15m | 49 | 65.3% | +13.7 pp | 0.055 | Back Over HOLD_FINAL | +860.0 | +17.6% | +17.6 | 55.6% |
| 70 | `goal_70_90` | last_10m | 43 | 65.1% | +13.5 pp | 0.083 | Back Over HOLD_FINAL | +740.0 | +17.2% | +17.2 | 55.6% |
| 75 | `goal_75_90` | last_15m | 48 | 56.3% | +12.0 pp | 0.098 | Back Over HOLD_FINAL | +600.0 | +12.5% | +12.5 | 50.0% |

Melhor recorte financeiro:

```text
away_winning_by_1_home_pressing | 70 | goal_70_90 | last_15m
```

### 3. key_passes_recent_high

Leitura:

```text
Volume alto e boa significancia estatistica.
Sinal de gol por key passes recentes.
```

| Entrada | Target | Janela | N | Strike | Diff | p-value | Tipo | Lucro estimado | ROI | EV/trade | Break-even |
|---:|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 65 | `goal_65_85` | last_10m | 205 | 49.8% | +9.5 pp | 0.0015 | Back Over CASHOUT_ESTIMADO | +739.4 | +3.6% | +3.6 | 46.5% |

## Lay Over / Under Hold — estrategias lucrativas

### 1. favorite_winning_by_1_opp_cold_2of3

Leitura:

```text
Favorito vencendo por 1 + adversario frio.
Na La Liga, o sinal aparece mais forte em janela curta do que necessariamente em hold ate 90.
```

| Entrada | Target | Janela | N | Strike | Diff | p-value | Tipo | Lucro estimado | ROI | EV/trade | Break-even |
|---:|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 60 | `no_goal_60_80` | last_10m | 37 | 73.0% | +14.0 pp | 0.087 | Lay Over CASHOUT_ESTIMADO | +757.0 | +20.5% | +20.5 | 48.3% |
| 65 | `no_goal_65_80` | last_5m | 63 | 69.8% | +10.9 pp | 0.082 | Lay Over CASHOUT_ESTIMADO | +386.0 | +6.1% | +6.1 | 63.4% |
| 70 | `no_goal_70_85` | last_10m | 41 | 80.5% | +11.5 pp | 0.119 | Lay Over CASHOUT_ESTIMADO | +887.0 | +21.6% | +21.6 | 63.4% |

Melhor recorte financeiro:

```text
favorite_winning_by_1_opp_cold_2of3 | 70 | no_goal_70_85
```

### 2. both_teams_cold_2of3

Leitura:

```text
Jogo frio geral.
Destaque forte para Lay Over tardio 75-90.
```

| Entrada | Target | Janela | N | Strike | Diff | p-value | Tipo | Lucro estimado | ROI | EV/trade | Break-even |
|---:|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|
| 75 | `no_goal_75_90` | last_5m | 136 | 66.2% | +10.4 pp | 0.0076 | Lay Over HOLD_FINAL | +4400.0 | +32.4% | +32.4 | 50.0% |
| 75 | `no_goal_75_90` | last_15m | 110 | 65.5% | +9.7 pp | 0.029 | Lay Over HOLD_FINAL | +3400.0 | +30.9% | +30.9 | 50.0% |
| 70 | `no_goal_70_85` | last_15m | 86 | 79.1% | +10.1 pp | 0.035 | Lay Over CASHOUT_ESTIMADO | +1706.0 | +19.8% | +19.8 | 63.4% |

Melhor recorte financeiro:

```text
both_teams_cold_2of3 | 75 | no_goal_75_90 | last_5m
```

## Ranking por lucro estimado

| Rank | Estrategia | Operacao | Target | N | Lucro estimado | ROI | EV/trade |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | `both_teams_cold_2of3` | Lay Over | `no_goal_75_90` last_5m | 136 | +4400.0 | +32.4% | +32.4 |
| 2 | `both_teams_cold_2of3` | Lay Over | `no_goal_75_90` last_15m | 110 | +3400.0 | +30.9% | +30.9 |
| 3 | `both_teams_cold_2of3` | Lay Over | `no_goal_70_85` last_15m | 86 | +1706.0 | +19.8% | +19.8 |
| 4 | `favorite_winning_by_1_opp_cold_2of3` | Lay Over | `no_goal_70_85` last_10m | 41 | +887.0 | +21.6% | +21.6 |
| 5 | `away_winning_by_1_home_pressing` | Back Over | `goal_70_90` last_15m | 49 | +860.0 | +17.6% | +17.6 |
| 6 | `favorite_winning_by_1_opp_cold_2of3` | Lay Over | `no_goal_60_80` last_10m | 37 | +757.0 | +20.5% | +20.5 |
| 7 | `away_winning_by_1_home_pressing` | Back Over | `goal_70_90` last_10m | 43 | +740.0 | +17.2% | +17.2 |
| 8 | `key_passes_recent_high` | Back Over | `goal_65_85` last_10m | 205 | +739.4 | +3.6% | +3.6 |
| 9 | `away_winning_by_1_home_pressing` | Back Over | `goal_75_90` last_15m | 48 | +600.0 | +12.5% | +12.5 |
| 10 | `favorite_drawing_pressure_high_2of3` | Back Over | `goal_65_80` last_10m | 55 | +459.2 | +8.3% | +8.3 |

## Candidatos prioritarios para playbook La Liga

### Back Over

```text
1. away_winning_by_1_home_pressing | 70 | goal_70_90 | last_15m
2. favorite_drawing_pressure_high_2of3 | 65 | goal_65_80 | last_10m
3. key_passes_recent_high | 65 | goal_65_85 | last_10m
```

### Lay Over / Under Hold

```text
1. both_teams_cold_2of3 | 75 | no_goal_75_90 | last_5m
2. both_teams_cold_2of3 | 70 | no_goal_70_85 | last_15m
3. favorite_winning_by_1_opp_cold_2of3 | 70 | no_goal_70_85 | last_10m
```

## Veredito geral

```text
APROVADO COM RESSALVAS PARA PESQUISA OPERACIONAL
```

As estrategias sao lucrativas na estimativa operacional, mas ainda dependem de validacao com odds live timestampadas, comissao, spread, slippage, liquidez e drawdown trade a trade.
