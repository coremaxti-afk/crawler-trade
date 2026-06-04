# ANALYTICAL DATASET V1

## Status

Definido metodologicamente.

Nao implementado.

Marco PM:

> Como PM, considero esta a primeira definicao metodologica formal do LateGoalResearch. A partir daqui, Quant Research pode comecar o desenho do Dataset Analitico v1 com uma base consistente e auditavel.

---

## Contexto

A fase de coleta, auditoria, importacao PostgreSQL e validacao leve de qualidade foi concluida.

Status da base:

- APTO COM RESSALVAS.

Base disponivel:

- `matches_master`: 380 partidas.
- `match_statistics`: 380 partidas.
- `match_incidents`: 7647 registros.

Qualidade observada:

- Nao existem orfaos.
- Nao existem divergencias entre placar e incidentes.
- 16 partidas sem gols sao compativeis com o placar.
- `big_chances_home` possui 7 nulos.
- `big_chances_away` possui 7 nulos.

---

## 1. Target Principal

Nome:

- `target_late_goal_75`

Definicao:

- 1 se existir pelo menos um gol apos 75:00 ate o fim da partida.
- 0 caso contrario.

Fonte:

- `match_incidents`.

Unidade inicial:

- 1 linha por partida.

Regra temporal:

- gols com minuto maior que 75 contam como gol tardio.
- acrescimos do segundo tempo contam.

---

## 2. Targets Alternativos

- `target_late_goal_80`
- `target_late_goal_85`
- `target_home_late_goal_75`
- `target_away_late_goal_75`
- `target_goal_after_cutoff_X`
- `target_next_goal_after_X`
- `target_over_0_5_75_ft`
- `target_over_0_5_80_ft`

---

## 3. Horizonte Temporal

### V1A - Pre-Jogo

Grain:

- 1 linha por partida.

Target:

- `target_late_goal_75`.

Uso:

- H1.
- H2.
- H3.
- H4.
- parte de H7.

### V1B - In-Game por Cutoff

Grain:

- 1 linha por partida por cutoff.

Cutoffs recomendados:

- 60
- 65
- 70
- 75
- 80

Target:

- `target_goal_after_cutoff_X`.

Uso:

- H5.
- H6.
- H7.
- H8.
- H9.

---

## 4. Features Disponiveis Imediatamente

Fontes:

- `matches_master`.
- `match_statistics`.
- `match_incidents`.

Disponiveis para desenho imediato:

- identificadores de partida;
- data/temporada/liga;
- times mandante e visitante;
- gols por minuto via incidentes;
- placar ate cutoff;
- estado do jogo ate cutoff;
- cartoes ate cutoff;
- substituicoes ate cutoff;
- penaltis ate cutoff, se incident type permitir;
- VAR ate cutoff, se incident type permitir;
- tempo desde o ultimo gol;
- gols recentes antes do cutoff.

Observacao importante:

- Estatisticas full-match de `match_statistics` nao devem ser usadas como preditores in-game se contiverem eventos posteriores ao cutoff.
- `big_chances_home` e `big_chances_away` possuem nulos e devem ser tratadas como features opcionais, nao obrigatorias.

---

## 5. Features que Dependem de Graph / Momentum

Nao fazem parte do core v1.

Dependem de:

- `match_graph` populada.
- `graph.json` ou endpoint equivalente.

Exemplos futuros:

- `momentum_last_5m_X`.
- `momentum_last_10m_X`.
- `momentum_acceleration_X`.
- `sustained_pressure_X`.
- `pressure_flip_X`.

Hipotese principal:

- H8.

---

## 6. Features que Dependem de Lineups

Nao fazem parte do core v1.

Motivo:

- a base core nao possui lineups para todas as partidas.

Exemplos futuros:

- forca do XI inicial;
- qualidade do banco;
- substituicoes ofensivas;
- substituicoes defensivas;
- mudanca de formacao.

---

## 7. Features que Dependem de H2H

Nao fazem parte do core v1.

Prioridade:

- baixa.

Uso futuro:

- bloco exploratorio opcional.

Regra obrigatoria:

- usar apenas confrontos anteriores a data da partida analisada.

---

## 8. Estrategia de Validacao H1-H9

### H1 - xG Pre-Jogo

Target recomendado:

- `target_late_goal_75`.

Validacao:

- taxa de gol tardio por faixas/quartis de xG.

### H2 - Forecast Pre-Jogo

Target recomendado:

- `target_late_goal_75`.

Validacao:

- taxa de gol tardio por faixas de probabilidades pre-jogo.

### H3 - Forca Ofensiva

Targets recomendados:

- `target_home_late_goal_75`.
- `target_away_late_goal_75`.

Validacao:

- medias historicas anteriores por time.

### H4 - Fragilidade Defensiva

Targets recomendados:

- gol tardio sofrido por mandante/visitante.

Validacao:

- fragilidade defensiva historica anterior por time.

### H5 - Pressao Ofensiva In-Game

Target recomendado:

- `target_goal_after_cutoff_X`.

Status:

- depende de granularidade temporal confiavel das estatisticas.

### H6 - Estado Atual da Partida

Target recomendado:

- `target_goal_after_cutoff_X`.

Status:

- validavel imediatamente com `match_incidents`.

### H7 - Combinacao Multi-Fonte

Target recomendado:

- `target_late_goal_75` e `target_goal_after_cutoff_X`.

Status:

- parcialmente validavel com pre-jogo + incidents.

### H8 - Momentum e Pressao Temporal

Target recomendado:

- `target_goal_after_cutoff_X`.

Status:

- depende de graph/momentum.

### H9 - Eventos Alteram Probabilidade

Target recomendado:

- `target_goal_after_cutoff_X`.

Status:

- validavel parcialmente com `match_incidents`.

---

## 9. Ordem Recomendada de Testes

1. Auditoria do target.
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

## Regras de Data Leakage

Toda feature deve informar:

- fonte;
- formula;
- momento em que fica disponivel;
- janela temporal;
- risco de leakage.

Proibido:

- usar placar final como preditor;
- usar total de gols final como preditor;
- usar estatisticas produzidas apos o cutoff;
- usar historico futuro;
- usar target como feature;
- usar split aleatorio como validacao principal.

---

## Decisao Metodologica

O Dataset Analitico v1 sera desenhado em duas camadas:

- V1A: match-level pre-jogo.
- V1B: match-cutoff in-game baseado em incidentes.

Nao criar nesta etapa:

- codigo;
- modelo;
- feature engineering executavel;
- alteracao de schema;
- coleta adicional.
