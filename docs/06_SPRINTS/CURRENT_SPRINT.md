# CURRENT SPRINT

## Sprint Atual

Status:

```text
ROADMAP EXPLORATORIO PRE-RANKING OPERACIONAL
```

Fase atual:

```text
ANALISE EXPLORATORIA E DESCOBERTA DE PADROES
```

Frente oficial ativa:

```text
ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
```

Frentes concluidas neste roadmap:

```text
1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1 — APROVADA COMO V1 EXPLORATORIA
2. ANALISE_REGIME_POR_FASE_V1 — APROVADA COMO V1 EXPLORATORIA
```

Proximas frentes:

```text
3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1 — ATIVA
4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1
6. RANKING_OPERACIONAL_FINAL_V1
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

## Concluido no roadmap atual

### 1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1

- [x] Agrupar familias e variacoes.
- [x] Medir overlap por fixture.
- [x] Identificar risco de duplicidade.
- [x] Confirmar que lucros de variacoes sobrepostas nao devem ser somados.

Documento:

```text
docs/04_RESEARCH/agrupamento_por_familia_e_variacoes_v1/AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

Achado principal:

```text
18 familias
714 variacoes
18 familias com alta sobreposicao
overlap maximo por fixture = 100% em todas as familias
```

### 2. ANALISE_REGIME_POR_FASE_V1

- [x] Rodar phase_count=6.
- [x] Rodar phase_count=8.
- [x] Separar Goal/Over e No Goal/Under.
- [x] Medir lucro/ROI/DD por fase.
- [x] Identificar familias consistentes e regime dependente.

Documento:

```text
docs/04_RESEARCH/analise_regime_por_fase_v1/ANALISE_REGIME_POR_FASE_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

Achados principais:

```text
Goal / Over: negativo em todas as fases no phase6 e phase8.
No Goal / Under: positivo em todas as fases no phase6 e phase8.
Melhor bloco phase6 para No Goal: fase 4.
Melhor bloco phase8 para No Goal: fase 5.
```

---

## Em andamento

### 3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1

Objetivo:

```text
Descobrir a partir de qual rodada os sinais da Serie A comecam a ficar confiaveis, sem misturar sinais bons com ruins.
```

Rodadas a testar:

```text
5, 6, 7, 8, 9, 10, 11, 12
```

Niveis obrigatorios:

```text
1. Liga geral
2. Direcao de mercado: Over/Goal/Back Over vs Under/No Goal/Lay Over
3. Familia/estrategia com todos os cutoffs/windows
```

Importante:

```text
A decisao exploratoria nao deve depender apenas da liga geral, porque Over ruim pode contaminar Under bom e uma estrategia Under ruim pode contaminar outra estrategia Under boa.
```

---

## Proximas Etapas

- [ ] Gerar prompt para `ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1`.
- [ ] Executar script da maturidade por rodada.
- [ ] Auditar entrega da maturidade por rodada.
- [ ] Atualizar GitHub com a entrega da maturidade.
- [ ] Gerar prompt para `ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1`.
- [ ] Gerar prompt para `ANALISE_PADROES_PREJUIZO_POR_TIME_V1`.
- [ ] Somente depois preparar `RANKING_OPERACIONAL_FINAL_V1`.

---

## Decisao Operacional Atual

Nenhuma estrategia deve ser aprovada operacionalmente apenas com base nas frentes exploratorias.

As frentes atuais servem para:

```text
descobrir padroes
organizar hipoteses
identificar riscos
preparar validacao preditiva/operacional posterior
```

A selecao futura deve priorizar:

```text
lucro final + ROI + EV + drawdown + sequencia maxima de perdas + robustez por time + consistencia por fase + maturidade por rodada + duplicidade por familia
```

---

## Restricoes

- Nao criar robo.
- Nao criar producao.
- Nao fazer backtesting financeiro real.
- Nao usar odds live nao timestampadas.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao aprovar operacao final durante fase exploratoria.

Todas as simulacoes com odds medias devem ser classificadas como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```
