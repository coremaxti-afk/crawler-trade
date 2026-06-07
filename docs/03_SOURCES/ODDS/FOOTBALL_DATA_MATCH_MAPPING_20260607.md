# Football-Data x SofaScore Match Mapping - 20260607

## Escopo

Match mapping exploratorio entre Football-Data.co.uk EPL 2024/25 e SofaScore EPL 2024/25.

Esta tarefa nao cria importer, nao altera schema, nao altera banco, nao cria dataset, nao cria features, nao modela e nao faz backtesting.

## Fontes

- Football-Data: `data/raw/football_data/england/premier_league_2024_2025/E0_2024_2025.csv`
- SofaScore inventory: `Crawler/Sofascore/data/raw/sofascore/premier_league_61627/inventory.json`
- SofaScore eventos: `Crawler/Sofascore/data/raw/sofascore/premier_league_61627/matches/{event_id}/event.json`
- Documento base: `docs/03_SOURCES/ODDS/FOOTBALL_DATA_DISCOVERY_20260607.md`

## Resumo Executivo

- Total de partidas Football-Data: **380**.
- Total no inventory SofaScore: **381**.
- Total SofaScore importavel considerado: **380**.
- Total pareadas: **380**.
- Taxa de pareamento Football-Data: **100.00%**.
- Partidas Football-Data nao pareadas: **0**.
- Partidas SofaScore importaveis nao pareadas: **0**.
- Ambiguidades de chave: **0**.
- Conflitos de placar detectados por data/time: **0**.
- Partidas pareadas com horario identico em UTC: **379/380**.
- Placar/resultado compativel nas pareadas: **380/380**.
- Recomendacao: **avancar para Data Engineer**.

## Regra de Pareamento

Chave exploratoria usada:

```text
date_key + normalized_home_team + normalized_away_team + full_time_score
```

Regras:

- Football-Data `Date` + `Time` foi interpretado como horario local `Europe/London`.
- SofaScore `startTimestamp` foi convertido de UTC para `Europe/London` para criar a data local.
- Placar Football-Data: `FTHG-FTAG`.
- Placar SofaScore: `homeScore.current-awayScore.current`.
- Foi excluida a partida conhecida `12436452`, cancelada/nao importavel.
- Foram considerados apenas eventos SofaScore com `status.type = finished` e placar disponivel.

## Regras de Normalizacao de Times

| Football-Data / Variacao | Normalizado |
|---|---|
| `Man United` | `manchester united` |
| `Man City` | `manchester city` |
| `Newcastle` | `newcastle united` |
| `Nott'm Forest` | `nottingham forest` |
| `Wolves` | `wolverhampton` |
| `Tottenham` | `tottenham hotspur` |
| `West Ham` | `west ham united` |
| `Brighton` / `Brighton & Hove Albion` | `brighton hove albion` |
| `Ipswich` | `ipswich town` |
| `Leicester` | `leicester city` |
| `Bournemouth` / `AFC Bournemouth` | `bournemouth` |

## Conflitos de Nomes

| Normalizado | Nomes originais observados |
|---|---|
| brighton hove albion | Brighton, Brighton & Hove Albion |
| ipswich town | Ipswich, Ipswich Town |
| leicester city | Leicester, Leicester City |
| liverpool | Liverpool, Liverpool FC |
| manchester city | Man City, Manchester City |
| manchester united | Man United, Manchester United |
| newcastle united | Newcastle, Newcastle United |
| nottingham forest | Nott'm Forest, Nottingham Forest |
| tottenham hotspur | Tottenham, Tottenham Hotspur |
| west ham united | West Ham, West Ham United |
| wolverhampton | Wolverhampton, Wolves |

Todos os conflitos observados sao resolviveis por dicionario explicito de nomes.

## Diferencas de Data/Hora

