# LA_LIGA_2025_26_PREMIER_LEAGUE_SIMILARITY_AND_PROFIT_NOTES_V1

## Status

```text
REGISTRO DE PESQUISA — AGUARDANDO LA LIGA 2024/25
```

Este documento registra os achados iniciais do discovery La Liga 2025/26 e sua comparação com as famílias já observadas na Premier League.

A análise ainda é preliminar porque falta a chegada dos dados da La Liga 2024/25 para validação multi-temporada.

---

## Decisão Executiva

```text
APROVADO COM RESSALVAS PARA AUDITORIA OPERACIONAL
```

A La Liga 2025/26 apresentou sinais que se assemelham às famílias lucrativas da Premier League, especialmente:

- favorito vencendo por 1 + adversário frio;
- ambos times frios;
- time que está atrás pressionando;
- favorito empatando e pressionando.

---

## Famílias semelhantes à Premier League

### 1. favorite_winning_by_1_opp_cold_2of3

Semelhante às famílias fortes da Premier League:

```text
favorite_winning_by_1_opp_cold_2of3
team_winning_by_1_opp_cold_2of3
```

Na La Liga 2025/26 apareceu como:

```text
60' | no_goal_60_80 | last_10m
N = 37
Strike = 73.0%
Diff = +14.0 pp
```

E também:

```text
65' | no_goal_65_80 | last_5m
N = 63
Strike = 69.8%
Diff = +10.9 pp
```

Parecer:

```text
Semelhante à Premier League, mas na La Liga parece melhor em janela curta, não necessariamente hold até 90.
```

---

### 2. both_teams_cold_2of3

Família já conhecida na Premier League.

Na La Liga 2025/26 apareceu forte com bom volume:

```text
75' | no_goal_75_90 | last_5m
N = 136
Strike = 66.2%
Diff = +10.4 pp
```

E também:

```text
70' | no_goal_70_85 | last_15m
N = 86
Strike = 79.1%
Diff = +10.1 pp
```

Parecer:

```text
Semelhante à Premier League e com bom volume. Deve ir para cálculo financeiro, break-even e drawdown.
```

---

### 3. away_winning_by_1_home_pressing

Na Premier League a família forte foi:

```text
home_winning_by_1_visitor_pressing
```

Na La Liga surgiu uma versão conceitualmente parecida, mas invertida:

```text
away_winning_by_1_home_pressing
```

Resultado relevante:

```text
70' | goal_70_90 | last_15m
N = 49
Strike = 65.3%
Diff = +13.7 pp
```

Parecer:

```text
Semelhante no conceito: time perdendo por 1 pressionando no fim.
Na La Liga apareceu mais forte como mandante pressionando visitante que vence por 1.
```

---

## Nova família forte da La Liga

### favorite_drawing_pressure_high_2of3

Resultado principal:

```text
60' | goal_60_75 | last_10m
N = 59
Strike = 50.8%
Diff = +15.8 pp
```

Parecer:

```text
Nova família forte para Back Over: favorito empatando + pressão alta.
```

Essa família não é idêntica à principal da Premier League, mas pode ser muito interessante porque combina:

- favorito pré-jogo;
- jogo empatado;
- pressão alta recente;
- janela curta de gol.

---

## Estratégias mais lucrativas / prioritárias da La Liga 2025/26 para próxima auditoria

As estratégias abaixo devem ser priorizadas para cálculo de lucro, ROI, EV, break-even e drawdown:

| Prioridade | Estratégia | Entrada | Target | Janela | Mercado sugerido | N | Strike | Diff |
|---:|---|---:|---|---|---|---:|---:|---:|
| 1 | `favorite_drawing_pressure_high_2of3` | 60 | `goal_60_75` | `last_10m` | Back Over | 59 | 50.8% | +15.8 pp |
| 2 | `away_winning_by_1_home_pressing` | 70 | `goal_70_90` | `last_15m` | Back Over | 49 | 65.3% | +13.7 pp |
| 3 | `key_passes_recent_high` | 65 | `goal_65_85` | `last_10m` | Back Over | 205 | 49.8% | +9.5 pp |
| 4 | `both_teams_cold_2of3` | 75 | `no_goal_75_90` | `last_5m` | Lay Over | 136 | 66.2% | +10.4 pp |
| 5 | `both_teams_cold_2of3` | 70 | `no_goal_70_85` | `last_15m` | Lay Over | 86 | 79.1% | +10.1 pp |
| 6 | `favorite_winning_by_1_opp_cold_2of3` | 60 | `no_goal_60_80` | `last_10m` | Lay Over | 37 | 73.0% | +14.0 pp |
| 7 | `favorite_winning_by_1_opp_cold_2of3` | 65 | `no_goal_65_80` | `last_5m` | Lay Over | 63 | 69.8% | +10.9 pp |

Observação:

```text
Lucro final ainda precisa ser calculado pelo script de break-even/drawdown com odds médias oficiais.
```

---

## Comparação conceitual com Premier League

| Família | Premier League | La Liga 2025/26 | Parecer |
|---|---|---|---|
| Favorito +1 adversário frio | Forte | Forte em janela curta | Confirmada parcialmente |
| Ambos frios | Forte, mas com alerta de duplicidade | Forte e com volume | Promissora |
| Time atrás pressionando | Forte no BO75 da EPL | Forte com mandante pressionando visitante +1 | Semelhante/invertida |
| Favorito empatado pressionando | Não era núcleo principal | Muito forte | Nova família La Liga |

---

## Próxima etapa

Assim que os dados da La Liga 2024/25 chegarem:

1. Rodar o mesmo discovery.
2. Rodar break-even por janela.
3. Rodar drawdown por estratégia original.
4. Comparar La Liga 2025/26 vs La Liga 2024/25.
5. Depois comparar La Liga vs Premier League.

Critérios principais:

```text
lucro final
ROI
EV
break-even
drawdown
sequência máxima de perdas
consistência por temporada
```

---

## Decisão atual

```text
MANTER LA LIGA 2025/26 COMO PRIMEIRA FRENTE MULTI-LIGA PROMISSORA
```

A validação só deve avançar após chegada da La Liga 2024/25.
