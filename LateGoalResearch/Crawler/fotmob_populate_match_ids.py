```python
import requests
from sqlalchemy import create_engine, text
from datetime import datetime

# ==========================
# CONFIGURAÇÃO
# ==========================

DRY_RUN = True

DB_USER = "postgres"
DB_PASSWORD = "92601050"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "late_goal_research"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================
# ALIASES
# ==========================

ALIASES = {
    "man united": "manchester united",
    "man city": "manchester city",
    "newcastle": "newcastle united",
    "wolves": "wolverhampton wanderers",
    "brighton": "brighton and hove albion",
    "bournemouth": "afc bournemouth",
    "tottenham": "tottenham hotspur",
    "west ham": "west ham united",
    "leicester": "leicester city",
    "ipswich": "ipswich town",
    "nottm forest": "nottingham forest"
}

def normalize(name):
    name = name.lower().strip()
    return ALIASES.get(name, name)

# ==========================
# BAIXAR DADOS FOTMOB
# ==========================

print("Baixando fixtures FotMob...")

url = "https://www.fotmob.com/api/data/leagues?id=47&season=2024/2025"
data = requests.get(url).json()

fotmob_matches = data["overview"]["leagueOverviewMatches"]

print(f"Fixtures FotMob: {len(fotmob_matches)}")

# ==========================
# LER MATCHES UNDERSTAT
# ==========================

with engine.connect() as conn:
    rows = conn.execute(text("""
        SELECT
            id,
            understat_match_id,
            match_date,
            home_team,
            away_team
        FROM matches
        WHERE fotmob_match_id IS NULL
        ORDER BY match_date
    """)).fetchall()

print(f"Matches Understat: {len(rows)}")

# ==========================
# MATCHING
# ==========================

updates = []

for row in rows:

    understat_date = row.match_date.strftime("%Y-%m-%d %H:%M")
    understat_home = normalize(row.home_team)
    understat_away = normalize(row.away_team)

    for fm in fotmob_matches:

        fm_date = datetime.fromisoformat(
            fm["status"]["utcTime"].replace("Z", "+00:00")
        ).strftime("%Y-%m-%d %H:%M")

        fm_home = normalize(fm["home"]["name"])
        fm_away = normalize(fm["away"]["name"])

        if (
            understat_date == fm_date
            and understat_home == fm_home
            and understat_away == fm_away
        ):
            updates.append(
                (
                    int(fm["id"]),
                    row.id,
                    row.home_team,
                    row.away_team
                )
            )
            break

print(f"\nEncontrados: {len(updates)}")
print(f"Não encontrados: {len(rows) - len(updates)}")

print("\nPrimeiros 10 matches encontrados:\n")

for item in updates[:10]:
    fotmob_id, match_id, home, away = item

    print(
        f"match_id={match_id} | "
        f"fotmob_id={fotmob_id} | "
        f"{home} x {away}"
    )

# ==========================
# UPDATE (DESATIVADO)
# ==========================

if DRY_RUN:
    print("\nDRY_RUN=True")
    print("Nenhuma alteração foi feita no banco.")
else:

    with engine.begin() as conn:

        for fotmob_id, match_id, _, _ in updates:

            conn.execute(
                text("""
                    UPDATE matches
                    SET fotmob_match_id = :fotmob_id
                    WHERE id = :match_id
                """),
                {
                    "fotmob_id": fotmob_id,
                    "match_id": match_id
                }
            )

    print(f"\nAtualizados: {len(updates)}")
```
