from sqlalchemy import create_engine

# ==========================
# CONFIGURAÇÃO DO BANCO
# ==========================

DB_USER = "postgres"
DB_PASSWORD = "XXXXXXXXX"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "late_goal_research"

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/"
    f"{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)
