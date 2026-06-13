# SOURCES

Esta pasta centraliza toda a documentação de descoberta e engenharia reversa das fontes de dados.

## Fontes

- UNDERSTAT
- FOTMOB
- SOFASCORE
- SPORTMONKS
- FOOTBALL-DATA
- API-FOOTBALL
- ODDS

Cada fonte deve conter:

- endpoints descobertos
- exemplos de payload
- limitações
- mapeamentos
- estratégia de coleta
- roadmap de exploração

---

## Estado operacional das fontes

### SportMonks

Status atual: **fonte primária candidata para H8 em escala**.

Evidência mais recente:

- `docs/03_SOURCES/SPORTMONKS/SPORTMONKS_EPL_2025_26_VALIDATION_AND_SOFASCORE_COMPARISON.md`
- `data/processed/reports/sportmonks_epl_2025_26_endpoint_quality_matrix.csv`

Resumo:

- EPL 2025/26 auditada com 380 fixtures esperadas.
- 380 JSONs válidos nas 8 categorias coletadas.
- `trends` é o principal endpoint H8 por minuto/time.
- SportMonks substitui parcialmente SofaScore para pressão quantitativa por minuto.
- SportMonks não substitui totalmente SofaScore `graph` nem `shotmap`.

Decisão preliminar:

- Coletar sempre: `trends`, `timeline`, `match_state`, `base/identity` mínimo para join.
- Coletar seletivamente: `xgfixture`, `statistics`, `commentaries`.
- Não priorizar para H8 cutoff core: `matchfacts`, `lineups`, `odds/premiumOdds`, `predictions`.

Próxima validação necessária:

- Validar semanticamente `trends` para confirmar se os valores são acumulados, incrementais ou snapshot por minuto antes de criar features H8.

### SofaScore

Status atual: **fonte especializada/backup para H8**.

Mantém valor alto em:

- `graph`: momentum proprietário por minuto.
- `shotmap`: shot-level com coordenadas, minuto/timeSeconds, xG e xGOT.
- `incidents`: eventos de partida para validação.

Decisão preliminar:

- Não usar SofaScore como dependência primária para coleta massiva se SportMonks cobrir a liga/temporada.
- Manter SofaScore para benchmark, QA e features especializadas de momentum/shot quality.

### Football-Data

Status atual: **fonte consolidada para odds pré-jogo/closing EPL 2024/25**.

Uso principal:

- odds pre-match/closing;
- mapeamento com SofaScore;
- contexto de mercado histórico não-live.

### API-Football

Status atual: **fonte complementar a auditar**.

Uso potencial:

- base/fixtures;
- events;
- odds se entregar mercado histórico útil;
- cobertura alternativa quando SportMonks/SofaScore falharem.

Não deve substituir SportMonks `trends` sem evidência de pressão minuto a minuto equivalente.
