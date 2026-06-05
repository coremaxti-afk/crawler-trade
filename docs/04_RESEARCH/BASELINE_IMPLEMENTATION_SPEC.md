# BASELINE IMPLEMENTATION SPEC

Status: especificacao operacional.

Nao implementado.

Nao contem codigo.

Nao executa treinamento.

Nao executa baseline.

Nao altera datasets.

Nao altera PostgreSQL, schema, crawlers ou importers.

Documento base: `docs/04_RESEARCH/BASELINE_EXPERIMENT_PLAN.md`.

---

## 1. Objetivo

Definir, com nivel operacional suficiente, como uma futura implementacao do Baseline 1 deve ser estruturada e executada sem novas decisoes metodologicas.

O Baseline 1 e obrigatoriamente:

- tipo: pre-jogo apenas;
- target: `target_late_goal_75`;
- features: H3 + H4 aprovadas no plano;
- unidade final: 1 linha por partida;
- split: temporal cronologico 60/20/20;
- shuffle: proibido;
- features in-game: proibidas;
- xG/xGA da propria partida: proibidos;
- forecast baseado em informacao pos-kickoff: proibido.

Esta especificacao nao autoriza a implementacao. Ela apenas define o desenho da implementacao futura.

---

## 2. Escopo Funcional do Baseline 1

### Baseline 1A - Obrigatorio

Baseline 1A deve usar somente features historicas pre-jogo home/away derivadas do feature set team-level.

Features base permitidas:

- `goals_for_avg_last_3`
- `goals_for_avg_last_10`
- `shots_on_target_for_avg_last_5`
- `shots_against_avg_last_5`
- `shots_on_target_against_avg_last_5`
- `big_chances_against_avg_last_5`

Features finais esperadas apos conversao match-level:

- `home_goals_for_avg_last_3`
- `home_goals_for_avg_last_10`
- `home_shots_on_target_for_avg_last_5`
- `home_shots_against_avg_last_5`
- `home_shots_on_target_against_avg_last_5`
- `home_big_chances_against_avg_last_5`
- `away_goals_for_avg_last_3`
- `away_goals_for_avg_last_10`
- `away_shots_on_target_for_avg_last_5`
- `away_shots_against_avg_last_5`
- `away_shots_on_target_against_avg_last_5`
- `away_big_chances_against_avg_last_5`

Total esperado: 12 features preditivas.

### Baseline 1B - Opcional

Baseline 1B so pode ser implementado com aprovacao explicita do PM/CTO.

A extensao opcional adiciona diferencas home-away simples:

- `diff_goals_for_avg_last_3`
- `diff_goals_for_avg_last_10`
- `diff_shots_on_target_for_avg_last_5`
- `diff_shots_against_avg_last_5`
- `diff_shots_on_target_against_avg_last_5`
- `diff_big_chances_against_avg_last_5`

Formula obrigatoria:

```text
diff_feature = home_feature - away_feature
```

Total esperado no Baseline 1B: 18 features preditivas.

Baseline 1B nao substitui Baseline 1A. Se autorizado, deve ser reportado separadamente.

---

## 3. Baseline Nulo

Baseline nulo e a referencia probabilistica minima do experimento.

Definicao operacional:

- a probabilidade prevista para todas as partidas deve ser constante;
- essa probabilidade constante deve ser igual a prevalencia observada de `target_late_goal_75` no conjunto de treino;
- a prevalencia deve ser calculada somente depois do split temporal;
- a prevalencia de validacao ou teste nao pode ser usada para ajustar o baseline nulo.

O baseline nulo deve ser avaliado em treino, validacao e teste usando a mesma probabilidade constante aprendida no treino.

Metricas obrigatorias do baseline nulo:

- ROC-AUC do baseline nulo;
- PR-AUC do baseline nulo;
- Brier Score do baseline nulo;
- Log Loss do baseline nulo.

