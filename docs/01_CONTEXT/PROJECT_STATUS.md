# PROJECT STATUS

## Estado Atual da Base

- Inventory SofaScore EPL: 381 partidas.
- Partidas importaveis: 380.
- Partida descartada da importacao atual: `12436452`.
- `matches_master`: 380 partidas.
- `match_statistics`: 380 partidas.
- `match_incidents`: 7647 registros.
- `match_graph`: 34861 pontos em 379 partidas.
- `match_shotmap`: 9883 finalizacoes em 380 partidas.
- `match_source_status`: 760 registros.
- Football-Data: 380 staging rows, 380 mappings e 34280 odds importadas localmente.
- Odds Features V1: 380 linhas, 380 partidas unicas, status APTO.
- Dataset Odds V1: 380 linhas, 380 partidas unicas, target unido explicitamente, status APTO COM RESSALVAS.
- H8 Composite Pressure Score V1: 1520 linhas match_id + cutoff, 5040 resultados disponiveis, status exploratorio concluido.

---

## SportMonks H8

Documento principal:

- `docs/03_SOURCES/SPORTMONKS/SPORTMONKS_EPL_2025_26_VALIDATION_AND_SOFASCORE_COMPARISON.md`

Matriz:

- `data/processed/reports/sportmonks_epl_2025_26_endpoint_quality_matrix.csv`

Estado:

- Premier League 2025/26 auditada.
- 380 fixtures esperadas.
- 380 JSONs validos em cada uma das 8 categorias coletadas.
- Categorias auditadas: `base`, `identity`, `match_state`, `timeline`, `statistics`, `commentaries`, `trends`, `xgfixture`.
- `trends`: 109.087 MB total, 293.96 KB medio por fixture, granularidade minuto/time.
- `timeline`: 8.409 MB total, 22.66 KB medio por fixture, eventos objetivos por minuto.
- `xgfixture`: agregado por fixture/time; nao e xG temporal nem shot-level.

Decisao Data Acquisition:

- SportMonks e fonte primaria candidata para H8 em escala.
- SportMonks substitui parcialmente SofaScore para pressao quantitativa por minuto/time.
- SofaScore permanece necessario como fonte especializada/backup para `graph` e `shotmap`.

Coleta recomendada:

- Coletar sempre: `trends`, `timeline`, `match_state`, `base/identity` minimo para join.
- Coletar seletivo: `xgfixture`, `statistics`, `commentaries`.
- Nao priorizar para H8 cutoff core: `matchfacts`, `lineups`, `odds/premiumOdds`, `predictions`.

Pendencia antes de feature engineering:

- Validar semanticamente `trends` para identificar se cada tipo representa valor acumulado, incremental ou snapshot por minuto.
- Confirmar regra segura para cutoffs 60/65/70/75.

---

## Operacional Trade Research

Documento:

- docs/04_RESEARCH/OPERACIONAL_TRADE_TOP_STRATEGIES_V1.md

Principais achados:

LAY OVER (mais forte)
- favorite_winning_by_1 + h8_cold_combo_10m_2of3
- favorite_winning_by_1 + h8_pressure_score_10m_bottom25

BACK OVER
- home_winning_by_1 + h8_pressure_score_10m_top25
- home_winning_by_1 + h8_shot_quality_top25

Conclusao:

- Estrategias LAY OVER em jogo frio apresentaram maior robustez.
- Estrategias BACK OVER funcionam melhor com protocolo dinamico.

Status:

- Pesquisa exploratoria.
- Nao autoriza producao.
- Nao autoriza robo.
- Nao autoriza trade real.
- Nao autoriza backtesting financeiro real.

---

(Restante do documento mantido)
