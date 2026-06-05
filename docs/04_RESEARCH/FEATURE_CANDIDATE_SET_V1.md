# FEATURE CANDIDATE SET V1

## Status

Documento de consolidacao metodologica.

Nao contem codigo.

Nao contem modelos.

Nao executa baseline.

---

## Objetivo

Consolidar as features avaliadas ate o momento no LateGoalResearch, classificando-as como:

- APROVADA / MANTER
- OBSERVAR
- BLOQUEADA
- DESCARTAR

Este documento nao substitui os relatorios estatisticos originais. Ele resume o estado atual para orientar a proxima decisao do PM/Quant antes de qualquer baseline ou modelagem.

---

## Fontes de Referencia

Documentos usados como base:

- `docs/04_RESEARCH/INITIAL_STATISTICAL_VALIDATION_H6_H9.md`
- `docs/04_RESEARCH/STATISTICAL_VALIDATION_H1_H2.md`
- `docs/04_RESEARCH/STATISTICAL_VALIDATION_H3_H4.md`
- `docs/04_RESEARCH/FEATURE_CATALOG_H1_H9.md`
- `docs/04_RESEARCH/TARGET_SPECIFICATION.md`
- `docs/04_RESEARCH/STATISTICAL_VALIDATION_PLAN.md`

Artefatos de dados relacionados:

- `LateGoalResearch/data/processed/datasets/late_goal_dataset_v1.csv`
- `LateGoalResearch/data/processed/datasets/late_goal_dataset_v1b_ingame.csv`
- `LateGoalResearch/data/processed/features/historical_prematch_features_v1.csv`

---

## Targets de Referencia

### Match-level

- `target_late_goal_75`

Definicao:

- 1 se existe pelo menos um gol apos 75:00 ate o fim da partida.
- 0 caso contrario.

### In-game por cutoff

- `target_goal_after_cutoff`

Definicao:

- 1 se existe gol com minuto maior que `cutoff_minute`.
- 0 caso contrario.

### Direcional por time

- `target_directional_late_goal_75`

Definicao usada em H3/H4:

- linhas `is_home = 1`: `home_late_goal_count_75 > 0`.
- linhas `is_home = 0`: `away_late_goal_count_75 > 0`.

---

## Resumo Executivo

### Features aprovadas para manter

H6 - Estado da partida:

- `score_diff_home_until_cutoff`
- `score_state_group`

H9 - Eventos:

- `cards_until_cutoff`
- `substitutions_until_cutoff`

H3 - Forca ofensiva historica pre-jogo:

- `goals_for_avg_last_3`
- `goals_for_avg_last_10`
- `shots_on_target_for_avg_last_5`

H4 - Fragilidade defensiva historica pre-jogo:

- `shots_against_avg_last_5`
- `shots_on_target_against_avg_last_5`
- `big_chances_against_avg_last_5`

### Features em observacao

H6:

- `total_goals_until_cutoff`
- `time_since_last_goal_until_cutoff`

H9:

- `goal_last_10m_until_cutoff`

H3:

- `goals_for_avg_last_5`
- `shots_for_avg_last_5`
- `big_chances_for_avg_last_5`

H4:

- `goals_against_avg_last_3`
- `goals_against_avg_last_5`
- `goals_against_avg_last_10`

### Features bloqueadas

H1/H2:

- `matches.home_xg`
- `matches.away_xg`
- `team_match_stats.xg` da propria partida
- `team_match_stats.xga` da propria partida
- `forecast_*`
- probabilidades pre-jogo nao comprovadas

H9:

- `red_cards_until_cutoff`
- `yellow_cards_until_cutoff`

Motivo:

- colunas nulas por design no dataset in-game atual, pois a cor do cartao nao foi importada.

### Features descartadas nesta amostra

H6:

- `is_draw_until_cutoff`
- `home_leading_until_cutoff`
- `away_leading_until_cutoff`

H9:

- `goal_last_5m_until_cutoff`

---

# 1. Features Aprovadas / MANTER

## H6 - Estado da Partida

### `score_diff_home_until_cutoff`

