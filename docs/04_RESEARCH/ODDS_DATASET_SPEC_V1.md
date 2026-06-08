# ODDS DATASET SPEC V1

## Status

Especificacao metodologica do Dataset de Odds V1.

Nao contem codigo.

Nao cria dataset.

Nao executa baseline.

Nao cria modelo.

Nao faz backtesting.

Nao cria producao.

---

## 1. Objetivo

Definir o desenho metodologico do Dataset de Odds V1 a partir do catalogo:

- `docs/04_RESEARCH/ODDS_FEATURE_CATALOG_V1.md`

A finalidade do Dataset de Odds V1 e permitir validacao estatistica futura das odds historicas pre-jogo contra gols tardios, mantendo regras anti-leakage e controle de complexidade.

---

## 2. Decisao Quant

O Dataset de Odds V1 deve comecar com um escopo reduzido e auditavel.

Prioridade V1:

1. Over/Under 2.5
2. Match Odds 1X2

Asian Handicap deve ficar para versao futura.

Motivo:

- Over/Under 2.5 mede expectativa direta de gols.
- Match Odds 1X2 mede forca relativa e equilibrio.
- Asian Handicap exige tratamento adicional de linhas, direcao do handicap e normalizacao, aumentando risco metodologico na V1.

---

## 3. Grain do Dataset

Grain oficial:

```text
1 linha por match_id
```

Justificativa:

- odds sao informacao pre-jogo;
- nao variam por cutoff na V1;
- podem ser reutilizadas futuramente em interacoes com cutoffs in-game, mas o dataset base deve permanecer match-level.

Chave primaria esperada:

```text
match_id
```

Chaves auxiliares esperadas:

- `sofascore_event_id`, se disponivel;
- `football_data_match_id`, se disponivel;
- `league`;
- `season`;
- `match_date`;
- `home_team`;
- `away_team`.

---

## 4. Fontes Utilizadas

Fontes aprovadas:

- Football-Data odds historicas importadas.
- Dataset master de partidas para identificacao e join.
- Dataset target aprovado apenas para anexar target em validacao futura, nao obrigatoriamente no dataset de features.

Mercados aprovados para V1:

- Match Odds 1X2.
- Over/Under 2.5.

Tipos de odds aprovados para V1:

1. closing odds;
2. average odds;
3. max odds apenas como campo auxiliar/auditoria, nao como feature primaria.

Recomendacao Quant:

- usar closing odds como fonte primaria;
- usar average odds como fallback controlado ou feature secundaria;
- nao priorizar max odds como feature V1.

---

## 5. Features Aprovadas para V1

### 5.1 Over/Under 2.5

Features obrigatorias:

- `odds_over25_close`
- `odds_under25_close`
- `implied_prob_over25_raw`
- `implied_prob_under25_raw`
- `implied_prob_over25_norm`
- `implied_prob_under25_norm`
- `over25_closing_strength`
- `over25_market_balance`

Definicoes:

#### odds_over25_close

Odd de fechamento pre-jogo para Over 2.5.

Interpretacao:

- menor odd indica maior expectativa de Over.

#### odds_under25_close

Odd de fechamento pre-jogo para Under 2.5.

Interpretacao:

- menor odd indica maior expectativa de Under.

#### implied_prob_over25_raw

```text
1 / odds_over25_close
```

Interpretacao:

- probabilidade implicita bruta do Over 2.5, ainda com margem da casa.

#### implied_prob_under25_raw

```text
1 / odds_under25_close
```

#### implied_prob_over25_norm

Probabilidade implicita do Over 2.5 normalizada removendo margem simples do mercado:

```text
implied_prob_over25_raw / (implied_prob_over25_raw + implied_prob_under25_raw)
```

#### implied_prob_under25_norm

```text
implied_prob_under25_raw / (implied_prob_over25_raw + implied_prob_under25_raw)
```

#### over25_closing_strength

Forca relativa do Over 2.5.

Formula recomendada:

```text
implied_prob_over25_norm - implied_prob_under25_norm
```

Interpretacao:

- valor positivo: mercado favorece Over;
- valor negativo: mercado favorece Under.

#### over25_market_balance

Equilibrio do mercado Over/Under.

Formula recomendada:

```text
abs(implied_prob_over25_norm - implied_prob_under25_norm)
```

Interpretacao:

- valor baixo: mercado equilibrado;
- valor alto: mercado direcional.

---

### 5.2 Match Odds 1X2

Features obrigatorias:

- `odds_home_close`
- `odds_draw_close`
- `odds_away_close`
- `implied_prob_home_raw`
- `implied_prob_draw_raw`
- `implied_prob_away_raw`
- `implied_prob_home_norm`
- `implied_prob_draw_norm`
- `implied_prob_away_norm`
- `favorite_side`
- `favorite_strength`
- `match_balance`

#### odds_home_close

Odd de fechamento pre-jogo para vitoria do mandante.

#### odds_draw_close

Odd de fechamento pre-jogo para empate.

#### odds_away_close

Odd de fechamento pre-jogo para vitoria do visitante.

#### implied_prob_home_raw

