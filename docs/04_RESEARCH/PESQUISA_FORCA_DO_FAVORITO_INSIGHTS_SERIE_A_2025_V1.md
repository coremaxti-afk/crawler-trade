# PESQUISA_FORCA_DO_FAVORITO_INSIGHTS_SERIE_A_2025_V1

Data: 2026-06-18

Agente: 05 - Data Science / Quant Research

## Resumo Executivo

A pesquisa de força do favorito na Serie A 2025 não encontrou uma nova estratégia vencedora.

Ela explicou por que a principal estratégia descoberta no Discovery V4 funciona.

Conclusão principal:

```text
O edge da estratégia não depende apenas do estado do jogo.

Ele depende da combinação:

favorito forte
+
vencendo por 1 gol
+
adversário frio
```

---

## Descoberta 1 - A estratégia líder continua sendo a mesma

A principal estratégia dependente de favorito encontrada no Discovery V4 continua sendo:

```text
favorite_winning_by_1_opp_cold_2of3
```

Ela aparece repetidamente entre os resultados PROMISSORES da Serie A 2025.

Interpretação:

```text
A pesquisa de força do favorito não substituiu a estratégia.
Ela refinou a compreensão do edge.
```

---

## Descoberta 2 - Nem todo favorito é igual

Hipótese inicial:

```text
A estratégia funciona para qualquer favorito.
```

Resultado observado:

```text
A estratégia foi classificada como:

FUNCIONA_FAVORITO_FORTE
```

Implicação:

```text
Misturar todos os favoritos reduz a capacidade de entender onde o edge realmente existe.
```

---

## Descoberta 3 - O edge parece concentrado em favoritos fortes

O melhor equilíbrio entre:

```text
N
lucro
ROI
EV
robustez
```

foi encontrado repetidamente na categoria:

```text
FAVORITO_FORTE
```

Observação:

```text
SUPER_FAVORITO apresentou algumas linhas com métricas excelentes,
mas frequentemente com amostras menores.
```

---

## Descoberta 4 - Super favorito não é automaticamente melhor

Hipótese gerada:

```text
O mercado pode precificar corretamente parte da vantagem dos super favoritos.
```

Possível consequência:

```text
Favoritos fortes podem apresentar melhor equilíbrio entre:

força esportiva
+
ineficiência de mercado
```

Status:

```text
HIPOTESE
NAO VALIDADA
```

Requer análise multi-liga e multi-temporada.

---

## Descoberta 5 - O lado Over permanece frágil

As estratégias:

```text
favorite_losing_pressure_high_2of3
underdog_winning_favorite_pressing_2of3
favorite_drawing_pressure_high_2of3
```

apresentaram sinais interessantes em algumas linhas.

Porém:

```text
N insuficiente
fragmentação excessiva
baixa robustez
```

Conclusão:

```text
Não devem entrar no pipeline principal neste momento.
```

---

## Nova leitura operacional da estratégia líder

Antes:

```text
favorite_winning_by_1_opp_cold_2of3
```

Depois da pesquisa:

```text
favorite_winning_by_1_opp_cold_2of3
+
FAVORITO_FORTE
```

Esta passa a ser a interpretação operacional preferencial para Serie A 2025.

---

## Hipóteses geradas para pesquisas futuras

### Hipótese H1

```text
Favoritos fortes são mais rentáveis que super favoritos.
```

Validar em:

```text
EPL
La Liga
Serie A
Bundesliga
Ligue 1
```

---

### Hipótese H2

```text
A força do favorito é parte estrutural do edge
em estratégias de Under tardio.
```

Validar em:

```text
favorite_winning_by_1_opp_cold_2of3
team_winning_by_1_opp_cold_2of3
```

---

### Hipótese H3

```text
Segmentar favoritos reduz ruído estatístico.
```

Validar comparando:

```text
estratégia agregada
vs
estratégia segmentada por força do favorito
```

---

## Parecer do Agente 05

A pesquisa foi aprovada e considerada útil.

Resultado principal:

```text
A força do favorito não é um filtro cosmético.

Ela explica parte relevante do edge da principal estratégia da Serie A 2025.
```

Recomendação:

```text
Executar a mesma frente em EPL e La Liga antes de transformar o filtro em regra global do projeto.
```
