# Trade Operations Calculation Rules V1

## Objetivo

Definir as regras V1 para transformar resultados estatisticos de uma estrategia em metricas financeiras e operacionais de trade.

Este documento e executavel conceitualmente pelo agente **06 - Trade Operations Quant** e por rotinas em lote do Codex, sem permitir que o Codex tome decisao financeira.

## Escopo V1

A V1 calcula:

1. ROI simples.
2. EV por trade.
3. Lucro/prejuizo total.
4. Break-even.
5. Hold vs cashout.
6. Back Over.
7. Lay Over.
8. Conversao Back Under para Lay Over.
9. Sensibilidade simples de odds.
10. Lucro medio por trade.

## Fora do escopo V1

A V1 nao calcula:

- comissao real;
- slippage;
- spread;
- liquidez;
- delay;
- suspensao de mercado;
- drawdown avancado;
- Kelly fracionado;
- curva de capital;
- simulacao Monte Carlo;
- odds live timestampadas;
- cashout dinamico real.

Esses itens ficam reservados para V2.

## Entradas obrigatorias

| Campo | Descricao |
|---|---|
| `strategy_name` | Nome da estrategia avaliada. |
| `market_type` | Mercado analisado, por exemplo Over/Under. |
| `operation_type` | Tipo de operacao: `BACK_OVER`, `BACK_UNDER`, `LAY_OVER`, `LAY_UNDER`. |
| `entry_minute` | Minuto de entrada. |
| `exit_minute` | Minuto de saida. |
| `entry_odd` | Odd media de entrada. |
| `exit_odd` | Odd media de saida. |
| `stake` | Valor financeiro por trade. |
| `hit_rate` | Taxa de acerto estatistica da estrategia. |
| `trade_count` | Numero total de trades avaliados. |
| `wins` | Numero de trades vencedores. |
| `losses` | Numero de trades perdedores. |
| `cashout_rule` | Regra de encerramento antecipado. |
| `hold_rule` | Regra de manter posicao ate o evento final. |
| `commission` | Comissao. Na V1, deve ser documentada, mas pode ser mantida em 0 quando nao houver dado confiavel. |

## Saidas obrigatorias

| Campo | Descricao |
|---|---|
| `total_profit` | Lucro ou prejuizo total. |
| `ROI` | Retorno sobre o capital total exposto. |
| `EV_per_trade` | Valor esperado por trade. |
| `break_even_rate` | Taxa minima de acerto para nao perder dinheiro. |
| `avg_profit_per_trade` | Lucro medio por trade. |
| `max_loss_sequence` | Maior sequencia de perdas. |
| `simple_drawdown` | Maior queda simples acumulada. |
| `hold_profit` | Resultado estimado em hold. |
| `cashout_profit` | Resultado estimado em cashout. |
| `odds_sensitivity` | Resultado com variacao simples de odds. |
| `operational_verdict` | Veredito operacional. |

## Definicoes basicas

### Capital exposto

```text
capital_exposto = stake * trade_count
```

### Lucro bruto de Back vencedor

```text
profit_back_win = stake * (entry_odd - 1)
```

### Prejuizo de Back perdedor

```text
loss_back = -stake
```

### Lucro de Lay vencedor

No Lay, a estrategia vence quando o evento layado nao acontece.

```text
profit_lay_win = stake
```

### Prejuizo de Lay perdedor

```text
loss_lay = -stake * (entry_odd - 1)
```

### Responsabilidade no Lay

```text
lay_liability = stake * (entry_odd - 1)
```

## ROI simples

```text
ROI = total_profit / capital_exposto
```

Quando expresso em percentual:

```text
ROI_percent = ROI * 100
```

## EV por trade

### Para Back

```text
EV_per_trade = (hit_rate * profit_back_win) + ((1 - hit_rate) * loss_back)
```

### Para Lay

```text
EV_per_trade = (hit_rate * profit_lay_win) + ((1 - hit_rate) * loss_lay)
```

Na V1, `hit_rate` deve representar a taxa de acerto da operacao ja convertida para o lado correto da operacao.

Exemplo: em `LAY_OVER`, `hit_rate` deve representar a frequencia em que o Over layado nao vence.

## Lucro/prejuizo total

```text
total_profit = (wins * profit_per_win) + (losses * loss_per_loss)
```

Onde `profit_per_win` e `loss_per_loss` dependem do tipo de operacao.

## Break-even

### Break-even em Back

```text
break_even_rate_back = 1 / entry_odd
```

### Break-even em Lay

```text
break_even_rate_lay = (entry_odd - 1) / entry_odd
```

## Lucro medio por trade

```text
avg_profit_per_trade = total_profit / trade_count
```

## Hold vs cashout

### Hold