Nenhum valor fixo deve ser predefinido nesta especificacao. Todos os valores devem ser calculados durante a execucao futura.

---

## 4. Hierarquia Oficial das Metricas

A avaliacao do Baseline 1 deve seguir a hierarquia abaixo.

Metrica principal:

- ROC-AUC Test.

Criterio co-obrigatorio:

- PR-AUC Test.

Metricas secundarias:

- Brier Score;
- Log Loss;
- Lift@Top20%;
- Calibration by bins.

Regra de aprovacao:

- a aprovacao exige analise conjunta da metrica principal e do criterio co-obrigatorio;
- ROC-AUC Test deve indicar capacidade minima de ranking;
- PR-AUC Test deve superar a prevalencia do teste pelo criterio aprovado no plano;
- metricas secundarias nao aprovam o baseline sozinhas, mas podem bloquear, qualificar ou enfraquecer a interpretacao se indicarem ma calibracao ou ganho operacional insuficiente.

Criterios minimos mantidos do plano:

- `ROC-AUC Test > 0.55`;
- `PR-AUC Test > prevalence_test + 0.03`;
- estabilidade recomendada: `abs(ROC-AUC Validation - ROC-AUC Test) <= 0.07`, salvo justificativa documentada.

---

## 5. Estrutura de Diretorios Recomendada

Estrutura recomendada para implementacao futura:

```text
LateGoalResearch/
  Analytics/
    Baseline/
      __init__.py
      baseline_config.py
      build_baseline_dataset.py
      temporal_split.py
      imputation.py
      train_baseline_model.py
      evaluate_baseline.py
      run_baseline_1_prematch.py
  data/
    processed/
      baseline/
        baseline_1_prematch_dataset.csv
        baseline_1_prematch_train.csv
        baseline_1_prematch_validation.csv
        baseline_1_prematch_test.csv
      models/
        baseline_1_prematch_model.pkl
      reports/
        baseline_1_prematch_metrics.json
        baseline_1_prematch_validation_report.json
        baseline_1_prematch_feature_manifest.json
  docs/
    04_RESEARCH/
      BASELINE_PREMATCH_H3_H4_RESULTS.md
```

Observacao: caminhos exatos podem ser ajustados pelo CTO antes da implementacao, mas a separacao entre codigo, dados processados, artefatos de modelo, reports e documentacao deve ser preservada.

---

## 6. Estrutura dos Arquivos da Futura Implementacao

### `Analytics/Baseline/baseline_config.py`

Responsabilidade:

- centralizar constantes operacionais;
- definir caminhos de input/output;
- definir whitelist oficial de features permitidas;
- definir blacklist auxiliar de features proibidas;
- definir parametros de split temporal;
- definir nome do target;
- definir versao do experimento.

Nao deve:

- executar pipeline;
- ler ou escrever arquivos por efeito colateral;
- conter logica de treinamento.

Conteudo esperado:

- `BASELINE_NAME = "baseline_1_prematch_h3_h4"`
- `TARGET_COLUMN = "target_late_goal_75"`
- `TRAIN_RATIO = 0.60`
- `VALIDATION_RATIO = 0.20`
- `TEST_RATIO = 0.20`
- `SHUFFLE = False`
- `ALLOWED_TEAM_LEVEL_FEATURES`
- `ALLOWED_MATCH_LEVEL_FEATURES_1A`
- `OPTIONAL_DIFF_FEATURES_1B`
- `FORBIDDEN_FEATURE_PATTERNS`
- input paths;
- output paths.

### `Analytics/Baseline/build_baseline_dataset.py`

Responsabilidade:

- ler `historical_prematch_features_v1.csv`;
- ler `late_goal_dataset_v1.csv`;
- validar grain team-level de origem;
- converter team-level para match-level;
- anexar target match-level;
- aplicar whitelist oficial de features;
- rejeitar features nao aprovadas;
- registrar colunas removidas e motivo da remocao;
- gerar dataset baseline match-level antes do split.

