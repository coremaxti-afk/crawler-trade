# H8 SHORT-TERM / LATE MARKET STRATEGY PLAN

## Status

Plano metodologico de pesquisa para estrategias de janela curta e mercado tardio baseadas em H8.

Nao contem codigo.

Nao cria dataset.

Nao executa baseline.

Nao cria modelo.

Nao faz backtesting.

Nao cria producao.

---

## 1. Contexto

O projeto ja testou frentes isoladas e combinadas para gol tardio, incluindo:

- H8 para gol apos 75;
- Segmentacao + H8;
- Match State;
- Odds pre-jogo;
- Odds + H8 / Match State.

Nenhuma dessas frentes autorizou baseline, modelo, backtesting ou producao.

Nova hipotese PM:

```text
H8 pode ser mais adequado para janelas curtas a partir dos 60 minutos do que para prever apenas gol apos 75.
```

Justificativa Quant:

H8 mede dinamica recente do jogo: chutes, xG, momentum e tendencia de pressao. Esses sinais tendem a ser mais coerentes para horizontes curtos, por exemplo 10 a 20 minutos apos o cutoff, do que para prever eventos muito distantes como apenas gol apos 75.

---

## 2. Objetivo

Criar uma pesquisa metodologica para avaliar se sinais H8 no minuto 60 ajudam a identificar:

1. jogos quentes, candidatos a Back Over / Lay Under;
2. jogos mornos, candidatos a Back Under / Lay Over;
3. janelas de tempo em que o sinal H8 e mais informativo;
4. quais alvos podem ser avaliados sem odds live;
5. quais analises exigiriam odds live em fase futura.

Foco inicial:

```text
entrada aos 60 minutos
```

---

## 3. Escopo V1

A V1 deve ser estatistica e exploratoria.

Permitido:

- definir targets;
- definir features candidatas;
- definir filtros;
- definir criterios de validacao;
- avaliar taxas/eventos em janelas curtas em etapa futura controlada.

Nao permitido nesta etapa:

- criar codigo;
- criar dataset;
- executar baseline;
- criar modelo;
- fazer backtesting;
- criar producao;
- simular PnL real;
- usar odds live sem fonte validada.

---

## 4. Cutoff Inicial

Cutoff principal:

```text
60
```

Motivo:

- H8 teve melhores sinais anteriores no cutoff 60;
- Segmentacao + H8 tambem mostrou melhor sinal em cutoff 60;
- entrada aos 60 permite janelas curtas suficientes para avaliar 60-70, 60-75 e 60-80.

Cutoffs futuros opcionais:

- 65;
- 70;
- 75.

Regra:

- V1 deve priorizar 60;
- outros cutoffs so entram se 60 mostrar sinal minimamente promissor.

---

## 5. Targets Aprovados

### 5.1 Targets principais

#### T1 — goal_60_70

Definicao:

```text
Houve pelo menos um gol entre 60 e 70.
```

Uso:

- janela curta mais direta para capturar efeito imediato de pressao H8.

Prioridade:

```text
MUITO ALTA
```

---

#### T2 — goal_60_75

Definicao:

```text
Houve pelo menos um gol entre 60 e 75.
```

Uso:

- janela curta-media;
- ponte entre H8 @60 e mercado tardio antes dos 75.

Prioridade:

```text
ALTA
```

---

#### T3 — goal_60_80

Definicao:

```text
Houve pelo menos um gol entre 60 e 80.
```

Uso:

- janela mais ampla;
- pode aumentar N positivo, mas dilui efeito imediato.

Prioridade:

```text
MEDIA-ALTA
```

---

### 5.2 Targets secundarios / complementares

#### T4 — goal_65_80

Definicao:

```text
Houve pelo menos um gol entre 65 e 80.
```

Uso:

- robustez futura se sinais persistirem depois dos 60;
- nao e target principal da V1.

Prioridade:

```text
MEDIA
```

---

#### T5 — no_goal_60_75

Definicao:

```text
Nao houve gol entre 60 e 75.
```

Uso:

- avaliar estrategia Back Under / Lay Over sem odds live;
- target complementar ao goal_60_75.

