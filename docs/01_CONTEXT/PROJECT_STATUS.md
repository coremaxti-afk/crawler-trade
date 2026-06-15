# PROJECT STATUS

## Estado Atual do Projeto

FASE ATUAL:

```text
AUDITORIA DE RISCO DAS ESTRATEGIAS ORIGINAIS + VALIDACAO MULTI-LIGA
```

Frentes encerradas:

```text
SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_V1/V2
STATUS: CONCLUIDO
DECISAO: APROVADO COM RESSALVAS
```

```text
SPORTMONKS_OPERATIONAL_PLAYBOOKS_V1/V2/V3
STATUS: DOCUMENTADO, MAS PAUSADO COMO FRENTE PRINCIPAL
DECISAO: USAR COMO REFERENCIA, NAO COMO BASE FINAL DE LUCRO
```

Frente atual:

```text
SPORTMONKS_STRATEGY_DRAWDOWN_AUDIT_V1
STATUS: ATIVA
DECISAO: APROVADO COM RESSALVAS PARA AUDITORIA DE RISCO DAS ESTRATEGIAS ORIGINAIS
```

Nova frente de validacao:

```text
SPORTMONKS_MULTI_LEAGUE_DISCOVERY_VALIDATION
STATUS: INICIADA
PRIMEIRA LIGA: LA LIGA 2025/26
```

---

## Objetivos ja atingidos

- validacao semantica de SportMonks trends;
- validacao de participant_id por time;
- validacao de cutoffs 60/65/70/75;
- validacao de janelas 5/10/15 minutos;
- descoberta de estrategias por lado/time;
- integracao Football-Data para definicao de favorito;
- avaliacao financeira inicial pelo agente 06;
- criacao dos playbooks operacionais V1/V2/V3;
- identificacao de inconsistencia causada por agregacao/filtros dos playbooks;
- retorno para estrategias originais;
- criacao de auditoria de drawdown por estrategia e temporada.

---

## Mudanca de decisao operacional

A frente de playbooks V3 gerou especificacoes uteis, mas tambem complicou a leitura de lucro final porque aplicou filtros e agregacoes que mudaram N e profit em relacao as estrategias originais.

Decisao atual:

```text
Priorizar estrategias originais, sem filtros V3, sem agregacao de targets e sem juntar estrategias parecidas.
```

A partir deste ponto, a escolha de estrategias deve priorizar:

- lucro final;
- ROI;
- EV por trade;
- drawdown maximo;
- sequencia maxima de perdas;
- consistencia por temporada;
- duplicidades.

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

## Descoberta Estrategica do Projeto

```text
Alta taxa de acerto != maior lucratividade.
Baixa taxa de acerto pode ser lucrativa com odds altas.
```

Por isso o agente oficial:

```text
06 - Trade Operations Quant
```

continua obrigatorio para:

- ROI;
- EV;
- break-even;
- hold vs cashout;
- drawdown;
- sensibilidade de odds;
- lucro operacional.

Nenhuma estrategia estatistica pode ser operacionalmente aprovada sem passar por avaliacao operacional.

---

## Resultado da Auditoria de Drawdown EPL

Documento base:

```text
docs/04_RESEARCH/STRATEGY_DRAWDOWN_AUDIT_RESULTS_V1.md
```

Melhor estrategia geral por consistencia e lucro nas duas temporadas:

```text
team_winning_by_1_opp_cold_2of3
65' | no_goal_65_80 | last_10m
```

Resultados:

| Temporada | N | Strike | Profit | ROI | EV/trade | Max DD | Loss streak |
|---|---:|---:|---:|---:|---:|---:|---:|
| EPL 2024/25 | 55 | 72.7% | +3100 | +56.4% | +56.4 | -120 | 2 |
| EPL 2025/26 | 46 | 80.4% | +3160 | +68.7% | +68.7 | -120 | 2 |

Melhor Back Over original:

```text
home_winning_by_1_visitor_pressing
75' | goal_75_90
```

