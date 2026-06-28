# PLANO_ESTUDO_FORCA_ESTADO_TEMPERATURA_JOGO_V1

## Status

```text
FRENTE_COMPLEMENTAR_ATIVA
STATUS: PLANEJAMENTO_ESTRUTURADO
NAO APROVA OPERACAO REAL
NAO INVALIDA O ENCERRAMENTO_CIENTIFICO_GOLS_TARDIOS_V1
```

Esta frente organiza o estudo complementar sobre a interacao entre:

```text
forca do favorito
estado do favorito/time no placar
temperatura do jogo
direcao de mercado Goal / No Goal
cutoff
familia de estrategia
mandante/visitante
time especifico, apenas em etapa posterior
```

A frente nasce a partir da validacao de segmentacao por forca do favorito, que indicou que o agregado por liga pode esconder comportamentos diferentes entre contextos Over/Goal e Under/No Goal.

---

## Tese cientifica inicial

Hipotese macro:

```text
Favorito forte/medio possui maior qualidade tecnica e poder ofensivo para transformar jogo quente em gol.
Favorito fraco/sem favorito claro possui menor capacidade tecnica de converter pressao em gol; em jogo frio, tende a combinar melhor com No Goal.
```

Leitura esperada:

```text
FAVORITO_FORTE + JOGO_QUENTE -> Goal
FAVORITO_MEDIO + JOGO_QUENTE -> Goal
FAVORITO_FRACO + JOGO_FRIO -> No Goal
SEM_FAVORITO_CLARO_OU_JOGO_PARELHO + JOGO_FRIO -> No Goal
```

A tese deve ser refinada com o estado do favorito/time no placar:

```text
FAVORITO_GANHANDO
FAVORITO_EMPATANDO
FAVORITO_PERDENDO
```

Para jogos sem favorito claro, usar leitura por lado analisado:

```text
LADO_ANALISADO_GANHANDO
EMPATE
LADO_ANALISADO_PERDENDO
```

---

## Regra central de escopo

O estudo deve ser completo, mas hierarquico.

Nao executar uma unica matriz total como decisao principal com:

```text
forca x estado x temperatura x direcao x cutoff x familia x casa/fora x time
```

Motivo: a combinacao explode o numero de blocos, reduz N por celula e aumenta o risco de falso positivo.

Exemplo de explosao:

```text
4 forcas do favorito
x 3 estados do placar
x 3 temperaturas
x 2 direcoes
x 5 cutoffs
= 360 blocos

360 x 2 casa/fora = 720 blocos
720 x 15 familias = 10.800 combinacoes
720 x 17 familias = 12.240 combinacoes
```

Se adicionar time especifico cedo demais:

```text
720 x 20 times = 14.400 combinacoes
14.400 x 15 familias = 216.000 combinacoes
```

Conclusao metodologica:

```text
primeiro provar o fenomeno macro
depois explicar por familia
depois investigar casa/fora
depois investigar time especifico apenas nos blocos sobreviventes
```

---

## Ordem oficial das etapas

### Etapa 1 — Classificador base

Script planejado:

```text
classificar_contexto_forca_estado_temperatura_v1.py
```

Responsabilidade:

```text
ler trades e entradas existentes
classificar forca do favorito
classificar estado do favorito/time no placar
classificar temperatura do jogo
classificar mandante/visitante
marcar direcao Goal / No Goal
marcar cutoff
marcar familia e estrategia
criar base unica classificada
```

Este script nao deve aprovar, rankear ou decidir nada.

Saidas esperadas:

```text
trades_classificados_forca_estado_temperatura_v1.csv
manifesto_classificacao_contexto_v1.md
```

---

### Etapa 2 — Matriz macro da tese

Script planejado:

```text
validacao_matriz_forca_estado_temperatura_v1.py
```

Responsabilidade:

```text
testar forca do favorito x estado x temperatura x direcao x cutoff
sem quebrar por familia como decisao principal
comparar blocos esperados contra controles
aplicar deduplicacao em multiplos niveis
```

A decisao principal deve usar:

```text
resultado deduplicado por fixture
```

Saidas esperadas:

```text
matriz_macro_por_bloco.csv
comparacao_goal_no_goal_por_bloco.csv
ranking_blocos_macro.csv
relatorio_matriz_macro_temporada.md
manifesto_validacao_matriz_macro.md
```

---

### Etapa 3 — Familias explicativas dos blocos sobreviventes

Script planejado:

```text
analise_familias_blocos_matriz_v1.py
```

Responsabilidade:

```text
abrir por familia apenas os blocos macro promissores
identificar quais familias explicam o resultado
separar familia explicativa de familia descartada
impedir conclusao baseada em familia com N baixo
```

Regra:

```text
familia nao deve ser usada para cacar vencedor em bloco macro ruim
familia serve para explicar ou fragilizar blocos macro sobreviventes
```

Saidas esperadas:

```text
familias_por_bloco_promissor.csv
familias_descartadas_por_bloco.csv
relatorio_familias_blocos_promissores.md
```

---

### Etapa 4 — Mandante/visitante como camada auxiliar

Script planejado:

```text
analise_mandante_visitante_blocos_v1.py
```

Responsabilidade:

```text
abrir blocos macro/familia sobreviventes por favorito mandante/visitante
ou por lado analisado mandante/visitante quando nao houver favorito claro
```

Regra:

```text
mandante/visitante e diagnostico auxiliar na V1
nao e criterio principal de aprovacao da tese
```

Travas sugeridas:

```text
bloco principal N >= 100
subgrupo mandante/visitante N >= 50
```

Se nao bater, classificar como:

```text
INSIGHT_AUXILIAR_N_BAIXO
```

Saidas esperadas:

```text
mandante_visitante_por_bloco.csv
relatorio_mandante_visitante_blocos.md
```

---

### Etapa 5 — Agregador da temporada

Script planejado:

```text
agregar_estudo_forca_estado_temperatura_temporada_v1.py
```

Responsabilidade:

```text
ler todos os artefatos anteriores da mesma temporada
gerar relatorios por forca do favorito
gerar relatorio agregado da temporada
nao gerar estabilidade multi-temporada
```

Relatorios esperados por temporada:

```text
relatorio_favorito_forte.md
relatorio_favorito_medio.md
relatorio_favorito_fraco.md
relatorio_sem_favorito_claro.md
relatorio_agregado_temporada.md
```

Cada relatorio por forca deve conter:

```text
ganhando + quente + Goal
ganhando + frio + Goal
empatando + quente + Goal
empatando + frio + Goal
perdendo + quente + Goal
perdendo + frio + Goal
os mesmos cenarios para No Goal
cutoffs
familias explicativas
mandante/visitante auxiliar
alertas
```

---

### Etapa 6 — Times especificos, apenas depois

Script futuro planejado:

```text
analise_times_blocos_promissores_v1.py
```

Status:

```text
POSTERIOR
NAO EXECUTAR NA PRIMEIRA RODADA
```

Responsabilidade futura:

```text
pegar apenas blocos macro/familia ja promissores
ver se o resultado se concentra em poucos times
identificar dependencia de clube, elenco ou perfil historico
```

Regra:

```text
nao testar todos os times em todos os cenarios desde o inicio
nao transformar concentracao em poucos times em robustez
```

---

### Etapa 7 — Pipeline do estudo

Script futuro planejado:

```text
executar_pipeline_estudo_forca_estado_temperatura_v1.py
```

Status:

```text
SOMENTE DEPOIS QUE AS ETAPAS 1 A 5 EXISTIREM E FOREM VALIDADAS
```

Responsabilidade:

```text
executar a esteira completa por season_id
respeitar isolamento por temporada
agregar artefatos sem misturar temporadas indevidamente
nao aprovar operacao real
```

---

## Deduplicacao obrigatoria

Todo relatorio deve separar:

```text
N_trades_bruto
fixtures_unicos
N_pos_deduplicacao_por_cutoff
N_pos_deduplicacao_por_fixture
exposicoes_por_fixture
```

A leitura final deve priorizar:

```text
N_pos_deduplicacao_por_fixture
```

Motivo:

```text
evitar que o mesmo jogo seja analisado varias vezes na mesma conclusao
```

O lucro bruto antes da deduplicacao deve ser tratado apenas como diagnostico de overlap.

---

## Cutoff

A analise deve ter tres visoes:

```text
1. cutoff individual
2. agregado de cutoffs
3. melhor cutoff como hipotese futura
```

Regra:

```text
cutoff individual = diagnostico
agregado deduplicado = leitura principal
melhor cutoff = hipotese para validacao posterior
```

Nao escolher o melhor cutoff depois do resultado e declarar aprovacao.

---

## Hold e cashout

Decisao oficial para V1:

```text
HOLD COMO BASE PRINCIPAL
CASHOUT FORA DO ESCOPO DA V1
```

Motivo:

```text
a V1 testa se o contexto gera a direcao correta
cashout testa politica de saida e deve ser estudo separado
```

Futuro possivel:

```text
VALIDACAO_POLITICA_SAIDA_CASHOUT_V1
```

Somente se a tese macro sobreviver.

---

## Niveis de evidencia

Cada bloco deve receber um nivel:

```text
EVIDENCIA_FORTE
EVIDENCIA_MODERADA
EVIDENCIA_FRACA
INCONCLUSIVO
REJEITADO
```

Criterios de avaliacao:

```text
N suficiente
fixtures unicos suficientes
ROI positivo
EV positivo
lucro positivo
drawdown aceitavel
lucro/DD adequado
sobrevive deduplicacao por fixture
nao depende de apenas um cutoff
nao depende de uma unica familia
nao depende de poucos times
```

---

## Relacao com estudos anteriores

Esta frente reaproveita a esteira e os artefatos existentes, principalmente:

```text
strategy_drawdown_trades
strategy_drawdown_summary
discovery_entries_v4
validacao_segmentacao_forca_favorito_v1
analise_forca_favorito_por_estrategia_v1
agrupamento_por_familia_e_variacoes_v1
analise_regime_por_fase
analise_maturidade_liga_por_rodada
analise_padrao_por_time, apenas em etapa posterior
```

Reaproveitar como fonte, sem alterar artefatos historicos.

---

## Regras permanentes

```text
NAO aprovar operacao real
NAO criar robo
NAO vender sinais
NAO chamar odds medias de backtesting financeiro real
NAO misturar temporadas sem isolamento por season_id
NAO somar familias sobrepostas sem deduplicacao
NAO usar time especifico como filtro antes dos blocos macro sobreviverem
NAO usar cashout na V1
NAO transformar melhor cutoff retrospectivo em regra final
```

Todos os resultados financeiros devem permanecer como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```

---

## Decisao atual

```text
SEGUIR CRONOGRAMA HIERARQUICO
INICIAR PELA ETAPA 1 — CLASSIFICADOR BASE
GERAR PIPELINE APENAS DEPOIS DAS ETAPAS 1 A 5
```
