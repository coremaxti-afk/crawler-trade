# ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1

## Status

```text
FRENTE_ATIVA_DE_PESQUISA
DISCOVERY_DE_FLUXO_DO_PRIMEIRO_TEMPO
HOLD_ONLY
SEM_OPERACAO_REAL_APROVADA
SEM_CASHOUT
SEM_ROBO_OPERACIONAL_NESTA_ETAPA
```

## Decisao registrada

O usuario decidiu seguir a recomendacao de abrir a frente:

```text
ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1
```

A frente substitui, como proxima prioridade de pesquisa, a continuidade da frente complementar de Forca + Estado + Temperatura, que deve permanecer arquivada/encerrada sem priorizacao operacional.

## Objetivo central

Analisar todo o primeiro tempo como fluxo de jogo, e nao apenas como snapshots por cutoff.

Pergunta principal:

```text
Quais padroes de trajetoria do primeiro tempo distinguem jogos que terminam 0x0 no intervalo de jogos que produzem gol antes do intervalo?
```

Pergunta operacional futura:

```text
Quais padroes estatisticamente consistentes podem virar regras objetivas de notificacao em robo externo, inicialmente em paper/observacao, para posterior avaliacao prospectiva?
```

## Principio metodologico

Esta frente nao deve repetir mecanicamente o estudo de Gols Tardios trocando cutoffs de 60/65/70/75 por 20/25/30.

A evolucao esperada e estudar:

```text
trajetoria completa do 1T
ritmo ofensivo por fase
aceleracao/desaceleracao
volume vs qualidade
tipo de 0x0
pressao real vs pressao falsa
pressao unilateral vs bilateral
risco condicional de gol ate o intervalo
```

## Escopo inicial

Mercados/eventos analisados:

```text
HT_GOAL
HT_NO_GOAL
GOAL_0_15
GOAL_16_30
GOAL_31_45_PLUS
OVER_1_5_HT
```

Modo inicial:

```text
DISCOVERY
HOLD_ONLY
SEM_CASHOUT
SEM_OPERACAO
SEM_PLAYBOOK_OPERACIONAL
SEM_ALERTA_REAL COMO APROVACAO DE ENTRADA
```

## Dados live/in-live considerados

Indicadores base reaproveitaveis da arquitetura SportMonks/team-side:

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

Esses indicadores devem ser analisados por jogo, por lado e por fase do primeiro tempo.

## Fases naturais do primeiro tempo

A analise deve reconstruir o primeiro tempo como filme, usando blocos naturais:

```text
fase_1: 0-10
fase_2: 11-20
fase_3: 21-30
fase_4: 31-45+
```

A leitura principal nao e escolher um unico minuto de entrada. A leitura principal e entender a sequencia:

```text
fase_1 -> fase_2 -> fase_3 -> fase_4
```

Exemplos de trajetorias:

```text
FRIO -> FRIO -> FRIO -> FRIO
FRIO -> MORNO -> QUENTE -> QUENTE
QUENTE -> QUENTE -> FRIO -> FRIO
FRIO -> FRIO -> QUENTE -> CAOTICO
MORNO -> MORNO -> MORNO -> MORNO
```

## Roadmap oficial em 5 etapas

### Etapa 1 — Reconstrucao do filme do primeiro tempo

Objetivo:

```text
Construir uma base fixture-level e phase-level que descreva o comportamento ofensivo do primeiro tempo completo.
```

Saidas esperadas:

```text
base_primeiro_tempo_fases_v1.csv
summary_baseline_primeiro_tempo_v1.csv
relatorio_reconstrucao_primeiro_tempo_v1.md
```

Campos minimos:

```text
fixture_id
season_id
league_name
fixture_name
home_team
away_team
score_ht
goals_0_15
goals_16_30
goals_31_45_plus
ht_goal
ht_no_goal
over_1_5_ht
fase
team_side
attacks
dangerous_attacks
shots_total
shots_on_target
shots_off_target
corners
key_passes
big_chances_created
big_chances_missed
```

Regras:

```text
1. Separar mandante e visitante.
2. Preservar fixture_id para deduplicacao.
3. Nao criar estrategia nesta etapa.
4. Nao calcular ROI nesta etapa.
5. Medir baseline por liga/temporada antes de qualquer ranking.
```

---

### Etapa 2 — Criacao de features de trajetoria

Objetivo:

```text
Transformar estatisticas brutas do primeiro tempo em features de fluxo, qualidade e mudanca de ritmo.
```

Features candidatas:

```text
volume_total_1t
qualidade_total_1t
intensidade_fase_1
intensidade_fase_2
intensidade_fase_3
intensidade_fase_4
slope_intensidade_1t
aceleracao_intensidade_1t
pico_pressao_1t
queda_pos_pico_1t
pressao_recente_vs_pressao_media
assimetria_ofensiva
conversao_pressao_em_finalizacao
conversao_finalizacao_em_sot
big_chance_rate
key_pass_rate
corner_pressure_rate
```

Separar obrigatoriamente:

```text
volume_ofensivo
qualidade_ofensiva
conversao_de_pressao
pressao_unilateral
pressao_bilateral
pressao_falsa
pressao_real
```

Exemplos de leitura:

```text
muito dangerous attack sem SOT = pressao possivelmente falsa
baixo volume com SOT/big chance = baixa frequencia, alta qualidade
pressao crescente por fase = aquecimento progressivo
pico isolado seguido de queda = jogo que perdeu intensidade
```

---

### Etapa 3 — Classificacao de trajetorias e tipos de 0x0

Objetivo:

```text
Classificar o tipo de primeiro tempo e o tipo de 0x0 observado, sem ainda transformar isso em estrategia operacional.
```

Perfis candidatos:

```text
FRIO_CONSTANTE
AQUECIMENTO_PROGRESSIVO
QUENTE_CONSTANTE
PICO_ISOLADO
DESACELERACAO
PRESSAO_UNILATERAL_CRESCENTE
PRESSAO_BILATERAL_CRESCENTE
CAOS_SEM_QUALIDADE
BAIXO_VOLUME_ALTA_QUALIDADE
ALTO_VOLUME_BAIXA_QUALIDADE
```

Tipos de 0x0:

```text
0X0_MORTO
0X0_FALSO_FRIO
0X0_PRESSAO_UNILATERAL
0X0_PRESSAO_BILATERAL
0X0_CAOTICO_SEM_PRECISAO
0X0_COM_CHANCES_REAIS
0X0_COM_PICO_RECENTE
0X0_ESFRIANDO
```

Saidas esperadas:

```text
base_trajetorias_primeiro_tempo_v1.csv
ranking_perfis_primeiro_tempo_v1.csv
relatorio_classificacao_trajetorias_primeiro_tempo_v1.md
```

Leituras obrigatorias:

```text
N fixtures por perfil
HT_GOAL% por perfil
HT_NO_GOAL% por perfil
lift vs baseline da liga
diferenca absoluta vs baseline
estabilidade por liga
estabilidade por temporada
concentracao por time/liga, apenas como alerta de risco
```

---

### Etapa 4 — Conversao de perfis em estrategias candidatas

Objetivo:

```text
Converter apenas perfis com evidencia estatistica minima em regras objetivas testaveis.
```

Exemplos de estrategias candidatas:

```text
HT_GOAL_AQUECIMENTO_PROGRESSIVO_COM_QUALIDADE_V1
HT_GOAL_PRESSAO_BILATERAL_CRESCENTE_V1
HT_GOAL_PRESSAO_UNILATERAL_COM_SOT_RECENTE_V1
HT_NO_GOAL_FRIO_CONSTANTE_V1
HT_NO_GOAL_PRESSAO_FALSA_V1
HT_NO_GOAL_SEM_QUALIDADE_OFENSIVA_V1
```

Cada estrategia deve conter:

```text
strategy_id
strategy_name
direcao: HT_GOAL ou HT_NO_GOAL
condicoes objetivas
fase(s) usadas
estatisticas live usadas
N bruto
N dedup fixture
baseline comparavel
target
modo HOLD
status cientifico
```

Exemplo de regra futura, ainda nao aprovada:

```text
strategy_id: HT_GOAL_AQUECIMENTO_PROGRESSIVO_COM_QUALIDADE_V1
placar: 0x0
fase observada: 21-30 ou 31-45+
condicoes:
  - intensidade atual > intensidade fase anterior
  - shots_on_target recente >= limite validado
  - dangerous_attacks recente >= limite validado por liga
  - corners/key_passes/big_chances como filtros auxiliares
  - perfil classificado como AQUECIMENTO_PROGRESSIVO_COM_QUALIDADE
target: gol ate HT
modo: HOLD
status: CANDIDATA_DE_DISCOVERY
```

Importante:

```text
Nao escolher thresholds manualmente para agradar exemplo operacional.
Thresholds devem sair da distribuicao historica, percentis, lift vs baseline e estabilidade por liga/temporada.
```

---

### Etapa 5 — Validacao estatistica e preparacao para robo de notificacao Corner Pro

