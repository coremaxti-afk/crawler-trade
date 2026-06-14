# TRADE_OPERATIONS_TOP10_RENTABILITY_RANKING_V1

## Objetivo

Registrar o ranking operacional de rentabilidade das estrategias descobertas em:

```text
SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V2.md
```

Este documento pertence ao escopo do agente:

```text
06 - Trade Operations Quant
```

Ele transforma estrategias ja encontradas em metricas financeiras operacionais.

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
```

As odds usadas sao odds medias observadas no mercado Proximo Gol.

## Regra de favorito

Favorito e definido exclusivamente por odd pre-jogo 1X2:

```text
menor odd pre-jogo = favorito
```

Exemplos:

```text
AvgH < AvgA => mandante favorito
AvgA < AvgH => visitante favorito
```

Nao usar nome do time, mando de campo, tabela ou forca subjetiva para definir favorito.

## Curva media de odds usada

Back Over equivalente:

| Minuto | Odd media |
|---:|---:|
| 60 | 1.50 |
| 65 | 1.60 |
| 70 | 1.80 |
| 75 | 2.00 |
| 80 | 2.45 |
| 85 | 3.35 |

## Regra operacional critica

Antes de calcular lucro, ROI, EV ou break-even, classificar a operacao:

```text
se exit_minute >= 90:
    operation_settlement = HOLD_FINAL
else:
    operation_settlement = CASHOUT_ESTIMADO
```

Exemplos:

```text
no_goal_60_90 = HOLD_FINAL
no_goal_60_80 = CASHOUT_ESTIMADO
no_goal_65_80 = CASHOUT_ESTIMADO
no_goal_70_85 = CASHOUT_ESTIMADO
goal_75_90 = HOLD_FINAL
goal_70_80 = CASHOUT_ESTIMADO
```

## Regra especial para Lay Over com cashout

Lay Over encerrado antes de 90 nao pode usar lucro cheio de +stake.

Formula usada para acerto em Lay Over com fechamento antes do fim:

```text
profit_per_win = lay_stake * (1 - (entry_odd / exit_odd))
```

Perda se sair gol antes do fechamento:

```text
loss_per_loss = -lay_stake * (entry_odd - 1)
```

Lucro cheio de +stake so e permitido em `HOLD_FINAL` quando o evento layado nao acontece ate o fim.

## Formulas usadas

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

## Top 10 por rentabilidade operacional

Ranking ordenado por ROI.

| Rank | Status original | Estrategia | Target | Janela | N | Taxa | Operacao | Tipo | Lucro | ROI | EV/trade |
|---:|---|---|---|---|---:|---:|---|---|---:|---:|---:|
| 1 | PROMISSOR | `home_winning_by_1_visitor_pressing` | `goal_75_90` | `last_5m` | 36 | 63.9% | Back Over | HOLD_FINAL | +1000.00 | +27.8% | +27.78 |
| 2 | OBSERVACAO | `favorite_winning_by_1_opp_cold_2of3` | `no_goal_70_90` | `last_15m` | 34 | 58.8% | Lay Over | HOLD_FINAL | +880.00 | +25.9% | +25.88 |
| 3 | PROMISSOR | `both_teams_cold_2of3` | `no_goal_60_90` | `last_10m` | 40 | 50.0% | Lay Over | HOLD_FINAL | +1000.00 | +25.0% | +25.00 |
| 4 | PROMISSOR | `favorite_winning_by_1_opp_cold_2of3` | `no_goal_70_85` | `last_15m` | 34 | 82.4% | Lay Over | CASHOUT_ESTIMADO | +815.52 | +24.0% | +23.99 |
| 5 | OBSERVACAO | `opponent_no_recent_key_passes` | `no_goal_65_90` | `last_15m` | 42 | 52.4% | Lay Over | HOLD_FINAL | +1000.00 | +23.8% | +23.81 |
| 6 | PROMISSOR | `favorite_winning_by_1_opp_cold_2of3` | `no_goal_60_90` | `last_10m` | 40 | 47.5% | Lay Over | HOLD_FINAL | +850.00 | +21.2% | +21.25 |
| 7 | PROMISSOR | `team_winning_by_1_opp_cold_2of3` | `no_goal_70_85` | `last_15m` | 45 | 80.0% | Lay Over | CASHOUT_ESTIMADO | +945.67 | +21.0% | +21.01 |
| 8 | OBSERVACAO | `team_winning_by_1_opp_cold_2of3` | `no_goal_65_90` | `last_10m` | 46 | 50.0% | Lay Over | HOLD_FINAL | +920.00 | +20.0% | +20.00 |
| 9 | OBSERVACAO | `favorite_winning_by_1_opp_cold_2of3` | `no_goal_65_90` | `last_10m` | 32 | 50.0% | Lay Over | HOLD_FINAL | +640.00 | +20.0% | +20.00 |
| 10 | OBSERVACAO | `opponent_no_recent_key_passes` | `no_goal_70_85` | `last_15m` | 37 | 78.4% | Lay Over | CASHOUT_ESTIMADO | +701.79 | +19.0% | +18.97 |

## Leitura operacional

O ranking corrigido mostra dominio de operacoes `Lay Over / no_goal`, especialmente em janelas de `HOLD_FINAL` ate 90.

As estrategias com fechamento antes de 90 continuam positivas, mas recebem ressalva porque dependem de cashout estimado por odds medias.

## Observacoes importantes

- O ranking usa odds medias, nao odds live reais por timestamp.
- Cashout antes de 90 e estimativa operacional, nao simulacao real.
- Sem odds live timestampadas, nao considerar esse ranking como validacao final de producao.
- A ausencia de comissao, slippage, spread e liquidez tende a deixar a rentabilidade otimista.
- A decisao final deve passar pelo PM e pelo agente 06 - Trade Operations Quant.

## Veredito geral

```text
APROVADO COM RESSALVAS PARA PESQUISA OPERACIONAL
```

Nenhuma estrategia deve ser enviada para producao apenas com este ranking.

Proxima etapa recomendada:

```text
validar com odds live timestampadas
calcular comissao, spread, slippage e liquidez
reprocessar ROI e EV por liga, temporada e janela operacional
```
