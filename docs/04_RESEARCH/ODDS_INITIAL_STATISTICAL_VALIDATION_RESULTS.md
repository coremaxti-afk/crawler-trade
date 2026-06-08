# ODDS INITIAL STATISTICAL VALIDATION RESULTS

## Status

Validacao estatistica inicial executada sobre o Dataset Odds V1.

Nao contem modelo.

Nao contem baseline.

Nao contem backtesting.

Nao contem producao.

---

## 1. Resumo Executivo

Dataset analisado:

- `late_goal_dataset_odds_v1.csv`

Target:

- `target_late_goal_75`

Amostra:

- 380 partidas
- 189 positivos
- 191 negativos
- taxa geral positiva: 49.74%

Features avaliadas:

- `implied_prob_over25_norm`
- `over25_closing_strength`
- `favorite_strength`
- `match_balance`
- `favorite_side`

Resultado geral:

```text
MANTER: 0
OBSERVAR: 3 cortes/grupos
DESCARTAR: maioria dos cortes/grupos
```

Parecer Quant:

```text
ODDS PRE-JOGO NAO MOSTRARAM SINAL FORTE ISOLADO PARA target_late_goal_75
```

As odds podem continuar como variaveis auxiliares para interacoes futuras, mas nao justificam baseline isolado neste momento.

---

## 2. Regras de Validacao

Features continuas foram avaliadas por:

- top 25% vs restante;
- bottom 25% vs restante.

Feature categorica `favorite_side` foi avaliada por:

- `home` vs restante;
- `away` vs restante;
- `none_clear` vs restante.

Metricas calculadas:

- N;
- positivos;
- negativos;
- taxa positiva;
- diferenca vs taxa geral em pontos percentuais;
- odds ratio;
- intervalo de confianca 95%;
- p-value Fisher exact test;
- classificacao.

Criterios:

### MANTER

- N >= 30;
- efeito absoluto >= 5 p.p.;
- OR >= 1.25 ou OR <= 0.80;
- p-value < 0.10;
- interpretacao coerente.

### OBSERVAR

- efeito absoluto >= 5 p.p.; ou
- OR relevante mas p-value fraco; ou
- sinal coerente para futura interacao.

### DESCARTAR

- efeito fraco;
- OR proximo de 1;
- p-value fraco;
- interpretacao instavel.

---

## 3. Resultado por Feature

### 3.1 implied_prob_over25_norm

| Corte | Threshold | N | Positivos | Negativos | Taxa | Diff vs geral | OR | IC 95% | p-value | Classe |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| Top 25% | 0.6414 | 96 | 45 | 51 | 46.9% | -2.9 p.p. | 0.86 | [0.54, 1.36] | 0.5558 | DESCARTAR |
| Bottom 25% | 0.5315 | 95 | 51 | 44 | 53.7% | +3.9 p.p. | 1.23 | [0.78, 1.97] | 0.4078 | DESCARTAR |

Interpretação:

- expectativa alta de Over 2.5 nao aumentou a taxa de gol tardio;
- o bottom 25% teve taxa maior, mas efeito pequeno e nao significativo;
- sinal contrario ao esperado para a hipotese principal.

Decisao:

```text
DESCARTAR COMO FEATURE ISOLADA
```

---

### 3.2 over25_closing_strength

| Corte | Threshold | N | Positivos | Negativos | Taxa | Diff vs geral | OR | IC 95% | p-value | Classe |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| Top 25% | 0.2829 | 96 | 45 | 51 | 46.9% | -2.9 p.p. | 0.86 | [0.54, 1.36] | 0.5558 | DESCARTAR |
| Bottom 25% | 0.0630 | 95 | 51 | 44 | 53.7% | +3.9 p.p. | 1.23 | [0.78, 1.97] | 0.4078 | DESCARTAR |

Interpretação:

- resultado equivalente a `implied_prob_over25_norm`, como esperado pela dependencia matematica entre as features;
- nao houve evidencia de que mercado fortemente inclinado ao Over aumente gols apos 75.

Decisao:

```text
DESCARTAR COMO FEATURE ISOLADA
```

---

### 3.3 favorite_strength

