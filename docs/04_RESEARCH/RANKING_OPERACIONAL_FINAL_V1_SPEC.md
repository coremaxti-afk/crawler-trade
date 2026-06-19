# RANKING_OPERACIONAL_FINAL_V1_SPEC

## Status

`PROXIMO PASSO OFICIAL`

## Objetivo

Criar uma camada final que cruze:

```text
Discovery V4
Normalizacao fixture-level pre-DD
DD V4 corrigido
Rentabilidade por Time V4
Validacao Preditiva V1.1
```

A camada deve transformar relatorios separados em uma decisao operacional unica.

## Perguntas que o ranking deve responder

Para cada estrategia:

- Posso operar?
- A partir de qual rodada?
- Qual mercado?
- Qual target/cutoff/window?
- Qual lucro estimado?
- Qual ROI?
- Qual drawdown?
- Qual max losing streak?
- A estrategia depende de poucos times?
- Quais times evitar?
- Qual classificacao preditiva operacional?

## Fontes obrigatorias

### DD V4 corrigido

Usar:

```text
strategy_drawdown_summary_serie_a_2025_tempos_expandidos.csv
strategy_drawdown_trades_serie_a_2025_tempos_expandidos.csv
```

Campos minimos esperados:

- `profit_final`
- `ROI`
- `N_total`
- `max_drawdown_abs`
- `max_drawdown_pct`
- `max_losing_streak`
- `max_winning_streak`
- `temporal_order_verified`
- `dd_quality_alerts`

### Rentabilidade por Time V4

Usar:

```text
rentabilidade_das_estrategias_por_time_v4.csv
```

Campos minimos esperados:

- `robustez_score`
- `impacto_top3_pct`
- `lucro_sem_top1`
- `lucro_sem_top3`
- `lucro_sem_top1_negativo`
- `lucro_sem_top3_negativo`
- dependencia por time quando existir

### Validacao Preditiva V1.1

Usar:

```text
validacao_preditiva_da_estrategia_v1_1_serie_a_2025_tempos_expandidos_summary.csv
```

Campos minimos esperados:

- `classificacao_preditiva_estatistica`
- `classificacao_preditiva_operacional`
- `operacionalmente_relevante`
- `previsibilidade_score`
- `fase_confirmacao`
- `grupo_resultado_final`

## Classificacao final proposta

### APROVADA

Regras sugeridas:

```text
classificacao_preditiva_operacional IN (CONFIRMADA_10_RODADAS, CONFIRMADA_FASE_1, CONFIRMADA_FASE_2, CONFIRMADA_MEIO)
profit_final >= 1000
ROI >= 0.10
N_total >= 50
max_drawdown_pct <= 0.25
robustez_score >= 0.60
lucro_sem_top3 > 0
lucro_sem_top1 > 0
temporal_order_verified = True
```

Prioridade adicional:

```text
market_type = lay_over
target LIKE no_goal_*
```

### APROVADA_COM_RESSALVA

Regras sugeridas:

```text
classificacao_preditiva_operacional positiva
profit_final >= 500
ROI >= 0.05
N_total >= 30
```

Mas com uma ou mais ressalvas:

- drawdown alto
- dependencia moderada por time
- `robustez_score < 0.60`
- `lucro_sem_top3` baixo
- confirmacao tardia

### OBSERVAR

Regras sugeridas:

```text
profit_final > 0
ROI > 0
```

Mas:

- N pequeno
- lucro fraco
- confirmacao tardia
- dependencia forte por time
- nao passou nos filtros operacionais

### DESCARTAR

Regras sugeridas:

```text
classificacao_preditiva_operacional IN (
  FALSO_POSITIVO_NEGATIVO,
  FALSO_POSITIVO_BREAK_EVEN,
  NAO_LUCRATIVA_SEM_SINAL,
  CONFIRMADA_FRACA_NAO_OPERACIONAL,
  POSITIVO_FRACO_NAO_OPERACIONAL,
  LUCRATIVA_FRACA_NAO_PREVISIVEL
)
```

Tambem descartar inicialmente:

```text
market_type = back_over
target LIKE goal_*
```

quando houver historico negativo ou falso positivo.

## Padroes operacionais iniciais

### Padrao bom observado

- `lay_over`
- `no_goal_*`
- adversario frio
- adversario sem big chances
- adversario sem key passes recentes
- time vencendo por 1
- oponente sem SOT contra
- entrada entre 65 e 75

Familias candidatas:

- `opponent_no_big_chances`
- `team_winning_by_1_no_sot_against`
- `opponent_no_recent_key_passes`
- `both_teams_cold_2of3`
- `team_winning_by_1_opp_cold_2of3`
- `favorite_winning_by_1_opp_cold_2of3`

### Padrao ruim observado

- `back_over`
- `goal_*`
- pressao alta como unico gatilho
- big chances recentes para buscar gol
- time perdendo pressionando
- favorito pressionando para buscar gol
- SOT/key passes/corners recentes usados isoladamente para buscar gol

Familias de alerta:

- `team_losing_pressure_high_2of3`
- `favorite_drawing_pressure_high_2of3`
- `favorite_losing_pressure_high_2of3`
- `underdog_winning_favorite_pressing_2of3`
- `big_chances_recent` em `goal_*`

## Saidas esperadas

Gerar:

```text
ranking_operacional_final_v1_serie_a_2025_tempos_expandidos.csv
ranking_operacional_final_v1_serie_a_2025_tempos_expandidos.json
RANKING_OPERACIONAL_FINAL_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

Colunas minimas:

- `strategy_name`
- `target`
- `cutoff`
- `window`
- `market_type`
- `settlement`
- `N_total`
- `profit_final`
- `ROI`
- `max_drawdown_abs`
- `max_drawdown_pct`
- `max_losing_streak`
- `classificacao_preditiva_operacional`
- `previsibilidade_score`
- `robustez_score`
- `impacto_top3_pct`
- `lucro_sem_top1`
- `lucro_sem_top3`
- `status_operacional_final`
- `motivo_status`
- `rodada_minima_para_operar`
- `times_evitar`
- `observacoes`

## Regra de decisao inicial

Nenhuma estrategia deve ser aprovada para operar depois da 5a rodada com base na V1.1, pois nenhuma foi confirmada nas primeiras 5 rodadas.

Primeira janela operacional sugerida:

```text
apos a 10a rodada
```

priorizando estrategias `CONFIRMADA_10_RODADAS` e `lay_over/no_goal`.
