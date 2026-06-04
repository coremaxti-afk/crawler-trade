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

---

## Em Andamento

- [ ] Validar retomada controlada da coleta SofaScore v2
- [ ] Finalizar coleta completa da EPL

---

## Correção Operacional HTTP 403 SofaScore

Status:

Implementado e revisado.

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

Próxima validação operacional:

```bash
python LateGoalResearch/Crawler/Sofascore/v2_sofascore_match_collector.py --dry-run

python LateGoalResearch/Crawler/Sofascore/v2_sofascore_match_collector.py --list-pending

python LateGoalResearch/Crawler/Sofascore/v2_sofascore_match_collector.py \
  --limit 1 \
  --endpoint-delay 10 \
  --match-delay 30 \
  --jitter 10 \
  --backoff 60 \
  --max-retries 2
```

---

## Próximos Passos

- [ ] Executar `--dry-run`
- [ ] Executar `--list-pending`
- [ ] Executar coleta mínima com `--limit 1`
- [ ] Validar `collection_log.jsonl`
- [ ] Validar se não houve sobrescrita de JSON válido
- [ ] Validar se nenhum novo HTTP 403 ocorreu no teste mínimo
- [ ] Ampliar coleta gradualmente se teste mínimo for aprovado
- [ ] Finalizar coleta EPL completa
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

EM EXECUÇÃO
