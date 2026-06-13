# TRADE_ENTRY_PROFILE_ANALYSIS_V1

## Resumo Executivo

Status:

```text
APROVADO COM RESSALVAS
```

Este estudo transforma as estratégias estatísticas mais promissoras em perfis operacionais de entrada usando dados SportMonks EPL 2025/26 ja coletados.

A entrega e valida como estudo de Data QA/Research, mas nao deve ser interpretada como regra final de execucao porque as estrategias `favorite_*` ainda nao foram reproduzidas exatamente com favorito pre-jogo real.

Ressalva principal:

```text
As estrategias favorite_* foram reproduzidas usando proxy: time vencendo por 1 no cutoff.
Favorito pre-jogo real ainda nao foi validado via odds.
```

## Escopo e Restricoes

- Usar apenas dados ja coletados.
- Nao coletar novos dados.
- Nao criar importer.
- Nao alterar schema.
- Nao criar dataset final.
- Nao criar modelo.
- Nao fazer backtesting financeiro real.
- Nao criar feature builder definitivo.
- Nao criar robo.
- Nao criar producao.

## Fonte

SportMonks EPL 2025/26:

```text
data/raw/sportmonks/full_collection/england_premier_league_league_8_season_25583_2025_2026
```

Endpoints esperados usados:

```text
trends
timeline
match_state
```

## Metodologia

Foram calculados perfis reais no momento da entrada para as estrategias alvo.

Para tendencias acumuladas, as janelas foram calculadas como diferenca entre o valor no cutoff e o valor no inicio da janela.

Exemplo:

```text
last_10m = value_at_cutoff - value_at_cutoff_minus_10
```

Para `Ball Possession %`, a leitura foi tratada como snapshot/estado, nao como acumulado.

## Regras Anti-Leakage

- Todos os dados de entrada usam `minute <= cutoff`.
- Reavaliacoes dinamicas usam apenas `minute <= reavaliacao`.
- Gols futuros entram apenas como resultado.
- `statistics` final nao foi usado como feature de cutoff.
- `xgfixture` final nao foi usado como feature de cutoff.
- xG temporal nao foi inventado.
- Big Chances, Key Passes e Shots On Target foram tratados como proxies separados, sem chamar de xG.

## Estrategias Analisadas

1. `favorite_winning_by_1 + h8_cold_combo_10m_2of3`
2. `favorite_winning_by_1 + h8_pressure_score_10m_bottom25`
3. `home_winning_by_1 + h8_pressure_score_10m_top25`
4. `home_winning_by_1 + h8_shot_quality_top25`

## Ressalva Metodologica - Favorito Pre-Jogo

As estrategias contendo `favorite_*` ainda nao foram reproduzidas exatamente nesta etapa.

Motivo:

```text
Os dados SportMonks usados no estudo nao continham identificacao consolidada do favorito pre-jogo.
```

Proxy temporario usado:

```text
time vencendo por 1 gol no cutoff
```

Portanto, os resultados devem ser interpretados como:

- aproximacao operacional das estrategias originais;
- validacao do perfil frio/quente no momento da entrada;
- nao reproducao exata baseada em favoritismo pre-jogo.

Proxima etapa recomendada:

```text
Integrar odds pre-jogo para marcar favorito real antes da partida e reexecutar as estrategias favorite_*.
```

## Thresholds de Referencia

```json
{
  "base60_pressure_p25": 7.25,
  "base65_pressure_p75": 12.5875,
  "base65_quality_p75": 7.225,
  "cold_p25": {
    "total_shots_total_last_10m": 2,
    "total_dangerous_attacks_last_10m": 7,
    "total_key_passes_last_10m": 1
  }
}
```

## Contagens

| Item | Valor |
|---|---:|
| Fixtures | 380 |
| Base60 winning_by_1 | 165 |
| Base65 home_winning_by_1 | 86 |
| Entradas geradas | 155 |

## Perfil - favorite_winning_by_1 + h8_cold_combo_10m_2of3

Status:

```text
APROVADO COM RESSALVAS
```

| Metrica | Valor |
|---|---:|
| N proxy | 69 |
| Reproducao exata | false |
| Favorito disponivel | false |
| Gol 60-75 | 30.4% |
| Sem gol 60-75 | 69.6% |
| Finalizacoes totais ultimos 10 min media | 1.39 |
| Finalizacoes totais ultimos 10 min mediana | 1.00 |
| Finalizacoes totais ultimos 10 min p75 | 2.00 |
| Finalizacoes no gol ultimos 10 min media | 0.65 |
| Finalizacoes no gol ultimos 10 min mediana | 0.00 |
| Finalizacoes no gol ultimos 10 min p75 | 1.00 |
| Attacks ultimos 10 min media | 17.80 |
| Dangerous Attacks ultimos 10 min media | 8.38 |
| Dangerous Attacks ultimos 10 min mediana | 8.00 |
| Dangerous Attacks ultimos 10 min p75 | 11.00 |
| Corners ultimos 10 min media | 0.74 |
| Key Passes ultimos 10 min media | 0.90 |
| Big Chances Created ultimos 10 min media | 0.36 |
| Big Chances Missed ultimos 10 min media | 0.16 |

### Dinamica

| Grupo | N | Gol 60-75 | Sem gol 60-75 | Gol 70-75 | Sem gol 70-75 |
|---|---:|---:|---:|---:|---:|
| Continuou frio | 26 | 11.5% | 88.5% | 3.8% | 96.2% |
| Esquentou | 43 | 41.9% | 58.1% | 9.3% | 90.7% |

### Leitura Operacional Temporaria

