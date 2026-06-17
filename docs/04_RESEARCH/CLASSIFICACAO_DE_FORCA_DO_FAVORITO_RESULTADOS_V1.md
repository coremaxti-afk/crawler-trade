# CLASSIFICACAO_DE_FORCA_DO_FAVORITO_RESULTADOS_V1

Agente responsavel: `05 - Data Science / Quant Research`

Status: `DESENHO METODOLOGICO APROVADO - EXECUCAO DEPENDE DAS BASES POR LIGA/TEMPORADA`

Data: 2026-06-17

---

## 1. Objetivo

Criar uma camada de avaliacao para medir se as estrategias que usam favorito pre-jogo funcionam para qualquer favorito ou apenas para uma faixa especifica de odd.

Regra mantida do projeto:

```text
favorito = menor odd pre-jogo entre mandante e visitante
empate nunca define favorito
```

Fontes esperadas:

```text
Football-Data: AvgH, AvgD, AvgA
SportMonks: trends, timeline, match_state, identity
Outputs existentes: discovery entries/summary e, quando disponivel, outputs do Agente 06
```

---

## 2. Decisao de prioridade no projeto

Esta frente deve acontecer:

```text
DEPOIS do discovery bruto da liga/temporada
ANTES do ranking financeiro final e antes da promocao operacional pelo Agente 06
```

Motivo:

1. O discovery precisa primeiro encontrar quais estrategias existem e quais tem sinal.
2. A classificacao de forca do favorito deve segmentar apenas as estrategias que dependem de favorito.
3. O Agente 06 deve receber a estrategia ja segmentada por categoria de favorito, para evitar misturar super favorito com favorito fraco.

Fluxo recomendado:

```text
Discovery bruto por liga/temporada
-> Drawdown Audit original
-> Classificacao de Forca do Favorito
-> Agente 06: ROI / EV / lucro / drawdown por segmento
-> Ranking operacional final
```

---

## 3. Hipotese de pesquisa

Hipotese principal:

```text
Estrategias com favorite_* podem ter performance diferente conforme a forca pre-jogo do favorito.
```

Exemplos onde isso pode mudar a leitura:

```text
favorite_winning_by_1_opp_cold_2of3
favorite_losing_pressure_high_2of3
favorite_drawing_pressure_high_2of3
underdog_winning_favorite_pressing_2of3
```

Risco atual:

```text
Misturar favorito de odd 1.25 com favorito de odd 2.20 pode esconder padroes importantes.
```

---

## 4. Campos obrigatorios

Por jogo:

```text
league
season
fixture_id
home_team
away_team
home_goals_final
away_goals_final
AvgH
AvgD
AvgA
home_odd
away_odd
draw_odd
favorite_side
favorite_odd
underdog_odd
odds_gap
favorite_implied_raw
favorite_implied_norm
favorite_result
favorite_goals_for
favorite_goals_against
```

Por linha de estrategia:

```text
strategy_name
family
league
season
cutoff
window
target
team_side
favorite_side
favorite_strength_category
n
wins
losses
strike_rate
baseline_rate
diff_vs_baseline
p_value
odds_ratio
roi_estimated
ev_estimated
profit_estimated
max_drawdown
loss_streak
final_classification
```

---

## 5. Definicoes matematicas

### 5.1 Favorite odd

```text
favorite_odd = min(AvgH, AvgA)
```

### 5.2 Favorite side

```text
se AvgH < AvgA -> favorite_side = home
se AvgA < AvgH -> favorite_side = away
se AvgH == AvgA -> favorite_side = no_clear_favorite
```

### 5.3 Underdog odd

```text
underdog_odd = max(AvgH, AvgA)
```

### 5.4 Odds gap

```text
odds_gap = underdog_odd - favorite_odd
```

### 5.5 Implied probability raw

```text
favorite_implied_raw = 1 / favorite_odd
```

### 5.6 Implied probability normalizada 1X2

```text
raw_home = 1 / AvgH
raw_draw = 1 / AvgD
raw_away = 1 / AvgA
raw_total = raw_home + raw_draw + raw_away
favorite_implied_norm = raw_favorite / raw_total
```

Usar a normalizada como leitura principal, porque reduz o efeito da margem do mercado.

---

## 6. Proposta inicial de categorias

A classificacao final nao deve assumir cortes fixos sem validar a distribuicao por liga e temporada.

Mesmo assim, para iniciar a auditoria, usar quatro metodos candidatos.

---

### 6.1 Metodo A - faixas fixas por odd

Proposta inicial apenas para teste:

| Categoria | Favorite odd |
|---|---:|
| SUPER_FAVORITO | <= 1.40 |
| FAVORITO_FORTE | > 1.40 e <= 1.70 |
| FAVORITO_MEDIO | > 1.70 e <= 2.00 |
| SEM_FAVORITO_CLARO | > 2.00 ou empate tecnico home/away |

Observacao:

```text
Esses cortes devem ser rejeitados se concentrarem N demais em uma categoria ou deixarem categorias sem amostra.
```

---

