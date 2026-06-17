# API-Football Live Match Collector V2

## Objetivo

Coletar dados live de uma fixture da API-Football a cada 60 segundos, com foco em mercados selecionados:

- `1x2`
- `gols`
- `escanteios`
- `cartoes`

Documento de referencia operacional completo:

```text
docs/03_SOURCES/API_FOOTBALL/API_FOOTBALL_LIVE_ODDS_AUTOMATION_20260617.md
```

## Validacoes praticas registradas

- `Iraq vs Norway`, fixture `1539016`: teste positivo durante o jogo, com mercados live de gols e linhas.
- `France vs Senegal`, fixture `1489383`: teste pos-FT com `live_odds.json` vazio.
- `Fortaleza EC vs America Mineiro`, fixture `1520725`: live odds disponiveis perto do fim, mas com cobertura reduzida.

Conclusao:

```text
odds/live precisa ser coletado durante a partida
```

## Diferenca para a V1

- a V1 coletava `odds/live` completo;
- a V2 usa `odds/live/bets` para descobrir os `bet ids` live;
- a V2 tenta coletar apenas os mercados alvo;
- a V2 salva tambem `fixtures?live=all` a cada ciclo;
- a V2 adiciona retries/backoff.

## Limite importante da documentacao oficial

O endpoint `odds/live` documentado aceita filtro por:

- `fixture`
- `league`
- `bet`

Ele **nao documenta filtro por bookmaker**.

Por isso:

- a V2 tenta focar nos mercados corretos;
- mas **nao consegue garantir apenas Bet365 / Betfair Exchange / Betfair Sportsbook via parametro oficial**.

Esses nomes ficam registrados apenas como preferencia operacional no metadata.

## Mercados alvo

O script tenta localizar no catalogo live nomes equivalentes a:

- `Fulltime Result` / `Match Winner` / `1x2`
- `Over/Under Line` / `Match Goals`
- `Match Corners` / `Total Corners`
- `Total Cards`

Se algum mercado nao estiver disponivel naquela fixture, ele nao sera coletado.

## Exemplo de uso

```powershell
$env:API_FOOTBALL_KEY="SUA_CHAVE"
python C:\LateGoalResearch\Crawler\ApiFootball\api_football_live_match_collector_v2.py `
  --fixture-id 1489381 `
  --poll-seconds 60 `
  --capture-context `
  --output-root C:\LateGoalResearch\data\raw\api_football\live_monitor_v2
```

## Estrutura de saida

```text
data/raw/api_football/live_monitor_v2/
  fixture_<fixture_id>/
    run_metadata.json
    latest_status.json
    selected_live_bets.json
    poll_log.jsonl
    summary.md
    context_once/
      status.json
      odds_live_bets_catalog.json
      odds_prematch.json
      fixture_lineups.json
      fixture_players.json
      predictions.json
    snapshots/
      <timestamp>/
        fixture.json
        fixture_statistics.json
        fixture_events.json
        fixtures_live_all.json
        live_odds_match_result_1x2.json
        live_odds_goals_over_under.json
        live_odds_corners.json
        live_odds_cards.json
```

## Uso na automacao

A automacao do Codex so precisa:

1. descobrir o `fixture_id`;
2. disparar o script no inicio do jogo;
3. deixar o proprio coletor rodar ate o `FT`.

Launcher recomendado:

```text
scripts/api_football_world_cup_live_monitor_launcher.py
```
