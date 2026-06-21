# PROJECT STATUS

## Estado Atual do Projeto

FASE ATUAL:

```text
COMPARACAO BI-TEMPORADA 2024 X 2025 PRE-RANKING OPERACIONAL
```

O projeto concluiu as 5 frentes exploratorias da Serie A 2025 e ja possui a temporada Serie A 2024 processada na mesma linha metodologica.

Como o acesso atual da SportMonks limita o historico ate a temporada 2024, a validacao fora da amostra sera tratada inicialmente como comparacao bi-temporada:

```text
Serie A 2024 x Serie A 2025
```

O objetivo agora nao e aprovar operacao final. O objetivo e comparar se as estrategias mantem qualidade entre temporadas, principalmente em:

```text
rodada de maturidade
phase6
phase8
oscilacao de lucro/ROI/DD
qualidade por familia/variacao
```

A analise por time fica secundaria, pois times mudam elenco, tecnico, estilo e contexto entre temporadas.

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

Se uma solicitacao pular etapas, misturar objetivos, fragilizar a metodologia ou gerar falsa confianca operacional, o agente deve discordar primeiro, explicar o risco tecnico e propor o caminho correto.

---

## Roadmap Exploratorio Serie A 2025 — Concluido

Ordem executada:

```text
1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
2. ANALISE_REGIME_POR_FASE_V1
3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1
```

---

## Temporada 2024

A temporada 2024 foi processada seguindo a mesma cadeia metodologica principal:

```text
DISCOVERY
NORMALIZACAO_FIXTURE_LEVEL
DRAWDOWN_V4
AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
ANALISE_REGIME_POR_FASE_V1
ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1
```

Leitura atual:

```text
2024 esta aprovada como base comparativa com ressalvas exploratorias.
Nao deve ser usada ainda para ranking operacional final.
```

---

## Script orquestrador de temporada

Script planejado/necessario:

```text
PIPELINE_TEMPORADA_COMPLETA_V1
```

Papel:

```text
Executar automaticamente todos os scripts aprovados para uma temporada, preservando a organizacao atual de pastas e artefatos.
```

Importante:

```text
O PIPELINE_TEMPORADA_COMPLETA_V1 nao e uma nova analise.
Ele e um orquestrador.
Cada etapa continua gerando seus proprios CSVs, JSONs e MDs nas respectivas pastas.
O pipeline gera apenas log, manifest e relatorio de execucao.
```

Esse script deve permitir reproduzir uma temporada completa de forma consistente antes da comparacao entre temporadas.

---

## Hipoteses congeladas para comparacao 2024 x 2025

As hipoteses abaixo devem ser testadas entre 2024 e 2025 antes do ranking operacional final:

```text
1. Familias No Goal sao superiores a Goal/Over no agregado.
2. Goal/Over permanece estruturalmente pior que No Goal.
3. No Goal e lucrativo em varias fases da temporada.
4. As melhores familias No Goal amadurecem cedo.
5. A rodada de maturidade permanece semelhante entre 2024 e 2025.
6. A curva phase6 mostra estabilidade aceitavel entre temporadas.
7. A curva phase8 revela oscilacoes importantes que precisam ser medidas.
8. O melhor contexto por favorito varia por temporada; portanto, a faixa de favorito ainda e inconclusiva como filtro operacional.
9. Perfis de time sao informativos, mas nao devem dominar a validacao por causa da mudanca natural dos times entre temporadas.
10. A selecao final deve considerar familia + variacao + rodada + fase + oscilacao + drawdown, e nao apenas lucro agregado.
```

---

## Frente atual

```text
COMPARACAO_BI_TEMPORADA_QUALIDADE_E_OSCILACAO_V1
```

Objetivo:

```text
Comparar Serie A 2024 x Serie A 2025 para medir se as familias/variacoes mantem qualidade, maturidade por rodada e comportamento por phase6/phase8.
```

Pergunta principal:

```text
Quais estrategias validam nas duas temporadas com qualidade parecida, maturidade semelhante e oscilacao aceitavel?
```

Perguntas centrais:

```text
1. As estrategias validam nas mesmas rodadas?
2. No Goal continua superior ao Goal nas duas temporadas?
3. A curva phase6 e parecida entre 2024 e 2025?
4. A curva phase8 e parecida entre 2024 e 2025?
5. Onde ocorre a maior oscilacao de lucro, ROI, DD e max losing streak?
6. Quais familias sao consistentes nas duas temporadas?
7. Quais familias sao boas em uma temporada e ruins/instaveis na outra?
8. Quais variacoes mantem qualidade nas duas temporadas?
9. O favorito deve ser tratado como filtro ou apenas variavel de contexto?
```

---

## Anatomia da estrategia — etapa futura

A analise detalhada da mecanica interna de cada estrategia, por exemplo:

```text
both_teams_cold_2of3
```

com estatisticas como:

```text
ataques perigosos
chutes no gol
chutes para fora
escanteios
posse
pressao
comportamento no placar
```

fica registrada como etapa futura:

```text
ANATOMIA_DA_ESTRATEGIA_V1
```

Essa etapa deve ocorrer somente depois que a comparacao 2024 x 2025 identificar quais familias/variacoes realmente merecem virar candidatas operacionais.

---

## Roadmap a partir de agora

```text
1. PIPELINE_TEMPORADA_COMPLETA_V1
2. COMPARACAO_BI_TEMPORADA_QUALIDADE_E_OSCILACAO_V1
3. RANKING_OPERACIONAL_FINAL_V1
4. VALIDACAO_OPERACIONAL_FINAL_V1
5. ANATOMIA_DA_ESTRATEGIA_V1
6. PLAYBOOK_OPERACIONAL_FINAL
```

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

## Decisao Operacional Atual

Nenhuma estrategia, time, perfil de favorito, fase, rodada ou filtro deve ser aprovado operacionalmente antes da comparacao 2024 x 2025 e da validacao operacional final.

A escolha futura deve priorizar:

- lucro final;
- ROI;
- EV por trade;
- drawdown maximo;
- sequencia maxima de perdas;
- consistencia por temporada;
- maturidade por rodada;
- estabilidade em phase6;
- estabilidade em phase8;
- oscilacao de lucro/ROI/DD;
- contexto de favorito como variavel, nao filtro automatico;
- duplicidades por familia/variacao.

---

## Restricoes

- Nao criar robo.
- Nao criar producao.
- Nao chamar simulacao com odds medias de backtesting financeiro real.
- Nao usar odds live inexistentes.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao aprovar operacao final durante comparacao exploratoria 2024 x 2025.
