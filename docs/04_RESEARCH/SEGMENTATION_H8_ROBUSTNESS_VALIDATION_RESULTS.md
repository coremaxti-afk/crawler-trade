# Segmentation H8 Robustness Validation Results

Data: 2026-06-07 12:50:56 UTC

## Resumo Executivo

Validacao de robustez executada para duas interacoes Segmentacao x H8, com target `target_late_goal_75` e cutoffs 60, 65 e 70.

Interacoes avaliadas:

1. `defensivo_fragile + shots_last_10m`
2. `ofensivo_forte_vs_defesa_fragil + shots_last_10m`

Resultado final:

- `defensivo_fragile + shots_last_10m`: **OBSERVAR**. Cutoffs positivos=3/3, N>=30=3/3, diff>=8 p.p.=1/3, OR>1.5=1/3, p<0.10=1/3.
- `ofensivo_forte_vs_defesa_fragil + shots_last_10m`: **DESCARTAR**. Cutoffs positivos=3/3, N>=30=0/3, diff>=8 p.p.=2/3, OR>1.5=2/3, p<0.10=1/3.

Nenhuma interacao atingiu classificacao `PROMISSOR ROBUSTO`. A interacao `defensivo_fragile + shots_last_10m` manteve sinal positivo em 3 de 3 cutoffs, mas o efeito forte/significativo ficou concentrado no cutoff 60 e houve alerta de concentracao por times. A interacao `ofensivo_forte_vs_defesa_fragil + shots_last_10m` teve sinal forte somente no cutoff 60, com N pequeno, e perdeu robustez nos cutoffs 65 e 70.

## Fontes Usadas

- `data/processed/datasets/team_profile_segment_dataset_v1.csv`
- `data/processed/datasets/late_goal_dataset_h8_v1.csv`

Nenhuma escrita em PostgreSQL foi realizada. Nenhum schema, importer, crawler, raw data, modelo, baseline, backtesting ou artefato de producao foi alterado.

## Metodologia

- Target: `target_late_goal_75`.
- Cutoffs: 60, 65, 70.
- Feature H8: `shots_last_10m`.
- Definicao de `shots_last_10m` alto: top 25% por cutoff, calculado sem usar target.

Thresholds por cutoff:

| Cutoff | Regra |
|---:|---|
| 60 | `shots_last_10m >= 4 (q75=4.000)` |
| 65 | `shots_last_10m >= 4 (q75=4.000)` |
| 70 | `shots_last_10m >= 4 (q75=4.000)` |

## Confirmacao Anti-Leakage

- Segmentacao dinamica veio do Dataset de Segmentacao V1, com perfis historicos calculados via `shift(1)` antes do expanding.
- H8 usa somente `shots_last_10m` no cutoff avaliado.
- O target foi usado somente como resposta.
- Nenhum evento apos o cutoff foi usado na feature H8.
- Nenhum placar final, coluna target-derived, schema, importer, crawler ou raw data foi alterado.
- Threshold de `shots_last_10m` alto foi calculado por cutoff sem olhar o target; por ser exploratorio, nao deve ser reaproveitado automaticamente em baseline.

## Resultado por Cutoff

### defensivo_fragile + shots_last_10m

Classificacao final: **OBSERVAR**.

| Cutoff | Threshold shots | N | Pos | Neg | Taxa | Geral | Dif. p.p. | OR | IC 95% | p-value |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| 60 | >= 4 | 52 | 34 | 18 | 65.4% | 50.0% | +15.4 | 2.10 | [1.14, 3.88] | 0.0224 |
| 65 | >= 4 | 48 | 26 | 22 | 54.2% | 50.0% | +4.2 | 1.21 | [0.66, 2.23] | 0.6389 |
| 70 | >= 4 | 46 | 25 | 21 | 54.3% | 50.0% | +4.3 | 1.22 | [0.66, 2.27] | 0.6330 |

### ofensivo_forte_vs_defesa_fragil + shots_last_10m

Classificacao final: **DESCARTAR**.

| Cutoff | Threshold shots | N | Pos | Neg | Taxa | Geral | Dif. p.p. | OR | IC 95% | p-value |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|
| 60 | >= 4 | 20 | 15 | 5 | 75.0% | 50.0% | +25.0 | 3.01 | [1.11, 8.18] | 0.0353 |
| 65 | >= 4 | 18 | 10 | 8 | 55.6% | 50.0% | +5.6 | 1.25 | [0.49, 3.18] | 0.8091 |
| 70 | >= 4 | 17 | 11 | 6 | 64.7% | 50.0% | +14.7 | 1.83 | [0.68, 4.91] | 0.3190 |

## Dependencia de Poucos Jogos e Times

### defensivo_fragile + shots_last_10m

