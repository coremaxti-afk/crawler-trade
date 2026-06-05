# BASELINE IN-GAME EXPERIMENT PLAN

## Status

Plano metodologico formal.

Nao implementado.

Nao contem codigo.

Nao executa treinamento.

Nao executa baseline.

Nao altera datasets.

---

## Objetivo

Definir o primeiro experimento baseline in-game do LateGoalResearch antes de qualquer implementacao.

Este plano deve ser revisado pelo PM e, se necessario, pelo CTO antes de qualquer tarefa ao Codex.

---

## Contexto

O Baseline 1A Pre-Match H3/H4 foi executado como referencia exploratoria controlada e obteve resultado quantitativo nao aprovado.

Resultado de referencia do Baseline 1A:

- ROC-AUC Test: 0.4910.
- PR-AUC Test: 0.5364.
- Prevalencia Test: 0.5263.
- Brier modelo vs baseline nulo: piorou +0.0089.
- Log Loss modelo vs baseline nulo: piorou +0.0180.

Interpretacao:

- O Baseline 1A nao autoriza backtesting, producao ou sistema decisorio.
- O Baseline In-Game V1 deve ser tratado como experimento separado, nao como extensao direta do baseline pre-jogo.

---

## Arquitetura Aprovada

Tipo:

- In-Game Only.

Cutoff inicial:

- 75 minutos.

Target:

- `target_late_goal_75`.

Hipoteses permitidas:

- H6 - Estado da Partida.
- H9 - Eventos.

Features permitidas:

- `score_diff_home_until_cutoff`
- `score_state_group`
- `cards_until_cutoff`
- `substitutions_until_cutoff`

Hipoteses bloqueadas ou fora do escopo:

- H1 - Bloqueada por leakage.
- H2 - Bloqueada por leakage.
- H3 - Fora do Baseline In-Game V1.
- H4 - Fora do Baseline In-Game V1.
- H5 - Nao validada.
- H7 - Nao validada como hipotese independente.
- H8 - Bloqueada por ausencia de graph/momentum.

Proibido:

- features pre-jogo;
- H1/H2/H8;
- eventos apos cutoff;
- estatisticas finais da partida;
- xG/xGA/forecast;
- target-derived columns.

---

## 1. Unidade do Experimento

Unidade final do Baseline In-Game V1:

- 1 linha por partida no cutoff 75.

Fonte esperada:

- `LateGoalResearch/data/processed/datasets/late_goal_dataset_v1b_ingame.csv`.

Filtro obrigatorio:

```text
cutoff_minute == 75
```

Target operacional recomendado:

- usar `target_goal_after_cutoff` no dataset in-game filtrado em `cutoff_minute = 75`.

Equivalencia esperada:

- para `cutoff_minute = 75`, `target_goal_after_cutoff` deve ser equivalente a `target_late_goal_75`.

Validacao obrigatoria:

- comparar `target_goal_after_cutoff` no cutoff 75 contra `target_late_goal_75` por `match_id`.
- bloquear execucao se houver divergencias nao explicadas.

Interpretacao:

- O experimento estima a probabilidade de haver pelo menos um gol apos 75:00 usando apenas o estado e eventos acumulados ate 75:00.

---

## 2. Cutoff Inicial

Cutoff aprovado para V1:

- 75 minutos.

Justificativa Quant:

- Alinha diretamente snapshot e target.
- Maximiza informacao disponivel antes da janela-alvo.
- Reduz ambiguidade metodologica no primeiro experimento.
- Permite testar o sinal de H6/H9 no ponto imediatamente anterior ao periodo de gol tardio.

Regra exata:

```text
features: eventos e estado com minute <= 75
target: gols com minute > 75
```

Ponto critico:

- eventos no minuto 75 entram nas features;
- eventos apos 75 entram no target;
- nenhum evento apos 75 pode entrar em `X`.

Ressalva operacional:

- cutoff 75 possui menor antecedencia pratica para tomada de decisao.
- Por isso, cutoffs anteriores devem ser planejados para uma versao futura, nao misturados no V1.

---

