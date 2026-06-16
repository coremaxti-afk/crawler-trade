# CHAT_HANDOFF_TECHNICAL_SUMMARY_20260616

## Objetivo deste arquivo

Resumo tecnico para handoff a um novo chat, cobrindo o que foi implementado e ajustado no projeto LateGoalResearch em SportMonks + Football-Data + discovery/drawdown.

---

## 1. Contexto operacional

O projeto real esta em:

```text
C:\LateGoalResearch
```

O workspace original do chat estava em outra pasta, por isso houve atrito para `git add / commit / push` diretamente em `C:\LateGoalResearch`.

### Implicacao

- Foi possivel ler/editar arquivos em `C:\LateGoalResearch` com permissao elevada.
- O fluxo Git direto a partir desta sessao nao ficou confiavel para versionamento do repo real.
- Para normalizar commits, o ideal e abrir o Codex diretamente em `C:\LateGoalResearch`.

---

## 2. Mapas de ligas e temporadas

Arquivos principais:

```text
C:\LateGoalResearch\data\raw\sportmonks\league_season_map\league_last_3_seasons.json
C:\LateGoalResearch\data\raw\sportmonks\league_season_map\league_last_3_seasons.xml
C:\LateGoalResearch\data\raw\sportmonks\league_season_map\league_season_map.json
```

### Campos importantes

```text
country
league_id
league_label
api_name
season_id
season_label
season_name
starting_at
ending_at
is_current
```

Esses arquivos foram usados como base para os runners simplificados por `league_id` e `season_id`.

---

## 3. Football-Data

### 3.1 Coletor base criado

Arquivo:

```text
C:\LateGoalResearch\Crawler\FootballData\football_data_odds_collector.py
```

### O que faz

- Baixa CSV bruto do Football-Data.co.uk.
- Salva sem transformar os dados.
- Gera `download_metadata.json` com auditoria simples.

### Parametros principais

```text
--league-code
--country
--league-label
--season
--source-type
--force
```

### Tutorial

```text
C:\LateGoalResearch\docs\03_SOURCES\ODDS\FOOTBALL_DATA_ODDS_COLLECTOR.md
```

---

### 3.2 Runner simplificado Football-Data

Arquivo:

```text
C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py
```

### O que faz

Recebe apenas:

```text
--league-id
--season-id
```

E resolve automaticamente:

```text
football_data_code
country
league_label
season_label
source_type
```

### Tutorial

```text
C:\LateGoalResearch\docs\03_SOURCES\ODDS\RUN_FOOTBALL_DATA_ODDS_COLLECTOR_SIMPLIFICADO.md
```

---

### 3.3 Mapa SportMonks x Football-Data

Arquivo:

```text
C:\LateGoalResearch\data\raw\football_data\football_data_league_odds_map.csv
```

### Status do mapa

- 30 ligas SportMonks avaliadas.
- 25 ligas com referencia Football-Data identificada.
- 5 ligas sem referencia confirmada no mapa local.

### Ligas sem disponibilidade confirmada no mapa

```text
Brazil Serie B
Czech Republic Chance Liga
Croatia 1. HNL
Saudi Arabia Pro League
Thailand Thai Premier League
```

---

### 3.4 CSVs Football-Data baixados nesta frente

Confirmados no raw local:

```text
C:\LateGoalResearch\data\raw\football_data\england\premier_league_2024_2025\E0_2024_2025.csv
C:\LateGoalResearch\data\raw\football_data\england\premier_league_2025_2026\E0_2025_2026.csv
C:\LateGoalResearch\data\raw\football_data\spain\la_liga_2024_2025\SP1_2024_2025.csv
C:\LateGoalResearch\data\raw\football_data\spain\la_liga_2025_2026\SP1_2025_2026.csv
```

A LaLiga 24/25 foi validada com uma copia dedicada do coletor:

```text
C:\LateGoalResearch\Crawler\FootballData\football_data_odds_collector_la_liga_24_25.py
```

---

## 4. SportMonks full season collection

### 4.1 Coletor base existente

Arquivo:

