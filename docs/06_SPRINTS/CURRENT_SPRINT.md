# CURRENT SPRINT

## Sprint Atual

Objetivo:

Concluir a transicao da base SofaScore EPL core importada para o primeiro Dataset Analitico V1 e preparar auditoria Quant Research / Data Science sem iniciar modelagem.

---

## Concluido

- [x] Criar sofascore_season_collector.py
- [x] Criar sofascore_match_collector.py
- [x] Descobrir temporada EPL
- [x] Gerar inventory.json
- [x] Gerar rounds.json
- [x] Gerar event.json
- [x] Gerar statistics.json
- [x] Gerar incidents.json
- [x] Gerar lineups.json quando disponivel
- [x] Gerar h2h.json quando disponivel
- [x] Implementar correcao operacional para HTTP 403 no coletor SofaScore v2
- [x] Executar teste operacional controlado de retomada
- [x] Validar coleta via 5G sem novo HTTP 403
- [x] Criar coletor SofaScore v3 em perfil core
- [x] Consolidar inventario real de partidas full/core
- [x] Confirmar total final contra o inventario de 381 partidas
- [x] Implementar sofascore_importer.py
- [x] Popular PostgreSQL com dados SofaScore core
- [x] Validar idempotencia do importer
- [x] Validar integridade basica entre matches_master, match_statistics e match_incidents
- [x] Concluir e validar a frente Importacao PostgreSQL SofaScore EPL pela area Data Engineer / Database
- [x] Criar validacao leve de qualidade pos-importacao
- [x] Gerar relatorio de qualidade dos dados importados
- [x] Definir desenho metodologico do Dataset Analitico V1
- [x] Implementar Dataset Builder V1
- [x] Gerar Dataset Analitico V1 com CSV, Parquet, metadata e validation report
- [x] Documentar Dataset Builder V1

---

## Atualizacao Operacional Mais Recente

O Dataset Analitico V1 foi gerado a partir do PostgreSQL local, sem escrita no banco, sem alteracao de schema, sem coleta adicional, sem importer e sem modelagem.

Script:

- `LateGoalResearch/Analytics/DatasetBuilder/dataset_builder_v1.py`

Commit:

- `1a1404e09079f2a1a7958ae948fefdc667872a50` - Cria Dataset Builder V1.

Artefatos locais gerados:

- `data/processed/datasets/late_goal_dataset_v1.csv`
- `data/processed/datasets/late_goal_dataset_v1.parquet`
- `data/processed/datasets/late_goal_dataset_v1_metadata.json`
- `data/processed/datasets/late_goal_dataset_v1_validation_report.json`

Status:

- APTO COM RESSALVAS.

Resumo:

- Linhas: 380.
- Grain: 1 linha por partida.
- Target principal: `target_late_goal_75`.
- Alias operacional: `has_late_goal`.
- Target positivo: 189.
- Target negativo: 191.
- Duplicatas por `match_id`: 0.
- Duplicatas por `sofascore_event_id`: 0.

---

## Auditoria Local SofaScore EPL

Resultado confirmado:

- Total no inventory: 381 partidas.
- Total de pastas locais: 381.
- Partidas full: 192.
- Partidas core: 188.
- Total importavel: 380.
- Partidas faltantes: 0.
- Partidas incompletas relevantes: 1.
- Partida descartada da importacao atual: `12436452`.

Observacao:

- A partida `12436449` foi corrigida/coletada com os 3 dados core e foi considerada importavel.

---

## Importacao PostgreSQL

Script:

- `LateGoalResearch/Crawler/Sofascore/sofascore_importer.py`

Commit:

- `84e641f` - Implementa importer SofaScore core.

Escopo importado:

- `matches_master`
- `match_statistics`
- `match_incidents`

Banco populado:

- `matches_master`: 380.
- `match_statistics`: 380.
- `match_incidents`: 7647.

Validacoes de integridade:

- Duplicatas em `matches_master`: 0.
- Duplicatas em `match_statistics`: 0.
- Orfaos em `match_statistics`: 0.
- Orfaos em `match_incidents`: 0.
- `12436452`: 0 registros nas tres tabelas.

Fora do escopo:

- `match_graph`
- lineups
- h2h
- features avancadas
- modelagem

Status:

- CONCLUIDO E VALIDADO.

---

## Dataset Analitico V1

Documentacao:

- `docs/04_RESEARCH/ANALYTICAL_DATASET_V1.md`
- `docs/04_RESEARCH/DATASET_BUILDER_V1.md`

Ressalvas:

- Estatisticas full-match de `match_statistics` possuem risco de leakage para uso in-game.
- `big_chances_home` possui 7 nulos.
- `big_chances_away` possui 7 nulos.
- Colunas target-derived nao podem ser usadas como features.

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

## Em Andamento

- [ ] Auditoria Quant Research / Data Science do Dataset Analitico V1
- [ ] Validar coerencia do target `target_late_goal_75`
- [ ] Classificar colunas por risco de leakage
- [ ] Separar identificadores, colunas de auditoria e potenciais features
- [ ] Propor primeira bateria exploratoria para H1/H2/H6/H9
- [ ] Recomendar seguir, seguir com ressalvas ou revisar Dataset V1

---

## Proxima Frente Aprovada pelo PM

Acionar Quant Research / Data Science para auditoria exploratoria inicial do Dataset V1.

Objetivo:

Confirmar que o target e a estrutura do dataset estao adequados para a proxima decisao metodologica.

Restricoes:

- Nao iniciar modelagem.
- Nao iniciar backtesting.
- Nao criar features avancadas H1-H9 sem aprovacao.
- Nao alterar banco.
- Nao alterar schema.
- Nao alterar collectors, importers ou dados brutos.

---

## Proximos Passos

- [ ] Quant Research / Data Science auditar o Dataset Analitico V1
- [ ] Registrar resultado da auditoria do target
- [ ] Atualizar documentacao de pesquisa com classificacao de colunas
- [ ] Definir se o Dataset V1 pode seguir para analises exploratorias
- [ ] Iniciar feature engineering somente apos aprovacao metodologica
- [ ] Iniciar modelagem apenas depois de dataset e features aprovados

---

## Resultado Esperado

Dataset Analitico V1 auditado, com target validado e riscos de leakage documentados antes de qualquer feature engineering avancada ou modelagem.

---

## Status

EM EXECUCAO - DATASET ANALITICO V1 GERADO; PROXIMA FRENTE: AUDITORIA QUANT RESEARCH / DATA SCIENCE.
