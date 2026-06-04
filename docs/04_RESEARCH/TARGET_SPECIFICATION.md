# TARGET SPECIFICATION

## Status

Definicao metodologica formal.

Nao implementado.

Nao contem codigo.

Nao contem SQL.

Nao inicia feature engineering.

Nao inicia modelagem.

---

## Contexto

Este documento formaliza os targets do Dataset Analitico v1 do LateGoalResearch.

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
- lineups e h2h fora do core v1.

Fonte principal para targets:

- `match_incidents`.

---

## Principios Gerais

Todo target deve possuir:

- nome claro;
- definicao objetiva;
- unidade analitica;
- fonte;
- regra temporal;
- regra de inclusao/exclusao;
- relacao com hipoteses H1-H9;
- risco de leakage documentado.

Os targets nao podem ser usados como variaveis explicativas.

---

## Convencoes Temporais

### Minuto base

O minuto do evento deve ser interpretado a partir de `match_incidents`.

### Regra para gol tardio

Para o target principal:

- gol tardio = gol com minuto maior que 75.

Portanto:

- minuto 75 nao conta como gol tardio no target principal;
- minuto 76 em diante conta;
- acrescimos do segundo tempo contam.

### Acrescimos

Gols em acrescimos devem ser incluidos quando o minuto registrado for posterior ao corte.

Exemplos:

- 90+1 conta para target 75, 80 e 85.
- 45+2 nao conta para target 75, 80 ou 85.

---

## Target Principal

### `target_late_goal_75`

Definicao:

- 1 se existir pelo menos um gol apos 75:00 ate o fim da partida.
- 0 caso contrario.

Unidade analitica:

- 1 linha por partida.

Fonte:

- `match_incidents`.

Evento base:

- gol.

Regra temporal:

- considerar gols com minuto maior que 75.

Casos especiais:

- partidas 0x0 recebem 0;
- partidas com gols apenas antes ou no minuto 75 recebem 0;
- partidas com multiplos gols apos 75 recebem 1;
- gol contra conta como gol da partida;
- penaltis convertidos contam como gol;
- penaltis perdidos nao contam como gol;
- gol anulado nao deve contar se estiver identificado como anulado/no goal.

Hipoteses relacionadas:

- H1.
- H2.
- H3.
- H4.
- H7.

Uso recomendado:

- target principal do Dataset Analitico v1A pre-jogo.
- target de referencia para analises match-level.

Risco de leakage:

- alto se o target for usado como feature;
- alto se placar final ou total de gols forem usados como preditores.

---

## Targets Alternativos por Janela

### `target_late_goal_80`

Definicao:

- 1 se existir pelo menos um gol apos 80:00 ate o fim da partida.
- 0 caso contrario.

Unidade analitica:

- 1 linha por partida.

Fonte:

- `match_incidents`.

Uso recomendado:

- analise de robustez temporal.
- comparacao com `target_late_goal_75`.

Risco:

- evento mais raro; pode exigir amostra maior.

### `target_late_goal_85`

Definicao:

- 1 se existir pelo menos um gol apos 85:00 ate o fim da partida.
- 0 caso contrario.

Unidade analitica:

- 1 linha por partida.

Fonte:

- `match_incidents`.

Uso recomendado:

- analise de gols muito tardios.

Risco:

- maior raridade do evento;
- maior instabilidade estatistica em amostras pequenas.

---

## Targets Direcionais por Time

### `target_home_late_goal_75`

Definicao:

- 1 se o mandante marcar pelo menos um gol apos 75:00.
- 0 caso contrario.

Unidade analitica:

- 1 linha por partida.

Fonte:

- `match_incidents`.

Uso recomendado:

- H3 Forca Ofensiva.
- H4 Fragilidade Defensiva do visitante.

Risco:

- exige atribuicao correta do beneficiario do gol, especialmente em gol contra.

### `target_away_late_goal_75`

Definicao:

- 1 se o visitante marcar pelo menos um gol apos 75:00.
- 0 caso contrario.

Unidade analitica:

- 1 linha por partida.

Fonte:

- `match_incidents`.

Uso recomendado:

- H3 Forca Ofensiva.
- H4 Fragilidade Defensiva do mandante.

Risco:

- exige atribuicao correta do beneficiario do gol, especialmente em gol contra.

---

## Targets por Cutoff In-Game

### `target_goal_after_cutoff_X`

Definicao:

