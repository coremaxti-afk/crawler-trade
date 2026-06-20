# ROADMAP_EXPLORATORIO_PRE_RANKING_OPERACIONAL_FINAL_V1

## Status

`ROADMAP DE DESENVOLVIMENTO DEFINIDO — FASE EXPLORATORIA`

## Diretriz obrigatoria relacionada

Antes de executar qualquer uma das frentes abaixo, todos os agentes devem seguir:

```text
docs/00_AGENTS/GOVERNANCE_V2.md
```

Regra central: nenhum agente deve concordar com o usuario apenas para agradar. Se uma solicitacao pular etapas, misturar objetivos ou fragilizar a metodologia, o agente deve discordar primeiro, explicar o risco tecnico e propor o caminho correto.

## Fase atual

A fase atual do projeto e:

```text
ANALISE EXPLORATORIA E DESCOBERTA DE PADROES
```

O objetivo agora nao e prever diretamente a proxima temporada.

O objetivo e descobrir padroes fortes no passado, organizar hipoteses e so depois transformar os melhores achados em validacao preditiva/operacional.

Fluxo metodologico:

```text
1. Analise exploratoria
2. Descoberta de padroes
3. Formulacao de hipoteses
4. Validacao preditiva
5. Validacao operacional
6. Ranking/decisao final
```

## Motivo do roadmap

Antes de gerar o `RANKING_OPERACIONAL_FINAL_V1`, foram identificados estudos exploratorios obrigatorios para evitar:

- misturar perguntas metodologicamente diferentes;
- contar variacoes da mesma entrada como estrategias independentes;
- deixar Over ruim contaminar Under bom;
- deixar uma estrategia Under ruim contaminar outra estrategia Under boa;
- escolher cutoff apenas por lucro passado sem medir overlap, DD e robustez;
- transformar achado exploratorio em decisao operacional antes da hora.

## Ordem oficial de desenvolvimento

Executar nesta ordem:

```text
1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
2. ANALISE_REGIME_POR_FASE_V1
3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1
```

Justificativa da ordem:

```text
Primeiro limpar/organizar familias e variacoes.
Depois analisar tempo da temporada.
Depois analisar maturidade por rodada.
Depois contexto de favorito/equilibrio.
Depois padroes de times que causam prejuizo.
```

---

# 1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1

## Papel no roadmap

Camada tecnica de higiene e organizacao antes das demais pesquisas.

## Objetivo

Evitar que o ranking e as analises futuras contem varias variacoes da mesma oportunidade como se fossem estrategias independentes.

Exemplo do problema:

```text
both_teams_cold_2of3 no_goal_60_75
both_teams_cold_2of3 no_goal_60_80
both_teams_cold_2of3 no_goal_60_85
both_teams_cold_2of3 no_goal_60_90
```

Essas linhas podem ser praticamente a mesma entrada com os mesmos jogos/times, mudando apenas:

- tempo de entrada;
- tempo de saida;
- cashout;
- hold final;
- cutoff/window/target.

## Perguntas que deve responder

```text
1. Quais linhas pertencem a mesma familia operacional?
2. Quantas variacoes existem dentro de cada familia?
3. Qual e o overlap de fixtures/times entre variacoes?
4. Qual variacao mais lucrou dentro da familia?
5. Qual variacao teve melhor ROI?
6. Qual variacao teve menor DD?
7. Qual variacao parece mais equilibrada?
8. As proximas frentes podem ser enviesadas por duplicidade dessa familia?
```

## Regra de familia

Criar campos:

```text
strategy_family
market_direction
variant_id
family_rank
is_primary_variant_candidate
overlap_with_primary_pct
overlap_fixture_pct
overlap_team_pct
```

Sugestao de familia:

```text
strategy_family = strategy_name + market_direction
```

Onde:

```text
market_direction = no_goal | goal
```

## Analise de overlap

Comparar variacoes dentro da mesma familia por:

```text
fixture_id
team_id ou team_side quando existir
season_id
league_id
```

Se:

```text
overlap_fixture_pct >= 70%
```

tratar como variacao da mesma oportunidade, nao como estrategia independente.

## Analise de melhor cutoff/target/window

O agrupamento deve mostrar, mas nao decidir definitivamente:

```text
melhor_cutoff_por_lucro
melhor_target_por_lucro
melhor_window_por_lucro
profit_melhor_variacao

melhor_cutoff_por_ROI
melhor_target_por_ROI
melhor_window_por_ROI
ROI_melhor_variacao

melhor_cutoff_por_menor_DD
melhor_target_por_menor_DD
melhor_window_por_menor_DD
DD_melhor_variacao

melhor_cutoff_equilibrado
melhor_target_equilibrado
melhor_window_equilibrado
score_equilibrado
primary_variant_candidate_reason
```

## Regra contra viés

O agrupamento por familia **nao pode excluir variacoes das proximas analises**.

Ele apenas:

- identifica familias;
- mede overlap;
- aponta candidatas principais;
- alerta risco de duplicidade;
- mostra cutoffs/targets/windows mais promissores.

As frentes seguintes devem manter dois niveis:

```text
1. analise por familia agregada
2. analise por variacao/cutoff/window
```

A escolha final da variacao principal so deve acontecer depois de cruzar:

```text
lucro
ROI
drawdown
fase da temporada
maturidade por rodada
forca/equilibrio do favorito
padroes de prejuizo por time
robustez por time
```

## Saidas esperadas

```text
agrupamento_por_familia_e_variacoes_v1_serie_a_2025_tempos_expandidos.csv
agrupamento_por_familia_e_variacoes_v1_serie_a_2025_tempos_expandidos.json
AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

---

# 2. ANALISE_REGIME_POR_FASE_V1

## Papel no roadmap

Camada de estudo do regime da temporada.

## Objetivo

Medir a lucratividade das estrategias por blocos da temporada, sem misturar com a pergunta de quando comecar a operar.

## Perguntas que deve responder

```text
1. Quais fases da temporada foram melhores para under/no_goal/lay_over?
2. Quais fases foram menos ruins ou possivelmente boas para over/goal/back_over?
3. A temporada mudou de regime?
4. Quais familias funcionaram em varias fases?
5. Quais familias foram dependentes de uma fase especifica?
6. Over melhora em alguma fase especifica, como fase 3 ou 6?
7. No Goal e forte em todas as fases ou so em algumas?
```

## Granularidades obrigatorias

Rodar o mesmo estudo com dois modelos:

```text
phase_count = 6
phase_count = 8
```

Interpretacao:

- `6 fases`: leitura macro da temporada.
- `8 fases`: leitura mais sensivel para detectar viradas menores de regime.

## Regra para evitar confusao

Toda linha de output deve conter:

```text
phase_count
phase_number
phase_start_round
phase_end_round
```

Assim, `fase 3 de 6` nunca sera confundida com `fase 3 de 8`.

## Niveis obrigatorios

Rodar por:

```text
1. direcao de mercado: goal/back_over vs no_goal/lay_over
2. familia de estrategia
3. variacao/cutoff/window
```

## Campos minimos esperados

Por estrategia/familia/variacao e por fase:

```text
strategy_family
strategy_name
target
cutoff
window
market_type
settlement
phase_count
phase_number
phase_start_round
phase_end_round
N_fase
profit_fase
ROI_fase
max_drawdown_fase
max_losing_streak_fase
```

Por familia/estrategia consolidada:

```text
profit_fase_1 ... profit_fase_N
ROI_fase_1 ... ROI_fase_N
N_fase_1 ... N_fase_N
qtd_fases_lucrativas
qtd_fases_negativas
melhor_fase
pior_fase
consistencia_por_fase
regime_dependente
```

## Saidas esperadas

```text
analise_regime_por_fase_v1_serie_a_2025_tempos_expandidos_phase6.csv
analise_regime_por_fase_v1_serie_a_2025_tempos_expandidos_phase8.csv
ANALISE_REGIME_POR_FASE_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

## Observacao inicial

Teste preliminar mostrou que as estrategias Over/Goal nao foram lucrativas no agregado em nenhuma das 6 fases, mas as fases 3 e 6 foram as menos negativas para Over.

Isso sugere que pode existir regime pontual para Over, mas ainda nao uma estrategia Over estavel.

---

# 3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1

## Papel no roadmap

Camada de maturidade temporal da competicao.

## Objetivo

Descobrir a partir de qual rodada os sinais da Serie A comecam a ficar confiaveis, sem misturar sinais bons com ruins.

## Pergunta principal

```text
Com dados ate a rodada X, os sinais que parecem bons continuam bons depois da rodada X?
```

