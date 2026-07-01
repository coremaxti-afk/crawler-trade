# STATUS_ANDAMENTO_ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1

## Status atual

```text
FRENTE_ATIVA_DE_PESQUISA
DISCOVERY_DE_FLUXO_DO_PRIMEIRO_TEMPO
ETAPA_5_APROVADA_COM_RESSALVAS
PROXIMA_ETAPA: ETAPA_6_CLASSIFICACAO_FRIO_QUENTE_POR_CUTOFF_V1
SEM_OPERACAO_REAL_APROVADA
SEM_ROBO_OPERACIONAL_NESTA_ETAPA
```

## Decisao registrada

O usuario decidiu dar continuidade ao estudo de trajetorias do primeiro tempo a partir da Etapa 5, adicionando uma camada de classificacao frio/quente por cutoff.

A proxima etapa correta nao e preparar diretamente alertas paper. Antes disso, a frente deve testar se o estado do jogo melhora ou piora as candidatas sobreviventes da Etapa 5.

Tese registrada:

```text
HT Goal nao deve ser avaliado apenas porque o preco parece atrativo.
HT Goal deve ser avaliado quando o estado do jogo justifica o preco observado.
```

Documento complementar criado:

```text
docs/04_RESEARCH/primeiro_tempo/ROADMAP_CONTINUACAO_FRIO_QUENTE_HT_GOAL_V1.md
```

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

## Etapa 6 — escopo da proxima execucao

Objetivo:

```text
Classificar o estado do jogo por cutoff para separar frio, morno, quente, caotico, aquecendo, esfriando, pressao real e pressao falsa.
```

Cutoffs:

```text
15,20,25,30,35,40
```

Indicadores esperados:

```text
attacks
dangerous_attacks
shots_total
shots_on_target
corners
key_passes
big_chances
ritmo recente
aceleracao
volume com qualidade
volume sem qualidade
assimetria entre times
```

## Ressalva sobre odds

Odds medias por cutoff podem ser usadas a partir da Etapa 8 para break-even, EV, ROI, resultado estimado, drawdown e DDD, mas sempre como:

```text
ESTIMATIVA_OPERACIONAL_COM_ODDS_MEDIAS
NAO_BACKTEST_FINANCEIRO_REAL
NAO_OPERACIONAL
```

## Proibicoes mantidas

```text
NAO_APROVAR_OPERACAO_REAL
NAO_CONFIGURAR_ROBO_OPERACIONAL
NAO_CHAMAR_ODDS_MEDIAS_DE_BACKTEST_REAL
NAO_REFAZER_DISCOVERY_BRUTO_NESTA_CONTINUIDADE
NAO_MISTURAR_COM_ADAPTACAO_COMPLETA_LATEGOAL_PARA_HT_GOAL
```
