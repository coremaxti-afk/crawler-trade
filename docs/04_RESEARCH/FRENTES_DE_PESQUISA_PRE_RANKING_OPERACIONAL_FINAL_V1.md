# ROADMAP_EXPLORATORIO_PRE_RANKING_OPERACIONAL_FINAL_V1

## Status

`COMPARACAO BI-TEMPORADA CONCLUIDA — SEGUIR PARA RANKING_OPERACIONAL_FINAL_V1`

## Diretriz obrigatoria relacionada

Antes de executar qualquer nova frente, todos os agentes devem seguir:

```text
docs/00_AGENTS/GOVERNANCE_V2.md
```

Regra central: nenhum agente deve concordar com o usuario apenas para agradar. Se uma solicitacao pular etapas, misturar objetivos ou fragilizar a metodologia, o agente deve discordar primeiro, explicar o risco tecnico e propor o caminho correto.

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

## Pipeline de temporada

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

---

## Comparacao bi-temporada 2024 x 2025

Analise concluida:

```text
COMPARACAO_MULTI_LIGA_TEMPORADA_QUALIDADE_E_OSCILACAO_V1.1
```

Documento:

```text
docs/04_RESEARCH/comparacao_multi_liga_temporada_qualidade_e_oscilacao_v1/COMPARACAO_MULTI_LIGA_TEMPORADA_QUALIDADE_E_OSCILACAO_V1_SERIE_A_2024__VS__SERIE_A_2025.md
```

Status:

```text
APROVADA COMO TRIAGEM BI-TEMPORADA
NAO APROVA OPERACAO FINAL
```

---

## Resultado consolidado da triagem

### Direcao de mercado

```text
No Goal/Under superior nas duas temporadas.
Goal/Over reprovado no agregado das duas temporadas.
```

### Maturidade

```text
As principais familias No Goal amadureceram na rodada 5 em 2024 e 2025.
```

### Phase6 e Phase8

```text
As familias No Goal aprovadas sao lucrativas nas duas temporadas, mas apresentam oscilacao por fase.
A maior parte recebeu OSCILANTE_PHASE6 e OSCILANTE_PHASE8.
```

---

## Familias consistentes para entrada no ranking

```text
1. team_winning_by_1_no_sot_against__no_goal — score 82,8
2. opponent_no_big_chances__no_goal — score 82,5
3. both_teams_cold_2of3__no_goal — score 78,7
4. opponent_no_recent_key_passes__no_goal — score 73,4
5. team_winning_by_1_low_dangerous_attacks_against__no_goal — score 71,1
```

Familias oscilantes:

```text
team_winning_by_1_opp_cold_2of3__no_goal
favorite_winning_by_1_opp_cold_2of3__no_goal
```

Todas as familias Goal/Over ficaram reprovadas ou inconclusivas.

---

## Hipoteses atualizadas

```text
1. Familias No Goal sao superiores a Goal/Over no agregado.
2. Goal/Over permanece estruturalmente pior que No Goal.
3. No Goal amadurece cedo nas duas temporadas comparadas.
4. A rodada 5 aparece como ponto forte para as familias No Goal analisadas.
5. A curva phase6/phase8 revela oscilacao importante.
6. A segmentacao por favorito importa, mas a melhor faixa ainda e inconclusiva.
7. Favorito forte nao deve ser automaticamente privilegiado.
8. Time especifico nao deve dominar a validacao porque muda muito entre temporadas.
9. O ranking final deve considerar familia + variacao + rodada + fase + oscilacao + drawdown, e nao apenas lucro agregado.
```

---

# Proxima fase oficial

```text
RANKING_OPERACIONAL_FINAL_V1
```

## Objetivo

Construir ranking conservador das familias/variacoes candidatas, sem aprovar operacao final.

## Perguntas obrigatorias

```text
1. Quais familias/variacoes mantem melhor combinacao de lucro, ROI, EV e N?
2. Quais tem drawdown e max losing streak aceitaveis?
3. Quais amadurecem cedo e de forma recorrente?
4. Quais sofrem maior penalizacao por phase6/phase8?
5. Quais devem ser candidatas fortes?
6. Quais devem ser candidatas com ressalva?
7. Quais devem ser rebaixadas por oscilacao?
8. Quais devem ser descartadas?
```

## Saida esperada da proxima fase

Separar familias/variacoes em:

```text
CANDIDATA_FORTE
CANDIDATA_COM_RESSALVA
OSCILANTE_REBAIXADA
REPROVADA
INCONCLUSIVA
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

Essa etapa deve vir depois do ranking e da validacao operacional final, apenas para familias/variacoes que sobreviverem.

---

## Roadmap posterior

```text
1. RANKING_OPERACIONAL_FINAL_V1
2. VALIDACAO_OPERACIONAL_FINAL_V1
3. ANATOMIA_DA_ESTRATEGIA_V1
4. PLAYBOOK_OPERACIONAL_FINAL
```

## Regra final

Nenhuma estrategia, filtro, perfil de time, contexto de favorito, rodada ou fase deve entrar como regra operacional definitiva antes do ranking e da validacao operacional final.
