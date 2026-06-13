# SPORTMONKS_TRENDS_SEMANTIC_VALIDATION_V1

## Status

```text
APTO COM RESSALVAS
```

SportMonks `trends` pode ser usado para H8 Team-Side V1 com cutoffs 60/65/70/75, desde que sejam aplicadas regras estritas de janela, periodo, tipo de indicador e anti-leakage.

Nao autoriza:

- modelo;
- baseline;
- robo;
- producao;
- trade real;
- backtesting financeiro real;
- importer;
- alteracao de schema;
- feature builder definitivo;
- multi-liga.

---

## Sumario Executivo

Foram revisados os arquivos SportMonks da EPL 2025/26 ja coletados.

Base observada:

```text
380 arquivos trends
380 arquivos timeline
```

Conclusao principal:

```text
SportMonks trends e util para pressao por time via participant_id.
```

Mas existem tres classes diferentes de dados:

1. Indicadores acumulados por time.
2. Indicadores snapshot/percentuais por minuto.
3. Indicadores finais/agregados fora do trends que nao podem ser usados como feature temporal.

Decisao:

```text
APTO COM RESSALVAS PARA H8 TEAM-SIDE V1
```

Pode avancar para:

```text
SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V1
```

---

## Pergunta Principal

### SportMonks trends pode ser usado com seguranca para cutoffs 60/65/70/75 e pressao por time?

Resposta:

```text
Sim, com ressalvas.
```

Seguro quando:

- usar somente registros com `minute <= cutoff`;
- calcular janelas por diferenca entre valores acumulados;
- separar `participant_id` por time;
- respeitar `period_id` e/ou minuto absoluto;
- tratar percentuais como snapshot, nao como acumulado;
- nao usar `statistics` final nem `xgfixture` como temporal.

---

# Estrutura Observada em trends

Cada registro relevante de trends possui:

```text
fixture_id
participant_id
type_id
period_id
value
minute
type.name
type.code
type.developer_name
type.stat_group
```

Leitura:

- `participant_id` identifica o time.
- `type_id` identifica o indicador.
- `minute` permite filtro por cutoff.
- `period_id` identifica o periodo do jogo.
- `value` pode ser acumulado ou snapshot, dependendo do tipo.

---

# Validacao por Tipo Prioritario

## 1. Attacks

```text
type_id: 43
developer_name: ATTACKS
```

Classificacao:

```text
ACUMULADO COM RESSALVAS
```

Uso permitido:

- cutoff 60/65/70/75;
- last_5m;
- last_10m;
- last_15m;
- pressao por time;
- diferenca entre valor no cutoff e valor no inicio da janela.

Regra:

```text
attacks_last_10m = attacks_at_cutoff - attacks_at_cutoff_minus_10
```

Ressalva:

- usar ultimo valor conhecido `<= minuto alvo`;
- nao usar valor posterior ao cutoff;
- cuidar com segundo tempo/period_id.

Status:

```text
WHITELIST
```

---

## 2. Dangerous Attacks

```text
type_id: 44
developer_name: DANGEROUS_ATTACKS
```

Classificacao:

```text
ACUMULADO COM RESSALVAS
```

Uso permitido:

- cutoff;
- last_5m/10m/15m;
- pressao por time;
- aceleracao de pressao.

Regra:

```text
dangerous_attacks_last_10m = dangerous_attacks_at_cutoff - dangerous_attacks_at_cutoff_minus_10
```

Status:

```text
WHITELIST
```

---

## 3. Ball Possession %

```text
type_id: 45
developer_name: BALL_POSSESSION
```

Classificacao:

```text
SNAPSHOT / PERCENTUAL COM CAUTELA
```

Nao deve ser tratado como acumulado.

Uso permitido:

- snapshot no cutoff;
- media dos snapshots na janela;
- tendencia de posse na janela.

Uso proibido:

```text
ball_possession_at_cutoff - ball_possession_at_cutoff_minus_10
```

Motivo:

Percentual pode subir e cair minuto a minuto. Nao representa volume acumulado.

Status:

```text
CAUTELA
```

---

## 4. Shots Total

```text
type_id: 42
developer_name: SHOTS_TOTAL
```

Classificacao:

```text
ACUMULADO COM RESSALVAS
```

Uso permitido:

- cutoff;
- last_5m/10m/15m;
- validacao de ritmo ofensivo por time.

Regra:

```text
shots_total_last_10m = shots_total_at_cutoff - shots_total_at_cutoff_minus_10
```

Status:

```text
WHITELIST
```

---

## 5. Shots On Target

```text
type_id: 86
developer_name: SHOTS_ON_TARGET
```

Classificacao:

```text
ACUMULADO COM RESSALVAS
```

Uso permitido:

- cutoff;
- last_5m/10m/15m;
- validacao de perigo real por time.

Status:

```text
WHITELIST
```

Observacao:

Tambem pode ser validado via `timeline` com evento `Shot On Target`.

---

## 6. Corners

```text
type_id: 34
developer_name: CORNERS
```

Classificacao:

```text
ACUMULADO COM RESSALVAS
```

Uso permitido:

- cutoff;
- last_5m/10m/15m;
- pressao territorial.

Status:

```text
WHITELIST
```

Observacao:

Tambem pode ser validado via `timeline` com evento `Corner`.

---

## 7. Key Passes

```text
type_id: 117
developer_name: KEY_PASSES
```

Classificacao:

```text
ACUMULADO COM RESSALVAS
```

Uso permitido:

- cutoff;
- last_5m/10m/15m;
- sinal de criacao ofensiva.

Ressalva:

- deve ser tratado como indicador SportMonks interno;
- validar consistencia contra shots/timeline antes de virar regra forte.

Status:

```text
WHITELIST COM CAUTELA
```

---

## 8. Big Chances Created

```text
type_id: 580
developer_name: BIG_CHANCES_CREATED
```

Classificacao:

```text
ACUMULADO COM RESSALVAS
```

Uso permitido:

- cutoff;
- last_5m/10m/15m;
- filtro de perigo alto.

Ressalva:

- baixa frequencia;
- pode gerar amostras pequenas;
- nao deve ser usado sozinho como filtro principal na V1.

Status:

```text
WHITELIST COM CAUTELA
```

---

## 9. Big Chances Missed

```text
type_id: 581
developer_name: BIG_CHANCES_MISSED
```

Classificacao:

```text
ACUMULADO COM RESSALVAS
```

Uso permitido:

- cutoff;
- last_5m/10m/15m;
- apoio para pressao/perigo.

Status:

```text
WHITELIST COM CAUTELA
```

---

## 10. Successful Passes

```text
type_id: 81
developer_name: SUCCESSFUL_PASSES
```

Classificacao:

```text
ACUMULADO COM CAUTELA
```

Uso permitido:

- apenas como contexto de controle/territorio;
- media/diferenca por janela, se validado por periodo;
- nao usar como proxy direto de perigo.

Ressalva:

- pode refletir posse esteril;
- risco de falso positivo em time que troca passes sem atacar.

Status:

```text
CAUTELA
```

---

## 11. Long Passes

```text
type_id: 62
developer_name: LONG_PASSES
```

Classificacao:

```text
ACUMULADO COM CAUTELA
```

Uso permitido:

- apoio secundario;
- contexto de estilo direto;
- nao usar sozinho para pressao.

Status:

```text
CAUTELA
```

---

# Campos Inseguros ou Proibidos

## statistics agregadas finais

Status:

```text
BLACKLIST PARA FEATURE TEMPORAL
```

Motivo:

`statistics` representa agregado final ou nao garante historico minuto a minuto. Usar como feature em cutoff gera risco de vazamento.

---

## xgfixture

Status:

```text
BLACKLIST PARA FEATURE TEMPORAL
```

Motivo:

Nao usar `xgfixture` como feature temporal em cutoffs 60/65/70/75. Pode conter xG agregado final ou sem granularidade segura por minuto.

---

## Percentuais de sucesso

Exemplos:

- Successful Passes Percentage;
- Successful Long Passes Percentage;
- Successful Crosses Percentage;
- Successful Dribbles Percentage;
- Ball Possession %.

Status:

```text
CAUTELA / SNAPSHOT
```

Uso permitido:

- snapshot no cutoff;
- media de snapshots na janela.

Uso proibido:

- diferenca como se fosse contagem acumulada;
- usar como volume ofensivo principal.

---

# Validacao de period_id

`period_id` aparece nos registros de trends e timeline.

Decisao:

```text
period_id deve ser preservado.
```

Regras:

1. Para janelas totalmente dentro do segundo tempo, como 60-75, usar `minute` absoluto e ultimo valor conhecido `<= cutoff`.
2. Nunca misturar registros de periodo sem controle.
3. Se uma janela atravessar intervalo, tratar periodos separadamente.
4. Para os cutoffs 60/65/70/75, normalmente estamos no segundo tempo, mas ainda assim o `period_id` deve ser mantido para auditoria.
5. Em jogos com acrescimos, minuto pode passar de 90; nao usar minutos acima do cutoff para feature.

Status:

```text
APTO COM RESSALVAS
```

---

# Regras Anti-Leakage

Permitido:

```text
minute <= cutoff
```

Proibido:

```text
minute > cutoff
```

Para janela last_10m em cutoff 60:

```text
inicio = 50
fim = 60
usar apenas valores <= 60
```

Para acumulados:

```text
valor_janela = ultimo_valor_<=fim - ultimo_valor_<=inicio
```

Para snapshots/percentuais:

```text
valor_janela = media ou tendencia dos snapshots entre inicio e fim
```

Nao usar:

