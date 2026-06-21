# ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1_SERIE_A_2025_TEMPOS_EXPANDIDOS

## Status

`APROVADA COMO V1_1 EXPLORATORIA`

## Objetivo

Corrigir a V1 focando apenas em familias No Goal lucrativas, para entender por que alguns times quebram estrategias que funcionam no agregado.

## O QUE O OPERADOR PRECISA SABER

Esta versao nao redescobre que Goal e ruim. Ela olha somente para familias No Goal lucrativas e procura explicar em que times e contextos elas falham.

## Familias No Goal incluidas

- `both_teams_cold_2of3__no_goal`
- `favorite_winning_by_1_opp_cold_2of3__no_goal`
- `opponent_no_big_chances__no_goal`
- `opponent_no_recent_key_passes__no_goal`
- `team_winning_by_1_low_dangerous_attacks_against__no_goal`
- `team_winning_by_1_no_sot_against__no_goal`
- `team_winning_by_1_opp_cold_2of3__no_goal`

## Times que realmente prejudicam No Goal

| team_name | familias_no_goal_afetadas | profit_total | ROI_total | drawdown_total | N_total |
| --- | ---: | ---: | ---: | ---: | ---: |
| São Paulo | 6 | -20665.6655 | -0.2237 | -1448.3673 | 924 |
| Internacional | 6 | -9537.8556 | -0.1366 | -1835.0000 | 698 |
| Botafogo | 6 | -6958.7146 | -0.0745 | -2333.6735 | 934 |
| Juventude | 3 | -4688.6643 | -0.0961 | -1935.0000 | 488 |
| Vasco da Gama | 4 | -3040.4462 | -0.0710 | -1580.0000 | 428 |
| Bragantino | 1 | -2523.4922 | -0.0949 | -1800.0000 | 266 |
| Sport Recife | 2 | -1655.7021 | -0.3599 | -1160.0000 | 46 |
| Flamengo | 3 | -1423.7953 | -0.0259 | -2400.0000 | 550 |
| Mirassol | 2 | -1245.6168 | -0.0523 | -1960.0000 | 238 |
| Grêmio | 1 | -395.5315 | -0.1521 | -341.5306 | 26 |

## Times contraditorios

O estudo confirmou que um time pode ser bom para uma familia e ruim para outra. Isso reforca que o problema nao e apenas o time isolado, mas:

```text
time + contexto + familia
```

Exemplos:

| team_name | familia_benefica | familia_prejudicial | profit_benefico | profit_prejudicial |
| --- | --- | --- | ---: | ---: |
| São Paulo | both_teams_cold_2of3__no_goal | opponent_no_recent_key_passes__no_goal | 3259.3162 | -4923.6491 |
| Juventude | both_teams_cold_2of3__no_goal | team_winning_by_1_no_sot_against__no_goal | 3688.9293 | -3121.0311 |
| Bragantino | both_teams_cold_2of3__no_goal | opponent_no_big_chances__no_goal | 2948.4222 | -2523.4922 |
| Mirassol | opponent_no_big_chances__no_goal | team_winning_by_1_low_dangerous_attacks_against__no_goal | 5600.5574 | -1044.6208 |

## Perfil dos times prejudiciais

| team_name | team_profile | favorite_strength_band_dominante | match_balance_type_dominante | phase_dominante | familias_afetadas_resumo |
| --- | --- | --- | --- | --- | --- |
| São Paulo | FAVORITO_MEDIO_DOMINANTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA | FAVORITO_MEDIO | FAVORITO_MEDIO_X_AZARAO_COMPETITIVO | 4 | 6 familias |
| Internacional | FAVORITO_MEDIO_DOMINANTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA | FAVORITO_MEDIO | FAVORITO_MEDIO_X_AZARAO_COMPETITIVO | 6 | 6 familias |
| Botafogo | FAVORITO_MEDIO_DOMINANTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA | FAVORITO_MEDIO | FAVORITO_MEDIO_X_AZARAO_COMPETITIVO | 6 | 6 familias |
| Juventude | AZARAO_RECORRENTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA | FAVORITO_FRACO | FAVORITO_FRACO | 5 | 3 familias |
| Vasco da Gama | AZARAO_RECORRENTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA | FAVORITO_FRACO | FAVORITO_FRACO | 3 | 4 familias |
| Flamengo | FAVORITO_FORTE_DOMINANTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA | FAVORITO_FORTE | FAVORITO_FORTE_X_ZEBRA | 1 | 3 familias |

