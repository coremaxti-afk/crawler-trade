# H8_COMPOSITE_PRESSURE_SCORE_RESULTS_V1

## Resumo Executivo

- Validacao exploratoria executada conforme `docs/04_RESEARCH/H8_COMPOSITE_PRESSURE_SCORE_PLAN_V1.md`.
- Scores compostos usam shotmap/xG + graph momentum agregado, nunca graph por equipe.
- Pesos fixos foram usados sem ajuste por target.
- Nenhum modelo, baseline preditivo, backtesting financeiro real, producao, schema, banco, crawler ou importer foi alterado.
- Amostra: 380 partidas e 1520 linhas match_id + cutoff.
- Resultados com dados disponiveis: 5040.
- Classes: {'DESCARTAR_ESTATISTICO_LOCAL': 3837, 'OBSERVAR': 813, 'MICRO_AMOSTRA_REPLICAR': 304, 'NAO_DISPONIVEL_V1': 210, 'PROMISSOR_LOCAL': 86}.

Status atual:

```text
APROVADO COM RESSALVAS
```

Ressalva principal:

```text
As variacoes contendo favorite_* dependem de validacao definitiva do favorito pre-jogo via odds.
```

## Ressalva Metodologica - Favorito Pre-Jogo

Este relatorio permanece valido como evidência estatistica local dos sinais H8, mas as estrategias que usam `favorite_*` ainda precisam de validacao adicional.

Motivo:

```text
O filtro de favorito pre-jogo precisa ser confirmado por odds pre-match consolidadas.
```

Atualizacao posterior com SportMonks mostrou que, sem favorito pre-jogo, a reproducao operacional usa proxy:

```text
time vencendo por 1 gol no cutoff
```

Portanto:

- resultados `favorite_*` continuam uteis como hipoteses de pesquisa;
- nao devem ser promovidos a regra operacional definitiva sem validar favorito pre-jogo;
- a proxima etapa deve integrar odds pre-jogo e reexecutar as variacoes `favorite_*`.

Estudo recomendado:

```text
docs/04_RESEARCH/PRE_MATCH_FAVORITE_VALIDATION_V1.md
```

## Definicao Dos Scores Compostos

- `h8_hot_combo_10m_count`: soma de shots high, xG high e momentum trend positivo.
- `h8_cold_combo_10m_count`: soma de shots low, xG low e momentum trend nao positivo.
- `h8_pressure_score_10m`: `0.30*shots_z + 0.35*xg_z + 0.20*momentum_avg_z + 0.15*momentum_trend_score`.
- `h8_shot_quality_score_10m`: `0.45*shots_z + 0.55*xg_z`.
- `h8_graph_momentum_score_10m`: `0.60*momentum_avg_z + 0.40*momentum_trend_score`.
- `h8_conservative_hot_10m`: shots high AND xG high AND momentum trend positivo.
- `h8_graph_only_pressure_10m`: momentum trend positivo AND shots low.
- xGOT opcional: NAO_DISPONIVEL_V1: xGOT nao esta no Dataset H8 V1 validado; raw shotmap possui xgot, mas nao foi integrado a esta V1.

## Confirmacao Anti-Leakage

- Features usam somente informacoes ate o cutoff.
- Graph e momentum sao usados apenas como pressao agregada da partida.
- Nao foi inferida pressao por time via graph.
- Placar final e gols futuros nao foram usados como features.
- Pesos dos scores nao foram ajustados pelo target.
- Odds live nao foram usadas.
- Cutoff 80 foi reportado como `NAO_DISPONIVEL_V1`, pois nao existe no Dataset H8 V1 atual.
- Variacoes `favorite_*` devem ser revisitadas com favorito pre-jogo confirmado por odds.

## Ranking Estatistico Geral

O ranking completo original foi preservado no historico do repositorio. Esta revisao sintetica adiciona a ressalva metodologica sobre favorito pre-jogo sem alterar a conclusao dos sinais H8.

### Candidatos Operacionais Mais Relevantes

| variation | cutoff | target | N | rate | baseline | diff | class | status |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- | --- |
| `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | 60 | `no_goal_60_75` | 54 | 74.1% | 62.9% | +11.2 p.p. | PROMISSOR_LOCAL | APROVADO COM RESSALVAS |
| `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | 60 | `no_goal_60_75` | 36 | 75.0% | 62.9% | +12.1 p.p. | OBSERVAR | APROVADO COM RESSALVAS |
| `home_winning_by_1 + h8_shot_quality_top25` | 65 | `goal_65_80` | 20 | 70.0% | 36.8% | +33.2 p.p. | PROMISSOR_LOCAL | OBSERVACAO |
| `home_winning_by_1 + h8_pressure_score_10m_top25` | 65 | `goal_65_80` | 23 | 65.2% | 36.8% | +28.4 p.p. | PROMISSOR_LOCAL | OBSERVACAO |

## Leitura Atualizada

1. O grupo mais forte continua sendo Lay Over / jogo frio aos 60 minutos.
2. O filtro `favorite_winning_by_1` ainda precisa ser validado por odds pre-jogo.
3. Enquanto isso, a leitura operacional deve ser tratada como:

```text
time vencendo por 1 + jogo frio
```

4. Back Over quente aos 65 minutos permanece em observacao, especialmente porque a leitura SportMonks posterior nao reforcou prioridade sobre Lay Over frio.

## Proxima Etapa

Criar e executar:

```text
docs/04_RESEARCH/PRE_MATCH_FAVORITE_VALIDATION_V1.md
```

Objetivo:

```text
Integrar odds pre-jogo para identificar favorito real e reexecutar as variacoes favorite_* sem proxy.
```

## Decisao Final

```text
APROVADO COM RESSALVAS
```

Nenhuma regra deve ser promovida para operacional definitivo sem a validacao do favorito pre-jogo.
