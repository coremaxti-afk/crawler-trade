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
# SNAPSHOTS
# ==========================

home_goals = 0
away_goals = 0

home_shots = 0
away_shots = 0

home_sot = 0
away_sot = 0

home_xg = 0
away_xg = 0

idx = 0

for minuto in range(1, 91):

    while idx < len(eventos) and eventos[idx].minute <= minuto:

        e = eventos[idx]

        if e.team_id == HOME_TEAM_ID:

            home_shots += 1
            home_xg += float(e.xg or 0)

            if e.is_on_target:
                home_sot += 1

            if e.event_type == "Goal":
                home_goals += 1

        elif e.team_id == AWAY_TEAM_ID:

            away_shots += 1
            away_xg += float(e.xg or 0)

            if e.is_on_target:
                away_sot += 1

            if e.event_type == "Goal":
                away_goals += 1

        idx += 1

    print(
        f"{minuto:02d} | "
        f"{home_goals}x{away_goals} | "
        f"Shots {home_shots}-{away_shots} | "
        f"SOT {home_sot}-{away_sot} | "
        f"xG {home_xg:.2f}-{away_xg:.2f}"
    )
