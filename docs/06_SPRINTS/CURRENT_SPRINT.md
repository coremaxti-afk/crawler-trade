# CURRENT SPRINT

## Sprint Atual

Status:

```text
VALIDACAO MULTI-TEMPORADA PRE-RANKING OPERACIONAL
```

Fase atual:

```text
VALIDACAO FORA DA AMOSTRA
```

Frente oficial ativa:

```text
VALIDACAO_MULTI_TEMPORADA_V1
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

Proximas frentes:

```text
6. VALIDACAO_MULTI_TEMPORADA_V1 — ATIVA
7. COMPARACAO_PADROES_2025_VS_OUTRAS_TEMPORADAS_V1
8. RANKING_OPERACIONAL_FINAL_V1
9. VALIDACAO_OPERACIONAL_FINAL_V1
10. PLAYBOOK_OPERACIONAL_FINAL
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

## Concluido no roadmap exploratorio atual

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

### 5. ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1

- [x] Corrigir a V1 para focar apenas familias No Goal lucrativas.
- [x] Identificar times que prejudicam No Goal.
- [x] Construir perfis de times prejudiciais.
- [x] Identificar times contraditorios.
- [x] Gerar hipoteses para validacao multi-temporada.

Documento:

```text
docs/04_RESEARCH/analise_padroes_prejuizo_por_time_v1_1/ANALISE_PADROES_PREJUIZO_POR_TIME_V1_1_SERIE_A_2025_TEMPOS_EXPANDIDOS.md
```

Achados principais:

```text
O perfil mais forte de prejuizo No Goal foi FAVORITO_MEDIO_DOMINANTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA.
São Paulo, Internacional e Botafogo sao os principais alertas exploratorios.
O problema nao e apenas o time isolado, mas time + contexto + familia.
Nenhum time deve ser excluido automaticamente com base nesta etapa.
```

---

## Hipoteses congeladas para validacao

```text
1. Familias No Goal sao superiores a Goal/Over no agregado.
2. No Goal e lucrativo em varias fases da temporada.
3. As melhores familias No Goal amadurecem cedo.
4. Jogos parelhos/sem favorito claro parecem favorecer as melhores familias No Goal.
5. Favorito medio dominante + prejuizo distribuido + multi-familia aparece como perfil recorrente de risco.
6. Alguns times sao contraditorios: bons para uma familia e ruins para outra.
7. A selecao final deve considerar familia + contexto + time, e nao apenas estrategia isolada.
```

---

## Em andamento

### 6. VALIDACAO_MULTI_TEMPORADA_V1

Objetivo:

```text
Validar se os padroes descobertos na Serie A 2025 sobrevivem em outras temporadas antes de construir o RANKING_OPERACIONAL_FINAL_V1.
```

Perguntas centrais:

```text
1. As familias No Goal continuam superiores em outras temporadas?
2. Goal/Over continua negativo em outras temporadas?
3. Jogos parelhos continuam sendo o melhor contexto para No Goal?
4. A maturidade cedo se repete?
5. O perfil FAVORITO_MEDIO_DOMINANTE/PREJUIZO_DISTRIBUIDO/MULTI_FAMILIA reaparece?
6. Os times/perfis prejudiciais de 2025 se repetem ou foram especificos da temporada?
7. Quais padroes sobrevivem o suficiente para entrar no Ranking Operacional Final?
```

---

## Proximas Etapas

- [ ] Gerar prompt para `VALIDACAO_MULTI_TEMPORADA_V1`.
- [ ] Executar validacao multi-temporada.
- [ ] Auditar resultado comparando 2025 vs outras temporadas.
- [ ] Separar padroes confirmados, enfraquecidos e reprovados.
- [ ] Atualizar GitHub com a validacao multi-temporada.
- [ ] Preparar `RANKING_OPERACIONAL_FINAL_V1` apenas com padroes confirmados.

---

## Decisao Operacional Atual

Nenhuma estrategia, time ou filtro deve ser aprovado operacionalmente antes da validacao multi-temporada.

As frentes atuais servem para:

```text
descobrir padroes
organizar hipoteses
identificar riscos
preparar validacao fora da amostra
```

A selecao futura deve priorizar:

```text
lucro final + ROI + EV + drawdown + sequencia maxima de perdas + robustez por time + consistencia por fase + maturidade por rodada + contexto de favorito + perfil de prejuizo por time + duplicidade por familia + robustez multi-temporada
```

---

## Restricoes

- Nao criar robo.
- Nao criar producao.
- Nao fazer backtesting financeiro real.
- Nao usar odds live nao timestampadas.
- Nao agregar estrategias parecidas sem deduplicacao e auditoria.
- Nao aprovar operacao final durante fase exploratoria ou validacao multi-temporada.

Todas as simulacoes com odds medias devem ser classificadas como:

```text
ESTIMATIVA OPERACIONAL COM ODDS MEDIAS
```
