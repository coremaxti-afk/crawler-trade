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

# Ranking Operacional

Critérios:

```text
N > 20
Estratégias estatisticamente validadas
Ordenação por retorno esperado
```

---

## 1) favorite_winning_by_1 + h8_cold_combo_10m_2of3

### Classificação

```text
LAY OVER
JOGO FRIO
```

### Estatísticas

| Métrica | Valor |
|----------|----------:|
| N | 54 |
| Sem gol 60-75 | 74.1% |
| ROI estimado | +61.15% |
| Lucro estimado | +3302.10 |

### Entrada

```text
Minuto 60
Favorito vencendo por 1 gol
```

### Interpretação

O jogo apresenta sinais consistentes de esfriamento ofensivo.

Pelo menos 2 dos 3 grupos:

- poucos chutes
- baixo xG
- momentum fraco

### Saída

```text
Hold até 75'
```

### Parecer

```text
Melhor estratégia encontrada até o momento.
Maior amostra.
Maior robustez.
```

---

## 2) favorite_winning_by_1 + h8_pressure_score_10m_bottom25

### Classificação

```text
LAY OVER
JOGO FRIO
```

### Estatísticas

| Métrica | Valor |
|----------|----------:|
| N | 36 |
| Sem gol 60-75 | 75.0% |
| ROI estimado | +62.50% |
| Lucro estimado | +2250.00 |

### Entrada

```text
Minuto 60
Favorito vencendo por 1 gol
```

### Interpretação

O score composto de pressão está entre os 25% mais baixos da base.

Componentes:

- chutes
- xG
- momentum médio
- momentum trend

### Saída

```text
Hold até 75'
```

### Parecer

```text
Melhor ROI por operação.
Menor amostra que a estratégia #1.
```

---

## 3) favorite_winning_by_1 + h8_cold_combo_10m_2of3 (Dinâmico)

### Classificação

```text
LAY OVER
PROTOCOLO DINÂMICO
```

### Estatísticas

| Métrica | Valor |
|----------|----------:|
| N | 54 |
| ROI estimado | +22.3% |

### Entrada

```text
Minuto 60
Favorito vencendo por 1
```

### Reavaliação

```text
70-75 minutos
```

### Lógica

Continuar somente se o jogo permanecer frio.

### Parecer

```text
Inferior ao hold simples.
```

---

## 4) favorite_winning_by_1 + h8_pressure_score_10m_bottom25 (Dinâmico)

### Classificação

```text
LAY OVER
PROTOCOLO DINÂMICO
```

### Estatísticas

| Métrica | Valor |
|----------|----------:|
| N | 36 |
| ROI estimado | +21.4% |

### Entrada

```text
Minuto 60
Favorito vencendo por 1
```

### Reavaliação

```text
70-75 minutos
```

### Parecer

```text
Inferior ao hold simples.
```

---

## 5) home_winning_by_1 + h8_pressure_score_10m_top25

### Classificação

```text
BACK OVER
JOGO QUENTE
```

### Estatísticas

| Métrica | Valor |
|----------|----------:|
| N | 23 |
| ROI Dinâmico | +7.6% |

### Entrada

```text
Minuto 65
Mandante vencendo por 1
```

### Reavaliação

```text
75 minutos
```

### Continuar

Se:

- pressão continua alta
- xG continua alto
- chutes continuam aparecendo

### Cashout

Se:

- jogo esfriar
- pressão desaparecer
- ausência de finalizações perigosas

### Parecer

```text
Melhor estratégia Back Over com N > 20.
```

---

## Estratégia Complementar

### home_winning_by_1 + h8_shot_quality_top25

| Métrica | Valor |
|----------|----------:|
| N | 20 |
| ROI Hold | +12.0% |
| ROI Dinâmico | +16.2% |

### Observação

```text
Não entrou no ranking oficial por possuir exatamente 20 jogos.
Mas é atualmente a estratégia Back Over mais interessante.
```

---

# Conclusões

## Grupo mais forte

```text
LAY OVER
```

Estratégias:

- favorite_winning_by_1 + h8_cold_combo_10m_2of3
- favorite_winning_by_1 + h8_pressure_score_10m_bottom25

---

## Melhor Back Over

```text
home_winning_by_1 + h8_shot_quality_top25
home_winning_by_1 + h8_pressure_score_10m_top25
```

---

# Pendência Metodológica

As configurações operacionais apresentadas neste documento ainda são aproximações.

Necessário executar estudo complementar:

```text
docs/04_RESEARCH/TRADE_ENTRY_PROFILE_ANALYSIS_V1.md
```

Objetivo:

Calcular os perfis médios reais de entrada de cada estratégia.

Para cada estratégia medir:

- finalizações últimos 10 min
- finalizações no gol últimos 10 min
- xG últimos 10 min
- xGOT últimos 10 min
- chances de gol
- contra-ataques
- momentum médio
- momentum trend
- estado do placar
- odds médias observadas

Resultado esperado:

Transformar os sinais estatísticos em parâmetros operacionais concretos para configuração de bot.
