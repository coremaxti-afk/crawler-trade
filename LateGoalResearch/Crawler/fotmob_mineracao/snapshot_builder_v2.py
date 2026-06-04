import json
from sqlalchemy import create_engine, text

# ==========================
# CONFIGURAÇÃO BANCO
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
# CONFIGURAÇÃO PARTIDA
# ==========================

MATCH_ID = 1

HOME_TEAM_ID = 10274
AWAY_TEAM_ID = 1757

# ==========================
# CARREGA EVENTOS
# ==========================

with engine.connect() as conn:

    eventos = conn.execute(
        text("""
            SELECT
                minute,
                minute_added,
                event_type,
                team_id,
                xg,
                is_on_target
            FROM events_v2
            WHERE match_id = :match_id
            ORDER BY minute, minute_added
        """),
        {"match_id": MATCH_ID}
    ).fetchall()

# ==========================
# CARREGA MOMENTUM
# ==========================

with open("matchdetails.json", "r", encoding="utf-8") as f:
    data = json.load(f)

momentum_raw = data["content"]["momentum"]["main"]["data"]

momentum_por_minuto = {}

for item in momentum_raw:

    minuto = int(item["minute"])

    if 1 <= minuto <= 90:
        momentum_por_minuto[minuto] = item["value"]

# ==========================
# SNAPSHOTS
# ==========================

home_score = 0
away_score = 0

home_shots = 0
away_shots = 0

home_sot = 0
away_sot = 0

home_xg = 0
away_xg = 0

idx = 0

with engine.begin() as conn:

    for minuto in range(1, 91):

        while (
            idx < len(eventos)
            and eventos[idx].minute <= minuto
        ):

            e = eventos[idx]

            if e.team_id == HOME_TEAM_ID:

                home_shots += 1
                home_xg += float(e.xg or 0)

                if e.is_on_target:
                    home_sot += 1

                if e.event_type == "Goal":
                    home_score += 1

            elif e.team_id == AWAY_TEAM_ID:

                away_shots += 1
                away_xg += float(e.xg or 0)

                if e.is_on_target:
                    away_sot += 1

                if e.event_type == "Goal":
                    away_score += 1

            idx += 1

        momentum = momentum_por_minuto.get(minuto, 0)

        conn.execute(
            text("""
                INSERT INTO snapshots (
                    match_id,
                    minute,

                    home_score,
                    away_score,

                    home_xg,
                    away_xg,

                    home_shots,
                    away_shots,

                    home_sot,
                    away_sot,

                    momentum
                )
                VALUES (
                    :match_id,
                    :minute,

                    :home_score,
                    :away_score,

                    :home_xg,
                    :away_xg,

                    :home_shots,
                    :away_shots,

                    :home_sot,
                    :away_sot,

                    :momentum
                )
            """),
            {
                "match_id": MATCH_ID,
                "minute": minuto,

                "home_score": home_score,
                "away_score": away_score,

                "home_xg": round(home_xg, 4),
                "away_xg": round(away_xg, 4),

                "home_shots": home_shots,
                "away_shots": away_shots,

                "home_sot": home_sot,
                "away_sot": away_sot,

                "momentum": momentum
            }
        )

print("Snapshots gravados com sucesso.")
