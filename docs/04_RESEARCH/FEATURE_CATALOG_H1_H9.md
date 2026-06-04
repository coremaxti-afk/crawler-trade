# FEATURE CATALOG H1-H9

## Status

Definicao metodologica inicial.

Nao implementado.

Nao contem codigo.

Nao contem modelo.

---

## Contexto

Este documento define o catalogo formal de features para as hipoteses H1-H9 do LateGoalResearch.

Base atual:

- `matches_master`: 380 partidas.
- `match_statistics`: 380 partidas.
- `match_incidents`: 7647 registros.

Status da base:

- APTO COM RESSALVAS.

Ressalvas conhecidas:

- `big_chances_home`: 7 nulos.
- `big_chances_away`: 7 nulos.
- `match_graph` ainda nao populada.
- lineups e h2h estao fora do core v1.

---

## Regras Gerais

Toda feature deve possuir:

- nome claro;
- hipotese associada;
- fonte;
- formula;
- momento em que fica disponivel;
- target recomendado;
- risco de data leakage.

Proibido:

- usar placar final como preditor;
- usar estatisticas full-match para prever evento apos cutoff;
- usar historico futuro;
- usar target como feature;
- usar features derivadas de graph antes de `match_graph` estar populada;
- usar lineups/h2h como obrigatorias no core v1.

---

## Targets de Referencia

### Target principal

- `target_late_goal_75`

Definicao:

- 1 se existir gol apos 75:00 ate o fim da partida.
- 0 caso contrario.

### Target por cutoff

- `target_goal_after_cutoff_X`

Definicao:

- 1 se existir gol apos o minuto de corte X.
- 0 caso contrario.

Cutoffs recomendados:

- 60
- 65
- 70
- 75
- 80

---

# H1 - xG Pre-Jogo

## Hipotese

Partidas com maior expectativa ofensiva possuem maior probabilidade de gols tardios.

## Features

### `pre_home_xg`

Fonte:

- Understat / `matches_master`, se disponivel como dado pre-jogo.

Formula:

- xG esperado do mandante antes da partida.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_late_goal_75`.

Risco de leakage:

- Alto se o campo representar xG final produzido na partida.
- Baixo apenas se for forecast/previsao pre-jogo.

### `pre_away_xg`

Fonte:

- Understat / `matches_master`, se disponivel como dado pre-jogo.

Formula:

- xG esperado do visitante antes da partida.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_late_goal_75`.

Risco de leakage:

- Alto se representar xG final da partida.

### `pre_total_xg`

Fonte:

- Understat.

Formula:

- `pre_home_xg + pre_away_xg`.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_late_goal_75`.

Risco de leakage:

- Herdado dos campos base.

### `pre_xg_diff_home`

Fonte:

- Understat.

Formula:

- `pre_home_xg - pre_away_xg`.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_home_late_goal_75` e `target_away_late_goal_75`.

Risco de leakage:

- Herdado dos campos base.

---

# H2 - Forecast Pre-Jogo

## Hipotese

Probabilidades pre-jogo ajudam a identificar partidas com maior propensao a gols tardios.

## Features

### `forecast_home_win`

Fonte:

- Understat.

Formula:

- Probabilidade pre-jogo de vitoria do mandante.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_late_goal_75`.

Risco de leakage:

- Baixo, se calculado antes da partida.

### `forecast_draw`

Fonte:

- Understat.

Formula:

- Probabilidade pre-jogo de empate.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_late_goal_75`.

Risco de leakage:

- Baixo.

### `forecast_away_win`

Fonte:

- Understat.

Formula:

- Probabilidade pre-jogo de vitoria do visitante.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_late_goal_75`.

Risco de leakage:

- Baixo.

### `forecast_balance_index`

Fonte:

- Understat.

Formula:

- `1 - max(forecast_home_win, forecast_draw, forecast_away_win)`.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_late_goal_75`.

Risco de leakage:

- Baixo.

---

# H3 - Forca Ofensiva

## Hipotese

Equipes ofensivamente fortes mantem capacidade de gerar chances ate os minutos finais.

## Features

### `home_attack_strength_prior`

Fonte:

- Historico Understat / SofaScore anterior a partida.

Formula:

- Media movel de producao ofensiva do mandante em jogos anteriores.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_home_late_goal_75`.

Risco de leakage:

- Alto se usar jogos futuros ou temporada completa.

### `away_attack_strength_prior`

Fonte:

- Historico Understat / SofaScore anterior a partida.

Formula:

- Media movel de producao ofensiva do visitante em jogos anteriores.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_away_late_goal_75`.