- 1 se existir pelo menos um gol apos o minuto de corte X.
- 0 caso contrario.

Unidade analitica:

- 1 linha por partida por cutoff.

Cutoffs padrao:

- 60.
- 65.
- 70.
- 75.
- 80.

Fonte:

- `match_incidents`.

Regra temporal:

- considerar apenas gols com minuto maior que X.

Uso recomendado:

- Dataset Analitico v1B.
- H5.
- H6.
- H7.
- H8.
- H9.

Regra anti-leakage:

- features da linha com cutoff X so podem usar informacao disponivel ate X.

Exemplo conceitual:

- Linha `match_id = A`, `cutoff = 70`.
- Features: eventos ate 70.
- Target: gol depois de 70.

Risco:

- alto se qualquer evento apos X entrar nas features.

---

## Target de Proximo Gol

### `target_next_goal_after_X`

Definicao:

- 1 se existir proximo gol apos o cutoff X.
- 0 se nao houver mais gols apos X.

Unidade analitica:

- 1 linha por partida por cutoff.

Fonte:

- `match_incidents`.

Uso recomendado:

- etapa futura.
- nao prioritario no Dataset v1.

Risco:

- exige cuidado com partidas encerradas sem novo gol.

### `target_next_goal_team_after_X`

Definicao:

- `home` se o proximo gol apos X for do mandante.
- `away` se o proximo gol apos X for do visitante.
- `none` se nao houver gol apos X.

Uso recomendado:

- etapa futura multiclasses.

Nao recomendado para v1:

- aumenta complexidade antes da validacao binaria.

---

## Targets Equivalentes a Over

### `target_over_0_5_75_ft`

Definicao:

- 1 se existir pelo menos um gol entre 75:01 e o fim.
- 0 caso contrario.

Equivalencia:

- equivalente operacional a `target_late_goal_75`.

Uso recomendado:

- nomenclatura alternativa para analise futura orientada a mercado.

### `target_over_0_5_80_ft`

Definicao:

- 1 se existir pelo menos um gol entre 80:01 e o fim.
- 0 caso contrario.

Equivalencia:

- equivalente operacional a `target_late_goal_80`.

Uso recomendado:

- analise futura orientada a mercado.

---

## Targets Fora do Escopo v1

Nao fazem parte do core v1:

- targets baseados em odds;
- targets de valor esperado financeiro;
- targets live market;
- targets com graph/momentum obrigatorio;
- targets dependentes de lineups;
- targets dependentes de h2h;
- targets multiclasses como primeira etapa.

---

## Matriz Target x Hipotese

| Hipotese | Target principal recomendado | Observacao |
|---|---|---|
| H1 xG Pre-Jogo | `target_late_goal_75` | match-level |
| H2 Forecast Pre-Jogo | `target_late_goal_75` | match-level |
| H3 Forca Ofensiva | `target_home_late_goal_75`, `target_away_late_goal_75` | direcional |
| H4 Fragilidade Defensiva | gol tardio sofrido por lado | direcional |
| H5 Pressao In-Game | `target_goal_after_cutoff_X` | depende de estatistica temporal |
| H6 Estado Atual | `target_goal_after_cutoff_X` | validavel com incidents |
| H7 Multi-Fonte | `target_late_goal_75`, `target_goal_after_cutoff_X` | comparacao de blocos |
| H8 Momentum | `target_goal_after_cutoff_X` | depende de graph |
| H9 Eventos | `target_goal_after_cutoff_X` | validavel com incidents |

---

## Auditoria Obrigatoria dos Targets

Antes de qualquer implementacao ou modelagem, auditar manualmente amostras contendo:

- partidas 0x0;
- partidas com gol exatamente no minuto 75;
- partidas com gol apos 75;
- partidas com gol apos 80;
- partidas com gol apos 85;
- partidas com gol em acrescimos;
- partidas com multiplos gols tardios;
- partidas com penalti convertido;
- partidas com gol contra;
- partidas com gol anulado, se houver.

Criterio de aceite:

- target calculado deve bater com leitura manual dos incidentes.

---

## Decisao Metodologica

O target principal do Dataset Analitico v1 e:

- `target_late_goal_75`.

O target principal para linhas in-game e:

- `target_goal_after_cutoff_X`.

A fase atual encerra a especificacao metodologica dos targets.

Nao executar nesta etapa:

- codigo;
- SQL;
- feature engineering;
- modelagem;
- backtesting.