- resultado final;
- `result_info`;
- scores finais fora da reconstrucao minuto a minuto;
- statistics final;
- xgfixture final;
- registros posteriores ao cutoff;
- timeline depois do cutoff;
- eventos de gol depois do cutoff como feature.

---

# Regras de Cutoff

Cutoffs permitidos para V1:

```text
60
65
70
75
```

Para cada cutoff:

1. Filtrar trends com `minute <= cutoff`.
2. Filtrar timeline com `minute <= cutoff`.
3. Calcular indicadores por `participant_id`.
4. Separar home/away via identity/mapping de participants.
5. Gerar features apenas com informacao anterior ou igual ao cutoff.

---

# Regras de Janela

Janelas permitidas:

```text
last_5m
last_10m
last_15m
```

Para acumulados:

```text
last_5m = valor(cutoff) - valor(cutoff - 5)
last_10m = valor(cutoff) - valor(cutoff - 10)
last_15m = valor(cutoff) - valor(cutoff - 15)
```

Para snapshots:

```text
media_5m
media_10m
media_15m
slope/tendencia simples
ultimo_valor_<=cutoff
```

Nao usar diferenca simples em percentual como contagem.

---

# Validacao Timeline

Arquivos timeline observados:

```text
380 arquivos timeline
```

Eventos observados no timeline:

```text
Shot Off Target
Corner
Shot On Target
Offside
Woodwork
```

## Timeline confirma eventos por minuto?

```text
SIM
```

Cada evento possui minuto e tipo.

## Timeline possui participant_id/team?

```text
SIM
```

Cada evento possui `participant_id`, permitindo separar os eventos por time.

## Timeline pode ser usada para contagem last_10m?

```text
SIM
```

Exemplo:

```text
shots_on_target_timeline_last_10m = count(event_type == Shot On Target, minute > cutoff - 10, minute <= cutoff, participant_id == team)
```

## Timeline pode validar trends?

```text
SIM, PARCIALMENTE
```

Timeline pode validar:

- Shots On Target;
- Shot Off Target;
- Corner;
- Offside;
- Woodwork.

Timeline nao valida diretamente:

- Attacks;
- Dangerous Attacks;
- Ball Possession %;
- Key Passes;
- Successful Passes;
- Long Passes;
- Big Chances Created.

Observacao:

No dataset revisado, `Goal` nao apareceu como tipo de evento dentro dos arquivos timeline analisados. Portanto, gols devem ser reconstruidos por fonte especifica de eventos/scores/commentaries/incidents antes de virar target ou filtro temporal.

---

# Whitelist V1 de Indicadores Permitidos

## Acumulados principais

```text
Attacks
Dangerous Attacks
Shots Total
Shots On Target
Shots Off Target
Corners
Key Passes
Big Chances Created
Big Chances Missed
```

Uso:

- cutoff;
- last_5m;
- last_10m;
- last_15m;
- por participant_id;
- com diferenca de acumulado.

## Timeline permitida

```text
Shot On Target
Shot Off Target
Corner
Offside
Woodwork
```

Uso:

- contagem por janela;
- validacao cruzada de trends;
- auditoria de eventos objetivos.

---

# Caution List V1

```text
Ball Possession %
Successful Passes
Successful Passes Percentage
Long Passes
Successful Long Passes
Successful Long Passes Percentage
Successful Crosses Percentage
Successful Dribbles Percentage
```

Uso permitido apenas como apoio/contexto, nao como gatilho principal na V1.

---

# Blacklist V1

```text
statistics agregadas finais
xgfixture
result_info
placar final
qualquer campo de resultado final
qualquer registro com minute > cutoff
qualquer tipo sem participant_id quando a estrategia exigir lado/time
percentuais tratados como acumulado
```

---

# Recomendacao para Proxima Execucao

Decisao:

```text
APTO COM RESSALVAS
```

Recomendar execucao controlada de:

```text
SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V1
```

Escopo recomendado:

1. EPL 2025/26 apenas.
2. Usar somente SportMonks ja coletado.
3. Cutoffs 60/65/70/75.
4. Janelas 5/10/15 minutos.
5. Separar features por time via `participant_id`.
6. Separar familias:
   - Under / Lay Over hold;
   - Over de janela curta.
7. Usar timeline apenas para validacao/contagem objetiva de eventos.
8. Nao criar modelo ou baseline.
9. Nao fazer backtest financeiro real.

---

# Proximo Agente Recomendado

```text
Quant Research / Data Science
```

Com apoio pontual de:

```text
Codex Developer
```

Somente para execucao tecnica controlada, sem alterar schema, importer ou criar feature builder definitivo.

---

# Decisao Final

```text
SPORTMONKS TRENDS = APTO COM RESSALVAS PARA H8 TEAM-SIDE V1
```

Pode avancar para discovery estatistico controlado, mantendo todas as restricoes de anti-leakage e sem operacionalizacao real.