Objetivo:

```text
Identificar quais estrategias candidatas possuem evidencia suficiente para virar alertas de observacao/paper em robo externo, inicialmente Corner Pro.
```

Metricas obrigatorias para qualquer estrategia:

```text
N bruto
fixtures_unicos
N dedup fixture
exposicoes_por_fixture
hit rate
baseline da liga/temporada
lift vs baseline
odds media, se disponivel
break-even
EV estimado
lucro estimado
ROI estimado
drawdown
max losing streak
estabilidade por liga
estabilidade por temporada
overlap com estrategias parecidas
```

Rotulo obrigatorio para resultados com odds, ROI, EV, lucro, drawdown ou taxa:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```

Proibido chamar de:

```text
BACKTESTING FINANCEIRO REAL
ODDS LIVE REAIS
SISTEMA LUCRATIVO VALIDADO
OPERACAO APROVADA
```

Criterios minimos sugeridos para virar alerta paper:

```text
N dedup fixture minimamente relevante
lift positivo e interpretavel vs baseline
resultado nao concentrado em uma unica liga/time
drawdown aceitavel para observacao
thresholds reproduziveis
baixa sobreposicao com regra equivalente
funcionar em mais de uma temporada ou justificar status inconclusivo
```

## Fase posterior — Robo de notificacao Corner Pro

O robo Corner Pro entra somente depois da Etapa 5, como ferramenta de notificacao/paper.

Status permitido:

```text
ALERTA_PAPER
OBSERVACAO_PROSPECTIVA
NAO_OPERACIONAL
```

Status proibido:

```text
ENTRADA_AUTOMATICA
OPERACAO_REAL_APROVADA
SINAL_COMERCIAL
CARTEIRA_APROVADA
```

Formato desejado de regra para configurar na plataforma:

```text
Nome do alerta
Mercado observado
Minuto/fase de observacao
Placar exigido
Condicoes live obrigatorias
Condicoes live auxiliares
Direcao sugerida para estudo: HT_GOAL ou HT_NO_GOAL
Target de avaliacao
Mensagem de alerta
Status: PAPER/OBSERVACAO
```

Exemplo de alerta paper futuro:

```text
ALERTA PAPER — HT_GOAL_AQUECIMENTO_PROGRESSIVO_COM_QUALIDADE_V1

Jogo: {home} vs {away}
Minuto: {minute}
Placar: 0x0
Perfil: AQUECIMENTO_PROGRESSIVO_COM_QUALIDADE
Motivos:
- intensidade ofensiva crescente
- SOT recente acima do limite validado
- dangerous attacks recente acima do limite validado
- escanteios/key passes/big chances conforme regra validada

Status: PAPER / OBSERVACAO
Acao: registrar e acompanhar ate HT, sem automatizar entrada real.
```

## Arquitetura futura de scripts

Sugestao inicial:

```text
scripts/research/primeiro_tempo/01_reconstruir_primeiro_tempo_fases_v1.py
scripts/research/primeiro_tempo/02_criar_features_trajetoria_primeiro_tempo_v1.py
scripts/research/primeiro_tempo/03_classificar_trajetorias_primeiro_tempo_v1.py
scripts/research/primeiro_tempo/04_gerar_estrategias_candidatas_primeiro_tempo_v1.py
scripts/research/primeiro_tempo/05_validar_estrategias_e_alertas_corner_pro_v1.py
```

Artefatos esperados:

```text
data/processed/primeiro_tempo/
docs/04_RESEARCH/primeiro_tempo/
reports/primeiro_tempo/
```

## Regras permanentes da frente

```text
1. Nao criar robo antes de encontrar padrao estatistico.
2. Nao transformar alerta em aprovacao operacional.
3. Nao definir thresholds por intuicao sem validar distribuicao historica.
4. Nao somar lucros de estrategias parecidas como independentes.
5. Nao usar cashout nesta V1.
6. Nao chamar odds medias de backtesting financeiro real.
7. Deduplicacao por fixture e obrigatoria.
8. Discovery nao e validacao.
9. Paper/prospectivo vem antes de qualquer discussao operacional.
10. Se a frente nao encontrar padrao robusto, encerrar sem forcar conclusao positiva.
```

## Decisao operacional atual

```text
Nenhuma estrategia de primeiro tempo esta aprovada.
Nenhum alerta Corner Pro esta aprovado.
Nenhuma entrada real esta aprovada.
A frente esta autorizada apenas como pesquisa quantitativa e preparacao metodologica para alertas paper futuros.
```
