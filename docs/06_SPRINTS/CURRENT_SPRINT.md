# CURRENT SPRINT

## Sprint Atual

Status:

```text
ESTUDO_FORCA_ESTADO_TEMPERATURA_JOGO_V1_EM_PLANEJAMENTO_ESTRUTURADO
```

Fase atual:

```text
FRENTE_COMPLEMENTAR_DE_GOLS_TARDIOS
VALIDACAO_MATRIZ_FORCA_ESTADO_TEMPERATURA_JOGO_V1
```

Frente oficial ativa:

```text
ESTUDO_FORCA_ESTADO_TEMPERATURA_JOGO_V1
```

Documento de planejamento:

```text
docs/04_RESEARCH/PLANO_ESTUDO_FORCA_ESTADO_TEMPERATURA_JOGO_V1.md
```

Status operacional:

```text
NENHUMA OPERACAO REAL APROVADA
```

---

## Contexto

O projeto de gols tardios V1 permanece encerrado como pesquisa retrospectiva e prospectiva simulada, com ressalvas estatisticas.

A frente atual nao reabre operacao real. Ela organiza uma validacao complementar da tese:

```text
forca do favorito
+ estado do favorito/time no placar
+ temperatura do jogo
+ direcao Goal / No Goal
+ cutoff
```

A tese nasceu da validacao de segmentacao por forca do favorito, na qual ligas originalmente mais Under no agregado passaram a mostrar alguns blocos Over/Goal quando segmentadas por favorito forte ou medio.

---

## Tese ativa

Hipotese macro:

```text
FAVORITO_FORTE/MEDIO + JOGO_QUENTE + ESTADO DO FAVORITO -> Goal
FAVORITO_FRACO/SEM_FAVORITO_CLARO + JOGO_FRIO + ESTADO DO LADO/TIME -> No Goal
```

Estados obrigatorios:

```text
FAVORITO_GANHANDO
FAVORITO_EMPATANDO
FAVORITO_PERDENDO
```

Para jogos sem favorito claro:

```text
LADO_ANALISADO_GANHANDO
EMPATE
LADO_ANALISADO_PERDENDO
```

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

## Cronograma oficial da frente

### Etapa 1 — Classificador base

```text
classificar_contexto_forca_estado_temperatura_v1.py
```

Objetivo:

```text
criar base unica classificada com forca do favorito, estado do placar, temperatura, mandante/visitante, direcao e cutoff.
```

Status:

```text
PROXIMA ACAO
```

---

### Etapa 2 — Validacao da matriz macro

```text
validacao_matriz_forca_estado_temperatura_v1.py
```

Objetivo:

```text
testar forca x estado x temperatura x direcao x cutoff sem quebrar por familia como decisao principal.
```

Status:

```text
AGUARDANDO ETAPA 1
```

---

### Etapa 3 — Familias explicativas

```text
analise_familias_blocos_matriz_v1.py
```

Objetivo:

```text
abrir por familia apenas os blocos macro sobreviventes.
```

Status:

```text
AGUARDANDO ETAPA 2
```

---

### Etapa 4 — Mandante/visitante auxiliar

```text
analise_mandante_visitante_blocos_v1.py
```

Objetivo:

```text
avaliar favorito mandante/visitante ou lado analisado mandante/visitante apenas como diagnostico auxiliar.
```

Status:

```text
AGUARDANDO ETAPA 3
```

---

### Etapa 5 — Agregador da temporada

```text
agregar_estudo_forca_estado_temperatura_temporada_v1.py
```

Objetivo:

```text
gerar 5 relatorios por temporada: favorito forte, favorito medio, favorito fraco, sem favorito claro e agregado da temporada.
```

Status:

```text
AGUARDANDO ETAPAS 1 A 4
```

---

### Etapa 6 — Times especificos

```text
analise_times_blocos_promissores_v1.py
```

Objetivo:

```text
avaliar concentracao por time apenas nos blocos macro/familia ja promissores.
```

Status:

```text
POSTERIOR
NAO EXECUTAR NA PRIMEIRA RODADA
```

---

### Etapa 7 — Pipeline do estudo

```text
executar_pipeline_estudo_forca_estado_temperatura_v1.py
```

Objetivo:

```text
rodar a esteira completa por season_id somente depois das etapas 1 a 5 existirem e validarem.
```

Status:

```text
FUTURO
NAO CRIAR AGORA
```

---

## Regras metodologicas da sprint

A frente deve ser hierarquica:

```text
1. primeiro provar o fenomeno macro.
2. depois explicar por familia.
3. depois investigar mandante/visitante.
4. depois investigar time especifico apenas nos blocos sobreviventes.
```

Evitar matriz total como decisao principal:

```text
forca x estado x temperatura x direcao x cutoff x familia x casa/fora x time
```

Motivo:

```text
risco de milhares de combinacoes, N baixo e falso positivo.
```

---

## Deduplicacao obrigatoria

Todo script deve separar:

```text
N_trades_bruto
fixtures_unicos
N_pos_deduplicacao_por_cutoff
N_pos_deduplicacao_por_fixture
exposicoes_por_fixture
```

A leitura final da sprint deve priorizar:

```text
resultado deduplicado por fixture
```

---

## Cutoff

A analise deve conter:

```text
cutoff individual
agregado de cutoffs
melhor cutoff apenas como hipotese futura
```

Proibido:

```text
escolher o melhor cutoff retrospectivo e declarar aprovacao.
```

---

## Hold e cashout

Regra da V1:

```text
HOLD COMO BASE PRINCIPAL
CASHOUT FORA DO ESCOPO DA V1
```

Cashout deve ser estudo futuro separado apenas se a tese macro sobreviver.

---

## Relatorios esperados por temporada

Quando o agregador existir, gerar:

```text
relatorio_favorito_forte.md
relatorio_favorito_medio.md
relatorio_favorito_fraco.md
relatorio_sem_favorito_claro.md
relatorio_agregado_temporada.md
```

O relatorio agregado deve responder:

```text
o que funcionou
o que falhou
onde Goal melhora
onde No Goal melhora
onde ha N baixo
onde ha overlap alto
onde a deduplicacao destruiu resultado
onde cutoff e consistente
onde familia explica o bloco
onde mandante/visitante ajuda
se vale avancar para a proxima etapa
```

---

## Decisao Operacional Atual

Nenhuma estrategia, time, perfil de favorito, rodada, fase, familia, alerta ou carteira deve ser aprovado operacionalmente.

Todas as simulacoes com odds medias devem ser classificadas como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```

---

## Restricoes

- Nao criar robo.
- Nao criar producao.
- Nao fazer backtesting financeiro real com odds medias.
- Nao usar odds live nao timestampadas.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao transformar baixa amostra em robustez.
- Nao comercializar sinais derivados do pipeline.
- Nao transformar time especifico em filtro antes de validar blocos macro.
- Nao usar cashout nesta V1.
- Nao criar pipeline antes das etapas 1 a 5.
