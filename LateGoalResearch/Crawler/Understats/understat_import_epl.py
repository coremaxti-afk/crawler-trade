import requests
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
# TESTE DE CONEXÃO
# ==========================

with engine.connect() as conn:
    result = conn.execute(text("SELECT current_database();"))
    print("Banco conectado:", result.fetchone()[0])

# ==========================
# UNDERSTAT
# ==========================

url = "https://understat.com/getLeagueData/EPL/2024"

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://understat.com/league/EPL/2024"
}

response = requests.post(url, headers=headers)

if response.status_code != 200:
    print("Erro ao acessar Understat:", response.status_code)
    exit()

data = response.json()

matches = data["dates"]

print(f"Jogos encontrados: {len(matches)}")

# ==========================
# IMPORTAÇÃO
# ==========================

insert_sql = text("""
INSERT INTO matches
(
    understat_match_id,
    league,
    season,
    match_date,
    home_team,
    away_team,
    home_goals,
    away_goals,
    home_xg,
    away_xg,
    forecast_home_win,
    forecast_draw,
    forecast_away_win
)
VALUES
(
    :understat_match_id,
    :league,
    :season,
    :match_date,
    :home_team,
    :away_team,
    :home_goals,
    :away_goals,
    :home_xg,
    :away_xg,
    :forecast_home_win,
    :forecast_draw,
    :forecast_away_win
)
ON CONFLICT (understat_match_id)
DO NOTHING
""")

contador = 0

with engine.begin() as conn:

    for match in matches:

        conn.execute(
            insert_sql,
            {
                "understat_match_id": int(match["id"]),

                "league": "Premier League",
                "season": "2024/25",

                "match_date": match["datetime"],

                "home_team": match["h"]["title"],
                "away_team": match["a"]["title"],

                "home_goals": int(match["goals"]["h"]),
                "away_goals": int(match["goals"]["a"]),

                "home_xg": float(match["xG"]["h"]),
                "away_xg": float(match["xG"]["a"]),

                "forecast_home_win": float(match["forecast"]["w"]),
                "forecast_draw": float(match["forecast"]["d"]),
                "forecast_away_win": float(match["forecast"]["l"])
            }
        )

        contador += 1

print(f"Importação concluída! Jogos processados: {contador}")
