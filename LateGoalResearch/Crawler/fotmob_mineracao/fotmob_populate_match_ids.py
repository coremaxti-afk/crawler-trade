import requests
from sqlalchemy import create_engine, text
from datetime import datetime

# ==========================
# CONFIGURAÇÃO
# ==========================

DRY_RUN = False

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

response = requests.get(url, timeout=30)
response.raise_for_status()

data = response.json()

fotmob_matches = data["overview"]["leagueOverviewMatches"]

print(f"Fixtures FotMob: {len(fotmob_matches)}")


# ==========================
# LER MATCHES UNDERSTAT
# ==========================

with engine.connect() as conn:

    rows = conn.execute(
        text("""
            SELECT
                id,
                understat_match_id,
                match_date,
                home_team,
                away_team
            FROM matches
            WHERE fotmob_match_id IS NULL
            ORDER BY match_date
        """)
    ).fetchall()

print(f"Matches Understat: {len(rows)}")


# ==========================
# MATCHING
# ==========================

updates = []
not_found = []

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

            updates.append(
                (
                    int(fm["id"]),
                    row.id,
                    row.understat_match_id,
                    row.home_team,
                    row.away_team
                )
            )

            match_found = True
            break

    if not match_found:

        not_found.append(
            (
                row.understat_match_id,
                row.match_date,
                row.home_team,
                row.away_team
            )
        )


# ==========================
# RESULTADOS
# ==========================

print()
print("=" * 60)
print("RESULTADO")
print("=" * 60)

print(f"Encontrados: {len(updates)}")
print(f"Não encontrados: {len(not_found)}")

print()
print("PRIMEIROS 10 MATCHES ENCONTRADOS")
print("-" * 60)

for item in updates[:10]:

    fotmob_id, match_id, understat_id, home, away = item

    print(
        f"match_id={match_id} | "
        f"understat_id={understat_id} | "
        f"fotmob_id={fotmob_id} | "
        f"{home} x {away}"
    )

print()

if not_found:

    print("=" * 60)
    print("MATCHES NÃO ENCONTRADOS")
    print("=" * 60)

    for item in not_found:

        understat_id, match_date, home, away = item

        print(
            f"{understat_id} | "
            f"{match_date} | "
            f"{home} x {away}"
        )

else:

    print("Todos os jogos foram encontrados.")


# ==========================
# UPDATE
# ==========================

if DRY_RUN:

    print()
    print("=" * 60)
    print("DRY RUN")
    print("=" * 60)
    print("Nenhuma alteração foi feita no banco.")

else:

    with engine.begin() as conn:

        for fotmob_id, match_id, _, _, _ in updates:

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

    print()
    print("=" * 60)
    print("BANCO ATUALIZADO")
    print("=" * 60)
    print(f"Registros atualizados: {len(updates)}")
