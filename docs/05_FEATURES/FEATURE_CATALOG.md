# FEATURE CATALOG

## Objetivo

Catálogo oficial de features utilizadas no projeto Late Goal Research.

As features estão divididas por estágio de disponibilidade:

- Prematch
- In Play
- Temporal
- Event Driven
- Multi-Source

---

# PREMATCH FEATURES

## Forecast

- forecast_home_win
- forecast_draw
- forecast_away_win

Fonte:
- Understat

---

## Team Strength

- home_xg
- away_xg
- total_xg
- home_xga
- away_xga

Fonte:
- Understat

---

## Advanced Team Metrics

- PPDA
- Deep

Fonte:
- Understat

---

# IN-PLAY FEATURES

## Match Statistics

- possession_home
- possession_away

- shots_home
- shots_away

- shots_on_target_home
- shots_on_target_away

- corners_home
- corners_away

- big_chances_home
- big_chances_away

Fonte:
- SofaScore
- FotMob

---

# TEMPORAL FEATURES

## Momentum

- momentum_last_5m
- momentum_last_10m
- momentum_last_15m

Fonte:
- match_graph

---

## Pressure Trend

- pressure_slope
- pressure_acceleration

Fonte:
- match_graph

---

## Momentum Extremes

- momentum_max
- momentum_min
- momentum_avg

Fonte:
- match_graph

---

# EVENT DRIVEN FEATURES

## Cards

- yellow_cards_home
- yellow_cards_away

- red_cards_home
- red_cards_away

Fonte:
- match_incidents

---

## Goals

- goals_last_5m
- goals_last_10m

Fonte:
- match_incidents

---

## Substitutions

- substitutions_home
- substitutions_away

- offensive_substitutions
- defensive_substitutions

Fonte:
- match_incidents

---

# GAME STATE FEATURES

## Current Score

- home_goals
- away_goals

- goal_difference

Fonte:
- matches_master

---

## Match State

- draw_state
- home_winning
- away_winning

Fonte:
- matches_master

---

# MULTI-SOURCE FEATURES

## Composite Features

- pressure_xg_ratio
- momentum_xg_ratio
- attack_efficiency
- pressure_conversion_rate

Status:
Planejado

---

# HIGH PRIORITY FEATURES

As features abaixo possuem maior potencial preditivo:

1. momentum_last_10m
2. pressure_slope
3. red_cards
4. goal_difference
5. pressure_conversion_rate
6. attack_efficiency
7. forecast_home_win

---

# STATUS

Catálogo em expansão contínua.
