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

#### SofaScore

Status:
Operacional para coleta.

#### FotMob

Status:
Parcialmente operacional.

---

## Coleta SofaScore

### Implementado

- sofascore_season_collector.py
- sofascore_match_collector.py

### Artefatos Gerados

- inventory.json
- rounds.json
- round_XX_events.json

### Resultado Atual

- 381 partidas descobertas da EPL.
- 50 partidas coletadas com sucesso.
- 250+ JSONs armazenados localmente.

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

---

## Bloqueios Atuais

### HTTP 403 SofaScore

Observado após alto volume de requisições.

Hipóteses:

- Rate limiting
- Session limiting
- IP limiting

Status:
Em investigação.

---

## Próximo Marco

1. Resolver HTTP 403.
2. Finalizar EPL completa.
3. Implementar sofascore_importer.py.
4. Popular PostgreSQL.
5. Construir features.
6. Validar hipóteses H1-H9.

---

## Objetivo da Próxima Fase

Transição da fase de coleta para a fase de engenharia de dados e pesquisa quantitativa.