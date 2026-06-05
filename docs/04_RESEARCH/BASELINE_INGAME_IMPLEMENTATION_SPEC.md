# BASELINE IN-GAME IMPLEMENTATION SPEC

## Status

Especificacao metodologica e operacional.

Nao implementado.

Nao contem codigo.

Nao executa treinamento.

Nao executa experimento.

Nao altera datasets.

Nao altera PostgreSQL, schema, crawlers ou importers.

Documento base:

- `docs/04_RESEARCH/BASELINE_INGAME_EXPERIMENT_PLAN.md`

---

## 1. Objetivo

Definir, com nivel operacional suficiente, como uma futura implementacao do Baseline In-Game V1 deve ser estruturada e validada sem novas decisoes metodologicas.

O Baseline In-Game V1 e obrigatoriamente:

- tipo: in-game only;
- cutoff: 75 minutos;
- target: `target_late_goal_75`;
- target operacional: `target_goal_after_cutoff` filtrado em `cutoff_minute = 75`;
- unidade final: 1 linha por partida;
- split: temporal cronologico 60/20/20;
- shuffle: proibido;
- features pre-jogo: proibidas;
- eventos apos cutoff: proibidos;
- estatisticas finais da partida: proibidas.

Esta especificacao nao autoriza implementacao. Ela apenas define o desenho da implementacao futura.

---

## 2. Snapshot Oficial

Snapshot oficial:

```text
cutoff_minute = 75
```

Regra temporal:

```text
features: somente informacoes com minute <= 75
target: gol com minute > 75
```

Interpretacao:

- eventos registrados exatamente no minuto 75 entram nas features;
- eventos registrados apos o minuto 75 entram no target;
- nenhum evento posterior ao cutoff pode entrar em `X`.

Fonte esperada:

- `LateGoalResearch/data/processed/datasets/late_goal_dataset_v1b_ingame.csv`.

Filtro obrigatorio:

```text
cutoff_minute == 75
```

Validacoes obrigatorias do snapshot:

- todas as linhas usadas devem ter `cutoff_minute = 75`;
- deve existir exatamente 1 linha por `match_id` apos o filtro;
- as features permitidas devem representar apenas estado/eventos ate 75;
- o target operacional deve representar apenas gols apos 75;
- se houver colunas ou auditoria de eventos, `max_event_minute_used_for_features <= 75`.

---

## 3. Unidade do Experimento

Unidade final:

- 1 linha por partida no cutoff 75.

Target oficial:

- `target_late_goal_75`.

Target operacional:

- `target_goal_after_cutoff` no dataset V1B, apos filtro `cutoff_minute = 75`.

Validacao de equivalencia:

- quando `target_late_goal_75` estiver disponivel por `match_id`, validar igualdade com `target_goal_after_cutoff` no cutoff 75;
- divergencias devem bloquear a execucao ate auditoria.

Grain esperado:

```text
match_id unico
cutoff_minute = 75
```

---

## 4. Features Permitidas

Whitelist oficial:

### H6 - Estado da Partida

- `score_diff_home_until_cutoff`
- `score_state_group`

### H9 - Eventos

- `cards_until_cutoff`
- `substitutions_until_cutoff`

Total esperado:

- 4 features base antes de codificacao categorica.

Observacao:

- `score_state_group` pode exigir codificacao categorica;
- a codificacao deve ser ajustada somente no treino;
- categorias novas em validacao/teste devem receber tratamento fixo documentado.

---

## 5. Features e Fontes Proibidas

Proibido usar:

- H1;
- H2;
- H8;
- xG;
- xGA;
- forecast;
- estatisticas finais da partida;
- eventos apos cutoff;
- target-derived features;
- `match_statistics` full-match;
- features pre-jogo H3/H4;
- placar final;
- total de gols final;
- qualquer coluna derivada diretamente do target.

Colunas proibidas explicitamente:

- `target_late_goal_75` em `X`;
- `target_goal_after_cutoff` em `X`;
- `has_late_goal`;
- `late_goal_count_75`;
- `first_late_goal_minute_75`;
- `home_late_goal_count_75`;
- `away_late_goal_count_75`;
- `home_goals` final;
- `away_goals` final;
- `total_goals` final;
- qualquer coluna com `xg`, `xga` ou `forecast`.

---

## 6. Estrategia de Split Temporal

Split aprovado:

- treino: 60%;
- validacao: 20%;
- teste: 20%.

Regra obrigatoria:

