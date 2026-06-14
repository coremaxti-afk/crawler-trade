# Trade Operations Cashout Lay Over Rules V1

## Objetivo

Documentar a regra operacional correta para calcular Lay Over, Back Under e cashout em estrategias que fecham antes do fim do mercado.

Este documento existe para evitar o erro critico de tratar uma operacao encerrada antes dos 90 minutos como se fosse hold final com lucro ou perda integral.

## Regra central

Antes de calcular lucro, ROI, EV ou break-even, o agente deve classificar a operacao como:

1. `HOLD_FINAL`
2. `CASHOUT_ESTIMADO`

## Classificacao obrigatoria

```text
se exit_minute >= 90:
    operation_settlement = HOLD_FINAL
else:
    operation_settlement = CASHOUT_ESTIMADO
```

## Exemplos

```text
no_goal_60_90 = HOLD_FINAL
no_goal_60_80 = CASHOUT_ESTIMADO
no_goal_65_80 = CASHOUT_ESTIMADO
no_goal_70_85 = CASHOUT_ESTIMADO
goal_75_90 = HOLD_FINAL
goal_70_80 = CASHOUT_ESTIMADO
```

## Proibicao critica

Nunca calcular lucro cheio em Lay Over quando a estrategia fecha antes dos 90 minutos.

Exemplo errado:

```text
LAY_OVER
entrada 60
saida 80
sem gol entre 60 e 80
stake 100

lucro = +100
```

Esse calculo esta errado porque a posicao foi encerrada antes do fim. O lucro cheio so existe em `HOLD_FINAL` quando o evento layado nao acontece ate o encerramento do mercado.

## Lay Over em HOLD_FINAL

Lay Over em hold final vence quando o evento layado nao acontece ate o fim do mercado.

```text
profit_per_win = stake
loss_per_loss = -stake * (entry_odd - 1)
```

Exemplo:

```text
LAY_OVER
entrada @ 1.50
stake 100
hold ate 90

se nao sair gol ate o fim:
    lucro = +100

se sair gol:
    perda = -50
```

## Lay Over em CASHOUT_ESTIMADO

Quando a operacao Lay Over e fechada antes do fim, o resultado depende da diferenca entre a odd de entrada e a odd de saida.

Para fechar um Lay, faz-se Back na saida.

Formula simplificada com hedge proporcional:

```text
cashout_profit_lay = lay_stake * (1 - (entry_odd / exit_odd))
```

Leitura:

```text
se exit_odd > entry_odd:
    cashout_profit_lay > 0

se exit_odd < entry_odd:
    cashout_profit_lay < 0
```

Portanto, em Lay Over:

- se a odd do Over sobe entre a entrada e a saida, o fechamento tende a gerar lucro;
- se a odd do Over cai entre a entrada e a saida, o fechamento tende a gerar prejuizo;
- o lucro nao e igual a `stake`, exceto em hold final vencedor.

## Exemplo correto: no_goal_60_80

Entrada:

```text
operation_type = LAY_OVER
entry_minute = 60
exit_minute = 80
entry_odd = 1.50
exit_odd = 2.45
stake = 100
```

Como `exit_minute < 90`, a operacao e:

```text
CASHOUT_ESTIMADO
```

Se nao sair gol entre 60 e 80:

```text
cashout_profit_lay = 100 * (1 - (1.50 / 2.45))
cashout_profit_lay = +38.78 aproximadamente
```

O lucro correto estimado e aproximadamente:

```text
+38.78
```

Nao e:

```text
+100
```

## Perda quando sai gol antes da saida

Se o evento layado acontece antes do minuto de saida, a operacao perde pela responsabilidade da entrada:

```text
loss_lay_event_before_exit = -stake * (entry_odd - 1)
```

Exemplo:

```text
entry_odd = 1.50
stake = 100

loss = -100 * (1.50 - 1)
loss = -50
```

## Formula V1 para Lay Over com fechamento antes do fim

Para estrategias como `no_goal_60_80`, `no_goal_65_80` ou `no_goal_70_85`:

```text
wins = trades sem gol ate exit_minute
losses = trades com gol antes de exit_minute

profit_per_win = lay_stake * (1 - (entry_odd / exit_odd))
loss_per_loss = -lay_stake * (entry_odd - 1)

total_profit = (wins * profit_per_win) + (losses * loss_per_loss)
ROI = total_profit / (trade_count * stake)
EV_per_trade = total_profit / trade_count
```

## Break-even em Lay Over com cashout

```text
break_even_rate_cashout = abs(loss_per_loss) / (profit_per_win + abs(loss_per_loss))
```

Se `profit_per_win <= 0`, a operacao nao possui break-even operacional positivo no formato avaliado.

## Back Under vs Lay Over

Back Under e Lay Over podem apontar para a mesma leitura estatistica, mas nao possuem a mesma estrutura financeira.

Nao e permitido assumir que:

```text
Back Under = Lay Over
```

sem recalcular:

- odd de entrada;
- odd de saida;
- responsabilidade;
- cashout;
- break-even;
- EV;
- ROI.

## Regra para estrategias ate 90

Quando a estrategia termina em 90, nao ha cashout intermediario.

Exemplo:

```text
no_goal_60_90
```

Significa:

```text
entrada aos 60
segura ate o final
resultado integral da operacao
```

Nesse caso, Lay Over pode usar:

```text
profit_per_win = stake
loss_per_loss = -stake * (entry_odd - 1)
```

## Regra para estrategias antes de 90

Quando a estrategia termina antes de 90, ha fechamento/cashout estimado.

Exemplo:

```text
no_goal_60_80
```

Significa:

```text
entrada aos 60
fecha aos 80
resultado pela diferenca entre entry_odd e exit_odd
```

Nesse caso, Lay Over nao pode usar:

```text
profit_per_win = stake
```

Deve usar:

```text
profit_per_win = lay_stake * (1 - (entry_odd / exit_odd))
```

## Sensibilidade de odds

Em cashout estimado, a sensibilidade deve variar tanto a odd de entrada quanto a odd de saida:

```text
entry_odd - 0.10
entry_odd
entry_odd + 0.10

exit_odd - 0.10
exit_odd
exit_odd + 0.10
```

A avaliacao operacional deve mostrar se pequena mudanca na entrada ou na saida destroi o EV.

## Veredito operacional

Uma estrategia deve ser marcada como `NAO COMPENSA FINANCEIRAMENTE` quando so parece lucrativa por confundir cashout antes do fim com hold final.

Uma estrategia pode ser `APROVADO COM RESSALVAS` quando:

- o EV e positivo;
- mas depende de odds medias;
- nao possui odds live timestampadas;
- o cashout e apenas estimado;
- ha grande sensibilidade entre entry_odd e exit_odd.

Uma estrategia so deve ser `APROVADO OPERACIONALMENTE` quando:

- o EV continua positivo apos a regra correta de cashout;
- o ROI continua positivo;
- o break-even e superado;
- a sensibilidade de odds nao destrui o resultado;
- a amostra e minimamente aceitavel.

## Regra final

O agente 06 - Trade Operations Quant deve sempre responder primeiro:

```text
A operacao e HOLD_FINAL ou CASHOUT_ESTIMADO?
```

Somente depois disso pode calcular lucro, ROI, EV e break-even.
