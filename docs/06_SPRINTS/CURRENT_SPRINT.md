# CURRENT SPRINT

## Sprint Atual

Status:

```text
ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1_EM_ANDAMENTO
ETAPA_5_TARGETS_RESTANTES_CONCLUIDA_COM_RESSALVAS
PROXIMA_ETAPA: ETAPA_6_CLASSIFICACAO_FRIO_QUENTE_POR_CUTOFF_V1
```

Frente oficial ativa:

```text
ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1
```

Documentos principais:

```text
docs/04_RESEARCH/ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1.md
docs/04_RESEARCH/primeiro_tempo/STATUS_ANDAMENTO_ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1.md
docs/04_RESEARCH/primeiro_tempo/ROADMAP_CONTINUACAO_FRIO_QUENTE_HT_GOAL_V1.md
```

Status operacional:

```text
NENHUMA_OPERACAO_REAL_APROVADA
NENHUM_ROBO_OPERACIONAL_APROVADO
PAPER_APENAS_EM_FASE_FUTURA
```

---

## Decisao atual registrada

A continuidade da frente de trajetorias do primeiro tempo deve partir da Etapa 5 ja concluida e seguir para uma camada de classificacao de estado do jogo.

Tese da continuidade:

```text
HT Goal nao deve ser avaliado apenas porque o preco parece atrativo.
HT Goal deve ser avaliado quando o estado do jogo justifica o preco observado.
```

A proxima etapa nao e a preparacao direta de alertas paper. Antes disso, a frente deve cruzar as sobreviventes da Etapa 5 com estados como frio, morno, quente, caotico, aquecendo, esfriando, pressao real e pressao falsa.

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

Sobreviventes da Etapa 5:

```text
HT_NO_GOAL_BAIXA_QUALIDADE_REAL_V1 observada_ate_30
HT_NO_GOAL_BAIXA_QUALIDADE_REAL_V1 observada_ate_35
HT_NO_GOAL_AQUECIMENTO_FRACO_V1 observada_ate_30
HT_NO_GOAL_AQUECIMENTO_FRACO_V1 observada_ate_35
HT_GOAL_QUALIDADE_PONTUAL_PRECOCE_V1 observada_ate_20
HT_GOAL_AQUECIMENTO_MODERADO_COM_QUALIDADE_V1 observada_ate_30
```

---

## Roadmap de continuidade

```text
Etapa 6 — Classificacao frio/quente por cutoff
Etapa 7 — Cruzamento das sobreviventes da Etapa 5 com estado do jogo
Etapa 8 — Avaliacao com odds medias por cutoff e por estado
Etapa 9 — Reclassificacao das sobreviventes
Etapa 10 — Analise dinamica de mudanca de estado
Etapa 11 — Simulacao manter vs sair
Etapa 12 — Paper trading com regras de entrada e reavaliacao
```

---

## Proxima acao

Criar prompt/execucao da:

```text
ETAPA_6_CLASSIFICACAO_FRIO_QUENTE_POR_CUTOFF_V1
```

Escopo:

```text
Usar as features ja construidas nas Etapas 1-5.
Nao refazer discovery bruto.
Nao misturar com a adaptacao completa LateGoal para HT Goal.
Classificar estados do jogo por cutoff e preparar base para cruzar com as candidatas sobreviventes da Etapa 5.
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
