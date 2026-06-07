# API-Football Free Plan Sweep - 20260607

## Escopo

Varredura controlada do plano gratuito da API-Football para avaliar cobertura antes de qualquer teste pago do plano PRO.

Esta execucao nao substitui oficialmente SofaScore, nao altera banco, schema, importers, datasets, features ou modelagem.

## Requests

- Total de requests consumidos: 91
- Limite absoluto: 100
- Margem operacional respeitada: sim

## Discovery

Foi usado discovery minimo por data/status `FT` nos dias recentes permitidos pelo plano gratuito. Se habilitado, `live=all` testa no maximo uma fixture live.

## Fixtures Testadas

| Fixture | Liga | Pais | Temporada | Data | Status | Placar |
|---|---|---|---:|---|---|---|
| 1534325 | 1. Division | Belarus | 2026 | 2026-06-07T11:00:00+00:00 | FT | Niva 1 x 1 Orsha |
| 1487714 | 4. liga - Divizie E | Czech-Republic | 2025 | 2026-06-07T08:15:00+00:00 | FT | SlaviÄÃ­n 1 x 0 Bzenec |
| 1487830 | 4. liga - Divizie F | Czech-Republic | 2025 | 2026-06-07T08:15:00+00:00 | FT | HavÃ­Å™ov 0 x 3 Vratimov |
| 1510596 | Division 2 - Norra GÃ¶taland | Sweden | 2026 | 2026-06-07T11:00:00+00:00 | FT | Herrestads 1 x 0 Motala |
| 1510778 | Division 2 - Norra Svealand | Sweden | 2026 | 2026-06-07T11:00:00+00:00 | FT | Helges 1 x 4 KungsÃ¤ngen |
| 1515749 | Division 2 - Norrland | Sweden | 2026 | 2026-06-07T11:00:00+00:00 | FT | Storfors 0 x 2 Boden |
| 1511143 | Division 2 - SÃ¶dra Svealand | Sweden | 2026 | 2026-06-07T11:00:00+00:00 | FT | Karlslund 1 x 3 Sleipner |
| 1504452 | Ettan - SÃ¶dra | Sweden | 2026 | 2026-06-07T11:00:00+00:00 | FT | AFC Malmo 2 x 1 Eskilsminne |
| 1537650 | Friendlies | World | 2026 | 2026-06-07T00:00:00+00:00 | FT | CuraÃ§ao 4 x 0 Aruba |

## Matriz de Cobertura

Ver arquivo bruto:

- `data\raw\api_football\sweeps\free_plan_20260607\coverage_matrix.csv`

Resumo por classificacao:

- util: 40
- util_parcial: 1
- vazio: 49

## Endpoints Uteis

- `fixture`: {'util': 9}
- `fixture_events`: {'util': 7, 'vazio': 2}
- `fixture_lineups`: {'vazio': 8, 'util_parcial': 1}
- `predictions`: {'util': 9}
- `odds`: {'vazio': 3, 'util': 6}
- `head_to_head`: {'util': 9}

## Endpoints Vazios, Bloqueados, Indisponiveis ou Pagos

- `fixture_statistics`: {'vazio': 9}
- `fixture_players`: {'vazio': 9}
- `injuries`: {'vazio': 9}
- `live_odds`: {'vazio': 9}

## Exemplos Concretos

### Fixture 1534325

- `fixture`: 1 registros
- `fixture_events`: 4' Goal Normal Goal - Orsha - M. Pashkevich
- `fixture_statistics`: sem registros
- `fixture_lineups`: sem registros
- `fixture_players`: sem registros
- `predictions`: winner=Niva, advice=Winner : Niva
- `injuries`: sem registros
- `odds`: sem registros
- `live_odds`: sem registros
- `head_to_head`: 8 registros

### Fixture 1487714

- `fixture`: 1 registros
- `fixture_events`: sem registros
- `fixture_statistics`: sem registros
- `fixture_lineups`: sem registros
- `fixture_players`: sem registros
- `predictions`: winner=Bzenec, advice=Double chance : draw or Bzenec
- `injuries`: sem registros
- `odds`: sem registros
- `live_odds`: sem registros
- `head_to_head`: 14 registros

### Fixture 1487830

