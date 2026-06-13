# SPORTMONKS_PREMIUM_ODDS_EMPTY_PAYLOAD_DIAGNOSTIC_V1

Status: DIAGNOSTICO CONCLUIDO COM LIMITACAO

Data: 2026-06-13

Agente: Data Acquisition Engineer

## Resumo executivo

A causa mais provavel para `premium_odds.json` retornar `data: []` em 380/380 fixtures da Premier League 2025/26 e uso de rota inadequada para o objetivo de odds 1X2 pre-jogo historicas.

Os documentos internos mostram que os 380 arquivos `premium_odds.json` existem, todos sao JSONs validos, mas todos retornaram `data: []`, sem bookmaker, timestamp, mercado 1X2 ou odds home/draw/away utilizaveis.

A documentacao oficial SportMonks separa:

- Standard pre-match odds: `/v3/football/odds/pre-match/fixtures/{ID}`
- Premium pre-match odds por fixture: `/v3/football/odds/premium/fixtures/{ID}`
- Premium historical odds: `/v3/football/odds/premium/history`
- Premium historical odds updated between range: `/v3/football/odds/premium/history/updated/between/{from}/{to}`

Ponto critico: a propria documentacao do Premium Odds informa que odds pre-match por fixture ficam disponiveis por ate 7 dias apos o inicio da partida. Portanto, consultar fixtures historicas da EPL 2025/26 por `/odds/premium/fixtures/{ID}` depois da janela operacional pode retornar vazio mesmo que odds tenham existido antes.

Decisao final:

```text
CORRIGIR_ENDPOINT
```

Classificacao secundaria:

```text
ROTA_INADEQUADA_PARA_HISTORICO_PRE_JOGO
```

`favorite_winning_by_1` permanece bloqueado como validacao oficial por odds pre-jogo ate obter odds 1X2 com mercado, bookmaker e timestamp.

## Governanca e restricoes

Restricoes respeitadas:

- Nao foi criado robo.
- Nao foi criada producao.
- Nao foi executado trade real.
- Nao foi criado modelo.
- Nao foi criado baseline.
- Nao foi feito backtesting financeiro real.
- Nao foi alterado schema.
- Nao foi criado importer.
- Nao foram apagados dados brutos.
- Nao foi feita coleta massiva nova.
- Nao foi feita chamada externa com API key, pois nenhuma chave local foi disponibilizada neste ambiente.

## Arquivos e documentos inspecionados

Documentos internos:

- `docs/00_AGENTS/AGENT_COORDINATION.md`
- `docs/00_AGENTS/GOVERNANCE_V2.md`
- `docs/01_CONTEXT/PROJECT_STATUS.md`
- `docs/06_SPRINTS/CURRENT_SPRINT.md`
- `docs/04_RESEARCH/PRE_MATCH_FAVORITE_VALIDATION_V1.md`
- `docs/03_SOURCES/SPORTMONKS/README.md`
- `docs/03_SOURCES/SPORTMONKS/SPORTMONKS_EPL_2025_26_VALIDATION_AND_SOFASCORE_COMPARISON.md`

Pasta local esperada, nao acessivel diretamente neste ambiente:

```text
data/raw/sportmonks/full_collection/england_premier_league_league_8_season_25583_2025_2026/
```

Arquivos odds indicados pela validacao anterior:

```text
02_fixtures/*/10_market/premium_odds.json
```

Resultado ja documentado em `PRE_MATCH_FAVORITE_VALIDATION_V1`:

- fixtures auditadas: 380
- arquivos `premium_odds.json` existentes: 380
- JSONs validos: 380
- payloads `data: []`: 380
- odds 1X2 pre-jogo utilizaveis: 0
- bookmakers identificados: 0
- timestamps identificados: 0

## Limitacao de inspecao

Nao foi possivel abrir os JSONs brutos locais neste ambiente porque a pasta `C:/LateGoalResearch/...` nao esta montada no runtime atual e os arquivos brutos nao estao versionados no GitHub.

Tambem nao foi encontrado no GitHub codigo, log ou metadata contendo explicitamente:

- URL exata usada na coleta original;
- parametros exatos usados;
- includes exatos usados;
- filtros exatos usados;
- HTTP status salvo por fixture;
- headers ou request metadata.

Assim, a rota original foi inferida pelo nome `premium_odds.json` e pelo objetivo da coleta, mas nao foi comprovada por metadata de request.

