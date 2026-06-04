# Spike API-Football - Fixture 1545540

Data da execucao: 2026-06-04

## Objetivo

Executar um segundo spike controlado da API-Football com apenas 1 partida finalizada de liga com maior cobertura que a USL League Two, salvando JSON bruto localmente e avaliando se os endpoints centrais retornam dados uteis.

Este documento nao oficializa substituicao do SofaScore. Ele registra apenas o resultado exploratorio do segundo spike.

## Fixture escolhida

- Fixture: `1545540`
- Partida: Ittihad Tanger 2 x 1 Wydad AC
- Liga: Botola Pro
- Pais: Morocco
- Temporada: 2025
- Rodada: Regular Season - 22
- Data: `2026-06-03T18:00:00+00:00`
- Status: FT
- Intervalo: 0 x 0
- Estadio: Stade Ibn Batouta

A fixture foi escolhida porque estava finalizada dentro da janela disponivel no plano gratuito e pertence a uma liga profissional nacional de maior cobertura relativa que a USL League Two usada no primeiro spike.

## Descoberta minima

Foi feita 1 request de descoberta por data/status:

```text
/fixtures?date=2026-06-03&status=FT
```

A busca nao executou lote e nao coletou dados detalhados antes da escolha da fixture.

## Local dos dados brutos

Os arquivos foram salvos localmente em:

```text
C:\LateGoalResearch\data\raw\api_football\spikes\fixture_1545540\
```

Arquivos gerados:

- `fixture.json`
- `fixture_statistics.json`
- `fixture_events.json`
- `fixture_lineups.json`
- `fixture_players.json`
- `predictions.json`
- `injuries.json`
- `odds.json`
- `live_odds.json`
- `head_to_head.json`
- `request_log.jsonl`
- `summary.md`

## Consumo de requests

- Descoberta minima: 1 request.
- Spike da fixture: 10 requests.
- Total da operacao: 11 requests.
- Limite definido para o segundo spike: 30 requests.
- O spike executado consumiu 10 requests e ficou abaixo do limite.

O `request_log.jsonl` registrou todos os 10 requests do spike. O ultimo retorno indicou `x-ratelimit-requests-remaining: 82` e `x-ratelimit-remaining: 4`.

## Endpoints testados

| Endpoint | Arquivo bruto | Classificacao | Observacao |
| --- | --- | --- | --- |
| `/fixtures?id=1545540` | `fixture.json` | util | Retornou metadados, placar, status, times, liga, rodada e estadio. |
| `/fixtures/statistics?fixture=1545540` | `fixture_statistics.json` | util parcial | Retornou 2 registros de time, mas a maioria dos campos veio vazia; cartoes vieram preenchidos. |
| `/fixtures/events?fixture=1545540` | `fixture_events.json` | util | Retornou 14 eventos de jogo. |
| `/fixtures/lineups?fixture=1545540` | `fixture_lineups.json` | util | Retornou escalações, banco e técnicos para os dois times. |
| `/fixtures/players?fixture=1545540` | `fixture_players.json` | vazio | HTTP 200, sem estatisticas de jogadores. |
| `/predictions?fixture=1545540` | `predictions.json` | util | Retornou predicao, percentuais, forma e comparativos. |
| `/injuries?fixture=1545540` | `injuries.json` | vazio | HTTP 200, sem registros. |
| `/odds?fixture=1545540` | `odds.json` | util | Retornou odds pre-jogo com multiplos bookmakers e mercados. |
| `/odds/live?fixture=1545540` | `live_odds.json` | vazio | HTTP 200, sem odds ao vivo para a fixture finalizada. |
| `/fixtures/headtohead?h2h=974-968` | `head_to_head.json` | util | Retornou historico direto entre Ittihad Tanger e Wydad AC. |

Nenhum endpoint testado retornou HTTP 403, erro de indisponibilidade ou mensagem explicita de plano pago.

## Dados uteis encontrados

### Fixture

O endpoint `/fixtures` retornou dados completos de contexto:

- identificacao da partida;
- data e status FT;
- liga, pais, temporada e rodada;
- estadio;
- times mandante e visitante;
- placar final;
- placar do intervalo.

Resultado observado:

- Ittihad Tanger 2 x 1 Wydad AC;
- intervalo: 0 x 0.

### Events

O endpoint `/fixtures/events` retornou 14 eventos:

- 5 cartoes;
- 6 substituicoes;
- 3 gols.

Eventos de gol observados:

- 61': Wydad AC, Mohamed Moufid;
- 74': Ittihad Tanger, Jawad Rhabra;
- 90+4': Ittihad Tanger, Mohamed El Arouch.

Este endpoint e relevante para H9, pois fornece eventos que alteram o estado da partida.

### Statistics

O endpoint `/fixtures/statistics` retornou estrutura para os dois times, mas com preenchimento muito limitado.

Campos preenchidos observados:

- Ittihad Tanger: Yellow Cards = 3, Red Cards = 0;
- Wydad AC: Yellow Cards = 2, Red Cards = 0.

Campos importantes como finalizacoes, posse, escanteios, passes e expected_goals apareceram na estrutura, mas sem valor preenchido nesta fixture.

Conclusao parcial: o endpoint existe e pode ser mapeado, mas a cobertura dos valores ainda precisa ser validada em outras competicoes antes de ser tratado como fonte robusta para estatisticas in-game.

