# PIPELINE

## Visao Geral

Este documento descreve o pipeline macro do LateGoalResearch.

Principio central:

```text
RAW / Fonte externa
↓
Coleta ou ingestao
↓
PostgreSQL / camada persistida
↓
Feature Engineering
↓
Dataset Analitico
↓
Pesquisa Quantitativa
↓
Modelagem
↓
Backtesting
↓
Operacao
```

Nenhuma etapa analitica deve consumir diretamente arquivos RAW quando houver camada persistida validada.

---

## Fontes e Fluxos

### Understat

```text
Understat
↓
matches
team_match_stats
```

Uso principal:

- historico de partidas;
- estatisticas avancadas por equipe;
- apoio a features historicas pre-match.

---

### FotMob

```text
FotMob
↓
fotmob_raw_matches
↓
events_v2
↓
snapshots
↓
results
```

Uso principal:

- eventos detalhados;
- snapshots minuto a minuto;
- targets historicos.

---

### SofaScore Core

```text
SofaScore
↓
match_mapping
↓
matches_master
↓
match_statistics
match_incidents
```

Uso principal:

- tabela mestre multi-fonte;
- estatisticas agregadas;
- incidentes da partida;
- suporte a targets e features in-game.

---

### SofaScore H8 Graph / Shotmap

```text
SofaScore graph.json
↓
match_graph

SofaScore shotmap.json
↓
match_shotmap

Status de fonte
↓
match_source_status
```

Uso principal:

- momentum minuto a minuto;
- eventos de finalizacao;
- cobertura e excecoes por artefato;
- features H8.

Observacao operacional:

- `event_id 12437015` possui `graph.json` conhecido como indisponivel HTTP 404.
- A partida deve ser mantida para artefatos disponiveis e excluida apenas de outputs que exigem graph completo.

---

### Football-Data.co.uk

```text
Football-Data CSV
↓
football_data_staging
↓
football_data_match_mapping
↓
football_data_odds
↓
football_data_import_runs / rastreabilidade
```

Uso principal:

- odds historicas pre-jogo;
- Match Odds / 1X2;
- Over/Under 2.5;
- Asian Handicap;
- opening-like/pre-close odds;
- closing odds;
- Avg odds;
- Max odds.

Estado operacional:

- 380 partidas pareadas com SofaScore;
- 380 partidas importadas localmente;
- 34.280 odds finais;
- 0 duplicatas;
- 0 orfaos;
- 0 odds invalidas;
- idempotencia validada.

---

## Integracao Multi-Fonte

```text
Understat
FotMob
SofaScore Core
SofaScore H8
Football-Data
↓
PostgreSQL consolidado
↓
Feature Engineering
↓
Dataset Analitico
↓
Pesquisa Quantitativa
↓
Modelagem
↓
Backtesting
↓
Operacao
```

---

## Regras Arquiteturais

- Dados brutos sao preservados.
- Transformacoes devem ser reproduziveis.
- Cada etapa deve ser auditavel.
- Importers devem ser idempotentes.
- Fonte, arquivo, hash e data de importacao devem ser rastreaveis quando aplicavel.
- Nenhuma analise deve usar diretamente arquivos RAW quando existir camada persistida validada.
- Backtesting e producao seguem bloqueados ate aprovacao explicita.
