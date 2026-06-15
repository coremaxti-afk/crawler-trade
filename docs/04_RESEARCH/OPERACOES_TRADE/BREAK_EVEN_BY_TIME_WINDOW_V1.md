# BREAK_EVEN_BY_TIME_WINDOW_V1

## Objetivo

Registrar os pontos de break-even por faixa de tempo para as operacoes Back Over e Lay Over / Under Hold.

Este documento pertence ao escopo operacional do agente:

```text
06 - Trade Operations Quant
```

## Status

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
NAO E BACKTESTING FINANCEIRO REAL
NAO E PRODUCAO
```

## Curva oficial de odds medias

```text
60 = 1.40
65 = 1.60
70 = 1.80
75 = 2.00
80 = 2.45
85 = 3.35
```

## Definicao

Break-even rate e a taxa minima de acerto necessaria para nao ganhar nem perder dinheiro.

```text
Taxa > break-even => lucrativo
Taxa = break-even => zero a zero
Taxa < break-even => prejuizo
```

## Uso recomendado

Além do break-even, sempre calcular edge:

```text
edge = strike_rate - break_even_rate
```

Exemplo:

```text
Strike = 63.9%
Break-even = 50.0%
Edge = +13.9 pp
```

## Under / Lay Over — break-even por faixa

| Faixa | Break-even |
|---|---:|
| 60-75 | 57.1% |
| 60-80 | 48.3% |
| 60-85 | 40.7% |
| 60-90 | 28.6% |
| 65-75 | 75.0% |
| 65-80 | 63.4% |
| 65-85 | 53.5% |
| 65-90 | 37.5% |
| 70-85 | 63.4% |
| 70-90 | 44.4% |
| 75-85 | 71.3% |
| 75-90 | 50.0% |
| 80-90 | 59.2% |

## Over / Back Over — break-even por faixa

| Faixa | Break-even |
|---|---:|
| 60-70 | 35.7% |
| 60-75 | 42.9% |
| 60-80 | 51.7% |
| 60-85 | 59.3% |
| 60-90 | 71.4% |
| 65-75 | 25.0% |
| 65-80 | 36.6% |
| 65-85 | 46.5% |
| 65-90 | 62.5% |
| 70-80 | 24.9% |
| 70-85 | 36.6% |
| 70-90 | 55.6% |
| 75-85 | 28.7% |
| 75-90 | 50.0% |
| 80-90 | 40.8% |

## Regras operacionais

### Hold final

Quando a janela termina em 90, a operacao e hold final.

Exemplos:

```text
no_goal_60_90 = Lay Over HOLD_FINAL
goal_75_90 = Back Over HOLD_FINAL
```

### Cashout estimado

Quando a janela termina antes de 90, a operacao e cashout estimado.

Exemplos:

```text
no_goal_65_80 = Lay Over CASHOUT_ESTIMADO
goal_70_85 = Back Over CASHOUT_ESTIMADO
```

## Regra critica

Nao aprovar uma estrategia apenas pela taxa de acerto.

A decisao operacional deve comparar:

```text
strike_rate
break_even_rate
edge
EV
ROI
lucro final
drawdown
```

## Observacao

Esses break-evens usam odds medias do projeto. Com odds live timestampadas, a tabela deve ser recalculada por jogo e por timestamp real.