```text
ORDER BY match_date ASC, match_id ASC
```

Sem:

- shuffle;
- stratification;
- balanceamento artificial.

Com 380 partidas, divisao esperada:

- treino: 228 partidas;
- validacao: 76 partidas;
- teste: 76 partidas.

Auditoria obrigatoria:

- total de linhas por split;
- datas minima/maxima por split;
- positivos/negativos por split;
- prevalencia por split;
- ausencia de overlap de `match_id`;
- monotonicidade temporal entre splits.

---

## 7. Estrategia de Validacao

Validacao primaria:

- avaliar o modelo futuro em treino, validacao e teste;
- usar o teste apenas uma vez para decisao final;
- comparar sempre contra baseline nulo;
- comparar tambem contra Baseline 1A apenas como referencia externa.

Nao permitido:

- selecionar features usando teste;
- ajustar thresholds usando teste;
- ajustar encoder/imputador usando validacao/teste;
- reexecutar multiplas variantes e escolher a melhor pelo teste sem novo plano aprovado.

Sinais de alerta:

- performance alta no treino e baixa em validacao/teste;
- PR-AUC abaixo do criterio minimo;
- Brier ou Log Loss piores que o baseline nulo;
- forte dependencia de uma unica categoria de `score_state_group`.

---

## 8. Estrategia de Imputacao e Codificacao

### Numericas

Features numericas esperadas:

- `score_diff_home_until_cutoff`
- `cards_until_cutoff`
- `substitutions_until_cutoff`

Regra:

- se houver nulos, imputar com mediana do treino;
- aplicar a mesma mediana em validacao e teste;
- reportar nulos antes/depois por split e feature.

### Categorica

Feature categorica esperada:

- `score_state_group`

Regra:

- ajustar encoder somente no treino;
- aplicar o encoder em validacao e teste;
- categorias desconhecidas devem ser tratadas por regra fixa;
- reportar categorias observadas por split.

Proibido:

- calcular imputacao com dataset inteiro;
- ajustar encoder com dataset inteiro;
- usar validacao/teste para definir categorias;
- remover linhas sem reportar impacto.

---

## 9. Baseline Nulo

Baseline nulo obrigatorio:

- probabilidade constante igual a prevalencia do target no treino.

Regra:

- calcular prevalencia apenas no treino;
- aplicar a mesma probabilidade constante em treino, validacao e teste.

Metricas obrigatorias do baseline nulo:

- ROC-AUC;
- PR-AUC;
- Brier Score;
- Log Loss;
- Lift@Top20%, quando aplicavel.

---

## 10. Metricas Principais

Metricas principais:

- ROC-AUC Test;
- PR-AUC Test.

Metrica principal oficial:

- ROC-AUC Test.

Criterio co-obrigatorio:

- PR-AUC Test.

Interpretacao:

- ROC-AUC mede ranking geral;
- PR-AUC mede concentracao de positivos;
- PR-AUC deve ser comparado contra a prevalencia do proprio split.

---

## 11. Metricas Secundarias

Metricas secundarias obrigatorias:

- Brier Score;
- Log Loss;
- Lift@Top20%;
- Calibration by bins.

Interpretacao:

- Brier Score mede qualidade probabilistica;
- Log Loss penaliza confianca errada;
- Lift@Top20% mede concentracao operacional dos casos de maior score;
- Calibration by bins avalia confiabilidade das probabilidades.

---

## 12. Criterios Minimos de Aprovacao

O Baseline In-Game V1 so pode ser aprovado se, no conjunto de teste:

1. `ROC-AUC Test > 0.55`.
2. `PR-AUC Test > prevalence_test + 0.03`.
3. Nenhuma feature proibida foi usada.
4. Snapshot foi validado em `cutoff_minute = 75`.
5. Nenhum evento apos 75 entrou nas features.
6. Split temporal foi documentado.
7. Imputacao/codificacao foram ajustadas somente no treino.
8. Baseline nulo foi reportado.

Criterio probabilistico auxiliar:

- Brier Score do modelo <= Brier Score do baseline nulo;
- Log Loss do modelo <= Log Loss do baseline nulo.

Regras de decisao:

- se ROC-AUC e PR-AUC falharem: `NAO APROVADO`;
- se ROC-AUC e PR-AUC passarem, mas Brier/Log Loss piorarem: `APTO COM RESSALVAS`;
- se criterios principais e probabilisticos passarem: `APROVADO`.

---

## 13. Comparacoes Obrigatorias

