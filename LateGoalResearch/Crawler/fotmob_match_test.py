import requests
from sqlalchemy import create_engine, text
from datetime import datetime

# ==========================
# CONFIGURAÇÃO DO BANCO
# ==========================

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
# BAIXAR JOGOS FOTMOB
# ==========================

url = "https://www.fotmob.com/api/data/leagues?id=47&season=2024/2025"

print("Baixando jogos FotMob...")

data = requests.get(url).json()

fotmob_matches = data["overview"]["leagueOverviewMatches"]

print(f"Jogos FotMob encontrados: {len(fotmob_matches)}")

# ==========================
# LER 10 JOGOS UNDERSTAT
# ==========================

sql = """
SELECT
    understat_match_id,
    match_date,
    home_team,
    away_team
FROM matches
ORDER BY match_date
LIMIT 10
"""

with engine.connect() as conn:
    rows = conn.execute(text(sql)).fetchall()

# ==========================
# MATCHING
# ==========================

found = 0

for row in rows:

    understat_date = row.match_date.strftime("%Y-%m-%d %H:%M")
    understat_home = normalize(row.home_team)
    understat_away = normalize(row.away_team)

    match_found = False

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
            print("=" * 60)
            print(f"UNDERSTAT : {row.home_team} x {row.away_team}")
            print(f"FOTMOB    : {fm['home']['name']} x {fm['away']['name']}")
            print(f"MATCH ID  : {fm['id']}")

            found += 1
            match_found = True
            break

    if not match_found:
        print("=" * 60)
        print(f"NÃO ENCONTRADO: {row.home_team} x {row.away_team}")

print("\nRESULTADO")
print(f"Encontrados: {found}")
print(f"Não encontrados: {len(rows) - found}")
