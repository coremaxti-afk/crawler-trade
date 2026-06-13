# PRE_MATCH_FAVORITE_VALIDATION_V1

Status: NAO APROVADO

Data: 2026-06-13

## Resumo executivo

A validacao definitiva do filtro `favorite_winning_by_1` nao pode ser aprovada com os dados atuais. Existem arquivos `premium_odds.json` para a Premier League 2025/26, mas todos os 380 payloads coletados estao vazios (`data: []`). Portanto nao ha odds 1X2 pre-jogo utilizaveis para calcular `home_odd`, `draw_odd`, `away_odd`, favorito real, overround ou probabilidades implicitas.

Decisao: `favorite_winning_by_1` ainda nao deixa de ser proxy. Ele permanece bloqueado para validacao oficial ate haver odds pre-jogo 1X2 com cobertura suficiente e timestamp/bookmaker documentado.

## Fonte das odds premium

Pasta auditada:

```text
C:/LateGoalResearch/data/raw/sportmonks/full_collection/england_premier_league_league_8_season_25583_2025_2026/02_fixtures/*/10_market/premium_odds.json
```

Nenhum request novo foi feito. Foram lidos apenas arquivos ja coletados.

## Cobertura das odds

| Metrica | Valor |
|---|---:|
| Fixtures auditadas | 380 |
| Arquivos premium_odds existentes | 380 |
| JSONs validos | 380 |
| Payloads com `data: []` | 380 |
| Odds 1X2 pre-jogo utilizaveis | 0 |
| Home odds extraidas | 0 |
| Draw odds extraidas | 0 |
| Away odds extraidas | 0 |
| Bookmakers identificados | 0 |
| Timestamps identificados | 0 |

## Regra oficial proposta de favorito

Regra que seria usada se as odds existissem:

```text
Favorito real = menor odd pre-jogo 1X2, desde que a menor odd seja <= 1.70.
```

Classificacao:

| Faixa | Classe |
|---|---|
| odd_favorite <= 1.40 | super_favorite |
| 1.41 <= odd_favorite <= 1.70 | favorite |
| min(home_odd, away_odd) > 1.70 | no_clear_favorite |

Regras:

```text
Draw nao pode ser favorite_side operacional.
Odds de empate servem apenas para probabilidade implicita/overround.
```

## Resultado da validacao

Como os arquivos `premium_odds.json` estao vazios, nenhuma partida recebeu favorito real.

| Classe | N |
|---|---:|
| home_favorite | 0 |
| away_favorite | 0 |
| no_clear_favorite calculado | 0 |
| blocked_no_1x2_odds | 380 |

## Reexecucao das estrategias favorite_*

### favorite_winning_by_1 + h8_cold_combo_10m_2of3

| Metrica | Valor |
|---|---:|
| Historico original N | 54 |
| Historico original no_goal_60_75 | 74.1% |
| SportMonks proxy N | 69 |
| SportMonks proxy no_goal_60_75 | 69.6% |
| Favorito real via odds N | 0 |
| Decisao | NAO APROVADO |

Motivo:

```text
Nao existem odds 1X2 pre-jogo utilizaveis nos arquivos premium_odds coletados.
```

### favorite_winning_by_1 + h8_pressure_score_10m_bottom25

| Metrica | Valor |
|---|---:|
| Historico original N | 36 |
| Historico original no_goal_60_75 | 75.0% |
| SportMonks proxy N | 42 |
| SportMonks proxy no_goal_60_75 | 71.4% |
| Favorito real via odds N | 0 |
| Decisao | NAO APROVADO |

Motivo:

```text
Nao existem odds 1X2 pre-jogo utilizaveis nos arquivos premium_odds coletados.
```

## Comparacao proxy vs favorito real

A comparacao nao pode ser calculada.

```text
proxy antigo = time vencendo por 1 no cutoff
favorito real = bloqueado por ausencia de odds pre-jogo 1X2
```

Resultado:

```text
favorite_winning_by_1 continua proxy e nao foi validado oficialmente.
```

## Riscos de leakage

Nenhum leakage adicional foi introduzido, porque nenhuma odd foi usada como feature.

A regra metodologica permanece:

- odds pre-jogo devem ser anteriores ao kickoff;
- odds sem timestamp nao devem ser tratadas como live odds;
- odds live nao devem ser usadas nesta validacao;
- resultado final nao pode ser feature;
- gols pos-cutoff nao podem ser feature.

## Limitacoes

- `premium_odds.json` existe para 380 fixtures, mas todos os payloads estao vazios.
- Nao foi possivel confirmar bookmaker.
- Nao foi possivel confirmar timestamp.
- Nao foi possivel confirmar mercado 1X2.
- Nao foi possivel calcular favorito real.
- Nao foi possivel reexecutar `favorite_*` sem proxy.

## Decisao final

```text
NAO APROVADO
```

O filtro `favorite_winning_by_1` nao esta validado por odds pre-jogo.

## Proxima etapa recomendada

Investigar a causa dos `premium_odds.json` vazios antes de qualquer nova analise `favorite_*`.

Hipoteses:

1. Endpoint premiumOdds nao foi chamado com include/filtro correto.
2. Plano/API key nao tinha permissao para mercado 1X2 pre-match.
3. Fixtures EPL 2025/26 ainda nao tinham odds disponiveis no momento da coleta.
4. Odds premium SportMonks nao cobre o mercado esperado nessa estrutura.
5. O endpoint correto para odds pre-match pode ser outro recurso/rota.

Proxima tarefa sugerida:

```text
SPORTMONKS_PREMIUM_ODDS_EMPTY_PAYLOAD_DIAGNOSTIC_V1
```

Objetivo:

```text
Diagnosticar por que 380/380 premium_odds.json retornaram data: [] e descobrir a rota/configuracao correta para odds pre-jogo 1X2.
```
