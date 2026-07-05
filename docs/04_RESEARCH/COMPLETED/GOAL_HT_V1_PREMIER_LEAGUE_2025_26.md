# GOAL HT V1 — Pesquisa de Gol no Primeiro Tempo

Status: **pesquisa concluída com mapa financeiro estimado**  
Liga/temporada: **Premier League 2025/26**  
Escopo: **gol ou não-gol do cutoff até o intervalo**  
Uso: **pesquisa, não operação real**

Este documento consolida a frente **GOAL HT V1**. Ele explica as perguntas que o projeto responde, a metodologia, os critérios de seleção e a leitura financeira final.

---

## 1. Perguntas que o projeto responde

### Pergunta principal

Depois de um cutoff do primeiro tempo, existe algum padrão observável que gere lucro estimado em mercados de **Goal HT** ou **No Goal HT** até o intervalo?

### Perguntas secundárias

1. Quais sinais sobrevivem depois de corrigir membership, cutoff e sobreposição?
2. Quais recortes geram lucro estimado com odds médias?
3. Quais recortes são apenas refinamentos contextuais de um recorte maior?
4. Quais candidatos não podem ser somados por pegarem os mesmos fixtures?
5. O estudo chegou a operação real ou apenas a um mapa de pesquisa?

### O que o projeto não responde

1. Não prova execução real em mercado live.
2. Não valida liquidez, spread, delay, suspensão ou slippage.
3. Não usa odds reais fixture a fixture.
4. Não testa cashout.
5. Não cria robô, staking ou deploy.
6. Não valida outras ligas/temporadas.

---

## 2. Definição do mercado pesquisado

| Item | Definição |
| --- | --- |
| GOAL | Back Over HT após cutoff até o intervalo |
| NO_GOAL | Lay Over HT após cutoff até o intervalo |
| Cutoffs | 15, 20, 25, 30, 35, 40 |
| Unidade | Fixture/candidato |
| Stake GOAL | R$ 100 fixos |
| Responsabilidade NO_GOAL | R$ 100 fixos |
| Odds | Médias por cutoff, não odds reais |

### Odds médias usadas

| Cutoff | Odd média Over HT |
| ---: | ---: |
| 15 | 1.64 |
| 20 | 1.77 |
| 25 | 1.96 |
| 30 | 2.21 |
| 35 | 2.78 |
| 40 | 3.73 |

---

## 3. Metodologia resumida

1. Reconstrução da base do primeiro tempo.
2. Expansão fixture-cutoff para 15/20/25/30/35/40.
3. Criação de targets pós-cutoff até o intervalo.
4. Construção de estratégias candidatas.
5. Correção de membership oficial.
6. Validação financeira com odds médias.
7. Auditoria de candidatos, observações e bloqueios.
8. Deduplicação por família macro.
9. Frentes contextuais de favoritismo e placar.
10. Auditoria fixture-level entre frentes.
11. Seleção global sem excluir sobreposições.

---

## 4. Critérios de decisão

Um recorte só pode virar representante ou refinamento relevante se passar por critérios financeiros e metodológicos.

| Critério | Uso |
| --- | --- |
| N | Evitar leitura forte com amostra pequena |
| Lucro | Métrica central do projeto |
| ROI | Eficiência sobre exposição |
| EV por entrada | Lucro médio esperado por entrada estimada |
| Drawdown | Risco de queda acumulada |
| Sequência negativa | Risco operacional teórico |
| Sensibilidade | Robustez contra variação de odds |
| Fixture overlap | Impede soma indevida |
| Família macro | Evita múltiplos oficiais da mesma origem |

Regra central: **lucro e risco financeiro mandam, mas sem dedup por fixture não existe carteira**.

---

## 5. Representantes globais finais

Estes são os três representantes globais do mapa final. Eles não formam carteira e não devem ser somados.

| Candidato | Lado | Cutoff | Contexto | N | Lucro | ROI | DD |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: |
| QPP35 | GOAL | 35 | Geral | 31 | R$ 1.904,00 | 61,4% | R$ -200,00 |
| AQUEC40_FAV | GOAL | 40 | Parelho | 20 | R$ 984,00 | 49,2% | R$ -354,00 |
| BQR35 | NO_GOAL | 35 | Geral | 44 | R$ 597,75 | 13,6% | R$ -300,00 |

### Leitura rápida

- **QPP35** é o melhor representante por equilíbrio entre N, lucro, ROI e drawdown.
- **AQUEC40_FAV** é forte em ROI, mas tem N menor e deve ficar com ressalva.
- **BQR35** é o representante mais conservador de NO_GOAL por N maior, mas tem ROI moderado.

---

