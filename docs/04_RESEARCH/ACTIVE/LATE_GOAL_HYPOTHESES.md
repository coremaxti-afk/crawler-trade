# LATE_GOAL_HYPOTHESES

## Objetivo

Registrar formalmente as hipóteses de pesquisa do projeto Late Goal Research.

Cada hipótese deverá passar por:

1. Definição conceitual
2. Construção de features
3. Teste quantitativo
4. Validação estatística
5. Decisão:
   - COMPLETED
   - ABANDONED

---

# H1 — xG Pré-Jogo

## Hipótese

Partidas com maior expectativa ofensiva possuem maior probabilidade de gols tardios.

## Variáveis

- home_xg
- away_xg
- total_xg

## Fonte

- Understat

## Status

Em pesquisa.

---

# H2 — Forecast Pré-Jogo

## Hipótese

Probabilidades pré-jogo ajudam a identificar partidas com maior propensão a gols tardios.

## Variáveis

- forecast_home_win
- forecast_draw
- forecast_away_win

## Fonte

- Understat

## Status

Em pesquisa.

---

# H3 — Força Ofensiva

## Hipótese

Equipes ofensivamente fortes mantêm capacidade de gerar chances até os minutos finais.

## Variáveis

- xG
- Deep
- PPDA

## Fonte

- Understat

## Status

Em pesquisa.

---

# H4 — Fragilidade Defensiva

## Hipótese

Equipes defensivamente frágeis apresentam maior incidência de gols tardios sofridos.

## Variáveis

- xGA
- PPDA

## Fonte

- Understat

## Status

Em pesquisa.

---

# H5 — Pressão Ofensiva In-Game

## Hipótese

Pressão ofensiva acumulada durante a partida aumenta a probabilidade de um gol tardio.

## Variáveis

- ataques
- finalizações
- finalizações no alvo
- escanteios

## Fonte

- FotMob
- Snapshots

## Status

Em pesquisa.

---

# H6 — Estado Atual da Partida

## Hipótese

O placar atual influencia o comportamento tático e a probabilidade de gols futuros.

## Exemplos

- 0x0
- 1x0
- 1x1
- 2x1

## Fonte

- Results
- Snapshots

## Status

Em pesquisa.

---

# H7 — Combinação Multi-Fonte

## Hipótese

A combinação de variáveis pré-jogo e in-game produz maior poder preditivo do que qualquer fonte isolada.

## Fontes

- Understat
- FotMob
- SofaScore

## Status

Alta prioridade.

---

# H8 — Momentum e Pressão Temporal

## Hipótese

O momentum acumulado nos minutos anteriores ao evento possui capacidade preditiva para gols tardios.

## Variáveis

- match_graph
- ataques consecutivos
- dominância territorial
- aceleração da pressão
- momentum acumulado

## Fonte

- SofaScore
match_graph (coleta pendente)

## Status

Alta prioridade.
Parcialmente validável

## Justificativa

Esta hipótese só se tornou possível após a descoberta dos dados de Graph do SofaScore.

## OBSERVAÇÃO

A arquitetura já suporta armazenamento temporal para validação futura.

---

# H9 — Eventos Alteram a Probabilidade Futura

## Hipótese

Eventos recentes modificam a probabilidade futura de ocorrência de um gol tardio.

## Exemplos

- cartão vermelho
- gol recente
- substituição ofensiva
- substituição defensiva
- pênalti perdido
- pênalti convertido

## Eventos disponíveis

- Goal
- Card
- Substitution
- Penalty
- VAR

## Fonte

- match_incidents
- FotMob Events

## Status

Alta prioridade.
Parcialmente validável

## Justificativa

Eventos mudam o contexto da partida e podem alterar drasticamente o comportamento das equipes.

---

# Hipóteses Priorizadas

As hipóteses abaixo representam atualmente o maior potencial de ganho preditivo:

1. H7 — Combinação Multi-Fonte
2. H8 — Momentum e Pressão Temporal
3. H9 — Eventos Alteram a Probabilidade Futura

---

# Hipóteses Futuras

Estas hipóteses ainda não estão em desenvolvimento.

## H10 — Big Chances

Investigar impacto de Big Chances na probabilidade de gol tardio.

## H11 — Pressão Pós-Gol

Investigar comportamento ofensivo após gols marcados.

## H12 — Cartão Vermelho

Investigar impacto isolado de expulsões.

## H13 — Sequência de Escanteios

Investigar pressão ofensiva através de escanteios consecutivos.

## H14 — Dominância Territorial

Investigar períodos prolongados de controle ofensivo.

---

# Critério de Evolução

ACTIVE → COMPLETED

Quando a hipótese apresentar evidência estatística consistente.

ACTIVE → ABANDONED

Quando a hipótese não apresentar valor preditivo relevante.

---

Última atualização:
Junho/2026
