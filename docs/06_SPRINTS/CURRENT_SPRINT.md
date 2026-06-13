# CURRENT SPRINT

## Sprint Atual

Objetivo:

Registrar a correcao metodologica da frente `favorite_winning_by_1 + jogo frio` e redirecionar a proxima pesquisa SportMonks para duas familias: `UNDER_HOLD` e `OVER_JANELA_CURTA`, usando SportMonks para investigar pressao por lado/time.

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
- [x] Corrigir interpretacao de ROI das estrategias Lay Over / Under frias com saida fixa aos 75.

---

## Correcao Metodologica - Lay Over / Under Frio

Erro identificado:

O lucro anterior foi interpretado como:

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

### h8_cold_combo_10m_2of3

Consolidado EPL 2024/25 + 2025/26:

- 123 entradas.
- 88 acertos.
- 35 erros.
- 71.5% sem gol 60-75.
- Lucro corrigido saida fixa 75: +450.
- ROI corrigido saida fixa 75: +3.7%.

### h8_pressure_score_10m_bottom25

Consolidado EPL 2024/25 + 2025/26:

- 80 entradas.
- 59 acertos.
- 21 erros.
- 73.8% sem gol 60-75.
- Lucro corrigido saida fixa 75: +425.
- ROI corrigido saida fixa 75: +5.3%.

Leitura PM:

- As estrategias continuam consistentes estatisticamente para prever ausencia de gol 60-75.
- O lucro operacional com cashout fixo aos 75 e baixo.
- Lay Over / Under frio tende a fazer mais sentido como HOLD ou janela mais longa.
- Para janela curta, a proxima pesquisa deve buscar tambem estrategias Over com gol dentro da janela.

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

Dividir a descoberta em duas familias:

#### UNDER_HOLD

Objetivo:

- Encontrar cenarios com alta probabilidade de nao sair gol ate janela mais longa ou liquidacao relevante.

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

#### OVER_JANELA_CURTA

Objetivo:

- Encontrar cenarios com alta probabilidade de gol entre 60-75, 65-80 ou 70-85.

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

Tarefas:

- [ ] Revisar `SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1.md` atualizado.
- [ ] Selecionar combos iniciais sem p-hacking livre.
- [ ] Explorar pressao por `participant_id`.
- [ ] Separar candidatos `UNDER_HOLD` e `OVER_JANELA_CURTA`.
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
- ROI alto anterior representa simulacao tipo HOLD/liquidacao completa.
- ROI corrigido para saida fixa 60-75 e baixo.
- Nao autoriza robo, producao, trade real, automacao operacional ou backtesting financeiro real.

### SportMonks

- `trends` e o principal endpoint candidato para pressao por minuto/time.
- `timeline` e obrigatorio para validacao objetiva de eventos por minuto.
- `match_state` e recomendado para gols/cartoes/substituicoes/scores/periods.
- `statistics` e `xgfixture` sao agregados finais e nao devem ser usados como cutoff features sem snapshot temporal.
- SportMonks Team-Side Strategy Discovery deve priorizar duas familias: `UNDER_HOLD` e `OVER_JANELA_CURTA`.

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

Validar semanticamente SportMonks `trends` e preparar a descoberta `SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1`, separando `UNDER_HOLD` e `OVER_JANELA_CURTA`, preservando anti-leakage por cutoff e sem criar modelo, baseline, robo, producao ou backtesting financeiro real.
