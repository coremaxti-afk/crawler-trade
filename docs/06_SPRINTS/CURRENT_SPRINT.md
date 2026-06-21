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
ANALISE_PADROES_PREJUIZO_POR_TIME_V1
```

Frentes concluidas neste roadmap:

```text
1. AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1 — APROVADA COMO V1 EXPLORATORIA
2. ANALISE_REGIME_POR_FASE_V1 — APROVADA COMO V1 EXPLORATORIA
3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1 — APROVADA COMO V1 EXPLORATORIA
4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1 — APROVADA COMO V1 EXPLORATORIA COM RESSALVA DE INTERPRETACAO
```

Proximas frentes:

```text
5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1 — ATIVA
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

### 3. ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1

- [x] Testar rodadas 5, 6, 7, 8, 9, 10, 11, 12.
- [x] Separar liga geral, direcao de mercado, familia e variacao.
- [x] Confirmar que liga geral pode ser contaminada por direcao negativa.
- [x] Confirmar que No Goal amadurece cedo nas melhores familias.

Documento:

```text
docs/04_RESEARCH/analise_maturidade_liga_por_rodada_v1/ANALISE_MATURIDADE_LIGA_POR_RODADA_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

Achados principais:

```text
Liga geral pode enganar por misturar Goal ruim com No Goal bom.
Goal / Over continua ruim mesmo removendo rodadas iniciais.
No Goal / Under permanece positivo desde a primeira rodada testada.
As melhores familias No Goal amadurecem cedo.
```

Ressalva:

```text
A V1 testou apenas rodadas 5 a 12.
Ainda nao prova se a maturidade comeca na rodada 5 ou antes.
```

### 4. ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1

- [x] Segmentar por favorito forte, medio, fraco e jogo parelho.
- [x] Separar Goal/Over e No Goal/Under.
- [x] Comparar tudo junto vs segmentado.
- [x] Identificar segmentos mais fortes e segmentos perigosos.

Documento:

```text
docs/04_RESEARCH/analise_forca_favorito_por_estrategia_v1/ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

Achados principais:

```text
A forca do favorito importa.
As melhores familias No Goal parecem mais fortes em jogos parelhos/sem favorito claro.
Goal nao ficou lucrativo no agregado em nenhum segmento.
Algumas familias Goal geraram hipoteses segmentadas, mas com risco de overfitting.
both_teams_cold_2of3 parece especialmente interessante em jogos parelhos.
favorite_winning_by_1_opp_cold_2of3 teve melhor resultado em jogo parelho do que em favorito forte.
```

---

## Em andamento

### 5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1

Objetivo:

```text
Descobrir quais caracteristicas aparecem nos times que deram prejuizo para cada estrategia/familia.
```

Perguntas centrais:

```text
1. Quais times deram prejuizo para cada familia?
2. Quais padroes esses times tinham?
3. O prejuizo aparece em determinados contextos de favorito/equilibrio?
4. O prejuizo aparece em determinadas fases da temporada?
5. O prejuizo aparece em determinadas janelas/cutoffs?
6. Existem perfis de time que quebram No Goal no fim do jogo?
```

Insumos obrigatorios:

```text
RENTABILIDADE_DAS_ESTRATEGIAS_POR_TIME_V4
AGRUPAMENTO_POR_FAMILIA_E_VARIACOES_V1
ANALISE_REGIME_POR_FASE_V1
ANALISE_MATURIDADE_DA_LIGA_POR_RODADA_V1
ANALISE_FORCA_FAVORITO_POR_ESTRATEGIA_V1
```

---

## Proximas Etapas

- [ ] Gerar prompt para `ANALISE_PADROES_PREJUIZO_POR_TIME_V1`.
- [ ] Executar script de padroes de prejuizo por time.
- [ ] Auditar entrega.
- [ ] Atualizar GitHub com a entrega.
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
lucro final + ROI + EV + drawdown + sequencia maxima de perdas + robustez por time + consistencia por fase + maturidade por rodada + contexto de favorito + duplicidade por familia
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
