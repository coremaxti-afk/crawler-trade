# UNDERSTAT

## Visão Geral

O Understat é a principal fonte de dados pré-jogo utilizada pelo projeto Late Goal Research.

Seu papel é fornecer métricas históricas e estatísticas avançadas das equipes antes do início das partidas.

---

## Papel no Projeto

Fonte principal para construção das features pré-match.

O Understat fornece:

- Dados históricos das partidas
- Estatísticas avançadas por equipe
- Métricas ofensivas
- Métricas defensivas
- Forecast pré-jogo

---

## Dados Confirmados

### Informações da Partida

- Match ID
- Data
- Liga
- Temporada
- Mandante
- Visitante
- Placar Final

### Métricas de Probabilidade

- Forecast Home Win
- Forecast Draw
- Forecast Away Win

### Métricas Ofensivas

- xG
- Home xG
- Away xG
- Deep

### Métricas Defensivas

- xGA
- PPDA

---

## Tabelas Relacionadas

### matches

Contém informações gerais da partida e probabilidades pré-jogo.

### team_match_stats

Contém estatísticas avançadas por equipe e por partida.

---

## Utilização

O Understat é utilizado principalmente para:

- Construção de features pré-jogo
- Avaliação de força ofensiva
- Avaliação de fragilidade defensiva
- Forecast da partida
- Modelagem preditiva

---

## Limitações

O Understat não fornece:

- Eventos minuto a minuto
- Cartões
- Substituições
- Momentum
- Pressão temporal
- Incidentes da partida

Esses dados são complementados por FotMob e SofaScore.

---

## Status

Fonte operacional e integrada ao projeto.