```text
Minuto 60
Time vencendo por 1 gol
Finalizacoes totais ultimos 10 min <= 1 a 2
Finalizacoes no gol ultimos 10 min = 0
Key Passes ultimos 10 min <= 1
Big Chances Created ultimos 10 min = 0
Dangerous Attacks ultimos 10 min perto de 8 ou menos
```

## Perfil - favorite_winning_by_1 + h8_pressure_score_10m_bottom25

Status:

```text
APROVADO COM RESSALVAS
```

| Metrica | Valor |
|---|---:|
| N proxy | 42 |
| Reproducao exata | false |
| Favorito disponivel | false |
| Gol 60-75 | 28.6% |
| Sem gol 60-75 | 71.4% |
| Finalizacoes totais ultimos 10 min media | 1.05 |
| Finalizacoes totais ultimos 10 min mediana | 1.00 |
| Finalizacoes totais ultimos 10 min p75 | 1.75 |
| Finalizacoes no gol ultimos 10 min media | 0.12 |
| Finalizacoes no gol ultimos 10 min mediana | 0.00 |
| Finalizacoes no gol ultimos 10 min p75 | 0.00 |
| Attacks ultimos 10 min media | 16.88 |
| Dangerous Attacks ultimos 10 min media | 8.45 |
| Dangerous Attacks ultimos 10 min mediana | 8.00 |
| Dangerous Attacks ultimos 10 min p75 | 11.00 |
| Corners ultimos 10 min media | 0.64 |
| Key Passes ultimos 10 min media | 0.74 |
| Big Chances Created ultimos 10 min media | 0.05 |
| Big Chances Missed ultimos 10 min media | 0.02 |

### Dinamica

| Grupo | N | Gol 60-75 | Sem gol 60-75 | Gol 70-75 | Sem gol 70-75 |
|---|---:|---:|---:|---:|---:|
| Continuou frio | 14 | 7.1% | 92.9% | 0.0% | 100.0% |
| Esquentou | 28 | 39.3% | 60.7% | 7.1% | 92.9% |

### Leitura Operacional Temporaria

```text
Minuto 60
Time vencendo por 1 gol
Finalizacoes totais ultimos 10 min <= 1 a 2
Finalizacoes no gol ultimos 10 min = 0
Big Chances Created ultimos 10 min = 0
Key Passes ultimos 10 min <= 1
Dangerous Attacks ultimos 10 min perto de 8 ou menos
```

## Perfil - home_winning_by_1 + h8_pressure_score_10m_top25

Status:

```text
OBSERVACAO
```

| Metrica | Valor |
|---|---:|
| N | 22 |
| Reproducao exata | false |
| Gol apos cutoff | 36.4% |
| Sem gol apos cutoff | 63.6% |
| Finalizacoes totais ultimos 10 min media | 4.09 |
| Finalizacoes no gol ultimos 10 min media | 1.91 |
| Attacks ultimos 10 min media | 17.32 |
| Dangerous Attacks ultimos 10 min media | 10.00 |
| Corners ultimos 10 min media | 1.27 |
| Key Passes ultimos 10 min media | 3.09 |
| Big Chances Created ultimos 10 min media | 1.18 |
| Big Chances Missed ultimos 10 min media | 0.77 |

### Dinamica

| Grupo | N | Gol 75-80 | Gol 75-85 | Sem gol 75-80 | Sem gol 75-85 |
|---|---:|---:|---:|---:|---:|
| Continuou quente | 11 | 9.1% | 18.2% | 90.9% | 81.8% |
| Esfriou | 11 | 18.2% | 36.4% | 81.8% | 63.6% |

### Leitura

Na leitura SportMonks recente, o Back Over ficou mais fraco que as estrategias Lay Over frias.

## Perfil - home_winning_by_1 + h8_shot_quality_top25

Status:

```text
OBSERVACAO
```

| Metrica | Valor |
|---|---:|
| N | 22 |
| Reproducao exata | false |
| Gol apos cutoff | 31.8% |
| Sem gol apos cutoff | 68.2% |
| Finalizacoes totais ultimos 10 min media | 3.73 |
| Finalizacoes no gol ultimos 10 min media | 1.91 |
| Attacks ultimos 10 min media | 16.05 |
| Dangerous Attacks ultimos 10 min media | 8.91 |
| Corners ultimos 10 min media | 1.00 |
| Key Passes ultimos 10 min media | 2.95 |
| Big Chances Created ultimos 10 min media | 1.36 |
| Big Chances Missed ultimos 10 min media | 0.86 |

### Dinamica

| Grupo | N | Gol 75-80 | Gol 75-85 | Sem gol 75-80 | Sem gol 75-85 |
|---|---:|---:|---:|---:|---:|
| Continuou quente | 10 | 10.0% | 20.0% | 90.0% | 80.0% |
| Esfriou | 12 | 16.7% | 33.3% | 83.3% | 66.7% |

### Leitura

A estrategia continua interessante como observacao historica, mas a leitura SportMonks recente nao reforcou prioridade operacional sobre Lay Over frio.

## Conclusao

O estudo reforca que o bloco mais promissor operacionalmente e:

```text
Lay Over / jogo frio / time vencendo por 1 / entrada aos 60 minutos
```

Porem, para transformar isso em regra final, falta validar:

```text
favorito pre-jogo real via odds
```

## Decisao Final

```text
APROVADO COM RESSALVAS
```

## Proxima Etapa Recomendada

Criar estudo:

```text
docs/04_RESEARCH/PRE_MATCH_FAVORITE_VALIDATION_V1.md
```

Objetivo:

```text
Integrar odds pre-jogo para identificar favorito real e reexecutar as estrategias favorite_* sem proxy.
```
