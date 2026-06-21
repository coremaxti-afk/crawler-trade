# ANALISE_MATURIDADE_LIGA_POR_RODADA_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS

## Status

`APROVADA COMO V1 EXPLORATORIA`

## Objetivo

Estudo exploratorio para medir a partir de qual rodada os sinais da Serie A 2025 comecam a ficar mais confiaveis, separando:

```text
1. liga geral
2. direcao de mercado
3. familia/estrategia
4. variacao/cutoff/window
```

Este estudo nao aprova operacao final, nao preve proxima temporada e nao deve ser usado como ranking operacional definitivo.

## O que o operador precisa saber

A liga geral pode enganar porque mistura estrategias Goal/Over ruins com estrategias No Goal/Under boas.

O estudo mostrou que:

```text
Goal / Over continua ruim mesmo removendo rodadas iniciais.
No Goal / Under permanece positivo desde a primeira rodada testada.
As melhores familias No Goal amadurecem cedo.
Nao apareceu evidencia de que esperar ate a rodada 10 melhora significativamente as melhores familias No Goal.
```

## Fontes usadas

- `strategy_drawdown_trades_serie_a_2025_tempos_expandidos.csv`
- `strategy_drawdown_summary_serie_a_2025_tempos_expandidos.csv`
- `agrupamento_por_familia_e_variacoes_v1_serie_a_2025_tempos_expandidos.csv`
- `analise_regime_por_fase_v1_resumo_familias_serie_a_2025_tempos_expandidos.csv`

## Rodadas avaliadas

```text
5, 6, 7, 8, 9, 10, 11, 12
```

Observacao metodologica:

```text
A V1 nao avaliou rodadas 1, 2, 3 e 4.
Logo, ela mostra que rodada 5 ja funciona para No Goal, mas ainda nao prova que a maturidade comeca exatamente na rodada 5.
```

## Achado principal — liga geral

A liga geral foi marcada com alerta:

```text
LIGA_GERAL_CONTAMINADA_POR_DIRECAO_NEGATIVA
```

Interpretacao:

```text
A leitura agregada da liga mistura Goal ruim com No Goal bom.
Portanto, a decisao exploratoria nao deve usar apenas o resultado geral da liga.
```

## Achado principal — Goal / Over

Todas as rodadas testadas continuaram classificadas como:

```text
NAO_MADURA
```

Mesmo esperando mais rodadas, o Goal/Over permaneceu negativo.

Leitura:

```text
Esperar mais rodadas nao salvou o mercado Goal/Over.
```

## Achado principal — No Goal / Under

Todas as rodadas testadas ficaram positivas.

Exemplos registrados na auditoria:

```text
rodada 5: profit_pos positivo
rodada 12: profit_pos positivo
```

Classificacao predominante:

```text
MADURA_CEDO
```

Leitura:

```text
No Goal/Under ja aparece forte desde a primeira rodada avaliada na V1.
```

## Familias No Goal mais fortes

Familias que apareceram como maduras cedo e relevantes:

```text
opponent_no_big_chances__no_goal
team_winning_by_1_no_sot_against__no_goal
favorite_winning_by_1_opp_cold_2of3__no_goal
opponent_no_recent_key_passes__no_goal
team_winning_by_1_opp_cold_2of3__no_goal
both_teams_cold_2of3__no_goal
```

## Ressalva sobre classificacoes

As classificacoes:

```text
MADURA_CEDO
MADURA_INTERMEDIARIA
MADURA_TARDIA
```

sao rótulos exploratorios baseados nas faixas de rodada definidas no estudo.

Elas nao devem ser interpretadas como verdade operacional definitiva.

O que deve pesar mais:

```text
profit_pos
ROI_pos
N_pos
drawdown_pos
continuidade do resultado em rodadas seguintes
```

## Limitação principal da V1

A V1 testou apenas rodadas 5 a 12.

Ainda falta responder:

```text
A maturidade comeca na rodada 5 ou ja poderia comecar nas rodadas 2, 3 ou 4?
```

Essa pergunta pode virar uma V1.1 ou V2 no futuro, caso seja prioritario.

## Parecer exploratorio

```text
APROVADA COMO V1 EXPLORATORIA
```

Conclusoes:

```text
1. A liga geral nao serve sozinha para decisao.
2. Goal/Over permanece negativo mesmo removendo rodadas iniciais.
3. No Goal/Under permanece positivo desde a primeira rodada testada.
4. As melhores familias No Goal amadurecem cedo.
5. Nao ha evidencia, nesta V1, de que esperar ate rodada 10 seja necessario para as melhores familias No Goal.
6. A V1 nao prova que a rodada minima real seja 5, pois nao testou rodadas 1 a 4.
```

## Artefatos

- `analise_maturidade_liga_por_rodada_v1_liga_geral_serie_a_2025_tempos_expandidos.csv`
- `analise_maturidade_liga_por_rodada_v1_market_direction_serie_a_2025_tempos_expandidos.csv`
- `analise_maturidade_liga_por_rodada_v1_familias_serie_a_2025_tempos_expandidos.csv`
- `analise_maturidade_liga_por_rodada_v1_variacoes_serie_a_2025_tempos_expandidos.csv`
- `analise_maturidade_liga_por_rodada_v1_pre_pos_serie_a_2025_tempos_expandidos.csv`
- `analise_maturidade_liga_por_rodada_v1_alertas_serie_a_2025_tempos_expandidos.csv`