## Rodadas obrigatorias

Testar:

```text
5, 6, 7, 8, 9, 10, 11, 12
```

## Niveis obrigatorios da analise

Este estudo deve ter 3 niveis principais:

```text
1. Liga geral
2. Direcao de mercado: Over/Goal/Back Over vs Under/No Goal/Lay Over
3. Familia/estrategia com todos os cutoffs/windows
```

A decisao exploratoria nao deve depender apenas da liga geral, porque:

- Over ruim pode contaminar Under bom;
- uma estrategia Under ruim pode contaminar uma estrategia Under boa;
- familias fortes podem ser escondidas pela media geral;
- sinais de cutoff/window podem variar dentro da mesma familia.

## Nivel 1 — Liga geral

Serve apenas como contexto macro:

```text
A Serie A comeca a estabilizar em qual rodada?
```

Campos:

```text
rodada_corte
qtd_estrategias_positivas_ate_rodada
qtd_estrategias_que_continuaram_positivas_depois
qtd_falsos_positivos
taxa_falso_positivo
profit_total_pos_rodada
ROI_total_pos_rodada
DD_total_pos_rodada
N_total_pos_rodada
```

## Nivel 2 — Direcao de mercado

Separar obrigatoriamente:

```text
goal / back_over
no_goal / lay_over
```

Perguntas:

```text
Under estabiliza antes de Over?
Over nunca estabiliza?
No Goal tem maturidade na rodada 7, 8, 9 ou 10?
```

## Nivel 3 — Familia/estrategia com todos os cutoffs

Para cada familia, juntar todas as variacoes e tambem manter detalhe por variacao.

Exemplo:

```text
both_teams_cold_2of3 / no_goal
- no_goal_60_75
- no_goal_60_80
- no_goal_60_85
- no_goal_60_90
- no_goal_65_90
- no_goal_70_90
```

Perguntas:

```text
Essa familia ja mostra sinal na rodada 7?
Qual cutoff fica melhor depois da rodada X?
O sinal e da familia inteira ou apenas de uma janela especifica?
```

Campos por familia/rodada:

```text
strategy_family
market_direction
rodada_corte
qtd_variacoes
N_ate_rodada
profit_ate_rodada
ROI_ate_rodada
N_pos_rodada
profit_pos_rodada
ROI_pos_rodada
DD_pos_rodada
max_losing_pos_rodada
qtd_variacoes_positivas_ate
qtd_variacoes_positivas_depois
taxa_continuidade
melhor_cutoff_pos_rodada
melhor_target_pos_rodada
melhor_window_pos_rodada
```

Campos por variacao/rodada:

```text
strategy_family
strategy_name
target
cutoff
window
market_type
settlement
rodada_corte
N_ate_rodada
profit_ate_rodada
ROI_ate_rodada
N_pos_rodada
profit_pos_rodada
ROI_pos_rodada
DD_pos_rodada
max_losing_pos_rodada
```

## Saidas esperadas

```text
maturidade_liga_por_rodada_v1_serie_a_2025_tempos_expandidos.csv
maturidade_direcao_mercado_por_rodada_v1_serie_a_2025_tempos_expandidos.csv
maturidade_familia_estrategia_por_rodada_v1_serie_a_2025_tempos_expandidos.csv
maturidade_variacao_cutoff_por_rodada_v1_serie_a_2025_tempos_expandidos.csv
ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

---

# 4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1

## Papel no roadmap

Camada de contexto pre-jogo/equilibrio entre times.

## Objetivo

Descobrir se as estrategias funcionam melhor em determinados contextos de forca do favorito ou equilibrio entre equipes.

Este estudo deve permanecer exploratorio.

## Perguntas que deve responder

```text
1. A estrategia funciona melhor quando os times sao parelhos?
2. Funciona melhor em favorito forte x zebra?
3. Funciona melhor com favorito medio?
4. Piora quando existe zebra muito fraca?
5. A estrategia nao depende da forca do favorito?
6. Estrategias como both_teams_cold_2of3 mudam quando o jogo e parelho vs favorito x zebra?
```

## Segmentos sugeridos

```text
favorito_forte_x_zebra
favorito_medio_x_azarao_competitivo
jogo_parelho
favorito_fraco
sem_favorito_claro
```

## Campos minimos esperados

```text
strategy_family
strategy_name
target
cutoff
window
market_type
settlement
favorite_strength_band
match_balance_type
N
profit
ROI
max_drawdown
max_losing_streak
win_rate
```

## Relacao com pesquisas anteriores de favoritos

Esta frente deve sincronizar com os estudos ja feitos de forca do favorito, preservando a visao exploratoria.

Ela nao deve transformar segmentacao de favorito em filtro operacional definitivo nesta etapa.

## Saidas esperadas

```text
analise_forca_favorito_por_estrategia_v1_serie_a_2025_tempos_expandidos.csv
ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

