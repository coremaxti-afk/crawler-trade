# SPORTMONKS_OPERATIONAL_ACTION_PLAN_V1

## Status

```text
PLANO DE ACAO PARA PM
```

Este documento registra o plano de acao apos a avaliacao estatistica SportMonks e a avaliacao operacional preliminar do Agente 06.

Importante:

```text
Captura de odds live/historicas timestampadas esta fora de escopo neste momento.
```

Portanto, a proxima fase deve seguir com simulacoes operacionais usando odds medias observadas do projeto.

---

## Contexto

A frente SportMonks Team-Side Strategy Discovery encontrou estrategias promissoras por lado/time, especialmente:

- Back Over tardio no minuto 75;
- Under / Lay Over hold em cenarios frios;
- favoritos vencendo por 1 com adversario frio;
- mandante vencendo por 1 com visitante pressionando.

A avaliacao do Agente 06 indicou que algumas frentes podem ser operacionalmente interessantes, principalmente:

```text
Back Over no minuto 75
```

Motivo:

```text
Mesmo com taxa de acerto menor, a odd alta pode compensar e gerar EV positivo.
```

---

## Decisao Estrategica

Nao priorizar captura de odds live neste ciclo.

Seguir com:

```text
SIMULACOES OPERACIONAIS COM ODDS MEDIAS OBSERVADAS
```

Ressalva obrigatoria:

```text
Essas simulacoes nao sao backtesting financeiro real.
Devem ser marcadas como ESTIMATIVA OPERACIONAL.
```

---

## Plano de Acao

### 1. Congelar Whitelist V1

Criar uma lista oficial de estrategias candidatas para avaliacao operacional.

Separar em duas familias:

```text
UNDER HOLD V1
OVER WINDOW V1
```

### UNDER HOLD V1

Candidatas:

- `favorite_winning_by_1_opp_cold_2of3`
- `both_teams_cold_2of3`
- `team_winning_by_1_opp_cold_2of3`
- `favorite_winning_by_1 + h8_cold_combo_10m_2of3`
- `favorite_winning_by_1 + h8_pressure_score_10m_bottom25`

Objetivo:

```text
Encontrar operacoes em que faz sentido segurar ate 80/90 ou ate o fim do mercado.
```

### OVER WINDOW V1

Candidatas:

- `home_winning_by_1_visitor_pressing`
- estrategias `goal_75_90` com pressao recente;
- estrategias `goal_70_85` com pressao recente;
- estrategias em que time perdendo/favorito pressiona.

Objetivo:

```text
Capturar gol em janela curta/tardia, especialmente Back Over 75.
```

---

## 2. Robustez Estatistica

Antes de promover qualquer estrategia, testar estabilidade contra pequenas variacoes:

- cutoff 70 vs 75;
- janela last_5m vs last_10m vs last_15m;
- home vs away;
- favorito por menor odd vs sem filtro favorito;
- vantagem de 1 gol vs empate/perdendo;
- target 75-85 vs 75-90.

Pergunta principal:

```text
A estrategia continua boa quando os parametros mudam um pouco?
```

---

## 3. Simulacao Operacional Padronizada

Agente responsavel:

```text
06 - Trade Operations Quant
```

Simular para cada estrategia:

- lucro total;
- ROI;
- EV por trade;
- break-even;
- lucro medio por trade;
- drawdown simples;
- sequencia maxima de perdas;
- hold vs cashout;
- sensibilidade de odds.

Separar claramente:

```text
HOLD
CASHOUT FIXO
CASHOUT DINAMICO ESTIMADO
```

Separar mercados:

```text
Back Over
Lay Over
Back Under
Conversao Back Under -> Lay Over
```

---

## 4. Odds Medias Oficiais para Simulacao

Documento de referencia:

```text
docs/04_RESEARCH/OPERACIONAL_TRADE_TOP_STRATEGIES_V1.md
```

Curva media observada do mercado Proximo Gol:

| Minuto | Odd Back Over equivalente |
|---:|---:|
| 60 | 1.50 |
| 65 | 1.60 |
| 70 | 1.80 |
| 75 | 2.00 |
| 80 | 2.45 |
| 85 | 3.35 |

Ressalva:

```text
Odds medias observadas manualmente.
Nao sao odds live historicas timestampadas.
```

Se a origem for Back Under, converter para Over equivalente:

```text
Odd_Over = Odd_Under / (Odd_Under - 1)
```

---

## 5. Playbooks Operacionais

Criar playbooks somente para estrategias aprovadas pelo Agente 06.

Exemplo:

```text
PLAYBOOK 001 - Back Over 75-90
Entrada: 75'
Condicao: mandante vencendo por 1 + visitante pressionando
Mercado: Back Over Proximo Gol
Saida: gol ou fim da janela
Status: estimativa operacional
```

Exemplo:

```text
PLAYBOOK 002 - Under Hold Frio
Entrada: 60/65/70
Condicao: favorito vencendo por 1 + adversario frio
Mercado: Lay Over / Back Under Proximo Gol
Saida: hold ate 80/90 ou fim do mercado
Status: estimativa operacional
```

---

## 6. Criterios de Avanco

Uma estrategia so pode avancar se tiver:

- parecer estatistico promissor;
- parecer operacional do Agente 06;
- EV positivo na simulacao;
- ROI positivo;
- break-even viavel;
- sensibilidade aceitavel a odds;
- drawdown simples toleravel;
- sem leakage.

Vereditos possiveis:

```text
APROVADO OPERACIONALMENTE
APROVADO COM RESSALVAS
NAO COMPENSA FINANCEIRAMENTE
```

---

## 7. Proxima Tarefa para PM

Acionar o PM para:

1. Registrar que captura de odds live esta fora de escopo.
2. Aprovar uso de simulacoes com odds medias como estimativa operacional.
3. Abrir frente oficial:

```text
SPORTMONKS_OPERATIONAL_PLAYBOOKS_V1
```

4. Encaminhar as estrategias promissoras ao Agente 06.
5. Somente depois consolidar os playbooks aprovados.

---

## Decisao Atual

```text
PROSSEGUIR COM SIMULACOES OPERACIONAIS BASEADAS EM ODDS MEDIAS
```

Nao promover para robo, producao, trade real ou backtesting financeiro real.
