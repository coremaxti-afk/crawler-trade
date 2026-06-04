from sqlalchemy import create_engine, text

DB_USER = "postgres"
DB_PASSWORD = "92601050"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "late_goal_research"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

with engine.begin() as conn:

    conn.execute(text("""
        INSERT INTO matches
        (
            league,
            season,
            match_date,
            home_team,
            away_team
        )
        VALUES
        (
            'Premier League',
            '2025/26',
            '2026-08-15',
            'Arsenal',
            'Chelsea'
        )
    """))

    print("Partida inserida com sucesso!")
