# ROADMAP_EXPLORATORIO_PRE_RANKING_OPERACIONAL_FINAL_V1

## Status

`ROADMAP EXPLORATORIO CONCLUIDO — SEGUIR PARA PIPELINE E COMPARACAO 2024 X 2025`

## Diretriz obrigatoria relacionada

Antes de executar qualquer nova frente, todos os agentes devem seguir:

```text
docs/00_AGENTS/GOVERNANCE_V2.md
```

Regra central: nenhum agente deve concordar com o usuario apenas para agradar. Se uma solicitacao pular etapas, misturar objetivos ou fragilizar a metodologia, o agente deve discordar primeiro, explicar o risco tecnico e propor o caminho correto.

## Fase atual

A fase atual do projeto passou a ser:

```text
ORQUESTRACAO DE TEMPORADA E COMPARACAO BI-TEMPORADA 2024 X 2025
```

Motivo:

```text
O acesso SportMonks atual limita o historico ate 2024.
A validacao fora da amostra sera inicialmente Serie A 2024 x Serie A 2025.
```

Nao construir ranking operacional final antes dessa comparacao.

---

## Roadmap exploratorio executado

As cinco frentes exploratorias foram executadas:

```text
1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
2. ANALISE_REGIME_POR_FASE_V1
3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1
```

---

## Script que processa uma temporada completa

### PIPELINE_TEMPORADA_COMPLETA_V1

Papel:

```text
Executar automaticamente todos os scripts aprovados para uma temporada.
```

Escopo esperado:

```text
DISCOVERY
NORMALIZACAO_FIXTURE_LEVEL
DRAWDOWN_V4
AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
ANALISE_REGIME_POR_FASE_V1
ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1
```

Regra arquitetural:

```text
O pipeline apenas orquestra.
Cada script continua gerando seus proprios artefatos nas respectivas pastas.
Nao gerar MD/CSV consolidado com todos os resultados analiticos.
```

Artefatos proprios do pipeline:

```text
INVENTARIO_PIPELINE_TEMPORADA_COMPLETA_V1.csv
pipeline_temporada_completa_v1.log
pipeline_temporada_completa_v1_manifest.json
PIPELINE_TEMPORADA_COMPLETA_V1_RELATORIO.md
```

---

## Resultado das cinco frentes de 2025

### 1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1

Status:

```text
APROVADA COMO V1 EXPLORATORIA
```

Conclusao:

```text
Nao somar lucro de variacoes da mesma familia como se fossem estrategias independentes.
```

### 2. ANALISE_REGIME_POR_FASE_V1

Status:

```text
APROVADA COMO V1 EXPLORATORIA
```

Conclusao:

```text
Goal/Over foi negativo em todas as fases.
No Goal/Under foi positivo em todas as fases.
```

### 3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1

Status:

```text
APROVADA COMO V1 EXPLORATORIA
```

Conclusao:

```text
A liga geral pode enganar por misturar Goal ruim com No Goal bom.
No Goal amadurece cedo nas melhores familias.
A V1 testou apenas rodadas 5 a 12.
```

### 4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1

Status:

```text
APROVADA COMO V1 EXPLORATORIA COM RESSALVA DE INTERPRETACAO
```

Conclusao atualizada apos comparacao preliminar com 2024:

```text
A forca do favorito importa, mas a melhor faixa ainda e inconclusiva.
Em 2025 jogo parelho foi muito forte.
Em 2024 favorito medio foi melhor.
Favorito forte nao deve ser privilegiado automaticamente.
```

### 5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1

Status:

```text
APROVADA COMO V1_1 EXPLORATORIA
```

Conclusao atualizada:

```text
A leitura por time e util, mas deve ser secundaria na comparacao 2024 x 2025.
Times mudam muito entre temporadas.
O foco deve ficar em familia, variacao, rodada, phase6, phase8 e oscilacao.
```

---

## Hipoteses congeladas para comparacao 2024 x 2025

```text
1. Familias No Goal sao superiores a Goal/Over no agregado.
2. No Goal e lucrativo em varias fases da temporada.
3. As melhores familias No Goal amadurecem cedo.
4. A rodada de maturidade deve ser parecida entre 2024 e 2025.
5. A curva phase6 deve ser medida para estabilidade.
6. A curva phase8 deve ser medida para oscilacao.
7. A segmentacao por favorito importa, mas a melhor faixa ainda e inconclusiva.
8. Favorito forte nao deve ser automaticamente privilegiado.
9. Time especifico nao deve dominar a validacao porque muda muito entre temporadas.
10. Perfis/contextos podem ser mantidos como variaveis auxiliares.
```

---

# Proxima fase analitica oficial

```text
COMPARACAO_BI_TEMPORADA_QUALIDADE_E_OSCILACAO_V1
```

## Objetivo

Comparar Serie A 2024 x Serie A 2025 para medir se as familias e variacoes mantem qualidade entre temporadas.

## Perguntas obrigatorias

```text
1. As estrategias validam nas mesmas rodadas?
2. No Goal continua superior ao Goal nas duas temporadas?
3. A curva phase6 e estavel entre 2024 e 2025?
4. A curva phase8 revela oscilacao perigosa?
5. O lucro esta concentrado em poucas fases?
6. O drawdown explode em alguma fase?
7. A qualidade de ROI e lucro e parecida entre temporadas?
8. Quais familias validam nas duas temporadas?
9. Quais familias validam so em uma temporada?
10. Quais variacoes devem ser rebaixadas por instabilidade?
```

## Saida esperada da proxima fase

Separar familias/variacoes em:

```text
VALIDA_NAS_DUAS_TEMPORADAS
VALIDA_SO_2025
VALIDA_SO_2024
OSCILANTE
REPROVADA_NAS_DUAS
INCONCLUSIVA
```

E maturidade em:

```text
MADURA_CEDO_NAS_DUAS
MADURA_SO_EM_UMA
INSTAVEL_POR_RODADA
```

---

## Anatomia da estrategia — etapa futura

A transformacao de estrategias em leitura operacional detalhada de dados reais, por exemplo:

```text
both_teams_cold_2of3
```

com:

```text
ataques perigosos
chutes no gol
chutes para fora
escanteios
posse
pressao
```

fica para:

```text
ANATOMIA_DA_ESTRATEGIA_V1
```

Essa etapa deve vir depois da comparacao 2024 x 2025 e antes do playbook operacional final, apenas para familias/variacoes que sobreviverem.

---

## Roadmap posterior

```text
1. PIPELINE_TEMPORADA_COMPLETA_V1
2. COMPARACAO_BI_TEMPORADA_QUALIDADE_E_OSCILACAO_V1
3. RANKING_OPERACIONAL_FINAL_V1
4. VALIDACAO_OPERACIONAL_FINAL_V1
5. ANATOMIA_DA_ESTRATEGIA_V1
6. PLAYBOOK_OPERACIONAL_FINAL
```

## Regra final

Nenhuma estrategia, filtro, perfil de time, contexto de favorito, rodada ou fase deve entrar como regra operacional definitiva antes da comparacao 2024 x 2025 e da validacao operacional final.
