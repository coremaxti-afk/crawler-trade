# GITHUB_AUDIT_20260616

## Objetivo

Registrar a auditoria entre:

- pasta operacional local `C:\LateGoalResearch`
- repositorio remoto `coremaxti-afk/crawler-trade`

 e definir o que deve ser sincronizado para o GitHub sem perder contexto remoto existente.

---

## Achados principais

### 1. A pasta local nao esta inicializada como Git

Em `C:\LateGoalResearch` nao existe `.git` na raiz.

Implicacao:

- nao ha historico local conectado diretamente ao GitHub;
- nao e possivel usar `git status`, `git add`, `git commit` e `git push` diretamente nessa pasta;
- a sincronizacao precisa ser feita com cuidado para nao sobrescrever o que ja existe no remoto.

### 2. O remoto existe e esta acessivel pelo conector

Repositorio identificado:

```text
coremaxti-afk/crawler-trade
branch padrao: main
```

O GitHub app confirmou permissao de `push`, mas o `git` local por HTTPS nao conseguiu autenticar no repositorio privado.

### 3. O GitHub nao esta espelhando a estrutura local atual

O remoto possui pelo menos:

- `docs/01_CONTEXT/PROJECT_STATUS.md`
- `docs/06_SPRINTS/CURRENT_SPRINT.md`

Esses caminhos nao existiam localmente antes desta auditoria e foram restaurados localmente a partir do remoto.

Ao mesmo tempo, arquivos centrais hoje usados na operacao local retornaram `404` no remoto, incluindo:

- `Crawler/Sportmonks/run_sportmonks_full_season_collector.py`
- `Crawler/FootballData/run_football_data_odds_collector.py`
- `Crawler/Sportmonks/run_strategy_discovery_v2.py`
- `scripts/research/run_strategy_drawdown.py`
- `scripts/research/calc_strategy_drawdown.py`
- `docs/04_RESEARCH/CHAT_HANDOFF_TECHNICAL_SUMMARY_20260616.md`
- `docs/04_RESEARCH/CHAT_HANDOFF_QUICKSTART_20260616.md`
- `docs/04_RESEARCH/TUTORIAL SCRIPTS/RUNNERS_OPERACIONAIS_COLETA_E_DISCOVERY.md`
- `data/raw/football_data/football_data_league_odds_map.csv`
- `data/raw/sportmonks/league_season_map/league_last_3_seasons.json`

Conclusao:

```text
o repositorio GitHub esta desatualizado em relacao ao pipeline operacional atual
```

### 4. Ha desvio estrutural entre local e remoto

Localmente, `docs` hoje contem:

- `03_SOURCES`
- `04_RESEARCH`
- `08_DATABASE`

No remoto, ha pelo menos:

- `01_CONTEXT`
- `06_SPRINTS`

Implicacao:

- o sincronismo correto nao e sobrescrever a arvore remota;
- e necessario fazer merge de contexto remoto + ativos locais novos.

### 5. Ha artefatos locais que nao devem ser tratados como codigo principal

Exemplos encontrados localmente:

- `__pycache__`
- arquivos temporarios como `_tmp_playbook_refinement_v1.py`
- variantes operacionais pontuais de coletores por liga
- CSVs detalhados grandes de entries/trades

Esses itens exigem selecao antes de publicar.

---

## Arquivos locais de maior prioridade para publicar

### Codigo

- `Crawler/FootballData/football_data_odds_collector.py`
- `Crawler/FootballData/run_football_data_odds_collector.py`
- `Crawler/Sportmonks/run_sportmonks_full_season_collector.py`
- `Crawler/Sportmonks/run_strategy_discovery_v2.py`
- `Crawler/Sportmonks/sportmonks_team_side_strategy_discovery_v2 editado.py`
- `scripts/research/calc_strategy_drawdown.py`
- `scripts/research/run_strategy_drawdown.py`

### Mapas e configuracao operacional

- `data/raw/football_data/football_data_league_odds_map.csv`
- `data/raw/sportmonks/league_season_map/league_last_3_seasons.json`

### Documentacao e handoff

- `docs/03_SOURCES/ODDS/RUN_FOOTBALL_DATA_ODDS_COLLECTOR_SIMPLIFICADO.md`
- `docs/04_RESEARCH/CHAT_HANDOFF_TECHNICAL_SUMMARY_20260616.md`
- `docs/04_RESEARCH/CHAT_HANDOFF_QUICKSTART_20260616.md`
- `docs/04_RESEARCH/STRATEGY_NAMING_AND_DEFINITIONS_REFERENCE_V1.md`
- `docs/04_RESEARCH/TUTORIAL SCRIPTS/FOOTBALL_DATA_ODDS_COLLECTOR.md`
- `docs/04_RESEARCH/TUTORIAL SCRIPTS/RUN_SPORTMONKS_FULL_SEASON_COLLECTOR_SIMPLIFICADO.md`
- `docs/04_RESEARCH/TUTORIAL SCRIPTS/RUN_STRATEGY_DISCOVERY_V2_SIMPLIFICADO.md`
- `docs/04_RESEARCH/TUTORIAL SCRIPTS/RUN_STRATEGY_DRAWDOWN_SIMPLIFICADO.md`
- `docs/04_RESEARCH/TUTORIAL SCRIPTS/RUNNERS_OPERACIONAIS_COLETA_E_DISCOVERY.md`
- `docs/04_RESEARCH/GITHUB_AUDIT_20260616.md`

### Relatorios pequenos e uteis para versao

- `data/processed/reports/strategy_naming_definitions_reference_v1.csv`
- `data/processed/reports/sportmonks_team_side_strategy_discovery_summary_v2_la_liga_2025_26_tempos_expandidos.csv`
- `data/processed/reports/strategy_drawdown_summary_la_liga_2025_26_tempos_expandidos.csv`

---

## Arquivos grandes que pedem criterio

Os seguintes artefatos existem localmente, mas sao grandes:

- `data/processed/reports/sportmonks_team_side_strategy_discovery_entries_v2_la_liga_2025_26_tempos_expandidos.csv` ~ 29 MB
- `data/processed/reports/strategy_drawdown_trades_la_liga_2025_26_tempos_expandidos.csv` ~ 17 MB

Eles podem ser versionados, mas nao sao bons candidatos para sincronizacao manual via conector arquivo a arquivo.

---

## Risco identificado no remoto

O remoto possui contexto de projeto que nao estava na pasta local, e um dos documentos remotos referencia:

```text
sportmonks_team_side_strategy_discovery_summary_v2_la_liga_2025_26_tempos_expandidos222.csv
```

Enquanto o arquivo local atual usa:

```text
sportmonks_team_side_strategy_discovery_summary_v2_la_liga_2025_26_tempos_expandidos.csv
```

Isso sugere pelo menos uma referencia remota stale/inconsistente que deve ser corrigida numa sincronizacao posterior.

---

## Decisao desta auditoria

Sincronizar primeiro:

- codigo principal dos runners e scripts
- mapas operacionais
- documentacao e handoff
- relatorios compactos e de leitura executiva

Evitar publicar junto, sem necessidade:

- `__pycache__`
- temporarios
- copias auxiliares
- CSVs detalhados grandes via fluxo manual arquivo a arquivo

---

## Proximo passo

Publicar automaticamente no GitHub, preservando os arquivos remotos ja existentes e adicionando os arquivos locais prioritarios que hoje nao estao no repositorio.
