# ANALYTICAL DATASET V1

## Status

Definido metodologicamente, implementado e gerado.

Status do dataset gerado:

- APTO COM RESSALVAS.

Documento operacional complementar:

- `docs/04_RESEARCH/DATASET_BUILDER_V1.md`

Script:

- `LateGoalResearch/Analytics/DatasetBuilder/dataset_builder_v1.py`

Commit de implementacao:

- `1a1404e09079f2a1a7958ae948fefdc667872a50` - Cria Dataset Builder V1.

---

## Contexto

A fase de coleta, auditoria, importacao PostgreSQL e validacao leve de qualidade foi concluida.

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

## Dataset Gerado

Arquivos locais gerados em `data/processed/datasets/`:

- `late_goal_dataset_v1.csv`
- `late_goal_dataset_v1.parquet`
- `late_goal_dataset_v1_metadata.json`
- `late_goal_dataset_v1_validation_report.json`

Resumo validado:

- linhas: 380.
- grain: 1 linha por partida.
- duplicatas por `match_id`: 0.
- duplicatas por `sofascore_event_id`: 0.
- status: APTO COM RESSALVAS.

---

## 1. Target Principal

Nome:

- `target_late_goal_75`

Alias operacional:

- `has_late_goal`

Definicao:

- 1 se existir pelo menos um gol apos 75:00 ate o fim da partida.
- 0 caso contrario.

Fonte:

- `match_incidents`.

Unidade inicial:

- 1 linha por partida.

Regra temporal:

- gols com minuto maior que 75 contam como gol tardio.
- acrescimos do segundo tempo contam conforme minuto registrado em `match_incidents`.

Distribuicao gerada:

- positivos: 189.
- negativos: 191.
- taxa positiva: 0.497368.

---

## 2. Targets Alternativos

Ainda nao implementados no Dataset Builder V1:

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

### V1A - Match-Level

Grain:

- 1 linha por partida.

Target:

- `target_late_goal_75`.

Uso permitido nesta etapa:

- auditoria de target;
- analise descritiva;
- preparacao metodologica para H1/H2/H6/H9.

Nao permitido nesta etapa:

- modelagem;
- backtesting;
- feature engineering avancada H1-H9.

### V1B - In-Game por Cutoff

Status:

- Nao implementado.

Grain futuro:

- 1 linha por partida por cutoff.

Cutoffs recomendados:

- 60
- 65
- 70
- 75
- 80

Target futuro:

- `target_goal_after_cutoff_X`.

---

## 4. Colunas Disponiveis no V1

Fontes:

- `matches_master`.
- `match_statistics`.
- `match_incidents`.

Blocos incluidos:

- identificadores de partida;
- data/temporada/liga;
- times mandante e visitante;
- placar final para auditoria;
- estatisticas full-match;
- agregados simples de incidentes;
- target de gol tardio apos 75.

Observacao importante:

- Estatisticas full-match de `match_statistics` nao devem ser usadas como preditores in-game se contiverem eventos posteriores ao cutoff.
- `big_chances_home` e `big_chances_away` possuem nulos e devem ser tratadas como features opcionais, nao obrigatorias.

---

## 5. Colunas Target-Derived Proibidas como Features

As colunas abaixo sao derivadas diretamente do target ou de eventos de gol futuros. Elas nao podem ser usadas como features preditivas:

- `has_late_goal`
- `target_late_goal_75`
- `late_goal_count_75`
- `home_late_goal_count_75`
- `away_late_goal_count_75`
- `first_late_goal_minute_75`

Uso permitido:

- auditoria;
- validacao do target;
- analise descritiva do alvo;
- rotulagem.

---

## 6. Ressalvas de Data Leakage

Toda feature deve informar:

- fonte;
- formula;
- momento em que fica disponivel;
- janela temporal;
- risco de leakage.

Proibido:

- usar target como feature;
- usar colunas target-derived como preditores;
- usar placar final como preditor;
- usar total de gols final como preditor;
- usar estatisticas full-match como preditores in-game por cutoff;
- usar historico futuro;
- usar split aleatorio como validacao principal.

Colunas de placar final presentes no V1 sao somente para auditoria e nao devem entrar como preditores:

- `home_goals`
- `away_goals`
- `total_goals`

---

## 7. Features que Dependem de Graph / Momentum

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

## 8. Features que Dependem de Lineups

Nao fazem parte do core v1.

Motivo:

- a base core nao possui lineups para todas as partidas.

---

## 9. Features que Dependem de H2H

Nao fazem parte do core v1.

Regra obrigatoria futura:

- usar apenas confrontos anteriores a data da partida analisada.

---

## 10. Estrategia de Validacao H1-H9

### H1 - xG Pre-Jogo

Target recomendado:

- `target_late_goal_75`.

Validacao:

- taxa de gol tardio por faixas/quartis de xG, apos revisao de leakage.

### H2 - Forecast Pre-Jogo

Target recomendado:

- `target_late_goal_75`.

Validacao:

- taxa de gol tardio por faixas de probabilidades pre-jogo.

### H3 - Forca Ofensiva

Status:

- nao implementar features historicas ainda.

### H4 - Fragilidade Defensiva

Status:

- nao implementar features historicas ainda.

### H5 - Pressao Ofensiva In-Game

Status:

- depende de granularidade temporal confiavel das estatisticas.

### H6 - Estado Atual da Partida

Status:

- validavel futuramente com dataset por cutoff baseado em `match_incidents`.

### H7 - Combinacao Multi-Fonte

Status:

- parcialmente validavel em etapa futura.

### H8 - Momentum e Pressao Temporal

Status:

- depende de graph/momentum.

### H9 - Eventos Alteram Probabilidade

Status:

- validavel parcialmente com `match_incidents`, em dataset por cutoff futuro.

---

## 11. Ordem Recomendada de Testes

1. Auditoria do target.
2. Classificacao de colunas por risco de leakage.
3. H6 - Estado Atual da Partida.
4. H9 - Eventos Alteram Probabilidade.
5. H1 - xG Pre-Jogo.
6. H2 - Forecast Pre-Jogo.
7. H3 - Forca Ofensiva.
8. H4 - Fragilidade Defensiva.
9. H7 - Combinacao Multi-Fonte.
10. H5 - Pressao Ofensiva In-Game.
11. H8 - Momentum e Pressao Temporal.

---

## Decisao Metodologica Atual

O Dataset Analitico V1 foi gerado e esta apto com ressalvas para auditoria pelo Quant Research / Data Science.

Nao iniciar ainda:

- modelagem;
- backtesting;
- feature engineering avancada;
- alteracao de schema;
- coleta adicional.