Nao deve:

- imputar valores;
- treinar modelo;
- criar features fora da whitelist;
- alterar datasets originais;
- ler PostgreSQL.

### `Analytics/Baseline/temporal_split.py`

Responsabilidade:

- receber dataset match-level consolidado;
- ordenar por `match_date`, horario e `match_id`;
- criar split cronologico 60/20/20;
- validar ausencia de sobreposicao temporal;
- reportar periodo e prevalencia por split;
- reportar quantidade de linhas com `history_matches_available = 0` ou flags equivalentes por split, quando disponivel.

Nao deve:

- embaralhar linhas;
- balancear classes;
- fazer stratified split;
- acessar features proibidas;
- treinar modelo.

### `Analytics/Baseline/imputation.py`

Responsabilidade:

- ajustar imputador usando somente o conjunto de treino;
- calcular mediana do treino por feature permitida;
- aplicar medianas de treino em treino, validacao e teste;
- registrar nulos antes/depois por split e feature;
- exportar manifest de imputacao;
- preservar observacoes sem historico no experimento principal.

Nao deve:

- calcular mediana no dataset completo;
- calcular qualquer estatistica usando validacao ou teste;
- excluir linhas sem registrar impacto;
- criar features novas.

### `Analytics/Baseline/train_baseline_model.py`

Responsabilidade futura:

- treinar o modelo simples aprovado posteriormente;
- usar somente matriz de features permitidas ja imputada;
- persistir artefato de modelo se autorizado;
- registrar parametros do modelo.

Nao deve:

- escolher arquitetura por conta propria;
- rodar busca automatica extensa;
- usar dados de validacao/teste no fit;
- executar backtesting.

Observacao: esta especificacao nao define o modelo final. A escolha do modelo deve ser aprovada antes da implementacao. Candidatos naturais para baseline simples sao regressao logistica ou arvore rasa, mas nenhuma escolha esta autorizada por este documento.

### `Analytics/Baseline/evaluate_baseline.py`

Responsabilidade futura:

- avaliar baseline nulo;
- avaliar baseline treinado;
- comparar modelo contra baseline nulo;
- calcular metricas por split;
- gerar tabelas de calibracao;
- gerar Lift@Top20%;
- produzir JSON de metricas;
- produzir relatorio tecnico em Markdown.

Nao deve:

- re-treinar modelo;
- ajustar thresholds usando teste;
- alterar datasets;
- alterar banco.

### `Analytics/Baseline/run_baseline_1_prematch.py`

Responsabilidade:

- orquestrar a execucao na ordem aprovada;
- chamar construcao do dataset;
- chamar split temporal;
- chamar imputacao;
- calcular baseline nulo;
- chamar treinamento, somente quando modelo estiver aprovado;
- chamar avaliacao;
- salvar artefatos e reports;
- encerrar com resumo executivo no terminal.

Nao deve:

- conter logica metodologica escondida;
- sobrescrever artefatos sem controle de versao ou timestamp, salvo decisao aprovada;
- acessar PostgreSQL.

---

## 7. Inputs Necessarios

Inputs obrigatorios:

1. `LateGoalResearch/data/processed/features/historical_prematch_features_v1.csv`
2. `LateGoalResearch/data/processed/features/historical_prematch_features_v1_metadata.json`
3. `LateGoalResearch/data/processed/features/historical_prematch_features_v1_validation_report.json`
4. `LateGoalResearch/data/processed/datasets/late_goal_dataset_v1.csv`
5. `LateGoalResearch/data/processed/datasets/late_goal_dataset_v1_metadata.json`
6. `LateGoalResearch/data/processed/datasets/late_goal_dataset_v1_validation_report.json`

Campos obrigatorios no feature set:

