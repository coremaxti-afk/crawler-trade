# STATUS_ANDAMENTO_ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1

## Status atual

```text
FRENTE_ATIVA_DE_PESQUISA
DISCOVERY_DE_FLUXO_DO_PRIMEIRO_TEMPO
HOLD_ONLY
SEM_OPERACAO_REAL_APROVADA
SEM_CASHOUT
SEM_ROBO_OPERACIONAL_NESTA_ETAPA
```

## Decisao registrada

O usuario decidiu seguir o roadmap atual da frente de primeiro tempo sem incluir odds e sem incluir filtros de favorito/pre-live nesta fase.

A frente deve continuar ate a etapa que deixaria as regras prontas para configuracao futura de alerta paper, mas sem configurar robo, sem ativar alerta real e sem aprovar operacao.

## Entregas ja realizadas

### Etapa 1 — Reconstrucao do primeiro tempo

Status final: `ETAPA_1_APROVADA_PARA_ETAPA_2`.

Resumo:

```text
liga: premier_league
temporada: 2025_2026
season_id: 25583
fixtures reconciliadas: 380
divergencias residuais: 0
```

### Etapa 2 — Features de trajetoria

Status final: `ETAPA_2_APROVADA_COM_RESSALVA_LEVE`.

Foram criadas features de volume, qualidade, intensidade, conversao de pressao, pico/queda, pressao recente, assimetria e estado do placar.

### Etapa 3 — Classificacao inicial

Status final: `ETAPA_3_INCONCLUSIVA_POR_CLASSIFICACAO_FRACA`.

Motivo: concentracao excessiva em poucos perfis.

### Etapa 3.1 — Recalibracao

Status final: `ETAPA_3_1_INCONCLUSIVA_POR_FRAGMENTACAO_EXCESSIVA`.

Melhorou a concentracao, mas gerou muitos perfis pequenos.

### Etapa 3.2 — Consolidacao de perfis

Status final: `ETAPA_3_2_APROVADA_COM_RESSALVAS`.

Grupos liberados para conversao em candidatas:

```text
HT_GOAL_AQUECIMENTO_MODERADO_COM_QUALIDADE
HT_GOAL_QUALIDADE_PONTUAL_PRECOCE
HT_NO_GOAL_AQUECIMENTO_FRACO
HT_NO_GOAL_BAIXA_QUALIDADE_REAL
```

Grupos bloqueados:

```text
HT_GOAL_QUALIDADE_REAL_ALTA -> BLOQUEADO_POR_OVERLAP
HT_NO_GOAL_FRIO_OBSERVAVEL -> BLOQUEADO_POR_OVERLAP
HT_NO_GOAL_PRESSAO_RECENTE_SEM_CONVERSAO -> BLOQUEADO_POR_N
```

### Etapa 4 — Estrategias candidatas

Status final: `ETAPA_4_APROVADA_COM_RESSALVAS`.

Estrategias candidatas criadas:

```text
HT_GOAL_AQUECIMENTO_MODERADO_COM_QUALIDADE_V1
HT_GOAL_QUALIDADE_PONTUAL_PRECOCE_V1
HT_NO_GOAL_AQUECIMENTO_FRACO_V1
HT_NO_GOAL_BAIXA_QUALIDADE_REAL_V1
```

Todas permaneceram como candidatas locais, sem validacao fora da amostra e dependentes de target restante.

### Etapa 5 — Targets restantes

Status final: `ETAPA_5_APROVADA_COM_RESSALVAS`.

Targets criados:

```text
GOAL_AFTER_20_TO_HT
GOAL_AFTER_30_TO_HT
GOAL_AFTER_35_TO_HT
NO_GOAL_AFTER_20_TO_HT
NO_GOAL_AFTER_30_TO_HT
NO_GOAL_AFTER_35_TO_HT
```

Leituras sobreviventes principais:

```text
HT_NO_GOAL_BAIXA_QUALIDADE_REAL_V1 observada_ate_30 -> SOBREVIVE_TARGET_RESTANTE_FORTE
HT_NO_GOAL_BAIXA_QUALIDADE_REAL_V1 observada_ate_35 -> SOBREVIVE_TARGET_RESTANTE_MODERADO
HT_NO_GOAL_AQUECIMENTO_FRACO_V1 observada_ate_30 -> SOBREVIVE_TARGET_RESTANTE_MODERADO
HT_NO_GOAL_AQUECIMENTO_FRACO_V1 observada_ate_35 -> SOBREVIVE_TARGET_RESTANTE_MODERADO
HT_GOAL_QUALIDADE_PONTUAL_PRECOCE_V1 observada_ate_20 -> SOBREVIVE_TARGET_RESTANTE_MODERADO
HT_GOAL_AQUECIMENTO_MODERADO_COM_QUALIDADE_V1 observada_ate_30 -> SOBREVIVE_TARGET_RESTANTE_MODERADO
```

Leituras inconclusivas por concentracao de estado:

```text
HT_GOAL_AQUECIMENTO_MODERADO_COM_QUALIDADE_V1 observada_ate_35
HT_GOAL_QUALIDADE_PONTUAL_PRECOCE_V1 observada_ate_30
```

## Ressalva sobre odds

Foi registrada a critica metodologica de que sem odds nao existe aprovacao financeira de uma estrategia de trade esportivo.

A frente atual valida apenas sinal estatistico, target restante, baseline, lift, N, leakage e overlap.

Ela nao valida lucro, ROI, EV, break-even, drawdown ou operacao real.

Status correto das candidatas atuais:

```text
CANDIDATA_ESTATISTICA_SEM_ODDS
NAO_VALIDADA_FINANCEIRAMENTE
NAO_OPERACIONAL
```

## Ressalva sobre segmentacao futura

Tambem foi registrada a possibilidade de que uma estrategia negativa no macro possa se tornar positiva em segmentos especificos, como favorito forte, favorito medio, odd pre-live 1x2 ate 1.60, mandante/visitante favorito, 0x0 aos 30, favorito vencendo, empatando ou perdendo.

Esses filtros nao entram na frente atual.

Status:

```text
PENDENCIA_FUTURA
ESTUDO_SEGMENTADO_POSTERIOR
NAO_INCLUIR_NA_FRENTE_ATUAL
```

## Proxima etapa sugerida dentro do roadmap atual

Nome sugerido:

```text
ETAPA_6_PREPARACAO_REGRAS_ALERTA_PAPER_CORNER_PRO_V1
```

Objetivo:

```text
Transformar as candidatas sobreviventes ao target restante em especificacoes objetivas de alerta paper, sem configurar robo e sem aprovar operacao.
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
