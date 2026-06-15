# CURRENT SPRINT

## Sprint Atual

Status:

```text
AUDITORIA DE DRAWDOWN DAS ESTRATEGIAS ORIGINAIS
VALIDACAO MULTI-LIGA INICIADA
```

Frente oficial ativa:

```text
SPORTMONKS_STRATEGY_DRAWDOWN_AUDIT_V1
```

Proxima frente:

```text
MULTI_LEAGUE_DRAWDOWN_AUDIT_V1
```

---

## Concluido

- [x] Validacao semantica de trends.
- [x] Validacao de participant_id por time.
- [x] Validacao de cutoffs 60/65/70/75.
- [x] Validacao de janelas 5/10/15 minutos.
- [x] Descoberta de estrategias por lado/time EPL.
- [x] Integracao com Football-Data para favorito.
- [x] Encerrar `SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1/V2`.
- [x] Formalizar agente 06 - Trade Operations Quant.
- [x] Criar playbooks operacionais V1/V2/V3.
- [x] Identificar risco de confusao por filtros/agregacoes de playbook V3.
- [x] Retornar para estrategias originais.
- [x] Criar script de auditoria de drawdown por estrategia/temporada.
- [x] Auditar drawdown EPL 2024/25 e EPL 2025/26.
- [x] Iniciar discovery multi-liga com La Liga 2025/26.

---

## Decisao Operacional Atual

A documentacao de playbooks V3 permanece como referencia operacional, mas a selecao de estrategias volta a usar:

```text
estrategias originais
sem filtros V3 por padrao
sem agregacao de targets
sem juntar estrategias parecidas
```

Prioridade atual:

```text
lucro final + ROI + EV + drawdown + sequencia maxima de perdas
```

---

## Estrategias Prioritarias EPL apos Drawdown Audit

### Lay Over / No Goal

- `team_winning_by_1_opp_cold_2of3 | 65 | no_goal_65_80 | last_10m`
- `favorite_winning_by_1_opp_cold_2of3 | 65 | no_goal_65_80 | last_10m`
- `favorite_winning_by_1_opp_cold_2of3 | 70 | no_goal_70_85 | last_15m` em observacao forte

### Back Over / Goal

- `home_winning_by_1_visitor_pressing | 75 | goal_75_90`

Pausar/descartar:

- `home_winning_by_1_visitor_pressing | 70 | goal_70_80 | last_15m`

---

## La Liga 2025/26 - Discovery Inicial

Status:

```text
APROVADO COM RESSALVAS PARA AUDITORIA OPERACIONAL
```

Resumo:

```text
714 combinacoes avaliadas
28 PROMISSOR
442 OBSERVACAO
244 DESCARTADO
```

Principais candidatas para auditoria:

- `favorite_drawing_pressure_high_2of3 | 60 | goal_60_75 | last_10m`
- `away_winning_by_1_home_pressing | 70 | goal_70_90 | last_15m`
- `key_passes_recent_high | 65 | goal_65_85 | last_10m`
- `both_teams_cold_2of3 | 75 | no_goal_75_90 | last_5m`
- `favorite_winning_by_1_opp_cold_2of3 | 60 | no_goal_60_80 | last_10m`

---

## Proximas Etapas

- [ ] Rodar drawdown audit nas estrategias La Liga 2025/26.
- [ ] Comparar EPL vs La Liga por estrategia/familia.
- [ ] Manter estrategias, targets e temporadas separados.
- [ ] Auditar duplicidades em `both_teams_cold_2of3`.
- [ ] Decidir top estrategias por lucro final, ROI, EV e drawdown.
- [ ] Documentar tutorial de uso do script para novas ligas/temporadas.

---

## Restricoes

- Nao criar robo.
- Nao executar trade real.
- Nao criar producao.
- Nao fazer backtesting financeiro real.
- Nao usar odds live nao timestampadas.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.

Todas as simulacoes com odds medias devem ser classificadas como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```
