# TRADE_OPERATIONS_TOP10_FINAL_PROFIT_EPL_2024_25_V1

## Objetivo

Registrar o ranking top 10 por lucro final das estrategias simuladas para a temporada:

```text
EPL 2024/25
```

Fonte de entrada:

```text
SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V2_EPL_2024_25.md
```

Este documento deve ficar separado do ranking da temporada 2025/26.

## Status

```text
PESQUISA OPERACIONAL
NAO E PRODUCAO
NAO E ROBO
NAO E BACKTESTING FINANCEIRO REAL
```

## Premissas usadas

```text
stake = 100 unidades
commission = 0
slippage = 0
spread = 0
liquidez = nao considerada
odds live timestampadas = nao disponiveis
wins = arredondado por N * taxa
```

## Curva media de odds usada

| Minuto | Odd media |
|---:|---:|
| 60 | 1.50 |
| 65 | 1.60 |
| 70 | 1.80 |
| 75 | 2.00 |
| 80 | 2.45 |
| 85 | 3.35 |

## Regra operacional aplicada

```text
se exit_minute >= 90:
    operation_settlement = HOLD_FINAL
else:
    operation_settlement = CASHOUT_ESTIMADO
```

## Regra de favorito

Favorito e definido exclusivamente pela menor odd pre-jogo 1X2:

```text
menor odd pre-jogo = favorito
```

## Formulas principais

### ROI

```text
ROI = total_profit / (N * stake)
```

### EV por trade

```text
EV_per_trade = total_profit / N
```

### Lay Over HOLD_FINAL

```text
profit_per_win = stake
loss_per_loss = -stake * (entry_odd - 1)
```

### Lay Over CASHOUT_ESTIMADO

```text
profit_per_win = stake * (1 - (entry_odd / exit_odd))
loss_per_loss = -stake * (entry_odd - 1)
```

### Back Over HOLD_FINAL

```text
profit_per_win = stake * (entry_odd - 1)
loss_per_loss = -stake
```

### Back Over CASHOUT_ESTIMADO

```text
profit_per_win = stake * (entry_odd - 1)
loss_per_loss = stake * ((entry_odd / exit_odd) - 1)
```

## Top 10 por lucro final

Ranking ordenado por lucro final absoluto, nao por ROI.

| Rank | Estrategia | Target | Tipo | N | W-L | Lucro final | ROI |
|---:|---|---|---|---:|---:|---:|---:|
| 1 | `team_winning_by_1_opp_cold_2of3` | `no_goal_65_90` | Lay Over HOLD_FINAL | 55 | 30-25 | +1500.00 | +27.3% |
| 2 | `favorite_winning_by_1_opp_cold_2of3` | `no_goal_65_90` | Lay Over HOLD_FINAL | 66 | 34-32 | +1480.00 | +22.4% |
| 3 | `team_winning_by_1_opp_cold_2of3` | `no_goal_65_90` | Lay Over HOLD_FINAL | 98 | 46-52 | +1480.00 | +15.1% |
| 4 | `big_chances_recent` | `goal_70_85` | Back Over CASHOUT_ESTIMADO | 100 | 48-52 | +1434.00 | +14.3% |
| 5 | `opponent_no_recent_key_passes` | `no_goal_65_90` | Lay Over HOLD_FINAL | 75 | 36-39 | +1260.00 | +16.8% |
| 6 | `favorite_winning_by_1_opp_cold_2of3` | `no_goal_65_90` | Lay Over HOLD_FINAL | 40 | 22-18 | +1120.00 | +28.0% |
| 7 | `opponent_no_recent_key_passes` | `no_goal_70_90` | Lay Over HOLD_FINAL | 47 | 27-20 | +1100.00 | +23.4% |
| 8 | `home_winning_by_1_visitor_pressing` | `goal_75_90` | Back Over HOLD_FINAL | 55 | 33-22 | +1100.00 | +20.0% |
| 9 | `team_winning_by_1_opp_cold_2of3` | `no_goal_70_90` | Lay Over HOLD_FINAL | 54 | 30-24 | +1080.00 | +20.0% |
| 10 | `favorite_winning_by_1_opp_cold_2of3` | `no_goal_75_90` | Lay Over HOLD_FINAL | 42 | 26-16 | +1000.00 | +23.8% |

## Leitura operacional

O ranking por lucro final da EPL 2024/25 ficou dominado por estrategias `Lay Over HOLD_FINAL`, especialmente em janelas terminadas em 90.

A principal excecao no top 10 e:

```text
big_chances_recent / goal_70_85
```

Ela entra como `Back Over CASHOUT_ESTIMADO` e depende de fechamento antes do fim.

## Ressalvas

- Ranking usa odds medias, nao odds live reais.
- Cashout antes de 90 e estimativa operacional.
- Comissao, spread, slippage e liquidez nao foram aplicados.
- O resultado nao deve ser usado como regra de producao.
- Validacao final exige odds live timestampadas.

## Veredito geral

```text
APROVADO COM RESSALVAS PARA PESQUISA OPERACIONAL
```