## 3. Snapshot In-Game Sem Leakage

O snapshot do Baseline In-Game V1 deve representar somente informacao disponivel ate o minuto 75.

Features permitidas e sua disponibilidade:

| Feature | Fonte | Momento disponivel | Regra anti-leakage |
|---|---|---|---|
| `score_diff_home_until_cutoff` | incidentes de gols validos | ate 75 | usar apenas gols com minuto <= 75 |
| `score_state_group` | placar derivado | ate 75 | derivar apenas do placar ate 75 |
| `cards_until_cutoff` | incidentes de cartao | ate 75 | contar apenas cartoes com minuto <= 75 |
| `substitutions_until_cutoff` | incidentes de substituicao | ate 75 | contar apenas substituicoes com minuto <= 75 |

Controles obrigatorios:

1. `cutoff_minute` deve ser 75 em todas as linhas.
2. `max_event_minute_used_for_features <= 75`, se houver auditoria de eventos disponivel.
3. Nenhuma feature pode usar eventos com minuto > 75.
4. Nenhuma estatistica full-match pode entrar em `X`.
5. Nenhuma coluna derivada do target pode entrar em `X`.
6. O target nao pode entrar em `X`.
7. Placar final nao pode entrar em `X`.
8. Total de gols final nao pode entrar em `X`.

---

## 4. Features Permitidas

Whitelist oficial do Baseline In-Game V1:

- `score_diff_home_until_cutoff`
- `score_state_group`
- `cards_until_cutoff`
- `substitutions_until_cutoff`

Observacao sobre `score_state_group`:

- se for categorica, deve ser codificada por tecnica simples e documentada;
- a codificacao deve ser ajustada somente no treino;
- categorias ausentes em validacao/teste devem ter tratamento definido sem usar informacao futura.

Features explicitamente proibidas:

- `target_late_goal_75`
- `target_goal_after_cutoff`
- `has_late_goal`
- `late_goal_count_75`
- `first_late_goal_minute_75`
- `home_late_goal_count_75`
- `away_late_goal_count_75`
- `home_goals`
- `away_goals`
- `total_goals`
- `xg`
- `xga`
- `forecast`
- qualquer feature pre-jogo H3/H4
- qualquer feature H1/H2/H8
- qualquer feature derivada de eventos apos 75
- qualquer estatistica final da partida

---

## 5. Target

Target oficial:

- `target_late_goal_75`.

Target operacional no dataset V1B:

- `target_goal_after_cutoff`, filtrado em `cutoff_minute = 75`.

Regra:

```text
target = 1 se existir gol com minuto > 75
target = 0 caso contrario
```

Validacao obrigatoria:

- se `target_late_goal_75` e `target_goal_after_cutoff` estiverem ambos disponiveis, devem ser iguais para `cutoff_minute = 75`.
- qualquer divergencia deve bloquear a execucao ate auditoria.

---

## 6. Split Temporal

Split recomendado:

- treino: 60%.
- validacao: 20%.
- teste: 20%.

Regra obrigatoria:

- ordenar por `match_date` em ordem crescente.
- sem shuffle.
- sem stratification.
- sem balanceamento.

Com 380 partidas, a divisao esperada e aproximadamente:

- treino: 228 partidas.
- validacao: 76 partidas.
- teste: 76 partidas.

Auditoria obrigatoria:

- datas minima/maxima de cada split;
- positivos/negativos por split;
- prevalencia por split;
- verificacao de que nenhum `match_id` aparece em mais de um split;
- verificacao de monotonicidade temporal.

---

## 7. Imputacao e Codificacao

Imputacao:

- se houver nulos em features numericas, imputar com mediana do treino;
- aplicar a mesma mediana em treino, validacao e teste;
- registrar nulos antes/depois por split e feature.

Codificacao categorica:

- `score_state_group` deve ser codificado somente com categorias aprendidas no treino;
- validacao/teste nao podem alterar o encoder;
- categorias desconhecidas devem ser tratadas por regra fixa documentada.

Proibido:

- calcular imputacao com dataset inteiro;
- usar validacao/teste para ajustar imputador ou encoder;
- remover linhas sem reportar impacto;
- criar features fora da whitelist.

---

## 8. Baseline Nulo

Baseline nulo obrigatorio:

- probabilidade constante igual a prevalencia do target no treino.

O baseline nulo deve ser avaliado em:

- treino;
- validacao;
- teste.

Metricas do baseline nulo:

- ROC-AUC;
- PR-AUC;
- Brier Score;
- Log Loss;
- Lift@Top20%, quando aplicavel.

---

## 9. Metricas de Avaliacao

Metricas principais:

- ROC-AUC Test.
- PR-AUC Test.

Metrica principal oficial:

- ROC-AUC Test.

Criterio co-obrigatorio:

- PR-AUC Test.

Metricas secundarias:

- Brier Score;
- Log Loss;
- Lift@Top20%;
- Calibration by bins.

---

## 10. Criterios Minimos de Aprovacao

O Baseline In-Game V1 so deve ser considerado aprovado se atender aos criterios no conjunto de teste:

1. `ROC-AUC Test > 0.55`.
2. `PR-AUC Test > prevalence_test + 0.03`.
3. Nenhuma feature proibida foi usada.
4. Split temporal foi documentado.
5. Snapshot foi validado sem eventos apos cutoff.
6. Imputacao/codificacao foram ajustadas somente no treino.
7. Baseline nulo foi reportado.

Criterio probabilistico auxiliar:

- Brier Score do modelo deve ser menor ou igual ao Brier Score do baseline nulo;
- Log Loss do modelo deve ser menor ou igual ao Log Loss do baseline nulo.

Se ROC/PR passarem, mas Brier/Log Loss piorarem, o status deve ser:

- `APTO COM RESSALVAS`.

Se ROC/PR falharem:

- `NAO APROVADO`.

---

## 11. Comparacoes Obrigatorias

### Comparacao com baseline nulo

Obrigatoria.

O relatorio deve mostrar:

- modelo vs baseline nulo em ROC-AUC;
- modelo vs baseline nulo em PR-AUC;
- modelo vs baseline nulo em Brier Score;
- modelo vs baseline nulo em Log Loss;
- modelo vs baseline nulo em Lift@Top20%.

### Comparacao com Baseline 1A Pre-Match

Obrigatoria como referencia externa, mas nao como criterio oficial unico.

Referencia Baseline 1A:

- ROC-AUC Test: 0.4910.
- PR-AUC Test: 0.5364.

Interpretacao:

- O Baseline In-Game V1 deve idealmente superar o Baseline 1A.
- Entretanto, a aprovacao oficial continua baseada nos criterios do proprio experimento e no baseline nulo.
- A comparacao deve deixar claro que os momentos de disponibilidade sao diferentes: pre-jogo vs minuto 75.

---

## 12. Validacoes Quantitativas Obrigatorias

Antes de qualquer treino:

- dataset filtrado deve conter apenas `cutoff_minute = 75`;
- 1 linha por `match_id`;
- target nao nulo;
- features obrigatorias presentes;
- nenhuma feature fora da whitelist em `X`;
- nenhuma coluna target-derived em `X`;
- nenhuma estatistica final da partida em `X`;
- nenhuma feature pre-jogo em `X`;
- nenhuma feature H1/H2/H8 em `X`;
- nenhuma evidencia de evento apos 75 usado em feature.

Durante split:

- split temporal por `match_date`;
- sem shuffle;
- sem sobreposicao de `match_id`;
- prevalencia por split;
- positivos/negativos por split.

Durante avaliacao:

- ROC-AUC calculado apenas se houver duas classes no split;
- PR-AUC comparado contra prevalencia do split;
- Brier/Log Loss comparados contra baseline nulo;
- Lift@Top20% reportado com tamanho do bucket;
- calibracao por bins reportada.

---

## 13. Riscos Metodologicos

### Risco 1 - Cutoff 75 tem baixa antecedencia operacional

Mitigacao:

- aceitar o risco no V1 para maximizar clareza metodologica;
- comparar cutoffs anteriores em V2 futuro.