### Lineups

O endpoint `/fixtures/lineups` retornou dados para os dois times:

- Ittihad Tanger: 11 titulares, 9 reservas, tecnico Abdelhak Benchikha;
- Wydad AC: 11 titulares, 9 reservas, tecnico Amine Benhachem.

As formacoes vieram nulas nesta fixture.

### Odds

O endpoint `/odds` retornou dados substanciais:

- 13 bookmakers;
- 324 mercados de aposta agregados;
- exemplos de bookmakers: 10Bet, William Hill, Bet365, Marathonbet, Unibet, Betfair, BetVictor, Pinnacle, SBO e 1xBet.

Exemplos de mercados retornados:

- Asian Handicap;
- Both Teams Score;
- Double Chance;
- Exact Goals Number;
- Correct Score;
- Corners Over Under;
- Team Goals;
- Cards e corners em diferentes recortes.

Este endpoint pode complementar dados pre-jogo e odds, mas ainda precisa de avaliacao de consistencia historica e disponibilidade por liga.

### Predictions

O endpoint `/predictions` retornou:

- vencedor previsto: Wydad AC;
- conselho: `Double chance : draw or Wydad AC`;
- percentuais: home 10%, draw 45%, away 45%.

Predictions podem complementar hipoteses pre-jogo, mas nao substituem dados in-game.

### Head to Head

O endpoint `/fixtures/headtohead` retornou 21 confrontos historicos entre os times.

Amostra observada:

- 2018-04-29: Ittihad Tanger 0 x 0 Wydad AC;
- 2017-04-30: Ittihad Tanger 0 x 1 Wydad AC;
- 2019-01-24: Ittihad Tanger 1 x 0 Wydad AC;
- 2020-03-12: Ittihad Tanger 0 x 2 Wydad AC;
- 2021-04-26: Ittihad Tanger 3 x 2 Wydad AC.

## Dados vazios nesta fixture

Os seguintes endpoints responderam HTTP 200, mas sem registros:

- `/fixtures/players`;
- `/injuries`;
- `/odds/live`.

## Comparacao com o primeiro spike

Primeiro spike, fixture `1524704`, USL League Two:

- uteis: fixture, predictions, head_to_head;
- vazios: events, statistics, lineups, players, injuries, odds, live_odds.

Segundo spike, fixture `1545540`, Botola Pro:

- uteis: fixture, events, lineups, predictions, odds, head_to_head;
- util parcial: statistics;
- vazios: players, injuries, live_odds.

Interpretacao: a ausencia de dados centrais no primeiro spike parece fortemente associada a cobertura da liga/fixture, nao a uma indisponibilidade geral da API-Football no plano gratuito.

## Desafios encontrados

1. A Premier League historica continuou fora da janela do plano gratuito.
2. A escolha precisou respeitar a janela disponivel do plano gratuito, sem discovery amplo.
3. Mesmo em liga profissional, estatisticas vieram quase todas vazias.
4. Estatisticas de jogadores nao foram retornadas.
5. Odds ao vivo nao vieram para fixture finalizada, o que era esperado ou pelo menos plausivel.
6. A API tem limite curto de requests por janela, entao o spike foi executado com intervalo entre chamadas.

## Solucoes aplicadas

1. Foi feita apenas 1 request de descoberta por data/status.
2. Foi escolhida apenas 1 fixture finalizada.
3. O script isolado `api_football_fixture_spike.py` foi reutilizado sem alterar banco, importer, features, schema ou coletores SofaScore.
4. O spike foi executado com `--request-budget 30`.
5. Cada endpoint gerou JSON bruto e entrada em `request_log.jsonl`.
6. O primeiro spike (`fixture_1524704`) nao foi sobrescrito.

## Avaliacao de substituicao ou complemento ao SofaScore

A API-Football deve seguir como: **complemento candidato**.

Motivos:

- Retornou eventos de partida, lineups, odds, predictions, fixture e head-to-head em uma liga de cobertura maior.
- Pode complementar H2, H7 e H9 com dados pre-jogo, eventos e contexto historico.
- Pode ajudar a reduzir dependencia de uma unica fonte.

Limites importantes:

- Nao confirmou cobertura robusta de estatisticas in-game.
- Nao retornou estatisticas de jogadores.
- Nao retornou odds ao vivo para esta fixture.
- Nao substitui match_graph/momentum do SofaScore.
- Ainda nao deve ser promovida a fonte oficial.

Conclusao: o segundo spike justifica manter API-Football como complemento candidato, mas nao como substituta oficial do SofaScore para dados in-game ricos. Antes de qualquer decisao arquitetural, recomenda-se que Data Acquisition/CTO definam se vale executar novo teste controlado em uma liga ainda mais coberta quando ela estiver disponivel no plano gratuito.

## Restricoes respeitadas

- Nenhum banco foi alterado.
- Nenhum importer foi criado.
- Nenhuma feature foi criada.
- Nenhuma modelagem foi feita.
- Nenhum schema foi alterado.
- Nenhum coletor SofaScore foi alterado.
- Nenhuma coleta em lote foi feita.
- Apenas 1 fixture foi coletada no segundo spike.
- O segundo spike ficou abaixo de 30 requests.
- O primeiro spike nao foi sobrescrito.
- Os dados foram salvos como JSON bruto exploratorio.