## 6. Métricas financeiras dos representantes

| Candidato | Wins | Losses | Hit | Odd | EV | Edge | Seq. neg. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| QPP35 | 18 | 13 | 58,1% | 2.78 | R$ 61,42 | +22,1 pp | 2 |
| AQUEC40_FAV | 8 | 12 | 40,0% | 3.73 | R$ 49,20 | +13,2 pp | n/d |
| BQR35 | 32 | 12 | 72,7% | 2.78 | R$ 13,59 | +8,7 pp | 3 |

Observação: `n/d` indica que a sequência negativa não ficou consolidada no relatório final recebido. O DD foi preservado porque é mais importante para leitura de risco.

---

## 7. Sensibilidade financeira conhecida

| Candidato | Base lucro | Base ROI | Odd -10% lucro | Odd -10% ROI | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| QPP35 | R$ 1.904,00 | 61,4% | R$ 1.403,60 | 45,3% | Forte |
| AQUEC40_FAV | R$ 984,00 | 49,2% | n/d | n/d | Não consolidado |
| BQR35 | R$ 597,75 | 13,6% | R$ 930,49 | 21,1% | Forte |

Para Lay NO_GOAL, a queda da odd melhora o lucro potencial do lado vencedor, por isso BQR35 melhora no cenário de odd menor.

---

## 8. Refinamentos preservados

Os refinamentos abaixo não foram excluídos. Eles ajudam leitura contextual, mas não são estratégias independentes.

| Refinamento | Pai | N | ROI | Lucro | DD | Soma? |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| QPP35_SCORE | QPP35 | 21 | 72,1% | R$ 1.514,00 | R$ -200,00 | Não |
| AQUEC40_ORIG | AQUEC40_FAV | 30 | 24,3% | R$ 730,00 | R$ -754,00 | Não |
| BQR35_FAV | BQR35 | 24 | 17,1% | R$ 411,24 | R$ -243,82 | Não |
| BQR40_FAV | BQR35 | 20 | 16,1% | R$ 322,71 | R$ -100,00 | Não |
| BQR35_SCORE | BQR35 | 30 | 14,5% | R$ 435,96 | R$ -243,82 | Não |

---

## 9. Pares que não podem ser somados

| Grupo | Pares bloqueados para soma | Motivo |
| --- | --- | --- |
| QPP | QPP35 + QPP35_SCORE | Score é subconjunto do original |
| AQUEC | AQUEC40_ORIG + AQUEC40_FAV | Favoritismo é subconjunto do original |
| BQR | BQR35 + BQR35_FAV | Favoritismo é subconjunto do original |
| BQR | BQR35 + BQR40_FAV | Variação contextual/cutoff dentro da mesma família |
| BQR | BQR35 + BQR35_SCORE | Score é subconjunto do original |
| BQR | BQR35_FAV + BQR35_SCORE | Sobreposição moderada |
| BQR | BQR40_FAV + BQR35_SCORE | Sobreposição moderada |

---

## 10. Critérios de bloqueio

| Item | Status | Motivo |
| --- | --- | --- |
| AQUECIMENTO_FRACO | Bloqueado | Membership original não reconstruído |
| Agregado Etapa 8 | Informativo | Contaminado por sobreposição |
| Recortes N 12-19 | Observação | N baixo para candidato principal |
| Recortes sensibilidade negativa | Frágil | Perdem robustez com odd -10% |
| ROI global/carteira | Não aprovado | Exige dedup por fixture |

---

## 11. Limitações críticas

1. Resultados usam odds médias, não odds reais fixture a fixture.
2. Não há liquidez, spread, delay, slippage ou suspensão.
3. Não há cashout.
4. Não há robô ou operação real.
5. A amostra é apenas Premier League 2025/26.
6. Contextuais são refinamentos, não estratégias independentes.
7. Não existe ROI global aprovado.

---

## 12. Leitura final

O projeto GOAL HT V1 respondeu que existem três famílias promissoras no primeiro tempo:

1. **QPP35 GOAL**: melhor candidato geral pelo lucro estimado e drawdown baixo.
2. **AQUEC40 GOAL em jogo parelho**: refinamento forte em ROI, mas com N menor.
3. **BQR35 NO_GOAL**: candidato conservador para ausência de gol até o intervalo.

A conclusão é de pesquisa: há sinais com lucro estimado, mas ainda não há validação operacional.

---

## 13. Próximos projetos separados

1. Odds reais fixture a fixture.
2. Dedup operacional por fixture.
3. Janelas recentes 5/10/15.
4. Discovery por nova liga/temporada.
5. Teste com liquidez, spread, delay e slippage.

Nenhum desses deve ser misturado dentro deste fechamento.