Status:

- MANTER.

Fonte:

- `late_goal_dataset_v1b_ingame`.

Momento disponivel:

- Ate o cutoff.

Target:

- `target_goal_after_cutoff`.

Evidencia:

- p-value: 0.00987.
- Cramer's V: 0.083688.
- Efeito maximo: 8.54 p.p.

Decisao:

- A diferenca de placar pela perspectiva do mandante possui associacao estatisticamente significativa com gol futuro apos o cutoff.

### `score_state_group`

Status:

- MANTER.

Fonte:

- derivacao interpretativa no relatorio H6/H9 a partir do estado do placar ate o cutoff.

Momento disponivel:

- Ate o cutoff.

Target:

- `target_goal_after_cutoff`.

Evidencia:

- p-value: 0.003145.
- Cramer's V: 0.096916.
- Efeito maximo: 8.54 p.p.

Decisao:

- Estado composto do placar e mais informativo que flags isoladas de empate/lideranca.

---

## H9 - Eventos

### `cards_until_cutoff`

Status:

- MANTER.

Fonte:

- `late_goal_dataset_v1b_ingame`.

Momento disponivel:

- Ate o cutoff.

Target:

- `target_goal_after_cutoff`.

Evidencia:

- p-value: 0.003972.
- Cramer's V: 0.083765.
- Efeito maximo: 5.90 p.p.

Decisao:

- Quantidade total de cartoes ate o cutoff apresenta sinal estatistico inicial.

### `substitutions_until_cutoff`

Status:

- MANTER.

Fonte:

- `late_goal_dataset_v1b_ingame`.

Momento disponivel:

- Ate o cutoff.

Target:

- `target_goal_after_cutoff`.

Evidencia:

- p-value: 0.
- Cramer's V: 0.14091.
- Efeito maximo: 12.23 p.p.

Decisao:

- Substituicoes acumuladas ate o cutoff apresentaram o sinal mais forte em H9.

---

## H3 - Forca Ofensiva Historica Pre-Jogo

### `goals_for_avg_last_3`

Status:

- MANTER.

Fonte:

- `historical_prematch_features_v1`.

Momento disponivel:

- Pre-jogo, calculado apenas com partidas anteriores.

Target:

- `target_directional_late_goal_75`.

Evidencia:

- N: 740.
- p-value: 0.0421.
- Cramer's V: 0.105.
- Efeito maximo: 6.1 p.p.

Decisao:

- Historico recente de gols marcados tem sinal inicial para gols tardios direcionais.

### `goals_for_avg_last_10`

Status:

- MANTER.

Fonte:

- `historical_prematch_features_v1`.

Momento disponivel:

- Pre-jogo, calculado apenas com partidas anteriores.

Target:

- `target_directional_late_goal_75`.

Evidencia:

- N: 740.
- p-value: 0.0086.
- Cramer's V: 0.126.
- Efeito maximo: 9.3 p.p.

Decisao:

- Janela de 10 jogos para gols a favor apresentou o melhor sinal ofensivo H3.

### `shots_on_target_for_avg_last_5`

Status:

- MANTER.

Fonte:

- `historical_prematch_features_v1`.

Momento disponivel:

- Pre-jogo, calculado apenas com partidas anteriores.

Target:

- `target_directional_late_goal_75`.

Evidencia:

- N: 740.
- p-value: 0.0298.
- Cramer's V: 0.110.
- Efeito maximo: 6.9 p.p.

Decisao:

- Chutes no alvo historicos a favor sao mais promissores do que volume bruto de finalizacoes.

---

## H4 - Fragilidade Defensiva Historica Pre-Jogo

### `shots_against_avg_last_5`

Status:

- MANTER.

Fonte:

- `historical_prematch_features_v1`.

Momento disponivel:

- Pre-jogo, calculado apenas com partidas anteriores.

Target:

- `target_directional_late_goal_75`.

Evidencia:

- N: 740.
- p-value: 0.0334.
- Cramer's V: 0.108.
- Efeito maximo: 7.8 p.p.

Decisao:

- Volume historico de finalizacoes sofridas possui associacao inicial com gol tardio do adversario.

### `shots_on_target_against_avg_last_5`

Status:

- MANTER.

Fonte:

- `historical_prematch_features_v1`.

Momento disponivel:

- Pre-jogo, calculado apenas com partidas anteriores.

Target:

- `target_directional_late_goal_75`.

Evidencia:

- N: 740.
- p-value: 0.0028.
- Cramer's V: 0.138.
- Efeito maximo: 10.8 p.p.

Decisao:

- Melhor feature defensiva historica no ranking atual.

### `big_chances_against_avg_last_5`

Status:

- MANTER.

Fonte:

- `historical_prematch_features_v1`.

Momento disponivel:

- Pre-jogo, calculado apenas com partidas anteriores.

Target:

- `target_directional_late_goal_75`.

Evidencia:

- N: 740.
- p-value: 0.0004.
- Cramer's V: 0.157.
- Efeito maximo: 9.1 p.p.

Decisao:

- Feature defensiva com maior efeito estatistico agregado entre H3/H4.

---

# 2. Features em Observacao

## H6

### `total_goals_until_cutoff`

Status:

- OBSERVAR.

Evidencia:

- p-value: 0.261339.
- Cramer's V: 0.04589.
- Efeito maximo: 3.26 p.p.

Motivo:

- Nao passou como sinal forte, mas possui diferencas de taxa suficientes para monitoramento.

### `time_since_last_goal_until_cutoff`

Status:

- OBSERVAR.

Evidencia:

- p-value: 0.14835.
- Cramer's V: 0.059708.
- Efeito maximo: 4.60 p.p.

Motivo:

- Alguns grupos apresentaram diferenca moderada, mas sem significancia estatistica forte.

---

## H9

### `goal_last_10m_until_cutoff`

Status:

- OBSERVAR.

Evidencia:

- p-value: 0.079035.
- OR: 0.834321.
- Diferenca grupo 1 vs baseline: -3.23 p.p.

Motivo:

- Sinal fraco/moderado, insuficiente para manter como feature principal nesta amostra.

---

## H3

### `goals_for_avg_last_5`

Status:

- OBSERVAR.

Evidencia:

- p-value: 0.1780.
- Cramer's V: 0.082.
- Efeito maximo: 4.5 p.p.

### `shots_for_avg_last_5`

Status:

- OBSERVAR.

Evidencia:

- p-value: 0.4959.
- Cramer's V: 0.057.
- Efeito maximo: 3.5 p.p.

### `big_chances_for_avg_last_5`

Status:

- OBSERVAR.

Evidencia:

- p-value: 0.2660.
- Cramer's V: 0.073.
- Efeito maximo: 4.9 p.p.

---

## H4

### `goals_against_avg_last_3`

Status:

- OBSERVAR.

Evidencia:

- p-value: 0.2209.
- Cramer's V: 0.077.
- Efeito maximo: 7.1 p.p.

### `goals_against_avg_last_5`

Status:

- OBSERVAR.

Evidencia:

- p-value: 0.0821.
- Cramer's V: 0.095.
- Efeito maximo: 7.7 p.p.

### `goals_against_avg_last_10`

Status:

- OBSERVAR.

Evidencia:

- p-value: 0.0944.
- Cramer's V: 0.093.
- Efeito maximo: 6.4 p.p.

---

# 3. Features Bloqueadas

## H1/H2 - xG, xGA, forecast e probabilidades pre-jogo

### `matches.home_xg`

Status:

- BLOQUEADA.

Motivo:

- xG final da propria partida.

### `matches.away_xg`

Status:

- BLOQUEADA.

Motivo:

- xG final da propria partida.

### `team_match_stats.xg`

Status:

- BLOQUEADA quando se refere a propria partida.

Motivo:

- estatistica final por time por partida.

### `team_match_stats.xga`

Status:

- BLOQUEADA quando se refere a propria partida.

Motivo:

- estatistica final por time por partida.

### `forecast_*`

Status:

- BLOQUEADA.