## Documentacao oficial consultada

### Premium odds por fixture

Endpoint documentado:

```text
https://api.sportmonks.com/v3/football/odds/premium/fixtures/{ID}
```

Uso descrito:

```text
Returns the premium odds for the requested fixture ID.
```

Campos esperados no payload nao vazio:

- `fixture_id`
- `market_id`
- `bookmaker_id`
- `label`
- `value`
- `probability`
- `created_at`
- `updated_at`
- `latest_bookmaker_update`

Includes aceitos:

```text
market
bookmaker
fixture
history
```

Filtros estaticos aceitos:

```text
markets
bookmakers
```

Observacao critica da documentacao:

```text
Premium Odds Feed provides a history of pre-match odds for fixtures for up to 7 days after the match has started.
```

### Standard pre-match odds por fixture

Endpoint documentado:

```text
https://api.sportmonks.com/v3/football/odds/pre-match/fixtures/{ID}
```

Exemplo oficial mostra:

- `market_id`: 1
- `label`: Home
- `value`: 1.48
- `market_description`: Match Winner
- `bookmaker_id`
- `latest_bookmaker_update`

Esse endpoint corresponde melhor ao objetivo operacional de obter 1X2 pre-jogo home/draw/away.

### Mercados

Endpoint Standard Markets:

```text
https://api.sportmonks.com/v3/odds/markets
```

Exemplo oficial:

```text
id: 1
name: Fulltime Result
developer_name: FULLTIME_RESULT
```

Endpoint Premium Markets:

```text
https://api.sportmonks.com/v3/odds/markets/premium
```

Exemplo oficial tambem mostra:

```text
id: 1
name: Fulltime Result
developer_name: FULLTIME_RESULT
```

Portanto o mercado alvo 1X2 parece ser `market_id=1` / `FULLTIME_RESULT`.

### Premium historical odds

Endpoint documentado:

```text
https://api.sportmonks.com/v3/football/odds/premium/history
```

Endpoint por janela de atualizacao historica:

```text
https://api.sportmonks.com/v3/football/odds/premium/history/updated/between/{from}/{to}
```

Observacoes:

- O endpoint historico retorna registros por `odd_id`, nao diretamente por fixture/market/bookmaker sem include.
- Ele exige resolver a ligacao com a entidade PremiumOdd usando include `odd` e possivelmente filtros/joins depois.
- A rota de janela possui range maximo de 5 minutos.
- Isso pode ser caro em requests e precisa de spike controlado antes de qualquer escala.

## Hipoteses avaliadas

| Hipotese | Resultado | Evidencia | Decisao |
|---|---|---|---|
| Endpoint premiumOdds chamado com include/filtro incorreto | Parcialmente plausivel | endpoint aceita `include=market;bookmaker;history` e filtros `markets/bookmakers`; sem metadata nao da para confirmar chamada original | POSSIVEL |
| Plano/API key sem permissao | Inconclusivo | se nao houvesse permissao, poderia haver erro/403; mas os arquivos vazios nao bastam para provar permissao ou falta dela | INCONCLUSIVO |
| Fixtures EPL 2025/26 sem odds no momento | Parcialmente plausivel | fixtures futuras/distantes podem nao ter odds; porem 380/380 vazias sugere problema mais sistemico | POSSIVEL |
| Mercado 1X2 nao disponivel em premiumOdds | Nao confirmado | Premium Markets mostra Fulltime Result id 1; Standard Odds claramente mostra Match Winner/Home/Draw/Away | POUCO PROVAVEL |
| Rota correta para pre-match 1X2 e outro endpoint | Forte | Standard endpoint `/odds/pre-match/fixtures/{ID}` e dedicado a pre-match odds e exemplo oficial mostra mercado Match Winner | PROVAVEL |
| Filtros bookmaker/market nao passados | Possivel | mercado id 1 e bookmakers precisam ser filtrados/testados para reduzir payload e garantir 1X2 | POSSIVEL |
| Endpoint requer `markets/bookmakers/include` | Possivel para coleta direcionada | docs mostram filtros `markets` e `bookmakers`; include `market;bookmaker` recomendado para debug | POSSIVEL |
| Endpoint usado e premium atual, nao historico | Forte | premium fixture endpoint tem janela de ate 7 dias apos kickoff; EPL 2025/26 historica pode estar fora da janela | PROVAVEL |
| Temporada EPL 2025/26 sem historico completo no momento | Possivel | sem chamada controlada nao da para diferenciar cobertura vs janela/endpoint | POSSIVEL |
| Provider retorna odds apenas para fixtures especificas | Possivel | deve ser testado em 1-3 fixtures proximas/futuras e historicas recentes | POSSIVEL |

