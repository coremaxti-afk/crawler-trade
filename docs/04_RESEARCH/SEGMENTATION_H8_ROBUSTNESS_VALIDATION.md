# SEGMENTATION H8 ROBUSTNESS VALIDATION

## Status

Plano metodologico de validacao de robustez.

Nao contem codigo.

Nao executa modelo.

Nao executa baseline.

Nao executa backtesting.

Nao cria producao.

---

## 1. Contexto

A validacao Segmentacao x H8 foi concluida e documentada em:

- `docs/04_RESEARCH/SEGMENTATION_H8_INTERACTION_RESULTS.md`

Commit de referencia:

- `9ec35320ce9dc543712acb3dfffdd24974e50b2a`

Resultado principal:

### PROMISSOR

- `defensivo_fragile + shots_last_10m`
- N = 52
- taxa = 65.4%
- diff = +15.4 p.p.
- OR = 2.10
- p = 0.0224

### OBSERVAR

- `ofensivo_forte_vs_defesa_fragil + shots_last_10m`
- N = 20
- taxa = 75.0%
- diff = +25.0 p.p.
- p = 0.0353
- classificacao: OBSERVAR por amostra pequena

Decisao PM:

- Autorizar validacao de robustez controlada.

---

## 2. Objetivo

Verificar se os sinais encontrados na validacao Segmentacao x H8 sao robustos ou se dependem de poucos jogos, cutoff especifico ou instabilidade temporal.

Perguntas principais:

1. O efeito permanece nos cutoffs 60, 65 e 70?
2. O efeito e sensivel ao cutoff?
3. O resultado depende de poucos jogos?
4. O efeito se mantem em blocos temporais diferentes?
5. Existe evidencia suficiente para manter a frente Segmentacao x H8 como prioridade?

---

## 3. Escopo Fechado

Esta validacao deve avaliar somente as seguintes interacoes:

### Interacao 1

```text
defensivo_fragile + shots_last_10m
```

### Interacao 2

```text
ofensivo_forte_vs_defesa_fragil + shots_last_10m
```

Cutoffs permitidos:

- 60
- 65
- 70

Nao avaliar cutoff 75 nesta etapa.

Nao expandir combinacoes.

Nao adicionar novas features H8.

Nao adicionar novos segmentos.

---

## 4. Target

Target principal:

```text
target_late_goal_75
```

O target permanece fixo para medir antecedencia operacional.

Observacao:

- cutoff 60 mede sinal ate 60 para gol apos 75.
- cutoff 65 mede sinal ate 65 para gol apos 75.
- cutoff 70 mede sinal ate 70 para gol apos 75.

---

## 5. Inputs Esperados

Fontes esperadas:

- `data/processed/datasets/team_profile_segment_dataset_v1.csv`
- `data/processed/features/h8_features_v1.csv`
- `data/processed/datasets/late_goal_dataset_v1.csv`, se necessario para auditoria de target

Documentos de referencia:

- `docs/04_RESEARCH/SEGMENTATION_H8_INTERACTION_PLAN.md`
- `docs/04_RESEARCH/SEGMENTATION_H8_INTERACTION_RESULTS.md`
- `docs/04_RESEARCH/TEAM_PROFILE_SEGMENTATION_RESULTS.md`
- `docs/04_RESEARCH/H8_FEATURE_CATALOG_V1.md`

---

## 6. Definicao Operacional das Interacoes

### 6.1 defensivo_fragile + shots_last_10m

Uma partida entra na interacao quando:

```text
defensivo_fragile == 1
E
shots_last_10m esta em nivel alto no cutoff avaliado
```

A definicao de `defensivo_fragile` deve vir do Team Profile Segment Dataset V1.

A definicao de `shots_last_10m` deve vir do H8 Feature Builder V1 no respectivo cutoff.

### 6.2 ofensivo_forte_vs_defesa_fragil + shots_last_10m

Uma partida entra na interacao quando:

```text
ofensivo_forte_vs_defesa_fragil == 1
E
shots_last_10m esta em nivel alto no cutoff avaliado
```

---

## 7. Definicao de shots_last_10m Alto

A regra preferencial deve ser a mesma usada na validacao Segmentacao x H8 original.

Caso o relatorio original tenha usado quartil superior, manter:

```text
shots_last_10m_high = top 25% dentro do cutoff
```

Regra anti-leakage:

- o threshold de alta pressao deve ser calculado sem usar o target;
- preferencialmente por cutoff;
- sem usar eventos apos o cutoff;
- sem usar estatisticas finais da partida.

Se o threshold for calculado na amostra completa por ser analise exploratoria, isso deve ser explicitamente registrado como limitacao e nao pode ser reaproveitado em baseline/modelagem futura.