```text
1 / odds_home_close
```

#### implied_prob_draw_raw

```text
1 / odds_draw_close
```

#### implied_prob_away_raw

```text
1 / odds_away_close
```

#### implied_prob_home_norm

Probabilidade normalizada removendo margem simples do mercado 1X2:

```text
implied_prob_home_raw / (implied_prob_home_raw + implied_prob_draw_raw + implied_prob_away_raw)
```

#### implied_prob_draw_norm

```text
implied_prob_draw_raw / (implied_prob_home_raw + implied_prob_draw_raw + implied_prob_away_raw)
```

#### implied_prob_away_norm

```text
implied_prob_away_raw / (implied_prob_home_raw + implied_prob_draw_raw + implied_prob_away_raw)
```

#### favorite_side

Lado com maior probabilidade normalizada entre mandante e visitante.

Valores esperados:

- `home`
- `away`
- `none_clear`, se diferenca abaixo de limiar minimo definido no builder.

#### favorite_strength

Intensidade do favoritismo.

Formula recomendada:

```text
max(implied_prob_home_norm, implied_prob_away_norm) - min(implied_prob_home_norm, implied_prob_away_norm)
```

Observacao:

- empate nao entra como favorito, mas influencia normalizacao.

#### match_balance

Equilibrio geral do mercado 1X2.

Formula recomendada:

```text
1 - (max(implied_prob_home_norm, implied_prob_draw_norm, implied_prob_away_norm) - min(implied_prob_home_norm, implied_prob_draw_norm, implied_prob_away_norm))
```

Interpretacao:

- maior valor: jogo mais equilibrado;
- menor valor: jogo mais desequilibrado.

---

## 6. Features Bloqueadas na V1

Bloqueadas para V1:

- `handicap_line`
- `favorite_handicap`
- `handicap_implied_strength`
- `handicap_market_confidence`
- qualquer feature derivada de Asian Handicap;
- odds live;
- odds in-play;
- odds apos kickoff;
- odds com timestamp incerto e risco de in-play;
- features de movimento de odds sem timestamp confiavel;
- diferencas entre abertura e fechamento, salvo se abertura pre-jogo estiver claramente disponivel e validada.

Motivo do bloqueio Asian Handicap:

- linhas podem variar por bookmaker;
- direcao do handicap exige padronizacao;
- mercados podem ter multiplas linhas por partida;
- risco de criar feature ambigua na primeira versao.

---

## 7. Regras Anti-Leakage

Regras obrigatorias:

1. Somente odds disponiveis antes do kickoff.
2. Nenhuma odd live/in-play.
3. Nenhuma atualizacao apos inicio do jogo.
4. Nenhuma informacao de resultado, placar final ou target na construcao das features.
5. Target, quando anexado em dataset analitico futuro, deve ser usado apenas como resposta.
6. Se closing odds nao tiverem garantia pre-kickoff, marcar como risco e bloquear uso em modelagem futura ate auditoria.
7. Features derivadas devem ser calculadas exclusivamente a partir das odds aprovadas.

Risco de leakage por tipo:

- Closing odds com timestamp pre-kickoff confirmado: baixo.
- Average odds pre-jogo sem timestamp individual: medio-baixo.
- Max odds sem timestamp: medio.
- Odds live/in-play: alto, proibido.

---

## 8. Validações Obrigatórias

Validation report deve confirmar:

### Cobertura

- numero de partidas no dataset;
- numero de partidas com Match Odds 1X2;
- numero de partidas com Over/Under 2.5;
- numero de partidas com ambas as familias;
- percentual de cobertura por mercado.

### Unicidade

- 0 duplicatas por `match_id`.

### Odds validas

- odds > 1.0;
- probabilidades brutas entre 0 e 1;
- probabilidades normalizadas entre 0 e 1;
- soma das probabilidades normalizadas do mercado 1X2 aproximadamente 1;
- soma das probabilidades normalizadas do mercado OU2.5 aproximadamente 1.

### Anti-leakage

- sem odds live/in-play;
- sem colunas de target em X;
- sem placar final;
- sem estatisticas full-match;
- sem eventos pos-kickoff.

### Nulos

Reportar nulos por feature.

Regras:

- se Over/Under 2.5 ausente, features OU devem ficar nulas;
- se 1X2 ausente, features 1X2 devem ficar nulas;
- nao imputar na criacao do dataset.

### Ranges

Reportar minimo, maximo e media de:

- `implied_prob_over25_norm`;
- `implied_prob_home_norm`;
- `implied_prob_draw_norm`;
- `implied_prob_away_norm`;
- `favorite_strength`;
- `match_balance`;
- `over25_closing_strength`.

---

## 9. Metadata Esperada

Arquivo esperado:

- `data/processed/features/odds_features_v1_metadata.json`

Campos minimos:

- `dataset_name`;
- `dataset_version`;
- `generated_at_utc`;
- `source_tables`;
- `source_files`, se aplicavel;
- `markets_included`;
- `markets_blocked`;
- `odds_types_included`;
- `row_count`;
- `unique_matches`;
- `feature_columns`;
- `blocked_features`;
- `anti_leakage_rules`;
- `known_limitations`;
- `status`.

