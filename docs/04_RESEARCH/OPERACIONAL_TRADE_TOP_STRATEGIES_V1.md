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

Ressalva principal:

```text
As estratégias com favorite_winning_by_1 ainda dependem de validação definitiva do favorito pré-jogo via odds.
```

Na etapa SportMonks, quando o favorito pré-jogo não estava disponível de forma consolidada, foi usado um proxy operacional:

```text
time vencendo por 1 gol no cutoff
```

Portanto, os resultados abaixo preservam o valor prático da leitura de jogo frio/quente, mas as estratégias com `favorite_*` ainda precisam ser reexecutadas com favorito pré-jogo real.

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

Observação:

```text
Ranking mantido como referência histórica.
Entradas favorite_* devem ser lidas com ressalva até validação do favorito pré-jogo.
```

---

## 1) favorite_winning_by_1 + h8_cold_combo_10m_2of3

### Classificação

```text
LAY OVER
JOGO FRIO
STATUS: APROVADO COM RESSALVAS
```

### Ressalva

```text
A reprodução SportMonks ainda não validou favorito pré-jogo.
Proxy usado na etapa operacional: time vencendo por 1 no cutoff.
```

### Estatísticas históricas originais

| Métrica | Valor |
|----------|----------:|
| N | 54 |
| Sem gol 60-75 | 74.1% |
| ROI estimado | +61.15% |
| Lucro estimado | +3302.10 |

### Perfil operacional SportMonks com proxy

| Métrica | Valor |
|---|---:|
| N proxy | 69 |
| Sem gol 60-75 | 69.6% |
| Finalizações totais últimos 10 min média | 1.39 |
| Finalizações no gol últimos 10 min média | 0.65 |
| Dangerous Attacks últimos 10 min média | 8.38 |
| Key Passes últimos 10 min média | 0.90 |
| Big Chances Created últimos 10 min média | 0.36 |
| Corners últimos 10 min média | 0.74 |

### Entrada

```text
Minuto 60
Favorito vencendo por 1 gol
```

Até validar favorito pré-jogo, leitura operacional aproximada:

```text
Minuto 60
Time vencendo por 1 gol
Jogo frio nos últimos 10 minutos
```

### Interpretação

O jogo apresenta sinais consistentes de esfriamento ofensivo.

Pelo menos 2 dos 3 grupos:

- poucos chutes
- baixa criação/perigo
- momentum/pressão fraca

### Saída

```text
Hold até 75'
```

### Parecer

```text
Melhor estratégia encontrada até o momento.
Maior amostra.
Maior robustez.
Ainda precisa validação definitiva do favorito pré-jogo.
```

---

## 2) favorite_winning_by_1 + h8_pressure_score_10m_bottom25

### Classificação

```text
LAY OVER
JOGO FRIO
STATUS: APROVADO COM RESSALVAS
```

### Ressalva

```text
A reprodução SportMonks ainda não validou favorito pré-jogo.
Proxy usado na etapa operacional: time vencendo por 1 no cutoff.
```

### Estatísticas históricas originais

| Métrica | Valor |
|----------|----------:|
| N | 36 |
| Sem gol 60-75 | 75.0% |
| ROI estimado | +62.50% |
| Lucro estimado | +2250.00 |

### Perfil operacional SportMonks com proxy

| Métrica | Valor |
|---|---:|
| N proxy | 42 |
| Sem gol 60-75 | 71.4% |
| Finalizações totais últimos 10 min média | 1.05 |
| Finalizações no gol últimos 10 min média | 0.12 |
| Dangerous Attacks últimos 10 min média | 8.45 |
| Key Passes últimos 10 min média | 0.74 |
| Big Chances Created últimos 10 min média | 0.05 |
| Corners últimos 10 min média | 0.64 |

### Entrada

```text
Minuto 60
Favorito vencendo por 1 gol
```

Até validar favorito pré-jogo, leitura operacional aproximada:

```text
Minuto 60
Time vencendo por 1 gol
Pressão ofensiva no quartil inferior
```

### Interpretação

O score composto de pressão está entre os 25% mais baixos da base.

Componentes:

- chutes
- criação/perigo
- dangerous attacks
- key passes
- big chances

### Saída

```text
Hold até 75'
```

### Parecer

```text
Melhor ROI por operação na leitura original.
Menor amostra que a estratégia #1.
Ainda precisa validação definitiva do favorito pré-jogo.
```

---

## 3) favorite_winning_by_1 + h8_cold_combo_10m_2of3 (Dinâmico)

### Classificação

```text
LAY OVER
PROTOCOLO DINÂMICO
STATUS: APROVADO COM RESSALVAS
```

### Ressalva

```text
A reprodução SportMonks ainda não validou favorito pré-jogo.
Proxy usado na etapa operacional: time vencendo por 1 no cutoff.
```

### Estatísticas históricas originais

| Métrica | Valor |
|----------|----------:|
| N | 54 |
| ROI estimado | +22.3% |

### Perfil dinâmico SportMonks com proxy

