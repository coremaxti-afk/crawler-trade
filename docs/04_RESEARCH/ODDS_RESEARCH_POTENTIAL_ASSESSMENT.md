## 1. Diagnóstico Quantitativo

A integração Football-Data abre uma nova frente relevante porque odds representam a expectativa agregada do mercado antes do jogo.

Status da base:

* 380 partidas mapeadas
* 34.280 odds históricas
* mercados 1X2, Over/Under 2.5 e Asian Handicap
* closing, average e max odds disponíveis
* integridade validada
* idempotência validada

Parecer Quant:

```text
ODDS DEVEM VIRAR NOVA FRENTE PRIORITÁRIA DE PESQUISA
```

Motivo:

As odds podem capturar informação pré-jogo que H3/H4 tentaram aproximar por estatísticas históricas, mas de forma mais agregada e eficiente.

---

## 2. Mercados com Maior Potencial

### Prioridade 1 — Over/Under 2.5

Maior potencial para gols tardios.

Motivo:

* mercado diretamente relacionado à expectativa de gols;
* pode indicar jogos com maior probabilidade de volume ofensivo;
* deve ser o primeiro mercado analisado.

Features futuras candidatas:

* implied_prob_over25
* implied_prob_under25
* over25_market_balance
* over25_closing_strength

---

### Prioridade 2 — Match Odds 1X2

Potencial médio-alto.

Motivo:

* captura força relativa entre equipes;
* pode ajudar a identificar favorito forte, equilíbrio ou zebra;
* útil para interação com estado do placar.

Features futuras candidatas:

* implied_prob_home
* implied_prob_draw
* implied_prob_away
* favorite_strength
* match_balance
* favorite_side

---

### Prioridade 3 — Asian Handicap

Potencial alto, mas mais complexo.

Motivo:

* representa expectativa de diferença de força;
* pode capturar dominância esperada melhor que 1X2;
* exige cuidado metodológico por linhas diferentes.

Features futuras candidatas:

* handicap_line
* favorite_handicap
* handicap_implied_strength
* handicap_market_confidence

---

## 3. Odds Prioritárias

Ordem recomendada:

1. Closing odds
2. Average odds
3. Max odds

### Closing Odds

Melhor proxy de expectativa final pré-jogo.

Risco:

* se forem obtidas após kickoff ou muito perto do jogo, é preciso garantir que são pré-jogo.

### Average Odds

Boa para reduzir ruído de uma única casa.

### Max Odds

Úteis para análise de dispersão, mas menor prioridade inicial.

---

## 4. Hipóteses Novas Possíveis

### O1 — Expectativa de Gols

Jogos com alta probabilidade implícita de Over 2.5 têm maior frequência de gols após 75.

Prioridade:

```text
ALTA
```

---

### O2 — Favorito Forte Perdendo ou Empatando

Favorito pré-jogo forte que chega aos 60/70 empatando ou perdendo pode gerar pressão tardia.

Prioridade:

```text
MUITO ALTA
```

---

### O3 — Jogo Equilibrado

Jogos com odds 1X2 equilibradas podem ter maior instabilidade e mais gols tardios.

Prioridade:

```text
MÉDIA
```

---

### O4 — Mercado Esperava Jogo Fechado, mas H8 Mostra Pressão

Under pré-jogo forte + shots_last_10m alto pode indicar mudança de regime in-game.

Prioridade:

```text
ALTA
```

---

### O5 — Asian Handicap e Fragilidade Real

Favorito por handicap alto contra defesa frágil pode ter maior chance de gol tardio se o jogo ainda estiver aberto.

Prioridade:

```text
MÉDIA-ALTA
```

---

## 5. Riscos Metodológicos

Principais riscos:

* usar odds capturadas após kickoff;
* misturar closing odds com informação in-play;
* usar odds finais sem confirmar timestamp;
* overfitting em muitos mercados;
* múltiplos testes excessivos;
* interpretar odds como causalidade;
* comparar odds de casas diferentes sem normalização;
* não remover margem da casa.

---

## 6. Possíveis Fontes de Leakage

### Leakage alto

* odds live/in-play;
* odds atualizadas após início do jogo;
* odds após escalações se o objetivo for modelo muito pré-jogo;
* qualquer odds gerada depois do minuto de previsão.

### Leakage médio

* closing odds sem timestamp claro;
* max odds se vierem de momentos posteriores ao kickoff;
* odds agregadas sem saber janela temporal.

### Leakage baixo

* odds pré-jogo confirmadas;
* closing odds claramente pré-kickoff;
* average odds históricas pré-jogo.

Regra obrigatória:

```text
Toda odds usada como feature deve estar disponível antes do kickoff.
```

---

## 7. Estratégia Recomendada

### Fase 1 — Auditoria de Odds

Antes de criar features:

* confirmar mercados disponíveis por partida;
* confirmar cobertura por mercado;
* confirmar se closing odds são pré-jogo;
* mapear casas/bookmakers;
* verificar nulos;
* verificar linhas Asian Handicap;
* verificar linhas Over/Under.

---

### Fase 2 — Catálogo de Features Odds

Criar documento:

```text
docs/04_RESEARCH/ODDS_FEATURE_CATALOG_V1.md
```

Sem implementação ainda.

---

### Fase 3 — Validação Estatística Inicial

Começar por:

1. Over/Under 2.5
2. Match Odds 1X2
3. Asian Handicap

Targets:

* target_late_goal_75
* gol após 60
* gol após 65
* gol após 70
* gol após 75

---

### Fase 4 — Interações

Só depois da análise isolada.

Interações prioritárias:

* Odds + H8
* Odds + Match State
* Odds + Segmentação
* Odds + Segmentação + H8

---

## 8. Priorização Final de Hipóteses Odds

### Prioridade 1

```text
O1 — Over/Under 2.5 vs gols tardios
```

### Prioridade 2

```text
O2 — Favorito forte + estado adverso no placar
```

### Prioridade 3

```text
O4 — Under pré-jogo + pressão H8 recente
```

### Prioridade 4

```text
O3 — equilíbrio pré-jogo via 1X2
```

### Prioridade 5

```text
O5 — Asian Handicap + fragilidade defensiva
```

---

## 9. Decisão Quant

Parecer:

```text
APROVADO COMO NOVA FRENTE PRIORITÁRIA
```

Mas ainda não autorizado para:

* código;
* feature builder;
* dataset;
* baseline;
* modelo;
* backtesting;
* produção.

Próxima etapa recomendada:

```text
Criar ODDS_FEATURE_CATALOG_V1.md
```

Objetivo:

Formalizar mercados, odds permitidas, fórmulas, risco de leakage e hipóteses antes de qualquer implementação.