---

## 8. Metricas Obrigatorias

Para cada interacao e cutoff:

- N partidas.
- positivos.
- negativos.
- taxa de ocorrencia do target.
- taxa geral da amostra comparavel.
- diferenca em pontos percentuais.
- odds ratio.
- intervalo de confianca de 95% para odds ratio.
- p-value.

Comparacao:

```text
interacao = 1
vs
restante da amostra elegivel do mesmo cutoff
```

---

## 9. Validacao de Estabilidade por Cutoff

Para cada interacao, reportar:

| Cutoff | N | Taxa | Diff p.p. | OR | p-value | Classe |
|---:|---:|---:|---:|---:|---:|---|

Criterio de estabilidade:

### Estavel

- efeito positivo em pelo menos 2 dos 3 cutoffs;
- pelo menos 1 cutoff com p-value < 0.10;
- nenhum cutoff com efeito fortemente negativo.

### Instavel

- efeito positivo em apenas 1 cutoff;
- inversao de sinal em cutoff adjacente;
- amostra pequena demais em todos os cutoffs.

---

## 10. Validacao de Dependencia de Poucos Jogos

Para cada interacao:

Reportar:

- lista de partidas positivas, se possivel em anexo ou tabela resumida;
- concentracao por time;
- maximo de partidas por time dentro da interacao;
- proporcao dos positivos explicada pelos 3 times mais frequentes;
- sensibilidade removendo o time mais frequente, se viavel.

Criterio de alerta:

```text
mais de 40% dos positivos concentrados em ate 2 times
```

ou

```text
N < 30 em todos os cutoffs
```

---

## 11. Validacao de Robustez Temporal

Dividir a temporada elegivel em blocos temporais simples:

- bloco inicial elegivel;
- bloco intermediario;
- bloco final.

Para cada bloco:

- N da interacao;
- positivos;
- taxa;
- diferenca vs taxa do bloco.

Criterio de estabilidade temporal:

- efeito positivo em pelo menos 2 blocos;
- nao depender exclusivamente de um unico bloco.

Se a amostra ficar pequena demais, registrar como:

```text
NAO CONCLUSIVO POR AMOSTRA
```

---

## 12. Criterios de Classificacao

### PROMISSOR ROBUSTO

Todos:

- N >= 30 em pelo menos 2 cutoffs;
- diff >= +8 p.p. em pelo menos 2 cutoffs;
- OR > 1.50 em pelo menos 2 cutoffs;
- p-value < 0.10 em pelo menos 1 cutoff;
- sem dependencia extrema de poucos jogos/times;
- sinal positivo em pelo menos 2 blocos temporais, quando avaliavel.

### OBSERVAR

Qualquer:

- efeito alto mas N pequeno;
- efeito positivo em apenas 1 cutoff;
- p-value fraco, mas direcao coerente;
- estabilidade temporal inconclusiva por amostra.

### DESCARTAR

Qualquer:

- efeito desaparece nos cutoffs alternativos;
- efeito negativo ou proximo de zero;
- sinal depende claramente de poucos jogos;
- N insuficiente e sem consistencia.

---

## 13. Regras Anti-Leakage

Obrigatorias:

- segmentacao historica deve usar somente jogos anteriores a partida analisada.
- H8 deve usar somente eventos com `minute <= cutoff`.
- `shots_last_10m` deve respeitar a janela anterior ao cutoff.
- target deve ser usado somente como resposta.
- nenhum evento apos cutoff pode entrar nas features.
- nenhuma estatistica full-match da partida analisada pode entrar como feature.
- nenhuma coluna target-derived pode entrar como feature.
- nenhum placar final pode entrar como feature.

---

## 14. Resultado Esperado

Documento final esperado apos execucao futura:

- `docs/04_RESEARCH/SEGMENTATION_H8_ROBUSTNESS_VALIDATION_RESULTS.md`

O relatorio deve conter:

1. Resumo executivo.
2. Metodologia.
3. Fontes usadas.
4. Confirmacao anti-leakage.
5. Resultado por interacao e cutoff.
6. Analise de dependencia de poucos jogos.
7. Analise de robustez temporal.
8. Classificacao final:
   - PROMISSOR ROBUSTO
   - OBSERVAR
   - DESCARTAR
9. Recomendacao da proxima etapa.

---

## 15. Decisao Quant

A validacao de robustez esta autorizada metodologicamente com escopo fechado.

Status:

```text
PRONTO PARA EXECUCAO CONTROLADA PELO CODEX
```

Restricoes mantidas:

- Nao criar modelo.
- Nao executar baseline.
- Nao fazer backtesting.
- Nao criar producao.
- Nao expandir combinacoes.
