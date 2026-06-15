# STRATEGY_NAMING_AND_DEFINITIONS_REFERENCE_V1

## Status

Decisao: **APROVADO COM RESSALVAS PARA REFERENCIA DE NOMENCLATURA E REPRODUTIBILIDADE**

Objetivo: documentar as nomenclaturas usadas no discovery SportMonks team-side para que qualquer estrategia possa ser auditada e reproduzida em outra liga/temporada sem depender de memoria operacional.

## Fontes Consultadas

- DEFINIDO NO CODIGO: `Crawler/Sportmonks/sportmonks_team_side_strategy_discovery_v2.py`
- DEFINIDO NO CODIGO: `Crawler/Sportmonks/sportmonks_team_side_strategy_discovery_v2 editado.py`
- DEFINIDO NA DOCUMENTACAO: `docs/04_RESEARCH/SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V1.md`
- DEFINIDO NA DOCUMENTACAO: `docs/04_RESEARCH/SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V2.md`
- DEFINIDO NA CONFIG: `configs/strategy_drawdown_config_v1.json`

## Base Tecnica Comum

### Fonte de H8

DEFINIDO NO CODIGO: os deltas de H8 saem de `SportMonks trends`, carregados de:

```text
02_fixtures/<fixture_id>/07_h8_pressure/trends.json
```

A timeline e preservada apenas para auditoria estrutural no script V2; os deltas quantitativos das estrategias usam `trends`.

### Indicadores permitidos

DEFINIDO NO CODIGO em `INDICATORS`:

```text
Attacks
Dangerous Attacks
Shots Total
Shots On Target
Shots Off Target
Corners
Key Passes
Big Chances Created
Big Chances Missed
```

Nas colunas do CSV, esses nomes viram snake_case:

```text
attacks
dangerous_attacks
shots_total
shots_on_target
shots_off_target
corners
key_passes
big_chances_created
big_chances_missed
```

### Cutoffs e janelas

DEFINIDO NO CODIGO:

```text
CUTOFFS = 60, 65, 70, 75
WINDOWS = last_5m, last_10m, last_15m
```

A janela e calculada como delta acumulado:

```text
valor_no_cutoff - valor_no_inicio_da_janela
```

Exemplo para cutoff 65 e last_10m:

```text
valor ate minuto 65 - valor ate minuto 55
```

### Targets originais V2

DEFINIDO NO CODIGO em `TARGETS_UNDER` e `TARGETS_OVER` no script V2 original:

```text
TARGETS_UNDER = (60,80), (60,90), (65,80), (65,90), (70,85), (70,90), (75,90)
TARGETS_OVER = (60,70), (60,75), (65,75), (65,80), (70,80), (70,85), (75,85), (75,90)
```

No script editado pelo usuario existem targets adicionais. Esta referencia documenta as regras das estrategias; a lista exata de targets deve ser conferida no script executado.

### Regra de target

DEFINIDO NO CODIGO:

```text
Under Hold => target no_goal_inicio_fim
Over Janela Curta => target goal_inicio_fim
```

A funcao `goals_between` usa:

```text
start < goal.minute <= end
```

Observacao: minuto 90 nao garante acrescimos se a fonte registrar 90+ ou 91+ como minuto acima de 90.

### Regra de favorito

DEFINIDO NO CODIGO em `load_football_data`:

```text
favorite_side = menor odd pre-jogo entre AvgH e AvgA
Draw nunca define favorito
AvgH < AvgA => favorite_side = home
AvgA < AvgH => favorite_side = away
AvgH == AvgA => favorite_side = tie_home_away
```

Fonte das odds:

```text
Football-Data AvgH, AvgD, AvgA
```

### Regra de placar

DEFINIDO NO CODIGO:

```text
score_diff = gols_do_time_analisado_no_cutoff - gols_do_adversario_no_cutoff
```

Logo:

```text
score_diff == 1  => time analisado vencendo por 1
score_diff == -1 => time analisado perdendo por 1
score_diff < 0   => time analisado perdendo por qualquer margem
score_diff == 0  => empatado para o time analisado
score_diff > 0   => time analisado vencendo por qualquer margem
```

### Colunas principais do CSV

DEFINIDO NO CODIGO / CSV:

```text
strategy_id
strategy_name
family
target
hit
fixture_id
fixture_name
cutoff
window
period_id
team_side
participant_id
opponent_participant_id
team_name
opponent_name
team_score_cutoff
opponent_score_cutoff
score_diff
favorite_side
favorite_odd
home_odd
draw_odd
away_odd
odds_gap
team_attacks
opp_attacks
team_dangerous_attacks
opp_dangerous_attacks
team_shots_total
opp_shots_total
team_shots_on_target
opp_shots_on_target
team_shots_off_target
opp_shots_off_target
team_corners
opp_corners
team_key_passes
opp_key_passes
team_big_chances_created
opp_big_chances_created
team_big_chances_missed
opp_big_chances_missed
```

## Componentes Obrigatorios

### favorite

DEFINIDO NO CODIGO. Time favorito pre-jogo pelo menor preco entre `AvgH` e `AvgA` do Football-Data. O empate (`AvgD`) nao pode ser favorito.

Colunas relacionadas: `favorite_side`, `favorite_odd`, `home_odd`, `away_odd`, `odds_gap`, `is_favorite_side`.

### underdog

DEFINIDO NO CODIGO. Time analisado e underdog quando existe `favorite_side` home/away e o `team_side` e o lado oposto.

Colunas relacionadas: `is_underdog_side`, `favorite_side`, `team_side`.

### home

DEFINIDO NO CODIGO. Lado mandante da fixture SportMonks, vindo de `participants.meta.location == home`.

Colunas relacionadas: `team_side = home`, `home_odd`, `team_name`.

### away

DEFINIDO NO CODIGO. Lado visitante da fixture SportMonks, vindo de `participants.meta.location == away`.

Colunas relacionadas: `team_side = away`, `away_odd`, `team_name`.

### team

DEFINIDO NO CODIGO. Linha do participante analisado. Cada fixture gera linha para mandante e visitante em cada cutoff/janela.

Colunas relacionadas: prefixo `team_*`, `team_side`, `team_name`, `participant_id`.

### opp

DEFINIDO NO CODIGO. Adversario do participante analisado na mesma linha.

Colunas relacionadas: prefixo `opp_*`, `opponent_name`, `opponent_participant_id`.

### drawing

DEFINIDO NO CODIGO. Para estrategias de favorito, significa `favorite_drawing == True`, isto e, o time favorito e o lado analisado e `score_diff == 0` no cutoff.

### winning_by_1

DEFINIDO NO CODIGO. Time analisado vencendo por exatamente 1 gol no cutoff: `score_diff == 1`.

### losing

DEFINIDO NO CODIGO. Time analisado perdendo no cutoff: `score_diff < 0`. Nao e restrito a perder por 1, salvo quando a estrategia usa explicitamente `score_diff == -1`.

### cold

INFERIDO PELO NOME, CONFIRMADO PELO CODIGO NOS COMBOS `cold_2of3`. Frio significa baixa atividade em metricas selecionadas contra percentil 25 (`<= p25`) ou zero evento, dependendo da estrategia.

### cold_2of3

DEFINIDO NO CODIGO quando aplicado ao adversario em `opp_cold_2of3`: pelo menos 2 de 3 metricas abaixo/iguais ao p25.

Metricas usadas em `opp_cold_2of3`:

```text
opp_shots_total_{window}m <= p25
opp_dangerous_attacks_{window}m <= p25
opp_key_passes_{window}m <= p25
```

### opp_cold_2of3

DEFINIDO NO CODIGO. O adversario do time analisado esta frio em 2 de 3 metricas: `shots_total`, `dangerous_attacks`, `key_passes`, todas com threshold `<= p25` por cutoff/janela.

### pressure_high

DEFINIDO NO CODIGO nos combos `pressure_high_2of3`. Pressao alta significa metricas do time analisado acima/iguais ao p75.

### pressure_high_2of3

DEFINIDO NO CODIGO. Pelo menos 2 de 3 metricas do time analisado em alta:

```text
team_dangerous_attacks_{window}m >= p75
team_shots_total_{window}m >= p75
team_key_passes_{window}m >= p75
```

### pressing

DEFINIDO NO CODIGO para `home_winning_by_1_visitor_pressing` e `away_winning_by_1_home_pressing`. Pressing nesse caso e uma regra OR, nao 2of3:

```text
team_dangerous_attacks_{window}m >= p75 OR team_shots_on_target_{window}m >= 1
```

### home_pressing

DEFINIDO NO CODIGO em `away_winning_by_1_home_pressing`. A linha analisada deve ser o mandante (`team_side == home`) e deve estar perdendo por 1 (`score_diff == -1`), pressionando por dangerous attacks p75 ou ao menos 1 chute no alvo.

### visitor_pressing

DEFINIDO NO CODIGO em `home_winning_by_1_visitor_pressing`. A linha analisada deve ser o visitante (`team_side == away`) e deve estar perdendo por 1 (`score_diff == -1`), pressionando por dangerous attacks p75 ou ao menos 1 chute no alvo.

### big_chances_recent

DEFINIDO NO CODIGO. Time analisado criou ao menos uma grande chance na janela:

```text
team_big_chances_created_{window}m >= 1
```

### key_passes_recent_high

DEFINIDO NO CODIGO. Time analisado tem key passes na janela acima/iguais ao p75:

```text
team_key_passes_{window}m >= p75
```

### opponent_no_recent_key_passes

DEFINIDO NO CODIGO. Time analisado vencendo por 1 e adversario sem key passes recentes:

```text
score_diff == 1
opp_key_passes_{window}m == 0
```

### both_teams_cold_2of3

DEFINIDO NO CODIGO. Apesar do nome dizer 2of3, a implementacao V2 exige pelo menos 3 de 4 condicoes frias entre os dois times:

```text
team_shots_total_{window}m <= p25
opp_shots_total_{window}m <= p25
team_dangerous_attacks_{window}m <= p25
opp_dangerous_attacks_{window}m <= p25
```

Observacao importante: ha divergencia semantica entre o nome `2of3` e a regra implementada `>= 3 de 4`. Para reproducibilidade, siga o codigo.

## Estrategias Obrigatorias

### favorite_drawing_pressure_high_2of3

1. Nome: `favorite_drawing_pressure_high_2of3`

2. Decomposicao:

```text
favorite = time favorito pre-jogo
drawing = favorito empatando no cutoff
pressure_high_2of3 = pressao alta em 2 de 3 metricas
```

3. Regra de favorito: menor odd pre-jogo 1X2 entre `AvgH` e `AvgA`; draw nao define favorito.

4. Regra de placar: empatado no cutoff (`score_diff == 0`) para o lado favorito.

5. Lado analisado: favorito pre-jogo (`is_favorite_side == True`).

6. Metricas usadas:

```text
team_dangerous_attacks_{window}m
team_shots_total_{window}m
team_key_passes_{window}m
```

7. Thresholds: pelo menos 2 de 3 metricas `>= p75` por cutoff/janela.

8. Janela temporal: `last_5m`, `last_10m`, `last_15m` conforme iteracao do script.

9. Colunas do CSV: `strategy_name`, `family`, `cutoff`, `target`, `window`, `team_side`, `favorite_side`, `score_diff`, `team_dangerous_attacks`, `team_shots_total`, `team_key_passes`, `hit`.

10. Exemplo pratico: minuto 60, Barcelona favorito pre-jogo, jogo 1x1, Barcelona tem dangerous attacks e key passes acima do p75 nos ultimos 10m. Estrategia ativa.

11. Observacoes de uso: `Over Janela Curta`; usada para discovery estatistico de Back Over.

### favorite_losing_pressure_high_2of3

1. Nome: `favorite_losing_pressure_high_2of3`

2. Decomposicao: favorito pre-jogo perdendo no cutoff com pressao alta em 2 de 3 metricas.

3. Regra de favorito: menor odd pre-jogo entre `AvgH` e `AvgA`.

4. Regra de placar: favorito perdendo por qualquer margem (`score_diff < 0`).

5. Lado analisado: favorito pre-jogo.

6. Metricas usadas: `team_dangerous_attacks_{window}m`, `team_shots_total_{window}m`, `team_key_passes_{window}m`.

7. Thresholds: pelo menos 2 de 3 metricas `>= p75`.

8. Janela temporal: `last_5m`, `last_10m`, `last_15m`.

9. Colunas do CSV: `favorite_side`, `score_diff`, `team_dangerous_attacks`, `team_shots_total`, `team_key_passes`, `target`, `hit`.

