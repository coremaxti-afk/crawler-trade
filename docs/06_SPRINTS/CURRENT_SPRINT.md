# CURRENT SPRINT

## Sprint Atual

Status:

```text
PREPARACAO DA COMPARACAO 2024 X 2025
```

Fase atual:

```text
ORQUESTRACAO DE TEMPORADA + COMPARACAO BI-TEMPORADA
```

Frente oficial ativa:

```text
PIPELINE_TEMPORADA_COMPLETA_V1
```

Frente analitica seguinte:

```text
COMPARACAO_BI_TEMPORADA_QUALIDADE_E_OSCILACAO_V1
```

---

## Contexto

O projeto concluiu o roadmap exploratorio da Serie A 2025 e ja processou a Serie A 2024 com a mesma familia de estudos.

Como nao ha acesso atual a 2023 via SportMonks, a validacao fora da amostra sera inicialmente uma comparacao bi-temporada:

```text
Serie A 2024 x Serie A 2025
```

O foco deixa de ser validacao por time especifico e passa a ser:

```text
rodada de maturidade
phase6
phase8
oscilacao de lucro
oscilacao de ROI
oscilacao de drawdown
max losing streak
qualidade por familia/variacao
```

---

## Script que analisa/orquestra todos os dados da temporada

### PIPELINE_TEMPORADA_COMPLETA_V1

Papel:

```text
Rodar automaticamente todos os scripts aprovados para uma temporada.
```

Etapas esperadas:

```text
1. DISCOVERY
2. NORMALIZACAO_FIXTURE_LEVEL
3. DRAWDOWN_V4
4. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
5. ANALISE_REGIME_POR_FASE_V1
6. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
7. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
8. ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1
```

Regra:

```text
O pipeline apenas orquestra.
Ele nao muda calculos.
Ele nao consolida resultados analiticos em um unico MD/CSV.
Cada script segue gerando seus proprios artefatos nas respectivas pastas.
```

Artefatos do proprio pipeline:

```text
INVENTARIO_PIPELINE_TEMPORADA_COMPLETA_V1.csv
pipeline_temporada_completa_v1.log
pipeline_temporada_completa_v1_manifest.json
PIPELINE_TEMPORADA_COMPLETA_V1_RELATORIO.md
```

---

## Roadmap exploratorio Serie A 2025 concluido

Frentes concluidas:

```text
1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1 — APROVADA COMO V1 EXPLORATORIA
2. ANALISE_REGIME_POR_FASE_V1 — APROVADA COMO V1 EXPLORATORIA
3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1 — APROVADA COMO V1 EXPLORATORIA
4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1 — APROVADA COMO V1 EXPLORATORIA COM RESSALVA DE INTERPRETACAO
5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1 — APROVADA COMO V1_1 EXPLORATORIA
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

Se uma solicitacao pular etapas, misturar objetivos ou fragilizar a metodologia, o agente deve discordar primeiro e propor o caminho correto.

---

## Hipoteses congeladas para comparacao 2024 x 2025

```text
1. Familias No Goal sao superiores a Goal/Over no agregado.
2. No Goal e lucrativo em varias fases da temporada.
3. As melhores familias No Goal amadurecem cedo.
4. A maturidade por rodada deve ser parecida entre 2024 e 2025.
5. A curva phase6 deve ser medida para estabilidade.
6. A curva phase8 deve ser medida para oscilacao.
7. A segmentacao por favorito importa, mas a melhor faixa ainda e inconclusiva.
8. Favorito forte nao deve ser automaticamente privilegiado.
9. Time especifico nao deve dominar a validacao porque muda muito entre temporadas.
10. Perfis/contextos podem ser mantidos como variaveis auxiliares.
```

---

## Em andamento

### 1. PIPELINE_TEMPORADA_COMPLETA_V1

Objetivo:

```text
Garantir que qualquer temporada seja processada de forma reprodutivel e com os mesmos artefatos das frentes aprovadas.
```

Critico:

```text
Nao transformar o pipeline em relatorio analitico consolidado.
Nao gerar um CSV gigante com todos os resultados.
Nao gerar um MD gigante com todas as analises.
```

### 2. COMPARACAO_BI_TEMPORADA_QUALIDADE_E_OSCILACAO_V1

Objetivo:

```text
Comparar 2024 x 2025 por familia, variacao, rodada, phase6, phase8, lucro, ROI, DD, max losing streak e N.
```

Perguntas centrais:

```text
1. As estrategias validam nas mesmas rodadas?
2. A qualidade do lucro/ROI e parecida?
3. O drawdown piora muito de uma temporada para outra?
4. A curva phase6 e estavel?
5. A curva phase8 revela oscilacao perigosa?
6. Quais familias validam nas duas temporadas?
7. Quais familias validam so em uma temporada?
8. Quais variacoes devem ser rebaixadas por instabilidade?
```

---

## Anatomia da Estrategia — futura, nao agora

A analise detalhada de mecanica interna, como ataques perigosos, chutes no gol, chutes para fora, escanteios e pressao, fica registrada para depois:

```text
ANATOMIA_DA_ESTRATEGIA_V1
```

Ela deve ser aplicada apenas nas familias/variacoes que sobreviverem a comparacao 2024 x 2025.

---

## Proximas Etapas

- [ ] Finalizar/validar `PIPELINE_TEMPORADA_COMPLETA_V1`.
- [ ] Garantir que 2024 e 2025 tenham artefatos equivalentes.
- [ ] Gerar prompt para `COMPARACAO_BI_TEMPORADA_QUALIDADE_E_OSCILACAO_V1`.
- [ ] Executar comparacao 2024 x 2025.
- [ ] Separar estrategias em confirmadas, oscilantes, reprovadas e inconclusivas.
- [ ] Atualizar GitHub com a comparacao.
- [ ] Somente depois preparar `RANKING_OPERACIONAL_FINAL_V1`.

---

## Decisao Operacional Atual

Nenhuma estrategia, time, perfil de favorito, rodada ou fase deve ser aprovado operacionalmente antes da comparacao 2024 x 2025 e da validacao operacional final.

A selecao futura deve priorizar:

```text
lucro final + ROI + EV + drawdown + sequencia maxima de perdas + maturidade por rodada + estabilidade phase6 + estabilidade phase8 + oscilacao entre temporadas + duplicidade por familia
```

---

## Restricoes

- Nao criar robo.
- Nao criar producao.
- Nao fazer backtesting financeiro real.
- Nao usar odds live nao timestampadas.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao aprovar operacao final durante comparacao exploratoria 2024 x 2025.

Todas as simulacoes com odds medias devem ser classificadas como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```
