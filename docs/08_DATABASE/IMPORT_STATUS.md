# IMPORT STATUS

## Objetivo

Acompanhar o estado da importação dos dados coletados para o PostgreSQL.

---

## Understat

Status:
Operacional

Origem:
Understat

Destino:
matches_master

Dados disponíveis:

- Match ID
- Liga
- Temporada
- Data
- Times
- Placar
- xG
- Forecast
- PPDA
- Deep
- xGA

---

## SofaScore

### Season Collector

Status:
Implementado

Artefatos:

- inventory.json
- rounds.json
- round_XX_events.json

---

### Match Collector

Status:
Implementado e endurecido operacionalmente no v2

Script relevante:

- `LateGoalResearch/Crawler/Sofascore/v2_sofascore_match_collector.py`

Commit relevante:

- `54bbb14` — Melhora robustez do coletor SofaScore v2

Artefatos originalmente coletados:

- event.json
- statistics.json
- incidents.json
- lineups.json
- h2h.json

Comportamento do v2:

- checkpoint por endpoint;
- validação de JSON existente;
- skip de JSON válido;
- backup de JSON inválido;
- log auditável em `data/raw/sofascore/premier_league_61627/collection_log.jsonl`;
- retry/backoff para falhas temporárias;
- HTTP 403 registra `blocked` e encerra o lote.

Status operacional:

- A correção funcionou tecnicamente.
- O HTTP 403 persistiu na retomada da partida 51.
- Coleta massiva pausada até nova decisão operacional.

---

### Perfil de Importação Inicial Recomendado

Para destravar a engenharia de dados, o importer inicial deve priorizar os JSONs core:

- event.json
- statistics.json
- incidents.json

Motivo:

- são suficientes para criar base inicial de partidas, estatísticas agregadas e eventos com minuto;
- permitem validar target de gols tardios e primeiras hipóteses;
- reduzem dependência de dados complementares;
- são compatíveis com uma futura coleta core reduzida.

JSONs complementares:

- lineups.json
- h2h.json

Observação:

- lineups e h2h não devem bloquear o importer inicial.
- Devem ser tratados como complementares em etapa futura.

---

### Graph / Minuto a Minuto

Status:

- Estrutura `match_graph` pronta.
- Coleta do endpoint graph ainda não implementada.

Interpretação:

- `incidents.json` possui eventos com minuto.
- Isso não equivale a dados minuto a minuto completos.
- Para momentum e pressão temporal, será necessário `graph.json` ou endpoint equivalente.

Impacto no importer:

- `match_graph` não deve bloquear o importer inicial.
- Importação de graph deve ser tratada como etapa posterior.

---

### Importer

Status:
Não iniciado

Script previsto:

- sofascore_importer.py

Prioridade sugerida:

1. Importer inicial para `event.json`, `statistics.json` e `incidents.json`.
2. Importação complementar de `lineups.json` e `h2h.json`, se necessário.
3. Importação de `graph.json` quando a coleta minuto a minuto for implementada.

---

## Tabelas PostgreSQL

### matches_master

Status:
Pronta

Uso inicial:

- receber dados centrais de `event.json` e integração com Understat/match_mapping.

---

### match_statistics

Status:
Pronta

Uso inicial:

- receber estatísticas agregadas de `statistics.json`.

---

### match_incidents

Status:
Pronta

Uso inicial:

- receber eventos de `incidents.json`, incluindo gols, cartões e substituições quando disponíveis.

---

### match_graph

Status:
Estrutura pronta

Observação:
Coleta do endpoint graph ainda não implementada.

Uso futuro:

- armazenar momentum/pressão temporal minuto a minuto ou por janela temporal.

---

## Estado Atual do Projeto

Temporadas descobertas:

- Premier League 2024/25

Partidas coletadas:

- 50+

JSONs coletados:

- 250+

Estado da coleta SofaScore:

- pausada por HTTP 403 persistente após teste de retomada.

---

## Próximo Marco

Implementar:

- sofascore_importer.py

Objetivo inicial:

Importar dados SofaScore core para:

- matches_master
- match_statistics
- match_incidents

Objetivo posterior:

Importar dados complementares para:

- match_graph, quando graph/minuto a minuto estiver disponível;
- tabelas complementares, se CTO aprovar necessidade futura para lineups/h2h.

---

## Bloqueios Conhecidos

### HTTP 403 SofaScore

Situação observada:

- coleta funcional em amostra inicial;
- bloqueio após grande volume de requisições;
- correção operacional implementada;
- HTTP 403 persistiu na retomada da partida 51.

Hipóteses:

- rate limiting
- session limiting
- IP limiting

Status:

- bloqueio externo ainda ativo;
- coleta massiva pausada;
- próxima decisão deve envolver Data Acquisition Engineer e CTO.

---

## Decisão Pendente

Avaliar se o projeto deve:

1. tentar novo teste SofaScore com perfil core de 3 JSONs;
2. iniciar importer com as 50 partidas já coletadas;
3. executar spike controlado da API-Football;
4. combinar as três frentes em sequência controlada.
