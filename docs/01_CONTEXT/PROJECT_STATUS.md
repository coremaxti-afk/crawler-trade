# PROJECT STATUS

## Estado Atual da Base

- Inventory SofaScore EPL 2024/25: 381 partidas.
- Partidas importaveis: 380.
- Partida descartada da importacao atual: `12436452`.
- `matches_master`: 380 partidas.
- `match_statistics`: 380 partidas.
- `match_incidents`: 7647 registros.
- `match_graph`: 34861 pontos em 379 partidas.
- `match_shotmap`: 9883 finalizacoes em 380 partidas.
- `match_source_status`: 760 registros.
- Football-Data EPL 2024/25: 380 staging rows, 380 mappings e 34280 odds importadas localmente.
- Odds Features V1: 380 linhas, 380 partidas unicas, status APTO.
- Dataset Odds V1: 380 linhas, 380 partidas unicas, target unido explicitamente, status APTO COM RESSALVAS.
- H8 Composite Pressure Score V1: 1520 linhas match_id + cutoff, 5040 resultados disponiveis, status exploratorio concluido.

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

## SofaScore EPL 2024/25

Estado:

- Fonte historica principal inicial para EPL 2024/25.
- Coleta/importacao estabilizada para 380 partidas importaveis.
- Continua valiosa para `graph` e `shotmap`.

Valor atual:

- `graph`: momentum proprietario minuto a minuto, util como comparador/backup.
- `shotmap`: shot-level com coordenadas, xG, xGOT e `timeSeconds`, ainda superior para qualidade de chute temporal.
- `incidents`: gols, cartoes e substituicoes.

Limite atual:

- Coleta operacional dificil/fragil.
- Pressao H8 V1 mede a partida, nao necessariamente cada time.

Decisao atual:

- SofaScore nao deve ser dependencia primaria futura para pressao H8 massiva se SportMonks for validado semanticamente.
- SofaScore permanece como fonte especializada/backup para `graph` e `shotmap`.

---

## API-Football

Documento principal:

- `docs/03_SOURCES/API_FOOTBALL/FIXTURE_1545540_SPIKE.md`

Estado:

- Spike exploratorio executado em fixture `1545540`.
- Partida: Ittihad Tanger 2 x 1 Wydad AC.
- Liga: Botola Pro, Morocco, temporada 2025.
- Dados brutos salvos localmente em `C:\LateGoalResearch\data\raw\api_football\spikes\fixture_1545540\`.

Endpoints testados:

- `/fixtures?id=1545540`: util.
- `/fixtures/statistics?fixture=1545540`: util parcial; estrutura retornada, mas muitos campos vazios.
- `/fixtures/events?fixture=1545540`: util; 14 eventos, principalmente cartoes, substituicoes e gols.
- `/fixtures/lineups?fixture=1545540`: util.
- `/fixtures/players?fixture=1545540`: vazio.
- `/predictions?fixture=1545540`: util.
- `/injuries?fixture=1545540`: vazio.
- `/odds?fixture=1545540`: util; odds pre-jogo com multiplos bookmakers/mercados.
- `/odds/live?fixture=1545540`: vazio para fixture finalizada.
- `/fixtures/headtohead`: util.

Decisao Data Acquisition:

- API-Football segue como complemento candidato.
- Ainda nao substitui SofaScore para dados in-game ricos.
- Eventos retornados foram uteis para H9/match state, mas nao confirmaram pressao minuto a minuto suficiente para H8.
- Estatisticas in-game robustas nao foram confirmadas.
- Odds live historicas nao foram confirmadas.

Status:

- Complemento candidato.
- Nao promover a fonte oficial H8 sem novo discovery em liga/fixture de cobertura alta, preferencialmente Premier League com plano Pro.

---

## SportMonks H8

Documento principal:

- `docs/03_SOURCES/SPORTMONKS/SPORTMONKS_EPL_2025_26_VALIDATION_AND_SOFASCORE_COMPARISON.md`

Matriz:

- `data/processed/reports/sportmonks_epl_2025_26_endpoint_quality_matrix.csv`

Estado:

- Premier League 2025/26 auditada.
- 380 fixtures esperadas.
- 380 JSONs validos em cada uma das 8 categorias coletadas.
- Categorias auditadas: `base`, `identity`, `match_state`, `timeline`, `statistics`, `commentaries`, `trends`, `xgfixture`.
- `trends`: 109.087 MB total, 293.96 KB medio por fixture, granularidade minuto/time.
- `timeline`: 8.409 MB total, 22.66 KB medio por fixture, eventos objetivos por minuto.
- `xgfixture`: agregado por fixture/time; nao e xG temporal nem shot-level.

Valor para H8:

- `trends` permite leitura por `minute`, `participant_id`, `period_id`, `value` e `type`.
- `trends` e a fonte SportMonks mais valiosa para pressao por time/minuto.
- `timeline` fornece eventos objetivos por minuto, como chutes, corners, offside e woodwork.
- `match_state` ajuda a reconstruir gols, cartoes, substituicoes, scores e periods ate cutoff.

Risco metodologico:

- `statistics` e `xgfixture` sao agregados finais e nao devem ser usados em cutoffs 60/65/70/75 sem snapshot temporal.
- Antes de feature engineering, e obrigatorio validar semanticamente se valores de `trends` sao acumulados, incrementais ou snapshots por minuto.

Decisao Data Acquisition:

- SportMonks e fonte primaria candidata para H8 em escala.
- SportMonks substitui parcialmente SofaScore para pressao quantitativa por minuto/time.
- SofaScore permanece necessario como fonte especializada/backup para `graph` e `shotmap`.

Coleta recomendada:

- Obrigatorios H8: `trends`, `timeline`, `match_state`, `base/identity` minimo para join.
- Seletivos: `xgfixture`, `statistics`, `commentaries`.
- Nao priorizar para H8 cutoff core: `matchfacts`, `lineups`, `odds/premiumOdds`, `predictions`.

Pendencia antes de feature engineering:

- Validar semanticamente `trends`.
- Confirmar regra segura para cutoffs 60/65/70/75.
- Nao criar importer, schema, feature builder definitivo, modelo, baseline ou backtesting antes dessa validacao.

---

## SportMonks Premium Odds Diagnostic

Documento principal:

- `docs/03_SOURCES/SPORTMONKS/SPORTMONKS_PREMIUM_ODDS_EMPTY_PAYLOAD_DIAGNOSTIC_V1.md`

Matriz:

- `data/processed/reports/sportmonks_premium_odds_empty_payload_diagnostic_v1.csv`

Estado:

- `PRE_MATCH_FAVORITE_VALIDATION_V1` identificou 380 arquivos `premium_odds.json` existentes e validos.
- 380/380 payloads retornaram `data: []`.
- Odds 1X2 pre-jogo utilizaveis: 0.
- Bookmakers identificados: 0.
- Timestamps identificados: 0.

Diagnostico Data Acquisition:

- Decisao final: `CORRIGIR_ENDPOINT`.
- Causa mais provavel: rota premium por fixture usada para objetivo historico de temporada inteira.
- A documentacao SportMonks indica que Premium Odds por fixture fica disponivel por ate 7 dias apos kickoff.
- Para odds 1X2 pre-jogo, testar primeiro Standard Odds pre-match: `/v3/football/odds/pre-match/fixtures/{ID}` com `filters=markets:1`.
- Premium Historical Odds deve ser testado apenas em spike controlado por causa de volume, paginacao e janela maxima de 5 minutos no endpoint updated-between.

Restricao:

- `favorite_winning_by_1` permanece NAO APROVADO como favorito real.
- Nao validar estrategias `favorite_*` sem odds 1X2 pre-jogo com bookmaker e timestamp.

---

## H8 / Momentum / Pressao

Estado:

- H8 V1 ja foi definido e testado com dados SofaScore.
- H8 Composite Pressure Score V1 foi concluido de forma exploratoria.
- Sinais de pressao recente existem, mas a versao SofaScore atual ainda nao separa pressao por time.

Principais sinais historicos:

- `momentum_trend_last_10m @60`.
- `shots_last_10m @60`.
- `h8_cold_combo_10m_2of3`.
- `h8_pressure_score_10m_bottom25`.
- `h8_pressure_score_10m_top25`.
- `h8_shot_quality_top25`.

Limite atual:

- H8 atual mede jogo quente/frio, mas nao responde plenamente quem esta pressionando.
- Para trade, a proxima evolucao relevante e H8 por time: home/away, favorito/azarão, winning/losing team.

Proxima frente:

- `H8_TEAM_SIDE_FEATURES_V1`, preferencialmente usando SportMonks `trends`/`timeline` apos validacao semantica.

---

## Odds / Football-Data

Estado:

- Football-Data EPL 2024/25 foi importado localmente.
- 380 partidas mapeadas.
- 34280 odds importadas.
- Cobertura completa de 1X2 e Over/Under 2.5 para Odds Features V1.

Conclusao Quant:

- Odds pre-jogo/closing nao sao frente principal isolada.
- Odds podem ser usadas como moderador/contexto.
- Odds live historicas e cashout real continuam nao resolvidos.

Restricao:

- Nao tratar odds closing sem timestamp como odds live.

---

## Match State / Interacoes

Estado:

- Match State foi testado em cutoffs 60/65/70 combinado com H8 e odds.
- Alguns sinais locais apareceram, mas dependem de robustez e de pressao por time para evoluir.

Principais aprendizados:

- Estado do placar e contexto fundamental para interpretar H8.
- Taxa alta isolada nao significa edge.
- Necessario comparar com baseline, odd, break-even, N e robustez.

---

## Operacional Trade Research

Documento:

- `docs/04_RESEARCH/OPERACIONAL_TRADE_TOP_STRATEGIES_V1.md`

Estado:

- Ranking operacional exploratorio concluido.
- Odds medias observadas do mercado Proximo Gol catalogadas a partir de amostras manuais/videos.
- Stake padrao das simulacoes: 100 unidades.
- Resultados sao simulacao/pesquisa exploratoria, nao backtesting financeiro real.

Principais estrategias LAY OVER:

- `favorite_winning_by_1 + h8_cold_combo_10m_2of3`
  - Entrada: 60'.
  - Saida: hold ate 75'.
  - N=54.
  - Sem gol 60-75: 74.1%.
  - ROI estimado: +61.15%.
- `favorite_winning_by_1 + h8_pressure_score_10m_bottom25`
  - Entrada: 60'.
  - Saida: hold ate 75'.
  - N=36.
  - Sem gol 60-75: 75.0%.
  - ROI estimado: +62.50%.

Principais estrategias BACK OVER:

- `home_winning_by_1 + h8_pressure_score_10m_top25`
  - Entrada: 65'.
  - Reavaliacao: 75'.
  - N=23.
  - ROI dinamico: +7.6%.
- `home_winning_by_1 + h8_shot_quality_top25`
  - N=20.
  - ROI hold: +12.0%.
  - ROI dinamico: +16.2%.
  - Fora do ranking oficial por N exatamente 20, mas observavel.

Conclusao:

- Estrategias LAY OVER em jogo frio apresentaram maior robustez.
- Estrategias BACK OVER funcionam melhor com protocolo dinamico.

Restricoes:

- Nao autoriza producao.
- Nao autoriza robo.
- Nao autoriza trade real.
- Nao autoriza backtesting financeiro real.

---

## Sprint / Prioridades Atuais

Prioridades imediatas:

1. Validar semanticamente SportMonks `trends`.
2. Confirmar se `trends` representa acumulado, incremental ou snapshot por minuto.
3. Definir pacote oficial minimo H8 SportMonks.
4. Executar spike minimo de odds 1X2 pre-match em rota corrigida, sem coleta massiva.
5. Decidir se SportMonks vira fonte primaria H8 em escala.
6. So depois encaminhar para importer/schema/feature builder.
7. Manter API-Football em discovery complementar, especialmente para fixture EPL no plano Pro.
8. Manter SofaScore como backup/especialista para graph/shotmap.
9. Avancar `TRADE_ENTRY_PROFILE_ANALYSIS_V1` apos estabilizar fonte H8 por time.

Bloqueios:

- Nao criar importer SportMonks ainda.
- Nao alterar schema/banco ainda.
- Nao criar feature builder definitivo ainda.
- Nao iniciar modelo/baseline/backtesting com SportMonks antes da validacao semantica.
- Nao escalar para 17 ligas x 3 temporadas sem pacote oficial minimo aprovado.
- Nao validar `favorite_winning_by_1` como favorito real sem odds 1X2 pre-jogo com bookmaker e timestamp.

---

## Estado dos Agentes

Estado oficial:

- Estrutura antiga permanece vigente.
- Nenhuma reorganizacao oficial de agentes foi aplicada.

Discussao recente nao oficial:

- Remover CTO do nucleo diario foi discutido, mas nao aplicado.
- Fundir Quant Research + Data Science em Quant & Modeling foi discutido, mas nao aplicado.
- Usuario decidiu permanecer com a estrutura antiga por enquanto.

---

## Proxima Decisao PM

A proxima decisao critica nao e criar feature nova.

As decisoes criticas sao:

```text
SportMonks `trends` pode ser usado com seguranca para cutoffs 60/65/70/75?
```

```text
Qual fonte/rota entregara odds 1X2 pre-jogo com bookmaker e timestamp para validar favorite_*?
```

Se SIM para `trends`:

- SportMonks passa a ser fonte primaria candidata para H8 por time.
- Iniciar desenho de `H8_TEAM_SIDE_FEATURES_V1`.

Se NAO:

- SportMonks permanece complemento.
- SofaScore shotmap/graph continuam essenciais.
- Buscar fonte alternativa para pressao minuto/time.
