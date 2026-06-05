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

## 3. Estrutura de Diretorios Recomendada

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

## 4. Estrutura dos Arquivos da Futura Implementacao

### `Analytics/Baseline/baseline_config.py`

Responsabilidade:

- centralizar constantes operacionais;
- definir caminhos de input/output;
- definir whitelist de features permitidas;
- definir blacklist de features proibidas;
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
- aplicar whitelist de features;
- rejeitar features proibidas;
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
- reportar periodo e prevalencia por split.

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
- exportar manifest de imputacao.

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

- avaliar baseline constante;
- avaliar baseline treinado;
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
- chamar treinamento, somente quando modelo estiver aprovado;
- chamar avaliacao;
- salvar artefatos e reports;
- encerrar com resumo executivo no terminal.

Nao deve:

- conter logica metodologica escondida;
- sobrescrever artefatos sem controle de versao ou timestamp, salvo decisao aprovada;
- acessar PostgreSQL.

---

## 5. Inputs Necessarios

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

## 6. Outputs Esperados

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

## 7. Pipeline Operacional Completo

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
13. Aplicar whitelist de features do Baseline 1A.
14. Executar scanner de features proibidas.
15. Ordenar cronologicamente por `match_date` e `match_id`.
16. Criar split temporal 60/20/20 sem shuffle.
17. Ajustar imputacao por mediana apenas no treino.
18. Aplicar imputacao em treino, validacao e teste.
19. Salvar datasets derivados de baseline.
20. Treinar modelo somente se a tarefa futura autorizar explicitamente.
21. Avaliar baseline constante.
22. Avaliar baseline treinado, se houver modelo aprovado.
23. Gerar reports JSON.
24. Gerar relatorio Markdown final.
25. Encerrar com resumo executivo.

---

## 8. Conversao Team-Level para Match-Level

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

## 9. Estrategia de Imputacao Operacional

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
- alerta para features com alta taxa de imputacao.

Limiar de alerta sugerido:

- mais de 10% de nulos imputados em qualquer split.

---

## 10. Estrategia de Split Temporal Operacional

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

Com 380 partidas, divisao esperada:

- treino: 228 partidas;
- validacao: 76 partidas;
- teste: 76 partidas.

Se a contagem final for diferente de 380, a regra 60/20/20 deve ser aplicada ao total real e o desvio precisa ser explicado no relatorio.

---

## 11. Relatorios Obrigatorios

### `baseline_1_prematch_feature_manifest.json`

Deve conter:

- versao do baseline;
- data de geracao;
- arquivos de entrada;
- features permitidas;
- features finais usadas;
- features proibidas verificadas;
- target;
- grain;
- status do scanner anti-leakage.

### `baseline_1_prematch_split_report.json`

Deve conter:

- total de linhas;
- total por split;
- datas minima/maxima por split;
- positivos/negativos por split;
- prevalencia por split;
- validacao de ausencia de overlap;
- validacao de ordem temporal.

### `baseline_1_prematch_imputation_report.json`

Deve conter:

- metodo de imputacao;
- estatisticas ajustadas somente no treino;
- nulos antes/depois por split;
- medianas por feature;
- alertas.

### `baseline_1_prematch_metrics.json`

Deve conter, para treino, validacao e teste:

- baseline constante;
- modelo treinado, se autorizado;
- ROC-AUC;
- PR-AUC;
- prevalence;
- Brier Score;
- Log Loss;
- Lift@Top20%;
- calibration bins.

### `baseline_1_prematch_validation_report.json`

Deve conter:

- status final: `APTO`, `APTO COM RESSALVAS` ou `NAO APTO`;
- erros bloqueantes;
- warnings;
- checks anti-leakage;
- checks de split;
- checks de imputacao;
- checks de target;
- checks de features proibidas.

### `docs/04_RESEARCH/BASELINE_PREMATCH_H3_H4_RESULTS.md`

Deve conter:

1. resumo executivo;
2. objetivo;
3. arquivos de entrada;
4. metodologia;
5. features usadas;
6. features proibidas verificadas;
7. split temporal;
8. imputacao;
9. metricas por split;
10. comparacao com baseline constante;
11. calibracao;
12. Lift@Top20%;
13. decisao final;
14. limitacoes;
15. recomendacoes.

---

## 12. Artefatos Gerados

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

## 13. Validacoes Obrigatorias

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
- nenhuma feature fora da whitelist entra no treino;
- nenhuma feature proibida entra no treino;
- target nao entra em `X`;
- colunas derivadas do target nao entram em `X`;
- colunas in-game nao entram em `X`;
- xG/xGA/forecast nao entram em `X`.

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
- taxa de imputacao registrada.

Validacoes de metricas:

- ROC-AUC calculado apenas quando existem duas classes no split;
- PR-AUC comparado contra prevalencia do split;
- Brier Score calculado com probabilidades;
- Log Loss com probabilidades clipadas para evitar infinito;
- Lift@Top20% documentado com tamanho do top bucket.

---

## 14. Controles Anti-Leakage

Controles obrigatorios antes de qualquer fit:

1. Scanner de nomes de colunas proibidas.
2. Whitelist fechada de features permitidas.
3. Rejeicao automatica de colunas target-derived.
4. Rejeicao automatica de features in-game.
5. Rejeicao automatica de xG/xGA da propria partida.
6. Rejeicao automatica de forecast.
7. Confirmacao de que feature set historico foi validado com `shift(1)`.
8. Split temporal antes de imputacao.
9. Fit do imputador somente no treino.
10. Fit do modelo somente no treino.
11. Validacao/teste usados apenas para avaliacao.
12. Relatorio explicito de todas as colunas usadas em `X`.

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

## 15. Ordem de Execucao dos Componentes

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
  -> validate feature whitelist
  -> validate forbidden features
  -> temporal split
  -> fit train-only imputer
  -> transform splits
  -> train approved model, if authorized
  -> evaluate constant baseline
  -> evaluate trained baseline, if authorized
  -> write artifacts
  -> write reports
```

---

## 16. Criterios de Aprovacao do Baseline Futuro

O baseline futuro so pode ser considerado aprovado se, no teste temporal:

1. `ROC-AUC Test > 0.55`.
2. `PR-AUC Test > prevalence_test + 0.03`.
3. `abs(ROC-AUC Validation - ROC-AUC Test) <= 0.07` ou divergencia justificada.
4. Nenhuma feature proibida foi usada.
5. Split temporal foi documentado.
6. Imputacao foi ajustada somente no treino.
7. Relatorios obrigatorios foram gerados.

Se falhar:

- nao avancar para backtesting;
- nao avancar para producao;
- registrar falha no relatorio;
- retornar ao Quant Research para revisao metodologica.

---

## 17. Fora de Escopo

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

## 18. Checklist para Tarefa Futura ao Codex

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
- imputacao por mediana fitada apenas no treino;
- scanner anti-leakage obrigatorio;
- relatorios JSON e Markdown obrigatorios;
- nenhuma implementacao ou treinamento autorizado por este documento.

Status: pronto para revisao do PM/CTO antes de qualquer implementacao.
