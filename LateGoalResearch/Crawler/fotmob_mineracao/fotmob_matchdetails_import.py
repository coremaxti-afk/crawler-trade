import json
import time
import requests

from sqlalchemy import create_engine, text

# ==========================
# CONFIGURAÇÃO
# ==========================

DB_USER = "postgres"
DB_PASSWORD = "92601050"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "late_goal_research"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

LIMIT = 5

# ==========================
# BUSCAR MATCHES
# ==========================

with engine.connect() as conn:

    matches = conn.execute(
        text("""
            SELECT fotmob_match_id
            FROM matches
            WHERE fotmob_match_id IS NOT NULL
            ORDER BY match_date
            LIMIT :limit
        """),
        {"limit": LIMIT}
    ).fetchall()

print(f"Partidas encontradas: {len(matches)}")

# ==========================
# IMPORTAÇÃO
# ==========================

inserted = 0

with engine.begin() as conn:

    for row in matches:

        fotmob_match_id = row.fotmob_match_id

        url = (
            f"https://www.fotmob.com/api/data/"
            f"matchDetails?matchId={fotmob_match_id}"
        )

        print(f"Baixando {fotmob_match_id}...")

        headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.fotmob.com/",
    "Accept": "application/json"
}

response = requests.get(
    url,
    headers=headers,
    timeout=30
)
        response.raise_for_status()

        data = response.json()

        conn.execute(
            text("""
                INSERT INTO fotmob_raw_matches
                (
                    fotmob_match_id,
                    json_data
                )
                VALUES
                (
                    :fotmob_match_id,
                    CAST(:json_data AS JSONB)
                )
                ON CONFLICT (fotmob_match_id)
                DO NOTHING
            """),
            {
                "fotmob_match_id": fotmob_match_id,
                "json_data": json.dumps(data)
            }
        )

        inserted += 1

        time.sleep(1)

print()
print(f"Importados: {inserted}")
