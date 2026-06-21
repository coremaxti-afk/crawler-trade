# ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS

## Status

`APROVADA COMO V1 EXPLORATORIA COM RESSALVA DE INTERPRETACAO`

## Objetivo

Estudo exploratorio para entender se familias, estrategias e variacoes mudam de comportamento conforme a forca do favorito pre-jogo.

Este estudo ajuda a separar contexto bom de contexto perigoso, mas nao autoriza operar, nao preve proxima temporada e nao substitui validacao futura.

## O que o operador precisa saber

A forca do favorito parece importar bastante.

O achado mais forte foi:

```text
As melhores familias No Goal tiveram melhor desempenho em jogos parelhos ou sem favorito claro.
```

Isso contraria uma expectativa inicial de que favorito forte seria necessariamente o melhor contexto.

## Fontes usadas

- `strategy_drawdown_trades_serie_a_2025_tempos_expandidos.csv`
- `strategy_drawdown_summary_serie_a_2025_tempos_expandidos.csv`
- `sportmonks_team_side_strategy_discovery_entries_v4_serie_a_2025_tempos_expandidos.csv`
- `agrupamento_por_familia_e_variacoes_v1_serie_a_2025_tempos_expandidos.csv`
- `analise_regime_por_fase_v1_resumo_familias_serie_a_2025_tempos_expandidos.csv`
- `analise_maturidade_liga_por_rodada_v1_familias_serie_a_2025_tempos_expandidos.csv`

## Qualidade dos dados

- Total trades: `77661`
- Total fixtures: `380`
- Fixtures com favorito identificado: `100.0%`
- Trades com favorito identificado: `100.0%`
- Campo ausente: `stake`
- Alertas registrados: `AMOSTRA_INSUFICIENTE`, `OVERLAP_ALTO_NAO_SOMAR_VARIACOES`, `SEGMENTO_PERIGOSO_IDENTIFICADO`

## Faixas de favorito usadas

```text
favorite_odds <= 1.50 -> FAVORITO_FORTE
1.50 < favorite_odds <= 1.85 -> FAVORITO_MEDIO
1.85 < favorite_odds <= 2.20 -> FAVORITO_FRACO
favorite_odds > 2.20 -> SEM_FAVORITO_CLARO_OU_JOGO_PARELHO
```

## Resultado por direcao de mercado

### Goal / Over

O Goal/Over continuou negativo em todos os segmentos agregados:

```text
FAVORITO_FORTE: negativo
FAVORITO_MEDIO: negativo
FAVORITO_FRACO: negativo
JOGO_PARELHO: negativo
```

Interpretacao:

```text
Goal nao passou a funcionar por causa da segmentacao por favorito.
Algumas familias Goal ficaram menos ruins ou pontualmente positivas em segmentos especificos, mas o mercado Goal agregado continua negativo.
```

### No Goal / Under

No Goal/Under foi positivo em todos os segmentos agregados.

Melhor segmento agregado:

```text
SEM_FAVORITO_CLARO_OU_JOGO_PARELHO
```

Resultado agregado desse segmento:

```text
N = 6034
profit = 130024.0283
ROI = 0.2155
win_rate = 0.7053
```

## Descoberta principal — jogos parelhos

As familias vencedoras de No Goal ficaram concentradas em:

```text
SEM_FAVORITO_CLARO_OU_JOGO_PARELHO
```

Exemplos:

```text
opponent_no_big_chances__no_goal
team_winning_by_1_no_sot_against__no_goal
opponent_no_recent_key_passes__no_goal
team_winning_by_1_opp_cold_2of3__no_goal
both_teams_cold_2of3__no_goal
favorite_winning_by_1_opp_cold_2of3__no_goal
```

## Exemplo importante — both_teams_cold_2of3

A hipotese de que `both_teams_cold_2of3` funciona melhor em jogos parelhos ganhou forca.

Resultados por segmento:

```text
JOGO_PARELHO: ROI 22.5%
FAVORITO_FRACO: ROI 6.8%
FAVORITO_MEDIO: ROI 13.4%
FAVORITO_FORTE: ROI 12.2%
```

Interpretacao:

