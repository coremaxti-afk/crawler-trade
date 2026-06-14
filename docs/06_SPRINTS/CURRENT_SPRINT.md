# CURRENT SPRINT

## Sprint Atual

Status:

```text
DISCOVERY SPORTMONKS CONCLUIDO
MIGRACAO PARA PLAYBOOKS OPERACIONAIS
```

Nova frente oficial:

```text
SPORTMONKS_OPERATIONAL_PLAYBOOKS_V1
```

---

## Concluido

- [x] Validacao semantica de trends.
- [x] Validacao de participant_id por time.
- [x] Validacao de cutoffs 60/65/70/75.
- [x] Validacao de janelas 5/10/15 minutos.
- [x] Descoberta de estrategias por lado/time.
- [x] Integracao com Football-Data para favorito.
- [x] Encerrar `SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1/V2`.
- [x] Formalizar agente 06 - Trade Operations Quant.

---

## Estrategias Prioritarias

### UNDER HOLD V1

- favorite_winning_by_1_opp_cold_2of3
- both_teams_cold_2of3
- team_winning_by_1_opp_cold_2of3

### OVER WINDOW V1

- home_winning_by_1_visitor_pressing
- janela 75 -> goal_75_90
- N=36
- taxa=63.9%
- p=0.041

---

## Proximas Etapas

- [ ] Congelar whitelist oficial de estrategias.
- [ ] Enviar estrategias ao agente 06.
- [ ] Calcular EV, ROI e break-even.
- [ ] Construir playbooks operacionais.
- [ ] Classificar tudo como ESTIMATIVA OPERACIONAL.
- [ ] Nao promover para producao.

---

## Restricoes

- Nao criar robo.
- Nao executar trade real.
- Nao criar producao.
- Nao fazer backtesting financeiro real.
- Nao usar odds live nao timestampadas.

Todas as simulacoes com odds medias devem ser classificadas como:

```text
ESTIMATIVA OPERACIONAL
```