### 6.2 Metodo B - quantis por liga/temporada

Calcular quantis da `favorite_odd` por liga e temporada:

```text
Q25
Q50
Q75
```

Classificacao:

| Categoria | Regra |
|---|---|
| SUPER_FAVORITO | favorite_odd <= Q25 |
| FAVORITO_FORTE | Q25 < favorite_odd <= Q50 |
| FAVORITO_MEDIO | Q50 < favorite_odd <= Q75 |
| FAVORITO_FRACO | favorite_odd > Q75 |

Vantagem:

```text
Respeita a distribuicao de cada liga/temporada.
```

Risco:

```text
Pode chamar de super favorito um time que nao seria super favorito em termos absolutos, caso a liga seja muito equilibrada.
```

---

### 6.3 Metodo C - implied probability normalizada

Proposta inicial:

| Categoria | favorite_implied_norm |
|---|---:|
| SUPER_FAVORITO | >= 0.62 |
| FAVORITO_FORTE | >= 0.54 e < 0.62 |
| FAVORITO_MEDIO | >= 0.47 e < 0.54 |
| SEM_FAVORITO_CLARO | < 0.47 |

Vantagem:

```text
Mais comparavel entre ligas, porque trabalha em probabilidade.
```

---

### 6.4 Metodo D - odds gap

Proposta inicial:

| Categoria | odds_gap |
|---|---:|
| SUPER_FAVORITO | >= 3.00 |
| FAVORITO_FORTE | >= 1.50 e < 3.00 |
| FAVORITO_MEDIO | >= 0.70 e < 1.50 |
| SEM_FAVORITO_CLARO | < 0.70 |

Vantagem:

```text
Mede separacao entre favorito e underdog.
```

Risco:

```text
Odds muito altas podem inflar gap sem significar vantagem real proporcional.
```

---

## 7. Metodo recomendado para classificacao oficial V1

Usar classificacao hibrida:

```text
1. Calcular distribuicao por liga/temporada.
2. Comparar odd fixa, quantis, implied probability e odds_gap.
3. Usar implied probability normalizada como eixo principal.
4. Usar quantis como sanity check de N.
5. Usar odds_gap como coluna auxiliar, nao como classificacao principal.
```

Regra sugerida V1:

```text
favorite_strength_category = categoria por implied probability normalizada
favorite_strength_quantile = categoria por quantil da liga/temporada
favorite_strength_gap = categoria por odds_gap
```

A categoria operacional principal deve ser `favorite_strength_category`.

---

## 8. Significado de cada faixa

Para cada liga e temporada, calcular por categoria:

```text
N de jogos
odd media do favorito
odd mediana do favorito
implied probability media
implied probability mediana
taxa de vitoria do favorito
taxa de empate
taxa de derrota
gols marcados pelo favorito
gols sofridos pelo favorito
saldo medio do favorito
frequencia de favorito vencendo por 1 aos 60/65/70/75
frequencia de favorito perdendo por 1 aos 60/65/70/75
frequencia de favorito empatando aos 60/65/70/75
frequencia de favorito pressionando
frequencia de underdog pressionando
```

Pressao deve ser calculada usando os thresholds ja existentes por liga/temporada/cutoff/janela:

```text
pressure_high_2of3 = pelo menos 2 de 3 acima de p75
- dangerous_attacks
- shots_total
- key_passes
```

---

## 9. Cruzamento com estrategias existentes

Estruturar por:

```text
strategy_name
league
season
cutoff
window
target
favorite_strength_category
```

Calcular:

```text
N
wins
losses
strike_rate
baseline_rate
diff_vs_baseline
p_value
odds_ratio
ROI estimado quando houver output do Agente 06
EV estimado quando houver output do Agente 06
profit estimado quando houver output do Agente 06
max_drawdown quando houver output de drawdown
loss_streak quando houver output de drawdown
```

Nao misturar ligas.
Nao misturar temporadas.
Nao consolidar categorias sem mostrar a abertura.

---

## 10. Baseline

O baseline deve ser calculado dentro do mesmo contexto:

```text
mesma liga
mesma temporada
mesmo cutoff
mesmo target
mesma categoria de favorito
```

Exemplo:

```text
favorite_drawing_pressure_high_2of3
La Liga 2025/26
cutoff 60
target goal_60_90
SUPER_FAVORITO
```

Comparar contra:

```text
todos os jogos/linhas elegiveis do mesmo cutoff + target + SUPER_FAVORITO
```

Nao comparar contra baseline geral da liga se a pergunta e sobre categoria do favorito.

---

## 11. Regras de amostra minima

Classificacao estatistica por segmento:

| Condicao | Status |
|---|---|
| N < 10 | AMOSTRA_INSUFICIENTE |
| 10 <= N < 20 | OBSERVACAO |
| N >= 20 e diff positivo | ELEGIVEL |
| N >= 20 e diff positivo e p <= 0.10 | FORTE_ESTATISTICO |

Para decisao operacional, preferir:

```text
N >= 20 por categoria
N >= 40 idealmente para ranking financeiro
```

---