| Corte | Threshold | N | Positivos | Negativos | Taxa | Diff vs geral | OR | IC 95% | p-value | Classe |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| Top 25% | 0.4934 | 95 | 43 | 52 | 45.3% | -4.5 p.p. | 0.79 | [0.49, 1.25] | 0.3441 | OBSERVAR |
| Bottom 25% | 0.1346 | 95 | 50 | 45 | 52.6% | +2.9 p.p. | 1.17 | [0.73, 1.86] | 0.5544 | DESCARTAR |

Interpretação:

- favoritos muito fortes tiveram menor taxa de gol tardio;
- efeito direcional negativo moderado, mas sem significancia;
- pode indicar que jogos muito desequilibrados pre-jogo nao necessariamente geram gols apos 75.

Decisao:

```text
OBSERVAR APENAS PARA INTERACAO FUTURA COM MATCH STATE/H8
```

Uso futuro recomendado:

- favorito forte empatando aos 60/65/70;
- favorito forte perdendo por 1;
- favorito forte + `shots_last_10m` alto.

---

### 3.4 match_balance

| Corte | Threshold | N | Positivos | Negativos | Taxa | Diff vs geral | OR | IC 95% | p-value | Classe |
|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| Top 25% | 0.8304 | 95 | 51 | 44 | 53.7% | +3.9 p.p. | 1.23 | [0.78, 1.97] | 0.4078 | DESCARTAR |
| Bottom 25% | 0.5066 | 95 | 43 | 52 | 45.3% | -4.5 p.p. | 0.79 | [0.49, 1.25] | 0.3441 | OBSERVAR |

Interpretação:

- jogos mais equilibrados tiveram taxa levemente maior;
- jogos menos equilibrados tiveram taxa menor;
- efeito coerente, mas abaixo de 5 p.p. e sem significancia.

Decisao:

```text
OBSERVAR APENAS COMO MODERADOR FUTURO
```

Uso futuro recomendado:

- `match_balance + empate_ate_cutoff`;
- `match_balance + 3 gols ja marcados`;
- `match_balance + shots_last_10m`.

---

### 3.5 favorite_side

| Grupo | N | Positivos | Negativos | Taxa | Diff vs geral | OR | IC 95% | p-value | Classe |
|---|---:|---:|---:|---:|---:|---:|---|---:|---|
| home | 229 | 109 | 120 | 47.6% | -2.1 p.p. | 0.81 | [0.53, 1.22] | 0.3456 | DESCARTAR |
| away | 127 | 66 | 61 | 52.0% | +2.2 p.p. | 1.14 | [0.75, 1.75] | 0.5869 | DESCARTAR |
| none_clear | 24 | 14 | 10 | 58.3% | +8.6 p.p. | 1.45 | [0.63, 3.35] | 0.4072 | OBSERVAR |

Interpretação:

- favorito mandante nao apresentou sinal positivo;
- favorito visitante apresentou efeito pequeno e nao significativo;
- jogos sem favorito claro tiveram maior taxa, mas N=24 e p-value fraco.

Decisao:

```text
OBSERVAR none_clear APENAS COMO HIPOTESE EXPLORATORIA
```

---

## 4. Ranking dos Sinais Observados

Ranking por efeito positivo bruto:

1. `favorite_side = none_clear`
   - N=24
   - taxa=58.3%
   - diff +8.6 p.p.
   - OR=1.45
   - p=0.4072
   - Classe: OBSERVAR

2. `implied_prob_over25_norm bottom25`
   - N=95
   - taxa=53.7%
   - diff +3.9 p.p.
   - OR=1.23
   - p=0.4078
   - Classe: DESCARTAR

3. `over25_closing_strength bottom25`
   - N=95
   - taxa=53.7%
   - diff +3.9 p.p.
   - OR=1.23
   - p=0.4078
   - Classe: DESCARTAR

4. `match_balance top25`
   - N=95
   - taxa=53.7%
   - diff +3.9 p.p.
   - OR=1.23
   - p=0.4078
   - Classe: DESCARTAR

5. `favorite_side = away`
   - N=127
   - taxa=52.0%
   - diff +2.2 p.p.
   - OR=1.14
   - p=0.5869
   - Classe: DESCARTAR

Nenhum sinal positivo atingiu criterio de MANTER.