| Cutoff | Positivos | Time mais frequente | Pos. com top time | Pos. com top 2 | Share top 2 | Sens. N sem top | Sens. taxa sem top | Sens. diff p.p. |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 60 | 34 | Brentford | 10 | 19 | 55.9% | 37 | 64.9% | +14.2 |
| 65 | 26 | Southampton | 9 | 14 | 53.8% | 32 | 53.1% | +4.2 |
| 70 | 25 | Southampton | 7 | 14 | 56.0% | 37 | 48.6% | -0.3 |

### ofensivo_forte_vs_defesa_fragil + shots_last_10m

| Cutoff | Positivos | Time mais frequente | Pos. com top time | Pos. com top 2 | Share top 2 | Sens. N sem top | Sens. taxa sem top | Sens. diff p.p. |
|---:|---:|---|---:|---:|---:|---:|---:|---:|
| 60 | 15 | Southampton | 4 | 8 | 53.3% | 15 | 73.3% | +24.4 |
| 65 | 10 | Arsenal | 3 | 5 | 50.0% | 13 | 53.8% | +2.1 |
| 70 | 11 | Southampton | 4 | 5 | 45.5% | 13 | 53.8% | +4.9 |

## Robustez Temporal

### defensivo_fragile + shots_last_10m

| Cutoff | Bloco | N | Pos | Taxa | Geral bloco | Dif. p.p. |
|---:|---|---:|---:|---:|---:|---:|
| 60 | inicial | 17 | 9 | 52.9% | 47.7% | +5.3 |
| 60 | intermediario | 12 | 8 | 66.7% | 53.8% | +12.9 |
| 60 | final | 23 | 17 | 73.9% | 48.6% | +25.3 |
| 65 | inicial | 15 | 9 | 60.0% | 47.7% | +12.3 |
| 65 | intermediario | 14 | 5 | 35.7% | 53.8% | -18.1 |
| 65 | final | 19 | 12 | 63.2% | 48.6% | +14.6 |
| 70 | inicial | 13 | 9 | 69.2% | 47.7% | +21.6 |
| 70 | intermediario | 17 | 7 | 41.2% | 53.8% | -12.6 |
| 70 | final | 16 | 9 | 56.2% | 48.6% | +7.7 |

### ofensivo_forte_vs_defesa_fragil + shots_last_10m

| Cutoff | Bloco | N | Pos | Taxa | Geral bloco | Dif. p.p. |
|---:|---|---:|---:|---:|---:|---:|
| 60 | inicial | 4 | 4 | 100.0% | 47.7% | +52.3 |
| 60 | intermediario | 6 | 4 | 66.7% | 53.8% | +12.9 |
| 60 | final | 10 | 7 | 70.0% | 48.6% | +21.4 |
| 65 | inicial | 4 | 4 | 100.0% | 47.7% | +52.3 |
| 65 | intermediario | 6 | 1 | 16.7% | 53.8% | -37.1 |
| 65 | final | 8 | 5 | 62.5% | 48.6% | +13.9 |
| 70 | inicial | 2 | 2 | 100.0% | 47.7% | +52.3 |
| 70 | intermediario | 8 | 4 | 50.0% | 53.8% | -3.8 |
| 70 | final | 7 | 5 | 71.4% | 48.6% | +22.8 |

## Leitura dos Resultados

### defensivo_fragile + shots_last_10m

O sinal e positivo nos cutoffs 60, 65 e 70, sempre com N acima de 30. No entanto, apenas o cutoff 60 combina diff >= 8 p.p., OR > 1.5 e p-value < 0.10; nos cutoffs 65 e 70 o efeito cai para cerca de +4 p.p. e perde forca estatistica. A analise de concentracao tambem aponta dependencia relevante de poucos times positivos. Por isso, a classificacao final e `OBSERVAR`, nao `PROMISSOR ROBUSTO`.

### ofensivo_forte_vs_defesa_fragil + shots_last_10m

O sinal e forte no cutoff 60, mas a amostra e pequena. Nos cutoffs 65 e 70 o efeito fica instavel, com N pequeno e p-values fracos, apesar de diff ainda positiva em 70. A classificacao final e `DESCARTAR` nesta formulacao de robustez.

## Classificacao Final

| Interacao | Classificacao | Motivo principal |
|---|---|---|
| `defensivo_fragile + shots_last_10m` | OBSERVAR | Sinal positivo em 3 cutoffs, mas robustez forte apenas no cutoff 60 e alerta de concentracao por times. |
| `ofensivo_forte_vs_defesa_fragil + shots_last_10m` | DESCARTAR | Sinal dependente do cutoff 60, N pequeno e falta de estabilidade nos cutoffs alternativos. |

## Recomendacao

Nao iniciar baseline ou backtesting com essas interacoes neste momento. Encaminhar ao Quant Research com recomendacao de:

- manter `defensivo_fragile + shots_last_10m` em OBSERVAR para futura revalidacao com mais temporadas ou ligas;
- descartar `ofensivo_forte_vs_defesa_fragil + shots_last_10m` como interacao robusta nesta amostra;
- nao expandir combinacoes antes de decisao Quant/PM.

## Status Final

Status: VALIDACAO DE ROBUSTEZ CONCLUIDA.
