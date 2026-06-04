# MATCHES SCHEMA

## Tabela

matches

---

## Objetivo

Armazenar informações gerais das partidas importadas do Understat.

---

## Campos Principais

### Identificação

- match_id
- league
- season
- date

---

### Equipes

- home_team
- away_team

---

### Resultado

- home_goals
- away_goals

---

### Forecast

- forecast_home
- forecast_draw
- forecast_away

---

### Métricas xG

- home_xg
- away_xg

---

## Utilização

Esta tabela é utilizada para:

- Features pré-jogo
- Forecast
- Análise histórica
- Integração entre fontes

---

## Dependências

Relacionada com:

- team_match_stats
- match_mapping
- matches_master

---

## Status

Ativa.