---

## 10. Validation Report Esperado

Arquivo esperado:

- `data/processed/features/odds_features_v1_validation_report.json`

Campos minimos:

- `status`;
- `row_count`;
- `expected_matches`;
- `unique_matches`;
- `duplicate_match_id_rows`;
- `coverage_1x2_count`;
- `coverage_ou25_count`;
- `coverage_both_count`;
- `invalid_odds_count`;
- `invalid_probability_count`;
- `probability_sum_1x2_max_abs_error`;
- `probability_sum_ou25_max_abs_error`;
- `target_columns_present`;
- `full_match_columns_present`;
- `inplay_odds_detected`;
- `leakage_warnings`;
- `nulls_by_feature`;
- `validation_errors`;
- `validation_warnings`.

Status permitido:

- `APTO`;
- `APTO COM RESSALVAS`;
- `BLOQUEADO`.

---

## 11. Features que Entram na V1

Entram:

### Expectativa de gols

- `odds_over25_close`
- `odds_under25_close`
- `implied_prob_over25_norm`
- `implied_prob_under25_norm`
- `over25_closing_strength`
- `over25_market_balance`

### Forca relativa

- `odds_home_close`
- `odds_draw_close`
- `odds_away_close`
- `implied_prob_home_norm`
- `implied_prob_draw_norm`
- `implied_prob_away_norm`
- `favorite_side`
- `favorite_strength`
- `match_balance`

Features raw tambem podem ser exportadas para auditoria:

- `implied_prob_over25_raw`
- `implied_prob_under25_raw`
- `implied_prob_home_raw`
- `implied_prob_draw_raw`
- `implied_prob_away_raw`

---

## 12. Features para Versoes Futuras

Ficam para V2 ou posterior:

### Asian Handicap

- `handicap_line`
- `favorite_handicap`
- `handicap_implied_strength`
- `handicap_market_confidence`

### Movimento de mercado

- abertura vs fechamento;
- closing line movement;
- drift do favorito;
- steam move;
- variacao over/under.

### Dispersao entre casas

- max-min odds;
- diferenca entre max e average;
- consenso vs outlier.

Motivo:

- exigem timestamps ou padronizacao adicional;
- maior risco de leakage/metodologia ambigua;
- devem ser tratados apos V1 validada.

---

## 13. Como Combinar Odds com H8 e Segmentacao Futuramente

Somente apos validacao estatistica isolada de odds.

Interacoes futuras candidatas:

### Odds + H8

- `implied_prob_over25_norm + shots_last_10m`
- `implied_prob_over25_norm + momentum_trend_last_10m`
- `favorite_strength + shots_last_10m`
- `favorite_strength + momentum_trend_last_10m`

### Odds + Segmentacao

- `favorite_strength + defensivo_fragile`
- `implied_prob_over25_norm + defensivo_fragile`
- `favorite_strength + ofensivo_forte_vs_defesa_fragil`

### Odds + Match State

- favorito forte empatando aos 60/65/70;
- favorito forte perdendo por 1;
- Over forte + 3 gols ja marcados;
- Under forte + pressao H8 alta.

### Odds + Segmentacao + H8

- `defensivo_fragile + shots_last_10m + implied_prob_over25_norm`
- `ofensivo_forte_vs_defesa_fragil + shots_last_10m + favorite_strength`

Regra:

- nao criar interacoes antes de validar odds isoladas;
- limitar numero de combinacoes para evitar p-hacking.

---

## 14. Riscos Metodologicos

1. Closing odds podem estar sem timestamp individual.
2. Max odds podem refletir momentos nao controlados.
3. Overround precisa ser normalizado.
4. Asian Handicap pode ter multiplas linhas.
5. Bookmakers diferentes podem ter cobertura desigual.
6. Odds representam consenso do mercado, nao causalidade.
7. Uma temporada unica limita significancia.
8. Muitas features de odds aumentam risco de multipla testagem.
9. Interacoes com H8/Segmentacao podem gerar overfitting exploratorio.

Mitigacao:

- V1 enxuta;
- normalizacao simples de probabilidades;
- validation report rigoroso;
- sem modelo antes de validacao estatistica;
- sem interacoes antes da fase isolada.

---

## 15. Proxima Etapa Recomendada

Apos aprovacao deste documento:

1. CTO revisar se o escopo tecnico do builder e viavel.
2. Codex implementar `Odds Feature Builder V1` como script isolado.
3. Gerar metadata e validation report.
4. Quant revisar artefatos.
5. Somente depois autorizar `ODDS INITIAL STATISTICAL VALIDATION`.

---

## 16. Decisao Quant

```text
ODDS DATASET SPEC V1 APROVADO METODOLOGICAMENTE
```

Status:

```text
PRONTO PARA REVISAO PM/CTO
```

Restricoes mantidas:

- nao criar modelo;
- nao executar baseline;
- nao fazer backtesting;
- nao criar producao;
- nao usar odds live/in-play;
- nao usar target como feature.
