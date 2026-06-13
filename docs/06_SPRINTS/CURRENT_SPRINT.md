# CURRENT SPRINT

## Sprint Atual

Objetivo:

Encerrar a frente `favorite_winning_by_1 + jogo frio` como pesquisa operacional exploratoria aprovada com ressalvas na Premier League e abrir a proxima frente `SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1`, usando SportMonks para investigar pressao por lado/time.

Restricoes permanentes:

- Nao criar producao.
- Nao criar robo.
- Nao executar trade real.
- Nao criar modelo ou baseline preditivo sem aprovacao.
- Nao executar backtesting financeiro real com odds live nao timestampadas.
- Nao criar features com leakage, target-derived ou pos-cutoff.

---

## Concluido

- [x] Consolidar ranking operacional de estrategias (`OPERACIONAL_TRADE_TOP_STRATEGIES_V1`).
- [x] Catalogar estrategias LAY OVER em jogo frio.
- [x] Catalogar estrategias BACK OVER em jogo quente.
- [x] Consolidar odds medias observadas para mercado Proximo Gol.
- [x] Coletar SportMonks EPL 2025/26 pacote H8.
- [x] Auditar SportMonks EPL 2025/26 contra SofaScore.
- [x] Gerar matriz de qualidade SportMonks EPL 2025/26.
- [x] Registrar spike API-Football fixture `1545540`.
- [x] Classificar API-Football como complemento candidato, nao substituto oficial H8.
- [x] Classificar SportMonks como fonte primaria candidata para H8 em escala, pendente validacao semantica.
- [x] Executar diagnostico `SPORTMONKS_PREMIUM_ODDS_EMPTY_PAYLOAD_DIAGNOSTIC_V1`.
- [x] Atualizar `OPERACIONAL_TRADE_TOP_STRATEGIES_V1` com consolidado EPL 2024/25 + 2025/26.
- [x] Atualizar `FOOTBALL_DATA_FAVORITE_VALIDATION_V2`.
- [x] Registrar que `favorite_side = menor odd pre-jogo 1X2` e a regra operacional correta para comparacao historica.
- [x] Encerrar `favorite_winning_by_1 + jogo frio` como APROVADO COM RESSALVAS PARA PESQUISA OPERACIONAL.
- [x] Criar `SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1.md`.

---

## Resultado Consolidado - favorite_winning_by_1 + jogo frio

### h8_cold_combo_10m_2of3

Consolidado EPL 2024/25 + 2025/26:

- 123 entradas.
- 88 acertos.
- 35 erros.
- 71.5% sem gol 60-75.
- ROI estimado com Lay Over @1.50: +57.3%.

### h8_pressure_score_10m_bottom25

Consolidado EPL 2024/25 + 2025/26:

- 80 entradas.
- 59 acertos.
- 21 erros.
- 73.8% sem gol 60-75.
- ROI estimado com Lay Over @1.50: +60.6%.

Leitura PM:

- `h8_cold_combo_10m_2of3` tem maior amostra.
- `h8_pressure_score_10m_bottom25` tem melhor taxa.
- Ambas seguem apenas como pesquisa operacional exploratoria.

Ressalvas:

- odds de entrada do mercado Proximo Gol ainda sao medias observadas/manualizadas;
- nao ha odds live reais por timestamp;
- validacao ainda e Premier League apenas;
- precisa replicacao multi-liga;
- resultado nao autoriza execucao real.

---

## Em andamento / pendente

### Prioridade 1 - SportMonks semantic validation

- [ ] Finalizar coletas SportMonks ja iniciadas sem aumentar escopo.
- [ ] Validar semanticamente SportMonks `trends` antes de criar features H8.
- [ ] Confirmar se valores de `trends` sao acumulados, incrementais ou snapshots por minuto.
- [ ] Validar se `trends` permite cutoffs seguros 60/65/70/75 usando apenas `minute <= cutoff`.
- [ ] Definir whitelist V1 de indicadores por time.
- [ ] Definir pacote oficial minimo H8 SportMonks para escala.

