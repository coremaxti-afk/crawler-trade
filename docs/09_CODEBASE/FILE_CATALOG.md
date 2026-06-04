# FILE CATALOG

## SofaScore

### sofascore_client.py
Função: Cliente de acesso aos endpoints do SofaScore.

### sofascore_collector.py
Função: Coletar dados de uma única partida.
Saídas: event.json, statistics.json, incidents.json, lineups.json, h2h.json.

### sofascore_season_collector.py
Função: Inventariar todas as partidas de uma temporada.
Saída: inventory.json.

## Understat

### understat_import_epl.py
Função: Importar partidas EPL para a tabela matches.

### understat_import_team_stats.py
Função: Importar estatísticas avançadas para team_match_stats.

## FotMob

### fotmob_populate_match_ids.py
Função: Relacionar partidas Understat com IDs FotMob.

### snapshot_builder_v2.py
Função: Construir snapshots minuto a minuto para modelagem.
Saída: tabela snapshots.

---

Este catálogo deve ser atualizado sempre que novos scripts forem adicionados ao projeto.