Resultados principais:

| Temporada | Janela | N | Strike | Profit | ROI | EV/trade | Max DD |
|---|---|---:|---:|---:|---:|---:|---:|
| EPL 2024/25 | last_10m | 47 | 59.6% | +900 | +19.1% | +19.1 | -600 |
| EPL 2025/26 | last_5m | 36 | 63.9% | +1000 | +27.8% | +27.8 | -300 |

Estrategia pausada/descartada:

```text
home_winning_by_1_visitor_pressing
70' | goal_70_80 | last_15m
```

Motivo: prejuizo e drawdown alto em ambas temporadas.

---

## Estrategias originais prioritarias atuais

### Lay Over / No Goal

1. `team_winning_by_1_opp_cold_2of3 | 65 | no_goal_65_80 | last_10m`
2. `favorite_winning_by_1_opp_cold_2of3 | 65 | no_goal_65_80 | last_10m`
3. `favorite_winning_by_1_opp_cold_2of3 | 70 | no_goal_70_85 | last_15m` em observacao forte

### Back Over / Goal

1. `home_winning_by_1_visitor_pressing | 75 | goal_75_90`
2. `favorite_drawing_pressure_high_2of3 | 60 | goal_60_75` em validacao La Liga
3. `away_winning_by_1_home_pressing | 70 | goal_70_90` em validacao La Liga
4. `key_passes_recent_high | 65 | goal_65_85` em validacao La Liga

---

## La Liga 2025/26 Discovery

Primeira frente multi-liga avaliada:

```text
sportmonks_team_side_strategy_discovery_summary_v2_la_liga_2025_26_tempos_expandidos222.csv
```

Resumo:

```text
714 combinacoes avaliadas
28 PROMISSOR
442 OBSERVACAO
244 DESCARTADO
```

Distribuicao dos promissores:

```text
Over janela curta: 19
Under/Lay Over: 9
```

Principais sinais:

- `favorite_drawing_pressure_high_2of3 | 60 | goal_60_75 | last_10m` — N=59, strike=50.8%, diff=+15.8 pp, p=0.010;
- `away_winning_by_1_home_pressing | 70 | goal_70_90 | last_15m` — N=49, strike=65.3%, diff=+13.7 pp, p=0.055;
- `key_passes_recent_high | 65 | goal_65_85 | last_10m` — N=205, strike=49.8%, diff=+9.5 pp, p=0.0015;
- `both_teams_cold_2of3 | 75 | no_goal_75_90 | last_5m` — N=136, strike=66.2%, diff=+10.4 pp, p=0.0076;
- `favorite_winning_by_1_opp_cold_2of3 | 60 | no_goal_60_80 | last_10m` — N=37, strike=73.0%, diff=+14.0 pp, p=0.087.

Veredito:

```text
APROVADO COM RESSALVAS PARA AUDITORIA OPERACIONAL
```

---

## Alertas atuais

### Duplicidades

A auditoria detectou duplicidades especialmente em `both_teams_cold_2of3`.

Essa familia deve ser tratada com cautela ate auditoria completa da origem das duplicidades.

### Playbooks V3

Os playbooks V3 devem ser preservados como documentacao operacional, mas nao devem ser usados como fonte principal para lucro final enquanto houver risco de agregacao/filtro alterando N e profit.

---

## Proxima Frente Oficial

```text
MULTI_LEAGUE_DRAWDOWN_AUDIT_V1
```

Objetivo:

Aplicar o script de drawdown nas estrategias originais para La Liga e futuras ligas/temporadas, mantendo:

- estrategias separadas;
- temporadas separadas;
- targets separados;
- sem filtros V3 por padrao;
- foco em lucro final + drawdown + ROI + EV.

---

## Restricoes

- Nao criar robo.
- Nao executar trade real.
- Nao criar producao.
- Nao chamar simulacao com odds medias de backtesting financeiro real.
- Nao usar odds live inexistentes.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
