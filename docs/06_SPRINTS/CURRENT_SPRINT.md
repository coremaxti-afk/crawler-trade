# CURRENT SPRINT

## Sprint Atual

Objetivo:

Construir a base historica SofaScore e preparar/importar os dados core para PostgreSQL.

---

## Concluido

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
- [x] Implementar correcao operacional para HTTP 403 no coletor SofaScore v2
- [x] Executar teste operacional controlado de retomada
- [x] Validar coleta via 5G sem novo HTTP 403
- [x] Criar coletor SofaScore v3 em perfil core
- [x] Executar lote core com 188 partidas planejadas
- [x] Consolidar inventario real de partidas full/core
- [x] Confirmar total final contra o inventario de 381 partidas
- [x] Implementar sofascore_importer.py
- [x] Popular PostgreSQL com dados SofaScore core
- [x] Validar idempotencia do importer
- [x] Validar integridade basica entre matches_master, match_statistics e match_incidents

---

## Atualizacao Operacional Mais Recente

Resultado observado:

- Coleta executada atraves de conexao 5G sem novo HTTP 403 em mais de 100 partidas.
- Evidencia forte de que o bloqueio anterior estava associado a IP/conexao e volume de requests, nao a falha primaria do coletor.
- Para reduzir volume, foi criado o coletor v3 em perfil core.

Perfis de coleta:

- Full: 5 JSONs por partida.
  - `event.json`
  - `statistics.json`
  - `incidents.json`
  - `lineups.json`
  - `h2h.json`

- Core: 3 JSONs por partida.
  - `event.json`
  - `statistics.json`
  - `incidents.json`

---

## Auditoria Local SofaScore EPL

Resultado confirmado:

- Total no inventory: 381 partidas.
- Total de pastas locais: 381.
- Partidas full: 192.
- Partidas core: 188.
- Total importavel: 380.
- Partidas faltantes: 0.
- Partidas incompletas relevantes: 1.
- Partida descartada da importacao atual: `12436452`.

Observacao:

- A partida `12436449` foi corrigida/coletada com os 3 dados core e foi considerada importavel.

---

## Importacao PostgreSQL

Script:

- `LateGoalResearch/Crawler/Sofascore/sofascore_importer.py`

Commit:

- `84e641f` - Implementa importer SofaScore core

Escopo importado:

- `matches_master`
- `match_statistics`
- `match_incidents`

Fora do escopo:

- `match_graph`
- lineups
- h2h
- features
- dataset analitico
- modelagem

Resultado da primeira importacao:

- processed: 380
- inserted: 380
- updated: 0
- failed: 0
- known_skipped: 1

Resultado da segunda execucao:

- processed: 380
- inserted: 0
- updated: 380
- failed: 0
- known_skipped: 1

Contagens finais no banco:

- `matches_master`: 380 eventos distintos.
- `match_statistics`: 380 eventos distintos.
- `match_incidents`: 7647 registros, cobrindo 380 eventos.
- Registros para `12436452`: 0.
- Orfaos em `match_statistics`: 0.
- Orfaos em `match_incidents`: 0.
- Partidas importadas sem estatisticas: 0.

---

## Em Andamento

- [ ] Validar amostras importadas por coluna
- [ ] Revisar qualidade dos dados de `match_statistics`
- [ ] Revisar qualidade dos dados de `match_incidents`
- [ ] Definir proximo passo tecnico com CTO/Data Engineer

---

## Proximos Passos

- [ ] Conferir amostras de partidas full e core no PostgreSQL
- [ ] Validar consistencia de placar e data em `matches_master`
- [ ] Validar campos principais em `match_statistics`
- [ ] Validar gols, cartoes e substituicoes em `match_incidents`
- [ ] Decidir se a proxima etapa sera graph, importacao complementar ou catalogo de features
- [ ] Implementar coleta de graph em etapa posterior, se aprovada
- [ ] Iniciar Feature Engineering somente apos aprovacao

---

## Resultado Esperado

Base historica SofaScore EPL core importada no PostgreSQL, validada e pronta para a proxima decisao de engenharia de dados.

---

## Status

EM EXECUCAO - COLETA CORE CONCLUIDA; IMPORTER SOFASCORE IMPLEMENTADO; POSTGRESQL POPULADO COM 380 PARTIDAS IMPORTAVEIS
