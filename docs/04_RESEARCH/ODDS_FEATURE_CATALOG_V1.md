## Status

Catálogo metodológico de features candidatas derivadas de odds históricas.

Não contém código.

Não contém dataset.

Não contém baseline.

Não contém modelo.

Não contém backtesting.

Não contém produção.

---

# 1. Objetivo

Formalizar as features candidatas derivadas da integração Football-Data.

Mercados aprovados para pesquisa:

1. Over/Under 2.5
2. Match Odds 1X2
3. Asian Handicap

Objetivo principal:

Avaliar se expectativas implícitas do mercado pré-jogo possuem relação com:

* gols tardios;
* pressão ofensiva posterior;
* estados específicos da partida;
* interações futuras com H8 e Segmentação.

---

# 2. Regras Gerais Anti-Leakage

Todas as features deste catálogo devem obedecer:

```text
Disponíveis antes do kickoff.
```

Proibido:

* odds live;
* odds in-play;
* odds atualizadas após kickoff;
* mercados resolvidos após início da partida.

Prioridade:

```text
Closing Odds Pré-Jogo
```

---

# 3. Features — Over/Under 2.5

## OU_01

### Nome

```text
implied_prob_over25
```

### Definição

Probabilidade implícita do mercado Over 2.5.

### Interpretação

Mercado espera muitos gols.

### Hipótese

Jogos com alta expectativa de gols possuem maior frequência de gols tardios.

### Leakage

Baixo.

### Prioridade

ALTA.

### Dependências

Closing odds Over 2.5.

---

## OU_02

### Nome

```text
implied_prob_under25
```

### Definição

Probabilidade implícita do mercado Under 2.5.

### Interpretação

Mercado espera poucos gols.

### Hipótese

Pode identificar jogos mais fechados.

### Leakage

Baixo.

### Prioridade

ALTA.

### Dependências

Closing odds Under 2.5.

---

## OU_03

### Nome

```text
over25_market_balance
```

### Definição

Equilíbrio entre Over e Under.

### Interpretação

Mercado indeciso.

### Hipótese

Jogos com incerteza podem gerar maior volatilidade tardia.

### Leakage

Baixo.

### Prioridade

MÉDIA.

---

## OU_04

### Nome

```text
over25_closing_strength
```

### Definição

Força relativa do Over em relação ao Under.

### Interpretação

Quanto maior, maior expectativa ofensiva.

### Hipótese

Pode explicar gols após 75.

### Leakage

Baixo.

### Prioridade

ALTA.

---

# 4. Features — Match Odds 1X2

## MO_01

### Nome

```text
implied_prob_home
```

### Definição

Probabilidade implícita da vitória do mandante.

### Interpretação

Força esperada do mandante.

### Hipótese

Favoritos podem gerar pressão tardia.

### Leakage

Baixo.

### Prioridade

ALTA.

---

## MO_02

### Nome

```text
implied_prob_draw
```

### Definição

Probabilidade implícita de empate.

### Interpretação

Mercado espera equilíbrio.

### Hipótese

Jogos equilibrados podem permanecer vivos até o final.

### Leakage

Baixo.

### Prioridade

MÉDIA.

---

## MO_03

### Nome

```text
implied_prob_away
```

### Definição

Probabilidade implícita da vitória do visitante.

### Interpretação

Força esperada do visitante.

### Hipótese

Permite medir favoritismo visitante.

### Leakage

Baixo.

### Prioridade

ALTA.

---

## MO_04

### Nome

```text
favorite_strength
```

### Definição

Intensidade do favoritismo.

### Interpretação

Quanto maior, mais forte o favorito.

### Hipótese

Favoritos fortes empatando aos 60–75 podem aumentar pressão ofensiva.

### Leakage

Baixo.

### Prioridade

MUITO ALTA.

---

## MO_05

### Nome

```text
match_balance
```

### Definição