- `match_id`
- `sofascore_event_id`
- `season`
- `match_date`
- `team_name`
- `opponent_team`
- `is_home`
- `history_matches_available`
- as 6 features H3/H4 permitidas.

Campos obrigatorios no Dataset V1:

- `match_id`
- `match_date`
- `home_team`
- `away_team`
- `target_late_goal_75`

Campos opcionais para auditoria:

- `league`
- `season`
- `sofascore_event_id`
- `has_late_goal`

---

## 8. Outputs Esperados

Outputs minimos da implementacao futura:

```text
data/processed/baseline/baseline_1_prematch_dataset.csv
data/processed/baseline/baseline_1_prematch_train.csv
data/processed/baseline/baseline_1_prematch_validation.csv
data/processed/baseline/baseline_1_prematch_test.csv
data/processed/reports/baseline_1_prematch_feature_manifest.json
data/processed/reports/baseline_1_prematch_imputation_report.json
data/processed/reports/baseline_1_prematch_split_report.json
data/processed/reports/baseline_1_prematch_metrics.json
data/processed/reports/baseline_1_prematch_validation_report.json
docs/04_RESEARCH/BASELINE_PREMATCH_H3_H4_RESULTS.md
```

Output de modelo, somente se treinamento for aprovado:

```text
data/processed/models/baseline_1_prematch_model.pkl
```

Todos os outputs devem ser derivados. Nenhum output deve substituir ou modificar os datasets originais.

---

## 9. Pipeline Operacional Completo

Ordem operacional completa:

1. Carregar configuracao.
2. Ler feature set historico pre-jogo.
3. Ler metadata e validation report do feature set.
4. Bloquear execucao se validation report do feature set nao estiver `APTO` ou `APTO COM RESSALVAS` aprovado.
5. Ler Dataset V1.
6. Ler metadata e validation report do Dataset V1.
7. Validar existencia do target `target_late_goal_75`.
8. Validar que o feature set esta no grain team-level.
9. Validar uma linha home e uma linha away por `match_id`.
10. Converter team-level para match-level.
11. Aplicar prefixos `home_` e `away_`.
12. Anexar target por `match_id`.
13. Aplicar whitelist oficial de features do Baseline 1A.
14. Executar scanner auxiliar de features proibidas.
15. Registrar auditoria final das colunas usadas em `X`, target, colunas removidas e motivo.
16. Ordenar cronologicamente por `match_date` e `match_id`.
17. Criar split temporal 60/20/20 sem shuffle.
18. Reportar observacoes sem historico por split.
19. Ajustar imputacao por mediana apenas no treino.
20. Aplicar imputacao em treino, validacao e teste.
21. Salvar datasets derivados de baseline.
22. Calcular baseline nulo com prevalencia do target no treino.
23. Treinar modelo somente se a tarefa futura autorizar explicitamente.
24. Avaliar baseline nulo.
25. Avaliar baseline treinado, se houver modelo aprovado.
26. Comparar modelo contra baseline nulo, incluindo Brier Score e Log Loss.
27. Gerar reports JSON.
28. Gerar relatorio Markdown final.
29. Encerrar com resumo executivo.

---

## 10. Conversao Team-Level para Match-Level

Entrada: `historical_prematch_features_v1.csv`, uma linha por time por partida.

Processo obrigatorio:

1. Separar linhas `is_home = 1`.
2. Validar unicidade de `match_id` nas linhas home.
3. Separar linhas `is_home = 0`.
4. Validar unicidade de `match_id` nas linhas away.
5. Prefixar colunas permitidas das linhas home com `home_`.
6. Prefixar colunas permitidas das linhas away com `away_`.
7. Fazer merge home-away por `match_id`.
8. Validar que o numero de linhas finais e igual ao numero de partidas unicas.
9. Anexar `target_late_goal_75` do Dataset V1 por `match_id`.
10. Validar que target nao possui nulos.

Saida esperada: dataset match-level com exatamente 1 linha por `match_id`.

