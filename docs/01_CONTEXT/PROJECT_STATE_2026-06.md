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
Implementada, executada e validada.

Script:

- `LateGoalResearch/Crawler/Sofascore/sofascore_importer.py`

Commit:

- `84e641f` - Implementa importer SofaScore core.

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

## Validacao de Qualidade

Status:

- APTO COM RESSALVAS.

Resultados principais:

- Nao existem orfaos.
- Nao existem divergencias entre placar e incidentes.
- 16 partidas sem gols sao compativeis com o placar.
- `big_chances_home` possui 7 nulos.
- `big_chances_away` possui 7 nulos.

---

## Dataset Analitico V1

Status:

- Implementado e gerado.
- APTO COM RESSALVAS.

Script:

- `LateGoalResearch/Analytics/DatasetBuilder/dataset_builder_v1.py`

Commit:

- `1a1404e09079f2a1a7958ae948fefdc667872a50` - Cria Dataset Builder V1.

Documentacao:

- `docs/04_RESEARCH/ANALYTICAL_DATASET_V1.md`
- `docs/04_RESEARCH/DATASET_BUILDER_V1.md`

Artefatos locais gerados:

- `data/processed/datasets/late_goal_dataset_v1.csv`
- `data/processed/datasets/late_goal_dataset_v1.parquet`
- `data/processed/datasets/late_goal_dataset_v1_metadata.json`
- `data/processed/datasets/late_goal_dataset_v1_validation_report.json`

Resumo validado:

- Linhas: 380.
- Grain: 1 linha por partida.
- Target principal: `target_late_goal_75`.
- Alias operacional: `has_late_goal`.
- Target positivo: 189.
- Target negativo: 191.
- Duplicatas por `match_id`: 0.
- Duplicatas por `sofascore_event_id`: 0.

Ressalvas:

- Estatisticas full-match de `match_statistics` possuem risco de leakage para uso in-game.
- Colunas target-derived nao podem ser usadas como features preditivas.
- `big_chances_home` e `big_chances_away` possuem 7 nulos cada.

Colunas target-derived proibidas como features:

- `has_late_goal`
- `target_late_goal_75`
- `late_goal_count_75`
- `home_late_goal_count_75`
- `away_late_goal_count_75`
- `first_late_goal_minute_75`

Colunas de placar final proibidas como preditores:

- `home_goals`
- `away_goals`
- `total_goals`

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

- `docs/04_RESEARCH/ACTIVE/LATE_GOAL_HYPOTHESES.md`

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

### Modelagem

Status:

- Nenhuma modelagem iniciada.
- Nenhum backtesting iniciado.
- Nenhum split treino/teste definido.

---

## Proximo Marco

1. Quant Research / Data Science auditar o Dataset Analitico V1.
2. Validar coerencia do target `target_late_goal_75`.
3. Classificar colunas por risco de leakage.
4. Definir a primeira bateria exploratoria para H1/H2/H6/H9.
5. Iniciar feature engineering somente apos aprovacao metodologica.
6. Iniciar modelagem apenas depois de dataset e features aprovados.

---

## Objetivo da Proxima Fase

Auditar o Dataset Analitico V1, consolidar regras de leakage e preparar a transicao controlada para analises exploratorias, mantendo dados brutos preservados e sem iniciar modelagem prematuramente.
