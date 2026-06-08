# ODDS INITIAL STATISTICAL VALIDATION

## Status

Plano metodologico para validacao estatistica inicial das features de odds.

Nao contem codigo.

Nao contem resultado estatistico executado.

Nao cria modelo.

Nao executa baseline.

Nao faz backtesting.

Nao cria producao.

---

## 1. Contexto

O Dataset Odds V1 foi revisado pelo Quant Research.

Parecer:

```text
APTO COM RESSALVAS
```

Confirmacoes:

- 380 linhas.
- 380 partidas unicas.
- 0 duplicatas.
- `target_late_goal_75` unido corretamente.
- target preservado: 191 negativos / 189 positivos.
- 0 target mismatches.
- 0 odds invalidas.
- 0 probabilidades invalidas.
- sem Asian Handicap.
- sem live/in-play.
- sem full-match columns.

Ressalva metodologica:

- Football-Data nao fornece timestamp individual das closing odds, mas a semantica pre-jogo esta documentada.

---

## 2. Objetivo

Executar validacao estatistica inicial das features de odds contra:

```text
target_late_goal_75
```

Objetivo analitico:

Responder se odds pre-jogo carregam sinal estatistico para gols tardios.

Perguntas principais:

1. Odds pre-jogo carregam sinal para gols tardios?
2. Over/Under 2.5 e mais util que Match Odds 1X2?
3. `favorite_strength` ajuda?
4. `match_balance` ajuda?
5. Alguma feature deve entrar em analise combinada futura com H8 ou Segmentacao?

---

## 3. Dataset Esperado

Fonte esperada:

- `data/processed/datasets/late_goal_dataset_odds_v1.csv`

Artefatos auxiliares:

- `data/processed/datasets/late_goal_dataset_odds_v1_metadata.json`
- `data/processed/datasets/late_goal_dataset_odds_v1_validation_report.json`

Grain:

```text
1 linha por match_id
```

Target:

```text
target_late_goal_75
```

---

## 4. Features Prioritarias

Features autorizadas para validacao inicial:

1. `implied_prob_over25_norm`
2. `over25_closing_strength`
3. `favorite_strength`
4. `match_balance`
5. `favorite_side`

---

## 5. Metodologia por Tipo de Feature

### 5.1 Features Continuas

Features:

- `implied_prob_over25_norm`
- `over25_closing_strength`
- `favorite_strength`
- `match_balance`

Avaliacoes obrigatorias:

1. Top 25% vs restante.
2. Bottom 25% vs restante, quando interpretavel.
3. Correlação simples com target, apenas como diagnostico auxiliar.
4. Diferenca de media entre target positivo e negativo.

Para cada corte reportar:

- N.
- Positivos.
- Negativos.
- Taxa de target no grupo.
- Taxa geral.
- Diferenca em pontos percentuais.
- Odds ratio.
- Intervalo de confianca 95% do OR.
- p-value por Fisher exact test.

### 5.2 Feature Categorica

Feature:

- `favorite_side`

Grupos:

- `home`
- `away`
- `none_clear`

Para cada grupo reportar:

- N.
- Positivos.
- Negativos.
- Taxa de target.
- Diferenca vs taxa geral.
- Odds ratio vs restante.
- Intervalo de confianca 95%.
- p-value.

---

## 6. Criterios de Classificacao

### MANTER

Feature ou corte com:

- N >= 30;
- efeito absoluto >= 5 p.p.;
- OR >= 1.25 ou OR <= 0.80;
- p-value < 0.10;
- interpretacao coerente.

### OBSERVAR

Feature ou corte com:

- efeito absoluto >= 5 p.p. mas p-value fraco; ou
- OR relevante mas amostra limitada; ou
- sinal coerente para futura interacao com H8/Segmentacao.

### DESCARTAR

Feature ou corte com:

- efeito fraco;
- OR proximo de 1;
- p-value fraco;
- interpretacao instavel.

---

## 7. Hipoteses por Feature

### implied_prob_over25_norm

Hipotese:

- jogos com maior probabilidade implicita de Over 2.5 tem maior chance de gol tardio.

Tipo de informacao:

- expectativa de gols.

Possivel interacao futura:

- `implied_prob_over25_norm + shots_last_10m`
- `implied_prob_over25_norm + defensivo_fragile`

### over25_closing_strength

Hipotese:

- quanto mais o mercado favorece Over 2.5 sobre Under 2.5, maior a chance de gol tardio.

Tipo de informacao:

- expectativa direcional de gols.

Possivel interacao futura:

- `over25_closing_strength + momentum_trend_last_10m`

### favorite_strength

Hipotese:

- jogos com favorito forte podem gerar pressao tardia, principalmente se o favorito estiver empatando ou perdendo in-game.

Tipo de informacao:

- forca relativa.

Possivel interacao futura:

- `favorite_strength + match_state`
- `favorite_strength + shots_last_10m`
- `favorite_strength + ofensivo_forte_vs_defesa_fragil`

### match_balance

Hipotese:

- jogos mais equilibrados podem permanecer competitivos ate o fim e gerar mais gols tardios.

Tipo de informacao:

- equilibrio/desequilibrio pre-jogo.

Possivel interacao futura:

- `match_balance + empate_ate_cutoff`

### favorite_side

Hipotese:

- favorito mandante, favorito visitante ou ausencia de favorito claro podem ter comportamentos distintos em gols tardios.

Tipo de informacao:

- direcao do favoritismo.

Possivel interacao futura:

- favorito forte perdendo;
- favorito forte empatando;
- visitante favorito vencendo por 1.

---

## 8. Regras Anti-Leakage

Obrigatorio:

- usar apenas features do Dataset Odds V1;
- odds devem ser closing pre-jogo pela semantica Football-Data;
- target deve ser usado apenas como resposta;
- nao usar odds live/in-play;
- nao usar Asian Handicap;
- nao usar full-match columns;
- nao usar placar final;
- nao criar features novas alem das autorizadas para esta validacao.

Ressalva obrigatoria no relatorio final:

```text
Football-Data nao fornece timestamp individual das closing odds; closing odds sao tratadas como pre-jogo pela semantica da fonte.
```

---

## 9. Resultado Esperado Apos Execucao

O relatorio final deve conter:

1. Resumo executivo.
2. Confirmacao de dataset e target.
3. Tabela por feature.
4. Tabela por corte/grupo.
5. Ranking das features por efeito observado.
6. Comparacao Over/Under 2.5 vs Match Odds 1X2.
7. Respostas as perguntas principais.
8. Classificacao final:
   - MANTER
   - OBSERVAR
   - DESCARTAR
9. Recomendacao da proxima etapa.

---

## 10. Restricoes

- Nao criar modelo.
- Nao executar baseline.
- Nao fazer backtesting.
- Nao criar producao.
- Nao expandir para Asian Handicap.
- Nao criar interacoes ainda.

---

## 11. Decisao Quant

Status metodologico:

```text
PRONTO PARA EXECUCAO CONTROLADA PELO CODEX
```

Proxima acao recomendada:

- Codex executar a validacao estatistica descrita neste documento.
- Atualizar este mesmo arquivo com resultados reais ou criar secao final de resultados executados.