Validacoes obrigatorias da conversao:

- `match_id` unico apos conversao;
- total de linhas igual ao numero de partidas unicas;
- nenhuma partida sem home;
- nenhuma partida sem away;
- nenhuma partida com mais de uma home;
- nenhuma partida com mais de uma away;
- target preenchido para todas as partidas;
- colunas target-derived ausentes do conjunto de features.

---

## 11. Regra para `history_matches_available = 0`

Observacoes sem historico anterior devem permanecer no experimento principal.

Regras operacionais:

- manter observacoes no experimento principal;
- nao remover partidas por ausencia de historico;
- imputar valores ausentes usando estatisticas aprendidas apenas no treino;
- reportar quantidade de observacoes com historico ausente por split;
- reportar quantidade de nulos imputados por split e feature;
- permitir analise de sensibilidade futura, se aprovada, excluindo partidas sem historico minimo.

A ausencia de historico no inicio da temporada e uma condicao operacional esperada, nao motivo automatico para remover partidas do experimento principal.

Analise de sensibilidade futura permitida, somente se aprovada:

- excluir partidas em que pelo menos um time tenha `history_matches_available < 3`;
- reportar resultados separadamente;
- nao substituir o resultado principal.

---

## 12. Estrategia de Imputacao Operacional

Problema esperado:

- primeiras partidas da temporada podem ter nulos porque times ainda nao possuem historico anterior.

Regra operacional principal:

- imputacao deve ser ajustada exclusivamente no treino.

Metodo aprovado:

- mediana do treino por feature.

Passos obrigatorios:

1. Apos split temporal, identificar nulos por feature em treino, validacao e teste.
2. Calcular mediana de cada feature usando somente treino.
3. Registrar medianas em `baseline_1_prematch_imputation_report.json`.
4. Aplicar medianas de treino no treino.
5. Aplicar as mesmas medianas de treino na validacao.
6. Aplicar as mesmas medianas de treino no teste.
7. Registrar nulos restantes apos imputacao.
8. Bloquear execucao se alguma feature permanecer nula apos imputacao.

Proibido:

- calcular mediana no dataset completo;
- usar validacao/teste para ajustar imputador;
- imputar target;
- imputar usando valores futuros;
- descartar linhas sem reportar.

Relatorio de imputacao deve conter:

- feature;
- mediana ajustada no treino;
- nulos antes por split;
- nulos depois por split;
- percentual imputado por split;
- quantidade de linhas com `history_matches_available = 0` ou equivalente por split;
- alerta para features com alta taxa de imputacao.

Limiar de alerta sugerido:

- mais de 10% de nulos imputados em qualquer split.

---

## 13. Estrategia de Split Temporal Operacional

Split aprovado:

- treino: 60%;
- validacao: 20%;
- teste: 20%.

Regra de ordenacao:

```text
ORDER BY match_date ASC, match_id ASC
```

Sem shuffle.

Sem stratification.

Sem balanceamento.

Passos obrigatorios:

1. Validar `match_date` nao nulo.
2. Converter `match_date` para datetime.
3. Ordenar por `match_date`, `match_id`.
4. Calcular indices de corte com base no numero total de partidas.
5. Atribuir as primeiras 60% linhas ao treino.
6. Atribuir as proximas 20% linhas a validacao.
7. Atribuir as ultimas 20% linhas ao teste.
8. Validar que nao ha sobreposicao de `match_id` entre splits.
9. Validar monotonicidade temporal entre splits.
10. Registrar datas minima/maxima por split.
11. Registrar prevalencia do target por split.
12. Registrar quantidade de observacoes com historico ausente por split.

Com 380 partidas, divisao esperada:

- treino: 228 partidas;
- validacao: 76 partidas;
- teste: 76 partidas.

Se a contagem final for diferente de 380, a regra 60/20/20 deve ser aplicada ao total real e o desvio precisa ser explicado no relatorio.

---