Motivo:

- importado junto do registro final Understat e nao comprovado como pre-kickoff.

### Probabilidades pre-jogo externas

Status:

- BLOQUEADA / NAO DISPONIVEL.

Motivo:

- nenhuma fonte segura versionada/importada foi encontrada.

---

## H9 - Cartoes por cor

### `red_cards_until_cutoff`

Status:

- BLOQUEADA nesta etapa.

Motivo:

- coluna nula por design no Dataset V1B; cor do cartao nao disponivel na importacao atual.

### `yellow_cards_until_cutoff`

Status:

- BLOQUEADA nesta etapa.

Motivo:

- coluna nula por design no Dataset V1B; cor do cartao nao disponivel na importacao atual.

---

# 4. Features Descartadas nesta Amostra

## H6

### `is_draw_until_cutoff`

Status:

- DESCARTAR nesta amostra.

Evidencia:

- p-value: 0.205801.
- OR: 0.87145.
- Diferenca grupo 1 vs baseline: -2.50 p.p.

Motivo:

- flag isolada de empate perdeu informacao frente ao estado composto do placar.

### `home_leading_until_cutoff`

Status:

- DESCARTAR nesta amostra.

Evidencia:

- p-value: 0.110669.
- OR: 1.162576.
- Diferenca grupo 1 vs baseline: 2.15 p.p.

### `away_leading_until_cutoff`

Status:

- DESCARTAR nesta amostra.

Evidencia:

- p-value: 0.655687.
- OR: 0.955095.
- Diferenca grupo 1 vs baseline: -0.76 p.p.

---

## H9

### `goal_last_5m_until_cutoff`

Status:

- DESCARTAR nesta amostra.

Evidencia:

- p-value: 0.399569.
- OR: 0.893517.
- Diferenca grupo 1 vs baseline: -2.35 p.p.

Motivo:

- sem evidencia suficiente de associacao nesta amostra.

---

# 5. Ranking Preliminar das Features Mantidas

| Rank | Hipotese | Feature | Tipo | Evidencia principal |
|---:|---|---|---|---|
| 1 | H4 | `shots_on_target_against_avg_last_5` | pre-jogo historica | p=0.0028; efeito max 10.8 p.p. |
| 2 | H3 | `goals_for_avg_last_10` | pre-jogo historica | p=0.0086; efeito max 9.3 p.p. |
| 3 | H4 | `big_chances_against_avg_last_5` | pre-jogo historica | p=0.0004; efeito max 9.1 p.p. |
| 4 | H4 | `shots_against_avg_last_5` | pre-jogo historica | p=0.0334; efeito max 7.8 p.p. |
| 5 | H3 | `shots_on_target_for_avg_last_5` | pre-jogo historica | p=0.0298; efeito max 6.9 p.p. |
| 6 | H3 | `goals_for_avg_last_3` | pre-jogo historica | p=0.0421; efeito max 6.1 p.p. |
| 7 | H9 | `substitutions_until_cutoff` | in-game | p=0; efeito max 12.23 p.p. |
| 8 | H6 | `score_state_group` | in-game | p=0.003145; efeito max 8.54 p.p. |
| 9 | H6 | `score_diff_home_until_cutoff` | in-game | p=0.00987; efeito max 8.54 p.p. |
| 10 | H9 | `cards_until_cutoff` | in-game | p=0.003972; efeito max 5.90 p.p. |

Observacao:

- O ranking mistura features pre-jogo e in-game apenas como consolidacao de evidencias. Em qualquer baseline futuro, os blocos devem ser avaliados separadamente para evitar comparacao indevida entre momentos de disponibilidade diferentes.

---

# 6. Regras de Uso na Proxima Etapa

## Permitidas para bloco pre-jogo

- `goals_for_avg_last_3`
- `goals_for_avg_last_10`
- `shots_on_target_for_avg_last_5`
- `shots_against_avg_last_5`
- `shots_on_target_against_avg_last_5`
- `big_chances_against_avg_last_5`

## Permitidas para bloco in-game

