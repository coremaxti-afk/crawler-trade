# ROADMAP_EXPLORATORIO_PRE_RANKING_OPERACIONAL_FINAL_V1

## Status

`ROADMAP EXPLORATORIO CONCLUIDO — SEGUIR PARA VALIDACAO MULTI-TEMPORADA`

## Diretriz obrigatoria relacionada

Antes de executar qualquer nova frente, todos os agentes devem seguir:

```text
docs/00_AGENTS/GOVERNANCE_V2.md
```

Regra central: nenhum agente deve concordar com o usuario apenas para agradar. Se uma solicitacao pular etapas, misturar objetivos ou fragilizar a metodologia, o agente deve discordar primeiro, explicar o risco tecnico e propor o caminho correto.

## Fase atual

A fase atual do projeto passou a ser:

```text
VALIDACAO MULTI-TEMPORADA PRE-RANKING OPERACIONAL
```

O objetivo agora e validar fora da amostra os padroes descobertos na Serie A 2025.

Nao construir ranking operacional final antes dessa validacao.

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

## Resultado das frentes

### 1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1

Status:

```text
APROVADA COMO V1 EXPLORATORIA
```

Documento:

```text
docs/04_RESEARCH/agrupamento_por_familia_e_variacoes_v1/AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
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

Documento:

```text
docs/04_RESEARCH/analise_regime_por_fase_v1/ANALISE_REGIME_POR_FASE_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
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

Documento:

```text
docs/04_RESEARCH/analise_maturidade_liga_por_rodada_v1/ANALISE_MATURIDADE_LIGA_POR_RODADA_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
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

Documento:

```text
docs/04_RESEARCH/analise_forca_favorito_por_estrategia_v1/ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

Conclusao:

```text
As melhores familias No Goal parecem mais fortes em jogos parelhos/sem favorito claro.
Goal nao ficou lucrativo no agregado em nenhum segmento.
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

Conclusao:

```text
O perfil mais forte de prejuizo No Goal foi FAVORITO_MEDIO_DOMINANTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA.
São Paulo, Internacional e Botafogo sao os principais alertas exploratorios.
Nenhum time deve ser excluido automaticamente com base nesta etapa.
```

---

## Hipoteses congeladas para validacao multi-temporada

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

# Proxima fase oficial

```text
VALIDACAO_MULTI_TEMPORADA_V1
```

## Objetivo

Validar se os padroes descobertos na Serie A 2025 sobrevivem em outras temporadas.

## Perguntas obrigatorias

```text
1. As familias No Goal continuam superiores em outras temporadas?
2. Goal/Over continua negativo em outras temporadas?
3. Jogos parelhos/sem favorito claro continuam favorecendo No Goal?
4. A maturidade cedo se repete?
5. O perfil FAVORITO_MEDIO_DOMINANTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA reaparece?
6. Os times/perfis prejudiciais de 2025 se repetem ou foram especificos da temporada?
7. Quais padroes sobrevivem o suficiente para entrar no Ranking Operacional Final?
```

## Saida esperada da proxima fase

Separar os padroes em:

```text
CONFIRMADO_MULTI_TEMPORADA
ENFRAQUECIDO
REPROVADO
INCONCLUSIVO
```

---

## Roadmap posterior

```text
1. VALIDACAO_MULTI_TEMPORADA_V1
2. COMPARACAO_PADROES_2025_VS_OUTRAS_TEMPORADAS_V1
3. RANKING_OPERACIONAL_FINAL_V1
4. VALIDACAO_OPERACIONAL_FINAL_V1
5. PLAYBOOK_OPERACIONAL_FINAL
```

## Regra final

Nenhuma estrategia, filtro, perfil de time ou contexto deve entrar como regra operacional definitiva antes da validacao multi-temporada.