## 14. Comparacao Contra Baseline Nulo

A avaliacao futura deve comparar o modelo treinado contra o baseline nulo.

Comparacoes obrigatorias:

- Brier Score do modelo vs Brier Score do baseline nulo;
- Log Loss do modelo vs Log Loss do baseline nulo.

O relatorio final deve apresentar ambas as comparacoes por split, no minimo para validacao e teste.

A comparacao deve deixar claro:

- se o modelo melhora a qualidade probabilistica contra a probabilidade constante do treino;
- se a melhora em ranking tambem vem acompanhada de melhora ou degradacao probabilistica;
- se o modelo tem ROC-AUC/PR-AUC promissores, mas Brier Score ou Log Loss piores que o baseline nulo.

A aprovacao final nao deve ser baseada apenas em Brier Score ou Log Loss, mas esses indicadores devem qualificar a decisao.

---

## 15. Relatorios Obrigatorios

### `baseline_1_prematch_feature_manifest.json`

Deve conter:

- versao do baseline;
- data de geracao;
- arquivos de entrada;
- features permitidas;
- features finais usadas;
- whitelist oficial aplicada;
- features proibidas verificadas;
- target;
- colunas removidas;
- motivo da remocao quando aplicavel;
- grain;
- status do scanner anti-leakage.

### `baseline_1_prematch_split_report.json`

Deve conter:

- total de linhas;
- total por split;
- datas minima/maxima por split;
- positivos/negativos por split;
- prevalencia por split;
- quantidade de observacoes sem historico por split;
- validacao de ausencia de overlap;
- validacao de ordem temporal.

### `baseline_1_prematch_imputation_report.json`

Deve conter:

- metodo de imputacao;
- estatisticas ajustadas somente no treino;
- nulos antes/depois por split;
- medianas por feature;
- quantidade imputada por split;
- alertas.

### `baseline_1_prematch_metrics.json`

Deve conter, para treino, validacao e teste:

- baseline nulo;
- modelo treinado, se autorizado;
- ROC-AUC;
- PR-AUC;
- prevalence;
- Brier Score;
- Log Loss;
- Lift@Top20%;
- calibration bins;
- comparacao modelo vs baseline nulo em Brier Score;
- comparacao modelo vs baseline nulo em Log Loss.

### `baseline_1_prematch_validation_report.json`

Deve conter:

- status final: `APTO`, `APTO COM RESSALVAS` ou `NAO APTO`;
- erros bloqueantes;
- warnings;
- checks anti-leakage;
- checks de split;
- checks de imputacao;
- checks de target;
- checks de features proibidas;
- lista completa das colunas usadas em `X`;
- target utilizado;
- colunas removidas;
- motivo da remocao quando aplicavel.

### `docs/04_RESEARCH/BASELINE_PREMATCH_H3_H4_RESULTS.md`

Deve conter:

1. resumo executivo;
2. objetivo;
3. arquivos de entrada;
4. metodologia;
5. features usadas;
6. features proibidas verificadas;
7. auditoria final das colunas de `X`;
8. target utilizado;
9. colunas removidas e motivo;
10. split temporal;
11. quantidade de observacoes sem historico por split;
12. imputacao;
13. baseline nulo;
14. metricas por split;
15. comparacao com baseline nulo;
16. calibracao;
17. Lift@Top20%;
18. decisao final;
19. limitacoes;
20. recomendacoes.

---

## 16. Artefatos Gerados

Artefatos de dados derivados:

- dataset match-level consolidado;
- dataset de treino;
- dataset de validacao;
- dataset de teste.

Artefatos de auditoria:

- manifest de features;
- report de split;
- report de imputacao;
- report de validacao;
- metricas em JSON.

Artefatos de pesquisa:

- relatorio Markdown em `docs/04_RESEARCH`.

Artefato de modelo:

- somente se treinamento for explicitamente autorizado.

