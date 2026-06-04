from sqlalchemy import create_engine, text

DB_USER = "postgres"
DB_PASSWORD = "92601050"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "late_goal_research"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

with engine.connect() as conn:

    result = conn.execute(text("""
        SELECT id,
               home_team,
               away_team,
               match_date
        FROM matches
        LIMIT 5
    """))

    for row in result:
        print(row)