| Event ID | Partida | Football-Data | SofaScore local | Dif. min |
|---|---|---|---|---|
| 12437030 | Ipswich x Everton | 19/10/2024 15:00 | 2024-10-19T15:15:00+01:00 | 15 |

## Compatibilidade de Placar

- Nenhuma incompatibilidade de placar foi detectada nas partidas pareadas.
- Resultado H/D/A compativel em **380/380** partidas pareadas.

## Partidas Nao Pareadas - Football-Data

- Nenhuma partida Football-Data ficou sem pareamento.

## Partidas Nao Pareadas - SofaScore Importavel

- Nenhuma partida SofaScore importavel ficou sem pareamento.

## Ambiguidades

- Nenhuma ambiguidade relevante de chave foi encontrada.

## Exemplos de Partidas Pareadas

| Event ID | Date | Time | Football-Data | SofaScore | Score | Dif. min |
|---|---|---|---|---|---|---|
| 12436870 | 16/08/2024 | 20:00 | Man United x Fulham | Manchester United x Fulham | 1-0 | 0 |
| 12436872 | 17/08/2024 | 15:00 | Arsenal x Wolves | Arsenal x Wolverhampton | 2-0 | 0 |
| 12436873 | 17/08/2024 | 15:00 | Everton x Brighton | Everton x Brighton & Hove Albion | 0-3 | 0 |
| 12436871 | 17/08/2024 | 12:30 | Ipswich x Liverpool | Ipswich Town x Liverpool FC | 0-2 | 0 |
| 12436874 | 17/08/2024 | 15:00 | Newcastle x Southampton | Newcastle United x Southampton | 1-0 | 0 |
| 12436875 | 17/08/2024 | 15:00 | Nott'm Forest x Bournemouth | Nottingham Forest x Bournemouth | 1-1 | 0 |
| 12436877 | 17/08/2024 | 17:30 | West Ham x Aston Villa | West Ham United x Aston Villa | 1-2 | 0 |
| 12436879 | 18/08/2024 | 14:00 | Brentford x Crystal Palace | Brentford x Crystal Palace | 2-1 | 0 |
| 12436880 | 18/08/2024 | 16:30 | Chelsea x Man City | Chelsea x Manchester City | 0-2 | 0 |
| 12436881 | 19/08/2024 | 20:00 | Leicester x Tottenham | Leicester City x Tottenham Hotspur | 1-1 | 0 |
| 12436886 | 24/08/2024 | 17:30 | Aston Villa x Arsenal | Aston Villa x Arsenal | 0-2 | 0 |
| 12436888 | 24/08/2024 | 12:30 | Brighton x Man United | Brighton & Hove Albion x Manchester United | 2-1 | 0 |

## Criterio CTO

| Criterio | Resultado | Status |
|---|---:|---|
| Pareamento >= 95% | 100.00% | APROVADO |
| Conflitos resolviveis por dicionario explicito | 11 grupos | APROVADO |
| Placar compativel | 380/380 | APROVADO |
| Sem ambiguidade relevante | 0 ambiguidades | APROVADO |

## Recomendacao

**AVANCAR PARA DATA ENGINEER**.

Football-Data atingiu os criterios exploratorios para avancar para Data Engineer:

- 380/380 partidas pareadas.
- 100% de taxa de pareamento.
- 0 partidas nao pareadas.
- 0 ambiguidades relevantes.
- 0 conflitos de placar.
- Conflitos de nomes resolviveis por dicionario explicito.

Proximo passo recomendado:

1. Data Engineer/CTO especificar tabela ou contrato de mapping sem alterar schema ainda.
2. Validar oficialmente dicionario de nomes.
3. Somente depois propor importer Football-Data sob aprovacao CTO.

## Restricoes Respeitadas

- Nenhum importer criado.
- Nenhum banco alterado.
- Nenhum schema alterado.
- Nenhum dataset criado.
- Nenhuma feature criada.
- Nenhuma modelagem executada.
- Nenhum backtesting executado.
