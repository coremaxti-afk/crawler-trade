# SPORTMONKS

## Status

SportMonks esta classificada como **fonte primaria candidata para H8 em escala**, com base na auditoria da Premier League 2025/26.

Documento principal:

- `SPORTMONKS_EPL_2025_26_VALIDATION_AND_SOFASCORE_COMPARISON.md`

Matriz:

- `data/processed/reports/sportmonks_epl_2025_26_endpoint_quality_matrix.csv`

## Evidencia atual

Coleta auditada:

- League: Premier League (`8`)
- Season: 2025/26 (`25583`)
- Fixtures esperadas: 380
- Cobertura: 380 JSONs validos em cada categoria coletada
- Categorias: `base`, `identity`, `match_state`, `timeline`, `statistics`, `commentaries`, `trends`, `xgfixture`

## Valor para H8

### Core

- `trends`: pressao por minuto/time, incluindo ataques, dangerous attacks, posse, chutes, escanteios, passes e big chances.
- `timeline`: eventos objetivos por minuto, incluindo chutes, corners, offside e woodwork.
- `match_state`: eventos de jogo, placar, gols, cartoes, substituicoes, scores/periods.
- `base/identity`: chaves de join, teams/participants, liga, temporada, estado do fixture.

### Seletivo

- `xgfixture`: xG agregado por fixture/time; nao e temporal nem shot-level.
- `statistics`: agregados finais; risco alto de leakage para cutoffs.
- `commentaries`: texto/narrativa minuto a minuto; util para auditoria, mas exige parsing textual.

### Fora do core H8

- `matchfacts`
- `lineups`
- `predictions`
- `odds/premiumOdds`

## Comparacao com SofaScore

SportMonks substitui parcialmente SofaScore para pressao quantitativa por minuto/time.

SportMonks nao substitui totalmente:

- SofaScore `graph`: momentum proprietario minuto a minuto.
- SofaScore `shotmap`: shot-level com coordenadas, xG, xGOT e timeSeconds.

Decisao preliminar:

- SportMonks = fonte primaria para escala H8.
- SofaScore = fonte especializada/backup para `graph`, `shotmap` e QA.

## Proxima validacao obrigatoria

Antes de feature engineering:

- validar semanticamente `trends`;
- identificar se cada tipo e acumulado, incremental ou snapshot por minuto;
- definir regra segura para cutoffs 60/65/70/75;
- bloquear `statistics` e `xgfixture` como features de cutoff sem snapshot temporal.