Risco de leakage:

- Alto se usar jogos futuros ou temporada completa.

### `home_late_goal_rate_prior`

Fonte:

- `match_incidents` historico anterior.

Formula:

- proporcao de jogos anteriores do mandante com gol marcado apos 75:00.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_home_late_goal_75`.

Risco de leakage:

- Alto se incluir a propria partida ou partidas futuras.

### `away_late_goal_rate_prior`

Fonte:

- `match_incidents` historico anterior.

Formula:

- proporcao de jogos anteriores do visitante com gol marcado apos 75:00.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_away_late_goal_75`.

Risco de leakage:

- Alto se incluir a propria partida ou partidas futuras.

---

# H4 - Fragilidade Defensiva

## Hipotese

Equipes defensivamente frageis apresentam maior incidencia de gols tardios sofridos.

## Features

### `home_defensive_weakness_prior`

Fonte:

- Historico anterior por time.

Formula:

- media movel de gols/xGA/chances sofridas pelo mandante antes da partida.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- gol tardio do visitante.

Risco de leakage:

- Alto se usar dados futuros.

### `away_defensive_weakness_prior`

Fonte:

- Historico anterior por time.

Formula:

- media movel de gols/xGA/chances sofridas pelo visitante antes da partida.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- gol tardio do mandante.

Risco de leakage:

- Alto se usar dados futuros.

### `home_late_conceded_rate_prior`

Fonte:

- `match_incidents` historico anterior.

Formula:

- proporcao de jogos anteriores em que o mandante sofreu gol apos 75:00.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_away_late_goal_75`.

Risco de leakage:

- Alto se incluir a partida atual ou jogos futuros.

### `away_late_conceded_rate_prior`

Fonte:

- `match_incidents` historico anterior.

Formula:

- proporcao de jogos anteriores em que o visitante sofreu gol apos 75:00.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_home_late_goal_75`.

Risco de leakage:

- Alto se incluir a partida atual ou jogos futuros.

---

# H5 - Pressao Ofensiva In-Game

## Hipotese

Pressao ofensiva acumulada durante a partida aumenta a probabilidade de gol futuro.

## Status V1

Parcial.

Depende de estatisticas temporais confiaveis ate o cutoff.

Se `match_statistics` for full-match, nao pode ser usada como preditor in-game.

## Features Futuras

### `home_shots_until_X`

Fonte:

- snapshots/statistics temporais.

Formula:

- finalizacoes do mandante ate cutoff X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Alto se derivada de estatistica final.

### `away_shots_until_X`

Fonte:

- snapshots/statistics temporais.

Formula:

- finalizacoes do visitante ate cutoff X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Alto se derivada de estatistica final.

### `home_big_chances_until_X`

Fonte:

- snapshots/statistics temporais.

Formula:

- big chances do mandante ate cutoff X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Alto se usar `big_chances_home` full-match.
- Requer regra para nulos.

### `away_big_chances_until_X`

Fonte:

- snapshots/statistics temporais.

Formula:

- big chances do visitante ate cutoff X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Alto se usar `big_chances_away` full-match.
- Requer regra para nulos.

---

# H6 - Estado Atual da Partida

## Hipotese

O placar atual influencia o comportamento tatico e a probabilidade de gols futuros.

## Features

### `home_goals_until_X`

Fonte:

- `match_incidents`.

Formula:

- gols do mandante com minuto menor ou igual ao cutoff X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo se filtrar corretamente por cutoff.

### `away_goals_until_X`

Fonte:

- `match_incidents`.

Formula:

- gols do visitante com minuto menor ou igual ao cutoff X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo se filtrar corretamente por cutoff.

### `score_diff_home_until_X`

Fonte:

- `match_incidents`.

Formula:

- `home_goals_until_X - away_goals_until_X`.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo.

### `is_draw_until_X`

Fonte:

- `match_incidents`.

Formula:

- 1 se `home_goals_until_X = away_goals_until_X`; caso contrario 0.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo.

### `time_since_last_goal_X`

Fonte:

- `match_incidents`.

Formula:

- `X - ultimo_minuto_de_gol_antes_ou_igual_X`.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo se nao usar gols apos X.

---

# H7 - Combinacao Multi-Fonte

## Hipotese

