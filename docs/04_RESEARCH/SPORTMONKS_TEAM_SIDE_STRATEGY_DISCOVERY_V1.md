# SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1

## Status

Plano metodologico exploratorio.

Nao contem codigo.
Nao contem dataset.
Nao contem modelo.
Nao contem baseline.
Nao contem backtesting financeiro real.
Nao autoriza robo, producao, trade real ou automacao operacional.

---

## Contexto

A avaliacao consolidada das estrategias `favorite_winning_by_1 + jogo frio` foi concluida para Premier League 2024/25 + 2025/26.

A definicao operacional aprovada para compatibilidade historica foi:

```text
favorite_side = menor odd pre-jogo 1X2
```

Nao usar, nesta comparacao historica, cutoff rigido de odd como regra principal:

```text
favorite_odd <= 1.70
```

Motivo:

O corte `<= 1.70` reduziu excessivamente a amostra da EPL 2025/26:

- `h8_cold_combo_10m_2of3`: N=15
- `h8_pressure_score_10m_bottom25`: N=8

Portanto, para comparacao historica, a regra correta e:

```text
menor odd = favorito
```

---

## Resultado Consolidado EPL 2024/25 + EPL 2025/26

### 1. favorite_winning_by_1 + h8_cold_combo_10m_2of3

2024/25:

- 54 entradas
- 40 acertos
- 14 erros
- 74.1% sem gol 60-75

2025/26:

- 69 entradas
- 48 acertos
- 21 erros
- 69.6% sem gol 60-75

Consolidado:

- 123 entradas
- 88 acertos
- 35 erros
- 71.5% sem gol 60-75
- erro: 28.5%

Estimativa operacional com Lay Over @1.50:

- lucro se sem gol: +100
- perda se gol: -50
- lucro estimado: +7050
- ROI estimado: +57.3%

### 2. favorite_winning_by_1 + h8_pressure_score_10m_bottom25

2024/25:

- 38 entradas
- 29 acertos
- 9 erros
- 76.3% sem gol 60-75

2025/26:

- 42 entradas
- 30 acertos
- 12 erros
- 71.4% sem gol 60-75

Consolidado:

- 80 entradas
- 59 acertos
- 21 erros
- 73.8% sem gol 60-75
- erro: 26.2%

Estimativa operacional com Lay Over @1.50:

- lucro estimado: +4850
- ROI estimado: +60.6%

---

## Decisao PM

A frente `favorite_winning_by_1 + jogo frio` esta:

```text
APROVADA COM RESSALVAS PARA PESQUISA OPERACIONAL
```

Interpretacao:

- As duas estrategias mostram consistencia exploratoria na Premier League.
- `h8_cold_combo_10m_2of3` tem maior amostra: N=123, acerto 71.5%.
- `h8_pressure_score_10m_bottom25` tem melhor taxa: N=80, acerto 73.8%.

Nao autoriza:

- robo;
- producao;
- trade real;
- automacao operacional;
- backtesting financeiro real.

Ressalvas:

- odds de entrada do mercado Proximo Gol ainda sao medias observadas/manualizadas;
- nao ha odds live reais por timestamp;
- validacao ainda e Premier League apenas;
- precisa replicacao multi-liga;
- resultado e pesquisa operacional, nao execucao real.

Documentos relacionados:

- `docs/04_RESEARCH/OPERACIONAL_TRADE_TOP_STRATEGIES_V1.md`
  - Commit: `4715562bb6abb0d6bf0a1817b6ecc69cae34ca18`
- `docs/04_RESEARCH/FOOTBALL_DATA_FAVORITE_VALIDATION_V2.md`
  - Commit: `3323a30bd228c7512f8e1eaf9b3c7bd9ccdb2094`

---

## Proxima Frente Oficial

```text
SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1
```

Objetivo:

Usar dados SportMonks ja coletados para descobrir novas estrategias e combos por lado/time, explorando tendencias minuto a minuto por `participant_id`.

Motivo:

SportMonks permite algo que o SofaScore antigo nao entregava bem:

```text
pressao por time
```

Isso pode transformar H8 de leitura agregada da partida em leitura direcional:

- quem esta pressionando;
- quem esta esfriando;
- se o favorito esta pressionando;
- se o underdog esta pressionando;
- se o time perdendo esta pressionando;
- se o time vencendo por 1 esta sofrendo pressao.

---

## Hipoteses e Combos Candidatos

Explorar, de forma controlada e sem p-hacking livre, os seguintes grupos:

### Pressao do time perdendo

- time perdendo pressionando;
- time perdendo por 1 com dangerous attacks subindo;
- time perdendo por 1 com key passes subindo;
- time perdendo por 1 com shots on target recentes.

### Pressao do favorito

- favorito perdendo pressionando;
- favorito empatando e pressionando;
- favorito vencendo mas adversario pressionando;
- favorito vencendo por 1 e esfriando.

### Pressao do underdog

- underdog vencendo por 1 e sendo pressionado;
- underdog vencendo por 1 e mantendo pressao;
- underdog perdendo e pressionando.

### Match state + team-side pressure

- mandante vencendo por 1 e visitante pressionando;
- visitante vencendo por 1 e mandante pressionando;
- time vencendo por 1 mas esfriando;
- time vencendo por 1 sofrendo dangerous attacks crescentes;
- empate com um lado dominando pressao.

### Indicadores SportMonks candidatos

- attacks ultimos 10 minutos;
- dangerous attacks ultimos 10 minutos;
- shots ultimos 10 minutos;
- shots on target ultimos 10 minutos;
- corners ultimos 10 minutos;
- key passes ultimos 10 minutos, se disponivel;
- big chances ultimos 10 minutos, se disponivel;
- posse/territorio por minuto, se semanticamente seguro;
- aceleracao de dangerous attacks;
- aceleracao de shots/corners;
- queda de pressao do time vencendo.

---

## Escopo V1

Cutoffs candidatos:

- 60
- 65
- 70
- 75

Janelas candidatas:

- 5 minutos
- 10 minutos
- 15 minutos

Targets exploratorios:

- sem gol 60-75
- gol 60-75
- sem gol 65-80
- gol 65-80
- sem gol 70-85
- gol 70-85
- gol apos cutoff
- no_goal_after_cutoff

Mercados teoricos:

- Lay Over em jogo frio/dominado pelo time vencendo;
- Back Over quando o time perdendo/favorito pressionar;
- no-goal window quando jogo esfriar por lado;
- goal window quando pressao direcional aumentar.

---

## Regras Anti-Leakage

Obrigatorio:

- usar apenas dados com `minute <= cutoff`;
- nao usar estatisticas finais como features de cutoff;
- nao usar `xgfixture` como feature de cutoff, pois e agregado final;
- nao usar placar final como feature;
- nao usar gols futuros como feature;
- nao usar target-derived columns;
- separar target de features;
- preservar grain auditavel por `match_id + cutoff + strategy_candidate`.

SportMonks `trends` deve ser validado semanticamente antes de feature definitiva:

- acumulado;
- incremental;
- snapshot por minuto.

Se a semantica nao for confirmada, o campo deve ficar como `NAO_USAR_V1`.

---

## Resultado Esperado

Produzir documento futuro:

```text
docs/04_RESEARCH/SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V1.md
```

O resultado deve reportar, por padrao/estrategia candidata:

- N;
- wins;
- losses;
- taxa;
- baseline do target;
- diff em pontos percentuais;
- odds ratio;
- p-value quando aplicavel;
- classificacao estatistica;
- leitura operacional;
- se depende de odds/cashout;
- se e candidata a replicacao multi-liga.

Classificacoes sugeridas:

- PROMISSOR_LOCAL;
- MICRO_AMOSTRA_REPLICAR;
- REPLICACAO_MULTI_LIGA;
- OBSERVAR;
- DESCARTAR_ESTATISTICO_LOCAL;
- NAO_DISPONIVEL_V1.

---

## Agente Recomendado

Agente primario:

- Quant Research / Data Science.

Apoio:

- Data Acquisition para interpretacao da estrutura SportMonks.
- Codex apenas para execucao tecnica apos escopo fechado.

---

## Restrições

Nao criar:

- modelo;
- baseline;
- robo;
- producao;
- automacao operacional;
- backtesting financeiro real;
- importer;
- schema;
- feature builder definitivo.

Nao usar:

- dados pos-cutoff;
- odds live inexistentes;
- `xgfixture` como snapshot temporal;
- estatisticas agregadas finais como se fossem dados in-game.

---

## Proxima Acao

Antes de executar discovery amplo:

1. Validar semantica de SportMonks `trends`.
2. Confirmar quais tipos de `trends` sao seguros para janelas 5/10/15 minutos.
3. Definir whitelist V1 de indicadores por time.
4. Somente depois autorizar Codex a executar descoberta controlada.