```text
C:\LateGoalResearch\Crawler\Sportmonks\sportmonks_full_season_collector.py
```

### Padrao de salvamento

Nao foi alterado pelos runners. Continua salvando em:

```text
C:\LateGoalResearch\data\raw\sportmonks\full_collection\<pais>_<liga>_league_<league_id>_season_<season_id>_<season_label>
```

Exemplo:

```text
C:\LateGoalResearch\data\raw\sportmonks\full_collection\spain_la_liga_league_564_season_25659_2025_2026
```

---

### 4.2 Runner simplificado SportMonks collector

Arquivo:

```text
C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py
```

### O que faz

Aceita:

```text
--season-id
```

ou, de forma mais segura:

```text
--league-id
--season-id
```

E resolve automaticamente:

```text
country-label
league-label
season-label
output-root
```

### Parametros uteis

```text
--categories
--fixture-limit
--max-requests
--delay-min
--delay-max
--retries
--force
--dry-run
```

### Tutorial

```text
C:\LateGoalResearch\docs\04_RESEARCH\TUTORIAL SCRIPTS\RUN_SPORTMONKS_FULL_SEASON_COLLECTOR_SIMPLIFICADO.md
```

---

## 5. Strategy Discovery V2

### 5.1 Script base

Arquivos principais:

```text
C:\LateGoalResearch\Crawler\Sportmonks\sportmonks_team_side_strategy_discovery_v2.py
C:\LateGoalResearch\Crawler\Sportmonks\sportmonks_team_side_strategy_discovery_v2 editado.py
```

### Observacao

O script `editado.py` e o que foi usado nos ajustes mais recentes.

---

### 5.2 O que foi ajustado no script editado

#### a) Targets expandidos

Foram ampliadas combinacoes em:

```text
TARGETS_UNDER
TARGETS_OVER
```

Exemplos adicionados pelo usuario:

```text
60_75
60_85
60_90
```

#### b) Aliases LaLiga

Foi corrigido o pareamento entre SportMonks e Football-Data via `TEAM_ALIASES`.

Problema original:

```text
missing_odds alto por diferenca de nomes
```

Exemplos de alias tratados:

```text
Athletic Club <-> Ath Bilbao
Atlético de Madrid <-> Ath Madrid
FC Barcelona <-> Barcelona
Real Betis <-> Betis
Celta de Vigo <-> Celta
Deportivo Alavés <-> Alaves
Rayo Vallecano <-> Vallecano
Real Sociedad <-> Sociedad
Espanyol <-> Espanol
Real Oviedo <-> Oviedo
```

Resultado apos ajuste:

```text
LaLiga 2025/26: missing_odds caiu para 0
```

#### c) Exportacao CSV amigavel ao Excel

A funcao de escrita do script editado foi ajustada para:

```text
delimiter = ;
encoding = utf-8-sig
```

#### d) Summary mais legivel

Foram adicionadas colunas auxiliares no summary do discovery, como:

```text
rate_pct
baseline_pct
diff_vs_baseline_pp
odds_ratio_fmt
p_value_fmt
```

E o summary passou a ser ordenado para leitura.

---

### 5.3 Runner simplificado do discovery

Arquivo:

```text
C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py
```

### O que faz

Recebe:

```text
--league-id
--season-id
```

E resolve automaticamente:

```text
SportMonks 02_fixtures
Football-Data CSV
season-label
summary CSV
entries CSV
report MD
```

### Tutorial

```text
C:\LateGoalResearch\docs\04_RESEARCH\TUTORIAL SCRIPTS\RUN_STRATEGY_DISCOVERY_V2_SIMPLIFICADO.md
```

---

### 5.4 Resultados relevantes validados

#### LaLiga 2025/26

Antes do ajuste de aliases, houve alto `missing_odds`.

Depois do ajuste:

```text
fixtures: 380
missing_odds: 0
matched: 380
base_rows: 9120
```

#### Saidas usadas