## 12. Classificacao final por estrategia

Categorias finais:

```text
FUNCIONA_QUALQUER_FAVORITO
FUNCIONA_SUPER_FAVORITO
FUNCIONA_FAVORITO_FORTE
FUNCIONA_FAVORITO_MEDIO
NAO_DEPENDE_DA_FORCA_DO_FAVORITO
AMOSTRA_INSUFICIENTE
```

Regras propostas:

### 12.1 FUNCIONA_QUALQUER_FAVORITO

```text
A estrategia tem diff positivo em pelo menos 3 categorias de favorito,
sem queda operacional grave em favorito fraco/sem favorito claro,
e sem concentrar todo o lucro em uma categoria unica.
```

### 12.2 FUNCIONA_SUPER_FAVORITO

```text
SUPER_FAVORITO e a unica categoria com N suficiente e resultado positivo consistente,
ou e claramente a melhor categoria em strike/ROI/EV/drawdown.
```

### 12.3 FUNCIONA_FAVORITO_FORTE

```text
FAVORITO_FORTE tem melhor equilibrio entre N, strike, lucro, ROI/EV e drawdown.
```

### 12.4 FUNCIONA_FAVORITO_MEDIO

```text
FAVORITO_MEDIO performa melhor que super/forte, ou mantem lucro com melhor odd operacional.
```

### 12.5 NAO_DEPENDE_DA_FORCA_DO_FAVORITO

```text
A estrategia nao usa favorito na definicao,
ou os resultados por categoria nao alteram a decisao operacional.
```

### 12.6 AMOSTRA_INSUFICIENTE

```text
Nenhuma categoria atinge N minimo confiavel,
ou a abertura por categoria fragmenta demais a amostra.
```

---

## 13. Estrategias prioritarias para cruzamento

Prioridade 1 - dependem diretamente de favorito:

```text
favorite_winning_by_1_opp_cold_2of3
favorite_losing_pressure_high_2of3
favorite_drawing_pressure_high_2of3
underdog_winning_favorite_pressing_2of3
```

Prioridade 2 - podem ser afetadas indiretamente pela forca do favorito:

```text
team_winning_by_1_opp_cold_2of3
home_winning_by_1_visitor_pressing
away_winning_by_1_home_pressing
opponent_no_big_chances
opponent_no_recent_key_passes
```

Prioridade 3 - nao dependem de favorito, mas devem ser usadas como controle:

```text
both_teams_cold_2of3
dangerous_attacks_accelerating
shots_on_target_recent
big_chances_recent
key_passes_recent_high
corners_recent_high
```

---

## 14. Outputs esperados

### 14.1 CSV principal

```text
data/processed/reports/classificacao_forca_favorito_v1.csv
```

Uma linha por:

```text
league + season + strategy_name + cutoff + window + target + favorite_strength_category
```

### 14.2 JSON principal

```text
data/processed/reports/classificacao_forca_favorito_v1.json
```

Estrutura sugerida:

```json
{
  "metadata": {
    "version": "CLASSIFICACAO_DE_FORCA_DO_FAVORITO_V1",
    "generated_at": null,
    "method": "implied_probability_norm_primary_quantile_sanity_check",
    "financial_mode": "ESTIMATIVA_OPERACIONAL_COM_ODDS_MEDIAS"
  },
  "league_season_distributions": [],
  "strategy_results": [],
  "final_classifications": []
}
```

---

## 15. Cuidados metodologicos

Obrigatorio:

```text
Nao criar modelo.
Nao criar robo.
Nao criar producao.
Nao usar odds live.
Nao usar odds pos-jogo.
Nao misturar ligas sem reportar separadamente.
Nao misturar temporadas sem reportar separadamente.
Nao promover estrategia por taxa de acerto isolada.
Nao promover segmento com N baixo apenas por ROI alto.
```

Toda leitura financeira deve manter a ressalva:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```

---

## 16. Resultado operacional esperado

Ao final da execucao, o projeto deve responder:

```text
Esta estrategia depende de qualquer favorito ou de um tipo especifico de favorito?
```

E tambem:

```text
Qual faixa de odd representa melhor o favorito ideal para esta estrategia?
```

Formato esperado da resposta final por estrategia:

| Estrategia | Liga | Temporada | Melhor categoria | Decisao | Observacao |
|---|---|---|---|---|---|
| favorite_drawing_pressure_high_2of3 | la_liga | 2025/26 | FAVORITO_FORTE | FUNCIONA_FAVORITO_FORTE | Exemplo; preencher apos execucao |

---

## 17. Parecer do Agente 05

Esta frente e necessaria e deve ser tratada como camada de segmentacao obrigatoria para estrategias com favorito.

Ela nao deve substituir o discovery.

Ela deve entrar entre o discovery/drawdown e a validacao financeira final.

Parecer:

```text
APROVADO COMO FRENTE METODOLOGICA.
EXECUTAR POR LIGA/TEMPORADA ASSIM QUE AS BASES DE DISCOVERY/ENTRIES ESTIVEREM DISPONIVEIS.
```
