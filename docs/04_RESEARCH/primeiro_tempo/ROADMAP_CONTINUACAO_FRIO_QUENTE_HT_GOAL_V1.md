# ROADMAP_CONTINUACAO_FRIO_QUENTE_HT_GOAL_V1

## Decisao

A continuidade da frente ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1 deve partir da Etapa 5 ja concluida e seguir para uma nova camada de classificacao de estado do jogo.

## Proxima etapa

```text
ETAPA_6_CLASSIFICACAO_FRIO_QUENTE_POR_CUTOFF_V1
```

## Objetivo

Classificar cada fixture/cutoff do primeiro tempo em estados de jogo para entender quando os sinais da Etapa 5 melhoram ou pioram.

Estados candidatos:

```text
FRIO
MORNO
QUENTE
CAOTICO
AQUECENDO
ESFRIANDO
PRESSAO_REAL
PRESSAO_FALSA
```

## Roadmap

```text
Etapa 6 - Classificacao frio/quente por cutoff
Etapa 7 - Cruzamento das sobreviventes da Etapa 5 com estado do jogo
Etapa 8 - Avaliacao com odds medias por cutoff e por estado
Etapa 9 - Reclassificacao das sobreviventes
Etapa 10 - Analise dinamica de mudanca de estado
Etapa 11 - Simulacao manter vs sair
Etapa 12 - Paper trading com regras de entrada e reavaliacao
```

## Regras

```text
Nao refazer discovery bruto nesta continuidade.
Nao misturar com adaptacao completa LateGoal para HT Goal.
Nao aprovar operacao real.
Nao configurar robo operacional.
Usar odds medias apenas como estimativa operacional, nunca como backtest financeiro real.
```