10. Exemplo pratico: minuto 65, Real Madrid favorito, perdendo 0x1, com shots total e dangerous attacks acima do p75 nos ultimos 10m. Estrategia ativa.

11. Observacoes de uso: `Over Janela Curta`; discovery estatistico de Back Over.

### underdog_winning_favorite_pressing_2of3

1. Nome: `underdog_winning_favorite_pressing_2of3`

2. Decomposicao: nome descreve underdog vencendo e favorito pressionando; no codigo, a linha analisada e o favorito perdendo e pressionando em 2 de 3 metricas.

3. Regra de favorito: menor odd pre-jogo entre `AvgH` e `AvgA`.

4. Regra de placar: favorito perdendo (`score_diff < 0`). Isso implica adversario/underdog vencendo, se houver favorito definido.

5. Lado analisado: favorito pre-jogo (`is_favorite_side == True`).

6. Metricas usadas: `team_dangerous_attacks_{window}m`, `team_shots_total_{window}m`, `team_key_passes_{window}m`.

7. Thresholds: pelo menos 2 de 3 metricas `>= p75`.

8. Janela temporal: `last_5m`, `last_10m`, `last_15m`.

9. Colunas do CSV: `favorite_side`, `team_side`, `score_diff`, `team_dangerous_attacks`, `team_shots_total`, `team_key_passes`.

10. Exemplo pratico: minuto 70, favorito e visitante, esta perdendo 0x1 para o underdog, e tem dangerous attacks e shots total acima do p75 nos ultimos 15m. Estrategia ativa.

11. Observacoes de uso: `Over Janela Curta`; discovery estatistico. Nome e regra estao alinhados conceitualmente, mas a implementacao testa diretamente o favorito pressionando, nao uma coluna chamada `underdog_winning`.

### favorite_winning_by_1_opp_cold_2of3

1. Nome: `favorite_winning_by_1_opp_cold_2of3`

2. Decomposicao: favorito vencendo por 1 e adversario frio em 2 de 3 metricas.

3. Regra de favorito: menor odd pre-jogo entre `AvgH` e `AvgA`.

4. Regra de placar: favorito vencendo por exatamente 1 (`favorite_winning_by_1 == True`).

5. Lado analisado: favorito pre-jogo.

6. Metricas usadas no adversario: `opp_shots_total_{window}m`, `opp_dangerous_attacks_{window}m`, `opp_key_passes_{window}m`.

7. Thresholds: pelo menos 2 de 3 metricas do adversario `<= p25`.

8. Janela temporal: `last_5m`, `last_10m`, `last_15m`.

9. Colunas do CSV: `favorite_side`, `score_diff`, `opp_shots_total`, `opp_dangerous_attacks`, `opp_key_passes`, `target`, `hit`.

10. Exemplo pratico: minuto 65, Inter favorito vence 1x0, adversario tem shots total e key passes no p25 ou abaixo nos ultimos 10m. Estrategia ativa.

11. Observacoes de uso: `Under Hold`; usada para Lay Over / segurar ausencia de gol.

### team_winning_by_1_opp_cold_2of3

1. Nome: `team_winning_by_1_opp_cold_2of3`

2. Decomposicao: time analisado vencendo por 1 e adversario frio em 2 de 3 metricas.

3. Regra de favorito: sem exigencia de favorito.

4. Regra de placar: time analisado vencendo por exatamente 1 (`score_diff == 1`).

5. Lado analisado: qualquer time, mandante ou visitante.

6. Metricas usadas no adversario: `opp_shots_total_{window}m`, `opp_dangerous_attacks_{window}m`, `opp_key_passes_{window}m`.

7. Thresholds: pelo menos 2 de 3 metricas `<= p25`.

8. Janela temporal: `last_5m`, `last_10m`, `last_15m`.

9. Colunas do CSV: `score_diff`, `team_side`, `opp_shots_total`, `opp_dangerous_attacks`, `opp_key_passes`.

10. Exemplo pratico: minuto 65, mandante vence 2x1, visitante tem dangerous attacks e key passes abaixo do p25 nos ultimos 10m. Estrategia ativa.

11. Observacoes de uso: `Under Hold`; Lay Over / ausencia de gol.

### home_winning_by_1_visitor_pressing

