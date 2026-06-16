# RUN_STRATEGY_DRAWDOWN_SIMPLIFICADO

## Objetivo

Este runner calcula drawdown usando os `entries.csv` gerados pelo discovery V2, sem precisar montar caminhos manualmente.

Ele recebe:

```text
--league-id
--season-id
```

E adiciona marcadores nas saidas:

```text
league_id
league_label
season_id
season_label
season
```

## Script

```text
C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py
```

## Conferir sem executar

```powershell
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py `
  --league-id 564 `
  --season-id 25659 `
  --dry-run
```

## Executar LaLiga 2025/26

```powershell
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py `
  --league-id 564 `
  --season-id 25659
```

## Executar LaLiga 2024/25

```powershell
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py `
  --league-id 564 `
  --season-id 23621
```

## Marcadores opcionais

Se quiser forcar um marcador de liga:

```powershell
--league-label la_liga
```

Se quiser forcar um marcador de temporada:

```powershell
--season-marker la_liga_2025_26
```

## Saidas

O runner salva em:

```text
C:\LateGoalResearch\data\processed\reports\strategy_drawdown_summary_<liga>_<temporada>_<tag>.csv
C:\LateGoalResearch\data\processed\reports\strategy_drawdown_trades_<liga>_<temporada>_<tag>.csv
```

## Observacao

Este runner nao altera a logica financeira. Ele apenas localiza o CSV de entradas, chama `calc_strategy_drawdown.py` e adiciona marcadores confiaveis de liga/temporada nas saidas.
## Modo padrao: todas as estrategias

Por padrao, o runner nao usa mais apenas a config Top 10.

Ele le o `entries.csv` do discovery e gera automaticamente uma config com todas as combinacoes encontradas:

```text
strategy_name + cutoff + target + window
```

A config gerada fica em:

```text
C:\LateGoalResearch\data\processed\reports\strategy_drawdown_config_all_<liga>_<temporada>_<tag>.json
```

Se quiser voltar para a config manual Top 10, use:

```powershell
--use-config
```

## Regra de cashout estimado

O runner classifica automaticamente o settlement pelo minuto final do target:

```text
target termina antes de 90 => CASHOUT_ESTIMADO
target termina em 90       => HOLD_FINAL
```

Exemplos:

```text
no_goal_60_75 => lay_over + CASHOUT_ESTIMADO
goal_60_75    => back_over + CASHOUT_ESTIMADO
no_goal_60_90 => lay_over + HOLD_FINAL
goal_60_90    => back_over + HOLD_FINAL
```

Com stake 100 e odds medias 60=1.50, 75=2.00:

```text
Lay Over 60_75 com no goal: lucro estimado = 25, nao 100
Lay Over 60_75 com goal: red = -50
Back Over 60_75 com goal: lucro = 50
Back Over 60_75 sem goal: cashout estimado = -25
```

Esses valores continuam sendo **ESTIMATIVA OPERACIONAL COM ODDS MEDIAS**, nao backtesting financeiro real com odds live.
