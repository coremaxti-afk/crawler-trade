# SportMonks EPL 2025/26 Validation and SofaScore Comparison

Status: AUDITORIA CONCLUIDA

Data: 2026-06-12

Escopo: validar a coleta bruta SportMonks da Premier League 2025/26 e comparar conceitualmente com os dados SofaScore ja documentados para H8.

Restricoes respeitadas: nao foi criado importer, schema, banco, dataset analitico, feature builder, modelo, baseline ou backtesting. A auditoria leu apenas JSONs ja coletados.

## Fontes auditadas

SportMonks EPL 2025/26:

```text
C:/LateGoalResearch/data/raw/sportmonks/full_collection/england_premier_league_league_8_season_25583_2025_2026
```

Matriz CSV:

```text
data/processed/reports/sportmonks_epl_2025_26_endpoint_quality_matrix.csv
```

Referencias SofaScore locais usadas:

```text
docs/03_SOURCES/SOFASCORE/GRAPH_MOMENTUM_ENDPOINT.md
docs/03_SOURCES/SOFASCORE/ENDPOINT_DISCOVERY_20260605.md
```

## Sumario executivo

A coleta SportMonks EPL 2025/26 esta completa para o pacote H8 coletado: 380 fixtures esperadas e 380 JSONs validos em cada uma das 8 categorias presentes.

A categoria mais valiosa e `trends`, com 109.087 MB no total e granularidade minuto/time para ataques, dangerous attacks, posse, chutes, escanteios, passes e outras estatisticas. `timeline` tambem tem alto valor porque oferece eventos objetivos por minuto, sobretudo chutes, escanteios, impedimentos e woodwork.

Decisao: SportMonks pode substituir parcialmente o SofaScore para H8. Ele reduz muito a dependencia do SofaScore para pressao quantitativa por time e estatisticas minuto a minuto, mas nao substitui completamente `graph` nem `shotmap`, porque SofaScore ainda entrega momentum proprietario simplificado e shot-level data com coordenadas/xG/xGOT por finalizacao.

## Cobertura SportMonks EPL 2025/26

Fixtures esperadas: 380

| Categoria | Cobertura | Valid JSON | Vazios | Erros | Total MB | Avg KB | Temporal | H8 | Risco | Decisao |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| base | 100.0% | 380/380 | 0 | 0 | 0.416 | 1.12 | timestamp | BAIXO VALOR | BAIXO | optional if API-Football covers base |
| identity | 100.0% | 380/380 | 0 | 0 | 0.927 | 2.50 | timestamp | BAIXO VALOR | BAIXO | optional |
| match_state | 100.0% | 380/380 | 0 | 0 | 4.175 | 11.25 | minute+timestamp | MEDIO VALOR | MEDIO | keep optional/validation |
| timeline | 100.0% | 380/380 | 0 | 0 | 8.409 | 22.66 | minute+timestamp | ALTO VALOR | MEDIO | mandatory for H8 validation |
| statistics | 100.0% | 380/380 | 0 | 0 | 8.084 | 21.78 | timestamp | MEDIO VALOR | ALTO | optional; avoid cutoff features |
| commentaries | 100.0% | 380/380 | 0 | 0 | 8.208 | 22.12 | minute | MEDIO VALOR | MEDIO | optional enrichment |
| trends | 100.0% | 380/380 | 0 | 0 | 109.087 | 293.96 | minute+timestamp | ALTO VALOR | MEDIO | mandatory SportMonks H8 core |
| xgfixture | 100.0% | 380/380 | 0 | 0 | 4.634 | 12.49 | timestamp | MEDIO VALOR | ALTO | optional context; leakage if used before FT |
| matchfacts | 0.0% | 0/380 | 0 | 0 | 0.000 | 0.00 | none | BAIXO VALOR | BAIXO | discard for H8 cutoff core |
| lineups | 0.0% | 0/380 | 0 | 0 | 0.000 | 0.00 | none | BAIXO VALOR | BAIXO | optional non-H8 context |

Observacao: `matchfacts` e `lineups` aparecem como 0/380 nesta auditoria porque nao fazem parte do pacote H8 coletado nesta pasta. Isso nao indica erro da API; indica apenas que estes endpoints nao foram coletados nesta rodada EPL 25/26 H8.

## Campos principais observados

### trends

Top tipos observados:

```text
Passes, Successful Passes, Attacks, Ball Possession %, Long Passes, Successful Long Passes Percentage, Duels Won, Successful Passes Percentage, Dangerous Attacks, Successful Long Passes
```

Resumo: `trends` possui `minute`, `participant_id`, `period_id`, `value` e `type`, permitindo leitura por time e por minuto. E a melhor fonte SportMonks para pressoes/cutoffs.

### timeline

Top tipos observados:

```text
Shot Off Target, Corner, Shot On Target, Offside, Woodwork
```

Resumo: `timeline` tem eventos objetivos por minuto. Ele nao substitui totalmente shotmap porque nao traz coordenadas/xG por chute, mas valida chutes, corners e offside no tempo.

### statistics

Top tipos observados:

```text
Corners, Shots Off Target, Shots Total, Attacks, Dangerous Attacks, Ball Possession %, Ball Safe, Shots Insidebox, Shots Outsidebox, Goal Kicks
```

Resumo: `statistics` e majoritariamente agregado final por time. Alto risco de leakage se usado como feature em cutoffs 60/65/70/75 sem garantia de snapshot temporal.

### commentaries

Campos principais:

```text
[].id, [].fixture_id, [].comment, [].minute, [].extra_minute, [].is_goal, [].is_important, [].order
```

