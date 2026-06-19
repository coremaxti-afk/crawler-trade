# VALIDACAO_PREDITIVA_DA_ESTRATEGIA_V1_1_SERIE_A_2025_TEMPOS_EXPANDIDOS

## Status

`APROVADA COMO CAMADA DE PESQUISA TEMPORAL POS-DD CORRIGIDO`

## Contexto

Esta camada foi criada depois da correcao do DD V4, que passou a fornecer `fixture_date_parsed`, `round` e `temporal_order_rank` diretamente nos trades.

A validacao preditiva V1.1 consome:

- Trades DD: `strategy_drawdown_trades_serie_a_2025_tempos_expandidos.csv`
- Summary DD: `strategy_drawdown_summary_serie_a_2025_tempos_expandidos.csv`
- Fonte temporal ativa: `DD_TRADES`
- Manifest SportMonks: `NAO_UTILIZADO`
- Leitura financeira: `ESTIMATIVA OPERACIONAL COM ODDS MEDIAS`

## Resultado validado

Foram validados os CSVs e o MD da entrega V1.1.

Resumo:

- Total de estrategias: `714`
- Linhas de fases: `4.284 = 714 * 6`
- Rolling windows: `146.040`
- Duplicatas no summary: `0`
- N das fases bate com N_total: `100%`
- Confirmadas estatisticamente: `246`
- Confirmadas operacionalmente: `186`
- Confirmadas fracas nao operacionais: `60`
- Falsos positivos negativos: `56`
- Falsos positivos break-even: `3`
- Lucrativas operacionais nao previsiveis: `0`
- Lucrativas fracas nao previsiveis: `3`
- Nao lucrativas sem sinal: `302`

## Correcao conceitual feita

A V1 tinha erro conceitual na secao `Estrategias lucrativas mas nao previsiveis`, pois listava estrategias negativas.

A V1.1 corrigiu isso separando:

- `LUCRATIVA_FRACA_NAO_PREVISIVEL`
- `LUCRATIVA_OPERACIONAL_NAO_PREVISIVEL`
- `NAO_LUCRATIVA_SEM_SINAL`
- `FALSO_POSITIVO_NEGATIVO`
- `FALSO_POSITIVO_BREAK_EVEN`
- `CONFIRMADA_FRACA_NAO_OPERACIONAL`
- `POSITIVO_FRACO_NAO_OPERACIONAL`

## Classificacao estatistica vs operacional

A classificacao estatistica mede se houve sinal temporal.

A classificacao operacional mede se o sinal tambem possui lucro, ROI e N minimos para decisao pratica.

Filtros operacionais usados:

```text
profit_final >= 500
ROI_final >= 5%
N_total >= 30
```

## Leitura operacional principal

A V1.1 mostrou que nenhuma estrategia foi confirmada com seguranca nas primeiras 5 rodadas.

As primeiras confirmacoes relevantes aparecem ate 10 rodadas ou por fase.

Padrao das estrategias que deram certo:

- `lay_over`
- `no_goal_*`
- adversario frio
- adversario sem big chances
- adversario sem key passes recentes
- time vencendo por 1
- oponente sem SOT contra
- entradas principalmente entre 65 e 75

Familias candidatas observadas:

- `opponent_no_big_chances`
- `team_winning_by_1_no_sot_against`
- `opponent_no_recent_key_passes`
- `both_teams_cold_2of3`
- `team_winning_by_1_opp_cold_2of3`
- `favorite_winning_by_1_opp_cold_2of3`

Padrao das estrategias que deram errado:

- `back_over`
- `goal_*`
- pressao alta como unico gatilho
- time perdendo pressionando
- favorito pressionando para buscar gol
- big chances recentes usadas para buscar gol
- SOT/key passes/corners recentes usados isoladamente para buscar gol

Familias de alerta:

- `team_losing_pressure_high_2of3`
- `favorite_drawing_pressure_high_2of3`
- `favorite_losing_pressure_high_2of3`
- `underdog_winning_favorite_pressing_2of3`
- `big_chances_recent` quando usado em `goal_*`

## Decisao

`VALIDACAO_PREDITIVA_DA_ESTRATEGIA_V1_1` fica aprovada como camada oficial de pesquisa temporal pos-DD corrigido.

Ela nao substitui Discovery, Normalizacao, DD ou Rentabilidade por Time.

Ela deve alimentar o proximo passo:

```text
RANKING_OPERACIONAL_FINAL_V1
```
