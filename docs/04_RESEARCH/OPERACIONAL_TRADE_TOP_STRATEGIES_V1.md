# OPERACIONAL_TRADE_TOP_STRATEGIES_V1

## Objetivo

Transformar os resultados das pesquisas quantitativas em um guia operacional simples para futuras validações práticas.

Importante:

- Não representa produção.
- Não representa backtesting financeiro real.
- Não representa recomendação de investimento.
- Utiliza odds médias observadas em amostras manuais de mercado Próximo Gol.
- Utiliza apenas estratégias já validadas estatisticamente.

---

## Status Atual

```text
APROVADO COM RESSALVAS
```

Este documento pode ser usado como guia de pesquisa operacional, mas ainda não deve ser tratado como regra final de execução.

Atualização metodológica importante:

```text
Para manter compatibilidade com o estudo histórico SofaScore, a definição operacional usada para favorito passa a ser:
favorite_side = menor odd pré-jogo 1X2, sem cutoff rígido de odd.
```

O corte `odd <= 1.70` foi considerado conservador demais para replicar a lógica histórica e reduziu excessivamente a amostra na temporada 2025/26.

---

# Curva média observada — Próximo Gol

Back Over equivalente:

| Minuto | Odd Média |
|----------|----------:|
| 60 | 1.50 |
| 65 | 1.60 |
| 70 | 1.80 |
| 75 | 2.00 |
| 80 | 2.45 |
| 85 | 3.35 |

Stake padrão utilizada nas simulações:

```text
100 unidades
```

---

# Resultado Consolidado Corrigido — EPL 2024/25 + EPL 2025/26

A média correta deve usar a regra histórica:

```text
Favorito = menor odd pré-jogo, sem cutoff de 1.70
```

Com isso, os números de 2025/26 considerados para comparação são os perfis SportMonks/proxy por menor odd, não o teste conservador com `odd <= 1.70`.

| Estratégia | Temporada | Acertos | Entradas | Taxa sem gol 60-75 | Taxa gol 60-75 |
|---|---|---:|---:|---:|---:|
| `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | 2024/25 | 40 | 54 | 74.1% | 25.9% |
| `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | 2025/26 | 48 | 69 | 69.6% | 30.4% |
| `favorite_winning_by_1 + h8_cold_combo_10m_2of3` | Consolidado | 88 | 123 | 71.5% | 28.5% |
| `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | 2024/25 | 29 | 38 | 76.3% | 23.7% |
| `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | 2025/26 | 30 | 42 | 71.4% | 28.6% |
| `favorite_winning_by_1 + h8_pressure_score_10m_bottom25` | Consolidado | 59 | 80 | 73.8% | 26.2% |

Leitura:

```text
As duas estratégias se mantêm acima de 70% no consolidado EPL.
A estratégia h8_pressure_score_10m_bottom25 tem maior taxa.
A estratégia h8_cold_combo_10m_2of3 tem maior amostra.
```

---

# Ranking Operacional Atualizado

Critérios:

```text
N > 20
Favorito = menor odd pré-jogo 1X2
Target: sem gol entre 60 e 75
Ordenação por equilíbrio entre N e taxa
```

---

## 1) favorite_winning_by_1 + h8_cold_combo_10m_2of3

### Classificação

```text
LAY OVER
JOGO FRIO
STATUS: APROVADO COM RESSALVAS
```

### Estatísticas por temporada

| Temporada | Entradas | Acertos | Erros | Taxa acerto | Taxa erro |
|---|---:|---:|---:|---:|---:|
| 2024/25 | 54 | 40 | 14 | 74.1% | 25.9% |
| 2025/26 | 69 | 48 | 21 | 69.6% | 30.4% |
| Consolidado | 123 | 88 | 35 | 71.5% | 28.5% |

### Entrada

```text
Minuto 60
Favorito pré-jogo pela menor odd vencendo por 1 gol
Jogo frio em 2 de 3 sinais H8
```

### Perfil operacional SportMonks 2025/26

