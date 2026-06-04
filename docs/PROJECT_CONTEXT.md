# PROJECT STATUS UPDATE – JUNE 2026

## Current Objective

The project aims to build a quantitative research platform focused on identifying patterns associated with late goals in football matches.

The long-term objective is to create predictive models capable of identifying situations with increased probability of goals during the final stages of a match.

---

## Current Data Architecture

### Primary Historical Source

Understat

Available:

* historical matches
* xG
* xGA
* results
* team statistics
* player statistics

---

### Database

PostgreSQL

Main table:

```text
matches
```

Relevant fields:

```text
understat_match_id
league
season
match_date
home_team
away_team
home_goals
away_goals
home_xg
away_xg
fotmob_match_id
```

---

## FotMob Integration

### Objective

Enrich Understat matches with:

* snapshots
* momentum
* events
* player statistics
* attacking metrics

---

### Major Achievement

The project successfully solved:

```text
Understat Match
↓
FotMob Match ID
```

using:

```text
https://www.fotmob.com/api/data/leagues?id=47&season=2024/2025
```

Result:

```text
369 matches mapped successfully.
```

This problem is considered solved.

---

## MatchDetails Investigation

### Endpoint

```text
https://www.fotmob.com/api/data/matchDetails
```

### Intended Data

* momentum
* events
* attacking zones
* playerStats
* shotmap
* expectedGoals
* matchFacts

---

### Current Status

Blocked.

Current response:

```text
403
TURNSTILE_REQUIRED
```

Attempts performed:

* requests
* custom headers
* x-mas header
* Playwright
* network interception
* browser automation

No reproducible solution currently exists.

---

### Important Evidence

A historical file:

```text
matchdetails.json
```

exists and contains valid MatchDetails payload.

This proves that payload capture was successful at least once.

The reproduction method remains unknown.

---

## Project Decision

The project must not depend exclusively on FotMob.

MatchDetails investigation remains active but is no longer considered a blocking dependency.

Development must continue using currently available data.

---

## New Research Direction

The project is moving toward a multi-source architecture.

Potential sources:

* Understat
* SofaScore
* Flashscore
* FBref
* StatsBomb Open Data
* SoccerNet
* AiScore
* Odds providers

Objective:

Reduce dependency on any single provider.

---

## Current Priorities

### Priority 1

Expand historical database:

* EPL 2021/2022
* EPL 2022/2023
* EPL 2023/2024
* EPL 2025/2026

---

### Priority 2

Expand coverage:

* La Liga
* Bundesliga
* Serie A
* Ligue 1
* Brasileirão

---

### Priority 3

Research alternative snapshot providers.

Primary candidates:

1. SofaScore
2. StatsBomb Open Data
3. Flashscore

---

### Priority 4

Build first quantitative late-goal model using currently available data.

The model should not wait for MatchDetails resolution.

---

## Current Assessment

Project Status:

```text
Database Infrastructure ..... COMPLETE
Understat Integration ....... COMPLETE
FotMob Match Mapping ........ COMPLETE
FotMob MatchDetails ......... BLOCKED
Historical Expansion ........ IN PROGRESS
Alternative Sources ......... RESEARCH PHASE
Model Development ........... NEXT MAJOR STEP
```

The project should continue progressing while MatchDetails research remains a parallel investigation.
