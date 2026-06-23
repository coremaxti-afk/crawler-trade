# PROJECT STATUS

## Estado Atual do Projeto

FASE ATUAL:

```text
POS-PLAYBOOK_OPERACIONAL_V1 — PREPARACAO DA ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1
```

O projeto concluiu o ciclo de pesquisa e consolidacao operacional da Serie A 2024/2025 e ja iniciou validacoes em Premier League 2024/25 x 2025/26.

Status oficial:

```text
PLAYBOOK_OPERACIONAL_V1 GERADO COMO DOCUMENTO OPERACIONAL CANDIDATO
GERADOR_PLAYBOOK_OPERACIONAL_V1 PLANEJADO/EM IMPLEMENTACAO PARA AUTOMATIZAR FUTURAS LIGAS
ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1 APROVADA COMO PROXIMA FRENTE
NENHUMA OPERACAO REAL APROVADA
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

Se uma solicitacao pular etapas, misturar objetivos, fragilizar a metodologia, inflar lucro/ROI/robustez ou gerar falsa confianca operacional, o agente deve discordar primeiro, explicar o risco tecnico e propor o caminho correto.

---

## Ordem oficial do pipeline analitico

A ordem logica dos scripts/etapas do projeto, do Discovery ate o Playbook, e:

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

Observacao:

```text
ANALISE_REGIME_POR_FASE_V1_GLOBAL serve para ler o regime geral da liga por Goal/No Goal e por familia.
ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1 deve servir para decisao operacional: olhar apenas carteira principal + observacao + familias Goal/Over menos piores ou dependentes de fase.
```

---

## Entregas ja realizadas e que devem constar no projeto

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

Correcoes de documentacao:

```text
VALIDACAO_OPERACIONAL_FINAL_V1 incorporou a logica explicita auditada pela V1.1.
VALIDACAO_OPERACIONAL_FINAL_V1_1 fica como auditoria historica, nao como frente oficial separada.
```

---

## Modelo mental oficial atualizado

O projeto deve analisar uma liga/temporada em cinco dimensoes principais:

```text
1. Tendencia da liga
   A liga puxa mais para Goal/Over ou No Goal/Under?

2. Comportamento dos favoritos
   Favorito forte, medio, fraco ou jogo parelho muda o padrao?

3. Comparacao entre temporadas
   A familia sobrevive, oscila ou quebra entre temporadas?

4. Maturidade / previsibilidade
   A partir de qual rodada a liga ou familia fornece sinal confiavel?

5. Regime por fase
   Em quais fases do calendario cada direcao/familia funciona ou quebra?
```

Interpretacao importante:

```text
Uma estrategia Goal/Over pode ser ruim no agregado anual e ainda assim ser lucrativa em uma fase especifica.
Portanto Goal/Over nao deve ser descartado apenas pela temporada inteira; deve ser classificado como potencialmente DEPENDENTE_DE_REGIME quando houver fase forte recorrente.
```

---

## Status das conclusoes principais

### Serie A 2024 x 2025

```text
No Goal/Under foi superior no agregado das duas temporadas.
Goal/Over foi fraco no agregado anual.
Familias No Goal amadureceram cedo.
Favorito forte nao deve ser usado como filtro automatico.
Padrões por time sao informativos, mas nao devem virar blacklist automatica.
```

Carteira candidata consolidada da Serie A:

```text
CARTEIRA_PRINCIPAL:
- opponent_no_big_chances__no_goal
- team_winning_by_1_no_sot_against__no_goal
- both_teams_cold_2of3__no_goal

CARTEIRA_OBSERVACAO:
- team_winning_by_1_opp_cold_2of3__no_goal
- opponent_no_recent_key_passes__no_goal
- favorite_winning_by_1_opp_cold_2of3__no_goal
- team_winning_by_1_low_dangerous_attacks_against__no_goal
```

### Premier League 2024/25 x 2025/26

```text
O pipeline ja foi executado em multiplas frentes da Premier League.
A validacao operacional final da Premier League 2025/26 retornou 0 familias em carteira principal e 7 em observacao.
Isso indica que o framework esta conservador e que a liga ainda exige validacao por regime/familia antes de qualquer playbook operacional forte.
```

Achado importante em Premier League:

```text
Goal/Over e muito dependente de regime.
Na Premier League 2024/25 e 2025/26, fases intermediarias repetiram lucro forte para Goal/Over, apesar do agregado anual ser fraco/instavel.
```

---

## Nova frente oficial aprovada

```text
ANALISE_REGIME_DAS_FAMILIAS_SELECIONADAS_V1
```

Objetivo:

```text
Analisar apenas familias/variacoes selecionadas ou candidatas, separando:
- carteira principal;
- carteira observacao;
- familias Goal/Over dependentes de fase;
- familias menos piores por regime.
```

Perguntas principais:

```text
1. Em quais fases cada familia selecionada funciona melhor?
2. A fase forte se repete entre temporadas?
3. Quais fases devem ser evitadas?
4. Existem familias Goal/Over ruins no agregado, mas lucrativas em fases recorrentes?
5. O regime por fase melhora a leitura operacional sem criar filtro artificial?
```

Status:

```text
APROVADA COMO PROXIMA ETAPA
NAO EXECUTADA AINDA
NAO APROVA OPERACAO REAL
```

---

## Papel do regime global vs regime das selecionadas

```text
REGIME GLOBAL:
Serve para entender o clima da liga e a direcao Goal/No Goal por fase.
Pode ser contaminado por familias ruins.
Nao deve decidir operacao sozinho.

REGIME DAS FAMILIAS SELECIONADAS:
Serve para olhar apenas candidatas relevantes e entender onde cada uma funciona.
E a camada operacional do estudo de regime.
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

Nenhuma estrategia, time, perfil de favorito, fase, rodada ou filtro esta aprovado para operacao real.

A escolha futura deve priorizar:

- lucro final;
- ROI;
- EV por trade;
- drawdown maximo;
- sequencia maxima de perdas;
- consistencia por temporada;
- maturidade por rodada;
- comportamento em phase6;
- comportamento em phase8;
- oscilacao de lucro/ROI/DD;
- contexto de favorito como variavel, nao filtro automatico;
- duplicidades por familia/variacao;
- regime por fase apenas quando houver repeticao e justificativa.

---

## Restricoes

- Nao criar robo.
- Nao criar producao.
- Nao chamar simulacao com odds medias de backtesting financeiro real.
- Nao usar odds live inexistentes.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao transformar fase forte isolada em regra operacional sem validacao.
- Nao aprovar operacao real durante a montagem do playbook ou dos estudos de regime.
