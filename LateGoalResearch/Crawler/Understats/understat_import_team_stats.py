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

# ==========================
# UNDERSTAT
# ==========================

url = "https://understat.com/getLeagueData/EPL/2024"

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://understat.com/league/EPL/2024"
}

data = requests.post(url, headers=headers).json()

teams = data["teams"]

contador = 0
nao_encontrados = 0

with engine.begin() as conn:

    for team_id, team_data in teams.items():

        team_name = team_data["title"]

        for game in team_data["history"]:

            match_date = game["date"]

            if game["h_a"] == "h":

                sql_match = text("""
                    SELECT id
                    FROM matches
                    WHERE match_date = :match_date
                    AND home_team = :team_name
                    LIMIT 1
                """)

            else:

                sql_match = text("""
                    SELECT id
                    FROM matches
                    WHERE match_date = :match_date
                    AND away_team = :team_name
                    LIMIT 1
                """)

            result = conn.execute(
                sql_match,
                {
                    "match_date": match_date,
                    "team_name": team_name
                }
            ).fetchone()

            if result is None:

                nao_encontrados += 1
                continue

            match_id = result[0]

            conn.execute(
                text("""
                INSERT INTO team_match_stats
                (
                    match_id,
                    team_name,
                    is_home,
                    match_date,
                    understat_team_id,

                    xg,
                    xga,

                    npxg,
                    npxga,

                    ppda_att,
                    ppda_def,

                    ppda_allowed_att,
                    ppda_allowed_def,

                    deep,
                    deep_allowed,

                    scored,
                    missed,

                    xpts,
                    pts,

                    npxgd,

                    result
                )
                VALUES
                (
                    :match_id,
                    :team_name,
                    :is_home,
                    :match_date,
                    :understat_team_id,

                    :xg,
                    :xga,

                    :npxg,
                    :npxga,

                    :ppda_att,
                    :ppda_def,

                    :ppda_allowed_att,
                    :ppda_allowed_def,

                    :deep,
                    :deep_allowed,

                    :scored,
                    :missed,

                    :xpts,
                    :pts,

                    :npxgd,

                    :result
                )
                """),
                {
                    "match_id": match_id,
                    "team_name": team_name,
                    "is_home": game["h_a"] == "h",
                    "match_date": match_date,
                    "understat_team_id": int(team_id),

                    "xg": game["xG"],
                    "xga": game["xGA"],

                    "npxg": game["npxG"],
                    "npxga": game["npxGA"],

                    "ppda_att": game["ppda"]["att"],
                    "ppda_def": game["ppda"]["def"],

                    "ppda_allowed_att": game["ppda_allowed"]["att"],
                    "ppda_allowed_def": game["ppda_allowed"]["def"],

                    "deep": game["deep"],
                    "deep_allowed": game["deep_allowed"],

                    "scored": game["scored"],
                    "missed": game["missed"],

                    "xpts": game["xpts"],
                    "pts": game["pts"],

                    "npxgd": game["npxGD"],

                    "result": game["result"]
                }
            )

            contador += 1

print()
print("Importação concluída")
print("Registros inseridos:", contador)
print("Jogos não encontrados:", nao_encontrados)