---

## 5. Respostas as Perguntas

### 1. Odds pre-jogo carregam sinal para gols tardios?

Resposta:

```text
NAO COMO FEATURES ISOLADAS NESTA AMOSTRA
```

As odds pre-jogo mostraram sinais fracos e sem significancia estatistica contra `target_late_goal_75`.

### 2. Over/Under 2.5 e mais util que 1X2?

Resposta:

```text
NAO
```

Over/Under 2.5 nao apresentou efeito positivo no sentido esperado. O top 25% de expectativa de Over teve taxa menor que a media geral.

### 3. favorite_strength ajuda?

Resposta:

```text
NAO ISOLADAMENTE
```

O top 25% de `favorite_strength` teve taxa menor de gol tardio:

- taxa=45.3%
- diff -4.5 p.p.
- OR=0.79
- p=0.3441

Pode ser util apenas em interacao com Match State ou H8.

### 4. match_balance ajuda?

Resposta:

```text
SINAL FRACO, NAO SUFICIENTE ISOLADAMENTE
```

Jogos mais equilibrados tiveram taxa levemente maior, mas sem significancia:

- taxa=53.7%
- diff +3.9 p.p.
- OR=1.23
- p=0.4078

### 5. Alguma feature deve entrar em analise combinada futura com H8/Segmentacao?

Resposta:

```text
SIM, MAS APENAS COMO OBSERVAR
```

Candidatas futuras:

- `favorite_strength`, especialmente com Match State e H8;
- `match_balance`, especialmente com empate ate cutoff;
- `favorite_side = none_clear`, apenas exploratorio por N pequeno;
- `implied_prob_over25_norm`, nao por sinal isolado, mas por interpretabilidade como expectativa de gols.

---

## 6. Comparacao por Familia de Mercado

### Over/Under 2.5

Resultado:

```text
FRACO / DESCARTAR ISOLADO
```

A hipotese de que alta expectativa pre-jogo de gols aumentaria gols tardios nao foi suportada.

### Match Odds 1X2

Resultado:

```text
FRACO / OBSERVAR COMO MODERADOR
```

1X2 nao gerou sinal forte isolado, mas `favorite_strength`, `match_balance` e `favorite_side` podem servir como moderadores de situacoes in-game.

Conclusao comparativa:

```text
1X2 parece mais util que Over/Under 2.5 para interacoes futuras, mas nenhum mercado foi forte isoladamente.
```

---

## 7. Riscos e Ressalvas

1. Amostra unica de 380 partidas limita poder estatistico.
2. Odds closing da Football-Data nao possuem timestamp individual.
3. Odds sao pre-jogo e podem nao capturar dinamica in-game.
4. Cortes por quartil sao exploratorios.
5. Nenhum resultado deve ser usado para modelo ou baseline neste momento.
6. Multiplos testes aumentam risco de falso positivo.

---

## 8. Decisao Final Quant

```text
MANTER: 0
OBSERVAR: favorite_strength, match_balance, favorite_side=none_clear
DESCARTAR ISOLADO: implied_prob_over25_norm, over25_closing_strength
```

Parecer geral:

```text
ODDS INITIAL STATISTICAL VALIDATION: APTO COM RESSALVAS
```

Conclusao:

```text
ODDS PRE-JOGO NAO DEVEM VIRAR BASELINE ISOLADO AGORA
```

Recomendacao:

- nao criar modelo;
- nao executar baseline;
- nao fazer backtesting;
- nao criar producao;
- manter odds apenas como candidatas auxiliares para interacoes controladas com H8, Match State e Segmentacao.

---

## 9. Proxima Etapa Recomendada

Proxima etapa Quant recomendada:

```text
ODDS + H8 / MATCH STATE INTERACTION PLAN
```

Escopo sugerido, limitado:

1. `favorite_strength + score_state_group`
2. `favorite_strength + shots_last_10m`
3. `match_balance + empate_ate_cutoff`
4. `match_balance + shots_last_10m`
5. `implied_prob_over25_norm + shots_last_10m`

Restricao:

- nao expandir combinacoes alem de um conjunto pequeno e predefinido;
- nao criar baseline antes da validacao de interacoes;
- nao usar Asian Handicap ainda.