| Grupo | N | Gol 60-75 | Sem gol 60-75 | Gol 70-75 | Sem gol 70-75 |
|---|---:|---:|---:|---:|---:|
| Continuou frio | 26 | 11.5% | 88.5% | 3.8% | 96.2% |
| Esquentou | 43 | 41.9% | 58.1% | 9.3% | 90.7% |

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
Inferior ao hold simples na simulação financeira anterior.
Mas a reavaliação SportMonks mostra forte separação entre continuou frio e esquentou.
Ainda precisa validação definitiva do favorito pré-jogo.
```

---

## 4) favorite_winning_by_1 + h8_pressure_score_10m_bottom25 (Dinâmico)

### Classificação

```text
LAY OVER
PROTOCOLO DINÂMICO
STATUS: APROVADO COM RESSALVAS
```

### Ressalva

```text
A reprodução SportMonks ainda não validou favorito pré-jogo.
Proxy usado na etapa operacional: time vencendo por 1 no cutoff.
```

### Estatísticas históricas originais

| Métrica | Valor |
|----------|----------:|
| N | 36 |
| ROI estimado | +21.4% |

### Perfil dinâmico SportMonks com proxy

| Grupo | N | Gol 60-75 | Sem gol 60-75 | Gol 70-75 | Sem gol 70-75 |
|---|---:|---:|---:|---:|---:|
| Continuou frio | 14 | 7.1% | 92.9% | 0.0% | 100.0% |
| Esquentou | 28 | 39.3% | 60.7% | 7.1% | 92.9% |

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
Inferior ao hold simples na simulação financeira anterior.
Mas a reavaliação SportMonks mostra que continuar frio é um filtro operacional forte.
Ainda precisa validação definitiva do favorito pré-jogo.
```

---

## 5) home_winning_by_1 + h8_pressure_score_10m_top25

### Classificação

```text
BACK OVER
JOGO QUENTE
STATUS: OBSERVAÇÃO
```

### Estatísticas históricas originais

| Métrica | Valor |
|----------|----------:|
| N | 23 |
| ROI Dinâmico | +7.6% |

### Perfil operacional SportMonks

| Métrica | Valor |
|---|---:|
| N proxy/reprodução | 22 |
| Gol após cutoff | 36.4% |
| Finalizações totais últimos 10 min média | 4.09 |
| Finalizações no gol últimos 10 min média | 1.91 |
| Dangerous Attacks últimos 10 min média | 10.00 |
| Key Passes últimos 10 min média | 3.09 |
| Big Chances Created últimos 10 min média | 1.18 |
| Corners últimos 10 min média | 1.27 |

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
- chutes continuam aparecendo
- key passes continuam altos
- big chances continuam aparecendo

### Cashout

Se:

- jogo esfriar
- pressão desaparecer
- ausência de finalizações perigosas

### Parecer

```text
Melhor Back Over com N > 20 no documento original.
Na leitura SportMonks recente ficou mais fraco que as estratégias Lay Over.
Manter em observação.
```

---

## Estratégia Complementar

### home_winning_by_1 + h8_shot_quality_top25

| Métrica | Valor |
|----------|----------:|
| N histórico | 20 |
| ROI Hold histórico | +12.0% |
| ROI Dinâmico histórico | +16.2% |
| N SportMonks | 22 |
| Gol após cutoff SportMonks | 31.8% |

### Perfil operacional SportMonks

| Métrica | Valor |
|---|---:|
| Finalizações totais últimos 10 min média | 3.73 |
| Finalizações no gol últimos 10 min média | 1.91 |
| Dangerous Attacks últimos 10 min média | 8.91 |
| Key Passes últimos 10 min média | 2.95 |
| Big Chances Created últimos 10 min média | 1.36 |
| Corners últimos 10 min média | 1.00 |

### Observação

```text
Não entrou no ranking oficial original por possuir exatamente 20 jogos.
Na leitura SportMonks recente, ficou em observação e não superou as estratégias Lay Over.
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

Ressalva:

```text
O termo favorite_winning_by_1 ainda precisa ser validado por odds pré-jogo.
Até lá, os perfis SportMonks devem ser interpretados como time vencendo por 1 + jogo frio.
```

---

## Melhor Back Over

```text
home_winning_by_1 + h8_pressure_score_10m_top25
home_winning_by_1 + h8_shot_quality_top25
```

Status:

```text
OBSERVAÇÃO
```

Motivo:

```text
Na leitura SportMonks recente, o Back Over ficou mais fraco do que o Lay Over frio.
```

---

# Sugestão Operacional Temporária

Enquanto o favorito pré-jogo não for validado, a regra operacional mais segura é tratar como estudo de proxy:

```text
Minuto 60
Time vencendo por 1 gol
Jogo frio nos últimos 10 minutos
Lay Over Próximo Gol
```

Parâmetros aproximados derivados do perfil SportMonks:

```text
Finalizações totais últimos 10 min <= 1 a 2
Finalizações no gol últimos 10 min = 0
Big Chances Created últimos 10 min = 0
Key Passes últimos 10 min <= 1
Dangerous Attacks últimos 10 min <= 8 a 9
Corners últimos 10 min <= 1
```

Esses parâmetros devem ser recalibrados quando houver favorito pré-jogo real.

---

# Pendência Metodológica

As configurações operacionais apresentadas neste documento ainda são aproximações.

A principal pendência atual é:

```text
Validar favorito pré-jogo via odds.
```

Documento/estudo complementar recomendado:

```text
docs/04_RESEARCH/PRE_MATCH_FAVORITE_VALIDATION_V1.md
```

Objetivo:

```text
Integrar odds pré-jogo para marcar favorito real antes da partida e reexecutar as estratégias favorite_*.
```

Também é necessário manter o estudo:

```text
docs/04_RESEARCH/TRADE_ENTRY_PROFILE_ANALYSIS_V1.md
```

Objetivo:

Calcular e revisar os perfis médios reais de entrada de cada estratégia.

Para cada estratégia medir:

- finalizações últimos 10 min
- finalizações no gol últimos 10 min
- dangerous attacks últimos 10 min
- key passes últimos 10 min
- big chances created últimos 10 min
- corners últimos 10 min
- posse snapshot no cutoff
- estado do placar
- odds médias observadas
- favorito pré-jogo validado

Resultado esperado:

Transformar os sinais estatísticos em parâmetros operacionais concretos para configuração de plataforma, com separação clara entre:

```text
resultado histórico original
resultado SportMonks com proxy
resultado definitivo com favorito pré-jogo
```
