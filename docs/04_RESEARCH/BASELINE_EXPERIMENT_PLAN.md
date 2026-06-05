# BASELINE EXPERIMENT PLAN

## Status

Plano metodologico formal.

Nao implementado.

Nao contem codigo.

Nao contem scripts.

Nao executa treinamento.

Nao executa baseline.

Nao altera datasets.

---

## Objetivo

Definir o primeiro experimento baseline do LateGoalResearch antes de qualquer implementacao.

Este plano deve ser revisado pelo PM e, se necessario, pelo CTO antes de qualquer tarefa ao Codex.

---

## Arquitetura Aprovada

Tipo do primeiro baseline:

- Pre-Match Only.

Hipoteses permitidas:

- H3 - Forca Ofensiva.
- H4 - Fragilidade Defensiva.

Hipoteses bloqueadas ou fora do escopo:

- H1 - Bloqueada por leakage.
- H2 - Bloqueada por leakage.
- H5 - Nao validada.
- H6 - Validada inicialmente, mas in-game e fora do baseline 1.
- H7 - Nao validada como hipotese independente.
- H8 - Bloqueada por ausencia de graph/momentum.
- H9 - Validada inicialmente, mas in-game e fora do baseline 1.

Target:

- `target_late_goal_75`.

---

## 1. Unidade do Experimento

Unidade final do baseline:

- 1 linha por partida.

Fonte do target:

- `LateGoalResearch/data/processed/datasets/late_goal_dataset_v1.csv`.

Fonte das features:

- `LateGoalResearch/data/processed/features/historical_prematch_features_v1.csv`.

Target:

- `target_late_goal_75`.

Interpretação:

- O experimento tenta estimar a probabilidade de uma partida ter pelo menos um gol apos 75:00 usando apenas informacoes disponiveis antes do kickoff.

Nao usar:

- `target_directional_late_goal_75` como target do baseline 1.
- targets in-game.
- targets derivados como features.

---

## 2. Conversao Team-Level para Match-Level

O feature set historico pre-jogo possui grain:

- 1 linha por time por partida.

O baseline precisa de grain:

- 1 linha por partida.

Regra de conversao:

1. Para cada `match_id`, identificar a linha com `is_home = 1`.
2. Prefixar as features dessa linha com `home_`.
3. Identificar a linha com `is_home = 0`.
4. Prefixar as features dessa linha com `away_`.
5. Consolidar ambas em uma unica linha por `match_id`.
6. Anexar `target_late_goal_75` a partir do Dataset V1.

Features base permitidas:

- `goals_for_avg_last_3`
- `goals_for_avg_last_10`
- `shots_on_target_for_avg_last_5`
- `shots_against_avg_last_5`
- `shots_on_target_against_avg_last_5`
- `big_chances_against_avg_last_5`

Colunas match-level permitidas apos conversao:

### Mandante

- `home_goals_for_avg_last_3`
- `home_goals_for_avg_last_10`
- `home_shots_on_target_for_avg_last_5`
- `home_shots_against_avg_last_5`
- `home_shots_on_target_against_avg_last_5`
- `home_big_chances_against_avg_last_5`

### Visitante

- `away_goals_for_avg_last_3`
- `away_goals_for_avg_last_10`
- `away_shots_on_target_for_avg_last_5`
- `away_shots_against_avg_last_5`
- `away_shots_on_target_against_avg_last_5`
- `away_big_chances_against_avg_last_5`

### Derivacoes permitidas apenas se aprovadas no momento da implementacao

Derivacoes simples home-away podem ser permitidas como representacao estrutural, nao como novas hipoteses:

- `diff_goals_for_avg_last_3`
- `diff_goals_for_avg_last_10`
- `diff_shots_on_target_for_avg_last_5`
- `diff_shots_against_avg_last_5`
- `diff_shots_on_target_against_avg_last_5`
- `diff_big_chances_against_avg_last_5`

Formula:

- `diff_feature = home_feature - away_feature`.