## Padroes mais recorrentes

| team_profile | quantidade_de_times | profit_agregado | ROI_agregado | N_agregado |
| --- | ---: | ---: | ---: | ---: |
| FAVORITO_MEDIO_DOMINANTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA | 3 | -37162.2358 | -0.1454 | 2556 |
| AZARAO_RECORRENTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA | 2 | -7729.1106 | -0.0844 | 916 |
| FAVORITO_MEDIO_DOMINANTE/PREJUIZO_DISTRIBUIDO/FAMILIA_ESPECIFICA | 1 | -2523.4922 | -0.0949 | 266 |
| JOGO_PARELHO_DOMINANTE/PREJUIZO_CONCENTRADO_EM_FASE/MULTI_FAMILIA | 1 | -1655.7021 | -0.3599 | 46 |
| FAVORITO_FORTE_DOMINANTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA | 1 | -1423.7953 | -0.0259 | 550 |

## Leitura Quant

A V1.1 melhorou muito a V1 porque deixou de ser uma leitura dominada por Goal negativo e passou a focar nas familias No Goal lucrativas.

Achado principal:

```text
O perfil FAVORITO_MEDIO_DOMINANTE + PREJUIZO_DISTRIBUIDO + MULTI_FAMILIA foi o mais forte entre os times que prejudicam No Goal.
```

Times mais relevantes nesse perfil:

```text
São Paulo
Internacional
Botafogo
```

Juntos, esses times geraram aproximadamente:

```text
-37162.2358
```

em prejuizo agregado no conjunto de familias No Goal analisadas.

## Alertas metodologicos

- Nao aprova exclusao de times.
- Nao aprova operacao final.
- Nao cria blacklist.
- N abaixo de 20 nao deve sustentar conclusao.
- `OVERLAP_ALTO_NAO_SOMAR_VARIACOES`
- `TIME_CONTRADITORIO`

## Parecer exploratorio final

```text
APROVADA COMO V1_1 EXPLORATORIA
```

Conclusoes:

```text
1. A V1.1 respondeu melhor a pergunta principal do que a V1.
2. O problema nao e apenas o time isolado, mas time + contexto + familia.
3. O perfil mais forte de prejuizo No Goal foi FAVORITO_MEDIO_DOMINANTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA.
4. São Paulo, Internacional e Botafogo sao os principais alertas exploratorios.
5. O achado deve ser levado para validacao multi-temporada antes de virar regra operacional.
6. Nenhum time deve ser excluido automaticamente com base nesta etapa.
```

## Artefatos

- `analise_padroes_prejuizo_por_time_v1_1_no_goal_serie_a_2025_tempos_expandidos.csv`
- `analise_padroes_prejuizo_por_time_v1_1_team_profiles_serie_a_2025_tempos_expandidos.csv`
- `analise_padroes_prejuizo_por_time_v1_1_times_contraditorios_serie_a_2025_tempos_expandidos.csv`
- `analise_padroes_prejuizo_por_time_v1_1_padroes_serie_a_2025_tempos_expandidos.csv`
- `analise_padroes_prejuizo_por_time_v1_1_alertas_serie_a_2025_tempos_expandidos.csv`
- `analise_padroes_prejuizo_por_time_v1_1_serie_a_2025_tempos_expandidos.json`
- `ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md`
