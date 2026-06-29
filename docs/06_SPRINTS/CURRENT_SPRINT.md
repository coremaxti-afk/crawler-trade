# CURRENT SPRINT

## Sprint Atual

Status:

```text
ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1_EM_ANDAMENTO
ETAPA_5_TARGETS_RESTANTES_CONCLUIDA_COM_RESSALVAS
PROXIMA_ETAPA: PREPARACAO_REGRAS_ALERTA_PAPER_CORNER_PRO_V1
```

Frente oficial ativa:

```text
ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1
```

Documentos principais:

```text
docs/04_RESEARCH/ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1.md
docs/04_RESEARCH/primeiro_tempo/STATUS_ANDAMENTO_ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1.md
```

Status operacional:

```text
NENHUMA OPERACAO REAL APROVADA
NENHUM ROBO OPERACIONAL APROVADO
ALERTAS CORNER PRO SOMENTE COMO FASE FUTURA PAPER/OBSERVACAO
SEM_CASHOUT
```

---

## Decisao atual registrada

O usuario decidiu seguir o roadmap atual da frente de primeiro tempo **sem odds** e **sem filtros de favorito/pre-live** nesta fase.

O objetivo e chegar ate a etapa que deixaria as regras prontas para configuracao futura de alerta paper, mas:

```text
NAO_CONFIGURAR_ROBO_AGORA
NAO_ATIVAR_ALERTA_REAL
NAO_APROVAR_ENTRADA
NAO_CALCULAR_ROI_EV_LUCRO_DRAWDOWN_NESTA_FRENTE
```

---

## Andamento resumido

```text
Etapa 1 — Reconstrucao do 1T: APROVADA
Etapa 2 — Features de trajetoria: APROVADA_COM_RESSALVA_LEVE
Etapa 3 — Classificacao inicial: INCONCLUSIVA_POR_CLASSIFICACAO_FRACA
Etapa 3.1 — Recalibracao: INCONCLUSIVA_POR_FRAGMENTACAO_EXCESSIVA
Etapa 3.2 — Consolidacao: APROVADA_COM_RESSALVAS
Etapa 4 — Estrategias candidatas: APROVADA_COM_RESSALVAS
Etapa 5 — Targets restantes: APROVADA_COM_RESSALVAS
```

Candidatas sobreviventes ao target restante para considerar na proxima etapa paper:

```text
HT_NO_GOAL_BAIXA_QUALIDADE_REAL_V1 observada_ate_30
HT_NO_GOAL_BAIXA_QUALIDADE_REAL_V1 observada_ate_35
HT_NO_GOAL_AQUECIMENTO_FRACO_V1 observada_ate_30
HT_NO_GOAL_AQUECIMENTO_FRACO_V1 observada_ate_35
HT_GOAL_QUALIDADE_PONTUAL_PRECOCE_V1 observada_ate_20
HT_GOAL_AQUECIMENTO_MODERADO_COM_QUALIDADE_V1 observada_ate_30
```

Leituras inconclusivas por concentracao de estado:

```text
HT_GOAL_AQUECIMENTO_MODERADO_COM_QUALIDADE_V1 observada_ate_35
HT_GOAL_QUALIDADE_PONTUAL_PRECOCE_V1 observada_ate_30
```

---

## Proxima acao

Criar a etapa:

```text
ETAPA_6_PREPARACAO_REGRAS_ALERTA_PAPER_CORNER_PRO_V1
```

Objetivo:

```text
Transformar candidatas sobreviventes ao target restante em especificacoes objetivas de alerta paper, sem configuracao real e sem aprovacao operacional.
```

Permitido:

```text
formatar regra
listar condicoes observaveis
listar minuto/fase
listar target de acompanhamento
listar campos necessarios na plataforma
criar checklist de observacao paper
```

Proibido:

```text
configurar robo real
aprovar entrada
calcular ROI/lucro/EV/drawdown
usar odds nesta etapa
usar favorito/pre-live nesta etapa
emitir sinal comercial
```

---

## Ressalva sobre odds

Sem odds, nao existe aprovacao financeira de estrategia de trade esportivo.

As candidatas atuais devem ser tratadas como:

```text
CANDIDATA_ESTATISTICA_SEM_ODDS
NAO_VALIDADA_FINANCEIRAMENTE
NAO_OPERACIONAL
```

Odds, break-even, EV, ROI, lucro e drawdown ficam para frente futura especifica, caso autorizada.

---

## Ressalva sobre segmentacao futura

Fica registrada a possibilidade de estudos segmentados posteriores usando a base ja construida, incluindo:

```text
favorito forte
favorito medio
odd pre-live 1x2 ate 1.60
mandante/visitante favorito
0x0 aos 30
favorito vencendo/empatando/perdendo
```

Esses filtros nao entram na frente atual.

Status:

```text
PENDENCIA_FUTURA
ESTUDO_SEGMENTADO_POSTERIOR
NAO_INCLUIR_NA_FRENTE_ATUAL
```

---

## Governanca obrigatoria

Documento oficial:

```text
docs/00_AGENTS/GOVERNANCE_V2.md
```

Regra central:

```text
Nenhum agente deve concordar com o usuario apenas para agradar.
```

Se uma solicitacao pular etapas, inflar lucro/ROI/robustez ou gerar falsa confianca operacional, o agente deve discordar e propor o caminho correto.
