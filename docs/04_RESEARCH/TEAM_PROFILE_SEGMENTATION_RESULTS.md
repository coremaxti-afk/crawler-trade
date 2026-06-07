# Team Profile Segmentation Results

## Status

Validacao estatistica formal dos segmentos do `Team Profile Segment Dataset V1`.

Nao contem modelo.

Nao contem baseline.

Nao contem backtesting.

Nao contem producao.

---

## 1. Resumo Executivo

A validacao estatistica formal dos segmentos foi executada sobre o dataset versionado:

- `data/processed/datasets/team_profile_segment_dataset_v1.csv`

Target:

- `target_late_goal_75`

Resultado Quant:

```text
APROVADO COMO ANALISE EXPLORATORIA FORMAL
NAO APROVADO PARA MODELO
NAO APROVADO PARA BASELINE
NAO APROVADO PARA BACKTESTING
NAO APROVADO PARA PRODUCAO
```

Conclusao principal:

- Nenhum segmento atingiu criterio estatistico forte suficiente para ser classificado como `PROMISSOR` na validacao formal do dataset versionado.
- O segmento com maior efeito positivo foi `ofensivo_forte_vs_defesa_fragil`.
- O segmento `ambos_defesa_forte` nao apresentou evidencia robusta; o resultado anterior parece mais provavel ser artefato de amostra/cutoff do que sinal estavel.
- A segmentacao segue util como frente exploratoria, mas nao deve avancar diretamente para baseline.

---

## 2. Dataset Validado

Fonte:

- `Team Profile Segment Dataset V1`

Validacoes ja confirmadas:

- 380 partidas.
- 380 partidas unicas.
- 0 duplicatas.
- `target_late_goal_75` unido corretamente.
- 0 nulos no target.
- 0 divergencias no target.
- target preservado: 189 positivos / 191 negativos.
- 330 partidas elegiveis por perfil.
- 320 partidas segmentaveis.
- 0 violacoes temporais.
- 0 target-derived features em X.
- 0 colunas proibidas em X.
- 0 full-match columns.

Taxa geral do target:

```text
189 / 380 = 49.7%
```

---

## 3. Metodologia

Para cada segmento binario materializado no dataset, foi comparado:

```text
partidas dentro do segmento
vs
partidas fora do segmento
```

Para cada segmento foram calculados:

- N partidas.
- Positivos.
- Negativos.
- Taxa de ocorrencia do target.
- Diferenca em pontos percentuais contra a taxa geral.
- Odds ratio contra o restante da amostra.
- Intervalo de confianca aproximado de 95% para odds ratio.
- p-value por teste exato de Fisher.

Tabela 2x2 usada:

```text
                 target=1   target=0
segmento=1          a          b
segmento=0          c          d
```

Odds ratio:

```text
OR = (a * d) / (b * c)
```

---

## 4. Criterios de Classificacao

### PROMISSOR

Segmento com:

- N >= 30;
- diferenca positiva >= 5 p.p.;
- p-value < 0.10;
- odds ratio > 1.0.

### OBSERVAR

Segmento com:

- efeito positivo >= 3 p.p., mas significancia fraca; ou
- efeito positivo >= 5 p.p. com N pequeno ou p-value fraco; ou
- segmento metodologicamente relevante para monitoramento.

### DESCARTAR

Segmento com:

- efeito fraco;
- efeito negativo;
- amostra pequena sem sinal;
- p-value sem suporte estatistico.

---

## 5. Ranking Completo dos Segmentos

| Rank | Segmento | N | Pos | Neg | Taxa seg. | Taxa geral | Dif. p.p. | OR | IC 95% OR | p-value | Classe |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---|
| 1 | ofensivo_forte_vs_defesa_fragil | 56 | 32 | 24 | 57.1% | 49.7% | +7.4 | 1.42 | 0.80 - 2.51 | 0.2492 | OBSERVAR |
| 2 | sem_ofensivo_forte_sem_defesa_fragil | 43 | 23 | 20 | 53.5% | 49.7% | +3.7 | 1.18 | 0.63 - 2.24 | 0.6302 | OBSERVAR |
| 3 | ambos_defesa_forte | 30 | 16 | 14 | 53.3% | 49.7% | +3.6 | 1.17 | 0.55 - 2.47 | 0.7077 | OBSERVAR |
| 4 | ao_menos_uma_defesa_fragil | 163 | 83 | 80 | 50.9% | 49.7% | +1.2 | 1.09 | 0.72 - 1.63 | 0.7559 | DESCARTAR |
| 5 | ao_menos_um_ofensivo_forte | 177 | 88 | 89 | 49.7% | 49.7% | -0.0 | 1.00 | 0.67 - 1.49 | 1.0000 | DESCARTAR |
| 6 | ofensivo_fraco_vs_defesa_forte | 52 | 25 | 27 | 48.1% | 49.7% | -1.7 | 0.93 | 0.52 - 1.66 | 0.8816 | DESCARTAR |
| 7 | defesa_fragil_vs_defesa_fragil | 26 | 12 | 14 | 46.2% | 49.7% | -3.6 | 0.86 | 0.39 - 1.91 | 0.8395 | DESCARTAR |
| 8 | ofensivo_forte_vs_ofensivo_forte | 27 | 12 | 15 | 44.4% | 49.7% | -5.3 | 0.80 | 0.36 - 1.75 | 0.6905 | DESCARTAR |

