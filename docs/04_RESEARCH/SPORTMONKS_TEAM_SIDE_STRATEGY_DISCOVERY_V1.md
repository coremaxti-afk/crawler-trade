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

## Correcao Metodologica Importante

A frente `favorite_winning_by_1 + jogo frio` continua estatisticamente consistente para prever ausencia de gol entre 60 e 75.

Porem, foi identificado erro de interpretacao no calculo de lucro operacional.

O calculo anterior interpretava cada acerto como lucro cheio de stake:

```text
Acerto = +100
Erro = -50
```

Essa leitura corresponde a uma simulacao de hold/segurar a posicao ate liquidacao completa do mercado, nao a uma operacao com entrada aos 60 e saida/cashout fixo aos 75.

Para operacao real com entrada aos 60 e saida aos 75 usando curva media:

```text
Lay Over 60' @1.50
Back Over fechamento 75' @2.00
Stake = 100
```

Resultado aproximado:

```text
Acerto sem gol ate 75 = +25
Erro com gol antes de 75 = -50
```

Portanto, o lucro correto para saida fixa aos 75 e muito menor.

---

## Resultado Estatistico Consolidado EPL 2024/25 + EPL 2025/26

### 1. favorite_winning_by_1 + h8_cold_combo_10m_2of3

- 123 entradas
- 88 acertos
- 35 erros
- 71.5% sem gol 60-75
- 28.5% com gol 60-75

Calculo corrigido com saida fixa aos 75:

```text
88 * 25 - 35 * 50 = +450
```

Resultado:

- lucro final estimado: +450
- ROI estimado: +3.7%

### 2. favorite_winning_by_1 + h8_pressure_score_10m_bottom25

- 80 entradas
- 59 acertos
- 21 erros
- 73.8% sem gol 60-75
- 26.2% com gol 60-75

Calculo corrigido com saida fixa aos 75:

```text
59 * 25 - 21 * 50 = +425
```

Resultado:

- lucro final estimado: +425
- ROI estimado: +5.3%

---

## Interpretacao PM

As estrategias seguem validas como sinal estatistico de jogo frio/no-goal entre 60 e 75.

Mas a operacao de janela curta 60-75 com cashout fixo aos 75 gera lucro operacional baixo.

Conclusao:

- Lay Over / Under frio pode ser forte em formato HOLD ou janela mais longa.
- Lay Over / Under frio fica menos atrativo para cashout fixo curto 60-75.
- Para janela curta, e necessario buscar tambem estrategias Over, onde o gol dentro da janela gere lucro cheio.

---

## Decisao PM Atualizada

A frente `favorite_winning_by_1 + jogo frio` esta:

```text
APROVADA COM RESSALVAS PARA PESQUISA OPERACIONAL
```

Mas com a seguinte correcao:

```text
ROI alto anterior = simulacao tipo HOLD / liquidacao completa
ROI corrigido 60-75 com cashout fixo = baixo
```

Nao autoriza:

- robo;
- producao;
- trade real;
- automacao operacional;
- backtesting financeiro real.

Ressalvas:

- odds de entrada/saida ainda sao medias observadas/manualizadas;
- nao ha odds live reais por timestamp;
- validacao ainda e Premier League apenas;
- precisa replicacao multi-liga;
- resultado e pesquisa operacional, nao execucao real.

---

## Nova Direcao da Frente SportMonks

A proxima frente SportMonks deve ser dividida em duas familias.

---

## Familia 1 - Under / Lay Over de HOLD

Objetivo:

Encontrar cenarios com alta probabilidade de nao sair gol ate o fim ou ate janela mais longa.

Exemplos:

- jogo muito frio aos 60;
- favorito vencendo por 1 e jogo esfriando;
- baixa finalizacao;
- baixa pressao;
- poucos dangerous attacks;
- ausencia de big chances;
- ausencia de shots on target;
- time vencendo por 1 sem sofrer pressao real;
- adversario sem aceleracao ofensiva.

Meta:

```text
Buscar taxa de acerto 70%+ para segurar ate 80/90 ou ate liquidacao relevante.
```

Leitura operacional:

Esta familia so faz sentido se o protocolo permitir capturar mais valor do decaimento da odd do que o cashout curto 60-75.

---

## Familia 2 - Over de Janela Curta

Objetivo:

Encontrar cenarios com alta probabilidade de gol em janelas curtas:

- 60-75;
- 65-80;
- 70-85.

Exemplos:

- time perdendo pressionando;
- favorito perdendo pressionando;
- underdog vencendo e favorito pressionando;
- visitante pressionando mandante que vence por 1;
- dangerous attacks em aceleracao;
- shots on target recentes;
- big chances recentes;
- key passes recentes;
- escanteios e pressao territorial aumentando.

Meta:

```text
Encontrar operacoes com retorno relevante em janela curta, onde o gol dentro da janela gere lucro cheio.
```

---

## Objetivo do Discovery SportMonks

Usar dados SportMonks ja coletados para descobrir novas estrategias e combos por lado/time, explorando tendencias minuto a minuto por `participant_id`.

Motivo:

SportMonks permite investigar algo que o SofaScore antigo nao entregava bem:

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

## Indicadores SportMonks Candidatos

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

### Under / Lay Over HOLD

- sem gol 60-80
- sem gol 60-90
- sem gol 65-80
- sem gol 65-90
- sem gol 70-85
- sem gol 70-90

### Over Janela Curta

- gol 60-75
- gol 65-80
- gol 70-85
- gol apos cutoff em janela curta definida

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

- familia: UNDER_HOLD ou OVER_JANELA_CURTA;
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
4. Separar explicitamente candidatos UNDER_HOLD e OVER_JANELA_CURTA.
5. Somente depois autorizar Codex a executar descoberta controlada.
