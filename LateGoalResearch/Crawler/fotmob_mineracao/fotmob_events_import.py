import json
from sqlalchemy import create_engine, text

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
# CONFIGURAÇÃO
# ==========================

MATCH_ID_DB = 1

# ==========================
# CARREGA JSON
# ==========================

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

shots = data["content"]["shotmap"]["shots"]

# ==========================
# IMPORTAÇÃO
# ==========================

total = 0

with engine.begin() as conn:

    for shot in shots:

        conn.execute(
            text("""
                INSERT INTO events_v2 (
                    match_id,
                    minute,
                    minute_added,
                    event_type,
                    team_id,
                    player_name,
                    xg,
                    is_on_target,
                    shot_type,
                    situation
                )
                VALUES (
                    :match_id,
                    :minute,
                    :minute_added,
                    :event_type,
                    :team_id,
                    :player_name,
                    :xg,
                    :is_on_target,
                    :shot_type,
                    :situation
                )
            """),
            {
                "match_id": MATCH_ID_DB,
                "minute": shot.get("min"),
                "minute_added": shot.get("minAdded"),
                "event_type": shot.get("eventType"),
                "team_id": shot.get("teamId"),
                "player_name": shot.get("playerName"),
                "xg": shot.get("expectedGoals"),
                "is_on_target": shot.get("isOnTarget"),
                "shot_type": shot.get("shotType"),
                "situation": shot.get("situation")
            }
        )

        total += 1

print(f"Eventos importados: {total}")