- `fixture`: 1 registros
- `fixture_events`: sem registros
- `fixture_statistics`: sem registros
- `fixture_lineups`: sem registros
- `fixture_players`: sem registros
- `predictions`: winner=HavÃ­Å™ov, advice=Double chance : HavÃ­Å™ov or draw
- `injuries`: sem registros
- `odds`: sem registros
- `live_odds`: sem registros
- `head_to_head`: 8 registros

### Fixture 1510596

- `fixture`: 1 registros
- `fixture_events`: 2' Goal Normal Goal - Herrestads - I. Omicevic
- `fixture_statistics`: sem registros
- `fixture_lineups`: sem registros
- `fixture_players`: sem registros
- `predictions`: winner=Herrestads, advice=Double chance : Herrestads or draw
- `injuries`: sem registros
- `odds`: 11 bookmakers
- `live_odds`: sem registros
- `head_to_head`: 6 registros

### Fixture 1510778

- `fixture`: 1 registros
- `fixture_events`: 12' Goal Normal Goal - KungsÃ¤ngen - O. Asell
- `fixture_statistics`: sem registros
- `fixture_lineups`: sem registros
- `fixture_players`: sem registros
- `predictions`: winner=None, advice=No predictions available
- `injuries`: sem registros
- `odds`: 11 bookmakers
- `live_odds`: sem registros
- `head_to_head`: 2 registros

### Fixture 1515749

- `fixture`: 1 registros
- `fixture_events`: 48' Goal Normal Goal - Boden - T. Warne
- `fixture_statistics`: sem registros
- `fixture_lineups`: sem registros
- `fixture_players`: sem registros
- `predictions`: winner=Boden, advice=Double chance : draw or Boden
- `injuries`: sem registros
- `odds`: 2 bookmakers
- `live_odds`: sem registros
- `head_to_head`: 6 registros

### Fixture 1511143

- `fixture`: 1 registros
- `fixture_events`: 4' Goal Normal Goal - Sleipner - E. Devic
- `fixture_statistics`: sem registros
- `fixture_lineups`: sem registros
- `fixture_players`: sem registros
- `predictions`: winner=Sleipner, advice=Double chance : draw or Sleipner
- `injuries`: sem registros
- `odds`: 11 bookmakers
- `live_odds`: sem registros
- `head_to_head`: 4 registros

### Fixture 1504452

- `fixture`: 1 registros
- `fixture_events`: 12' Goal Normal Goal - AFC Malmo - A. Reuterskiold
- `fixture_statistics`: sem registros
- `fixture_lineups`: sem registros
- `fixture_players`: sem registros
- `predictions`: winner=AFC Malmo, advice=Combo Double chance : AFC Malmo or draw and +1.5 goals
- `injuries`: sem registros
- `odds`: 12 bookmakers
- `live_odds`: sem registros
- `head_to_head`: 2 registros

### Fixture 1537650

- `fixture`: 1 registros
- `fixture_events`: 53' Goal Normal Goal - CuraÃ§ao - J. Brenet
- `fixture_statistics`: sem registros
- `fixture_lineups`: CuraÃ§ao: 0 titulares, formacao=None
- `fixture_players`: sem registros
- `predictions`: winner=CuraÃ§ao, advice=Double chance : CuraÃ§ao or draw
- `injuries`: sem registros
- `odds`: 11 bookmakers
- `live_odds`: sem registros
- `head_to_head`: 2 registros

## Comparacao com Spikes Anteriores

- `fixture_1524704` (USL League Two): utilidade limitada a fixture, predictions e head-to-head; endpoints centrais de jogo vieram vazios.
- `fixture_1545540` (Botola Pro): retornou fixture, events, lineups, odds, predictions e head-to-head; statistics parcialmente preenchido; players/injuries/live_odds vazios.

## Parecer Final

API-Football Free serve como complemento candidato para: `fixture`, `fixture_events`, `predictions`, `odds`, `head_to_head`.

O PRO so parece justificar teste pago se o objetivo for ampliar janela historica/temporadas e confirmar se `events`, `lineups`, `statistics`, `players` e `odds` mantem cobertura em ligas-alvo. Sem essa confirmacao, nao ha base para substituir SofaScore.

## Restricoes Respeitadas

- Nenhum banco foi alterado.
- Nenhum schema foi alterado.
- Nenhum importer foi criado ou alterado.
- Nenhum dataset, feature, baseline ou modelo foi criado.
- Nenhum coletor SofaScore foi alterado.
- Spikes anteriores nao foram sobrescritos.
- JSONs foram salvos como dados brutos exploratorios.
