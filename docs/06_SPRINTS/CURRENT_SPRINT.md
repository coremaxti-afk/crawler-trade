# CURRENT SPRINT

## Sprint Atual

Objetivo:

Consolidar a pesquisa exploratoria de H8, Odds, Match State e protocolos dinamicos de trade teorico, incluindo ranking operacional de estrategias, validacao de fontes SportMonks/SofaScore e decisao de escopo de coleta, mantendo bloqueados producao, robo, trade real, modelo, baseline preditivo e backtesting real.

---

## Concluido

- [x] Consolidar ranking operacional de estrategias (OPERACIONAL_TRADE_TOP_STRATEGIES_V1)
- [x] Catalogar estrategias LAY OVER (jogo frio)
- [x] Catalogar estrategias BACK OVER (jogo quente)
- [x] Consolidar odds medias observadas para mercado Proximo Gol
- [x] Coletar SportMonks EPL 2025/26 pacote H8
- [x] Auditar SportMonks EPL 2025/26 contra SofaScore
- [x] Gerar matriz de qualidade SportMonks EPL 2025/26

---

## Em andamento / pendente

- [ ] Finalizar coletas SportMonks ja iniciadas sem aumentar escopo.
- [ ] Validar semanticamente SportMonks `trends` antes de criar features H8.
- [ ] Confirmar se valores de `trends` sao acumulados, incrementais ou snapshots por minuto.
- [ ] Definir pacote oficial minimo H8 SportMonks para escala.
- [ ] Encaminhar para CTO/Data Engineer somente depois da validacao semantica e decisao de escopo.

---

## Decisoes recentes

### SportMonks

- `trends` e o principal endpoint H8 para pressao por minuto/time.
- `timeline` e obrigatorio para validacao objetiva de eventos por minuto.
- `match_state` e recomendado para gols/cartoes/substituicoes/scores/periods.
- `xgfixture`, `statistics` e `commentaries` ficam como seletivos, nao core.
- `matchfacts`, `lineups`, `odds/premiumOdds` e `predictions` nao sao prioridade para H8 cutoff core.

### SofaScore

- SofaScore deixa de ser dependencia primaria para pressao H8 massiva quando SportMonks estiver disponivel.
- SofaScore continua valioso para `graph` e `shotmap`.
- `shotmap` segue superior para xG/xGOT temporal por finalizacao e coordenadas.

---

## Bloqueios

- Nao criar importer SportMonks ainda.
- Nao alterar schema/banco ainda.
- Nao criar feature builder definitivo ainda.
- Nao iniciar modelo/baseline/backtesting com SportMonks antes da validacao semantica de `trends`.
- Nao escalar para 17 ligas x 3 temporadas sem pacote oficial minimo aprovado.

---

(Restante mantido)
