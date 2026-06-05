# PROJECT STATUS

## Etapas do Projeto

1. Organizacao
2. Inventario das Fontes
3. Coleta Bruta
4. Banco de Dados
5. Integracao Multi-Fonte
6. Catalogo de Features
7. Engenharia de Features
8. Definicao do Alvo
9. Dataset Analitico
10. Pesquisa Quantitativa
11. Modelagem
12. Producao

---

## Concluido

- Estrutura documental do projeto consolidada.
- Governanca de agentes criada em `docs/00_AGENTS/AGENT_COORDINATION.md`.
- Perfil do PM criado em `docs/00_AGENTS/PM_PROFILE.md`.
- Documento base de hipoteses criado em `docs/04_RESEARCH/ACTIVE/LATE_GOAL_HYPOTHESES.md`.
- Understat integrado.
- FotMob integrado parcialmente.
- EPL 2024/2025 descoberta via SofaScore com 381 partidas no inventory.
- Match Mapping criado.
- PostgreSQL configurado.
- SQLAlchemy configurado.
- Tabelas `match_mapping`, `matches_master`, `match_statistics`, `match_incidents` e `match_graph` criadas.
- Coletor SofaScore v2 endurecido operacionalmente no commit `54bbb14`.
- Coletor SofaScore v3 core criado para reduzir volume de requests.
- Coleta SofaScore validada via 5G sem novo HTTP 403 em mais de 100 partidas.
- Auditoria local SofaScore EPL concluida.
- `sofascore_importer.py` implementado no commit `84e641f`.
- PostgreSQL populado com 380 partidas SofaScore importaveis.
- Idempotencia do importer validada com segunda execucao sem duplicacao.
- Validacao leve de qualidade concluida com status: APTO COM RESSALVAS.
- Desenho metodologico do Dataset Analitico V1 definido em `docs/04_RESEARCH/ANALYTICAL_DATASET_V1.md`.
- Dataset Builder V1 implementado no commit `1a1404e09079f2a1a7958ae948fefdc667872a50`.
- Dataset Analitico V1 gerado com 380 linhas e status APTO COM RESSALVAS.
- Target Audit concluido: `target_late_goal_75` com 189 positivos e 191 negativos.
- Validacao Estatistica Inicial H6/H9 concluida e revisada pelo Quant Research.
- Validacao H1/H2 preparada e corretamente bloqueada por risco confirmado de data leakage.

---

## Estado Atual da Coleta SofaScore

Resultado auditado:

- Total no inventory: 381 partidas.
- Total de pastas locais: 381.
- Partidas full: 192.
- Partidas core: 188.
- Total importavel: 380.
- Partidas faltantes: 0.
- Partidas incompletas relevantes: 1.
- Partida descartada da importacao atual: `12436452`.

Observacoes:

- A partida `12436449` foi corrigida/coletada e entrou como importavel.
- `lineups.json` e `h2h.json` permanecem preservados como dados brutos complementares.
- A estrategia core reduziu o volume de requests por partida de 5 para 3.

---

## Estado Atual da Importacao PostgreSQL

Tabelas populadas nesta etapa:

- `matches_master`
- `match_statistics`
- `match_incidents`

Contagens finais:

- `matches_master`: 380 partidas.
- `match_statistics`: 380 partidas.
- `match_incidents`: 7647 registros.
- Registros para `12436452`: 0.
- Orfaos em `match_statistics`: 0.
- Orfaos em `match_incidents`: 0.
- Partidas importadas sem estatisticas: 0.

Fora do escopo desta importacao:

- `match_graph`
- lineups
- h2h
- features avancadas
- modelagem

---

## Validacao Leve de Qualidade

Status:

- APTO COM RESSALVAS.

Resultados:

- Nao existem orfaos.
- Nao existem divergencias entre placar e incidentes.
- 16 partidas sem gols sao compativeis com o placar.
- `big_chances_home` possui 7 nulos.
- `big_chances_away` possui 7 nulos.

Interpretacao:

- A base esta apta com ressalvas para Dataset Analitico V1.
- As colunas `big_chances_home` e `big_chances_away` devem ser tratadas com ressalva e nao devem ser usadas como feature obrigatoria sem regra documentada de nulos.
- `match_graph`, lineups e h2h permanecem fora do core v1.

---

## Dataset Analitico V1

Status:

- Gerado.
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
- Colunas target-derived nao podem ser usadas como features.
- `big_chances_home` e `big_chances_away` possuem 7 nulos cada.

---

## Colunas Proibidas como Features nesta Etapa

Target-derived:

- `has_late_goal`
- `target_late_goal_75`
- `late_goal_count_75`
- `home_late_goal_count_75`
- `away_late_goal_count_75`
- `first_late_goal_minute_75`

Placar final / resultado final, proibidos como preditores:

- `home_goals`
- `away_goals`
- `total_goals`

Estatisticas finais da propria partida sao proibidas como preditores in-game.

---

## Validacao Estatistica Inicial H6/H9

Status:

- Concluida e aprovada pelo PM.

Documento:

- `docs/04_RESEARCH/INITIAL_STATISTICAL_VALIDATION_H6_H9.md`

Dataset utilizado:

- `late_goal_dataset_v1b_ingame`
- 1900 linhas
- 380 partidas
- cutoffs: 60, 65, 70, 75, 80
- target: `target_goal_after_cutoff`

Resultado H6 — Estado da Partida:

Manter:

- `score_diff_home_until_cutoff`
- `score_state_group`

Observar:

- `total_goals_until_cutoff`
- `time_since_last_goal_until_cutoff`

Descartar nesta amostra:

- `is_draw_until_cutoff`
- `home_leading_until_cutoff`
- `away_leading_until_cutoff`

Resultado H9 — Eventos:

Manter:

- `cards_until_cutoff`
- `substitutions_until_cutoff`

Observar:

- `goal_last_10m_until_cutoff`

Descartar nesta amostra:

- `goal_last_5m_until_cutoff`

Ressalva:

- `red_cards_until_cutoff` e `yellow_cards_until_cutoff` nao foram usados porque estao nulos por design.

---

## Validacao Estatistica H1/H2

Status:

- BLOQUEADA.

Documento:

- `docs/04_RESEARCH/STATISTICAL_VALIDATION_H1_H2.md`

Conclusao Quant:

- H1/H2 nao devem ser testadas estatisticamente ainda.

Motivo:

- Risco confirmado de data leakage.

Variaveis bloqueadas:

- `matches.home_xg`
- `matches.away_xg`
- `team_match_stats.xg`
- `team_match_stats.xga`
- `forecast_*`

Detalhes:

- `matches.home_xg` e `matches.away_xg` representam xG final da propria partida.
- `team_match_stats.xg/xga` sao estatisticas finais por time por partida.
- `forecast_*` vem junto do registro final Understat e nao foi comprovado como pre-kickoff.
- `matches_master` possui 0 valores nao nulos em xG/forecast.
- Nao ha probabilidades pre-jogo seguras nos artefatos atuais.

Decisao do PM:

- H1 bloqueada.
- H2 bloqueada.
- Nao usar xG da propria partida como feature pre-jogo.
- Nao usar forecast sem comprovacao pre-kickoff.
- Nao iniciar modelagem.

Nova exigencia:

- H1/H2 somente poderao ser retomadas apos construcao de dataset historico pre-jogo sem leakage.

---

## Em Andamento

### Avaliacao Metodologica H3/H4

Objetivo:

Determinar se H3 e H4 podem ser implementadas sem leakage utilizando apenas historico anterior ao jogo.

Regras:

- H3/H4 nao podem usar estatisticas finais da propria partida.
- H3/H4 so podem utilizar rolling windows, medias historicas ou metricas acumuladas ate antes da data da partida.
- Nao criar codigo, datasets executaveis ou modelagem antes de aprovacao metodologica.

---

### API-Football

Objetivo:

Avaliar como fonte alternativa/complementar ao SofaScore.

Status:

- Spikes controlados executados.
- API-Football permanece como complemento candidato, nao como substituta oficial do SofaScore.

---

## Proximas Etapas

1. Quant Research / Data Science avaliar H3/H4 sob regra anti-leakage.
2. Definir se forca ofensiva e fragilidade defensiva podem ser construidas usando historico anterior ao jogo.
3. Manter H1/H2 bloqueadas ate existir dataset pre-jogo seguro.
4. Iniciar feature engineering somente apos aprovacao metodologica.
5. Iniciar modelagem apenas depois de dataset e features aprovados.
6. Backtesting apenas depois de baseline validado.
7. Producao apenas em etapa futura.

---

## Descobertas Recentes

- SofaScore fornece dados suficientes para base core EPL em 380 partidas.
- Perfil core reduziu volume de requests e funcionou operacionalmente via 5G.
- A partida `12436452` deve permanecer fora da importacao atual.
- Importer SofaScore core e retomavel/idempotente.
- Base PostgreSQL esta apta com ressalvas para Dataset Analitico V1.
- Dataset Builder V1 gerou CSV, Parquet, metadata e validation report.
- `target_late_goal_75` foi criado com 189 positivos e 191 negativos.
- H6/H9 apresentaram primeiras features promissoras em dados reais.
- H1/H2 foram corretamente bloqueadas por data leakage.
- Estatisticas full-match exigem ressalva de leakage antes de qualquer uso preditivo.
- Nenhuma modelagem foi iniciada.
- `match_graph` segue pendente porque ainda nao ha `graph.json` coletado.