Equilíbrio entre as probabilidades de vitória.

### Interpretação

Mede quão aberto ou equilibrado é o confronto.

### Hipótese

Confrontos equilibrados podem gerar mais instabilidade tardia.

### Leakage

Baixo.

### Prioridade

ALTA.

---

## MO_06

### Nome

```text
favorite_side
```

### Definição

Identifica qual equipe é favorita.

### Interpretação

Mandante favorito ou visitante favorito.

### Hipótese

Permite futuras interações com Match State.

### Leakage

Baixo.

### Prioridade

MÉDIA.

---

# 5. Features — Asian Handicap

## AH_01

### Nome

```text
handicap_line
```

### Definição

Linha principal de handicap.

### Interpretação

Expectativa de diferença de força.

### Hipótese

Linhas extremas podem indicar dominância esperada.

### Leakage

Baixo.

### Prioridade

ALTA.

---

## AH_02

### Nome

```text
favorite_handicap
```

### Definição

Handicap associado ao favorito.

### Interpretação

Tamanho esperado da superioridade.

### Hipótese

Favoritos muito superiores podem manter pressão até o final.

### Leakage

Baixo.

### Prioridade

ALTA.

---

## AH_03

### Nome

```text
handicap_implied_strength
```

### Definição

Força implícita derivada do handicap.

### Interpretação

Proxy alternativa para diferença de qualidade.

### Hipótese

Pode superar Match Odds em capacidade explicativa.

### Leakage

Baixo.

### Prioridade

MÉDIA-ALTA.

---

## AH_04

### Nome

```text
handicap_market_confidence
```

### Definição

Confiança do mercado na linha de handicap.

### Interpretação

Convicção sobre superioridade de uma equipe.

### Hipótese

Pode melhorar interações com H8.

### Leakage

Baixo.

### Prioridade

MÉDIA.

---

# 6. Features que Representam Expectativa de Gols

Prioridade:

1. implied_prob_over25
2. implied_prob_under25
3. over25_closing_strength
4. over25_market_balance

---

# 7. Features que Representam Força Relativa

Prioridade:

1. favorite_strength
2. implied_prob_home
3. implied_prob_away
4. handicap_line
5. favorite_handicap

---

# 8. Features que Representam Desequilíbrio Entre Equipes

Prioridade:

1. favorite_strength
2. match_balance
3. handicap_line
4. handicap_implied_strength

---

# 9. Features Mais Promissoras para Interação com H8

Prioridade:

### Grupo A

favorite_strength

*

shots_last_10m

### Grupo B

favorite_strength

*

momentum_trend_last_10m

### Grupo C

implied_prob_over25

*

shots_last_10m

### Grupo D

over25_closing_strength

*

momentum_trend_last_10m

---

# 10. Features Mais Promissoras para Interação com Segmentação

### Grupo A

favorite_strength

*

defensivo_fragile

### Grupo B

favorite_strength

*

ofensivo_forte_vs_defesa_fragil

### Grupo C

implied_prob_over25

*

defensivo_fragile

### Grupo D

handicap_line

*

ofensivo_strong

---

# 11. Priorização Final

## Prioridade 1

```text
favorite_strength
```

## Prioridade 2

```text
implied_prob_over25
```

## Prioridade 3

```text
match_balance
```

## Prioridade 4

```text
favorite_handicap
```

## Prioridade 5

```text
over25_closing_strength
```

---

# 12. Próxima Etapa Recomendada

Não criar features ainda.

Não criar dataset ainda.

Próxima frente recomendada:

```text
ODDS INITIAL STATISTICAL VALIDATION
```

Objetivo:

Avaliar individualmente as features prioritárias contra:

* gol após 60
* gol após 65
* gol após 70
* gol após 75

antes de qualquer interação com H8 ou Segmentação.

---

# 13. Decisão Quant

```text
CATÁLOGO APROVADO
```

Pronto para revisão do PM.
