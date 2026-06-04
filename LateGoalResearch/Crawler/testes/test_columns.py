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

        SELECT column_name

        FROM information_schema.columns

        WHERE table_name = 'matches'

        ORDER BY ordinal_position

    """))

    for row in result:
        print(row[0])