Resumo: narrativa minuto a minuto. Util para enriquecer eventos e revisar lances, mas exige parsing textual se virar feature no futuro.

### xgfixture

Resumo: xG agregado por fixture/time. Na coleta atual esta sem `type` expandido; em discovery pontual, `xgfixture.type` mostrou Expected Goals, xGoT, xPTS, npxG, xG open play, set play, corners e free kicks. Nao e xG temporal/shot-level.

## Valor para H8

Dados que permitem features por cutoff 60/65/70/75:

- `trends`: permite cutoffs reais por minuto, desde que filtrado por `minute <= cutoff`.
- `timeline`: permite contagem de eventos ate cutoff, como chutes, corners, offside e woodwork.
- `commentaries`: permite leitura textual ate cutoff, mas exige cuidado operacional/parsing.
- `match_state`: permite gols/cartoes/substituicoes ate cutoff.

Nao usar diretamente para cutoff sem snapshot temporal:

- `statistics`: agregado final.
- `xgfixture`: agregado final.
- `base`/`identity`: contexto, nao dinamica.

## Comparacao com SofaScore

### SportMonks trends vs SofaScore graph

- SportMonks substitui? Parcialmente.
- SportMonks complementa? Sim, muito.
- SofaScore entrega algo unico? Sim, `graphPoints` com momentum proprietario simples por minuto.
- Melhor para H8: SportMonks para features explicaveis por time; SofaScore para momentum sintetico pronto.
- Prioridade: SportMonks `trends` como fonte primaria; SofaScore `graph` como comparador/backup opcional.

### SportMonks timeline/events vs SofaScore incidents

- SportMonks substitui? Parcialmente.
- SportMonks complementa? Sim.
- Melhor para H8: SportMonks `timeline` para chutes/corners/offside; incidents para validacao de gols/cartoes/substituicoes.
- Prioridade: SportMonks para coleta ampla; SofaScore incidents opcional.

### SportMonks timeline/events vs SofaScore shotmap

- SportMonks substitui? Nao completamente.
- SofaScore unico? Sim: shot-level com coordenadas, xG, xGOT e timeSeconds.
- Prioridade: manter SofaScore shotmap se o objetivo incluir xG temporal/shot quality.

### SportMonks xgfixture vs SofaScore shotmap xG/xGOT

- SportMonks substitui? Nao para xG temporal.
- SportMonks complementa? Sim, como xG agregado e splits de contexto quando `xgfixture.type` e usado.
- Melhor para H8: SofaScore shotmap para cutoffs; SportMonks xgfixture para pos-jogo/contexto agregado.

## Decisao sobre dependencia do SofaScore

Classificacao: PARCIALMENTE.

SportMonks pode reduzir fortemente a dependencia do SofaScore para H8 porque entrega `trends` com pressao numerica por time/minuto e alta cobertura operacional. Isso cobre uma lacuna importante do SofaScore: ataques, dangerous attacks e posse minuto a minuto nao foram confirmados como endpoints publicos simples no SofaScore.

O que perderiamos parando SofaScore:

- `graph` momentum proprietario minuto a minuto.
- `shotmap` com shot-level, coordenadas, xG, xGOT e timeSeconds.
- `average-positions` e alguns detalhes contextuais especificos.

O que ganhamos com SportMonks:

- API oficial/documentada, mais estavel operacionalmente.
- 100% de cobertura na EPL 25/26 para o pacote coletado.
- `trends` minuto a minuto por time com attacks/dangerous_attacks/posse/chutes.
- Menor risco de bloqueio operacional que SofaScore.

SofaScore ainda vale a dificuldade operacional?

Sim, mas como fonte opcional/backup ou fonte especializada para `graph` e `shotmap`, nao como dependencia primaria para todos os jogos.

## Recomendacao final

### Endpoints SportMonks obrigatorios

- `trends`: core H8 para pressao, ataques, dangerous attacks, posse e chutes por minuto/time.
- `timeline`: validacao objetiva de chutes/corners/offside por minuto.
- `match_state`: gols, cartoes, substituicoes, scores e periods.
- `base`/`identity`: contexto e chaves de join quando nao coberto por outra fonte.

### Endpoints SportMonks opcionais

- `commentaries`: enriquecimento textual e auditoria de lances.
- `xgfixture`: contexto agregado de xG, xGoT e xPTS, sem uso direto em cutoffs.
- `statistics`: agregados finais para analise pos-jogo/QA, nao para cutoff sem snapshot.

### Endpoints SportMonks descartaveis para H8 cutoff core

- `matchfacts`: historico/pre-match; baixo valor para momentum intra-jogo.
- `lineups`: util como contexto, mas nao parte do H8 minuto a minuto.
- `odds/premiumOdds`: pre-match/historico de odds; nao substitui live odds minuto a minuto.
- `predictions`: sem acesso atual e, mesmo com acesso, seria output/modelo de terceiro, nao dado bruto.

### Recomendacao sobre SofaScore

Manter SofaScore como fonte opcional/backup, nao como dependencia primaria. Priorizar SportMonks para coleta massiva H8 e manter SofaScore somente para:

- `graph`, se quisermos comparar momentum proprietario;
- `shotmap`, se quisermos xG/xGOT temporal por chute e coordenadas;
- amostras controladas de QA/benchmark.

## Proximo agente recomendado

Quant Research com escopo de validacao semantica.

Objetivo do proximo agente: validar semanticamente `trends` em amostra de jogos, checar se os valores sao acumulados ou estado por minuto, e definir regras de leitura seguras para cutoffs 60/65/70/75 sem criar features ainda.