---

# 5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1

## Papel no roadmap

Camada de explicacao exploratoria da rentabilidade por time.

## Objetivo

Evoluir a rentabilidade por time para descobrir quais padroes aparecem nos times que dao prejuizo para cada estrategia/familia.

## Pergunta principal

```text
Quais caracteristicas aparecem nos times que deram prejuizo para uma estrategia?
```

## O que nao basta responder

Nao basta dizer:

```text
Time X deu prejuizo.
Time Y deu lucro.
```

O estudo precisa tentar responder:

```text
Por que esse time deu prejuizo?
Que padroes estavam presentes?
```

## Padroes candidatos

```text
time sofre gol tarde
time marca gol tarde
time quebra under no fim
time gera pressao falsa
time comeca frio mas acelera depois
time cede muitas chances apos 70
time e instavel fora de casa
time muda comportamento quando esta vencendo por 1
time muda comportamento quando esta perdendo por 1
```

## Campos minimos esperados

```text
team_id
team_name
strategy_family
strategy_name
target
cutoff
window
profit_by_team
ROI_by_team
N_by_team
late_goals_for
late_goals_against
goals_75_90_for
goals_75_90_against
SOT_after_70
big_chances_after_70
dangerous_attacks_after_70
team_risk_profile
padrao_prejuizo_detectado
```

## Relacao com Rentabilidade por Time V4

Esta frente deve usar a Rentabilidade por Time V4 como base, mas nao deve apenas repetir whitelist/blacklist.

Ela deve buscar explicacoes exploratorias para os times que mais afetam negativamente cada familia/estrategia.

## Saidas esperadas

```text
analise_padroes_prejuizo_por_time_v1_serie_a_2025_tempos_expandidos.csv
ANALISE_PADROES_PREJUIZO_POR_TIME_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

---

# Como os 5 estudos alimentam o Ranking Operacional Final

O `RANKING_OPERACIONAL_FINAL_V1` deve usar esses estudos assim:

## Do Agrupamento por Familia

Usar:

```text
strategy_family
variant_id
is_primary_variant_candidate
overlap_fixture_pct
overlap_team_pct
melhor_cutoff_por_lucro
melhor_cutoff_por_ROI
melhor_cutoff_equilibrado
risco_de_duplicidade
```

## Do Regime por Fase

Usar:

```text
consistencia_por_fase
qtd_fases_lucrativas
qtd_fases_negativas
melhor_fase
pior_fase
regime_dependente
```

## Da Maturidade por Rodada

Usar:

```text
rodada_corte_recomendada_liga
rodada_corte_recomendada_direcao
rodada_corte_recomendada_familia
profit_pos_rodada
ROI_pos_rodada
DD_pos_rodada
N_pos_rodada
taxa_continuidade
```

## Da Forca do Favorito

Usar:

```text
favorite_strength_band
match_balance_type
segmento_favorito_mais_lucrativo
segmento_favorito_mais_arriscado
```

## Dos Padroes de Prejuizo por Time

Usar:

```text
team_risk_profile
padrao_prejuizo_detectado
times_alerta
caracteristicas_alerta
```

## Regra de decisao futura

Nesta fase, esses estudos nao aprovam operacao automaticamente.

Eles servem para alimentar hipoteses e preparar o ranking operacional final.

O ranking final so deve decidir depois de cruzar:

```text
lucro
ROI
N
drawdown
maturidade por rodada
regime por fase
forca/equilibrio do favorito
padroes de prejuizo por time
robustez por time
sobreposicao por familia/variacao
```

## Decisao

Antes de criar o `RANKING_OPERACIONAL_FINAL_V1`, executar os 5 estudos na ordem oficial:

```text
1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
2. ANALISE_REGIME_POR_FASE_V1
3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1
```

Depois disso, gerar o ranking final consolidado.
