# IMPORT PIPELINE

## Objetivo

Padronizar o fluxo de ingestão de dados do projeto Late Goal Research.

---

## Fluxo Geral

RAW
↓
Validação
↓
Transformação
↓
PostgreSQL
↓
Dataset Analítico
↓
Feature Engineering
↓
Modelagem

---

## Estado Atual

### Implementado

- understat collectors
- sofascore_season_collector.py
- sofascore_match_collector.py

### Em Desenvolvimento

- sofascore_importer.py

### Planejado

- feature_builder.py
- analytics_dataset_builder.py
- model_training_pipeline.py

---

## Understat

Status:
Implementado

Objetivo:
Fornecer métricas pré-jogo.

Dados disponíveis:

- Match ID
- Data
- Liga
- Temporada
- Home Team
- Away Team
- Home Goals
- Away Goals
- xG
- Forecast
- PPDA
- Deep
- xGA

Destino:

- matches_master

---

## SofaScore Season Collector

Status:
Implementado

Objetivo:

Descobrir todas as partidas de uma temporada.

Artefatos:

- inventory.json
- rounds.json
- round_01_events.json
- ...
- round_38_events.json

---

## SofaScore Match Collector V2

Status:
Implementado

Objetivo:

Coletar dados detalhados de cada partida.

Arquivos coletados:

- event.json
- statistics.json
- incidents.json
- lineups.json
- h2h.json

Estrutura:

matches/{event_id}/

- event.json
- statistics.json
- incidents.json
- lineups.json
- h2h.json

Funcionalidades:

- leitura de inventory.json
- coleta automática por event_id
- skip automático
- delay configurável
- processamento em lote

---

## PostgreSQL

Status:
Em desenvolvimento

Tabelas alvo:

- matches_master
- match_statistics
- match_incidents
- match_graph

---

## Próxima Etapa

Implementar:

sofascore_importer.py

Objetivo:

Importar JSONs coletados para PostgreSQL.

---

## Problemas Encontrados

### HTTP 403 SofaScore

Situação observada:

- 50 partidas coletadas com sucesso
- bloqueio após aproximadamente 250 requisições

Hipóteses:

- rate limiting
- session limiting
- IP limiting

Necessário investigar:

- coleta em lotes
- reinicialização de sessão
- pausas maiores
- possível troca de IP
