# RUNNERS_OPERACIONAIS_COLETA_E_DISCOVERY

Este arquivo centraliza os runners simplificados criados para facilitar a coleta e analise por liga/temporada.

Objetivo: evitar comandos longos no PowerShell. Na maioria dos casos, basta informar:

```text
--league-id
--season-id
```

Os runners usam os mapas locais do projeto para descobrir caminhos, labels e arquivos.

## Mapas usados pelos runners

Mapa SportMonks com ligas e temporadas:

```text
C:\LateGoalResearch\data\raw\sportmonks\league_season_map\league_last_3_seasons.json
```

Mapa Football-Data com codigos de odds:

```text
C:\LateGoalResearch\data\raw\football_data\football_data_league_odds_map.csv
```

Coletas SportMonks completas:

```text
C:\LateGoalResearch\data\raw\sportmonks\full_collection\
```

CSVs Football-Data:

```text
C:\LateGoalResearch\data\raw\football_data\
```


---

# 0. Coletar dados SportMonks full season

## Runner

```text
C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py
```

## O que faz

Executa a coleta SportMonks usando apenas `season-id` ou `league-id + season-id`.

Resolve automaticamente:

```text
country-label
league-label
season-label
pasta de saida
```

## Conferir sem coletar

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py `
  --season-id 25659 `
  --dry-run
```

## Coletar H8 da temporada

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py `
  --league-id 564 `
  --season-id 25659
```

O padrao e `--categories h8`.

## Coletar todas as categorias

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py `
  --league-id 564 `
  --season-id 25659 `
  --categories all
```

## Testar com poucos jogos

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py `
  --league-id 564 `
  --season-id 25659 `
  --fixture-limit 3 `
  --max-requests 50
```

---

# 1. Baixar odds Football-Data

## Runner

```text
C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py
```

## O que faz

Baixa o CSV bruto do Football-Data para a liga/temporada informada.

Resolve automaticamente:

```text
codigo Football-Data
pais
league-label
temporada
source-type
pasta de saida
```

## Conferir sem baixar

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py `
  --league-id 564 `
  --season-id 25659 `
  --dry-run
```

## Baixar odds

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py `
  --league-id 564 `
  --season-id 25659
```

## Forcar novo download

Use apenas se quiser sobrescrever o CSV local:

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py `
  --league-id 564 `
  --season-id 25659 `
  --force
```

## Saida esperada

Exemplo LaLiga 2025/26:

```text
C:\LateGoalResearch\data\raw\football_data\spain\la_liga_2025_2026\SP1_2025_2026.csv
```

---

# 2. Rodar Strategy Discovery V2

## Runner

```text
C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py
```

## O que faz

Executa o discovery V2 usando dados SportMonks + odds Football-Data.

Resolve automaticamente:

```text
pasta SportMonks 02_fixtures
CSV Football-Data
season-label
summary CSV
entries CSV
relatorio Markdown
```

## Conferir sem executar

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py `
  --league-id 564 `
  --season-id 25659 `
  --dry-run
```

## Executar discovery

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py `
  --league-id 564 `
  --season-id 25659
```

## Saidas esperadas

Resumo CSV:

```text
C:\LateGoalResearch\data\processed\reports\sportmonks_team_side_strategy_discovery_summary_v2_<liga>_<temporada>_tempos_expandidos.csv
```

Entradas CSV:

```text
C:\LateGoalResearch\data\processed\reports\sportmonks_team_side_strategy_discovery_entries_v2_<liga>_<temporada>_tempos_expandidos.csv
```

Relatorio Markdown:

```text
C:\LateGoalResearch\docs\04_RESEARCH\SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V2_<LIGA>_<TEMPORADA>_TEMPOS_EXPANDIDOS.md
```

## Observacao

Este runner usa por padrao o script editado:

```text
C:\LateGoalResearch\Crawler\Sportmonks\sportmonks_team_side_strategy_discovery_v2 editado.py
```

Esse script inclui tempos/targets expandidos e exportacao CSV ajustada.

---

# 3. Rodar Drawdown

## Runner

```text
C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py
```

## O que faz

Calcula drawdown operacional a partir do `entries.csv` gerado pelo discovery V2.

Resolve automaticamente:

```text
entries CSV da liga/temporada
config com todas as estrategias
drawdown summary
drawdown trades
marcadores league_id, league_label, season_id, season_label
```

## Conferir sem executar

```powershell
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py `
  --league-id 564 `
  --season-id 25659 `
  --dry-run
```