## Diagnostico provavel

O diagnostico mais provavel e:

```text
A coleta usou endpoint premium por fixture atual/recente para uma validacao historica de temporada inteira.
```

Esse endpoint nao e o caminho mais seguro para odds 1X2 historicas pre-jogo de uma temporada completa, especialmente apos a janela de 7 dias documentada pela SportMonks.

Para 1X2 pre-jogo, o caminho tecnicamente mais direto e testar primeiro:

```text
/v3/football/odds/pre-match/fixtures/{fixture_id}?include=market;bookmaker&filters=markets:1
```

Para Premium Odds historico, o caminho correto exige spike separado com:

```text
/v3/football/odds/premium/history
/v3/football/odds/premium/history/updated/between/{from}/{to}
```

com include `odd` e filtros suficientes para mapear `odd_id -> fixture_id/market_id/bookmaker_id`.

## Recomendacao operacional

### Caminho 1 — Corrigir para Standard Odds pre-match 1X2

Prioridade alta para validar `favorite_winning_by_1`.

Teste controlado em 1-3 fixtures:

```text
GET /v3/football/odds/pre-match/fixtures/{fixture_id}?include=market;bookmaker&filters=markets:1
```

Objetivo:

- encontrar labels `Home`, `Draw`, `Away`;
- confirmar `market_id=1` / Fulltime Result;
- confirmar `bookmaker_id`;
- confirmar `latest_bookmaker_update` ou `created_at/updated_at`;
- escolher regra de bookmaker/linha: bookmaker principal, mediana entre bookmakers, media, ou closing-like.

### Caminho 2 — Premium Odds historico

Executar apenas se o plano realmente incluir premium historical odds e se a API permitir mapear odds historicas para fixture/market/bookmaker.

Teste controlado:

```text
GET /v3/football/odds/premium/history?include=odd
GET /v3/football/odds/premium/history/updated/between/{from}/{to}?include=odd
```

Risco:

- grande volume;
- paginacao;
- janela maxima de 5 minutos no endpoint updated-between;
- pode exigir estrategia de incremental load, fora do escopo atual.

### Caminho 3 — Usar Football-Data como fonte imediata de favorito

Para EPL 2024/25, Football-Data ja tem 1X2 e mapping 100% com SofaScore. Portanto e a fonte mais segura para validar favorito real em historico ja consolidado.

Limite:

- nao resolve EPL 2025/26 SportMonks se ainda nao houver CSV equivalente;
- odds sem timestamp granular live nao devem ser tratadas como live.

### Caminho 4 — API-Football

API-Football ja retornou odds pre-jogo em spike anterior. Pode ser testada em fixture EPL/plano Pro como alternativa complementar para 1X2.

## Decisao final

```text
CORRIGIR_ENDPOINT
```

Motivo:

- `premium_odds.json` vazio em 380/380 nao prova ausencia definitiva de odds.
- A documentacao mostra endpoint standard pre-match por fixture proprio para odds pre-jogo.
- A documentacao mostra que premium fixture odds tem janela de ate 7 dias apos kickoff.
- Para temporada historica, premium odds exige rota historica separada ou outra fonte.

## Estado de `favorite_winning_by_1`

Permanece:

```text
NAO APROVADO
```

Nao usar como favorito real ate obter odds 1X2 pre-jogo com:

- fixture_id;
- market_id 1 / Fulltime Result;
- labels Home/Draw/Away;
- bookmaker_id;
- timestamp de atualizacao;
- regra documentada de escolha da odd.

## Proximo passo recomendado

Data Acquisition Engineer deve executar um spike minimo, nao massivo:

1. Escolher 1 fixture historica recente dentro de 7 dias, se existir.
2. Escolher 1 fixture futura proxima.
3. Testar Standard Odds pre-match market 1.
4. Testar Premium Odds por fixture market 1 apenas se estiver dentro da janela.
5. Testar Premium Historical Odds apenas com 1 pequena janela de tempo.
6. Documentar resposta, sem importer, schema, dataset ou modelagem.