Hold significa manter a posicao ate o criterio final da aposta ou ate o encerramento natural do mercado.

```text
hold_profit = resultado_final_da_operacao_sem_saida_antecipada
```

Na V1, quando nao houver odds live timestampadas, o hold pode ser estimado usando `entry_odd`, `wins`, `losses` e `stake`.

### Cashout

Cashout significa encerrar a posicao em uma janela operacional usando `exit_odd` ou regra fixa de saida.

```text
cashout_profit = resultado_estimado_com_saida_em_exit_minute
```

Na V1, cashout deve ser tratado como estimativa simplificada, nao como simulacao real. Sem odds live timestampadas, o resultado deve ser marcado como aproximado.

## Back Over

Back Over vence quando o evento Over ocorre.

```text
profit_per_win = stake * (entry_odd - 1)
loss_per_loss = -stake
```

```text
total_profit_back_over = (wins * profit_per_win) + (losses * loss_per_loss)
```

## Lay Over

Lay Over vence quando o evento Over nao ocorre.

```text
profit_per_win = stake
loss_per_loss = -stake * (entry_odd - 1)
```

```text
total_profit_lay_over = (wins * profit_per_win) + (losses * loss_per_loss)
```

## Conversao Back Under para Lay Over

Back Under e Lay Over tem direcao logica semelhante, mas estrutura financeira diferente.

### Back Under

```text
profit_back_under_win = stake * (back_under_odd - 1)
loss_back_under = -stake
```

### Lay Over equivalente

```text
profit_lay_over_win = lay_stake
loss_lay_over = -lay_stake * (lay_over_odd - 1)
```

### Conversao conceitual

Se a estrategia estatistica diz que o Under tem valor, a leitura operacional equivalente em Lay Over deve recalcular:

- responsabilidade;
- break-even;
- EV;
- ROI;
- risco de perda;
- sensibilidade da odd layada.

Nao e permitido assumir que Back Under e Lay Over tem o mesmo ROI apenas porque apontam para a mesma direcao do jogo.

## Sensibilidade simples de odds

A V1 deve recalcular EV, ROI e lucro total nos seguintes cenarios:

### Entrada

- `entry_odd - 0.10`
- `entry_odd`
- `entry_odd + 0.10`

### Saida

- `exit_odd - 0.10`
- `exit_odd`
- `exit_odd + 0.10`

## Janelas operacionais obrigatorias

O agente deve organizar cenarios por janela:

- 60-75;
- 65-80;
- 70-85;
- 75-90.

Cada janela deve exibir, quando houver dados suficientes:

- taxa de acerto;
- quantidade de trades;
- EV por trade;
- ROI;
- lucro total;
- break-even;
- sensibilidade de odds;
- veredito operacional.

## Sequencia maxima de perdas

A V1 deve calcular a maior sequencia de perdas quando houver serie ordenada de resultados.

```text
max_loss_sequence = maior quantidade consecutiva de trades perdedores
```

Se a serie ordenada nao existir, o campo deve ser retornado como:

```text
max_loss_sequence = null
reason = "serie temporal de trades nao fornecida"
```

## Drawdown simples

A V1 pode calcular drawdown simples apenas se houver curva acumulada de resultados.

```text
simple_drawdown = maior queda entre um pico acumulado e o menor ponto posterior
```

Se nao houver curva acumulada, retornar:

```text
simple_drawdown = null
reason = "curva acumulada nao fornecida"
```

## Veredito operacional

O agente pode retornar apenas um dos seguintes vereditos:

- `APROVADO OPERACIONALMENTE`
- `APROVADO COM RESSALVAS`
- `NAO COMPENSA FINANCEIRAMENTE`

### Regra minima sugerida

`APROVADO OPERACIONALMENTE` quando:

- EV por trade > 0;
- ROI > 0;
- hit rate > break-even;
- amostra minimamente suficiente;
- sensibilidade de odds nao destrói o resultado com pequena variacao.

`APROVADO COM RESSALVAS` quando:

- EV positivo, mas sensivel a odds;
- ROI positivo, mas baixo;
- trade_count pequeno;
- cashout depende de estimativa sem odds live timestampadas;
- drawdown ou sequencia de perdas nao foram calculados por falta de serie ordenada.

`NAO COMPENSA FINANCEIRAMENTE` quando:

- EV <= 0;
- ROI <= 0;
- hit rate <= break-even;
- pequena piora de odd torna a operacao negativa;
- risco operacional supera o retorno esperado.

## Regra critica

Uma estrategia estatisticamente boa nao deve ser aprovada operacionalmente sem passar pelos calculos financeiros deste documento.

O agente 06 nao escolhe estrategia em producao. Ele entrega a avaliacao operacional para decisao do PM.
