# PROJECT STATUS

## Estado Atual do Projeto

FASE ATUAL:

```text
ANALISE EXPLORATORIA E DESCOBERTA DE PADROES PRE-RANKING OPERACIONAL
```

O projeto esta na etapa de organizar e testar padroes exploratorios antes do `RANKING_OPERACIONAL_FINAL_V1`.

O objetivo agora nao e prever diretamente a proxima temporada nem aprovar operacao final. O objetivo e descobrir padroes historicos fortes, separar duplicidades, entender regime da temporada e preparar hipoteses para validacao preditiva/operacional posterior.

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

## Roadmap Exploratorio Atual

Documento oficial:

```text
docs/04_RESEARCH/FRENTES_DE_PESQUISA_PRE_RANKING_OPERACIONAL_FINAL_V1.md
```

Ordem oficial:

```text
1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
2. ANALISE_REGIME_POR_FASE_V1
3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1
```

---

## Frentes concluidas do roadmap atual

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

Decisao metodologica:

```text
Nao corrigir agora.
O estudo respondeu a pergunta principal de regime por fase.
Seguir para ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1.
```

---

## Frente atual

```text
ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
```

Objetivo:

```text
Descobrir a partir de qual rodada os sinais da Serie A comecam a ficar confiaveis, sem misturar sinais bons com ruins.
```

Niveis obrigatorios:

```text
1. Liga geral
2. Direcao de mercado: Over/Goal/Back Over vs Under/No Goal/Lay Over
3. Familia/estrategia com todos os cutoffs/windows
```

Rodadas obrigatorias:

```text
5, 6, 7, 8, 9, 10, 11, 12
```

---

## Frentes anteriores importantes

```text
VALIDACAO_PREDITIVA_DA_ESTRATEGIA_V1_1
STATUS: APROVADA
DECISAO: base para classificacao preditiva exploratoria/operacional, mas nao substitui o roadmap atual.
```

```text
RENTABILIDADE_DAS_ESTRATEGIAS_POR_TIME_V4
STATUS: APROVADA COM PEQUENOS AJUSTES
DECISAO: usar como base para robustez por time e futura ANALISE_PADROES_PREJUIZO_POR_TIME_V1.
```

```text
STRATEGY_DRAWDOWN_TOP20_SERIE_A_2025_TEMPOS_EXPANDIDOS / DD V4 corrigido
STATUS: APROVADA
DECISAO: fonte base para lucro, ROI, drawdown, max losing streak e ordem temporal.
```

---

## Objetivos ja atingidos

- validacao semantica de SportMonks trends;
- validacao de participant_id por time;
- validacao de cutoffs 60/65/70/75;
- validacao de janelas 5/10/15 minutos;
- descoberta de estrategias por lado/time;
- integracao Football-Data para definicao de favorito;
- avaliacao financeira inicial pelo agente 06;
- criacao dos playbooks operacionais V1/V2/V3;
- identificacao de inconsistencia causada por agregacao/filtros dos playbooks;
- retorno para estrategias originais;
- criacao de auditoria de drawdown por estrategia e temporada;
- criacao da normalizacao fixture-level pre-DD;
- integracao do DD com a entrada normalizada pre-DD;
- criacao da rentabilidade por time V2/V4;
- validacao preditiva V1.1 pos-DD corrigido;
- agrupamento por familia e variacoes V1;
- analise de regime por fase V1.

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

A documentacao de playbooks V3 permanece como referencia operacional, mas a selecao de estrategias volta a usar:

```text
estrategias originais
sem filtros V3 por padrao
sem agregacao de targets
sem juntar estrategias parecidas sem agrupamento/overlap
```

A partir deste ponto, a escolha de estrategias deve priorizar:

- lucro final;
- ROI;
- EV por trade;
- drawdown maximo;
- sequencia maxima de perdas;
- consistencia por temporada/fase;
- duplicidades por familia/variacao;
- robustez por time.

---

## Proxima Frente Oficial

```text
ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
```

Depois dela:

```text
ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
ANALISE_PADROES_PREJUIZO_POR_TIME_V1
RANKING_OPERACIONAL_FINAL_V1
```

---

## Restricoes

- Nao criar robo.
- Nao criar producao.
- Nao chamar simulacao com odds medias de backtesting financeiro real.
- Nao usar odds live inexistentes.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao aprovar operacao final durante etapa exploratoria.
