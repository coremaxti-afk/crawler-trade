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
  - Commit: `4715562bb6abb0d6bf0a1817b6ecc69cae34ca18`

Documento de validacao de favorito:

- `docs/04_RESEARCH/FOOTBALL_DATA_FAVORITE_VALIDATION_V2.md`
  - Commit: `3323a30bd228c7512f8e1eaf9b3c7bd9ccdb2094`

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

### Resultado Consolidado EPL 2024/25 + EPL 2025/26

#### favorite_winning_by_1 + h8_cold_combo_10m_2of3

2024/25:

- 54 entradas.
- 40 acertos.
- 14 erros.
- 74.1% sem gol 60-75.

2025/26:

- 69 entradas.
- 48 acertos.
- 21 erros.
- 69.6% sem gol 60-75.

Consolidado:

- 123 entradas.
- 88 acertos.
- 35 erros.
- 71.5% sem gol 60-75.
- Erro: 28.5%.

Estimativa operacional com Lay Over @1.50:

- lucro se sem gol: +100.
- perda se gol: -50.
- lucro estimado: +7050.
- ROI estimado: +57.3%.

#### favorite_winning_by_1 + h8_pressure_score_10m_bottom25

2024/25:

- 38 entradas.
- 29 acertos.
- 9 erros.
- 76.3% sem gol 60-75.

2025/26:

- 42 entradas.
- 30 acertos.
- 12 erros.
- 71.4% sem gol 60-75.

Consolidado:

- 80 entradas.
- 59 acertos.
- 21 erros.
- 73.8% sem gol 60-75.
- Erro: 26.2%.

Estimativa operacional com Lay Over @1.50:

- lucro estimado: +4850.
- ROI estimado: +60.6%.

Interpretação PM:

- As duas estrategias mostram consistencia exploratoria na Premier League.
- `h8_cold_combo_10m_2of3` tem maior amostra: N=123, acerto 71.5%.
- `h8_pressure_score_10m_bottom25` tem melhor taxa: N=80, acerto 73.8%.

Ressalvas:

- odds de entrada do mercado Proximo Gol ainda sao medias observadas/manualizadas;
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

Documento criado:

- `docs/04_RESEARCH/SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1.md`

Status:

```text
ABERTA COMO PLANO METODOLOGICO EXPLORATORIO
```

Objetivo:

Usar dados SportMonks ja coletados para descobrir novas estrategias e combos por lado/time, explorando tendencias minuto a minuto por `participant_id`.

Motivo:

SportMonks permite investigar algo que o SofaScore antigo nao entregava bem:

```text
pressao por time
```

Grupos de combos candidatos:

- time perdendo pressionando;
- favorito perdendo pressionando;
- favorito vencendo e adversario pressionando;
- mandante vencendo por 1 e visitante pressionando;
- time vencendo por 1 mas esfriando;
- time perdendo por 1 com dangerous attacks subindo;
- key passes ultimos 10 minutos;
- big chances ultimos 10 minutos;
- shots on target ultimos 10 minutos;
- corners/dangerous attacks em aceleracao.

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
4. Definir pacote oficial minimo H8 SportMonks para escala.
5. Autorizar, se aprovado, descoberta controlada `SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1`.
6. Manter API-Football em discovery complementar.
7. Manter SofaScore como backup/especialista para graph/shotmap.

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
- Autorizar discovery controlado `SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1`.

Se NAO:

- SportMonks permanece complemento.
- SofaScore shotmap/graph continuam essenciais.
- Buscar fonte alternativa para pressao minuto/time.
