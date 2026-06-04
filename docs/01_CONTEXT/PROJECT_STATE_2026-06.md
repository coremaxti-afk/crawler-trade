# PROJECT STATE 2026-06

## Visão Geral

Projeto:

LateGoalResearch

Objetivo:

Descobrir padrões quantitativos capazes de antecipar gols tardios através da integração de múltiplas fontes de dados.

---

## Estado Atual

### Infraestrutura

- PostgreSQL configurado.
- SQLAlchemy configurado.
- Configuração centralizada em config/database.py.

### Fontes

#### Understat

Status:
Operacional.

Uso atual:

- fonte principal para xG, xGA, forecast, PPDA e métricas pré-jogo.

#### SofaScore

Status:
Operacional em nível de collector, mas com bloqueio externo persistente.

Observação:

- O coletor SofaScore v2 foi endurecido operacionalmente contra falhas.
- O HTTP 403 persistiu na retomada da partida 51.
- A coleta massiva deve permanecer pausada até nova decisão operacional.

#### FotMob

Status:
Parcialmente operacional.

#### API-Football

Status:
Em avaliação como fonte alternativa/complementar.

Observação:

- Possui plano gratuito limitado a 100 requests/dia.
- Deve ser tratada inicialmente como spike controlado, não como substituição imediata do SofaScore.

---

## Coleta SofaScore

### Implementado

- sofascore_season_collector.py
- sofascore_match_collector.py
- v2_sofascore_match_collector.py

### Artefatos Gerados

- inventory.json
- rounds.json
- round_XX_events.json

### Resultado Atual

- 381 partidas descobertas da EPL.
- 50 partidas coletadas com sucesso.
- 250+ JSONs armazenados localmente.
- Correção operacional do coletor v2 implementada no commit `54bbb14`.

### Correção Operacional do Coletor v2

Implementado:

- checkpoint por endpoint;
- validação de JSON existente;
- skip de JSON válido sem sobrescrita;
- backup de JSON inválido em `_invalid_json_backup`;
- log auditável em `data/raw/sofascore/premier_league_61627/collection_log.jsonl`;
- retry/backoff para HTTP 429, HTTP 5xx, timeout e falhas temporárias;
- HTTP 403 registra `blocked` e encerra o lote;
- parâmetros operacionais como `--limit`, `--dry-run`, `--list-pending`, delays e jitter.

Resultado do teste:

- A correção funcionou operacionalmente.
- O SofaScore ainda retornou HTTP 403 na retomada da partida 51.

---

## Perfis de Coleta SofaScore em Discussão

### Perfil Full

Coleta completa originalmente considerada:

- `event.json`
- `statistics.json`
- `incidents.json`
- `lineups.json`
- `h2h.json`

### Perfil Core

Perfil recomendado para avaliação operacional com menor volume de requests:

- `event.json`
- `statistics.json`
- `incidents.json`

Motivo:

- reduz de 5 para 3 requests por partida;
- representa aproximadamente 40% menos requests por partida;
- preserva os dados essenciais para importer inicial, target de gols tardios e primeiras análises.

Observação:

- `lineups.json` e `h2h.json` não devem ser removidos da arquitetura.
- Eles devem permanecer como complementares para coleta futura.

---

## Coleta Minuto a Minuto / Graph

Status:

- Ainda não implementada.

Interpretação operacional:

- `incidents.json` fornece eventos com minuto, como gols, cartões e substituições.
- Isso não equivale a série temporal minuto a minuto completa.
- Momentum/pressão temporal depende de `graph.json` ou endpoint equivalente.

Estimativa preliminar:

- Se o graph/momentum vier em um único endpoint por partida, será aproximadamente 1 request adicional por partida.
- Com perfil core + graph, a coleta passaria de 3 para 4 requests por partida.
- A estimativa deve ser confirmada pelo Data Acquisition Engineer antes de implementação.

---

## Banco de Dados

Tabelas principais:

- matches_master
- match_statistics
- match_incidents
- match_graph
- match_mapping

Status:
Estrutura pronta.

Observação:

- `match_graph` está preparada, mas a coleta do endpoint graph ainda não foi implementada.

---

## Hipóteses Ativas

- H1 xG Pré-Jogo
- H2 Forecast Pré-Jogo
- H3 Força Ofensiva
- H4 Fragilidade Defensiva
- H5 Pressão Ofensiva In-Game
- H6 Estado Atual da Partida
- H7 Combinação Multi-Fonte
- H8 Momentum e Pressão Temporal
- H9 Eventos Alteram Probabilidade

Documento principal:

- `docs/04_RESEARCH/LATE_GOAL_HYPOTHESES.md`

---

## Bloqueios Atuais

### HTTP 403 SofaScore

Observado após alto volume de requisições e persistente na retomada controlada da partida 51.

Hipóteses:

- Rate limiting
- Session limiting
- IP limiting

Status:

- Bloqueio externo ainda ativo.
- Coleta SofaScore massiva pausada.
- Próxima decisão deve envolver Data Acquisition Engineer e CTO.

---

## Próximo Marco

1. Decidir estratégia operacional para SofaScore após persistência do 403.
2. Avaliar coleta core de 3 JSONs por partida.
3. Avaliar spike controlado da API-Football como fonte alternativa/complementar.
4. Considerar iniciar importer PostgreSQL com as 50 partidas já coletadas.
5. Finalizar EPL completa quando a coleta estiver operacionalmente estável.
6. Implementar sofascore_importer.py.
7. Popular PostgreSQL.
8. Construir features.
9. Validar hipóteses H1-H9.

---

## Objetivo da Próxima Fase

Transição controlada da fase de coleta para a fase de engenharia de dados e pesquisa quantitativa, sem depender de uma única fonte e sem pressionar fontes externas bloqueadas.
