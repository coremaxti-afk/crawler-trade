# PROJECT STATUS

## Estado Atual do Projeto

FASE ATUAL:

```text
VALIDACAO MULTI-TEMPORADA PRE-RANKING OPERACIONAL
```

O projeto concluiu as 5 frentes exploratorias da Serie A 2025 e agora deve validar fora da amostra os principais achados antes de construir o `RANKING_OPERACIONAL_FINAL_V1`.

O objetivo agora nao e aprovar operacao final. O objetivo e verificar quais padroes descobertos em 2025 sobrevivem em outras temporadas.

---

## Governanca obrigatoria

Documento oficial:

```text
docs/00_AGENTS/GOVERNANCE_V2.md
```

Regra central ativa:

```text
Nenhum agente deve concordar com o usuario apenas para agradar.
```

Se uma solicitacao pular etapas, misturar objetivos, fragilizar a metodologia ou gerar falsa confianca operacional, o agente deve discordar primeiro, explicar o risco tecnico e propor o caminho correto.

---

## Roadmap Exploratorio Serie A 2025 — Concluido

Ordem executada:

```text
1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
2. ANALISE_REGIME_POR_FASE_V1
3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1
```

---

## Frentes concluidas

### 1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1

Status:

```text
APROVADA COMO V1 EXPLORATORIA
```

Documento:

```text
docs/04_RESEARCH/agrupamento_por_familia_e_variacoes_v1/AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

Achado principal:

```text
18 familias
714 variacoes
18 familias com alta sobreposicao
overlap maximo por fixture = 100% em todas as familias
```

Decisao metodologica:

```text
Nao somar lucro de variacoes da mesma familia como se fossem estrategias independentes.
Manter variacoes disponiveis para proximas frentes, mas considerar alertas de overlap.
```

### 2. ANALISE_REGIME_POR_FASE_V1

Status:

```text
APROVADA COMO V1 EXPLORATORIA
```

Documento:

```text
docs/04_RESEARCH/analise_regime_por_fase_v1/ANALISE_REGIME_POR_FASE_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

Achados principais:

```text
Goal / Over:
- negativo em todas as fases no phase6
- negativo em todas as fases no phase8
- nao houve fase claramente lucrativa para Over

No Goal / Under:
- positivo em todas as fases no phase6
- positivo em todas as fases no phase8
- melhor bloco phase6: fase 4
- melhor bloco phase8: fase 5
```

### 3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1

Status:

```text
APROVADA COMO V1 EXPLORATORIA
```

Documento:

```text
docs/04_RESEARCH/analise_maturidade_liga_por_rodada_v1/ANALISE_MATURIDADE_LIGA_POR_RODADA_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

Achados principais:

```text
A liga geral pode enganar porque mistura Goal ruim com No Goal bom.
Goal / Over continua ruim mesmo removendo rodadas iniciais.
No Goal / Under permanece positivo desde a primeira rodada testada.
As melhores familias No Goal amadurecem cedo.
Nao apareceu evidencia de que esperar ate rodada 10 melhora significativamente as melhores familias No Goal.
```

Ressalva:

```text
A V1 testou apenas rodadas 5 a 12.
Ela mostra que rodada 5 ja funciona para No Goal, mas nao prova que a maturidade comeca exatamente na rodada 5.
```

### 4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1

Status:

```text
APROVADA COMO V1 EXPLORATORIA COM RESSALVA DE INTERPRETACAO
```

Documento:

```text
docs/04_RESEARCH/analise_forca_favorito_por_estrategia_v1/ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

Achados principais:

```text
A forca do favorito importa.
As melhores familias No Goal parecem mais fortes em jogos parelhos/sem favorito claro.
Goal nao ficou lucrativo no agregado em nenhum segmento.
Algumas familias Goal geraram hipoteses segmentadas, mas ainda com risco de overfitting.
both_teams_cold_2of3 parece especialmente interessante em jogos parelhos.
favorite_winning_by_1_opp_cold_2of3 teve resultado contraintuitivo: melhor em jogo parelho do que em favorito forte.
```

