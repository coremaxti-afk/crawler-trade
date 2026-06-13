# PROJECT STATUS

## Estado Atual da Base

- SofaScore EPL 2024/25: 381 partidas no inventario; 380 partidas importaveis.
- `matches_master`: 380 partidas.
- `match_statistics`: 380 partidas.
- `match_incidents`: 7647 registros.
- `match_graph`: 34861 pontos em 379 partidas.
- `match_shotmap`: 9883 finalizacoes em 380 partidas.
- Football-Data EPL 2024/25: 380 staging rows, 380 mappings e 34280 odds importadas localmente.
- SportMonks EPL 2025/26: 380 fixtures auditadas no pacote H8 coletado.
- H8 Composite Pressure Score V1: 1520 linhas match_id + cutoff, 5040 resultados disponiveis.

---

## Objetivo Atual do Projeto

O objetivo vigente nao e apenas prever se havera gol tardio.

O projeto deve responder se existe uma operacao de trade esportivo com:

- criterio de entrada;
- criterio de saida;
- comparacao hold vs cashout;
- leitura dinamica de jogo quente/frio;
- lucro/prejuizo por odd;
- separacao entre taxa estatistica, EV teorico, EV com cashout e operacionalidade real.

Documento de referencia:

- `docs/01_CONTEXT/PROJECT_OBJECTIVE_TRADE_INSIGHTS.md`

Restricoes permanentes:

- Nao autoriza producao.
- Nao autoriza robo.
- Nao autoriza trade real.
- Nao autoriza automacao operacional.
- Nao autoriza modelo/baseline novo sem aprovacao.
- Nao autoriza backtesting financeiro real com odds live nao timestampadas.
- Nao autoriza features com leakage, target-derived ou pos-cutoff.

---

## Frentes de Fonte de Dados

### SofaScore EPL 2024/25

- Fonte historica principal inicial.
- Continua valiosa para `graph` e `shotmap`.
- `graph`: momentum proprietario minuto a minuto.
- `shotmap`: shot-level com coordenadas, xG, xGOT e `timeSeconds`.
- Limite: coleta operacional dificil/fragil e H8 V1 mede pressao agregada da partida, nao pressao por time.
- Decisao atual: manter como fonte especializada/backup para `graph` e `shotmap`.

### API-Football

Documento principal:

- `docs/03_SOURCES/API_FOOTBALL/FIXTURE_1545540_SPIKE.md`

Estado:

- Spike exploratorio em fixture `1545540`.
- Retornou fixture, events, lineups, odds, predictions e head-to-head.
- Estatisticas in-game robustas nao foram confirmadas.
- Odds live para fixture finalizada vieram vazias.
- Decisao: complemento candidato, nao fonte oficial H8 sem novo discovery em fixture EPL/plano Pro.

### SportMonks H8

Documento principal:

- `docs/03_SOURCES/SPORTMONKS/SPORTMONKS_EPL_2025_26_VALIDATION_AND_SOFASCORE_COMPARISON.md`

Matriz:

- `data/processed/reports/sportmonks_epl_2025_26_endpoint_quality_matrix.csv`

Estado:

- Premier League 2025/26 auditada.
- 380 fixtures esperadas.
- 380 JSONs validos em cada uma das 8 categorias coletadas.
- Categorias auditadas: `base`, `identity`, `match_state`, `timeline`, `statistics`, `commentaries`, `trends`, `xgfixture`.
- `trends`: granularidade minuto/time, principal fonte candidata para pressao H8 por time.
- `timeline`: eventos objetivos por minuto.
- `xgfixture` e `statistics`: agregados finais; nao usar diretamente em cutoffs sem snapshot temporal.

Decisao atual:

- SportMonks e fonte primaria candidata para H8 por time em escala.
- SportMonks substitui parcialmente SofaScore para pressao quantitativa por minuto/time.
- SofaScore permanece como fonte especializada/backup para `graph` e `shotmap`.

Pendencia antes de feature engineering:

- Validar semanticamente `trends`.
- Confirmar se valores de `trends` sao acumulados, incrementais ou snapshots por minuto.
- Confirmar regra segura para cutoffs 60/65/70/75.

### SportMonks Premium Odds Diagnostic

Documento principal:

- `docs/03_SOURCES/SPORTMONKS/SPORTMONKS_PREMIUM_ODDS_EMPTY_PAYLOAD_DIAGNOSTIC_V1.md`

Estado:

- 380/380 payloads `premium_odds.json` retornaram `data: []`.
- Odds 1X2 pre-jogo utilizaveis: 0.
- Decisao: `CORRIGIR_ENDPOINT`.
- Para odds 1X2 pre-jogo, testar primeiro Standard Odds pre-match: `/v3/football/odds/pre-match/fixtures/{ID}` com `filters=markets:1`.
- Premium Historical Odds deve ser testado apenas em spike controlado.

---

## Operacional Trade Research

Documento principal:

- `docs/04_RESEARCH/OPERACIONAL_TRADE_TOP_STRATEGIES_V1.md`

Documento de validacao de favorito:

- `docs/04_RESEARCH/FOOTBALL_DATA_FAVORITE_VALIDATION_V2.md`

### Decisao da frente favorite_winning_by_1 + jogo frio

Status:

```text
APROVADO COM RESSALVAS PARA PESQUISA OPERACIONAL
```

Definicao operacional aprovada para comparacao historica:

```text
favorite_side = menor odd pre-jogo 1X2
```

Nao usar como regra principal nesta comparacao historica:

```text
favorite_odd <= 1.70
```

Motivo:

O corte `<= 1.70` reduziu excessivamente a amostra da EPL 2025/26:

- `h8_cold_combo_10m_2of3`: N=15.
- `h8_pressure_score_10m_bottom25`: N=8.

### Correcao de ROI operacional

Erro identificado:

O lucro anterior foi interpretado como se cada acerto gerasse lucro cheio de stake:

```text
Acerto = +100
Erro = -50
```

Essa leitura corresponde a uma simulacao de HOLD/liquidacao completa, nao a uma operacao com entrada aos 60 e saida/cashout fixo aos 75.

Correcao para janela 60-75:

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

### Resultado Consolidado EPL 2024/25 + EPL 2025/26

#### favorite_winning_by_1 + h8_cold_combo_10m_2of3

- 123 entradas.
- 88 acertos.
- 35 erros.
- 71.5% sem gol 60-75.
- 28.5% com gol 60-75.
- Lucro corrigido saida fixa 75: +450.
- ROI corrigido saida fixa 75: +3.7%.

#### favorite_winning_by_1 + h8_pressure_score_10m_bottom25

- 80 entradas.
- 59 acertos.
- 21 erros.
- 73.8% sem gol 60-75.
- 26.2% com gol 60-75.
- Lucro corrigido saida fixa 75: +425.
- ROI corrigido saida fixa 75: +5.3%.

Interpretacao PM:

- As estrategias seguem consistentes estatisticamente para prever ausencia de gol entre 60 e 75.
- O lucro operacional com cashout fixo aos 75 e baixo.
- Lay Over / Under frio so tende a ter lucro relevante se usado em formato HOLD, segurando mais tempo ou ate liquidacao relevante.
- Para operacoes de janela curta, a pesquisa deve buscar estrategias Over em que o gol dentro da janela gere lucro cheio.

Ressalvas:

- odds de entrada/saida ainda sao medias observadas/manualizadas;
- nao ha odds live reais por timestamp;
- validacao ainda e Premier League apenas;
- precisa replicacao multi-liga;
- resultado e pesquisa operacional, nao execucao real.

Nao autoriza:

- robo;
- producao;
- trade real;
- automacao operacional;
- backtesting financeiro real.

---

## Nova Frente Oficial

Documento:

- `docs/04_RESEARCH/SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1.md`

Status:

```text
ABERTA COMO PLANO METODOLOGICO EXPLORATORIO
```

Nova direcao:

A proxima frente SportMonks deve ser dividida em duas familias:

### 1. UNDER_HOLD

Objetivo:

Encontrar cenarios com alta probabilidade de nao sair gol ate o fim ou ate janela mais longa.

Exemplos:

- jogo muito frio aos 60;
- favorito vencendo por 1 e jogo esfriando;
- baixa finalizacao;
- baixa pressao;
- poucos dangerous attacks;
- ausencia de big chances;
- ausencia de shots on target.

Meta:

- buscar taxa de acerto 70%+ para segurar ate 80/90 ou ate liquidacao relevante.

### 2. OVER_JANELA_CURTA

Objetivo:

Encontrar cenarios com alta probabilidade de gol entre 60-75, 65-80 ou 70-85.

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

- encontrar operacoes com retorno relevante em janela curta, onde o gol dentro da janela gere lucro cheio.

Restricoes da nova frente:

- nao criar modelo;
- nao criar baseline;
- nao criar robo;
- nao criar producao;
- nao fazer backtesting financeiro real;
- usar apenas dados SportMonks ja coletados;
- preservar anti-leakage por cutoff;
- separar descoberta estatistica de operacionalizacao.

Agente recomendado:

- Quant Research / Data Science ou Data QA / Research Agent.
- Codex apenas para execucao tecnica apos escopo fechado.

---

## Estado dos Agentes

Estado oficial:

- Estrutura antiga permanece vigente.
- Nenhuma reorganizacao oficial foi aplicada.

---

## Sprint / Prioridades Atuais

Prioridades imediatas:

1. Validar semanticamente SportMonks `trends`.
2. Confirmar se `trends` representa acumulado, incremental ou snapshot por minuto.
3. Definir whitelist V1 de indicadores por time.
4. Separar candidatos `UNDER_HOLD` e `OVER_JANELA_CURTA`.
5. Definir pacote oficial minimo H8 SportMonks para escala.
6. Autorizar, se aprovado, descoberta controlada `SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1`.
7. Manter API-Football em discovery complementar.
8. Manter SofaScore como backup/especialista para graph/shotmap.

Bloqueios:

- Nao criar importer SportMonks ainda.
- Nao alterar schema/banco ainda.
- Nao criar feature builder definitivo ainda.
- Nao iniciar modelo/baseline/backtesting com SportMonks antes da validacao semantica.
- Nao escalar para multiplas ligas/temporadas sem pacote oficial minimo aprovado.
- Nao tratar odds medias observadas como odds live reais.

---

## Proxima Decisao PM

A proxima decisao critica e:

```text
SportMonks `trends` pode ser usado com seguranca para cutoffs 60/65/70/75 e para pressao por time?
```

Se SIM:

- SportMonks passa a ser fonte primaria candidata para H8 por time.
- Autorizar discovery controlado `SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1`, separado em `UNDER_HOLD` e `OVER_JANELA_CURTA`.

Se NAO:

- SportMonks permanece complemento.
- SofaScore shotmap/graph continuam essenciais.
- Buscar fonte alternativa para pressao minuto/time.
