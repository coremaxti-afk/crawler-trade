# ODDS INTERACTION PLAN V1

## Status

Plano metodologico para analise de interacoes Odds + H8 / Match State.

Nao contem codigo.

Nao cria dataset.

Nao executa baseline.

Nao cria modelo.

Nao faz backtesting.

Nao cria producao.

---

## 1. Contexto

A validacao estatistica inicial de Odds V1 indicou que odds pre-jogo nao apresentaram sinal forte isolado para `target_late_goal_75`.

Resultado anterior:

- MANTER: 0
- OBSERVAR: `favorite_strength`, `match_balance`, `favorite_side = none_clear`
- DESCARTAR isolado: `implied_prob_over25_norm`, `over25_closing_strength`

Decisao PM para esta etapa:

- nao focar apenas em `target_late_goal_75`;
- priorizar cutoff 60;
- usar gol apos 60 como target principal;
- usar gols apos 65, 70 e 75 como targets secundarios.

Justificativa Quant:

O cutoff 60 foi onde apareceram os melhores sinais anteriores em:

- H8 isolado;
- Segmentacao + H8.

Portanto, Odds devem ser avaliadas prioritariamente como moderadoras de dinamica in-game em cutoff 60, nao como preditores isolados de gol apos 75.

---

## 2. Objetivo

Definir uma analise controlada de interacoes entre:

- odds pre-jogo;
- features H8 ate cutoff;
- Match State ate cutoff.

Objetivo principal:

```text
Avaliar se odds pre-jogo ajudam a qualificar sinais in-game no minuto 60.
```

Perguntas principais:

1. `favorite_strength` melhora a interpretacao de H8 no cutoff 60?
2. `match_balance` melhora a interpretacao de H8 no cutoff 60?
3. `favorite_strength` combinado com Match State no cutoff 60 gera sinal para gol apos 60?
4. `match_balance` combinado com Match State no cutoff 60 gera sinal para gol apos 60?
5. Alguma interacao justifica futura validacao expandida para cutoffs 65/70/75?

---

## 3. Target Principal e Targets Secundarios

### Target principal

```text
goal_after_60
```

Definicao:

- indicador binario se houve pelo menos um gol apos o minuto 60.

### Targets secundarios

```text
goal_after_65
goal_after_70
goal_after_75
```

Uso dos targets secundarios:

- apenas robustez;
- nao devem substituir a conclusao principal;
- nao devem ser usados para escolher retroativamente o melhor cutoff.

---

## 4. Cutoff Principal e Cutoffs Secundarios

### Cutoff principal

```text
60
```

### Cutoffs secundarios

```text
65
70
75
```

Regra:

- toda decisao de MANTER/OBSERVAR/DESCARTAR deve priorizar o comportamento no cutoff 60;
- cutoffs 65/70/75 servem para verificar estabilidade ou enfraquecimento do sinal.

---

## 5. Fontes Esperadas

Fontes candidatas:

- Dataset Odds V1;
- Dataset H8 V1;
- Dataset in-game com Match State;
- target derivado de incidentes ate/depois de cada cutoff.

Artefatos ja existentes que podem servir como base:

- `LateGoalResearch/data/processed/datasets/late_goal_dataset_odds_v1.csv`
- `data/processed/features/h8_features_v1.*`, se aplicavel;
- `data/processed/datasets/late_goal_dataset_v1b_ingame.csv`, se aplicavel;
- targets previamente validados para gols apos cutoffs.

Observacao:

Este documento nao autoriza criacao de dataset. Ele apenas define a especificacao analitica para a proxima execucao controlada.

---

## 6. Features de Odds Autorizadas

### Principais

- `favorite_strength`
- `match_balance`

### Auxiliares, somente se necessario

- `favorite_side`
- `implied_prob_over25_norm`

Nao priorizar nesta V1:

- `over25_closing_strength`
- Asian Handicap
- movement odds
- max odds
- average odds

Justificativa:

- `favorite_strength` e `match_balance` foram os unicos sinais de odds com valor potencial como moderadores;
- Over/Under 2.5 nao mostrou sinal isolado suficiente e deve ficar secundario.

---

## 7. Features H8 Autorizadas

Prioridade H8 no cutoff 60:

- `shots_last_10m`
- `momentum_trend_last_10m`

Features H8 secundarias, somente se ja existirem no dataset validado:

- `momentum_last_5m_avg`
- `xg_last_10m`

Regra:

- usar apenas valores calculados ate o cutoff;
- para cutoff 60, janelas devem respeitar `minute <= 60`;
- proibido usar qualquer evento apos o cutoff.

---

## 8. Features Match State Autorizadas

Para cutoff 60:

- `score_state_group`
- `score_diff_home_until_cutoff`
- `total_goals_until_cutoff`

Segmentos prioritarios de Match State:

- empate aos 60;
- favorito forte empatando aos 60;
- favorito forte perdendo aos 60;
- jogo equilibrado pre-jogo + empate aos 60;
- 3 gols ja marcados aos 60, apenas como exploratorio secundario.

---

## 9. Interacoes Prioritarias V1

### Grupo A — favorite_strength + H8 @60

Interacoes:

1. `favorite_strength_high + shots_last_10m_high @60`
2. `favorite_strength_high + momentum_trend_last_10m_positive @60`
3. `favorite_strength_low + shots_last_10m_high @60`

Objetivo:

- verificar se pressao in-game tem significado diferente em jogos com favorito forte vs jogos sem favorito forte.

---

### Grupo B — match_balance + H8 @60

Interacoes:

1. `match_balance_high + shots_last_10m_high @60`
2. `match_balance_high + momentum_trend_last_10m_positive @60`
3. `match_balance_low + shots_last_10m_high @60`

Objetivo:

- verificar se jogos equilibrados pre-jogo amplificam sinais H8 no minuto 60.

---

### Grupo C — favorite_strength + Match State @60

Interacoes:

1. `favorite_strength_high + empate_aos_60`
2. `favorite_strength_high + favorito_perdendo_aos_60`
3. `favorite_strength_high + favorito_vencendo_por_1_aos_60`

Objetivo:

- testar a hipotese de pressao tardia quando favorito forte ainda nao resolveu a partida.

---

### Grupo D — match_balance + Match State @60

Interacoes:

1. `match_balance_high + empate_aos_60`
2. `match_balance_high + total_goals_until_60_eq_2_or_3`
3. `match_balance_low + empate_aos_60`

Objetivo:

- testar se equilibrio pre-jogo combinado com jogo aberto/empatado aos 60 aumenta gols apos 60.

---

## 10. Definicoes de Cortes

### favorite_strength_high

Recomendacao:

```text
top 25% de favorite_strength
```

### favorite_strength_low

Recomendacao:

```text
bottom 25% de favorite_strength
```

### match_balance_high

Recomendacao:

```text
top 25% de match_balance
```

### match_balance_low

Recomendacao:

```text
bottom 25% de match_balance
```

### shots_last_10m_high

Recomendacao:

```text
top 25% de shots_last_10m no cutoff 60
```

### momentum_trend_last_10m_positive

Recomendacao:

```text
momentum_trend_last_10m > 0
```

Caso a distribuicao tenha muitos empates/zeros, usar top 25% como alternativa documentada.

---

## 11. Metricas Obrigatorias

Para cada interacao:

- cutoff;
- target avaliado;
- N;
- positivos;
- negativos;
- taxa positiva do grupo;
- taxa baseline do cutoff;
- diferenca em pontos percentuais;
- odds ratio;
- intervalo de confianca 95%;
- p-value Fisher exact test;
- classificacao;
- observacao de interpretabilidade.

---

## 12. Baselines de Comparacao

Para cada target/cutoff, comparar contra:

1. taxa geral do target no cutoff;
2. componente H8 isolado equivalente;
3. componente odds isolado equivalente;
4. componente Match State isolado equivalente, quando aplicavel.

