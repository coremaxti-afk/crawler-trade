# H8 Feature Builder V1 - Technical Specification

Status: IMPLEMENTACAO AUTORIZADA PELO PM
Data: 2026-06-06

## Objetivo

Implementar um Feature Builder H8 auditavel e reprodutivel para gerar features de Graph/Momentum e Shotmap a partir das tabelas PostgreSQL ja populadas.

O builder nao cria modelo, nao executa baseline, nao executa backtesting, nao altera schema, nao altera importer e nao escreve no PostgreSQL.

## Arquivo de implementacao

```text
Analytics/FeatureBuilder/h8_feature_builder_v1.py
```

## Fontes

Leitura somente:

- `matches_master`
- `match_graph`
- `match_shotmap`
- `match_source_status`

## Grain

```text
1 linha por match_id + cutoff_minute
```

Cutoffs oficiais V1:

- 60
- 65
- 70
- 75

Quantidade esperada:

```text
380 partidas importaveis x 4 cutoffs = 1520 linhas
```

## Separacao Graph e Shotmap

Graph e Shotmap devem permanecer separados no codigo, nos metadados, no relatorio de validacao e na interpretacao posterior.

Graph usa apenas:

```text
match_graph.minute
match_graph.point_index
match_graph.momentum_value
```

Shotmap usa apenas:

```text
match_shotmap.minute
match_shotmap.shot_index
match_shotmap.xg
```

## Whitelist oficial de features

### H8-A Graph

- `momentum_last_5m_avg`
- `momentum_last_10m_avg`
- `momentum_trend_last_10m`
- `momentum_sum_until_cutoff`

### H8-B Shotmap

- `xg_last_5m`
- `xg_last_10m`
- `shots_last_5m`
- `shots_last_10m`
- `xg_sum_until_cutoff`

Nenhuma coluna fora desta whitelist pode ser tratada como feature H8 V1.

## Definicoes operacionais

### momentum_last_5m_avg

```text
avg(momentum_value)
where minute > cutoff_minute - 5
  and minute <= cutoff_minute
```

### momentum_last_10m_avg

```text
avg(momentum_value)
where minute > cutoff_minute - 10
  and minute <= cutoff_minute
```

### momentum_trend_last_10m

```text
last(momentum_value ordered by minute, point_index)
-
first(momentum_value ordered by minute, point_index)
where minute > cutoff_minute - 10
  and minute <= cutoff_minute
```

### momentum_sum_until_cutoff

```text
sum(momentum_value)
where minute <= cutoff_minute
```

### xg_last_5m

```text
sum(xg)
where minute > cutoff_minute - 5
  and minute <= cutoff_minute
```

### xg_last_10m

```text
sum(xg)
where minute > cutoff_minute - 10
  and minute <= cutoff_minute
```

### shots_last_5m

```text
count(shot_index)
where minute > cutoff_minute - 5
  and minute <= cutoff_minute
```

### shots_last_10m

```text
count(shot_index)
where minute > cutoff_minute - 10
  and minute <= cutoff_minute
```

### xg_sum_until_cutoff

```text
sum(xg)
where minute <= cutoff_minute
```

## Politica para dados ausentes

### Graph

- `12437015` e known_missing para `graph.json`, HTTP 404 confirmado.
- A partida deve permanecer no dataset H8.
- Features Graph devem ficar nulas apenas para esta partida.
- `graph_known_missing = 1` deve sinalizar a excecao.
- Outputs que exigirem Graph completo devem excluir ou tratar explicitamente esta partida.

### Shotmap

- Cobertura esperada: 380 partidas importaveis.
- Quando uma partida nao tiver finalizacao em uma janela, features de contagem devem ser 0 e features de xG da janela devem ser 0.

## Auditoria anti-leakage

O builder deve validar que:

- todas as features usam somente `minute <= cutoff_minute`;
- nenhuma coluna de target entra no output;
- nenhuma coluna derivada de late goal entra no output;
- placar final nao entra no output;
- estatisticas full-match nao entram no output;
- Graph e Shotmap permanecem separados;
- whitelist oficial e aplicada;
- `momentum_value` e preservado como importado, sem inversao de sinal, normalizacao ou transformacao.

## Outputs

Diretorio:

```text
data/processed/features/
```

Arquivos:

```text
h8_features_v1.csv
h8_features_v1.parquet
h8_features_v1_metadata.json
h8_features_v1_validation_report.json
```

Parquet e gerado apenas se `pyarrow` ou `fastparquet` estiver disponivel no ambiente.

## Colunas de identificacao e cobertura

- `match_id`
- `sofascore_event_id`
- `league`
- `season`
- `match_date`
- `home_team`
- `away_team`
- `cutoff_minute`
- `graph_available`
- `graph_known_missing`
- `shotmap_available`
- `graph_points_until_cutoff`
- `graph_points_last_5m`
- `graph_points_last_10m`
- `shots_until_cutoff`

## Validacoes obrigatorias

- `match_id + cutoff_minute` unico.
- 1520 linhas esperadas.
- 380 partidas unicas.
- 4 cutoffs oficiais presentes.
- Cada cutoff com 380 partidas.
- Graph disponivel em 379 partidas por cutoff.
- Shotmap disponivel em 380 partidas por cutoff.
- `12437015` aparece como known_missing de Graph.
- Features Graph nulas somente quando Graph esta indisponivel/known_missing.
- Features Shotmap nao nulas nas 380 partidas.
- Nenhuma coluna de target ou placar final no output.
- Whitelist completa presente.

## Comando de execucao

```bash
python C:\LateGoalResearch\Analytics\FeatureBuilder\h8_feature_builder_v1.py
```

Opcional:

```bash
python C:\LateGoalResearch\Analytics\FeatureBuilder\h8_feature_builder_v1.py --cutoffs 60,65,70,75
```

## Resultado da execucao inicial

Execucao local concluida em 2026-06-06:

- Linhas geradas: 1520.
- Partidas unicas: 380.
- Eventos com Graph: 379.
- Eventos com Shotmap: 380.
- Status do validation report: APTO COM RESSALVAS.
- Erros: 0.
- Warnings: 2.

Warnings esperados:

- Feature set e match-level e nao team-directional; Graph momentum sign e preservado como importado.
- O feature set nao inclui target columns por design; join com target dataset deve ser explicito em analises downstream.

## Status final

Feature Builder H8 V1 especificado, implementado e executado localmente com validacao anti-leakage aprovada.