---

## 6. Segmentos PROMISSOR

Nenhum segmento foi classificado como `PROMISSOR` nesta validacao formal.

Motivo:

- O maior efeito positivo foi `ofensivo_forte_vs_defesa_fragil`, com +7.4 p.p., mas p-value = 0.2492 e intervalo de confianca do OR cruzando 1.
- Nenhum segmento combinou efeito relevante com suporte estatistico suficiente.

---

## 7. Segmentos OBSERVAR

### 7.1 ofensivo_forte_vs_defesa_fragil

Resultado:

- N: 56.
- Positivos: 32.
- Taxa: 57.1%.
- Diferenca: +7.4 p.p.
- OR: 1.42.
- IC 95% OR: 0.80 - 2.51.
- p-value: 0.2492.

Classificacao:

```text
OBSERVAR
```

Interpretacao:

- E o segmento com maior efeito observado.
- A direcao e coerente com a hipotese original.
- A significancia ainda e insuficiente.
- Deve ser mantido como principal candidato exploratorio em futuras temporadas/amostras.

### 7.2 sem_ofensivo_forte_sem_defesa_fragil

Resultado:

- N: 43.
- Positivos: 23.
- Taxa: 53.5%.
- Diferenca: +3.7 p.p.
- OR: 1.18.
- IC 95% OR: 0.63 - 2.24.
- p-value: 0.6302.

Classificacao:

```text
OBSERVAR
```

Interpretacao:

- Efeito positivo pequeno.
- Significancia fraca.
- Deve ser mantido apenas como controle exploratorio, nao como candidato principal.

### 7.3 ambos_defesa_forte

Resultado:

- N: 30.
- Positivos: 16.
- Taxa: 53.3%.
- Diferenca: +3.6 p.p.
- OR: 1.17.
- IC 95% OR: 0.55 - 2.47.
- p-value: 0.7077.

Classificacao:

```text
OBSERVAR COM RESSALVA
```

Interpretacao:

- O comportamento e contraintuitivo.
- O efeito e pequeno.
- O suporte estatistico e fraco.
- O resultado anterior em cutoff especifico provavelmente foi artefato de amostra/cutoff.
- Nao deve ser usado como segmento prioritario.

---

## 8. Segmentos DESCARTAR

### 8.1 ao_menos_uma_defesa_fragil

- N alto: 163.
- Taxa: 50.9%.
- Diferenca: +1.2 p.p.
- p-value: 0.7559.

Classificacao:

```text
DESCARTAR
```

Motivo:

- Apesar da amostra grande, o efeito e muito fraco.

### 8.2 ao_menos_um_ofensivo_forte

- N: 177.
- Taxa: 49.7%.
- Diferenca: aproximadamente 0.
- p-value: 1.0000.

Classificacao:

```text
DESCARTAR
```

Motivo:

- Nao ha efeito observavel.

### 8.3 ofensivo_fraco_vs_defesa_forte

- N: 52.
- Taxa: 48.1%.
- Diferenca: -1.7 p.p.
- OR: 0.93.
- p-value: 0.8816.

Classificacao:

```text
DESCARTAR
```

Motivo:

- Efeito fraco e negativo.

### 8.4 defesa_fragil_vs_defesa_fragil

- N: 26.
- Taxa: 46.2%.
- Diferenca: -3.6 p.p.
- OR: 0.86.
- p-value: 0.8395.

Classificacao:

```text
DESCARTAR
```

Motivo:

- Amostra pequena.
- Efeito negativo.
- Sem suporte estatistico.

### 8.5 ofensivo_forte_vs_ofensivo_forte

- N: 27.
- Taxa: 44.4%.
- Diferenca: -5.3 p.p.
- OR: 0.80.
- p-value: 0.6905.

Classificacao:

```text
DESCARTAR
```

Motivo:

- Amostra pequena.
- Efeito negativo.
- Sem suporte estatistico.

---

## 9. Respostas as Perguntas Principais

### 1. Existem segmentos com frequencia anormalmente alta de gols apos 75?

Nao de forma estatisticamente consistente.

O segmento com maior taxa foi:

- `ofensivo_forte_vs_defesa_fragil`: 57.1%, +7.4 p.p.

Mas p-value = 0.2492, insuficiente para classificar como PROMISSOR.

### 2. Existem segmentos com frequencia anormalmente baixa?

Nao de forma estatisticamente consistente.

O menor segmento foi:

- `ofensivo_forte_vs_ofensivo_forte`: 44.4%, -5.3 p.p.

Mas N = 27 e p-value = 0.6905.

### 3. Quais segmentos apresentam maior efeito observado?

Ranking por diferenca positiva:

1. `ofensivo_forte_vs_defesa_fragil`: +7.4 p.p.
2. `sem_ofensivo_forte_sem_defesa_fragil`: +3.7 p.p.
3. `ambos_defesa_forte`: +3.6 p.p.
4. `ao_menos_uma_defesa_fragil`: +1.2 p.p.

### 4. O efeito e estatisticamente consistente?

Nao.

Nenhum segmento apresentou p-value < 0.10 na validacao formal do dataset versionado.

### 5. Existem segmentos inviaveis por amostra pequena?

Sim.

Segmentos com N < 30:

- `defesa_fragil_vs_defesa_fragil`: N = 26.
- `ofensivo_forte_vs_ofensivo_forte`: N = 27.

Estes segmentos nao devem ser usados como base de decisao nesta temporada.

### 6. O segmento `ambos_defesa_forte` possui comportamento real ou artefato?

A evidencia atual favorece a interpretacao de artefato.

Motivos:

- N minimo: 30.
- Efeito pequeno: +3.6 p.p.
- OR proximo de 1: 1.17.
- IC 95% cruza 1 amplamente: 0.55 - 2.47.
- p-value muito fraco: 0.7077.

Decisao Quant:

```text
MANTER EM OBSERVAR COM RESSALVA
NAO USAR COMO SEGMENTO PRIORITARIO
```

---

## 10. Riscos Metodologicos

### Risco 1 - Uma temporada apenas

A amostra de 380 partidas limita conclusoes estatisticas.

### Risco 2 - Segmentos sobrepostos

Alguns segmentos nao sao mutuamente exclusivos.

Exemplo:

- `ofensivo_forte_vs_defesa_fragil` pode tambem compor `ao_menos_um_ofensivo_forte`.

### Risco 3 - Multipla testagem

Foram avaliados multiplos segmentos.

Mesmo achados com p-value moderado deveriam ser tratados com cautela.

### Risco 4 - Segmentos pequenos

Segmentos com N < 30 sao instaveis.

### Risco 5 - Sinal anterior por cutoff nao se manteve no target fixo pos-75

A analise exploratoria anterior por cutoffs sugeriu sinais mais fortes. No dataset versionado focado em `target_late_goal_75`, o sinal ficou mais fraco.

---

## 11. Decisao Quant

```text
VALIDACAO ESTATISTICA FORMAL CONCLUIDA
```

Status dos segmentos:

```text
PROMISSOR: 0
OBSERVAR: 3
DESCARTAR: 5
```

Segmentos em OBSERVAR:

- `ofensivo_forte_vs_defesa_fragil`.
- `sem_ofensivo_forte_sem_defesa_fragil`.
- `ambos_defesa_forte` com ressalva.

Segmentos DESCARTAR:

- `ao_menos_uma_defesa_fragil`.
- `ao_menos_um_ofensivo_forte`.
- `ofensivo_fraco_vs_defesa_forte`.
- `defesa_fragil_vs_defesa_fragil`.
- `ofensivo_forte_vs_ofensivo_forte`.

---

## 12. Recomendacao da Proxima Etapa

Nao avançar para baseline de segmentacao neste momento.

Recomendacao Quant:

1. Registrar a validacao formal como inconclusiva para uso preditivo.
2. Manter `ofensivo_forte_vs_defesa_fragil` como hipotese exploratoria principal.
3. Reavaliar segmentacao apenas quando houver amostra multi-temporada.
4. Nao usar `ambos_defesa_forte` como driver prioritario.
5. Nao criar modelo, baseline, backtesting ou producao com estes segmentos nesta fase.

Proxima frente sugerida:

```text
AMPLIAR AMOSTRA MULTI-TEMPORADA
```

ou, se o PM preferir seguir apenas com a temporada atual:

```text
ENCERRAR FRENTE DE SEGMENTACAO COMO EXPLORATORIA INCONCLUSIVA
```

---

## 13. Restricoes Mantidas

- Nao criar modelo.
- Nao executar baseline.
- Nao fazer backtesting.
- Nao criar producao.
- Nao usar segmentos como sistema decisorio.
- Nao misturar segmentos com H8/H6/H9 em modelo sem nova aprovacao.
