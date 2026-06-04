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

## Em Andamento

- [ ] Decidir estratégia operacional após persistência do HTTP 403 na retomada
- [ ] Finalizar coleta completa da EPL

---

## Bloqueado / Atenção

### HTTP 403 SofaScore persiste

Situação:

- A correção técnica do coletor SofaScore v2 funcionou operacionalmente.
- O coletor preservou o comportamento esperado de checkpoint, validação de JSONs, logs e interrupção segura.
- Porém, na retomada da coleta a partir da partida 51, o SofaScore ainda retornou HTTP 403.

Interpretação:

- O problema não é mais tratado como falha primária do código do coletor.
- O bloqueio externo da fonte permanece ativo.
- A coleta SofaScore deve permanecer pausada até nova decisão operacional.

Decisão provisória do PM:

- Não retornar diretamente ao Codex neste momento.
- Não executar coleta massiva.
- Encaminhar para nova avaliação conjunta de Data Acquisition Engineer e CTO.

---

## Correção Operacional HTTP 403 SofaScore

Status:

Implementado, revisado e testado operacionalmente.

Commit:

- `54bbb14` — Melhora robustez do coletor SofaScore v2

Arquivo alterado:

- `LateGoalResearch/Crawler/Sofascore/v2_sofascore_match_collector.py`

Resumo:

- Implementado checkpoint por endpoint.
- A partida só é considerada completa quando os 5 JSONs existem e são válidos:
  - `event.json`
  - `statistics.json`
  - `incidents.json`
  - `lineups.json`
  - `h2h.json`
- JSON válido existente é pulado e não sobrescrito.
- JSON inválido é movido para `_invalid_json_backup`.
- Adicionado log auditável em `data/raw/sofascore/premier_league_61627/collection_log.jsonl`.
- Adicionado retry/backoff para HTTP 429, HTTP 5xx, timeout e falhas temporárias.
- HTTP 403 registra `blocked` e encerra o lote.
- Adicionados parâmetros operacionais:
  - `--limit`
  - `--dry-run`
  - `--list-pending`
  - delay entre endpoints
  - delay entre partidas
  - jitter

Escopo preservado:

- schema do banco não alterado;
- importer PostgreSQL não alterado;
- features não alteradas;
- modelagem não alterada;
- outros collectors não alterados;
- estrutura dos JSONs brutos preservada.

Validação:

- Data Acquisition Engineer aprovou para teste operacional controlado.
- Coleta massiva ainda não deve ser executada.
- Teste de retomada indicou persistência de HTTP 403 na partida 51.

---

## Próximos Passos

- [ ] Enviar resultado do teste ao Data Acquisition Engineer
- [ ] Solicitar análise operacional sobre alternativas seguras para retomada
- [ ] Enviar recomendação do Data Acquisition ao CTO
- [ ] CTO decidir se a coleta permanece pausada, se muda cadência operacional ou se prioriza outra frente
- [ ] Considerar iniciar Data Engineer / Database com as 50 partidas já coletadas, se aprovado pelo CTO/PM
- [ ] Finalizar coleta EPL completa somente após nova decisão operacional
- [ ] Implementar sofascore_importer.py
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

EM EXECUÇÃO — COLETA SOFASCORE PAUSADA POR HTTP 403 PERSISTENTE
