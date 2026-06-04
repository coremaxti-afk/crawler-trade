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
- [x] Validar coleta via 5G sem novo HTTP 403
- [x] Executar lote core com 188 partidas planejadas

---

## Atualização Operacional Mais Recente

Resultado observado:

- Coleta executada através de conexão 5G.
- 107 partidas adicionais foram coletadas inicialmente sem ocorrência de HTTP 403.
- Evidência forte de que o bloqueio anterior estava relacionado ao IP/conexão anterior e não a uma falha primária do coletor.

Marco de coleta por perfil:

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

## Resumo Final do Lote Core

Resultado informado:

- Partidas planejadas: 188
- Endpoints coletados: 558
- Endpoints pulados: 6
- Endpoints falhos: 0
- Bloqueio operacional: False
- Log: `data\raw\sofascore\premier_league_61627\collection_log_v3.jsonl`

Interpretação:

- O lote core foi executado com sucesso operacional.
- Não houve falhas de endpoint.
- Não houve novo bloqueio HTTP 403.
- Os 6 endpoints pulados devem ser tratados como comportamento esperado se já existiam JSONs válidos.
- A coleta core está aprovada como estratégia operacional para reduzir volume de requests.

---

## Em Andamento

- [ ] Consolidar inventário real de partidas completas (5 JSONs) e partidas core (3 JSONs)
- [ ] Confirmar total final de partidas EPL coletadas contra o inventário de 381 partidas
- [ ] Iniciar planejamento do sofascore_importer.py

---

## Correção Operacional HTTP 403 SofaScore

Status:

Implementado, revisado e validado operacionalmente.

Commit:

- `54bbb14` — Melhora robustez do coletor SofaScore v2

Observação atual:

- A persistência anterior do HTTP 403 continua registrada historicamente.
- Porém os testes em 5G e o lote core indicam que o problema estava fortemente associado à origem da conexão/IP e ao volume de requisições.
- Não há evidência atual de falha estrutural do coletor.

---

## Próximos Passos

- [ ] Validar contagem final de partidas coletadas
- [ ] Validar consistência entre inventário, pastas locais e logs
- [ ] Consolidar inventário real de partidas full e core
- [ ] Acionar Data Engineer / Database para planejar importer com suporte a dados full/core
- [ ] Implementar sofascore_importer.py
- [ ] Popular PostgreSQL
- [ ] Validar match_statistics
- [ ] Validar match_incidents
- [ ] Implementar coleta de graph em etapa posterior
- [ ] Iniciar Feature Engineering

---

## Resultado Esperado

Base histórica consistente da Premier League disponível para integração multi-fonte e validação das hipóteses H1-H9.

---

## Status

EM EXECUÇÃO — COLETA CORE SOFASCORE CONCLUÍDA COM SUCESSO OPERACIONAL; PRÓXIMA FRENTE: CONSOLIDAÇÃO E IMPORTER