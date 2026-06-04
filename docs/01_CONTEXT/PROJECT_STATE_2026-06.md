# PROJECT STATE 2026-06

## Visao Geral

Projeto:

LateGoalResearch

Objetivo:

Descobrir padroes quantitativos capazes de antecipar gols tardios atraves da integracao de multiplas fontes de dados.

---

## Estado Atual

### Infraestrutura

- PostgreSQL configurado.
- SQLAlchemy configurado.
- Configuracao centralizada em `config/database.py`.

### Fontes

#### Understat

Status:
Operacional.

Uso atual:

- Fonte principal para xG, xGA, forecast, PPDA e metricas pre-jogo.

#### SofaScore

Status:
Operacional para base historica core EPL.

Resumo atual:

- Temporada EPL 2024/25 descoberta com 381 partidas.
- 381 pastas locais de partidas existentes.
- 192 partidas full com 5 JSONs.
- 188 partidas core com 3 JSONs.
- 380 partidas importaveis.
- 1 partida descartada da importacao atual: `12436452`.

Observacoes:

- O coletor v2 foi endurecido operacionalmente contra falhas.
- O coletor v3 core foi criado para reduzir volume de requests.
- A coleta via 5G rodou sem novo HTTP 403 em mais de 100 partidas.
- O risco de novo bloqueio por volume/conexao ainda deve ser considerado em coletas futuras.

#### FotMob

Status:
Parcialmente operacional.

#### API-Football

Status:
Em avaliacao como fonte alternativa/complementar.

Observacao:

- Spikes controlados foram executados.
- API-Football permanece como complemento candidato, nao como substituta oficial do SofaScore.

---

## Coleta SofaScore

### Implementado

- `sofascore_season_collector.py`
- `sofascore_match_collector.py`
- `v2_sofascore_match_collector.py`
- `v3_sofascore_match_collector.py`

### Artefatos Gerados

- `inventory.json`
- `rounds.json`
- `round_XX_events.json`
- `event.json`
- `statistics.json`
- `incidents.json`
- `lineups.json`, quando em perfil full
- `h2h.json`, quando em perfil full

### Perfis de Coleta

#### Perfil Full

- `event.json`
- `statistics.json`
- `incidents.json`
- `lineups.json`
- `h2h.json`

#### Perfil Core

- `event.json`
- `statistics.json`
- `incidents.json`

Motivo do perfil core:

- reduz de 5 para 3 requests por partida;
- diminui risco operacional de novo HTTP 403;
- preserva dados essenciais para importer inicial, target e primeiras validacoes.

---

## Banco de Dados

Tabelas principais:

- `matches_master`
- `match_statistics`
- `match_incidents`
- `match_graph`
- `match_mapping`

### Importacao SofaScore Core

Status:
Implementada e executada.

Script:

- `LateGoalResearch/Crawler/Sofascore/sofascore_importer.py`

Commit:

- `84e641f` - Implementa importer SofaScore core

Tabelas populadas:

- `matches_master`
- `match_statistics`
- `match_incidents`

Contagens finais:

- `matches_master`: 380 eventos distintos.
- `match_statistics`: 380 eventos distintos.
- `match_incidents`: 7647 registros, cobrindo 380 eventos.
- Registros para `12436452`: 0.
- Orfaos em `match_statistics`: 0.
- Orfaos em `match_incidents`: 0.

Idempotencia:

- Primeira execucao: 380 inserts, 0 falhas.
- Segunda execucao: 380 updates, 0 inserts, 0 falhas.
- Nao houve duplicacao de partidas/statistics.

### match_graph

Status:
Estrutura pronta, mas nao populada.

Observacao:

- Ainda nao ha `graph.json` ou endpoint equivalente coletado/importado.

---

## Hipoteses Ativas

- H1 xG Pre-Jogo
- H2 Forecast Pre-Jogo
- H3 Forca Ofensiva
- H4 Fragilidade Defensiva
- H5 Pressao Ofensiva In-Game
- H6 Estado Atual da Partida
- H7 Combinacao Multi-Fonte
- H8 Momentum e Pressao Temporal
- H9 Eventos Alteram Probabilidade

Documento principal:

- `docs/04_RESEARCH/LATE_GOAL_HYPOTHESES.md`

---

## Bloqueios / Atencao

### SofaScore HTTP 403

Historico:

- HTTP 403 apareceu apos alto volume de requisicoes.
- Evidencia recente indica relacao forte com IP/conexao e volume.
- Coleta via 5G e perfil core rodou sem novo bloqueio relevante.

Status atual:

- Nao ha bloqueio ativo impedindo uso da base coletada/importada.
- Coletas futuras ainda devem respeitar baixo volume, checkpoint, retry/backoff e perfil core quando possivel.

### Graph / Momentum

Status:

- Pendente.
- H8 depende de `match_graph` ou fonte equivalente para momentum/pressao temporal.

---

## Proximo Marco

1. Validar amostras importadas no PostgreSQL.
2. Revisar qualidade dos dados em `match_statistics` e `match_incidents`.
3. Decidir com CTO/Data Engineer se a proxima frente sera graph, importacao complementar ou catalogo de features.
4. Implementar novas etapas apenas apos aprovacao de escopo.
5. Preparar base para features H1-H9 sem misturar coleta, importacao e modelagem.

---

## Objetivo da Proxima Fase

Validar a base SofaScore core importada e preparar a transicao controlada para engenharia de features/dataset analitico, mantendo dados brutos preservados e evitando dependencia de uma unica fonte.
