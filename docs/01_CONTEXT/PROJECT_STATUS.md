# PROJECT STATUS

## Estado Atual do Projeto

FASE ATUAL:

```text
PREPARACAO DO RANKING_OPERACIONAL_FINAL_V1
```

A fase de comparacao bi-temporada entre Serie A 2024 e Serie A 2025 foi concluida como triagem exploratoria.

Status da entrega:

```text
COMPARACAO_MULTI_LIGA_TEMPORADA_QUALIDADE_E_OSCILACAO_V1.1
APROVADA COMO TRIAGEM BI-TEMPORADA
NAO APROVA OPERACAO FINAL
```

Documento registrado:

```text
docs/04_RESEARCH/comparacao_multi_liga_temporada_qualidade_e_oscilacao_v1/COMPARACAO_MULTI_LIGA_TEMPORADA_QUALIDADE_E_OSCILACAO_V1_SERIE_A_2024__VS__SERIE_A_2025.md
```

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

## Roadmap Exploratorio Serie A 2025 — Concluido

Ordem executada:

```text
1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
2. ANALISE_REGIME_POR_FASE_V1
3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1
```

---

## Temporadas comparadas

```text
Serie A 2024
Serie A 2025
```

Motivo do escopo:

```text
O acesso atual da SportMonks limita o historico ate 2024.
A primeira validacao fora da amostra foi feita como comparacao 2024 x 2025.
```

---

## Script orquestrador de temporada

Script planejado/necessario:

```text
PIPELINE_TEMPORADA_COMPLETA_V1
```

Papel:

```text
Executar automaticamente todos os scripts aprovados para uma temporada, preservando a organizacao atual de pastas e artefatos.
```

Importante:

```text
O PIPELINE_TEMPORADA_COMPLETA_V1 nao e uma nova analise.
Ele e um orquestrador.
Cada etapa continua gerando seus proprios CSVs, JSONs e MDs nas respectivas pastas.
O pipeline gera apenas log, manifest e relatorio de execucao.
```

---

## Resultado da comparacao bi-temporada V1.1

### Goal vs No Goal

```text
Goal/Over: reprovado no agregado das duas temporadas.
No Goal/Under: superior nas duas temporadas.
```

### Maturidade

As principais familias No Goal amadureceram cedo nas duas temporadas:

```text
maturity_2024 = rodada 5
maturity_2025 = rodada 5
delta_rounds = 0
```

### Phase6 e Phase8

```text
As familias No Goal aprovadas sao lucrativas nas duas temporadas, mas nao sao estaveis por fase.
A maioria ficou classificada como OSCILANTE_PHASE6 e OSCILANTE_PHASE8.
```

Interpretação:

```text
A oscilacao por fase nao reprova automaticamente a familia.
Mas impede aprovacao operacional direta.
O ranking operacional deve penalizar familias com maior risco por fase.
```

---

## Familias No Goal consistentes na triagem

Top familias aprovadas como consistentes:

```text
1. team_winning_by_1_no_sot_against__no_goal — score 82,8
2. opponent_no_big_chances__no_goal — score 82,5
3. both_teams_cold_2of3__no_goal — score 78,7
4. opponent_no_recent_key_passes__no_goal — score 73,4
5. team_winning_by_1_low_dangerous_attacks_against__no_goal — score 71,1
```

Familias No Goal classificadas como oscilantes:

```text
team_winning_by_1_opp_cold_2of3__no_goal
favorite_winning_by_1_opp_cold_2of3__no_goal
```

---

## Hipoteses atualizadas apos comparacao 2024 x 2025

```text
1. Familias No Goal sao superiores a Goal/Over no agregado.
2. Goal/Over permanece estruturalmente pior que No Goal.
3. No Goal amadurece cedo nas duas temporadas comparadas.
4. A rodada 5 aparece como ponto forte para as familias No Goal analisadas.
5. A curva phase6/phase8 revela oscilacao importante.
6. A segmentacao por favorito importa, mas a melhor faixa ainda e inconclusiva.
7. Favorito forte nao deve ser automaticamente privilegiado.
8. Perfis de time sao informativos, mas nao devem dominar a validacao.
9. Ranking final deve considerar lucro + ROI + EV + DD + max losing streak + maturidade + oscilacao phase6/phase8.
```

---

## Frente atual

```text
RANKING_OPERACIONAL_FINAL_V1
```

Objetivo:

```text
Construir um ranking conservador das familias/variacoes candidatas, usando a triagem 2024 x 2025 como base, sem aprovar operacao final ainda.
```

Pergunta principal:

```text
Quais familias/variacoes merecem virar candidatas operacionais considerando lucro, ROI, EV, drawdown, max losing streak, maturidade e oscilacao por fase?
```

---

## Anatomia da estrategia — etapa futura

A analise detalhada da mecanica interna de cada estrategia, por exemplo:

```text
both_teams_cold_2of3
```

com estatisticas como:

```text
ataques perigosos
chutes no gol
chutes para fora
escanteios
posse
pressao
comportamento no placar
```

fica registrada como etapa futura:

```text
ANATOMIA_DA_ESTRATEGIA_V1
```

Essa etapa deve ocorrer somente depois que o ranking operacional identificar quais familias/variacoes realmente merecem virar candidatas operacionais.

---

## Roadmap a partir de agora

```text
1. RANKING_OPERACIONAL_FINAL_V1
2. VALIDACAO_OPERACIONAL_FINAL_V1
3. ANATOMIA_DA_ESTRATEGIA_V1
4. PLAYBOOK_OPERACIONAL_FINAL
```

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

Nenhuma estrategia, time, perfil de favorito, fase, rodada ou filtro deve ser aprovado operacionalmente antes do ranking, da validacao operacional final e da futura leitura de anatomia da estrategia.

A escolha futura deve priorizar:

- lucro final;
- ROI;
- EV por trade;
- drawdown maximo;
- sequencia maxima de perdas;
- consistencia por temporada;
- maturidade por rodada;
- estabilidade em phase6;
- estabilidade em phase8;
- oscilacao de lucro/ROI/DD;
- contexto de favorito como variavel, nao filtro automatico;
- duplicidades por familia/variacao.

---

## Restricoes

- Nao criar robo.
- Nao criar producao.
- Nao chamar simulacao com odds medias de backtesting financeiro real.
- Nao usar odds live inexistentes.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao aprovar operacao final durante a montagem do ranking.
