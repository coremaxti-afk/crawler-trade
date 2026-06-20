# FRENTES_DE_PESQUISA_PRE_RANKING_OPERACIONAL_FINAL_V1

## Status

`DEFINIDO COMO ETAPA PREVIA AO RANKING_OPERACIONAL_FINAL_V1`

## Motivo

Antes de gerar o `RANKING_OPERACIONAL_FINAL_V1`, foram identificadas 3 frentes que precisam ser tratadas separadamente para evitar mistura conceitual e para impedir que o ranking conte a mesma oportunidade varias vezes.

A validacao preditiva V1.1 foi util, mas misturou parte da leitura de fase da temporada com a leitura de estabilidade por rodada.

A partir daqui, as frentes ficam separadas.

---

# Frente 1 — ANALISE_REGIME_POR_FASE_V1

## Objetivo

Medir a lucratividade das estrategias por blocos da temporada, sem misturar com a pergunta de quando entrar.

Este estudo deve responder:

- Quais fases da temporada foram melhores para `under/no_goal/lay_over`?
- Quais fases foram menos ruins ou possivelmente boas para `over/goal/back_over`?
- A temporada mudou de regime?
- Quais estrategias funcionaram em varias fases?
- Quais estrategias foram dependentes de uma fase especifica?

## Granularidades obrigatorias

Rodar o mesmo estudo com dois modelos:

```text
phase_count = 6
phase_count = 8
```

Interpretação:

- `6 fases`: leitura macro da temporada.
- `8 fases`: leitura mais sensivel para detectar viradas menores de regime.

## Regra para evitar confusao

Toda linha de output deve conter:

```text
phase_count
phase_number
phase_start_round
phase_end_round
```

Assim, `fase 3 de 6` nunca sera confundida com `fase 3 de 8`.

## Campos minimos esperados

Por estrategia e por fase:

```text
strategy_name
target
cutoff
window
market_type
settlement
phase_count
phase_number
phase_start_round
phase_end_round
N_fase
profit_fase
ROI_fase
max_drawdown_fase
max_losing_streak_fase
```

Por estrategia consolidada:

```text
profit_fase_1 ... profit_fase_N
ROI_fase_1 ... ROI_fase_N
N_fase_1 ... N_fase_N
qtd_fases_lucrativas
qtd_fases_negativas
melhor_fase
pior_fase
consistencia_por_fase
regime_dependente
```

## Saidas esperadas

```text
analise_regime_por_fase_v1_serie_a_2025_tempos_expandidos_phase6.csv
analise_regime_por_fase_v1_serie_a_2025_tempos_expandidos_phase8.csv
ANALISE_REGIME_POR_FASE_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

## Observacao inicial

Teste preliminar mostrou que as estrategias Over/Goal nao foram lucrativas no agregado em nenhuma das 6 fases, mas as fases 3 e 6 foram as menos negativas para Over.

Isso sugere que pode existir regime pontual para Over, mas ainda nao uma estrategia Over estavel.

---

# Frente 2 — SIMULACAO_ENTRADA_POR_RODADA_V1

## Objetivo

Medir em qual rodada a estrategia fica estavel o suficiente para operar e quanto lucro ainda sobra depois dessa validacao.

A pergunta principal e:

```text
Se eu esperar ate a rodada X para validar a estrategia, quanto lucro ainda consigo capturar da rodada X+1 ate o fim?
```

## Rodadas obrigatorias

Testar:

```text
5, 6, 7, 8, 9, 10, 11, 12
```

## Campos minimos esperados

Por estrategia e rodada de validacao:

```text
strategy_name
target
cutoff
window
market_type
settlement
rodada_validacao
N_ate_rodada
profit_ate_rodada
ROI_ate_rodada
N_pos_rodada
profit_pos_rodada
ROI_pos_rodada
DD_pos_rodada
max_losing_pos_rodada
lucro_perdido_ate_rodada
lucro_capturavel_pos_rodada
pct_lucro_capturavel
estrategia_estavel_na_rodada
falso_positivo_se_entrar_na_rodada
```

Por estrategia consolidada:

```text
melhor_rodada_para_operar
profit_pos_melhor_rodada
ROI_pos_melhor_rodada
DD_pos_melhor_rodada
N_pos_melhor_rodada
risco_falso_positivo_melhor_rodada
```

## Regras iniciais sugeridas

Para considerar uma estrategia estavel na rodada X:

```text
N_ate_rodada_X >= 5
profit_ate_rodada_X > 0
ROI_ate_rodada_X >= 5%
```

Para considerar que ainda existe valor operacional depois da rodada X:

```text
profit_pos_rodada_X >= 500
ROI_pos_rodada_X >= 5%
N_pos_rodada_X >= 20
```

Para aprovacao forte:

```text
profit_pos_rodada_X >= 1000
ROI_pos_rodada_X >= 10%
N_pos_rodada_X >= 30
```

## Saidas esperadas

```text
simulacao_entrada_por_rodada_v1_serie_a_2025_tempos_expandidos.csv
simulacao_entrada_por_rodada_v1_serie_a_2025_tempos_expandidos.json
SIMULACAO_ENTRADA_POR_RODADA_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

