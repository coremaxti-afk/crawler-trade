# CURRENT SPRINT

## Sprint Atual

Status:

```text
ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1_EM_PLANEJAMENTO_ESTRUTURADO
```

Fase atual:

```text
NOVA_FRENTE_MACRO_DE_PESQUISA
DISCOVERY_DE_FLUXO_DO_PRIMEIRO_TEMPO
```

Frente oficial ativa:

```text
ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1
```

Documento de planejamento:

```text
docs/04_RESEARCH/ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1.md
```

Status operacional:

```text
NENHUMA OPERACAO REAL APROVADA
NENHUM ROBO OPERACIONAL APROVADO
ALERTAS CORNER PRO SOMENTE COMO FASE FUTURA PAPER/OBSERVACAO
```

---

## Decisao registrada

O usuario decidiu seguir a recomendacao de abrir a frente:

```text
ANALISE_TRAJETORIAS_PRIMEIRO_TEMPO_V1
```

Objetivo:

```text
Analisar todo o primeiro tempo como fluxo de jogo, buscando padroes estatisticos que possam futuramente virar regras objetivas de notificacao na plataforma Corner Pro.
```

A frente nao deve repetir mecanicamente o estudo de Gols Tardios trocando cutoffs tardios por minutos do primeiro tempo. A proposta e aprimorar a pesquisa estudando:

```text
trajetoria completa do 1T
ritmo por fase
aceleracao e desaceleracao
volume vs qualidade
pressao real vs pressao falsa
pressao unilateral vs bilateral
tipos de 0x0
risco condicional de gol ate HT
```

---

## Contexto

O projeto de Gols Tardios V1 permanece encerrado como pesquisa retrospectiva/prospectiva simulada, com ressalvas estatisticas e sem autorizacao operacional.

A frente Forca + Estado + Temperatura/Favorito deve permanecer encerrada/arquivada sem priorizacao operacional imediata.

A nova frente ativa e independente e deve iniciar como discovery metodologico, sem cashout, sem playbook operacional e sem robo de entrada real.

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

Se uma solicitacao pular etapas, misturar objetivos, fragilizar a metodologia, inflar lucro/ROI/robustez ou gerar falsa confianca operacional, o agente deve discordar primeiro e propor o caminho correto.

---

## Cronograma oficial da frente em 5 etapas

### Etapa 1 — Reconstrucao do filme do primeiro tempo

Objetivo:

```text
Construir uma base fixture-level e phase-level que descreva o comportamento ofensivo do primeiro tempo completo.
```

Fases naturais:

```text
0-10
11-20
21-30
31-45+
```

Status:

```text
PROXIMA ACAO
```

---

### Etapa 2 — Criacao de features de trajetoria

Objetivo:

```text
Transformar estatisticas brutas em features de fluxo, qualidade, mudanca de ritmo, pressao real/falsa e assimetria ofensiva.
```

Features esperadas:

```text
volume_total_1t
qualidade_total_1t
intensidade_por_fase
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

Status:

```text
AGUARDANDO ETAPA 1
```

---

### Etapa 3 — Classificacao de trajetorias e tipos de 0x0

Objetivo:

```text
Classificar perfis de fluxo do primeiro tempo antes de transformar qualquer perfil em estrategia.
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

Status:

```text
AGUARDANDO ETAPA 2
```

---

### Etapa 4 — Conversao de perfis em estrategias candidatas

Objetivo:

```text
Converter apenas perfis com evidencia estatistica minima em regras objetivas testaveis.
```

Exemplos futuros:

```text
HT_GOAL_AQUECIMENTO_PROGRESSIVO_COM_QUALIDADE_V1
HT_GOAL_PRESSAO_BILATERAL_CRESCENTE_V1
HT_GOAL_PRESSAO_UNILATERAL_COM_SOT_RECENTE_V1
HT_NO_GOAL_FRIO_CONSTANTE_V1
HT_NO_GOAL_PRESSAO_FALSA_V1
HT_NO_GOAL_SEM_QUALIDADE_OFENSIVA_V1
```

Status:

```text
AGUARDANDO ETAPA 3
```

---

### Etapa 5 — Validacao estatistica e preparacao para alertas Corner Pro

Objetivo:

```text
Identificar quais estrategias candidatas possuem evidencia suficiente para virar alertas de observacao/paper na plataforma Corner Pro.
```

Metricas obrigatorias:

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

Status:

```text
AGUARDANDO ETAPA 4
```

---

## Fase posterior — Corner Pro

A configuracao do robo Corner Pro so deve ocorrer depois da Etapa 5 e apenas como:

```text
ALERTA_PAPER
OBSERVACAO_PROSPECTIVA
NAO_OPERACIONAL
```

Proibido:

```text
ENTRADA_AUTOMATICA
OPERACAO_REAL_APROVADA
SINAL_COMERCIAL
CARTEIRA_APROVADA
```

Formato futuro desejado para regra de alerta:

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

---

## Deduplicacao obrigatoria

Todo script deve separar:

```text
N_trades_bruto
fixtures_unicos
N_pos_deduplicacao_por_fase
N_pos_deduplicacao_por_fixture
exposicoes_por_fixture
```

A leitura final da sprint deve priorizar:

```text
resultado deduplicado por fixture
```

---

## Politica de odds e resultados financeiros

Todos os resultados com odds, N, lucro, ROI, EV, drawdown, hit rate ou taxa devem ser classificados como:

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

---

## Restricoes

- Nao criar robo antes de encontrar padrao estatistico.
- Nao configurar alerta Corner Pro como entrada real.
- Nao criar producao operacional.
- Nao usar cashout nesta V1.
- Nao escolher thresholds por intuicao sem validar historico.
- Nao transformar discovery em validacao.
- Nao somar lucros de estrategias parecidas sem deduplicacao e auditoria.
- Nao transformar baixa amostra em robustez.
- Nao comercializar sinais derivados do pipeline.
- Nao transformar melhor fase/minuto retrospectivo em regra final.
