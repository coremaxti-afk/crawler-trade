# DATA MODEL V1

## Objetivo

Consolidar a visao macro do modelo de dados do projeto LateGoalResearch.

Este documento nao substitui as especificacoes detalhadas em `docs/08_DATABASE`; ele resume as principais entidades persistidas por fonte e o papel arquitetural de cada camada.

---

## Understat

### matches

Partidas historicas e metadados basicos oriundos da fonte Understat.

### team_match_stats

Estatisticas avancadas por equipe e partida, utilizadas principalmente para features historicas pre-match.

---

## FotMob

### fotmob_raw_matches

Camada RAW/staging para payloads FotMob preservados.

### events_v2

Eventos detalhados da partida.

### snapshots

Estados acumulados minuto a minuto.

### results

Targets historicos e resultados utilizados em datasets analiticos.

---

## SofaScore Core

### match_mapping

Relacionamento entre IDs das diferentes fontes.

### matches_master

Tabela mestre de identificacao das partidas e ponto central de integracao multi-fonte.

### match_statistics

Estatisticas agregadas da partida.

### match_incidents

Eventos e incidentes da partida, incluindo gols, cartoes, substituicoes, periodos e decisoes VAR quando disponiveis.

---

## SofaScore H8

### match_graph

Momentum minuto a minuto oriundo de `graph.json`.

### match_shotmap

Finalizacoes da partida oriundas de `shotmap.json`, incluindo minuto, time, jogador, tipo de finalizacao e metricas como xG/xGOT quando disponiveis.

### match_source_status

Controle de cobertura, status de fonte, artefato e excecoes conhecidas por partida.

Uso principal:

- registrar artefatos disponiveis e ausentes;
- preservar excecoes conhecidas;
- permitir que datasets excluam apenas outputs que exigem artefatos faltantes.

Excecao conhecida:

- `event_id 12437015`: `graph.json` indisponivel HTTP 404; manter partida para artefatos disponiveis e excluir apenas de outputs que exigem graph completo.

---

## Football-Data.co.uk

### football_data_staging

Camada de ingestao do CSV Football-Data preservando linha original, versao de arquivo, origem e rastreabilidade.

### football_data_match_mapping

Mapping entre linha Football-Data, `sofascore_event_id` e `match_id`/partida mestre.

### football_data_odds

Odds historicas pre-jogo normalizadas por mercado, bookmaker/agregador, selecao e tipo de preco.

Mercados contemplados:

- Match Odds / 1X2;
- Over/Under 2.5;
- Asian Handicap;
- opening-like/pre-close odds;
- closing odds;
- Avg odds;
- Max odds.

### football_data_import_runs

Controle de execucoes do importer, arquivo, hash, URL, timestamp, contagens e status de validacao.

Estado operacional atual:

- 380 partidas importadas;
- 34.280 odds finais;
- 0 duplicatas;
- 0 orfaos;
- 0 odds invalidas;
- idempotencia validada.

---

## Camadas Analiticas

### Feature Engineering

Camada responsavel por transformar dados persistidos em variaveis candidatas.

### Dataset Analitico

Camada de montagem de datasets versionados para pesquisa quantitativa.

### Pesquisa Quantitativa

Camada de avaliacao metodologica e experimental.

### Modelagem / Backtesting / Operacao

Camadas posteriores, dependentes de aprovacao explicita. Nao devem ser acionadas automaticamente pela existencia de uma fonte importada.

---

## Status

Estrutura principal atualizada para refletir:

- SofaScore Core;
- SofaScore H8 Graph/Shotmap;
- Football-Data odds;
- integracao multi-fonte em PostgreSQL;
- separacao entre persistencia, features, datasets, pesquisa, modelagem e operacao.
