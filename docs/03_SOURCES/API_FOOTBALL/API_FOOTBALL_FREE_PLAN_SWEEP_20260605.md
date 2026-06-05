# API-Football Free Plan Sweep - 20260605

## Escopo

Varredura controlada do plano gratuito da API-Football para avaliar cobertura antes de qualquer teste pago do plano PRO.

Esta execucao nao substitui oficialmente SofaScore, nao altera banco, schema, importers, datasets, features ou modelagem.

## Requests

- Total de requests consumidos: 52
- Limite absoluto: 100
- Margem operacional respeitada: sim

## Discovery

Foi usado discovery minimo por data/status `FT` em 2026-06-05. O plano gratuito retornou fixtures suficientes na primeira data consultada, entao nao houve discovery amplo.

## Fixtures Testadas

| Fixture | Liga | Pais | Temporada | Data | Status | Placar |
|---|---|---|---:|---|---|---|
| 1490721 | 1. Liga U19 | Czech-Republic | 2025 | 2026-06-05T09:00:00+00:00 | FT | Karvina U19 2 x 1 Zlin U19 |
| 1489726 | 3. liga - CFL A | Czech-Republic | 2025 | 2026-06-05T14:00:00+00:00 | FT | Dukla Praha II 0 x 3 Pisek |
| 1487603 | 4. liga - Divizie D | Czech-Republic | 2025 | 2026-06-05T15:00:00+00:00 | FT | Lisen II 5 x 1 Humpolec |
| 1547213 | ASEAN Championship U19 | World | 2025 | 2026-06-05T09:00:00+00:00 | FT | Brunei U19 0 x 4 Malaysia U19 |
| 1542893 | Friendlies | World | 2026 | 2026-06-05T00:00:00+00:00 | FT | Czech Republic 3 x 1 Guatemala |

## Matriz de Cobertura

Arquivo gerado localmente:

- `data/raw/api_football/sweeps/free_plan_20260605/coverage_matrix.csv`

Resumo por classificacao final da matriz:

- util: 21
- vazio: 29

## Endpoints Uteis

- `fixture`: util em 5/5 fixtures.
- `fixture_events`: util em 4/5 fixtures.
- `predictions`: util em 5/5 fixtures.
- `head_to_head`: util em 5/5 fixtures.
- `fixture_lineups`: util em 1/5 fixtures.
- `odds`: util em 1/5 fixtures.

## Observacao de Rate Limit

- A API retornou `x-ratelimit-requests-limit=100`, indicando limite diario de 100 requests.
- A API tambem retornou `x-ratelimit-limit=10`, indicando janela curta de 10 requests.
- A primeira tentativa recebeu `HTTP 429` no request 11 ao tentar `head_to_head` da fixture `1490721`.
- O script foi ajustado para aguardar automaticamente quando `x-ratelimit-remaining=0` e a varredura foi retomada sem sobrescrever JSON bruto.
- Nao houve HTTP 403.

## Endpoints Vazios, Bloqueados, Indisponiveis ou Pagos

- `fixture_statistics`: vazio em 5/5 fixtures.
- `fixture_players`: vazio em 5/5 fixtures.
- `injuries`: vazio em 5/5 fixtures.
- `live_odds`: vazio em 5/5 fixtures.
- Nao houve mensagem explicita de plano pago nos endpoints testados.
- Nao houve HTTP 403.
- Houve 1 HTTP 429 transitorio por janela curta, nao por esgotamento diario.

## Exemplos Concretos

### Fixture 1490721

- `fixture_events`: 25' Goal Normal Goal - Karvina U19 - L. Tlolka.
- `predictions`: winner=Karvina U19; advice=Combo Double chance : Karvina U19 or draw and +1.5 goals.
- `head_to_head`: 10 registros.

### Fixture 1489726

- `fixture_events`: 22' Goal Normal Goal - Pisek - R. Polansky.
- `predictions`: winner=Pisek; advice=Double chance : draw or Pisek.
- `head_to_head`: 8 registros.

### Fixture 1487603

- `fixture_events`: sem registros.
- `predictions`: winner=Lisen II; advice=Winner : Lisen II.
- `head_to_head`: 6 registros.

### Fixture 1547213

- `fixture_events`: 22' Goal Normal Goal - Malaysia U19 - L. Hadi.
- `predictions`: winner=Malaysia U19; advice=Combo Winner : Malaysia U19 and +2.5 goals.
- `head_to_head`: 2 registros.

### Fixture 1542893

- `fixture_events`: 11' Goal Normal Goal - Czech Republic - P. Schick.
- `fixture_lineups`: Czech Republic com 11 titulares, formacao 5-4-1.
- `odds`: 11 bookmakers.
- `predictions`: winner=Czech Republic; advice=Combo Winner : Czech Republic and +1.5 goals.
- `head_to_head`: 1 registro.

## Comparacao com Spikes Anteriores

- `fixture_1524704` (USL League Two): utilidade limitada a fixture, predictions e head-to-head; endpoints centrais de jogo vieram vazios.
- `fixture_1545540` (Botola Pro): retornou fixture, events, lineups, odds, predictions e head-to-head; statistics parcialmente preenchido; players/injuries/live_odds vazios.

## Parecer Final

API-Football Free serve como complemento candidato para `fixture`, `fixture_events`, `predictions` e `head_to_head`.

O endpoint `fixture_events` retornou eventos minuto a minuto em 4/5 fixtures, sugerindo utilidade real para auditoria de eventos, mas ainda nao substitui SofaScore porque `statistics`, `players`, `injuries` e `live_odds` permaneceram vazios em toda a amostra.

O endpoint `lineups` e `odds` apareceu apenas na fixture de amistoso internacional, indicando cobertura inconsistente por liga/competicao.

O PRO so parece justificar teste pago se o objetivo for ampliar janela historica/temporadas e confirmar se `events`, `lineups`, `statistics`, `players` e `odds` mantem cobertura em ligas-alvo. Sem essa confirmacao, nao ha base para substituir SofaScore.

## Restricoes Respeitadas

- Nenhum banco foi alterado.
- Nenhum schema foi alterado.
- Nenhum importer foi criado ou alterado.
- Nenhum dataset, feature, baseline ou modelo foi criado.
- Nenhum coletor SofaScore foi alterado.
- Spikes anteriores nao foram sobrescritos.
- JSONs foram salvos como dados brutos exploratorios.