```text
C:\LateGoalResearch\data\processed\reports\sportmonks_team_side_strategy_discovery_summary_v2_la_liga_2025_26_tempos_expandidos.csv
C:\LateGoalResearch\data\processed\reports\sportmonks_team_side_strategy_discovery_entries_v2_la_liga_2025_26_tempos_expandidos.csv
C:\LateGoalResearch\docs\04_RESEARCH\SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V2_LA_LIGA_2025_26_TEMPOS_EXPANDIDOS.md
```

#### LaLiga 2024/25

Saidas equivalentes tambem foram geradas/parametrizadas.

---

## 6. Estrategia naming reference

Arquivo criado:

```text
C:\LateGoalResearch\docs\04_RESEARCH\STRATEGY_NAMING_AND_DEFINITIONS_REFERENCE_V1.md
```

CSV auxiliar:

```text
C:\LateGoalResearch\data\processed\reports\strategy_naming_definitions_reference_v1.csv
```

### O que documenta

- Termos como `favorite`, `underdog`, `opp_cold_2of3`, `pressure_high_2of3`, `pressing`.
- Regras de favorito, placar, lado analisado e thresholds.
- Estrategias obrigatorias como:

```text
favorite_drawing_pressure_high_2of3
favorite_losing_pressure_high_2of3
underdog_winning_favorite_pressing_2of3
favorite_winning_by_1_opp_cold_2of3
team_winning_by_1_opp_cold_2of3
home_winning_by_1_visitor_pressing
away_winning_by_1_home_pressing
both_teams_cold_2of3
big_chances_recent
key_passes_recent_high
opponent_no_recent_key_passes
```

### Ressalva importante documentada

`both_teams_cold_2of3` no nome sugere 2 de 3, mas o codigo executa 3 de 4 condicoes frias.

---

## 7. Drawdown

### 7.1 Script base ajustado

Arquivo:

```text
C:\LateGoalResearch\scripts\research\calc_strategy_drawdown.py
```

### Ajustes feitos

#### a) Leitura de CSV com `;`

O script passou a detectar e ler CSV separado por `;` ou `,`.

#### b) Escrita amigavel ao Excel

Saidas passaram a usar:

```text
encoding = utf-8-sig
delimiter = ;
```

#### c) Cashout estimado documentado no codigo

Foi mantida a logica existente, mas ajustado o uso operacional via runner:

```text
target final < 90 => CASHOUT_ESTIMADO
target final >= 90 => HOLD_FINAL
```

---

### 7.2 Runner simplificado do drawdown

Arquivo:

```text
C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py
```

### O que faz

Recebe:

```text
--league-id
--season-id
```

E resolve automaticamente:

```text
entries.csv da liga/temporada
config de estrategias
summary drawdown
trades drawdown
marcadores league_id, league_label, season_id, season_label
```

### Parametros uteis

```text
--league-label
--season-marker
--tag
--entries
--config
--use-config
--stake
--initial-bank
--dry-run
```

### Tutorial

```text
C:\LateGoalResearch\docs\04_RESEARCH\TUTORIAL SCRIPTS\RUN_STRATEGY_DRAWDOWN_SIMPLIFICADO.md
```

---

### 7.3 Mudanca importante no runner de drawdown

#### Antes

Usava apenas Top 10 estrategias da config manual:

```text
C:\LateGoalResearch\configs\strategy_drawdown_config_v1.json
```

#### Agora

Por padrao, o runner gera automaticamente uma config com **todas as estrategias** encontradas no `entries.csv`.

Arquivo gerado automaticamente:

```text
C:\LateGoalResearch\data\processed\reports\strategy_drawdown_config_all_<liga>_<temporada>_<tag>.json
```

Exemplo validado:

```text
C:\LateGoalResearch\data\processed\reports\strategy_drawdown_config_all_la_liga_2025_26_tempos_expandidos.json
```

Na LaLiga 2025/26, isso gerou:

```text
714 estrategias
```

Se quiser voltar para a config manual antiga, usar:

```text
--use-config
```

---

### 7.4 Regra operacional de cashout no drawdown

Agora o runner classifica settlement automaticamente:

```text
no_goal_60_75 => lay_over + CASHOUT_ESTIMADO
goal_60_75    => back_over + CASHOUT_ESTIMADO
no_goal_60_90 => lay_over + HOLD_FINAL
goal_60_90    => back_over + HOLD_FINAL
```

### Validacao unitária com stake 100 e odds medias 60=1.50 / 75=2.00

```text
Lay Over 60_75 com no goal: +25,00
Lay Over 60_75 com goal: -50,00
Back Over 60_75 com goal: +50,00
Back Over 60_75 sem goal: -25,00
```

Isso corrige a distorcao anterior em que alguns cenarios curtos estavam sendo tratados como lucro total de hold.

---

### 7.5 Saidas de drawdown formatadas para Excel

Os CSVs de drawdown passaram a incluir colunas legiveis, mantendo as colunas brutas.

Exemplos de colunas novas:

```text
strike_rate_pct
profit_final_fmt
ROI_pct
EV_per_trade_fmt
max_drawdown_abs_fmt
max_drawdown_pct_fmt
profit_fmt
equity_fmt
drawdown_fmt
```

Exemplo de leitura:

```text
27,0%
50,00
1,4%
1,35
-150,00
15,0%
```

### Arquivos validados

```text
C:\LateGoalResearch\data\processed\reports\strategy_drawdown_summary_la_liga_2025_26_tempos_expandidos.csv
C:\LateGoalResearch\data\processed\reports\strategy_drawdown_trades_la_liga_2025_26_tempos_expandidos.csv
```

Execucao real validada para LaLiga 2025/26:

```text
summary_rows: 714
trade_rows: 77335
```

---

## 8. Documentacao consolidada dos runners

Arquivo criado:

```text
C:\LateGoalResearch\docs\04_RESEARCH\TUTORIAL SCRIPTS\RUNNERS_OPERACIONAIS_COLETA_E_DISCOVERY.md
```

### O que centraliza

- Runner SportMonks full season
- Runner Football-Data odds
- Runner Strategy Discovery V2
- Runner Drawdown
- Fluxo recomendado por liga/temporada
- Exemplos prontos para LaLiga 24/25, LaLiga 25/26 e EPL 25/26

---

## 9. Runners principais hoje

### SportMonks full season

```text
C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py
```

### Football-Data odds

```text
C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py
```

### Strategy discovery V2

```text
C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py
```

### Drawdown

```text
C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py
```

---

## 10. Fluxo operacional recomendado

### Exemplo LaLiga 2025/26

1. Coletar SportMonks:

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_sportmonks_full_season_collector.py --league-id 564 --season-id 25659
```

2. Baixar odds Football-Data:

```powershell
python C:\LateGoalResearch\Crawler\FootballData\run_football_data_odds_collector.py --league-id 564 --season-id 25659
```

3. Rodar discovery V2:

```powershell
python C:\LateGoalResearch\Crawler\Sportmonks\run_strategy_discovery_v2.py --league-id 564 --season-id 25659
```

4. Rodar drawdown:

```powershell
python C:\LateGoalResearch\scripts\research\run_strategy_drawdown.py --league-id 564 --season-id 25659
```

---

## 11. Pendencias / cuidados para novo chat

### Git / versionamento

Se a intencao for commitar e subir tudo corretamente para GitHub, abrir o proximo chat diretamente em:

```text
C:\LateGoalResearch
```

### Aliases por liga

A LaLiga ja foi ajustada. Outras ligas provavelmente vao precisar de `TEAM_ALIASES` proprios para resolver `missing_odds`.

### Ligas sem Football-Data confirmado

Nao assumir disponibilidade universal; consultar sempre:

```text
C:\LateGoalResearch\data\raw\football_data\football_data_league_odds_map.csv
```

### Drawdown

O runner agora e muito mais util para screening amplo, mas continua sendo:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```

Nao tratar isso como backtesting financeiro real com odds live.

---

## 12. Arquivo criado para handoff

Este proprio resumo:

```text
C:\LateGoalResearch\docs\04_RESEARCH\CHAT_HANDOFF_TECHNICAL_SUMMARY_20260616.md
```