Recomendacao Quant:

- Baseline 1A: usar somente home/away.
- Baseline 1B: opcional, usar home/away + diff, somente se PM/CTO aprovarem.

Nao permitir nesta fase:

- razoes complexas;
- interacoes multiplicativas;
- transformacoes nao documentadas;
- selecao automatica de features;
- criacao de novas features permanentes.

---

## 3. Estrategia de Split Temporal

Split aprovado:

- treino: 60%.
- validacao: 20%.
- teste: 20%.

Regra obrigatoria:

- ordenar por `match_date` em ordem crescente.

Com 380 partidas, a divisao esperada e aproximadamente:

- treino: 228 partidas.
- validacao: 76 partidas.
- teste: 76 partidas.

Regras:

1. Nenhuma partida do futuro pode aparecer no treino em relacao ao periodo de validacao/teste.
2. O split deve ser feito apos consolidar uma linha por partida.
3. O split nao deve ser aleatorio.
4. O split deve preservar a ordem temporal da temporada.
5. Em caso de partidas no mesmo dia, ordenar adicionalmente por horario e `match_id`.

Auditoria obrigatoria:

- reportar primeira e ultima data do treino;
- reportar primeira e ultima data da validacao;
- reportar primeira e ultima data do teste;
- reportar quantidade de positivos/negativos em cada split;
- reportar prevalencia do target em cada split.

---

## 4. Estrategia de Imputacao

O feature set historico possui linhas de inicio de temporada sem historico anterior.

Problema:

- as primeiras partidas de cada time podem conter nulos por falta de jogos anteriores.

Regra principal:

- qualquer imputacao deve ser ajustada somente no conjunto de treino.

Permitido:

- imputacao por mediana do treino para cada feature;
- aplicar a mesma mediana do treino em validacao e teste;
- registrar quantidade de nulos imputados por split e por feature.

Proibido:

- calcular mediana usando dataset inteiro;
- calcular mediana usando validacao/teste;
- imputar usando informacao posterior no tempo;
- excluir linhas de validacao/teste sem registrar impacto.

Analise de sensibilidade recomendada:

- resultado principal: com imputacao por mediana do treino;
- resultado secundario: excluindo partidas sem historico minimo, se PM/Quant aprovarem.

Historico minimo sugerido para analise secundaria:

- ambos os times com `history_matches_available >= 3`.

Esta analise secundaria nao substitui o resultado principal.

---

## 5. Estrategia de Validacao

Validacao primaria:

- avaliar o modelo escolhido no conjunto de validacao para calibrar decisao operacional minima;
- avaliar uma unica vez no conjunto de teste para estimativa final fora da amostra temporal.

O primeiro baseline deve ser tratado como experimento exploratorio controlado, nao como modelo pronto.

Comparacoes obrigatorias:

1. Baseline constante:
   - probabilidade igual a prevalencia do target no treino.
2. Baseline treinado:
   - modelo simples aprovado posteriormente.

A implementacao futura deve reportar resultados separados para:

- treino;
- validacao;
- teste.

Sinais de alerta:

- performance alta em treino e baixa em validacao/teste;
- diferenca grande entre validacao e teste;
- PR-AUC abaixo ou igual a prevalencia do teste;
- dependencia excessiva de uma unica feature.

---

## 6. Metricas Principais

Metricas principais aprovadas:

- ROC-AUC.
- PR-AUC.

### ROC-AUC

Uso:

- medir capacidade de ranking entre partidas com e sem gol tardio.

Criterio minimo:

- ROC-AUC no teste maior que 0.55.

Interpretacao:

- 0.50: aleatorio.
- 0.55: sinal minimo aceitavel.
- 0.58: sinal promissor.
- 0.60 ou mais: sinal forte para esta fase.

### PR-AUC

Uso:

- medir capacidade de concentrar positivos nos rankings superiores.

Baseline aleatorio:

- prevalencia positiva do conjunto avaliado.

Criterio minimo aprovado:

- `PR-AUC Test > prevalence_test + 0.03`.

Exemplo:

- se `prevalence_test = 0.50`, entao PR-AUC minimo esperado = 0.53.

Regra:

- usar a prevalencia do conjunto de teste, nao a prevalencia global.

---

## 7. Metricas Secundarias

Metricas secundarias recomendadas:

- Brier Score.
- Log Loss.
- Lift@Top20%.
- Calibration by bins.

### Brier Score

Uso:

- avaliar qualidade probabilistica.

Menor e melhor.

### Log Loss

Uso:

- penalizar previsoes muito confiantes e erradas.

Menor e melhor.

### Lift@Top20%

Uso:

- avaliar se as partidas mais bem ranqueadas concentram mais gols tardios que a media.

Formula conceitual:

- `taxa_positiva_top20 / taxa_positiva_geral`.

Interpretacao:

- maior que 1.0 indica concentracao de positivos acima da media.

### Calibration by bins

Uso:

- comparar probabilidade prevista media contra taxa observada em grupos de probabilidade.

Objetivo:

- identificar se o baseline produz probabilidades calibradas ou apenas ranking.

---

## 8. Criterios Minimos de Aprovacao

O baseline so deve ser considerado aprovado se atender aos criterios minimos no conjunto de teste:

1. ROC-AUC Test > 0.55.
2. PR-AUC Test > prevalence_test + 0.03.
3. Resultado de validacao e teste nao devem divergir excessivamente.
4. Nenhuma feature proibida pode ser usada.
5. Split temporal deve estar documentado.
6. Imputacao deve ser ajustada somente no treino.

Criterio de estabilidade recomendado:

- `abs(ROC-AUC Validation - ROC-AUC Test) <= 0.07`.

Se o baseline falhar:

- nao avancar para backtesting;
- nao avancar para producao;
- revisar features, target ou amostra;
- registrar falha no relatorio.

---

## 9. Riscos Metodologicos

### Risco 1 - Amostra pequena de teste

Com 380 partidas, o teste deve conter aproximadamente 76 partidas.

Impacto:

- metricas podem ter alta variancia.

Mitigacao:

- reportar resultados com cautela;
- comparar validacao e teste;
- se permitido futuramente, usar intervalo de confianca por bootstrap.

### Risco 2 - Early-season rows

Primeiras partidas possuem pouco ou nenhum historico.

Impacto:

- nulos e imputacoes podem carregar sinal temporal artificial.

Mitigacao:

- documentar nulos por split;
- imputar apenas com estatisticas do treino;
- executar analise secundaria com historico minimo, se aprovada.

### Risco 3 - Dependencia entre partidas do mesmo time

Times aparecem repetidamente no dataset.

Impacto:

- risco de capturar padroes especificos de clubes, nao sinal geral.

Mitigacao:

- declarar limitacao;
- nao interpretar o primeiro baseline como prova de generalizacao multi-temporada.

### Risco 4 - Conversao incorreta home/away

O feature set original e team-level.

Impacto:

- inversao de mandante/visitante ou duplicacao de linhas pode invalidar o experimento.

Mitigacao:

- validar exatamente 1 linha por partida apos conversao;
- validar que cada partida possui 1 linha home e 1 linha away antes do pivot;
- auditar manualmente amostra de partidas.

### Risco 5 - Correlacao entre features

Features ofensivas e defensivas podem ser correlacionadas.

Impacto:

- interpretacao individual de coeficientes pode ser instavel.

Mitigacao:

- nao interpretar coeficientes como causalidade;
- reportar matriz de correlacao apenas como diagnostico, se aprovado.

### Risco 6 - Uso indevido de feature in-game

Features H6/H9 sao aprovadas para outro bloco, mas proibidas no baseline pre-match.

Impacto:

- contaminacao do experimento pre-jogo.

Mitigacao:

- whitelist explicita de features permitidas.

---

## 10. Controles Anti-Leakage

Controles obrigatorios:

1. Usar apenas features do `historical_prematch_features_v1` aprovadas neste plano.
2. Confirmar que features historicas foram calculadas com `shift(1)` antes de rolling/expanding.
3. Nao usar xG/xGA da propria partida.
4. Nao usar forecast.
5. Nao usar estatisticas full-match da propria partida.
6. Nao usar features in-game.
7. Nao usar target-derived columns como features.
8. Nao usar placar final ou total de gols como features.
9. Ajustar imputacao apenas no treino.
10. Fazer split temporal por `match_date`.
11. Validar que o target nao entra no conjunto de features.

Features explicitamente proibidas no Baseline 1:

- `score_diff_home_until_cutoff`
- `score_state_group`
- `cards_until_cutoff`
- `substitutions_until_cutoff`
- `xG`
- `xGA`
- `forecast`
- qualquer feature H1/H2/H8
- `has_late_goal`
- `target_late_goal_75`
- `late_goal_count_75`
- `home_late_goal_count_75`
- `away_late_goal_count_75`
- `first_late_goal_minute_75`
- `home_goals`
- `away_goals`
- `total_goals`

---

## 11. Escopo do Baseline 1

### Baseline 1A - Obrigatorio

Tipo:

- Pre-Match Only.

Features:

- home/away das 6 features permitidas.

Total esperado:

- 12 colunas preditivas antes de imputacao.

Objetivo:

- testar se H3/H4 possuem sinal preditivo minimo no target match-level.

### Baseline 1B - Opcional, depende de aprovacao

Tipo:

- Pre-Match Only com diferencas home-away.

Features:

- 12 colunas home/away;
- 6 colunas `diff_`.

Total esperado:

- 18 colunas preditivas.

Objetivo:

- testar se diferencas relativas entre equipes melhoram o ranking.

Condicao:

- so executar se PM/CTO aprovarem explicitamente.

---

## 12. Relatorio Esperado da Implementacao Futura

Quando a implementacao for autorizada, o relatorio do baseline deve conter:

1. data de execucao;
2. arquivos de entrada;
3. lista final de features usadas;
4. lista de features proibidas verificadas;
5. contagem de linhas antes/depois da conversao match-level;
6. contagem de nulos antes/depois da imputacao;
7. datas inicial/final de cada split;
8. prevalencia do target por split;
9. metricas de treino;
10. metricas de validacao;
11. metricas de teste;
12. comparacao contra baseline constante;
13. ROC-AUC;
14. PR-AUC;
15. Brier Score;
16. Log Loss;
17. Lift@Top20%;
18. calibracao por bins;
19. decisao final do baseline: aprovado, inconclusivo ou reprovado;
20. limitacoes.

---

## 13. Criterios de Aceite para Codex Futuro

Esta secao nao autoriza implementacao. Serve apenas para orientar tarefa futura.

Codex so deve ser acionado se PM/CTO aprovarem este plano.

Criterios de aceite futuros:

- nenhum arquivo de dados existente alterado;
- nenhum schema alterado;
- nenhum crawler/importer alterado;
- split temporal documentado;
- features proibidas ausentes do conjunto de treino;
- imputacao fitada somente no treino;
- metricas reportadas em train/validation/test;
- relatorio gerado em `docs/04_RESEARCH/BASELINE_PREMATCH_H3_H4_RESULTS.md` ou caminho aprovado pelo PM;
- codigo, se criado no futuro, deve ficar isolado e nao ser pipeline de producao.

---

## Decisao Quant

O plano do primeiro baseline esta definido como:

- Pre-Match Only.
- H3 + H4.
- Target: `target_late_goal_75`.
- Split temporal 60/20/20.
- Metricas principais: ROC-AUC e PR-AUC.
- Criterios minimos: ROC-AUC Test > 0.55 e PR-AUC Test > prevalence_test + 0.03.

Status:

- PRONTO PARA REVISAO DO PM.
- IMPLEMENTACAO AINDA BLOQUEADA.