Prioridade:

```text
ALTA PARA ESTRATEGIA UNDER
```

---

#### T6 — no_goal_60_80

Definicao:

```text
Nao houve gol entre 60 e 80.
```

Uso:

- avaliar ausencia de gol em janela um pouco mais ampla;
- pode ser relevante para jogos mornos.

Prioridade:

```text
MEDIA-ALTA PARA ESTRATEGIA UNDER
```

---

## 6. Priorizacao dos Targets

Ordem recomendada:

1. `goal_60_70`
2. `goal_60_75`
3. `no_goal_60_75`
4. `goal_60_80`
5. `no_goal_60_80`
6. `goal_65_80`

Racional:

- `goal_60_70` testa efeito imediato do H8.
- `goal_60_75` testa uma janela mais negociavel.
- `no_goal_60_75` testa o lado oposto da estrategia.
- `goal_60_80` e `no_goal_60_80` aumentam horizonte, mas podem diluir causalidade estatistica.
- `goal_65_80` deve ser robustez ou V2.

---

## 7. Features H8 que Entram Primeiro

Prioridade 1:

- `shots_last_10m`
- `xg_last_10m`
- `momentum_trend_last_10m`
- `momentum_last_10m_avg`

Motivo:

- representam volume ofensivo recente;
- representam qualidade das chances recentes;
- representam direcao da pressao;
- representam intensidade media recente.

Prioridade 2:

- `momentum_last_5m_avg`
- `shots_last_5m`
- `xg_last_5m`

Motivo:

- podem capturar aceleracao muito recente, mas sao mais ruidosas.

Nao priorizar na V1:

- `xg_sum_until_cutoff`;
- `momentum_sum_until_cutoff`.

Motivo:

- acumulados ate o cutoff misturam historia do jogo inteiro ate 60 e podem ser menos especificos para janela curta.

---

## 8. Features Contextuais Candidatas

### Match State

- `score_state`
- `score_diff`
- `total_goals_until_cutoff`

### Odds pre-jogo

- `favorite_strength`
- `match_balance`

### Segmentacao historica

- `defensive_fragile profile`
- `offensive_strong profile`

Essas features devem ser usadas como filtros/moderadores, nao como eixo principal da V1.

---

## 9. Filtros de Match State a Testar

### Para Back Over / Lay Under

Filtros prioritarios:

1. empate aos 60;
2. time favorito perdendo aos 60;
3. time favorito empatando aos 60;
4. placar com diferenca de 1 gol;
5. total de gols ate 60 entre 1 e 3.

Hipotese:

- jogos ainda competitivos podem transformar pressao H8 recente em maior chance de gol nos proximos 10-20 minutos.

### Para Back Under / Lay Over

Filtros prioritarios:

1. placar confortavel, diferenca de 2+ gols;
2. total de gols alto ate 60 com queda de momentum;
3. favorito vencendo confortavelmente;
4. jogo empatado mas sem volume ofensivo recente;
5. baixa atividade de finalizacao nos ultimos 10 minutos.

Hipotese:

- jogos sem pressao recente e/ou com incentivo competitivo reduzido podem ter menor chance de gol na janela curta.

---

## 10. Definicao de Jogo Quente

Um jogo deve ser classificado como quente quando cumprir combinacoes de sinais H8 recentes.

Candidatos de regra:

### Hot Signal A

```text
shots_last_10m alto
```

### Hot Signal B

```text
xg_last_10m alto
```

### Hot Signal C

```text
momentum_trend_last_10m positivo
```

### Hot Signal D

```text
momentum_last_10m_avg alto
```

Definicao V1 recomendada:

```text
Jogo quente = pelo menos 2 dos 4 sinais H8 ativos.
```

Cortes recomendados:

- alto = top 25% da distribuicao no cutoff 60;
- positivo = maior que zero, quando a feature for direcional;
- se houver muitos zeros, usar top 25% tambem para tendencia.

---

## 11. Definicao de Jogo Morno

Um jogo deve ser classificado como morno quando tiver baixa pressao ofensiva recente.

Candidatos de regra:

### Cold Signal A