| Métrica | Valor |
|---|---:|
| N | 69 |
| Sem gol 60-75 | 69.6% |
| Finalizações totais últimos 10 min média | 1.39 |
| Finalizações no gol últimos 10 min média | 0.65 |
| Dangerous Attacks últimos 10 min média | 8.38 |
| Key Passes últimos 10 min média | 0.90 |
| Big Chances Created últimos 10 min média | 0.36 |
| Corners últimos 10 min média | 0.74 |

### Saída

```text
Hold até 75'
```

### Parecer

```text
Estratégia mais robusta por amostra.
Consistente nas duas temporadas da Premier League.
A queda de 74.1% para 69.6% em 2025/26 exige ressalva, mas o consolidado de 71.5% em 123 entradas segue forte.
```

---

## 2) favorite_winning_by_1 + h8_pressure_score_10m_bottom25

### Classificação

```text
LAY OVER
JOGO FRIO
STATUS: APROVADO COM RESSALVAS
```

### Estatísticas por temporada

| Temporada | Entradas | Acertos | Erros | Taxa acerto | Taxa erro |
|---|---:|---:|---:|---:|---:|
| 2024/25 | 38 | 29 | 9 | 76.3% | 23.7% |
| 2025/26 | 42 | 30 | 12 | 71.4% | 28.6% |
| Consolidado | 80 | 59 | 21 | 73.8% | 26.2% |

### Entrada

```text
Minuto 60
Favorito pré-jogo pela menor odd vencendo por 1 gol
Pressure score dos últimos 10 minutos no bottom25
```

### Perfil operacional SportMonks 2025/26

| Métrica | Valor |
|---|---:|
| N | 42 |
| Sem gol 60-75 | 71.4% |
| Finalizações totais últimos 10 min média | 1.05 |
| Finalizações no gol últimos 10 min média | 0.12 |
| Dangerous Attacks últimos 10 min média | 8.45 |
| Key Passes últimos 10 min média | 0.74 |
| Big Chances Created últimos 10 min média | 0.05 |
| Corners últimos 10 min média | 0.64 |

### Saída

```text
Hold até 75'
```

### Parecer

```text
Estratégia com melhor taxa consolidada.
Amostra menor que cold_combo, mas consistente: 76.3% em 2024/25 e 71.4% em 2025/26.
```

---

# Estimativa Operacional com Odd Média Próximo Gol

Para Lay Over usando odd média 1.50:

```text
Lucro se não sair gol: +100
Perda se sair gol: -50
```

| Estratégia | N consolidado | Acerto | Erro | Lucro estimado | ROI estimado |
|---|---:|---:|---:|---:|---:|
| `h8_cold_combo_10m_2of3` | 123 | 88 | 35 | +7050 | +57.3% |
| `h8_pressure_score_10m_bottom25` | 80 | 59 | 21 | +4850 | +60.6% |

Cálculo:

```text
Lucro = acertos * 100 - erros * 50
ROI = lucro / (N * 100)
```

---

# Conclusão Atualizada

Podemos dizer que, na Premier League, as duas estratégias mostram consistência estatística exploratória:

```text
favorite_winning_by_1 + h8_cold_combo_10m_2of3
favorite_winning_by_1 + h8_pressure_score_10m_bottom25
```

Mas ainda com ressalvas:

- não é produção;
- não é robô;
- não é backtesting financeiro real;
- odds de entrada ainda são médias, não odds live reais por timestamp;
- precisa replicação multi-liga para robustez maior.

Decisão:

```text
APROVADO COM RESSALVAS PARA PESQUISA OPERACIONAL
```

---

# Próxima Etapa Recomendada

```text
SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1
```

Objetivo:

Testar novos combos por time usando SportMonks:

- time perdendo pressionando;
- favorito perdendo pressionando;
- adversário do favorito pressionando;
- mandante vencendo por 1 e visitante pressionando;
- dangerous attacks subindo;
- key passes subindo;
- big chances recentes;
- shots on target recentes.

Não avançar para robô ou produção.