Ressalva de interpretacao:

```text
Goal nao passou a funcionar no agregado.
Algumas familias Goal ficaram menos negativas ou pontualmente positivas em segmentos especificos.
```

### 5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1

Status:

```text
APROVADA COMO V1_1 EXPLORATORIA
```

Documento:

```text
docs/04_RESEARCH/analise_padroes_prejuizo_por_time_v1_1/ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

Achados principais:

```text
A V1.1 corrigiu a V1 ao focar apenas em familias No Goal lucrativas.
O problema nao e apenas o time isolado, mas time + contexto + familia.
O perfil mais forte de prejuizo No Goal foi FAVORITO_MEDIO_DOMINANTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA.
São Paulo, Internacional e Botafogo sao os principais alertas exploratorios.
Nenhum time deve ser excluido automaticamente com base nesta etapa.
```

---

## Hipoteses congeladas para validacao multi-temporada

As hipoteses abaixo devem ser testadas fora da amostra antes do ranking operacional final:

```text
1. Familias No Goal sao superiores a Goal/Over no agregado.
2. No Goal e lucrativo em varias fases da temporada.
3. As melhores familias No Goal amadurecem cedo.
4. Jogos parelhos/sem favorito claro parecem favorecer as melhores familias No Goal.
5. Favorito medio dominante + prejuizo distribuido + multi-familia aparece como perfil recorrente de risco.
6. Alguns times sao contraditorios: bons para uma familia e ruins para outra.
7. A selecao final deve considerar familia + contexto + time, e nao apenas estrategia isolada.
```

---

## Frente atual

```text
VALIDACAO_MULTI_TEMPORADA_V1
```

Objetivo:

```text
Validar se os padroes descobertos na Serie A 2025 sobrevivem em outras temporadas antes de construir o RANKING_OPERACIONAL_FINAL_V1.
```

Pergunta principal:

```text
Quais achados de 2025 continuam validos fora da amostra?
```

Temporadas/escopo a definir conforme dados disponiveis.

---

## Roadmap a partir de agora

```text
1. VALIDACAO_MULTI_TEMPORADA_V1
2. COMPARACAO_PADROES_2025_VS_OUTRAS_TEMPORADAS_V1
3. RANKING_OPERACIONAL_FINAL_V1
4. VALIDACAO_OPERACIONAL_FINAL_V1
5. PLAYBOOK_OPERACIONAL_FINAL
```

---

## Politica Oficial de Odds

O projeto seguira com:

```text
SIMULACOES OPERACIONAIS BASEADAS EM ODDS MEDIAS OBSERVADAS
```

Curva operacional atual:

```text
60 = 1.50
65 = 1.60
70 = 1.80
75 = 2.00
80 = 2.45
85 = 3.35
```

Ressalva obrigatoria:

```text
Nao constitui backtesting financeiro real.
Classificar como ESTIMATIVA OPERACIONAL COM ODDS MEDIAS.
```

---

## Decisao Operacional Atual

Nenhuma estrategia, time ou filtro deve ser aprovado operacionalmente antes da validacao multi-temporada.

A escolha futura deve priorizar:

- lucro final;
- ROI;
- EV por trade;
- drawdown maximo;
- sequencia maxima de perdas;
- consistencia por temporada/fase;
- maturidade por rodada;
- contexto de favorito/equilibrio;
- perfil de prejuizo por time;
- duplicidades por familia/variacao;
- robustez multi-temporada.

---

## Restricoes

- Nao criar robo.
- Nao criar producao.
- Nao chamar simulacao com odds medias de backtesting financeiro real.
- Nao usar odds live inexistentes.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao aprovar operacao final durante etapa exploratoria ou validacao multi-temporada.