### Baseline nulo

Comparacao obrigatoria.

Relatorio deve comparar modelo vs nulo em:

- ROC-AUC;
- PR-AUC;
- Brier Score;
- Log Loss;
- Lift@Top20%.

### Baseline 1A

Comparacao obrigatoria apenas como referencia externa.

Referencia Baseline 1A:

- ROC-AUC Test: 0.4910;
- PR-AUC Test: 0.5364.

Observacao:

- Baseline 1A e pre-jogo;
- Baseline In-Game V1 e minuto 75;
- os momentos de disponibilidade sao diferentes;
- superar Baseline 1A e desejavel, mas a aprovacao oficial depende dos criterios do proprio experimento.

---

## 14. Auditorias Anti-Leakage

Auditorias obrigatorias:

1. Confirmar `cutoff_minute = 75` em todas as linhas.
2. Confirmar 1 linha por `match_id`.
3. Confirmar ausencia de eventos apos cutoff nas features.
4. Confirmar ausencia de `match_statistics` full-match.
5. Confirmar ausencia de xG/xGA/forecast.
6. Confirmar ausencia de H1/H2/H8.
7. Confirmar ausencia de features pre-jogo.
8. Confirmar ausencia de target-derived features em `X`.
9. Confirmar target fora de `X`.
10. Confirmar split temporal antes de imputacao/codificacao.
11. Confirmar fit do imputador/encoder somente no treino.
12. Listar colunas finais usadas em `X`.

Whitelist deve prevalecer sobre blacklist:

- somente features explicitamente permitidas podem entrar em `X`;
- scanner de nomes proibidos e controle auxiliar, nao mecanismo de autorizacao.

---

## 15. Estrutura do Relatorio Final

Relatorio esperado da implementacao futura:

- `docs/04_RESEARCH/BASELINE_INGAME_V1_RESULTS.md`

Conteudo obrigatorio:

1. Resumo executivo.
2. Objetivo.
3. Arquivos de entrada.
4. Snapshot oficial.
5. Filtro de cutoff aplicado.
6. Validacao do snapshot.
7. Unidade do experimento.
8. Features usadas.
9. Features proibidas verificadas.
10. Auditoria final das colunas de `X`.
11. Target utilizado.
12. Comparacao `target_goal_after_cutoff` vs `target_late_goal_75`.
13. Split temporal.
14. Imputacao e codificacao.
15. Baseline nulo.
16. Metricas por split.
17. Comparacao com baseline nulo.
18. Comparacao externa com Baseline 1A.
19. Calibration by bins.
20. Lift@Top20%.
21. Decisao final.
22. Limitacoes.
23. Recomendacoes.

---

## 16. Artefatos Esperados da Implementacao Futura

Artefatos derivados esperados:

- dataset in-game filtrado no cutoff 75;
- split treino;
- split validacao;
- split teste;
- feature manifest;
- split report;
- imputation/coding report;
- metrics report;
- validation report;
- relatorio Markdown final.

Nenhum artefato pode substituir ou modificar datasets originais.

---

## 17. Baseline In-Game V2 Futuro

Direcao futura aprovada:

- comparar cutoffs 60, 65, 70 e 75.

Objetivo:

- medir trade-off entre antecedencia operacional e ganho informacional.

Regras futuras:

- cada cutoff deve ser avaliado separadamente;
- cada cutoff deve respeitar `minute <= cutoff` para features;
- cada cutoff deve respeitar `minute > cutoff` para target;
- metricas devem ser reportadas por cutoff;
- baseline nulo deve ser calculado por cutoff/split;
- a escolha do cutoff deve considerar performance e utilidade operacional.

Status:

- nao autorizado para implementacao por esta especificacao;
- nao faz parte do V1;
- deve exigir novo plano ou adendo aprovado pelo PM/CTO.

---

## Decisao Quant

O Baseline In-Game V1 esta especificado como:

- In-Game Only;
- cutoff unico 75;
- H6 + H9;
- target `target_late_goal_75`;
- target operacional `target_goal_after_cutoff` no cutoff 75;
- 4 features permitidas;
- split temporal 60/20/20;
- baseline nulo obrigatorio;
- comparacao externa com Baseline 1A;
- criterios minimos: ROC-AUC Test > 0.55 e PR-AUC Test > prevalence_test + 0.03.

Status:

- PRONTO PARA REVISAO DO PM.
- IMPLEMENTACAO AINDA BLOQUEADA.