```text
both_teams_cold_2of3 parece mais forte quando o jogo e parelho.
```

## Exemplo contraintuitivo — favorite_winning_by_1_opp_cold_2of3

O melhor resultado de `favorite_winning_by_1_opp_cold_2of3` nao apareceu em favorito forte.

Melhor segmento:

```text
SEM_FAVORITO_CLARO_OU_JOGO_PARELHO
ROI = 35.66%
```

Interpretacao:

```text
Mesmo uma estrategia com favorito no nome pode ter melhor desempenho em contexto mais equilibrado.
```

Isso reforca a importancia da pesquisa exploratoria antes de criar filtros operacionais.

## Tudo junto vs segmentado

O estudo mostrou:

```text
7 familias melhores sem segmentar
11 familias com indício de melhora segmentando
```

Mas isso exige cuidado.

Alguns casos de Goal parecem melhorar quando segmentados, por exemplo:

```text
home_winning_by_1_visitor_pressing__goal
profit_all = -25347.9881
best_segment = FAVORITO_FORTE
best_segment_profit = 2380.0203
best_segment_ROI = 13.52%
best_segment_N = 176
```

Ressalva:

```text
Isso ainda nao prova que segmentar resolveu a estrategia.
Pode ser hipotese promissora, mas precisa de validacao posterior por causa de risco de overfitting e amostra menor.
```

## Ressalva sobre o parecer do MD original

O MD original afirmou:

```text
Goal melhora em algum contexto: SIM
```

A leitura correta deve ser mais conservadora:

```text
Goal nao passou a funcionar no agregado.
Algumas familias Goal ficaram menos negativas ou pontualmente positivas em segmentos especificos.
```

Essa diferenca e importante para evitar falsa confianca operacional.

## Decisoes que este estudo permite tomar

```text
1. Levantar hipotese de que jogos parelhos sao o melhor contexto para No Goal.
2. Identificar segmentos perigosos onde estrategias ficam negativas.
3. Separar familias que parecem melhores sem segmentar de familias que merecem estudo segmentado.
4. Alimentar a proxima frente de pesquisa sobre padroes de prejuizo por time.
```

## Decisoes que este estudo NAO permite tomar

```text
1. Nao aprova operacao final.
2. Nao transforma segmentacao em filtro definitivo.
3. Nao salva automaticamente estrategias Goal negativas.
4. Nao deve eliminar estrategia sozinho.
5. Nao substitui validacao futura.
```

## Parecer exploratorio

```text
APROVADA COMO V1 EXPLORATORIA COM RESSALVA DE INTERPRETACAO
```

Conclusoes:

```text
1. A forca do favorito importa.
2. As melhores familias No Goal parecem mais fortes em jogos parelhos/sem favorito claro.
3. Goal nao ficou lucrativo no agregado em nenhum segmento.
4. Algumas familias Goal geraram hipoteses segmentadas, mas ainda com risco de overfitting.
5. both_teams_cold_2of3 parece especialmente interessante em jogos parelhos.
6. favorite_winning_by_1_opp_cold_2of3 teve resultado contraintuitivo: melhor em jogo parelho do que em favorito forte.
7. Esses achados devem alimentar a ANALISE_PADROES_PREJUIZO_POR_TIME_V1.
```

## Artefatos

- `analise_forca_favorito_por_estrategia_v1_market_direction_serie_a_2025_tempos_expandidos.csv`
- `analise_forca_favorito_por_estrategia_v1_familias_serie_a_2025_tempos_expandidos.csv`
- `analise_forca_favorito_por_estrategia_v1_estrategias_serie_a_2025_tempos_expandidos.csv`
- `analise_forca_favorito_por_estrategia_v1_variacoes_serie_a_2025_tempos_expandidos.csv`
- `analise_forca_favorito_por_estrategia_v1_tudo_junto_vs_segmentado_serie_a_2025_tempos_expandidos.csv`
- `analise_forca_favorito_por_estrategia_v1_alertas_serie_a_2025_tempos_expandidos.csv`
- `analise_forca_favorito_por_estrategia_v1_serie_a_2025_tempos_expandidos.json`
- `ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md`