### Risco 2 - Snapshot contaminado por eventos apos cutoff

Mitigacao:

- usar dataset V1B ja construido com regra de cutoff;
- auditar que features foram calculadas apenas com `minute <= 75`.

### Risco 3 - Target equivalente incorreto

Mitigacao:

- validar equivalencia entre `target_goal_after_cutoff` no cutoff 75 e `target_late_goal_75`.

### Risco 4 - Overfitting por amostra pequena

Mitigacao:

- manter modelo simples;
- reportar validacao e teste separadamente;
- nao avançar para backtesting sem cumprir criterios minimos.

### Risco 5 - Mistura indevida com pre-jogo

Mitigacao:

- whitelist fechada apenas com features H6/H9 in-game.

---

## 14. Escopo do Baseline In-Game V1

Permitido:

- cutoff unico em 75;
- apenas H6/H9;
- apenas 4 features aprovadas;
- baseline nulo;
- modelo simples futuro, se aprovado;
- split temporal 60/20/20;
- relatorio completo de metricas e anti-leakage.

Nao permitido:

- multiplos cutoffs no V1;
- features pre-jogo;
- H1/H2/H8;
- match_graph/momentum;
- xG/xGA/forecast;
- estatisticas finais da partida;
- backtesting;
- producao;
- thresholds decisorios operacionais.

---

## 15. Baseline In-Game V2 Futuro

Ideia aprovada para etapa futura:

- comparar multiplos cutoffs.

Cutoffs candidatos:

- 60;
- 65;
- 70;
- 75.

Objetivo do V2:

- medir trade-off entre antecedencia operacional e ganho informacional.

Hipotese operacional:

- cutoff 75 tende a ter mais informacao e possivelmente melhor performance;
- cutoffs 60/65/70 tendem a ser mais uteis operacionalmente, mas podem ter menor sinal;
- a comparacao deve mostrar em qual minuto o ganho informacional passa a ser relevante.

Regras para o V2 futuro:

- cada cutoff deve ser avaliado separadamente;
- nao misturar linhas de cutoffs diferentes no mesmo treino sem desenho especifico;
- cada cutoff deve ter target `goal_after_cutoff` correspondente;
- features devem respeitar `minute <= cutoff`;
- target deve respeitar `minute > cutoff`;
- metricas e baseline nulo devem ser reportados por cutoff;
- a decisao entre cutoffs deve considerar performance e antecedencia operacional.

Status do V2:

- planejado como direcao futura;
- nao autorizado para implementacao neste documento;
- nao faz parte do Baseline In-Game V1.

---

## 16. Relatorio Esperado da Implementacao Futura

Quando a implementacao for autorizada, o relatorio deve conter:

1. resumo executivo;
2. objetivo;
3. arquivos de entrada;
4. filtro de cutoff aplicado;
5. validacao do snapshot;
6. features usadas;
7. features proibidas verificadas;
8. auditoria final das colunas de `X`;
9. target utilizado;
10. comparacao `target_goal_after_cutoff` vs `target_late_goal_75`;
11. split temporal;
12. imputacao/codificacao;
13. baseline nulo;
14. metricas por split;
15. comparacao com baseline nulo;
16. comparacao externa com Baseline 1A;
17. calibracao;
18. Lift@Top20%;
19. decisao final;
20. limitacoes;
21. recomendacoes.

---

## Decisao Quant

O plano do Baseline In-Game V1 esta definido como:

- In-Game Only.
- Cutoff unico: 75.
- H6 + H9.
- Target: `target_late_goal_75`, operacionalizado por `target_goal_after_cutoff` no cutoff 75.
- Features: `score_diff_home_until_cutoff`, `score_state_group`, `cards_until_cutoff`, `substitutions_until_cutoff`.
- Split temporal 60/20/20.
- Metricas principais: ROC-AUC e PR-AUC.
- Criterios minimos: ROC-AUC Test > 0.55 e PR-AUC Test > prevalence_test + 0.03.

Status:

- PRONTO PARA REVISAO DO PM.
- IMPLEMENTACAO AINDA BLOQUEADA.