Nenhum artefato pode substituir arquivos de entrada.

---

## 17. Validacoes Obrigatorias

Validacoes de entrada:

- arquivos existem;
- CSVs sao legiveis;
- metadados existem;
- validation reports existem;
- `historical_prematch_features_v1` esta `APTO` ou aprovado com ressalvas;
- Dataset V1 possui `target_late_goal_75`;
- `target_late_goal_75` nao possui nulos.

Validacoes de grain:

- feature set possui 2 linhas por partida;
- uma linha home por partida;
- uma linha away por partida;
- dataset final possui 1 linha por partida;
- `match_id` unico no dataset final.

Validacoes de features:

- todas as features obrigatorias existem;
- whitelist oficial aplicada antes da matriz `X`;
- nenhuma feature fora da whitelist entra no treino;
- nenhuma feature proibida entra no treino;
- target nao entra em `X`;
- colunas derivadas do target nao entram em `X`;
- colunas in-game nao entram em `X`;
- xG/xGA/forecast nao entram em `X`;
- auditoria final lista todas as colunas usadas em `X`.

Validacoes temporais:

- split sem shuffle;
- datas ordenadas;
- treino termina antes ou no limite da validacao;
- validacao termina antes ou no limite do teste;
- nenhum `match_id` aparece em mais de um split.

Validacoes de imputacao:

- imputador ajustado apenas no treino;
- medianas registradas;
- validacao/teste usam medianas do treino;
- nulos restantes iguais a zero nas features finais;
- taxa de imputacao registrada;
- observacoes sem historico mantidas no experimento principal.

Validacoes de metricas:

- ROC-AUC calculado apenas quando existem duas classes no split;
- PR-AUC comparado contra prevalencia do split;
- Brier Score calculado com probabilidades;
- Log Loss com probabilidades clipadas para evitar infinito;
- Lift@Top20% documentado com tamanho do top bucket;
- baseline nulo reportado com ROC-AUC, PR-AUC, Brier Score e Log Loss;
- modelo comparado ao baseline nulo em Brier Score e Log Loss.

---

## 18. Controles Anti-Leakage

Regra oficial:

- whitelist oficial prevalece sobre blacklist;
- apenas features explicitamente aprovadas podem entrar em `X`;
- blacklist e scanner de nomes proibidos sao controles auxiliares, nao mecanismo de autorizacao.

Controles obrigatorios antes de qualquer fit:

1. Aplicar whitelist fechada de features permitidas.
2. Rejeitar automaticamente qualquer coluna fora da whitelist.
3. Rodar scanner auxiliar de nomes proibidos.
4. Rejeitar colunas target-derived.
5. Rejeitar features in-game.
6. Rejeitar xG/xGA da propria partida.
7. Rejeitar forecast.
8. Confirmar que feature set historico foi validado com `shift(1)`.
9. Fazer split temporal antes de imputacao.
10. Ajustar imputador somente no treino.
11. Ajustar modelo somente no treino.
12. Usar validacao/teste apenas para avaliacao.
13. Gerar auditoria final das colunas usadas em `X`.

Auditoria final obrigatoria:

- lista completa das colunas usadas em `X`;
- target utilizado;
- colunas removidas;
- motivo da remocao quando aplicavel;
- confirmacao de que nenhuma coluna fora da whitelist entrou em `X`;
- confirmacao de que nenhuma coluna de target entrou em `X`.

Padroes proibidos em nomes de colunas:

```text
target
late_goal
has_late_goal
home_late_goal
away_late_goal
first_late_goal
last_goal
incident
score
cutoff
cards_until
substitutions_until
xg
xga
forecast
home_goals
away_goals
total_goals
```

Observacao: a implementacao futura deve aplicar blacklist com cuidado para nao bloquear os nomes permitidos por engano. Por exemplo, `goals_for_avg_last_3` e permitido porque representa media historica pre-jogo; `home_goals` e proibido porque representa placar da propria partida.

