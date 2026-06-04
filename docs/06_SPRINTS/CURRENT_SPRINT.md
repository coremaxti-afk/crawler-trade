# CURRENT SPRINT

## Sprint Atual

Objetivo:

Construir a base histórica SofaScore e preparar a importação para PostgreSQL.

---

## Concluído

- [x] Criar sofascore_season_collector.py
- [x] Criar sofascore_match_collector.py
- [x] Descobrir temporada EPL
- [x] Gerar inventory.json
- [x] Gerar rounds.json
- [x] Coletar event.json
- [x] Coletar statistics.json
- [x] Coletar incidents.json
- [x] Coletar lineups.json
- [x] Coletar h2h.json
- [x] Coletar 50 partidas da EPL
- [x] Implementar correção operacional para HTTP 403 no coletor SofaScore v2
- [x] Executar teste operacional controlado de retomada

---

## Atualização Operacional Mais Recente

Resultado observado:

- Coleta executada através de conexão 5G.
- 107 partidas adicionais coletadas sem ocorrência de HTTP 403.
- Evidência forte de que o bloqueio está relacionado ao IP/conexão anterior e não a uma falha primária do coletor.

Marco atual da coleta:

- Até a partida 194: coleta completa com 5 JSONs por partida.
  - event.json
  - statistics.json
  - incidents.json
  - lineups.json
  - h2h.json

- A partir da partida 195: coleta em perfil core.
  - event.json
  - statistics.json
  - incidents.json

Objetivo do perfil core:

- reduzir volume de requests;
- diminuir risco de novo HTTP 403;
- priorizar os dados necessários para importer e primeiras análises.

---

## Em Andamento

- [ ] Finalizar coleta completa da EPL
- [ ] Monitorar estabilidade da coleta em conexão 5G
- [ ] Confirmar se a coleta ultrapassa 194 partidas sem retorno do HTTP 403

---

## Correção Operacional HTTP 403 SofaScore

Status:

Implementado, revisado e validado operacionalmente.

Commit:

- `54bbb14` — Melhora robustez do coletor SofaScore v2

Observação atual:

- A persistência anterior do HTTP 403 continua registrada.
- Porém os testes recentes em 5G indicam que o problema está fortemente associado à origem da conexão/IP.
- Não há evidência atual de falha estrutural do coletor.

---

## Próximos Passos

- [ ] Continuar coleta EPL até novo bloqueio ou conclusão da temporada
- [ ] Registrar número final de partidas coletadas antes de qualquer novo 403
- [ ] Consolidar inventário real de partidas completas (5 JSONs) e partidas core (3 JSONs)
- [ ] Iniciar planejamento do sofascore_importer.py
- [ ] Popular PostgreSQL
- [ ] Validar match_statistics
- [ ] Validar match_incidents
- [ ] Implementar coleta de graph
- [ ] Iniciar Feature Engineering

---

## Resultado Esperado

Base histórica consistente da Premier League disponível para integração multi-fonte e validação das hipóteses H1-H9.

---

## Status

EM EXECUÇÃO — COLETA SOFASCORE ATIVA EM 5G E PERFIL CORE A PARTIR DA PARTIDA 195