---

# Frente 3 — AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1

## Objetivo

Evitar que o ranking operacional conte varias variacoes da mesma oportunidade como se fossem estrategias independentes.

Exemplo do problema:

```text
both_teams_cold_2of3 no_goal_60_75
both_teams_cold_2of3 no_goal_60_80
both_teams_cold_2of3 no_goal_60_85
both_teams_cold_2of3 no_goal_60_90
```

Essas linhas podem ser praticamente a mesma entrada com os mesmos jogos/times, mudando apenas tempo de entrada, tempo de saida, cashout ou hold.

## Risco operacional

Se nao agrupar por familia, o ranking pode:

- superestimar a diversidade de estrategias;
- aprovar 4 ou 5 variacoes da mesma oportunidade;
- somar lucros de entradas sobrepostas;
- dar falsa sensacao de robustez.

## Regra de familia

Criar campos:

```text
strategy_family
variant_id
family_rank
is_primary_variant
overlap_with_primary_pct
overlap_fixture_pct
overlap_team_pct
```

Sugestao de familia:

```text
strategy_family = strategy_name + market_direction
```

Onde:

```text
market_direction = no_goal | goal
```

## Analise de overlap

Comparar variacoes dentro da mesma familia por:

```text
fixture_id
team_id ou team_side quando existir
season_id
league_id
```

Se:

```text
overlap_fixture_pct >= 70%
```

entao tratar como variacao da mesma oportunidade, nao como estrategia independente.

## Regra operacional

No ranking final:

```text
Aprovar no maximo 1 variacao principal por familia.
```

As demais devem aparecer como:

```text
VARIACAO_ALTERNATIVA
```

ou:

```text
NAO_SOMAR_LUCRO_COM_VARIACAO_PRINCIPAL
```

## Saidas esperadas

```text
agrupamento_por_familia_e_variacoes_v1_serie_a_2025_tempos_expandidos.csv
agrupamento_por_familia_e_variacoes_v1_serie_a_2025_tempos_expandidos.json
AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

---

# Como as 3 frentes alimentam o Ranking Operacional Final

O `RANKING_OPERACIONAL_FINAL_V1` deve usar as 3 frentes assim:

## Da Frente 1

Usar:

```text
consistencia_por_fase
qtd_fases_lucrativas
qtd_fases_negativas
melhor_fase
pior_fase
regime_dependente
```

## Da Frente 2

Usar:

```text
melhor_rodada_para_operar
profit_pos_melhor_rodada
ROI_pos_melhor_rodada
DD_pos_melhor_rodada
N_pos_melhor_rodada
```

## Da Frente 3

Usar:

```text
strategy_family
is_primary_variant
overlap_with_primary_pct
family_rank
```

## Nova regra para o ranking final

Uma estrategia so pode ser `APROVADA` se:

```text
is_primary_variant = True
profit_pos_melhor_rodada > 0
N_pos_melhor_rodada >= minimo operacional
classificacao_preditiva_operacional positiva
robustez por time aceitavel
DD controlado
```

Variacoes da mesma familia podem aparecer no relatorio, mas nao devem ser somadas como oportunidades independentes.

## Decisao

Antes de criar o `RANKING_OPERACIONAL_FINAL_V1`, executar:

```text
1. ANALISE_REGIME_POR_FASE_V1
2. SIMULACAO_ENTRADA_POR_RODADA_V1
3. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
```

Depois disso, gerar o ranking final consolidado.
