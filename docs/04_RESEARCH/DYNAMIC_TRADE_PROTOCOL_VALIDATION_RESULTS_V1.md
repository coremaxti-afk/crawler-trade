# DYNAMIC_TRADE_PROTOCOL_VALIDATION_RESULTS_V1

## Resumo Executivo

- Validacao exploratoria de quatro estrategias promissoras com protocolo dinamico de trade.
- Nao cria modelo, producao, robo ou backtesting financeiro real.
- Odds usadas sao medias travadas do plano; nenhuma odd live foi usada.
- Stake base: 100.
- Lay Over usa a odd Back Over como odd de lay.
- Back Over usa a odd Back Over como odd de back.
- Dataset H8 atual nao possui cutoff 80; por isso a decisao dinamica depois dos 75 nao faz nova leitura H8 aos 80.

Status atual:

```text
APROVADO COM RESSALVAS
```

Ressalva principal:

```text
As estrategias contendo favorite_* ainda dependem de validacao definitiva do favorito pre-jogo via odds.
```

As regras dinamicas de entrada/cashout continuam validas como protocolo exploratorio. Entretanto, cenarios baseados em `favorite_*` devem ser tratados como pendentes ate que o favorito pre-jogo seja validado por odds.

## Ressalva Metodologica - Favorito Pre-Jogo

As estrategias abaixo dependem de favorito pre-jogo:

- `favorite_winning_by_1 + h8_cold_combo_10m_2of3`
- `favorite_winning_by_1 + h8_pressure_score_10m_bottom25`

Na etapa SportMonks posterior, quando favorito pre-jogo nao estava disponivel de forma consolidada, foi usado proxy:

```text
time vencendo por 1 no cutoff
```

Portanto, os resultados dinamicos continuam uteis para entender o efeito de reavaliacao/cashout, mas nao devem ser lidos como reproducao definitiva do filtro `favorite_winning_by_1`.

Proxima etapa recomendada:

```text
PRE_MATCH_FAVORITE_VALIDATION_V1
```

Objetivo:

```text
Integrar odds pre-jogo para marcar favorito real e reexecutar as regras favorite_*.
```

## Formulas

- Back hold: `P(gol) * stake * (odd_back - 1) - P(no_goal) * stake`.
- Back cashout: hedge por `stake * odd_entry / odd_exit`; perda se sem gol = `stake - hedge`.
- Lay hold: lucro se sem gol = `stake`; perda se gol = `stake * (odd_lay - 1)`.
- Lay cashout: fechar com back em odd atual; lucro travado = `stake - stake * odd_lay / odd_back_atual`.

## Resultado Por Estrategia

| Estrategia | Nome completo | Trades | Hold total | Hold ROI | Dinamico total | Dinamico ROI | Delta | Status | Principais saidas dinamicas |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| S1 | `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | 54 | 3580.00 | 66.3% | 1201.76 | 22.3% | -2378.24 | APROVADO COM RESSALVAS | cashout_70_not_cold=26; loss_goal_60_70=11; win_no_goal_to_80=8; cashout_75_not_cold=6; loss_goal_70_75=2; loss_goal_75_80=1 |
| S2 | `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | 36 | 2430.00 | 67.5% | 770.59 | 21.4% | -1659.41 | APROVADO COM RESSALVAS | cashout_70_not_cold=20; loss_goal_60_70=7; win_no_goal_to_80=5; cashout_75_not_cold=2; loss_goal_70_75=1; loss_goal_75_80=1 |
| S3 | `home_winning_by_1 + h8_shot_quality_top25` | 20 | 100.00 | 5.0% | 325.00 | 16.2% | 225.00 | OBSERVACAO | win_goal_65_75=11; cashout_75_cold_or_not_hot=5; win_goal_75_85_after_hold=2; loss_no_goal_to_85=2 |
| S4 | `home_winning_by_1 + h8_pressure_score_10m_top25` | 23 | -50.00 | -2.2% | 175.00 | 7.6% | 225.00 | OBSERVACAO | win_goal_65_75=12; cashout_75_cold_or_not_hot=5; loss_no_goal_to_85=4; win_goal_75_85_after_hold=2 |

## Leitura

- `favorite_winning_by_1 + h8_cold_combo_10m_2of3`: protocolo dinamico piorou vs hold em -2378.24; ROI dinamico 22.3%.
- `favorite_winning_by_1 + h8_pressure_score_10m_bottom25`: protocolo dinamico piorou vs hold em -1659.41; ROI dinamico 21.4%.
- `home_winning_by_1 + h8_shot_quality_top25`: protocolo dinamico melhorou vs hold em 225.00; ROI dinamico 16.2%.
- `home_winning_by_1 + h8_pressure_score_10m_top25`: protocolo dinamico melhorou vs hold em 225.00; ROI dinamico 7.6%.

Conclusao operacional:

```text
Para Lay Over frio, hold simples continuou superior ao protocolo dinamico nesta simulacao.
Para Back Over quente, protocolo dinamico melhorou o hold, mas as amostras sao menores e ficam em observacao.
```

## Regras Anti-Leakage

- Entrada usa apenas estado/H8 ate o cutoff de entrada.
- Reavaliacao usa apenas H8 do cutoff de reavaliacao.
- Gols futuros entram somente como resultado da simulacao.
- Placar final nao foi usado como feature.
- Nao houve odds live reais; odds sao fixas do protocolo.

## Limitacoes

- Isto e simulacao protocolar deterministica, nao backtesting financeiro real.
- Nao considera liquidez, spread, suspensao de mercado, delay, comissao ou slippage.
- Odds sao medias travadas, nao precos historicos reais por jogo.
- Sem cutoff 80 no H8 atual, o trecho 75-85 nao consegue reavaliar novamente aos 80.
- Estrategias `favorite_*` ainda dependem de favorito pre-jogo validado por odds.

## Recomendacao

- Nao executar robo, producao ou backtesting real sem odds live/historicas por timestamp.
- Validar favorito pre-jogo antes de promover estrategias `favorite_*` para operacional definitivo.
- Manter as regras dinamicas como estudo exploratorio ate nova rodada com favorito validado.
