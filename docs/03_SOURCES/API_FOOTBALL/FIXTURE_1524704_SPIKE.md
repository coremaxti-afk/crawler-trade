# Spike API-Football - Fixture 1524704

Data da execucao: 2026-06-04

## Objetivo

Executar um spike controlado da API-Football com apenas 1 partida finalizada, salvando JSON bruto localmente e avaliando empiricamente quais endpoints retornam dados uteis no plano gratuito.

Este documento nao oficializa substituicao do SofaScore. Ele registra apenas o resultado exploratorio do spike.

## Escopo executado

- Fonte: API-Football v3.
- Fixture testada: `1524704`.
- Partida: Texoma 4 x 1 Fort Worth Vaqueros.
- Liga: USL League Two, USA.
- Temporada: 2026.
- Data da partida: `2026-06-03T00:00:00+00:00`.
- Status: FT.
- Estadio: Sherman Bearcat Stadium.

A Premier League historica nao foi usada porque o plano gratuito retornou restricao de acesso por data. A descoberta indicou disponibilidade apenas para a janela `2026-06-03` a `2026-06-05` naquele momento.

## Local dos dados brutos

Os arquivos foram salvos localmente em:

```text
C:\LateGoalResearch\data\raw\api_football\spikes\fixture_1524704\
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

- Descoberta do fixture_id: 6 requests.
- Spike da fixture: 10 requests.
- Total desta investigacao: 16 requests.
- Limite operacional do script de spike: 100 requests.
- O spike executado consumiu 10 requests e parou dentro do limite.

O `request_log.jsonl` registrou cada request executado no spike. O ultimo retorno do spike indicou `x-ratelimit-requests-remaining: 89`.

## Endpoints testados

| Endpoint | Arquivo bruto | Classificacao | Observacao |
| --- | --- | --- | --- |
| `/fixtures?id=1524704` | `fixture.json` | util | Retornou metadados, placar, status, times, liga e estadio. |
| `/fixtures/statistics?fixture=1524704` | `fixture_statistics.json` | vazio | HTTP 200, sem registros. |
| `/fixtures/events?fixture=1524704` | `fixture_events.json` | vazio | HTTP 200, sem registros. |
| `/fixtures/lineups?fixture=1524704` | `fixture_lineups.json` | vazio | HTTP 200, sem registros. |
| `/fixtures/players?fixture=1524704` | `fixture_players.json` | vazio | HTTP 200, sem registros. |
| `/predictions?fixture=1524704` | `predictions.json` | util | Retornou predicao, forma dos times, comparacoes e h2h embutido. |
| `/injuries?fixture=1524704` | `injuries.json` | vazio | HTTP 200, sem registros. |
| `/odds?fixture=1524704` | `odds.json` | vazio | HTTP 200, sem registros. |
| `/odds/live?fixture=1524704` | `live_odds.json` | vazio | HTTP 200, sem registros. |
| `/fixtures/headtohead?h2h=25487-9047` | `head_to_head.json` | util | Retornou 2 confrontos entre os times. |

Nenhum endpoint testado retornou HTTP 403, erro de indisponibilidade ou mensagem explicita de plano pago durante o spike.

## Dados uteis encontrados

### Fixture

O endpoint `/fixtures` retornou:

- identificacao da partida;
- data e status FT;
- estadio;
- liga, pais, temporada e rodada;
- times mandante e visitante;
- placar final;
- placar do intervalo.

Resultado observado:

- Texoma 4 x 1 Fort Worth Vaqueros;
- intervalo: Texoma 2 x 0 Fort Worth Vaqueros.

### Predictions

O endpoint `/predictions` retornou dados potencialmente uteis para contexto pre-jogo:

- vencedor previsto: Texoma;
- conselho: `Winner : Texoma`;
- percentuais: home 50%, draw 50%, away 0%;
- forma recente dos times;
- medias de gols marcados e sofridos;
- comparacao de forma, ataque, defesa, poisson, h2h e gols;
- h2h embutido com partida anterior.

Pontos relevantes:

- Texoma: forma recente `WLW`, 10 gols marcados e 2 sofridos em 3 jogos da liga.
- Fort Worth Vaqueros: forma recente `LLLLL`, 0 gols marcados e 17 sofridos em 5 jogos da liga.
- Comparacao total: Texoma 89%, Fort Worth Vaqueros 11%.

### Head to Head

O endpoint `/fixtures/headtohead` retornou 2 confrontos:

- 2026-05-20: Fort Worth Vaqueros 0 x 7 Texoma.
- 2026-06-03: Texoma 4 x 1 Fort Worth Vaqueros.

## Dados nao encontrados nesta partida

Apesar de todos os endpoints terem respondido HTTP 200, os seguintes dados vieram vazios:

- eventos da partida;
- estatisticas da partida;
- escalacoes;
- estatisticas de jogadores;
- lesoes;
- odds pre-jogo;
- odds ao vivo.

Isso significa que, para esta fixture especifica, a API-Football nao forneceu os dados mais importantes para substituir os endpoints ricos do SofaScore.

## Desafios encontrados

1. A Premier League 2024/25 nao estava disponivel no plano gratuito no momento da descoberta.
2. A API indicou restricao por janela de datas no plano gratuito.
3. A fixture valida encontrada pertence a uma liga de menor cobertura.
4. Endpoints tecnicamente disponiveis retornaram HTTP 200, mas sem dados detalhados.
5. O limite por janela curta chegou a 10/10 requests no fim do spike, entao execucoes consecutivas precisam de espera.
6. A chave da API nao estava configurada como variavel permanente de ambiente; foi usada apenas no processo de execucao para evitar persistencia local.

## Solucoes aplicadas

1. Foi feita uma descoberta minima de fixture com 6 requests.
2. Foi escolhida apenas 1 partida finalizada.
3. O script isolado `api_football_fixture_spike.py` foi usado sem alterar banco, importer, features, schema ou coletores SofaScore.
4. Cada endpoint gerou JSON bruto ou registro claro em `request_log.jsonl`.
5. O spike ficou abaixo do limite diario de 100 requests.
6. Os dados foram mantidos como material bruto exploratorio, sem transformacao para fonte oficial.

## Avaliacao de substituicao ou complemento ao SofaScore

A API-Football pode complementar o projeto com:

- metadados de partidas;
- placar final e intervalo;
- contexto pre-jogo via predictions;
- historico direto entre times;
- forma recente e comparacoes agregadas.

Com base nesta fixture, a API-Football ainda nao substitui o SofaScore para:

- eventos minuto a minuto;
- estatisticas detalhadas da partida;
- escalacoes;
- estatisticas de jogadores;
- dados ricos in-game.

Conclusao: o spike confirma potencial de complemento, mas nao confirma substituicao oficial do SofaScore. Para uma avaliacao mais forte, seria necessario repetir um spike controlado com uma partida de liga com maior cobertura dentro da janela permitida pelo plano gratuito, mantendo o mesmo limite baixo de requests.

## Restricoes respeitadas

- Nenhum banco foi alterado.
- Nenhum importer foi criado.
- Nenhuma feature foi criada.
- Nenhuma modelagem foi feita.
- Nenhum schema foi alterado.
- Nenhum coletor SofaScore foi alterado.
- Nenhuma execucao em lote foi feita.
- Apenas 1 fixture foi coletada no spike.
- Os dados foram salvos como JSON bruto exploratorio.