1. Nome: `home_winning_by_1_visitor_pressing`

2. Decomposicao: mandante vencendo por 1; visitante e o lado analisado e esta pressionando.

3. Regra de favorito: sem exigencia de favorito.

4. Regra de placar: visitante perdendo por exatamente 1 (`team_side == away` e `score_diff == -1`). Equivale a mandante vencendo por 1.

5. Lado analisado: visitante.

6. Metricas usadas: `team_dangerous_attacks_{window}m`, `team_shots_on_target_{window}m`.

7. Thresholds: `team_dangerous_attacks_{window}m >= p75` OU `team_shots_on_target_{window}m >= 1`.

8. Janela temporal: `last_5m`, `last_10m`, `last_15m`.

9. Colunas do CSV: `team_side`, `score_diff`, `team_dangerous_attacks`, `team_shots_on_target`, `target`, `hit`.

10. Exemplo pratico: minuto 75, Sevilla visitante perde 0x1 para Athletic, mas tem ao menos 1 chute no alvo nos ultimos 5m. Estrategia ativa.

11. Observacoes de uso: `Over Janela Curta`; Back Over.

### away_winning_by_1_home_pressing

1. Nome: `away_winning_by_1_home_pressing`

2. Decomposicao: visitante vencendo por 1; mandante e o lado analisado e esta pressionando.

3. Regra de favorito: sem exigencia de favorito.

4. Regra de placar: mandante perdendo por exatamente 1 (`team_side == home` e `score_diff == -1`). Equivale a visitante vencendo por 1.

5. Lado analisado: mandante.

6. Metricas usadas: `team_dangerous_attacks_{window}m`, `team_shots_on_target_{window}m`.

7. Thresholds: `team_dangerous_attacks_{window}m >= p75` OU `team_shots_on_target_{window}m >= 1`.

8. Janela temporal: `last_5m`, `last_10m`, `last_15m`.

9. Colunas do CSV: `team_side`, `score_diff`, `team_dangerous_attacks`, `team_shots_on_target`, `target`, `hit`.

10. Exemplo pratico: minuto 75, mandante perde 0x1 para visitante, mas tem dangerous attacks acima do p75 nos ultimos 10m. Estrategia ativa.

11. Observacoes de uso: `Over Janela Curta`; Back Over.

### both_teams_cold_2of3

1. Nome: `both_teams_cold_2of3`

2. Decomposicao: ambos os times frios. Atencao: no codigo, a regra e 3 de 4 condicoes frias, nao 2 de 3.

3. Regra de favorito: sem exigencia de favorito.

4. Regra de placar: qualquer placar.

5. Lado analisado: linha do time analisado e adversario simultaneamente.

6. Metricas usadas: `team_shots_total_{window}m`, `opp_shots_total_{window}m`, `team_dangerous_attacks_{window}m`, `opp_dangerous_attacks_{window}m`.

7. Thresholds: pelo menos 3 de 4 metricas `<= p25`.

8. Janela temporal: `last_5m`, `last_10m`, `last_15m`.

9. Colunas do CSV: `team_shots_total`, `opp_shots_total`, `team_dangerous_attacks`, `opp_dangerous_attacks`.

10. Exemplo pratico: minuto 60, ambos times sem volume; shots total dos dois e dangerous attacks do adversario abaixo do p25. Estrategia ativa.

11. Observacoes de uso: `Under Hold`; Lay Over / ausencia de gol. Divergencia nome vs codigo deve ser preservada em auditorias.

### big_chances_recent

1. Nome: `big_chances_recent`

2. Decomposicao: time analisado criou grande chance recente.

3. Regra de favorito: sem exigencia de favorito.

4. Regra de placar: qualquer placar.

5. Lado analisado: qualquer time.

6. Metricas usadas: `team_big_chances_created_{window}m`.

7. Thresholds: `>= 1`.

8. Janela temporal: `last_5m`, `last_10m`, `last_15m`.

9. Colunas do CSV: `team_big_chances_created`, `target`, `hit`, `cutoff`, `window`.

10. Exemplo pratico: minuto 70, Barcelona criou 1 grande chance nos ultimos 10m. Estrategia ativa.

11. Observacoes de uso: `Over Janela Curta`; Back Over / discovery estatistico.

### key_passes_recent_high

1. Nome: `key_passes_recent_high`

