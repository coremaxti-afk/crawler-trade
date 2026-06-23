# ROADMAP_OPERACIONAL_ATUAL_V1

## Status

```text
PLAYBOOK_OPERACIONAL_V1 CONCLUIDO COMO CANDIDATO
PROXIMA FRENTE: ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1
```

Este documento substitui a leitura antiga de pre-ranking. O projeto ja passou por ranking/selecao, validacao operacional, anatomia e playbook candidato.

---

## Governanca obrigatoria

Antes de executar qualquer nova frente, todos os agentes devem seguir:

```text
docs/00_AGENTS/GOVERNANCE_V2.md
```

Regra central: nenhum agente deve concordar com o usuario apenas para agradar. Se uma solicitacao pular etapas, misturar objetivos, fragilizar a metodologia, inflar lucro/ROI/robustez ou gerar falsa confianca operacional, o agente deve discordar primeiro, explicar o risco tecnico e propor o caminho correto.

---

## Pipeline oficial atualizado

```text
1. DISCOVERY_V4
2. NORMALIZACAO_FIXTURE_LEVEL
3. DRAWDOWN_V4
4. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
5. ANALISE_REGIME_POR_FASE_V1_GLOBAL
6. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
7. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
8. ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1
9. COMPARACAO_MULTI_LIGA_TEMPORADA_QUALIDADE_E_OSCILACAO_V1.1
10. ANATOMIA_NUMERICA_DAS_FAMILIAS_APROVADAS_V1
11. SELECAO_DAS_VARIACOES_OFICIAIS_POR_FAMILIA_V1
12. VALIDACAO_OPERACIONAL_FINAL_V1
13. PLAYBOOK_OPERACIONAL_V1
14. GERADOR_PLAYBOOK_OPERACIONAL_V1
15. ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1
```

---

## Entregas registradas como concluidas

```text
AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
ANALISE_REGIME_POR_FASE_V1
ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1
COMPARACAO_MULTI_LIGA_TEMPORADA_QUALIDADE_E_OSCILACAO_V1.1
ANATOMIA_NUMERICA_DAS_FAMILIAS_APROVADAS_V1
SELECAO_DAS_VARIACOES_OFICIAIS_POR_FAMILIA_V1
VALIDACAO_OPERACIONAL_FINAL_V1
PLAYBOOK_OPERACIONAL_V1
GERADOR_PLAYBOOK_OPERACIONAL_V1
```

Observacao:

```text
VALIDACAO_OPERACIONAL_FINAL_V1_1 foi uma auditoria/correcao documental.
A logica foi incorporada na V1.
Nao deve ser tratada como frente oficial separada.
```

---

## Resultado consolidado da Serie A

### Carteira principal candidata

```text
opponent_no_big_chances__no_goal
team_winning_by_1_no_sot_against__no_goal
both_teams_cold_2of3__no_goal
```

### Carteira observacao

```text
team_winning_by_1_opp_cold_2of3__no_goal
opponent_no_recent_key_passes__no_goal
favorite_winning_by_1_opp_cold_2of3__no_goal
team_winning_by_1_low_dangerous_attacks_against__no_goal
```

Status:

```text
CARTEIRA CANDIDATA
NAO APROVA OPERACAO REAL
```

---

## Resultado consolidado da Premier League

A Premier League ja possui execucoes para as principais frentes do pipeline, incluindo comparacao 2024/25 x 2025/26, anatomia, selecao e validacao operacional.

Leitura atual:

```text
Carteira principal Premier League 2025/26: 0 familias.
Carteira observacao Premier League 2025/26: 7 familias.
```

Interpretacao:

```text
A Premier League ainda nao deve gerar playbook operacional forte sem analisar regime das familias selecionadas.
```

---

## Modelo mental oficial do projeto

O projeto deve avaliar uma estrategia/familia em cinco camadas:

```text
1. Tendencia da liga
   Goal/Over ou No Goal/Under predomina?

2. Comportamento dos favoritos
   Favorito forte, medio, fraco ou jogo parelho muda o padrao?

3. Comparacao entre temporadas
   A familia sobrevive, oscila ou quebra?

4. Maturidade / previsibilidade
   A partir de qual rodada ha sinal confiavel?

5. Regime por fase
   Em quais fases da temporada a familia funciona ou quebra?
```

---

## Regime global vs regime das familias selecionadas

### Regime global

Objetivo:

```text
Entender o clima geral da liga por fase.
```

Uso correto:

```text
Leitura macro de Goal/No Goal e da mudanca de comportamento da temporada.
```

Limite:

```text
Pode estar contaminado por estrategias ruins.
Nao deve ser usado sozinho para decisao operacional.
```

### Regime das familias selecionadas

Objetivo:

```text
Analisar apenas familias/variacoes que passaram por filtros anteriores.
```

Uso correto:

```text
Identificar fases fortes, fracas, proibidas e recorrentes para cada familia candidata.
```

---

## Nova frente oficial

```text
ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1
```

### Objetivo

Analisar regime por fase apenas em subconjuntos relevantes:

```text
1. Carteira principal
2. Carteira observacao
3. Familias Goal/Over dependentes de fase
4. Variacoes oficiais selecionadas
5. Estrategias Goal menos piores quando houver evidencia de fase forte
```

### Perguntas obrigatorias

```text
1. Qual fase e forte por familia?
2. Qual fase e fraca/proibida por familia?
3. A fase forte se repete entre temporadas?
4. Existem estrategias Goal ruins no agregado, mas lucrativas em fase recorrente?
5. No Goal e estrutural ou tambem depende de fase?
6. O regime melhora a decisao sem criar overfitting?
```

### Saida esperada

Classificar por familia/variacao:

```text
REGIME_FORTE_RECORRENTE
REGIME_FORTE_ISOLADO
REGIME_OSCILANTE
REGIME_RISCO
REGIME_INCONCLUSIVO
```

---

## Observacao sobre Goal/Over

Goal/Over nao deve ser descartado apenas pelo agregado anual.

Nova regra interpretativa:

```text
Se Goal/Over for negativo no ano todo, mas tiver fase forte recorrente entre temporadas, classificar como DEPENDENTE_DE_REGIME, nao como REPROVADA definitiva.
```

Essa regra nao aprova operacao. Ela apenas preserva a hipotese para analise de regime das familias selecionadas.

---

## Ideia futura — nao aprovada ainda

```text
PADROES_MACRO_OPERACIONAIS_V1
```

Status:

```text
HIPOTESE FUTURA
NAO EXECUTAR AGORA
```

Motivo:

```text
Ainda falta consolidar o regime das familias selecionadas antes de agrupar familias em padroes macro como "time vencendo e adversario sem ataque real".
```

---

## Regra final

Nenhuma estrategia, filtro, perfil de time, contexto de favorito, rodada ou fase deve entrar como regra operacional definitiva antes de validacao suficiente.

Todos os resultados com odds medias devem permanecer rotulados como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```
