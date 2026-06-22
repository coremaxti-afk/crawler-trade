# CURRENT SPRINT

## Sprint Atual

Status:

```text
PREPARACAO DO RANKING_OPERACIONAL_FINAL_V1
```

Fase atual:

```text
POS-COMPARACAO BI-TEMPORADA 2024 X 2025
```

Frente oficial ativa:

```text
RANKING_OPERACIONAL_FINAL_V1
```

---

## Contexto

O projeto concluiu o roadmap exploratorio da Serie A 2025, processou a Serie A 2024 e concluiu a comparacao bi-temporada entre 2024 e 2025.

Status da comparacao:

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

Todos os agentes devem seguir:

```text
docs/00_AGENTS/GOVERNANCE_V2.md
```

Regra central:

```text
Nenhum agente deve concordar com o usuario apenas para agradar.
```

Se uma solicitacao pular etapas, misturar objetivos ou fragilizar a metodologia, o agente deve discordar primeiro e propor o caminho correto.

---

## Resultado aprovado da triagem bi-temporada

### Goal vs No Goal

```text
Goal/Over: reprovado no agregado das duas temporadas.
No Goal/Under: superior nas duas temporadas.
```

### Maturidade

```text
As principais familias No Goal amadureceram na rodada 5 em 2024 e 2025.
```

### Phase6 / Phase8

```text
As familias No Goal aprovadas sao lucrativas nas duas temporadas, mas apresentam oscilacao por fase.
A maioria ficou OSCILANTE_PHASE6 e OSCILANTE_PHASE8.
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

Familias No Goal oscilantes:

```text
team_winning_by_1_opp_cold_2of3__no_goal
favorite_winning_by_1_opp_cold_2of3__no_goal
```

Todas as familias Goal/Over ficaram reprovadas ou inconclusivas.

---

## Em andamento

### RANKING_OPERACIONAL_FINAL_V1

Objetivo:

```text
Construir um ranking conservador das familias/variacoes candidatas usando a triagem 2024 x 2025 como base.
```

A ranking deve considerar obrigatoriamente:

```text
lucro final
ROI
EV por trade
N
drawdown
max losing streak
maturidade por rodada
phase6_class
phase8_class
oscilacao entre temporadas
overlap/duplicidade por familia
```

Importante:

```text
Ranking nao significa operacao aprovada.
Ranking e uma lista priorizada de candidatas para validacao operacional final.
```

---

## Anatomia da Estrategia — futura, nao agora

A analise detalhada de mecanica interna, como ataques perigosos, chutes no gol, chutes para fora, escanteios e pressao, fica registrada para depois:

```text
ANATOMIA_DA_ESTRATEGIA_V1
```

Ela deve ser aplicada apenas nas familias/variacoes que sobreviverem ao ranking e a validacao operacional final.

---

## Proximas Etapas

- [ ] Gerar prompt para `RANKING_OPERACIONAL_FINAL_V1`.
- [ ] Executar ranking conservador das candidatas.
- [ ] Penalizar familias/variacoes com oscilacao forte em phase6/phase8.
- [ ] Separar candidatas fortes, candidatas com ressalva, oscilantes e reprovadas.
- [ ] Atualizar GitHub com o ranking.
- [ ] Preparar `VALIDACAO_OPERACIONAL_FINAL_V1`.
- [ ] Somente depois preparar `ANATOMIA_DA_ESTRATEGIA_V1`.

---

## Decisao Operacional Atual

Nenhuma estrategia, time, perfil de favorito, rodada ou fase deve ser aprovado operacionalmente durante o ranking.

A selecao futura deve priorizar:

```text
lucro final + ROI + EV + drawdown + sequencia maxima de perdas + maturidade por rodada + estabilidade phase6 + estabilidade phase8 + oscilacao entre temporadas + duplicidade por familia
```

---

## Restricoes

- Nao criar robo.
- Nao criar producao.
- Nao fazer backtesting financeiro real.
- Nao usar odds live nao timestampadas.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao aprovar operacao final durante montagem do ranking.

Todas as simulacoes com odds medias devem ser classificadas como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```
