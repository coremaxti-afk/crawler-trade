# PROJECT STATUS

## Estado Atual do Projeto

FASE ATUAL:

```text
TRANSICAO PARA PLAYBOOKS OPERACIONAIS
```

Frente encerrada:

```text
SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1/V2
STATUS: CONCLUIDO
DECISAO: APROVADO COM RESSALVAS
```

Objetivos atingidos:

- validacao semantica de trends;
- validacao de participant_id por time;
- validacao de cutoffs 60/65/70/75;
- validacao de janelas 5/10/15 minutos;
- descoberta de estrategias por lado/time;
- integracao Football-Data para definicao de favorito.

---

## Descobertas Principais

### UNDER HOLD

Estrategias de destaque:

- favorite_winning_by_1_opp_cold_2of3
- both_teams_cold_2of3
- team_winning_by_1_opp_cold_2of3

Resultado:

- taxas acima de 80% em alguns cenarios;
- evidencia de robustez para hold ate 80/90;
- alinhamento com historico SofaScore.

### OVER WINDOW

Principal descoberta:

```text
home_winning_by_1_visitor_pressing
75 -> goal_75_90
```

Metricas:

- N = 36
- taxa = 63.9%
- diff = +16.8 p.p.
- p = 0.041

Conclusao:

Estrategias com taxa menor podem superar estrategias Under devido ao payoff maior.

---

## Descoberta Estrategica do Projeto

```text
Alta taxa de acerto != maior lucratividade.
```

Por isso o agente oficial:

```text
06 - Trade Operations Quant
```

passa a ser obrigatorio para:

- ROI;
- EV;
- break-even;
- hold vs cashout;
- drawdown;
- sensibilidade de odds;
- lucro operacional.

Nenhuma estrategia estatistica pode ser operacionalmente aprovada sem passar pelo agente 06.

---

## Politica Oficial de Odds

O projeto seguira com:

```text
SIMULACOES OPERACIONAIS BASEADAS EM ODDS MEDIAS OBSERVADAS
```

Curva operacional atual:

```text
60 = 1.40
65 = 1.60
70 = 1.80
75 = 2.00
80 = 2.45
85 = 3.35
```

Ressalva obrigatoria:

```text
Nao constitui backtesting financeiro real.
Classificar como ESTIMATIVA OPERACIONAL.
```

---

## Progresso Recente do Agente 06

Foi registrado o documento:

```text
docs/04_RESEARCH/OPERACOES_TRADE/BREAK_EVEN_BY_TIME_WINDOW_V1.md
```

O documento consolida os pontos de break-even por faixa de tempo para:

- Under / Lay Over;
- Over / Back Over.

Regra operacional registrada:

```text
Taxa > break-even => lucrativo
Taxa = break-even => zero a zero
Taxa < break-even => prejuizo
```

Nova metrica recomendada para priorizacao de playbooks:

```text
edge = strike_rate - break_even_rate
```

Tambem foi reforcado que:

- janelas terminadas em 90 sao HOLD_FINAL;
- janelas encerradas antes de 90 sao CASHOUT_ESTIMADO;
- cashout antes de 90 nao pode ser tratado como lucro/prejuizo cheio de hold final.

---

## Proxima Frente Oficial

```text
SPORTMONKS_OPERATIONAL_PLAYBOOKS_V1
```

Objetivo:

Transformar estrategias aprovadas estatistica e operacionalmente em playbooks de execucao.

Exemplo:

```text
Back Over 75
Entrada: 75'
Condicao: visitante pressionando mandante vencendo por 1
Saida: gol ou fim da janela
Status: estimativa operacional
```

Acoes aprovadas:

1. Congelar whitelist de estrategias.
2. Criar familias UNDER HOLD V1.
3. Criar familias OVER WINDOW V1.
4. Executar avaliacao pelo agente 06.
5. Construir playbooks operacionais.
6. Nao promover para producao ou trade real.