A combinacao de variaveis pre-jogo e in-game produz maior poder preditivo do que qualquer fonte isolada.

## Blocos de Features

### `block_prematch_understat`

Fonte:

- Understat.

Componentes:

- xG pre-jogo.
- forecast.
- historico anterior.

Momento disponivel:

- Pre-jogo.

Target recomendado:

- `target_late_goal_75`.

Risco de leakage:

- Medio, depende da definicao dos campos.

### `block_incidents_until_X`

Fonte:

- `match_incidents`.

Componentes:

- placar ate X.
- cartoes ate X.
- substituicoes ate X.
- gols recentes ate X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo se filtrar por cutoff.

### `block_statistics_until_X`

Fonte:

- snapshots/statistics temporais.

Componentes:

- finalizacoes.
- escanteios.
- big chances.
- ataques perigosos, se disponivel.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Alto se usar estatistica full-match.

---

# H8 - Momentum e Pressao Temporal

## Hipotese

O momentum acumulado nos minutos anteriores ao evento possui capacidade preditiva para gols tardios.

## Status V1

Nao faz parte do core v1.

Depende de `match_graph` populada.

## Features Futuras

### `home_momentum_last_5m_X`

Fonte:

- `match_graph`.

Formula:

- soma ou media do momentum mandante entre X-5 e X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Alto se incluir pontos apos X.

### `away_momentum_last_5m_X`

Fonte:

- `match_graph`.

Formula:

- soma ou media do momentum visitante entre X-5 e X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Alto se incluir pontos apos X.

### `momentum_diff_last_5m_X`

Fonte:

- `match_graph`.

Formula:

- `home_momentum_last_5m_X - away_momentum_last_5m_X`.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Alto se janelas nao forem fechadas corretamente.

### `momentum_acceleration_X`

Fonte:

- `match_graph`.

Formula:

- momentum recente menos momentum da janela anterior.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Alto se usar dados posteriores a X.

---

# H9 - Eventos Alteram Probabilidade Futura

## Hipotese

Eventos recentes modificam a probabilidade futura de ocorrencia de um gol tardio.

## Features

### `red_cards_until_X`

Fonte:

- `match_incidents`.

Formula:

- numero de cartoes vermelhos ate cutoff X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo se filtrar por cutoff.

### `yellow_cards_until_X`

Fonte:

- `match_incidents`.

Formula:

- numero de cartoes amarelos ate cutoff X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo se filtrar por cutoff.

### `subs_until_X`

Fonte:

- `match_incidents`.

Formula:

- numero de substituicoes ate cutoff X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo se filtrar por cutoff.

### `goal_last_5m_X`

Fonte:

- `match_incidents`.

Formula:

- 1 se houve gol entre X-5 e X; caso contrario 0.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo se janela terminar em X.

### `goal_last_10m_X`

Fonte:

- `match_incidents`.

Formula:

- 1 se houve gol entre X-10 e X; caso contrario 0.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo se janela terminar em X.

### `penalty_events_until_X`

Fonte:

- `match_incidents`.

Formula:

- numero de eventos de penalti ate cutoff X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo se filtrar por cutoff.

### `var_events_until_X`

Fonte:

- `match_incidents`.

Formula:

- numero de eventos VAR ate cutoff X.

Momento disponivel:

- minuto X.

Target recomendado:

- `target_goal_after_cutoff_X`.

Risco de leakage:

- Baixo se filtrar por cutoff.

---

## Features Fora do Core V1

- lineups.
- h2h.
- graph/momentum.
- estatisticas full-match como preditores in-game.
- odds.
- mercado ao vivo.

---

## Ordem Recomendada de Validacao

1. Auditar targets.
2. H6 - Estado Atual da Partida.
3. H9 - Eventos Alteram Probabilidade.
4. H1 - xG Pre-Jogo.
5. H2 - Forecast Pre-Jogo.
6. H3 - Forca Ofensiva.
7. H4 - Fragilidade Defensiva.
8. H7 - Combinacao Multi-Fonte.
9. H5 - Pressao Ofensiva In-Game.
10. H8 - Momentum e Pressao Temporal.

---

## Criterio para Avancar

Antes de implementar qualquer feature:

- confirmar fonte real no banco;
- confirmar granularidade temporal;
- confirmar regra de nulos;
- confirmar target associado;
- confirmar ausencia de data leakage;
- obter aprovacao do PM/CTO quando houver impacto estrutural.