```text
shots_last_10m baixo
```

### Cold Signal B

```text
xg_last_10m baixo
```

### Cold Signal C

```text
momentum_trend_last_10m <= 0
```

### Cold Signal D

```text
momentum_last_10m_avg baixo
```

Definicao V1 recomendada:

```text
Jogo morno = pelo menos 2 dos 4 sinais frios ativos.
```

Cortes recomendados:

- baixo = bottom 25% da distribuicao no cutoff 60;
- tendencia nao positiva = menor ou igual a zero;
- alternativa conservadora = bottom 33% se bottom 25% gerar N muito pequeno.

---

## 12. Estrategias Candidatas

## 12.1 Back Over / Lay Under

Contexto:

- buscar gol em janela curta apos entrada aos 60.

Targets principais:

- `goal_60_70`;
- `goal_60_75`;
- `goal_60_80`.

Sinais candidatos:

- jogo quente;
- `shots_last_10m` alto;
- `xg_last_10m` alto;
- `momentum_trend_last_10m` positivo;
- `momentum_last_10m_avg` alto.

Filtros opcionais:

- empate aos 60;
- placar por 1 gol;
- favorito perdendo ou empatando;
- `defensive_fragile` em pelo menos um time;
- `offensive_strong` em pelo menos um time.

---

## 12.2 Back Under / Lay Over

Contexto:

- buscar ausencia de gol em janela curta apos entrada aos 60.

Targets principais:

- `no_goal_60_75`;
- `no_goal_60_80`.

Sinais candidatos:

- jogo morno;
- baixo volume de chutes;
- baixo xG recente;
- momentum baixo ou caindo;
- placar confortavel;
- pouca reacao ofensiva.

Filtros opcionais:

- diferenca de 2+ gols;
- favorito vencendo;
- baixa atividade ofensiva dos dois lados;
- `total_goals_until_cutoff` alto combinado com queda de ritmo.

---

## 13. Analises Possiveis Sem Odds Live

Sem odds live, a pesquisa pode avaliar apenas probabilidade/evento, nao valor de mercado real.

Analises permitidas:

1. taxa de gol por janela;
2. taxa de nao-gol por janela;
3. comparacao de jogo quente vs baseline;
4. comparacao de jogo morno vs baseline;
5. odds ratio e Fisher exact test;
6. estabilidade por cutoff;
7. concentracao por times;
8. comparacao com componentes isolados;
9. ranking de sinais por efeito observado;
10. avaliacao de robustez em 65/70/75.

Conclusao permitida sem odds live:

```text
Existe ou nao existe sinal estatistico de evento.
```

Conclusao nao permitida sem odds live:

```text
Existe ou nao existe valor esperado positivo de trade.
```

---

## 14. Analises que Exigiriam Odds Live no Futuro

Exigiriam odds live:

1. precificacao real aos 60;
2. comparacao probabilidade estimada vs odd de mercado;
3. EV esperado;
4. simulacao de entrada/saida;
5. PnL historico;
6. drawdown;
7. slippage;
8. liquidez;
9. tempo de exposicao;
10. backtesting real de mercado.

Sem odds live, a estrategia deve ser chamada apenas de:

```text
estrategia candidata baseada em sinal de evento
```

Nao chamar de:

```text
estrategia lucrativa
```

---

## 15. Criterios Minimos para Estrategia PROMISSORA

### Para Back Over / Lay Under

Uma regra e PROMISSORA se:

- N >= 40 para a janela principal;
- diff >= +8 p.p. vs baseline do target;
- OR > 1.50;
- p-value < 0.10;
- supera os componentes isolados;
- nao depende de um unico time;
- efeito aparece em pelo menos dois targets relacionados, por exemplo `goal_60_70` e `goal_60_75`.

### Para Back Under / Lay Over

Uma regra e PROMISSORA se:

- N >= 40;
- taxa de no-goal >= baseline + 8 p.p.;
- OR > 1.50 para no-goal, ou OR < 0.67 para goal;
- p-value < 0.10;
- interpretacao coerente;
- nao depende de um unico time;
- efeito aparece em `no_goal_60_75` e/ou `no_goal_60_80`.

