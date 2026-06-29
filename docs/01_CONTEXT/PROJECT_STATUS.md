# PROJECT STATUS

## Estado Atual do Projeto

FASE ATUAL:

```text
PESQUISA_GOLS_TARDIOS_V1_ENCERRADA_COM_RESSALVAS_ESTATISTICAS
FRENTE_COMPLEMENTAR_FORCA_ESTADO_TEMPERATURA_ENCERRADA_SEM_PRIORIZACAO_OPERACIONAL
FRENTE_ATIVA: ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1
ETAPA_5_TARGETS_RESTANTES_CONCLUIDA_COM_RESSALVAS
PROXIMA_ETAPA: PREPARACAO_REGRAS_ALERTA_PAPER_CORNER_PRO_V1
```

Status oficial:

```text
NENHUMA OPERACAO REAL APROVADA
NENHUM ROBO OPERACIONAL APROVADO
SEM_CASHOUT
FRENTE_ATUAL_SEM_ODDS_E_SEM_FAVORITO
```

Documentos da frente ativa:

```text
docs/04_RESEARCH/ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1.md
docs/04_RESEARCH/primeiro_tempo/STATUS_ANDAMENTO_ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1.md
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

## Gols Tardios V1

Status:

```text
PESQUISA V1 CONCLUIDA COM RESSALVAS ESTATISTICAS
SEM AUTORIZACAO PARA OPERACAO REAL
```

O pipeline de Gols Tardios V1 permanece encerrado como pesquisa retrospectiva/prospectiva simulada, com ressalvas estatisticas e sem autorizacao operacional.

Familias No Goal relevantes historicas:

```text
both_teams_cold_2of3__no_goal
team_winning_by_1_low_dangerous_attacks_against__no_goal
team_winning_by_1_opp_cold_2of3__no_goal
favorite_winning_by_1_opp_cold_2of3__no_goal
team_winning_by_1_no_sot_against__no_goal
opponent_no_recent_key_passes__no_goal
opponent_no_big_chances__no_goal
```

Nenhuma familia esta aprovada para operacao real.

---

## Frente complementar encerrada — Forca, Estado e Temperatura/Favorito

Status:

```text
FRENTE_COMPLEMENTAR_ENCERRADA_SEM_PRIORIZACAO_OPERACIONAL
NAO_SEGUIR_PARA_ETAPA_3
NAO_GERAR_FAMILIAS
NAO_VALIDAR_OPERACAO
NAO_USAR_CASHOUT
```

Conclusao:

```text
A frente Forca + Estado + Temperatura nao gerou evidencia suficiente para virar eixo principal de pesquisa. Os achados mais uteis foram diagnosticos, especialmente a pista de JOGO_FRIO + NO_GOAL, mas sem forca bastante para justificar continuidade imediata.
```

---

## Frente ativa — ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1

Status:

```text
FRENTE_ATIVA_DE_PESQUISA
DISCOVERY_DE_FLUXO_DO_PRIMEIRO_TEMPO
HOLD_ONLY
SEM_OPERACAO_REAL_APROVADA
SEM_CASHOUT
SEM_ROBO_OPERACIONAL_NESTA_ETAPA
```

Objetivo:

```text
Analisar todo o primeiro tempo como fluxo de jogo para encontrar padroes estatisticos que possam futuramente ser convertidos em regras objetivas de alerta paper na plataforma Corner Pro.
```

Andamento resumido:

```text
Etapa 1 — Reconstrucao do 1T: APROVADA
Etapa 2 — Features de trajetoria: APROVADA_COM_RESSALVA_LEVE
Etapa 3 — Classificacao inicial: INCONCLUSIVA_POR_CLASSIFICACAO_FRACA
Etapa 3.1 — Recalibracao: INCONCLUSIVA_POR_FRAGMENTACAO_EXCESSIVA
Etapa 3.2 — Consolidacao: APROVADA_COM_RESSALVAS
Etapa 4 — Estrategias candidatas: APROVADA_COM_RESSALVAS
Etapa 5 — Targets restantes: APROVADA_COM_RESSALVAS
```

Candidatas sobreviventes ao target restante para proxima etapa paper:

```text
HT_NO_GOAL_BAIXA_QUALIDADE_REAL_V1 observada_ate_30
HT_NO_GOAL_BAIXA_QUALIDADE_REAL_V1 observada_ate_35
HT_NO_GOAL_AQUECIMENTO_FRACO_V1 observada_ate_30
HT_NO_GOAL_AQUECIMENTO_FRACO_V1 observada_ate_35
HT_GOAL_QUALIDADE_PONTUAL_PRECOCE_V1 observada_ate_20
HT_GOAL_AQUECIMENTO_MODERADO_COM_QUALIDADE_V1 observada_ate_30
```

Proxima etapa sugerida:

```text
ETAPA_6_PREPARACAO_REGRAS_ALERTA_PAPER_CORNER_PRO_V1
```

Objetivo da proxima etapa:

```text
Transformar candidatas sobreviventes ao target restante em especificacoes objetivas de alerta paper, sem configuracao real e sem aprovacao operacional.
```

---

## Decisao atual sobre odds e favorito

O usuario decidiu seguir o roadmap atual sem odds e sem filtros de favorito/pre-live nesta fase.

Porem, fica registrada a ressalva metodologica:

```text
Sem odds, nao existe aprovacao financeira de estrategia de trade esportivo.
```

As candidatas atuais devem ser tratadas como:

```text
CANDIDATA_ESTATISTICA_SEM_ODDS
NAO_VALIDADA_FINANCEIRAMENTE
NAO_OPERACIONAL
```

Fica tambem registrada a possibilidade de estudos segmentados futuros partindo da base ja construida, incluindo:

```text
favorito forte
favorito medio
odd pre-live 1x2 ate 1.60
mandante/visitante favorito
0x0 aos 30
favorito vencendo/empatando/perdendo
```

Status desses estudos:

```text
PENDENCIA_FUTURA
ESTUDO_SEGMENTADO_POSTERIOR
NAO_INCLUIR_NA_FRENTE_ATUAL
```

---

## Politica Oficial de Odds

Todos os resultados financeiros futuros seguem como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```

Ressalvas obrigatorias:

```text
Nao constitui backtesting financeiro real.
Nao usa odds live reais por timestamp, salvo se dados timestampados forem comprovados.
Nao considera liquidez, spread, delay, slippage, suspensao de mercado ou comissao real, salvo se modelado explicitamente.
Nao constitui recomendacao de trading.
Nao autoriza operacao real.
```

---

## Decisao Operacional Atual

Nenhuma estrategia, time, perfil, fase, rodada, filtro, alerta, carteira ou familia esta aprovado para operacao real.

A futura configuracao de alertas no Corner Pro deve ser tratada somente como:

```text
ALERTA_PAPER
OBSERVACAO_PROSPECTIVA
NAO_OPERACIONAL
```

---

## Restricoes permanentes

- Nao criar robo operacional a partir desta pesquisa.
- Nao configurar alerta Corner Pro como entrada real antes de validacao prospectiva.
- Nao criar producao operacional.
- Nao chamar simulacao com odds medias de backtesting financeiro real.
- Nao usar odds live inexistentes ou nao timestampadas como se fossem reais.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao transformar baixa amostra em robustez.
- Nao comercializar sinais derivados do pipeline.
- Nao generalizar para outras ligas ou mercados sem reexecutar a esteira local.
- Nao usar time especifico como filtro antes de validar blocos macro.
- Nao transformar melhor fase/minuto retrospectivo em regra final.
- Nao usar cashout nesta V1.