Exemplo:

Para `favorite_strength_high + shots_last_10m_high @60`, comparar com:

- taxa geral de `goal_after_60`;
- `favorite_strength_high` isolado;
- `shots_last_10m_high @60` isolado.

---

## 13. Classificacao

### MANTER

Interacao com:

- N >= 30;
- diff >= +8 p.p. vs baseline do cutoff;
- OR > 1.50;
- p-value < 0.10;
- efeito superior aos componentes isolados;
- interpretacao coerente;
- sem concentracao extrema em poucos times.

### OBSERVAR

Interacao com:

- N >= 20;
- diff >= +5 p.p.; ou
- OR > 1.25;
- mas p-value fraco ou amostra limitada;
- sinal util para robustez futura.

### DESCARTAR

Interacao com:

- diff fraco;
- OR proximo de 1;
- p-value fraco;
- N insuficiente;
- sinal inferior aos componentes isolados;
- interpretacao incoerente.

---

## 14. Regras Anti-Leakage

Obrigatorio:

1. Odds devem ser pre-jogo.
2. H8 deve usar apenas eventos ate o cutoff.
3. Match State deve usar apenas gols/eventos ate o cutoff.
4. Target deve contar apenas gols apos o cutoff.
5. Proibido usar placar final como feature.
6. Proibido usar full-match statistics.
7. Proibido usar odds live/in-play.
8. Proibido usar Asian Handicap nesta V1.
9. Proibido escolher cutoff final com base no melhor resultado apos execucao.

Ressalva obrigatoria:

```text
Football-Data nao fornece timestamp individual das closing odds; closing odds sao tratadas como pre-jogo pela semantica da fonte.
```

---

## 15. Robustez Secundaria

Apos avaliar cutoff 60, repetir somente interacoes MANTER ou OBSERVAR em:

- cutoff 65 com `goal_after_65`;
- cutoff 70 com `goal_after_70`;
- cutoff 75 com `goal_after_75`.

Regra:

- se o sinal existir apenas em 60, classificar como sinal especifico de cutoff 60;
- se persistir em 65/70, classificar como mais robusto;
- se desaparecer em 65/70/75, manter como OBSERVAR no maximo.

---

## 16. Riscos Metodologicos

1. Amostra pequena apos interacoes.
2. Risco de p-hacking por combinacoes excessivas.
3. Odds isoladas foram fracas.
4. H8 e Segmentacao tambem tiveram sinais instaveis.
5. Cutoff 60 deve ser priorizado por decisao previa, nao por selecao retroativa.
6. Match State pode reduzir muito o N de alguns grupos.
7. Necessario controlar concentracao por times se algum sinal aparecer forte.

Mitigacao:

- limitar interacoes a este plano;
- foco principal no cutoff 60;
- cutoffs secundarios apenas para robustez;
- comparar sempre com componentes isolados;
- nao criar baseline antes da validacao estatistica.

---

## 17. Resultado Esperado da Execucao Futura

Documento futuro esperado:

```text
docs/04_RESEARCH/ODDS_INTERACTION_VALIDATION_RESULTS_V1.md
```

Conteudo minimo:

- resumo executivo;
- tabela de interacoes @60;
- comparacao com componentes isolados;
- robustez em 65/70/75 para sinais OBSERVAR/MANTER;
- ranking de interacoes;
- classificacao final;
- recomendacao Quant.

---

## 18. Decisao Quant

```text
ODDS_INTERACTION_PLAN_V1 APROVADO METODOLOGICAMENTE
```

Foco principal:

```text
cutoff 60 + goal_after_60
```

Targets secundarios:

```text
goal_after_65
goal_after_70
goal_after_75
```

Interacoes prioritarias:

- `favorite_strength + H8 @60`
- `match_balance + H8 @60`
- `favorite_strength + Match State @60`
- `match_balance + Match State @60`

Restricoes mantidas:

- nao criar modelo;
- nao executar baseline;
- nao fazer backtesting;
- nao criar producao.
