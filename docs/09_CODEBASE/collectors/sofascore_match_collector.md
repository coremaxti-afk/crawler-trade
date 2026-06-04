# SOFASCORE MATCH COLLECTOR

## Arquivo

Crawler/Sofascore/sofascore_match_collector.py

---

## Objetivo

Realizar a coleta de dados detalhados de partidas individuais do SofaScore.

O coletor recebe um event_id e baixa todos os endpoints necessários para pesquisa quantitativa e futura integração com PostgreSQL.

---

## Entradas

### event_id

Identificador único da partida no SofaScore.

Origem:

- inventory.json
- round_XX_events.json

Gerados pelo sofascore_season_collector.py.

---

## Endpoints Coletados

### event.json

Informações gerais da partida.

### statistics.json

Estatísticas agregadas da partida.

### incidents.json

Timeline de eventos.

### lineups.json

Escalações e jogadores.

### h2h.json

Histórico de confrontos.

---

## Estrutura de Saída

Data/raw/sofascore/matches/{event_id}/

- event.json
- statistics.json
- incidents.json
- lineups.json
- h2h.json

---

## Funcionalidades

- Coleta automática por partida.
- Salvamento em JSON formatado.
- Controle de erros por endpoint.
- Skip automático para partidas já coletadas.
- Compatível com coleta em lote.

---

## Problemas Conhecidos

### HTTP 403

Observado após grande volume de requisições.

Hipóteses:

- Rate limiting.
- Session limiting.
- IP limiting.

Status:
Em investigação.

---

## Utilização

Etapa intermediária entre:

sofascore_season_collector.py
↓
sofascore_match_collector.py
↓
sofascore_importer.py

---

## Status

Ativo.