### Prioridade 2 - SportMonks Team-Side Strategy Discovery

- [ ] Revisar `SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1.md`.
- [ ] Selecionar combos iniciais sem p-hacking livre.
- [ ] Explorar pressao por `participant_id`.
- [ ] Avaliar time perdendo pressionando.
- [ ] Avaliar favorito perdendo pressionando.
- [ ] Avaliar favorito vencendo e adversario pressionando.
- [ ] Avaliar mandante/visitante vencendo por 1 com pressao contraria.
- [ ] Avaliar jogo frio por lado/time.
- [ ] Separar descoberta estatistica de operacionalizacao.

### Prioridade 3 - Odds pre-match / favorito real

- [ ] Executar spike minimo SportMonks Standard Odds pre-match em 1-3 fixtures.
- [ ] Testar `market_id=1` / `FULLTIME_RESULT` com labels Home/Draw/Away.
- [ ] Testar rota `/v3/football/odds/pre-match/fixtures/{ID}` com `include=market;bookmaker` e `filters=markets:1`.
- [ ] Se necessario, testar Premium Historical Odds apenas em janela pequena, sem coleta massiva.

### Prioridade 4 - API-Football discovery complementar

- [ ] Executar discovery API-Football em uma fixture de Premier League usando plano Pro.
- [ ] Verificar se `/fixtures/events` retorna eventos historicos suficientes por minuto/time.
- [ ] Verificar se `/fixtures/statistics` tem cobertura robusta em Premier League.
- [ ] Confirmar se API-Football pode complementar ou substituir algum subconjunto do SofaScore/SportMonks.

---

## Decisoes recentes

### favorite_winning_by_1 + jogo frio

- Definicao operacional para comparacao historica: `favorite_side = menor odd pre-jogo 1X2`.
- Nao usar `favorite_odd <= 1.70` como regra principal nesta comparacao.
- Frente aprovada com ressalvas para pesquisa operacional EPL.
- Nao autoriza robo, producao, trade real, automacao operacional ou backtesting financeiro real.

### SportMonks

- `trends` e o principal endpoint candidato para pressao por minuto/time.
- `timeline` e obrigatorio para validacao objetiva de eventos por minuto.
- `match_state` e recomendado para gols/cartoes/substituicoes/scores/periods.
- `statistics` e `xgfixture` sao agregados finais e nao devem ser usados como cutoff features sem snapshot temporal.
- SportMonks Team-Side Strategy Discovery e a proxima frente oficial apos validacao semantica de `trends`.

### SofaScore

- SofaScore deixa de ser dependencia primaria para pressao H8 massiva se SportMonks `trends` for validado semanticamente.
- SofaScore continua valioso para `graph` e `shotmap`.

### API-Football

- API-Football segue como complemento candidato.
- Nao promover API-Football a substituto SofaScore/SportMonks para H8 sem novo discovery em fixture EPL/plano Pro.

### Agentes

- Estrutura antiga de agentes permanece vigente.
- Nenhuma reorganizacao oficial foi aplicada.

---

## Bloqueios

- Nao criar importer SportMonks ainda.
- Nao alterar schema/banco ainda.
- Nao criar feature builder definitivo ainda.
- Nao iniciar modelo/baseline/backtesting com SportMonks antes da validacao semantica de `trends`.
- Nao escalar para multiplas ligas/temporadas sem pacote oficial minimo aprovado.
- Nao transformar API-Football em fonte oficial H8 antes de discovery EPL no plano Pro.
- Nao tratar odds medias observadas como odds live reais.
- Nao transformar resultados `favorite_winning_by_1 + jogo frio` em recomendacao operacional real.

---

## Proximo agente recomendado

Quant Research / Data Science, com apoio de Data Acquisition.

Tarefa principal:

Validar semanticamente SportMonks `trends` e preparar a descoberta `SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1`, preservando anti-leakage por cutoff e sem criar modelo, baseline, robo, producao ou backtesting financeiro real.