2. Decomposicao: time analisado tem key passes recentes em nivel alto.

3. Regra de favorito: sem exigencia de favorito.

4. Regra de placar: qualquer placar.

5. Lado analisado: qualquer time.

6. Metricas usadas: `team_key_passes_{window}m`.

7. Thresholds: `>= p75` por cutoff/janela.

8. Janela temporal: `last_5m`, `last_10m`, `last_15m`.

9. Colunas do CSV: `team_key_passes`, `target`, `hit`, `cutoff`, `window`.

10. Exemplo pratico: minuto 65, time analisado tem key passes acima do p75 nos ultimos 5m. Estrategia ativa.

11. Observacoes de uso: `Over Janela Curta`; Back Over / discovery estatistico.

### opponent_no_recent_key_passes

1. Nome: `opponent_no_recent_key_passes`

2. Decomposicao: adversario sem key passes recentes enquanto o time analisado vence por 1.

3. Regra de favorito: sem exigencia de favorito.

4. Regra de placar: time analisado vencendo por 1 (`score_diff == 1`).

5. Lado analisado: time vencendo; metrica observada no adversario.

6. Metricas usadas: `opp_key_passes_{window}m`.

7. Thresholds: `== 0`.

8. Janela temporal: `last_5m`, `last_10m`, `last_15m`.

9. Colunas do CSV: `score_diff`, `opp_key_passes`, `target`, `hit`.

10. Exemplo pratico: minuto 65, mandante vence 1x0 e visitante teve 0 key passes nos ultimos 10m. Estrategia ativa.

11. Observacoes de uso: `Under Hold`; Lay Over / ausencia de gol.

## Outras Estrategias Definidas No Codigo

### team_winning_by_1_no_sot_against

DEFINIDO NO CODIGO. Time analisado vencendo por 1 e adversario com `opp_shots_on_target_{window}m == 0`. Uso: `Under Hold`.

### team_winning_by_1_low_dangerous_attacks_against

DEFINIDO NO CODIGO. Time analisado vencendo por 1 e adversario com `opp_dangerous_attacks_{window}m <= p25`. Uso: `Under Hold`.

### opponent_no_big_chances

DEFINIDO NO CODIGO. Time analisado vencendo por 1 e adversario com `opp_big_chances_created_{window}m == 0`. Uso: `Under Hold`.

### team_losing_pressure_high_2of3

DEFINIDO NO CODIGO. Time analisado perdendo por qualquer margem (`score_diff < 0`) e pressao alta em 2 de 3 metricas (`dangerous_attacks`, `shots_total`, `key_passes >= p75`). Uso: `Over Janela Curta`.

### dangerous_attacks_accelerating

DEFINIDO NO CODIGO. Time analisado com `team_dangerous_attacks_{window}m >= p75`. Uso: `Over Janela Curta`.

### shots_on_target_recent

DEFINIDO NO CODIGO. Time analisado com `team_shots_on_target_{window}m >= 1`. Uso: `Over Janela Curta`.

### corners_recent_high

DEFINIDO NO CODIGO. Time analisado com `team_corners_{window}m >= p75`. Uso: `Over Janela Curta`.

## Regras de Threshold

DEFINIDO NO CODIGO em `calculate_thresholds`:

```text
p25 e p75 sao calculados por cutoff, janela e indicador, usando os valores observados nas linhas base.
```

Implementacao:

```text
p25 = values[int(0.25 * (len(values) - 1))]
p75 = values[int(0.75 * (len(values) - 1))]
```

Observacao: e um quantil empirico simples por posicao ordenada, nao interpolado.

## Observacoes Finais

- Nao criar novas regras a partir deste documento; ele e um dicionario de leitura e reproducibilidade.
- Quando houver divergencia entre nome e codigo, o codigo prevalece para reproduzir o estudo.
- `both_teams_cold_2of3` tem divergencia importante: nome sugere 2 de 3, codigo executa 3 de 4.
- `pressing` nos playbooks home/away nao usa regra 2of3; usa OR entre dangerous attacks p75 e shots on target >= 1.
- Odds Football-Data sao pre-jogo/pre-close, nao odds live/minuto a minuto.
- Todas as regras usam apenas dados ate o cutoff para features; targets sao avaliados depois do cutoff.