## Executar drawdown

```powershell
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py `
  --league-id 564 `
  --season-id 25659
```

## Modo padrao

Por padrao, o runner usa **todas as estrategias do entries.csv**, nao apenas Top 10.

Ele cria automaticamente:

```text
C:\LateGoalResearch\data\processed\reports\strategy_drawdown_config_all_<liga>_<temporada>_tempos_expandidos.json
```

## Voltar para config manual Top 10

Se quiser usar a config antiga/manual:

```powershell
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py `
  --league-id 564 `
  --season-id 25659 `
  --use-config
```

Config manual padrao:

```text
C:\LateGoalResearch\configs\strategy_drawdown_config_v1.json
```

## Saidas esperadas

Resumo drawdown:

```text
C:\LateGoalResearch\data\processed\reports\strategy_drawdown_summary_<liga>_<temporada>_tempos_expandidos.csv
```

Trades drawdown:

```text
C:\LateGoalResearch\data\processed\reports\strategy_drawdown_trades_<liga>_<temporada>_tempos_expandidos.csv
```

## Regra de cashout estimado

O runner classifica automaticamente:

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
Lay Over 60_75 com no goal: +25,00
Lay Over 60_75 com goal: -50,00
Back Over 60_75 com goal: +50,00
Back Over 60_75 sem goal: -25,00
```

Esses valores sao **ESTIMATIVA OPERACIONAL COM ODDS MEDIAS**, nao backtesting financeiro real com odds live.

---

# 4. Fluxo recomendado por liga/temporada

## Passo 1: baixar odds Football-Data

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py `
  --league-id 564 `
  --season-id 25659
```

## Passo 2: rodar discovery V2

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py `
  --league-id 564 `
  --season-id 25659
```

## Passo 3: rodar drawdown

```powershell
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py `
  --league-id 564 `
  --season-id 25659
```

---

# 5. Exemplos prontos

## LaLiga 2025/26

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py --league-id 564 --season-id 25659
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py --league-id 564 --season-id 25659
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py --league-id 564 --season-id 25659
```

## LaLiga 2024/25

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py --league-id 564 --season-id 23621
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py --league-id 564 --season-id 23621
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py --league-id 564 --season-id 23621
```

## Premier League 2025/26

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py --league-id 8 --season-id 25583
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py --league-id 8 --season-id 25583
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py --league-id 8 --season-id 25583
```

---

# 6. Onde encontro league-id e season-id?

Use este arquivo:

```text
C:\LateGoalResearch\data\raw\sportmonks\league_season_map\league_last_3_seasons.json
```

Campos importantes:

```text
country
league_id
league_label
api_name
season_id
season_label
season_name
is_current
```

Tambem existe a versao XML:

```text
C:\LateGoalResearch\data\raw\sportmonks\league_season_map\league_last_3_seasons.xml
```

---

# 7. Observacoes importantes

- Se o runner Football-Data disser que a liga nao esta disponivel, consulte `football_data_league_odds_map.csv`.
- Se o discovery disser que nao encontrou `entries` ou `fixtures`, confirme se a coleta SportMonks da temporada ja existe.
- Se aparecer `missing_odds`, provavelmente faltam aliases de nomes entre SportMonks e Football-Data.
- Os CSVs foram ajustados para leitura no Excel PT-BR com separador `;` e colunas formatadas quando aplicavel.
- Os relatorios Markdown do discovery sao gerados automaticamente pelo runner do discovery V2.