---

## 19. Ordem de Execucao dos Componentes

Ordem exata recomendada:

```text
1. baseline_config.py
2. build_baseline_dataset.py
3. temporal_split.py
4. imputation.py
5. train_baseline_model.py
6. evaluate_baseline.py
7. run_baseline_1_prematch.py
```

Na execucao via orquestrador:

```text
run_baseline_1_prematch.py
  -> load config
  -> build match-level dataset
  -> apply official whitelist
  -> validate forbidden features
  -> write X-column audit
  -> temporal split
  -> report history_matches_available = 0 by split
  -> fit train-only imputer
  -> transform splits
  -> compute null baseline from train prevalence
  -> train approved model, if authorized
  -> evaluate null baseline
  -> evaluate trained baseline, if authorized
  -> compare model vs null baseline
  -> write artifacts
  -> write reports
```

---

## 20. Criterios de Aprovacao do Baseline Futuro

O baseline futuro so pode ser considerado aprovado se, no teste temporal:

1. `ROC-AUC Test > 0.55`.
2. `PR-AUC Test > prevalence_test + 0.03`.
3. A analise conjunta da metrica principal e do criterio co-obrigatorio for positiva.
4. `abs(ROC-AUC Validation - ROC-AUC Test) <= 0.07` ou divergencia justificada.
5. Nenhuma feature proibida foi usada.
6. Apenas features explicitamente aprovadas entraram em `X`.
7. Split temporal foi documentado.
8. Imputacao foi ajustada somente no treino.
9. Observacoes sem historico foram mantidas no experimento principal e reportadas por split.
10. Baseline nulo foi reportado.
11. Modelo foi comparado contra baseline nulo em Brier Score e Log Loss.
12. Relatorios obrigatorios foram gerados.

Se falhar:

- nao avancar para backtesting;
- nao avancar para producao;
- registrar falha no relatorio;
- retornar ao Quant Research para revisao metodologica.

---

## 21. Fora de Escopo

Esta especificacao nao autoriza:

- criacao de modelos agora;
- treinamento agora;
- baseline agora;
- backtesting;
- pipeline de producao;
- alteracao de datasets existentes;
- alteracao de PostgreSQL;
- alteracao de schema;
- alteracao de crawlers;
- alteracao de importers;
- uso de H6/H9;
- uso de H1/H2;
- uso de H8;
- uso de xG/xGA/forecast pos-kickoff;
- uso de estatisticas da propria partida.

---

## 22. Checklist para Tarefa Futura ao Codex

Antes de implementar, a tarefa futura deve declarar explicitamente:

- modelo aprovado;
- se Baseline 1B esta autorizado ou nao;
- caminhos finais de output;
- se artefatos derivados devem ser versionados;
- criterio de overwrite de artefatos;
- formato esperado do relatorio final.

Sem essas confirmacoes, Codex deve implementar no maximo componentes de preparacao e validacao, nunca treinamento.

---

## Decisao da Especificacao

Baseline 1 fica especificado operacionalmente como:

- pre-jogo apenas;
- H3 + H4 aprovadas;
- target `target_late_goal_75`;
- conversao team-level para match-level;
- split temporal cronologico 60/20/20;
- observacoes sem historico mantidas e imputadas no experimento principal;
- imputacao por mediana fitada apenas no treino;
- baseline nulo calculado pela prevalencia do treino;
- hierarquia oficial com ROC-AUC Test como metrica principal e PR-AUC Test como criterio co-obrigatorio;
- whitelist oficial prevalecendo sobre blacklist;
- auditoria final obrigatoria das colunas de `X`;
- comparacao contra baseline nulo em Brier Score e Log Loss;
- relatorios JSON e Markdown obrigatorios;
- nenhuma implementacao ou treinamento autorizado por este documento.

Status: pronto para aprovacao final do PM antes de qualquer implementacao.
