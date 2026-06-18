# RENTABILIDADE_DAS_ESTRATEGIAS_POR_TIME_RESULTADOS_V1

Agente responsavel: `05 - Data Science / Quant Research`

Status: `DESENHO METODOLOGICO APROVADO - EXECUCAO DEPENDE DAS TOP 20 E DOS OUTPUTS FINANCEIROS`

Data: 2026-06-18

---

## 1. Objetivo

Descobrir quais times contribuem positiva ou negativamente para o desempenho das Top 20 estrategias do projeto.

Pergunta central:

```text
Esta estrategia e robusta em varios times ou depende excessivamente de poucos times?
```

Hipotese:

```text
Algumas estrategias funcionam melhor com determinados times ou perfis de equipe.
```

---

## 2. Posicao correta no fluxo do projeto

Esta frente deve acontecer depois de:

```text
1. discovery bruto;
2. auditoria de drawdown;
3. validacao financeira inicial pelo Agente 06;
4. definicao das Top 20 estrategias candidatas.
```

Motivo:

```text
Nao faz sentido auditar rentabilidade por time em estrategias que ainda nao passaram pelo filtro financeiro principal.
```

Fluxo recomendado:

```text
Discovery
-> Drawdown Audit
-> Agente 06: lucro / ROI / EV / drawdown
-> Top 20 estrategias
-> RENTABILIDADE_DAS_ESTRATEGIAS_POR_TIME_V1
-> Decisao de robustez operacional
```

---

## 3. Escopo

Executar somente para as Top 20 estrategias do projeto.

Nunca misturar:

```text
estrategia
liga
temporada
target
cutoff
janela
lado operacional
```

Cada combinacao deve ser tratada como uma estrategia financeira distinta.

---

## 4. Perguntas de pesquisa

1. Quais times geram mais lucro?
2. Quais times destroem a estrategia?
3. Existem times sistematicamente Over?
4. Existem times sistematicamente Under?
5. A estrategia depende excessivamente de poucos times?
6. Se removermos determinado time, a estrategia continua lucrativa?

---

## 5. Entradas necessarias

A fonte pode continuar sendo JSON bruto SportMonks + arquivos processados ja gerados pelo projeto.

Campos minimos por entrada/trade:

```text
strategy_name
liga
temporada
fixture_id
fixture_name
home_team
away_team
team_name
opponent_name
team_side
cutoff
window
target
resultado_target
win_loss
stake
profit_estimated
roi_estimated
ev_estimated
favorite_side
favorite_team
underdog_team
team_score_cutoff
opponent_score_cutoff
score_diff
team_pressing_flag
opponent_pressing_flag
```

Quando algum campo nao existir, o script deve derivar a partir dos JSONs ou marcar como `NAO_DISPONIVEL`.

---

## 6. Quebras obrigatorias

Analisar rentabilidade por:

```text
time mandante
time visitante
favorito
azarao
time vencendo por 1
time perdendo por 1
time pressionando
adversario pressionando
```

Cada quebra deve gerar uma visao separada.

Nao misturar os papeis.

Exemplo:

```text
Arsenal como mandante != Arsenal como visitante
Arsenal como favorito != Arsenal como azarao
Arsenal vencendo por 1 != Arsenal perdendo por 1
```

---

## 7. Metricas por time

Calcular por time e por quebra:

```text
N
wins
losses
taxa_acerto
lucro_estimado
roi_estimado
ev_estimado
sequencia_maxima_perdas
lucro_com_time
lucro_sem_time
roi_sem_time
delta_lucro_sem_time
percentual_lucro_total_concentrado_no_time
```

Formula base:

```text
lucro_sem_time = lucro_total_estrategia - lucro_com_time
```

```text
delta_lucro_sem_time = lucro_sem_time - lucro_total_estrategia
```

---

## 8. Criterios minimos de amostra

Classificar N por time:

| N | Classificacao |
|---:|---|
| < 5 | IGNORAR |
| 5 a 9 | MICRO_AMOSTRA |
| 10 a 19 | OBSERVACIONAL |
| >= 20 | CONFIAVEL |

Regra:

```text
Nao tomar decisao operacional forte com MICRO_AMOSTRA.
```

---

## 9. Identificacao de dependencia de time

Para cada estrategia, calcular:

```text
lucro_total_estrategia
lucro_com_time
lucro_sem_time
percentual_lucro_total_concentrado_no_time
```

Pergunta obrigatoria:

```text
Se removermos este time, a estrategia continua lucrativa?
```

Sinal de dependencia:

```text
A estrategia vira negativa sem 1 ou 2 times especificos.
```

Ou:

```text
Mais de 40% do lucro total vem de um unico time.
```

Ou:

```text
Mais de 60% do lucro total vem dos 3 principais times.
```

Esses cortes sao iniciais e devem ser marcados como heuristica operacional.

---

## 10. Classificacoes finais

Criar as seguintes classificacoes:

```text
TIME_FAVORAVEL
TIME_DESFAVORAVEL
DEPENDENCIA_DE_TIME
ROBUSTA_MULTI_TIME
AMOSTRA_INSUFICIENTE
```

### 10.1 TIME_FAVORAVEL

```text
Time tem N minimo observacional e contribui positivamente para lucro/ROI da estrategia.
```

### 10.2 TIME_DESFAVORAVEL

```text
Time tem N minimo observacional e contribui negativamente para lucro/ROI da estrategia.
```

### 10.3 DEPENDENCIA_DE_TIME

```text
A estrategia perde a maior parte do lucro ou fica negativa quando um ou poucos times sao removidos.
```

### 10.4 ROBUSTA_MULTI_TIME

```text
A estrategia continua lucrativa mesmo removendo os principais times positivos.
```

### 10.5 AMOSTRA_INSUFICIENTE

```text
Nao ha N suficiente para conclusao por time.
```

---

## 11. Analise Over/Under por time

Para responder se existem times sistematicamente Over ou Under, calcular por time:

```text
total_trades_over
total_trades_under
wins_over
wins_under
roi_over
roi_under
profit_over
profit_under
```

Classificacao auxiliar:

```text
PERFIL_OVER
PERFIL_UNDER
PERFIL_NEUTRO
```

Cuidado:

```text
Perfil Over/Under deve ser calculado dentro da mesma liga e temporada.
Nao generalizar time entre ligas/temporadas sem mostrar a abertura.
```

---

## 12. Outputs esperados

### 12.1 Documento

```text
docs/04_RESEARCH/RENTABILIDADE_DAS_ESTRATEGIAS_POR_TIME_RESULTADOS_V1.md
```

### 12.2 CSV recomendado

```text
data/processed/reports/rentabilidade_das_estrategias_por_time_v1.csv
```

### 12.3 JSON recomendado

```text
data/processed/reports/rentabilidade_das_estrategias_por_time_v1.json
```

### 12.4 Script recomendado

```text
Crawler/Sportmonks/rentabilidade_das_estrategias_por_time_v1.py
```

---

## 13. Schema minimo do CSV

```text
strategy_name
liga
temporada
target
cutoff
janela
quebra
time
papel_do_time
N
wins
losses
taxa_acerto
lucro_estimado
roi_estimado
ev_estimado
sequencia_maxima_perdas
lucro_total_estrategia
lucro_com_time
lucro_sem_time
roi_sem_time
delta_lucro_sem_time
percentual_lucro_total_concentrado_no_time
classificacao_amostra
classificacao_time
```

---

## 14. Cuidados metodologicos

Proibido:

```text
criar modelos
alterar estrategia
criar producao
criar robos
sugerir trade real
misturar ligas
misturar temporadas
misturar targets
misturar cutoffs
misturar janelas
promover time com micro amostra
```

Toda leitura financeira deve ser marcada como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```

---

## 15. Resultado esperado

Ao final, o projeto deve responder:

```text
Esta estrategia e robusta ou depende excessivamente de poucos times?
```

E tambem:

```text
Quais times favorecem ou prejudicam a estrategia?
```

Formato executivo esperado:

| Estrategia | Liga | Temporada | Robustez | Times favoraveis | Times desfavoraveis | Parecer |
|---|---|---|---|---|---|---|
| exemplo | EPL | 2025/26 | ROBUSTA_MULTI_TIME | preencher apos execucao | preencher apos execucao | preencher apos execucao |

---

## 16. Parecer do Agente 05

A frente e aprovada como auditoria de robustez operacional por time.

Ela nao deve substituir ranking financeiro.

Ela deve ser usada para identificar:

```text
concentracao de lucro
concentracao de prejuizo
dependencia excessiva de poucos times
perfis Over/Under por equipe
```

Parecer:

```text
APROVADO COMO FRENTE POS-RANKING FINANCEIRO.
EXECUTAR APOS DEFINICAO DAS TOP 20 ESTRATEGIAS.
```
