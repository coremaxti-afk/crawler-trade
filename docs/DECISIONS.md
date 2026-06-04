# DECISIONS LOG

## DECISION-001
Salvar snapshots minuto a minuto.

Motivo:
Evitar perda de informação para futuras pesquisas.

## DECISION-002
Incluir acréscimos (45+ e 90+).

Motivo:
Grande parte dos gols tardios ocorre nos acréscimos.

## DECISION-003
Utilizar Understat + FotMob.

Motivo:
Combinar métricas pré-jogo e intra-jogo.

## DECISION: FotMob Match Mapping Considered Solved

Date: 2026-06-02

### Context

The project required a reliable relationship between Understat matches and FotMob matches.

Initial attempts relied on old FotMob endpoints and local cache files. Multiple approaches were evaluated.

### Investigation

The following sources were tested:

* FotMob historical cache files
* FotMob league endpoints
* worldfootballR cache datasets
* Direct API access
* Playwright browser interception

### Outcome

The endpoint:

https://www.fotmob.com/api/data/leagues?id=47&season=2024/2025

provides season fixtures containing:

* match id
* home team
* away team
* match date

This was sufficient to map Understat matches to FotMob IDs.

### Result

369 matches were successfully mapped and stored in matches.fotmob_match_id.

### Decision

The Understat → FotMob Match ID problem is considered solved.

Future work should not revisit mapping logic unless a new league requires special handling.

---

## DECISION: Do Not Block Project on FotMob MatchDetails

Date: 2026-06-02

### Context

The project attempted to collect:

* momentum
* events
* player stats
* attacking zones
* shot maps

from the FotMob matchDetails endpoint.

### Findings

Endpoint:

https://www.fotmob.com/api/data/matchDetails

returns:

403 TURNSTILE_REQUIRED

for direct requests.

Playwright interception currently reproduces the URL discovery but not payload retrieval.

A historical matchdetails.json exists and proves that payload capture was successful at least once.

### Decision

MatchDetails investigation remains open.

However:

* project progress must continue
* database expansion must continue
* model development must continue

## DECISION: Adopt Multi-Source Data Strategy

Date: 2026-06-02

### Context

The project originally planned to enrich Understat data primarily through FotMob.

Recent restrictions affecting the MatchDetails endpoint increased provider risk.

### Decision

The project will adopt a multi-source architecture.

Candidate providers:

- SofaScore
- AiScore
- StatsBomb
- Flashscore
- FBref

FotMob remains a supported provider but is no longer considered a mandatory dependency.

### Expected Benefits

- Reduced provider risk
- Better historical coverage
- Easier future expansion

MatchDetails is classified as a parallel research topic rather than a blocking dependency.

