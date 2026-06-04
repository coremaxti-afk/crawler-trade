# DATASET BUILDER V1

## Status

Implementado e executado.

Status do dataset gerado:

- APTO COM RESSALVAS.

Commit de implementacao:

- `1a1404e09079f2a1a7958ae948fefdc667872a50` - Cria Dataset Builder V1.

---

## Objetivo

Gerar o primeiro dataset analitico do LateGoalResearch a partir das tabelas PostgreSQL ja populadas com dados SofaScore EPL 2024/25.

O builder cria uma linha por partida e define o target inicial de gol tardio.

---

## Script

- `LateGoalResearch/Analytics/DatasetBuilder/dataset_builder_v1.py`

Escopo tecnico:

- leitura de PostgreSQL via `config.database.engine`;
- uso de consultas `SELECT`;
- construcao de dataframe analitico;
- validacao basica do dataset;
- exportacao de CSV, Parquet, metadata e validation report.

Fora do escopo:

- alteracao de schema;
- escrita no banco;
- coleta de dados;
- importacao de JSON raw;
- criacao de features avancadas H1-H9;
- modelagem;
- backtesting.

---

## Fontes PostgreSQL

Tabelas lidas:

- `matches_master`
- `match_statistics`
- `match_incidents`

Contagens esperadas e validadas:

- `matches_master`: 380
- `match_statistics`: 380
- `match_incidents`: 7647

Partida ignorada conforme regra da importacao:

- `12436452`

---

## Artefatos Gerados

Arquivos locais gerados em `data/processed/datasets/`:

- `late_goal_dataset_v1.csv`
- `late_goal_dataset_v1.parquet`
- `late_goal_dataset_v1_metadata.json`
- `late_goal_dataset_v1_validation_report.json`

Observacao:

- Os artefatos processados foram gerados localmente.
- O commit registrou o script do builder, nao os arquivos de dataset.

---

## Grain

Unidade do dataset:

- 1 linha por partida.

Total de linhas geradas:

- 380.

Duplicidades validadas:

- `match_id`: 0 duplicatas.
- `sofascore_event_id`: 0 duplicatas.

---

## Target Principal

Nome principal:

- `target_late_goal_75`

Alias operacional no dataset:

- `has_late_goal`

Definicao:

- 1 se existir pelo menos um incidente de gol com `minute > 75`.
- 0 caso contrario.

Fonte:

- `match_incidents`.

Distribuicao validada:

- target positivo: 189.
- target negativo: 191.
- taxa positiva: 0.497368.

---

## Colunas Target-Derived

As colunas abaixo sao derivadas diretamente do target ou de eventos de gol futuros e nao podem ser usadas como features preditivas:

- `has_late_goal`
- `target_late_goal_75`
- `late_goal_count_75`
- `home_late_goal_count_75`
- `away_late_goal_count_75`
- `first_late_goal_minute_75`

Essas colunas devem ser usadas apenas para auditoria, validacao do alvo, analise descritiva do target ou rotulagem.

---

## Ressalvas de Leakage

As estatisticas de `match_statistics` representam estatisticas full-match. Portanto:

- nao devem ser usadas como preditores in-game por cutoff;
- podem conter informacao posterior ao minuto analisado;
- exigem revisao metodologica antes de qualquer uso preditivo;
- em V1, servem para auditoria e analise exploratoria controlada.

Colunas de placar final tambem nao devem ser usadas como preditores:

- `home_goals`
- `away_goals`
- `total_goals`

Outras colunas de resultado final ou eventos posteriores ao cutoff devem ser classificadas como risco de leakage antes de qualquer experimento.

---

## Ressalvas de Qualidade

Status final:

- APTO COM RESSALVAS.

Ressalva conhecida:

- `big_chances_home`: 7 nulos.
- `big_chances_away`: 7 nulos.

Regra:

- `big_chances_home` e `big_chances_away` devem permanecer opcionais.
- Nao devem ser usadas como features obrigatorias sem regra documentada de tratamento de nulos.

---

## Validacoes Executadas

Validacoes registradas em `late_goal_dataset_v1_validation_report.json`:

- contagem de linhas;
- contagem das tabelas fonte;
- duplicidade de `match_id`;
- duplicidade de `sofascore_event_id`;
- nulos em campos obrigatorios;
- presenca das classes positiva e negativa do target;
- exportacao Parquet;
- nulos conhecidos em `big_chances_home` e `big_chances_away`.

Resultado:

- sem erros de validacao;
- uma ressalva de qualidade referente a big chances;
- dataset apto com ressalvas para auditoria pelo Quant Research / Data Science.

---

## Modelagem

Nenhuma modelagem foi iniciada.

Nao foram criados:

- modelos preditivos;
- backtests;
- splits treino/teste;
- features avancadas H1-H9;
- pipelines de producao.

Proxima etapa recomendada:

- Quant Research / Data Science auditar o target e classificar colunas por risco de leakage antes de qualquer experimento.