### OBSERVAR

- N >= 25;
- diff >= 5 p.p.; ou
- OR > 1.25;
- p-value fraco;
- interpretacao coerente.

### DESCARTAR

- efeito fraco;
- N pequeno;
- OR proximo de 1;
- p-value fraco;
- sinal incoerente;
- inferior aos componentes isolados.

---

## 16. Validacoes Obrigatorias

Para cada regra/sinal:

- N;
- positivos;
- negativos;
- taxa;
- baseline do target;
- diff em pontos percentuais;
- odds ratio;
- IC 95%;
- p-value;
- comparacao com componentes isolados;
- concentracao por time;
- classificacao;
- comentario de interpretabilidade.

Para targets de no-goal:

- explicitar que o positivo e ausencia de gol;
- nao misturar diretamente com resultados de target goal sem inversao correta.

---

## 17. Regras Anti-Leakage

Obrigatorio:

1. Features H8 devem usar apenas eventos ate o cutoff.
2. Match State deve usar apenas placar/eventos ate o cutoff.
3. Targets devem usar apenas gols dentro da janela posterior definida.
4. Para entrada aos 60, nenhuma feature pode usar evento apos 60.
5. Para robustez em 65, nenhuma feature pode usar evento apos 65.
6. Proibido usar placar final como feature.
7. Proibido usar estatisticas full-match como feature.
8. Odds pre-jogo podem ser usadas apenas como contexto, nao como odds live.
9. Odds live futuras devem ter timestamp validado.
10. Nao selecionar janela final retroativamente pelo melhor p-value.

---

## 18. Escopo de Execucao Futura V1

A execucao futura, se aprovada, deve avaliar primeiro:

### Bloco A — H8 Hot Signals @60

- `shots_last_10m_high`
- `xg_last_10m_high`
- `momentum_trend_last_10m_positive`
- `momentum_last_10m_avg_high`
- `hot_game_2of4`

Targets:

- `goal_60_70`
- `goal_60_75`
- `goal_60_80`

### Bloco B — H8 Cold Signals @60

- `shots_last_10m_low`
- `xg_last_10m_low`
- `momentum_trend_last_10m_non_positive`
- `momentum_last_10m_avg_low`
- `cold_game_2of4`

Targets:

- `no_goal_60_75`
- `no_goal_60_80`

### Bloco C — Match State Filters

- empate aos 60;
- diferenca de 1 gol;
- diferenca de 2+ gols;
- favorito empatando/perdendo;
- total_goals_until_60 entre 1 e 3.

### Bloco D — Moderadores Secundarios

- `favorite_strength_high`;
- `match_balance_high`;
- `defensive_fragile`;
- `offensive_strong`.

Regra:

- testar Bloco A e B antes de combinacoes complexas;
- so adicionar filtros se sinais H8 simples forem OBSERVAR ou PROMISSOR.

---

## 19. Recomendacao da Proxima Etapa

Proxima etapa recomendada:

```text
H8 SHORT-TERM SIGNAL VALIDATION V1
```

Documento futuro esperado:

```text
docs/04_RESEARCH/H8_SHORT_TERM_SIGNAL_VALIDATION_RESULTS_V1.md
```

Objetivo da execucao futura:

- calcular sinais H8 hot/cold no cutoff 60;
- avaliar targets de janela curta;
- responder se H8 tem mais valor em horizonte curto do que em gol apos 75;
- nao usar odds live;
- nao executar backtesting;
- nao criar modelo.

---

## 20. Decisao Quant

```text
H8_SHORT_TERM_LATE_MARKET_STRATEGY_PLAN APROVADO METODOLOGICAMENTE
```

Escopo V1:

```text
Validacao estatistica de eventos em janelas curtas, com entrada teorica aos 60 minutos.
```

Nao e ainda:

- estrategia lucrativa;
- backtesting;
- modelo;
- producao;
- simulacao de mercado.

Conclusao:

A hipotese e metodologicamente valida e deve ser testada primeiro sem odds live, como sinal de evento. Se houver sinal forte, uma fase futura podera avaliar odds live e viabilidade de mercado.
