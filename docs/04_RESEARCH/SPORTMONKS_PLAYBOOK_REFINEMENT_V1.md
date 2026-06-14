# SPORTMONKS_PLAYBOOK_REFINEMENT_V1

## Objetivo

Lapidar os playbooks operacionais aprovados sem criar novas estratégias.

## Playbooks congelados

- BO_75_HOME_WINNING_BY_1_VISITOR_PRESSING
- LO_65_TEAM_WINNING_BY_1_OPP_COLD_2OF3
- LO_65_FAVORITE_WINNING_BY_1_OPP_COLD_2OF3

Status:

```text
APROVADO COM RESSALVAS
```

## Regras

- Não criar novas estratégias.
- Não alterar features-base.
- Não criar modelos.
- Não criar produção.
- Não realizar trade real.

## Refinamentos permitidos

### Cutoff
- 65 vs 70 vs 75

### Janela
- last_5m
- last_10m
- last_15m

### Contexto
- mandante vs visitante
- favorito forte vs favorito leve
- vitória por 1 vs vitória por 2

### Mercado
- odd mínima operacional
- hold vs cashout
- sensibilidade ±0.10

## Critério de promoção

Um playbook pode avançar para V2 se:

- confirmar em EPL 24/25 e 25/26;
- manter EV positivo;
- manter ROI positivo;
- apresentar robustez a pequenas mudanças;
- não apresentar leakage.

## Decisão

```text
REFINAMENTO CONTROLADO ANTES DE QUALQUER PRODUÇÃO
```