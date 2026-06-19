# PROJECT STATUS

## Estado Atual do Projeto

FASE ATUAL:

```text
AUDITORIA DE RISCO DAS ESTRATEGIAS ORIGINAIS + VALIDACAO MULTI-LIGA + ROBUSTEZ POR TIME
```

Frentes encerradas:

```text
SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1/V2
STATUS: CONCLUIDO
DECISAO: APROVADO COM RESSALVAS
```

```text
SPORTMONKS_OPERATIONAL_PLAYBOOKS_V1/V2/V3
STATUS: DOCUMENTADO, MAS PAUSADO COMO FRENTE PRINCIPAL
DECISAO: USAR COMO REFERENCIA, NAO COMO BASE FINAL DE LUCRO
```

Frentes atuais:

```text
SPORTMONKS_STRATEGY_DRAWDOWN_AUDIT_V1
STATUS: ATIVA
DECISAO: APROVADO COM RESSALVAS PARA AUDITORIA DE RISCO DAS ESTRATEGIAS ORIGINAIS
```

```text
SPORTMONKS_MULTI_LEAGUE_DISCOVERY_VALIDATION
STATUS: INICIADA
PRIMEIRA LIGA: LA LIGA 2025/26
```

```text
RENTABILIDADE_DAS_ESTRATEGIAS_POR_TIME_V4
STATUS: APROVADA COM PEQUENOS AJUSTES
DECISAO: V2 CONTINUA COMO BASE DETALHADA; V3 ABORTADA; V4 PROMOVIDA COMO EXTENSAO QUANTITATIVA OFICIAL
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
- criacao da rentabilidade por time V2;
- decisao de abortar a V3 e promover a V4.

---

## Decisao Operacional Atual

A documentacao de playbooks V3 permanece como referencia operacional, mas a selecao de estrategias volta a usar:

```text
estrategias originais
sem filtros V3 por padrao
sem agregacao de targets
sem juntar estrategias parecidas
```

A partir deste ponto, a escolha de estrategias deve priorizar:

- lucro final;
- ROI;
- EV por trade;
- drawdown maximo;
- sequencia maxima de perdas;
- consistencia por temporada;
- duplicidades;
- robustez por time.

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

## Decisao sobre Rentabilidade por Time

Documentos oficiais:

```text
docs/04_RESEARCH/RENTABILIDADE_DAS_ESTRATEGIAS_POR_TIME_RESULTADOS_V4.md
docs/04_RESEARCH/DECISAO_RENTABILIDADE_POR_TIME_V4_VS_V3.md
```

Issue de decisao:

```text
#4 - DECISAO — abortar V3 e promover V4 da rentabilidade por time
```

Decisao oficial:

```text
V3 ABORTADA.
V2 MANTIDA COMO BASE DETALHADA.
V4 APROVADA COM PEQUENOS AJUSTES.
```

Metricas oficiais adicionadas na V4:

- `robustez_score`;
- `impacto_top3_pct`;
- `lucro_sem_top1_negativo`;
- `lucro_sem_top3_negativo`;
- ranking das estrategias mais robustas;
- ranking das estrategias mais dependentes.

Ajustes pendentes:

```text
1. robustez_score >= 0.60 deve ser ROBUSTA.
2. ranking das mais dependentes deve filtrar lucro_total >= 500 OU N >= 30.
```

---

## Proxima Frente Oficial

```text
MULTI_LEAGUE_DRAWDOWN_AUDIT_V1
```

Objetivo:

Aplicar o script de drawdown nas estrategias originais para La Liga e futuras ligas/temporadas, mantendo:

- estrategias separadas;
- temporadas separadas;
- targets separados;
- sem filtros V3 por padrao;
- foco em lucro final + drawdown + ROI + EV.

---

## Restricoes

- Nao criar robo.
- Nao criar producao.
- Nao chamar simulacao com odds medias de backtesting financeiro real.
- Nao usar odds live inexistentes.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
