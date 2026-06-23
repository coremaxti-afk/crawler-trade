# CURRENT SPRINT

## Sprint Atual

Status:

```text
PREPARACAO_ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1
```

Fase atual:

```text
POS-PLAYBOOK_OPERACIONAL_V1
```

Frente oficial ativa:

```text
ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1
```

---

## Contexto

O projeto concluiu o ciclo principal de pesquisa e consolidacao operacional:

```text
DISCOVERY
NORMALIZACAO_FIXTURE_LEVEL
DRAWDOWN_V4
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

A proxima frente aprovada e o estudo de regime aplicado apenas as familias selecionadas/candidatas.

---

## Governanca obrigatoria

Todos os agentes devem seguir:

```text
docs/00_AGENTS/GOVERNANCE_V2.md
```

Regra central:

```text
Nenhum agente deve concordar com o usuario apenas para agradar.
```

Se uma solicitacao pular etapas, misturar objetivos, fragilizar a metodologia, inflar lucro/ROI/robustez ou gerar falsa confianca operacional, o agente deve discordar primeiro e propor o caminho correto.

---

## Entregas consolidadas desde a comparacao bi-temporada

As entregas abaixo ja foram realizadas e devem ser consideradas parte do pipeline oficial:

```text
ANATOMIA_NUMERICA_DAS_FAMILIAS_APROVADAS_V1
SELECAO_DAS_VARIACOES_OFICIAIS_POR_FAMILIA_V1
VALIDACAO_OPERACIONAL_FINAL_V1
PLAYBOOK_OPERACIONAL_V1
GERADOR_PLAYBOOK_OPERACIONAL_V1
```

Correcao de documentacao:

```text
VALIDACAO_OPERACIONAL_FINAL_V1_1 foi incorporada como auditoria historica/documentacao da V1.
Nao e frente oficial separada.
```

---

## Modelo mental da validacao atual

O projeto agora deve pensar em cinco perguntas antes de qualquer leitura operacional:

```text
1. Tendencia da liga:
   A liga favorece Goal/Over ou No Goal/Under?

2. Favoritos:
   O comportamento muda com favorito forte, medio, fraco ou jogo parelho?

3. Comparacao entre temporadas:
   A familia sobrevive, oscila ou quebra?

4. Maturidade / previsibilidade:
   A partir de qual rodada a familia ou liga se torna confiavel?

5. Regime por fase:
   Em quais fases do calendario a familia funciona ou quebra?
```

---

## Resultado atual da Serie A

Carteira candidata consolidada:

### CARTEIRA_PRINCIPAL

```text
opponent_no_big_chances__no_goal
team_winning_by_1_no_sot_against__no_goal
both_teams_cold_2of3__no_goal
```

### CARTEIRA_OBSERVACAO

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

## Resultado atual da Premier League

A Premier League ja possui entregas para:

```text
AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
ANALISE_REGIME_POR_FASE_V1
ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1
COMPARACAO_MULTI_LIGA_TEMPORADA_QUALIDADE_E_OSCILACAO_V1
ANATOMIA_NUMERICA_DAS_FAMILIAS_APROVADAS_V1
SELECAO_DAS_VARIACOES_OFICIAIS_POR_FAMILIA_V1
VALIDACAO_OPERACIONAL_FINAL_V1
```

Leitura atual:

```text
VALIDACAO_OPERACIONAL_FINAL_V1_PREMIER_LEAGUE_2025_26 indicou 0 familias em carteira principal e 7 em observacao.
Premier League exige leitura de regime/familia antes de qualquer playbook forte.
```

Ponto critico:

```text
Goal/Over pode ser negativo no agregado anual, mas lucrativo em fases especificas.
Portanto Goal/Over deve ser tratado como DEPENDENTE_DE_REGIME quando houver repeticao de fase forte.
```

---

## Em andamento

### ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1

Objetivo:

```text
Pegar apenas as familias selecionadas/candidatas e identificar em quais fases elas funcionam, quebram ou ficam inconclusivas.
```

Escopo inicial:

```text
1. Carteira principal
2. Carteira observacao
3. Familias Goal/Over menos piores ou dependentes de regime
4. Variacoes oficiais selecionadas
```

Perguntas obrigatorias:

```text
1. Qual fase e forte para cada familia?
2. Qual fase e fraca/proibida para cada familia?
3. A fase forte se repete entre temporadas?
4. Goal/Over tem familias que devem sair de reprovadas para DEPENDENTE_DE_REGIME?
5. No Goal continua estrutural ou tambem vira regime-dependente?
```

Importante:

```text
Este estudo nao aprova operacao real.
Ele organiza o regime das candidatas para melhorar o playbook futuro.
```

---

## Proximas Etapas

- [ ] Gerar prompt para `ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1`.
- [ ] Executar regime apenas em familias selecionadas/candidatas.
- [ ] Separar fases fortes, fracas e proibidas por familia.
- [ ] Verificar repeticao entre temporadas.
- [ ] Atualizar playbook com leitura de regime quando houver evidencia suficiente.
- [ ] Manter `PADROES_MACRO_OPERACIONAIS_V1` apenas como ideia futura, nao etapa oficial atual.

---

## Decisao Operacional Atual

Nenhuma estrategia, time, perfil de favorito, rodada ou fase deve ser aprovado operacionalmente.

A selecao futura deve priorizar:

```text
lucro final + ROI + EV + drawdown + sequencia maxima de perdas + maturidade por rodada + estabilidade/risco phase6 + estabilidade/risco phase8 + oscilacao entre temporadas + duplicidade por familia + repeticao de regime por temporada
```

---

## Restricoes

- Nao criar robo.
- Nao criar producao.
- Nao fazer backtesting financeiro real.
- Nao usar odds live nao timestampadas.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao transformar fase forte isolada em regra operacional.
- Nao aprovar operacao final durante analise de regime.

Todas as simulacoes com odds medias devem ser classificadas como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```
