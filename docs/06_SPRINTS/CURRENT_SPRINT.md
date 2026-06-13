# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar a pesquisa exploratoria de H8, Odds, Match State e protocolos dinamicos de trade teorico, incorporando a validacao de fontes SportMonks/API-Football e definindo com seguranca a proxima fonte primaria candidata para H8 por time.

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

---

## Em andamento / pendente

### Prioridade 1 - SportMonks semantic validation

- [ ] Finalizar coletas SportMonks ja iniciadas sem aumentar escopo.
- [ ] Validar semanticamente SportMonks `trends` antes de criar features H8.
- [ ] Confirmar se valores de `trends` sao acumulados, incrementais ou snapshots por minuto.
- [ ] Validar se `trends` permite cutoffs seguros 60/65/70/75 usando apenas `minute <= cutoff`.
- [ ] Definir pacote oficial minimo H8 SportMonks para escala.
- [ ] Decidir se SportMonks vira fonte primaria H8 por time.

### Prioridade 2 - API-Football discovery complementar

- [ ] Executar discovery API-Football em uma fixture de Premier League usando plano Pro.
- [ ] Verificar se `/fixtures/events` retorna eventos historicos suficientes por minuto/time.
- [ ] Verificar se `/fixtures/statistics` tem cobertura robusta em Premier League.
- [ ] Confirmar se API-Football pode complementar ou substituir algum subconjunto do SofaScore/SportMonks.

### Prioridade 3 - Trade research operacional

- [ ] Criar/revisar `TRADE_ENTRY_PROFILE_ANALYSIS_V1.md` apos estabilizar a fonte H8 por time.
- [ ] Produzir/revisar `DYNAMIC_TRADE_PROTOCOL_EXPANSION_PLAN_V1.md`.
- [ ] Executar `DYNAMIC_TRADE_PROTOCOL_VALIDATION_V2` somente apos plano aprovado.
- [ ] Avaliar `MARKET_PRICE_CASHOUT_SENSITIVITY_V1` sem tratar odds medias como odds live reais.

---

## Decisoes recentes

### SportMonks

- `trends` e o principal endpoint H8 para pressao por minuto/time.
- `timeline` e obrigatorio para validacao objetiva de eventos por minuto.
- `match_state` e recomendado para gols/cartoes/substituicoes/scores/periods.
- `base/identity` e necessario para contexto e joins.
- `xgfixture`, `statistics` e `commentaries` ficam como seletivos, nao core.
- `statistics` e `xgfixture` sao agregados finais e nao devem ser usados como cutoff features sem snapshot temporal.
- `matchfacts`, `lineups`, `odds/premiumOdds` e `predictions` nao sao prioridade para H8 cutoff core.

### SofaScore

- SofaScore deixa de ser dependencia primaria para pressao H8 massiva se SportMonks `trends` for validado semanticamente.
- SofaScore continua valioso para `graph` e `shotmap`.
- `shotmap` segue superior para xG/xGOT temporal por finalizacao e coordenadas.

### API-Football

- API-Football segue como complemento candidato.
- Spike fixture `1545540` retornou fixture, events, lineups, odds, predictions e head-to-head.
- Estatisticas in-game robustas nao foram confirmadas no spike.
- Odds live para fixture finalizada vieram vazias.
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
- Nao escalar para 17 ligas x 3 temporadas sem pacote oficial minimo aprovado.
- Nao transformar API-Football em fonte oficial H8 antes de discovery EPL no plano Pro.
- Nao tratar odds medias observadas como odds live reais.

---

## Proximo agente recomendado

Quant Research / Data Science, com apoio de Data Acquisition.

Tarefa:

Validar semanticamente SportMonks `trends` em amostra controlada de jogos, checar se valores sao acumulados, incrementais ou snapshots por minuto e propor regra segura de leitura para cutoffs 60/65/70/75, sem criar features definitivas ainda.