- `score_diff_home_until_cutoff`
- `score_state_group`
- `cards_until_cutoff`
- `substitutions_until_cutoff`

## Somente observacao / monitoramento

- `total_goals_until_cutoff`
- `time_since_last_goal_until_cutoff`
- `goal_last_10m_until_cutoff`
- `goals_for_avg_last_5`
- `shots_for_avg_last_5`
- `big_chances_for_avg_last_5`
- `goals_against_avg_last_3`
- `goals_against_avg_last_5`
- `goals_against_avg_last_10`

## Proibidas

- targets e aliases de target como features;
- placar final como feature preditiva;
- estatisticas full-match da propria partida como feature in-game;
- xG/xGA da propria partida;
- forecast sem comprovacao pre-kickoff;
- eventos apos cutoff;
- qualquer media historica que use jogos futuros.

---

# 7. Conclusoes por Hipotese

## H1 - xG Pre-Jogo

Status:

- BLOQUEADA.

Motivo:

- nao existe xG pre-jogo seguro nos artefatos atuais.

## H2 - Forecast Pre-Jogo

Status:

- BLOQUEADA.

Motivo:

- forecast atual e ambiguo e nao comprovado como pre-kickoff.

## H3 - Forca Ofensiva

Status:

- MANTER COMO CANDIDATA.

Conclusao:

- ha evidencias iniciais para features historicas de gols marcados e chutes no alvo.

## H4 - Fragilidade Defensiva

Status:

- MANTER COMO CANDIDATA FORTE.

Conclusao:

- ha evidencias fortes para features historicas defensivas baseadas em chutes sofridos, chutes no alvo sofridos e big chances sofridas.

## H5 - Pressao Ofensiva In-Game

Status:

- NAO VALIDADA.

Motivo:

- depende de estatisticas temporais ou snapshots confiaveis; nao usar `match_statistics` full-match como preditor in-game.

## H6 - Estado da Partida

Status:

- VALIDADA INICIALMENTE.

Conclusao:

- estado composto do placar e diferenca de placar devem permanecer no conjunto candidato.

## H7 - Combinacao Multi-Fonte

Status:

- NAO VALIDADA COMO HIPOTESE INDEPENDENTE.

Conclusao:

- agora existem blocos candidatos pre-jogo e in-game, mas a combinacao ainda nao foi avaliada formalmente.

## H8 - Momentum e Pressao Temporal

Status:

- BLOQUEADA / PENDENTE.

Motivo:

- `match_graph` ainda nao esta populada.

## H9 - Eventos

Status:

- VALIDADA INICIALMENTE.

Conclusao:

- cartoes totais e substituicoes ate cutoff devem permanecer no conjunto candidato.

---

# 8. Recomendacoes para Proxima Etapa

1. Submeter este conjunto candidato ao PM para aprovacao.
2. Separar explicitamente dois blocos futuros:
   - bloco pre-jogo;
   - bloco in-game.
3. Nao iniciar modelo complexo ainda.
4. Antes de baseline, definir qual baseline sera permitido:
   - baseline pre-jogo;
   - baseline in-game por cutoff;
   - ou baseline combinado controlado.
5. Manter H1/H2 bloqueadas ate existir fonte pre-kickoff segura.
6. Manter H8 bloqueada ate `match_graph` ser coletada/importada.
7. Nao usar features observadas como principais sem nova rodada de validacao ou criterio aprovado pelo PM/Quant.

---

## Decisao Quant Atual

O Feature Candidate Set V1 esta pronto para revisao do PM.

Conjunto minimo recomendado para proxima etapa exploratoria:

Pre-jogo:

- `goals_for_avg_last_3`
- `goals_for_avg_last_10`
- `shots_on_target_for_avg_last_5`
- `shots_against_avg_last_5`
- `shots_on_target_against_avg_last_5`
- `big_chances_against_avg_last_5`

In-game:

- `score_diff_home_until_cutoff`
- `score_state_group`
- `cards_until_cutoff`
- `substitutions_until_cutoff`

Nenhuma modelagem deve ser iniciada antes de aprovacao do PM.
