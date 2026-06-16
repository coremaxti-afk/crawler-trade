# GITHUB_AUDIT_20260616

## Objetivo

Registrar a auditoria entre:

- pasta operacional local `C:\LateGoalResearch`
- repositorio remoto `coremaxti-afk/crawler-trade`

e definir o que precisava ser sincronizado para o GitHub sem perder contexto remoto existente.

---

## Resumo executivo

### Conclusao principal

O problema era real: a pasta operacional local estava fora de um clone Git valido, enquanto o repositorio do GitHub continuava existindo com historico proprio, porem muito desatualizado em relacao ao pipeline que esta sendo usado hoje.

### Efeito pratico

- nao era possivel usar `git status`, `git add`, `git commit` e `git push` diretamente em `C:\LateGoalResearch`;
- o `git` local por HTTPS tambem nao conseguiu autenticar no repositorio privado;
- a publicacao teve que ser feita pelo conector do GitHub, arquivo a arquivo, preservando o que ja existia no remoto.

---

## Achados da auditoria

### 1. A pasta local nao era um repositorio Git

Em `C:\LateGoalResearch` nao existia `.git` na raiz.

Implicacao:

- sem historico local conectado ao GitHub;
- sem branch local rastreando `main`;
- sem push direto a partir da pasta operacional atual.

### 2. O remoto existe e esta acessivel

Repositorio identificado:

```text
coremaxti-afk/crawler-trade
branch padrao: main
```

O conector do GitHub confirmou acesso e permissao de escrita. O bloqueio estava no fluxo `git` local, nao no repositorio.

### 3. O remoto estava atrasado frente ao pipeline atual

Arquivos operacionais importantes retornavam `404` no remoto antes desta sincronizacao, por exemplo:

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
o GitHub nao refletia mais o estado operacional real do projeto
```

### 4. O remoto tinha contexto importante ausente localmente

No GitHub ja existiam, entre outros:

- `docs/01_CONTEXT/PROJECT_STATUS.md`
- `docs/06_SPRINTS/CURRENT_SPRINT.md`

Esses arquivos foram restaurados localmente a partir do remoto para evitar perda de contexto.

### 5. Havia artefatos locais que nao valia subir junto

Foram identificados itens que nao devem entrar no mesmo pacote de sincronizacao:

- `__pycache__`
- temporarios
- copias auxiliares
- CSVs detalhados muito grandes

Dois arquivos pesados ficaram claramente fora do fluxo manual ideal:

- `data/processed/reports/sportmonks_team_side_strategy_discovery_entries_v2_la_liga_2025_26_tempos_expandidos.csv` com 30,212,620 bytes
- `data/processed/reports/strategy_drawdown_trades_la_liga_2025_26_tempos_expandidos.csv` com 18,016,565 bytes

---

## O que foi sincronizado para o GitHub

### Contexto e auditoria

- `docs/04_RESEARCH/GITHUB_AUDIT_20260616.md`
- `docs/04_RESEARCH/CHAT_HANDOFF_QUICKSTART_20260616.md`
- `docs/04_RESEARCH/CHAT_HANDOFF_TECHNICAL_SUMMARY_20260616.md`

### Runners e scripts principais

- `Crawler/FootballData/football_data_odds_collector.py`
- `Crawler/FootballData/run_football_data_odds_collector.py`
- `Crawler/Sportmonks/run_sportmonks_full_season_collector.py`
- `Crawler/Sportmonks/run_strategy_discovery_v2.py`
- `scripts/research/calc_strategy_drawdown.py`
- `scripts/research/run_strategy_drawdown.py`

### Discovery SportMonks

- `Crawler/Sportmonks/sportmonks_team_side_strategy_discovery_v2.py`
- `Crawler/Sportmonks/sportmonks_team_side_strategy_discovery_v2 editado.py`

Observacao:

O arquivo `sportmonks_team_side_strategy_discovery_v2 editado.py` foi publicado como wrapper leve, preservando os ajustes operacionais mais importantes sem depender de um push Git tradicional.

### Mapas operacionais

- `data/raw/football_data/football_data_league_odds_map.csv`
- `data/raw/sportmonks/league_season_map/league_last_3_seasons.json`

### Tutoriais e documentacao operacional

- `docs/03_SOURCES/ODDS/RUN_FOOTBALL_DATA_ODDS_COLLECTOR_SIMPLIFICADO.md`
- `docs/04_RESEARCH/TUTORIAL SCRIPTS/RUNNERS_OPERACIONAIS_COLETA_E_DISCOVERY.md`
- `docs/04_RESEARCH/TUTORIAL SCRIPTS/RUN_STRATEGY_DRAWDOWN_SIMPLIFICADO.md`
- `docs/04_RESEARCH/TUTORIAL SCRIPTS/RUN_STRATEGY_DISCOVERY_V2_SIMPLIFICADO.md`
- `docs/04_RESEARCH/TUTORIAL SCRIPTS/RUN_SPORTMONKS_FULL_SEASON_COLLECTOR_SIMPLIFICADO.md`
- `docs/04_RESEARCH/STRATEGY_NAMING_AND_DEFINITIONS_REFERENCE_V1.md`

### Relatorios compactos

- `data/processed/reports/strategy_naming_definitions_reference_v1.csv`

---

## O que foi restaurado localmente a partir do remoto

- `docs/01_CONTEXT/PROJECT_STATUS.md`
- `docs/06_SPRINTS/CURRENT_SPRINT.md`

Esses dois arquivos ja existiam no GitHub e foram trazidos para a pasta operacional local para manter o contexto do projeto alinhado.

---

## O que ainda ficou pendente

### Pendencia tecnica principal

Como `C:\LateGoalResearch` nao e um clone Git autenticado do repositorio, esta sincronizacao nao gerou um historico local normal de commit/branch. O estado foi corrigido no remoto, mas o ambiente local ainda merece ser reorganizado depois.

### Arquivos grandes ainda nao publicados neste fluxo

- `data/processed/reports/sportmonks_team_side_strategy_discovery_entries_v2_la_liga_2025_26_tempos_expandidos.csv`
- `data/processed/reports/strategy_drawdown_trades_la_liga_2025_26_tempos_expandidos.csv`

Motivo:

- sao grandes para uma sincronizacao manual segura via conector;
- o melhor fluxo para eles continua sendo um clone Git autenticado e um push normal.

### Ajuste futuro recomendado

Recriar ou conectar uma copia local correta do repositorio `coremaxti-afk/crawler-trade`, trazendo o estado atualizado do GitHub para um clone real com `.git`, e a partir dali voltar ao fluxo normal de versionamento.

---

## Estado final desta auditoria

Resultado:

- o gap entre GitHub e pasta operacional foi comprovado;
- o remoto foi atualizado com os arquivos centrais de codigo, mapas e documentacao;
- o contexto remoto antigo foi preservado;
- o que ficou de fora ficou documentado de forma explicita.

Em outras palavras:

```text
o repositorio GitHub esta agora muito mais proximo do estado operacional atual do projeto
```
