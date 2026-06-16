"""Discovery de estrategias por lado do time usando SportMonks + Football-Data.

Este script executa um estudo exploratorio, nao um modelo.

Fontes:
- SportMonks: trends, timeline, match_state e identity ja coletados em JSON bruto.
- Football-Data: odds pre-jogo 1X2 em CSV historico.

O que o script faz:
- calcula deltas por participant_id usando apenas minutos <= cutoff;
- separa time e adversario por participant_id;
- calcula placar no cutoff a partir dos eventos de gol do SportMonks;
- calcula targets futuros somente como alvo de avaliacao;
- junta favorito pre-jogo via Football-Data;
- testa combos Under Hold e Over Janela Curta;
- salva CSVs e relatorio Markdown.

O que o script NAO faz:
- nao cria modelo;
- nao cria baseline preditivo novo;
- nao faz backtesting financeiro real;
- nao altera schema;
- nao altera banco;
- nao cria robo;
- nao usa xgfixture;
- nao usa statistics final.

Como mudar campeonato/temporada:
- troque --sportmonks-root para a pasta bruta da liga/temporada SportMonks;
- troque --football-data-csv para o CSV Football-Data da mesma liga/temporada;
- troque --season-label para o nome que vai aparecer nos relatorios;
- se houver nomes diferentes entre fontes, ajuste TEAM_ALIASES abaixo.

Exemplo EPL 2025/26:
python sportmonks_team_side_strategy_discovery_v2.py ^
  --sportmonks-root C:\\LateGoalResearch\\data\\raw\\sportmonks\\full_collection\\england_premier_league_league_8_season_25583_2025_2026\\02_fixtures ^
  --football-data-csv C:\\LateGoalResearch\\data\\raw\\football_data\\england\\premier_league_2025_2026\\E0_2025_2026.csv ^
  --season-label epl_2025_26
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable


PROJECT_ROOT = Path(r"C:\LateGoalResearch")

DEFAULT_SPORTMONKS_ROOT = PROJECT_ROOT / (
    "data/raw/sportmonks/full_collection/"
    "england_premier_league_league_8_season_25583_2025_2026/02_fixtures"
)
DEFAULT_FOOTBALL_DATA_CSV = (
    PROJECT_ROOT / "data/raw/football_data/england/premier_league_2025_2026/E0_2025_2026.csv"
)
DEFAULT_DOC = (
    PROJECT_ROOT / "docs/04_RESEARCH/SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V2.md"
)
DEFAULT_SUMMARY = (
    PROJECT_ROOT / "data/processed/reports/sportmonks_team_side_strategy_discovery_summary_v2.csv"
)
DEFAULT_ENTRIES = (
    PROJECT_ROOT / "data/processed/reports/sportmonks_team_side_strategy_discovery_entries_v2.csv"
)

# Indicadores permitidos pela tarefa. Qualquer outro type vindo do trends e ignorado.
INDICATORS = [
    "Attacks",
    "Dangerous Attacks",
    "Shots Total",
    "Shots On Target",
    "Shots Off Target",
    "Corners",
    "Key Passes",
    "Big Chances Created",
    "Big Chances Missed",
]

CUTOFFS = [60, 65, 70, 75]
WINDOWS = [5, 10, 15]
TARGETS_UNDER = [(60, 80), (60, 90), (65, 80), (65, 90), (70, 85), (70, 90), (75, 90)]
TARGETS_OVER = [(60, 70), (60, 75), (65, 75), (65, 80), (70, 80), (70, 85), (75, 85), (75, 90)]

# Dicionario simples para parear SportMonks x Football-Data.
# Para outras ligas, adicione aliases quando o CSV abreviar nomes.
TEAM_ALIASES = {
    "man united": "manchester united",
    "manchester united": "manchester united",
    "man city": "manchester city",
    "manchester city": "manchester city",
    "newcastle": "newcastle united",
    "newcastle united": "newcastle united",
    "nott'm forest": "nottingham forest",
    "nott m forest": "nottingham forest",
    "nottingham forest": "nottingham forest",
    "wolves": "wolverhampton",
    "wolve": "wolverhampton",
    "wolverhampton": "wolverhampton",
    "wolverhampton wanderers": "wolverhampton",
    "tottenham": "tottenham hotspur",
    "tottenham hotspur": "tottenham hotspur",
    "west ham": "west ham united",
    "west ham united": "west ham united",
    "brighton": "brighton hove albion",
    "brighton & hove albion": "brighton hove albion",
    "brighton hove albion": "brighton hove albion",
    "ipswich": "ipswich town",
    "ipswich town": "ipswich town",
    "leicester": "leicester city",
    "leicester city": "leicester city",
    "bournemouth": "bournemouth",
    "afc bournemouth": "bournemouth",
    "leeds": "leeds united",
    "leed": "leeds united",
    "leeds united": "leeds united",
    "sunderland": "sunderland",
    "burnley": "burnley",
    "brentford": "brentford",
    "chelsea": "chelsea",
    "crystal palace": "crystal palace",
    "everton": "everton",
    "fulham": "fulham",
    "arsenal": "arsenal",
    "liverpool": "liverpool",
    "liverpool fc": "liverpool",
    "aston villa": "aston villa",
}


@dataclass
class Strategy:
    name: str
    family: str
    targets: list[tuple[int, int]]
    condition: Callable[[dict[str, Any], int], bool]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discovery SportMonks team-side V2 com favorito via Football-Data."
    )
    parser.add_argument("--sportmonks-root", default=str(DEFAULT_SPORTMONKS_ROOT))
    parser.add_argument("--football-data-csv", default=str(DEFAULT_FOOTBALL_DATA_CSV))
    parser.add_argument("--season-label", default="epl_2025_26")
    parser.add_argument("--summary-csv", default=str(DEFAULT_SUMMARY))
    parser.add_argument("--entries-csv", default=str(DEFAULT_ENTRIES))
    parser.add_argument("--report-md", default=str(DEFAULT_DOC))
    return parser.parse_args()


def normalize_team(name: str | None) -> str:
    raw = (name or "").lower().strip()
    if raw in TEAM_ALIASES:
        return TEAM_ALIASES[raw]
    text = raw.replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text).strip()
    text = text.replace(" and ", " ")
    text = re.sub(r"\s+", " ", text)
    return TEAM_ALIASES.get(text, text)


def safe_float(value: Any) -> float | None:
    try:
        if value in (None, ""):
            return None
        number = float(value)
        return None if math.isnan(number) else number
    except (TypeError, ValueError):
        return None


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def key_for_indicator(indicator: str) -> str:
    return indicator.lower().replace(" ", "_")


def target_name(family: str, start: int, end: int) -> str:
    prefix = "no_goal" if family == "Under Hold" else "goal"
    return f"{prefix}_{start}_{end}"


def load_football_data(csv_path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    """Carrega favorito pre-jogo 1X2 do Football-Data.

    Usamos AvgH/AvgD/AvgA porque sao a media de mercado e existem para EPL.
    Draw nunca define favorito; favorito e menor odd entre home e away.
    """
    odds_by_match: dict[tuple[str, str], dict[str, Any]] = {}
    with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            home_odd = safe_float(row.get("AvgH"))
            draw_odd = safe_float(row.get("AvgD"))
            away_odd = safe_float(row.get("AvgA"))
            favorite_side = ""
            favorite_odd = None
            if home_odd is not None and away_odd is not None:
                if home_odd < away_odd:
                    favorite_side = "home"
                    favorite_odd = home_odd
                elif away_odd < home_odd:
                    favorite_side = "away"
                    favorite_odd = away_odd
                else:
                    favorite_side = "tie_home_away"
                    favorite_odd = home_odd

            raw_home = 1 / home_odd if home_odd else None
            raw_draw = 1 / draw_odd if draw_odd else None
            raw_away = 1 / away_odd if away_odd else None
            raw_total = sum(value for value in (raw_home, raw_draw, raw_away) if value is not None)

            odds_by_match[(normalize_team(row.get("HomeTeam")), normalize_team(row.get("AwayTeam")))] = {
                "home_odd": home_odd,
                "draw_odd": draw_odd,
                "away_odd": away_odd,
                "favorite_side": favorite_side,
                "favorite_odd": favorite_odd,
                "odds_gap": abs(home_odd - away_odd)
                if home_odd is not None and away_odd is not None
                else None,
                "implied_home_raw": raw_home,
                "implied_draw_raw": raw_draw,
                "implied_away_raw": raw_away,
                "implied_home_norm": raw_home / raw_total if raw_home and raw_total else None,
                "implied_draw_norm": raw_draw / raw_total if raw_draw and raw_total else None,
                "implied_away_norm": raw_away / raw_total if raw_away and raw_total else None,
                "football_data_home": row.get("HomeTeam"),
                "football_data_away": row.get("AwayTeam"),
                "football_data_date": row.get("Date"),
                "football_data_time": row.get("Time"),
                "bookmaker": "Market average (AvgH/AvgD/AvgA)",
            }
    return odds_by_match


def value_at(series: list[tuple[int, float, Any]], minute: int) -> tuple[float, Any]:
    """Retorna ultimo valor acumulado conhecido ate o minuto."""
    value = 0.0
    period_id = None
    for item_minute, item_value, item_period_id in series:
        if item_minute <= minute:
            value = item_value
            period_id = item_period_id
        else:
            break
    return value, period_id


def delta_between(series: list[tuple[int, float, Any]], start: int, end: int) -> tuple[float, Any]:
    """Calcula delta de acumulado respeitando janela e cutoff."""
    end_value, end_period = value_at(series, end)
    start_value, start_period = value_at(series, max(0, start))
    return max(0.0, end_value - start_value), end_period or start_period


def score_at(goals: list[dict[str, Any]], cutoff: int, home_id: int, away_id: int) -> tuple[int, int]:
    home_goals = sum(1 for goal in goals if goal["minute"] <= cutoff and goal["participant_id"] == home_id)
    away_goals = sum(1 for goal in goals if goal["minute"] <= cutoff and goal["participant_id"] == away_id)
    return home_goals, away_goals


def goals_between(goals: list[dict[str, Any]], start: int, end: int) -> int:
    return sum(1 for goal in goals if start < goal["minute"] <= end)


def load_sportmonks_fixtures(root: Path) -> list[dict[str, Any]]:
    fixtures: list[dict[str, Any]] = []
    for fixture_dir in sorted(path for path in root.iterdir() if path.is_dir()):
        try:
            identity = read_json(fixture_dir / "02_identity/identity.json")["data"]
            match_state = read_json(fixture_dir / "03_match_state/match_state.json")["data"]
            trends = read_json(fixture_dir / "07_h8_pressure/trends.json")["data"].get("trends") or []
            timeline = read_json(fixture_dir / "05_minute_by_minute/timeline.json")["data"].get("timeline") or []
        except (OSError, KeyError, json.JSONDecodeError):
            continue

        participants: dict[str, dict[str, Any]] = {}
        for participant in identity.get("participants") or []:
            location = (participant.get("meta") or {}).get("location")
            if location in ("home", "away"):
                participants[location] = {"id": participant["id"], "name": participant["name"]}
        if "home" not in participants or "away" not in participants:
            continue

        goals: list[dict[str, Any]] = []
        for event in match_state.get("events") or []:
            event_type = (event.get("type") or {}).get("name") or ""
            if event_type.lower() == "goal" and event.get("minute") is not None:
                goals.append(
                    {
                        "minute": int(event["minute"]),
                        "participant_id": event.get("participant_id"),
                        "period_id": event.get("period_id"),
                    }
                )

        trends_by_participant: dict[int, dict[str, list[tuple[int, float, Any]]]] = {
            participants["home"]["id"]: {},
            participants["away"]["id"]: {},
        }
        for trend in trends:
            indicator = (trend.get("type") or {}).get("name")
            participant_id = trend.get("participant_id")
            minute = trend.get("minute")
            value = trend.get("value")
            if (
                indicator in INDICATORS
                and participant_id in trends_by_participant
                and minute is not None
                and value is not None
            ):
                trends_by_participant[participant_id].setdefault(indicator, []).append(
                    (int(minute), float(value), trend.get("period_id"))
                )
        for participant_trends in trends_by_participant.values():
            for indicator in participant_trends:
                participant_trends[indicator].sort()

        # Timeline e preservado para auditoria estrutural. Os deltas quantitativos saem de trends.
        timeline_counts: dict[int, dict[str, int]] = {
            participants["home"]["id"]: {},
            participants["away"]["id"]: {},
        }
        for event in timeline:
            participant_id = event.get("participant_id")
            minute = event.get("minute")
            event_type = ((event.get("type") or {}).get("name") or "").lower()
            if participant_id in timeline_counts and minute is not None and event_type:
                timeline_counts[participant_id][event_type] = timeline_counts[participant_id].get(event_type, 0) + 1

        fixtures.append(
            {
                "fixture_id": identity["id"],
                "fixture_name": identity.get("name"),
                "home_id": participants["home"]["id"],
                "away_id": participants["away"]["id"],
                "home_name": participants["home"]["name"],
                "away_name": participants["away"]["name"],
                "goals": goals,
                "trends": trends_by_participant,
                "timeline_counts": timeline_counts,
            }
        )
    return fixtures


def build_base_rows(
    fixtures: list[dict[str, Any]], football_data: dict[tuple[str, str], dict[str, Any]]
) -> tuple[list[dict[str, Any]], int]:
    """Cria linhas por fixture + cutoff + janela + participant_id."""
    rows: list[dict[str, Any]] = []
    missing_odds = 0
    for fixture in fixtures:
        odds = football_data.get(
            (normalize_team(fixture["home_name"]), normalize_team(fixture["away_name"]))
        )
        if not odds:
            missing_odds += 1
            continue

        for cutoff in CUTOFFS:
            home_score, away_score = score_at(
                fixture["goals"], cutoff, fixture["home_id"], fixture["away_id"]
            )
            for side, participant_id, opponent_id, team_name, opponent_name in [
                ("home", fixture["home_id"], fixture["away_id"], fixture["home_name"], fixture["away_name"]),
                ("away", fixture["away_id"], fixture["home_id"], fixture["away_name"], fixture["home_name"]),
            ]:
                score_diff = (home_score - away_score) if side == "home" else (away_score - home_score)
                for window in WINDOWS:
                    row: dict[str, Any] = {
                        "fixture_id": fixture["fixture_id"],
                        "fixture_name": fixture["fixture_name"],
                        "cutoff": cutoff,
                        "window": f"last_{window}m",
                        "team_side": side,
                        "participant_id": participant_id,
                        "opponent_participant_id": opponent_id,
                        "team_name": team_name,
                        "opponent_name": opponent_name,
                        "team_score_cutoff": home_score if side == "home" else away_score,
                        "opponent_score_cutoff": away_score if side == "home" else home_score,
                        "score_diff": score_diff,
                        "favorite_side": odds["favorite_side"],
                        "favorite_odd": odds["favorite_odd"],
                        "home_odd": odds["home_odd"],
                        "draw_odd": odds["draw_odd"],
                        "away_odd": odds["away_odd"],
                        "odds_gap": odds["odds_gap"],
                        "implied_home_norm": odds["implied_home_norm"],
                        "implied_draw_norm": odds["implied_draw_norm"],
                        "implied_away_norm": odds["implied_away_norm"],
                    }
                    row["is_favorite_side"] = side == odds["favorite_side"]
                    row["is_underdog_side"] = odds["favorite_side"] in ("home", "away") and side != odds["favorite_side"]
                    row["favorite_winning_by_1"] = row["is_favorite_side"] and score_diff == 1
                    row["favorite_losing"] = row["is_favorite_side"] and score_diff < 0
                    row["favorite_drawing"] = row["is_favorite_side"] and score_diff == 0
                    row["underdog_winning"] = row["is_underdog_side"] and score_diff > 0

                    period_id = None
                    for role, role_participant_id in [("team", participant_id), ("opp", opponent_id)]:
                        for indicator in INDICATORS:
                            indicator_key = key_for_indicator(indicator)
                            delta, delta_period = delta_between(
                                fixture["trends"][role_participant_id].get(indicator, []),
                                cutoff - window,
                                cutoff,
                            )
                            accumulated, accumulated_period = value_at(
                                fixture["trends"][role_participant_id].get(indicator, []), cutoff
                            )
                            row[f"{role}_{indicator_key}_{window}m"] = delta
                            row[f"{role}_{indicator_key}_cutoff"] = accumulated
                            period_id = period_id or delta_period or accumulated_period
                    row["period_id"] = period_id

                    for start, end in TARGETS_UNDER:
                        if start == cutoff:
                            row[f"no_goal_{start}_{end}"] = 1 if goals_between(fixture["goals"], start, end) == 0 else 0
                    for start, end in TARGETS_OVER:
                        if start == cutoff:
                            row[f"goal_{start}_{end}"] = 1 if goals_between(fixture["goals"], start, end) > 0 else 0
                    rows.append(row)
    return rows, missing_odds


def calculate_thresholds(rows: list[dict[str, Any]]) -> dict[tuple[int, int, str, str], float]:
    """Calcula p25/p75 por cutoff, janela e indicador."""
    thresholds: dict[tuple[int, int, str, str], float] = {}
    for cutoff in CUTOFFS:
        for window in WINDOWS:
            scoped = [row for row in rows if row["cutoff"] == cutoff and row["window"] == f"last_{window}m"]
            for role in ["team", "opp"]:
                for indicator in INDICATORS:
                    key = f"{role}_{key_for_indicator(indicator)}_{window}m"
                    values = sorted(float(row[key]) for row in scoped)
                    if not values:
                        continue
                    thresholds[(cutoff, window, key, "p25")] = values[int(0.25 * (len(values) - 1))]
                    thresholds[(cutoff, window, key, "p75")] = values[int(0.75 * (len(values) - 1))]
    return thresholds


def fisher_two_sided(a: int, b: int, c: int, d: int) -> float | None:
    """Teste exato de Fisher 2-sided para tabela 2x2."""
    from math import comb

    n = a + b + c + d
    row_1 = a + b
    col_1 = a + c
    if n == 0 or row_1 == 0:
        return None

    def probability(x: int) -> float:
        return comb(col_1, x) * comb(n - col_1, row_1 - x) / comb(n, row_1)

    low = max(0, row_1 - (n - col_1))
    high = min(row_1, col_1)
    observed = probability(a)
    return sum(probability(x) for x in range(low, high + 1) if probability(x) <= observed + 1e-15)


def odds_ratio(a: int, b: int, c: int, d: int) -> float:
    """Odds ratio com correcao quando existe zero em alguma celula."""
    if min(a, b, c, d) == 0:
        a, b, c, d = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    return (a * d) / (b * c)


def build_strategies(thresholds: dict[tuple[int, int, str, str], float]) -> list[Strategy]:
    """Define combos testados.

    As condicoes usam sempre a linha do time analisado. Para cenarios do adversario,
    usamos colunas `opp_*`.
    """

    def p(row: dict[str, Any], window: int, key: str, quantile: str) -> float:
        return thresholds[(row["cutoff"], window, key, quantile)]

    return [
        Strategy(
            "team_winning_by_1_opp_cold_2of3",
            "Under Hold",
            TARGETS_UNDER,
            lambda r, w: r["score_diff"] == 1
            and sum(
                [
                    r[f"opp_shots_total_{w}m"] <= p(r, w, f"opp_shots_total_{w}m", "p25"),
                    r[f"opp_dangerous_attacks_{w}m"] <= p(r, w, f"opp_dangerous_attacks_{w}m", "p25"),
                    r[f"opp_key_passes_{w}m"] <= p(r, w, f"opp_key_passes_{w}m", "p25"),
                ]
            )
            >= 2,
        ),
        Strategy(
            "favorite_winning_by_1_opp_cold_2of3",
            "Under Hold",
            TARGETS_UNDER,
            lambda r, w: r["favorite_winning_by_1"]
            and sum(
                [
                    r[f"opp_shots_total_{w}m"] <= p(r, w, f"opp_shots_total_{w}m", "p25"),
                    r[f"opp_dangerous_attacks_{w}m"] <= p(r, w, f"opp_dangerous_attacks_{w}m", "p25"),
                    r[f"opp_key_passes_{w}m"] <= p(r, w, f"opp_key_passes_{w}m", "p25"),
                ]
            )
            >= 2,
        ),
        Strategy("team_winning_by_1_no_sot_against", "Under Hold", TARGETS_UNDER, lambda r, w: r["score_diff"] == 1 and r[f"opp_shots_on_target_{w}m"] == 0),
        Strategy(
            "team_winning_by_1_low_dangerous_attacks_against",
            "Under Hold",
            TARGETS_UNDER,
            lambda r, w: r["score_diff"] == 1 and r[f"opp_dangerous_attacks_{w}m"] <= p(r, w, f"opp_dangerous_attacks_{w}m", "p25"),
        ),
        Strategy(
            "both_teams_cold_2of3",
            "Under Hold",
            TARGETS_UNDER,
            lambda r, w: sum(
                [
                    r[f"team_shots_total_{w}m"] <= p(r, w, f"team_shots_total_{w}m", "p25"),
                    r[f"opp_shots_total_{w}m"] <= p(r, w, f"opp_shots_total_{w}m", "p25"),
                    r[f"team_dangerous_attacks_{w}m"] <= p(r, w, f"team_dangerous_attacks_{w}m", "p25"),
                    r[f"opp_dangerous_attacks_{w}m"] <= p(r, w, f"opp_dangerous_attacks_{w}m", "p25"),
                ]
            )
            >= 3,
        ),
        Strategy("opponent_no_big_chances", "Under Hold", TARGETS_UNDER, lambda r, w: r["score_diff"] == 1 and r[f"opp_big_chances_created_{w}m"] == 0),
        Strategy("opponent_no_recent_key_passes", "Under Hold", TARGETS_UNDER, lambda r, w: r["score_diff"] == 1 and r[f"opp_key_passes_{w}m"] == 0),
        Strategy(
            "team_losing_pressure_high_2of3",
            "Over Janela Curta",
            TARGETS_OVER,
            lambda r, w: r["score_diff"] < 0
            and sum(
                [
                    r[f"team_dangerous_attacks_{w}m"] >= p(r, w, f"team_dangerous_attacks_{w}m", "p75"),
                    r[f"team_shots_total_{w}m"] >= p(r, w, f"team_shots_total_{w}m", "p75"),
                    r[f"team_key_passes_{w}m"] >= p(r, w, f"team_key_passes_{w}m", "p75"),
                ]
            )
            >= 2,
        ),
        Strategy(
            "favorite_losing_pressure_high_2of3",
            "Over Janela Curta",
            TARGETS_OVER,
            lambda r, w: r["favorite_losing"]
            and sum(
                [
                    r[f"team_dangerous_attacks_{w}m"] >= p(r, w, f"team_dangerous_attacks_{w}m", "p75"),
                    r[f"team_shots_total_{w}m"] >= p(r, w, f"team_shots_total_{w}m", "p75"),
                    r[f"team_key_passes_{w}m"] >= p(r, w, f"team_key_passes_{w}m", "p75"),
                ]
            )
            >= 2,
        ),
        Strategy(
            "favorite_drawing_pressure_high_2of3",
            "Over Janela Curta",
            TARGETS_OVER,
            lambda r, w: r["favorite_drawing"]
            and sum(
                [
                    r[f"team_dangerous_attacks_{w}m"] >= p(r, w, f"team_dangerous_attacks_{w}m", "p75"),
                    r[f"team_shots_total_{w}m"] >= p(r, w, f"team_shots_total_{w}m", "p75"),
                    r[f"team_key_passes_{w}m"] >= p(r, w, f"team_key_passes_{w}m", "p75"),
                ]
            )
            >= 2,
        ),
        Strategy(
            "underdog_winning_favorite_pressing_2of3",
            "Over Janela Curta",
            TARGETS_OVER,
            lambda r, w: r["is_favorite_side"]
            and r["score_diff"] < 0
            and sum(
                [
                    r[f"team_dangerous_attacks_{w}m"] >= p(r, w, f"team_dangerous_attacks_{w}m", "p75"),
                    r[f"team_shots_total_{w}m"] >= p(r, w, f"team_shots_total_{w}m", "p75"),
                    r[f"team_key_passes_{w}m"] >= p(r, w, f"team_key_passes_{w}m", "p75"),
                ]
            )
            >= 2,
        ),
        Strategy("dangerous_attacks_accelerating", "Over Janela Curta", TARGETS_OVER, lambda r, w: r[f"team_dangerous_attacks_{w}m"] >= p(r, w, f"team_dangerous_attacks_{w}m", "p75")),
        Strategy("shots_on_target_recent", "Over Janela Curta", TARGETS_OVER, lambda r, w: r[f"team_shots_on_target_{w}m"] >= 1),
        Strategy("big_chances_recent", "Over Janela Curta", TARGETS_OVER, lambda r, w: r[f"team_big_chances_created_{w}m"] >= 1),
        Strategy("key_passes_recent_high", "Over Janela Curta", TARGETS_OVER, lambda r, w: r[f"team_key_passes_{w}m"] >= p(r, w, f"team_key_passes_{w}m", "p75")),
        Strategy("corners_recent_high", "Over Janela Curta", TARGETS_OVER, lambda r, w: r[f"team_corners_{w}m"] >= p(r, w, f"team_corners_{w}m", "p75")),
        Strategy("home_winning_by_1_visitor_pressing", "Over Janela Curta", TARGETS_OVER, lambda r, w: r["team_side"] == "away" and r["score_diff"] == -1 and (r[f"team_dangerous_attacks_{w}m"] >= p(r, w, f"team_dangerous_attacks_{w}m", "p75") or r[f"team_shots_on_target_{w}m"] >= 1)),
        Strategy("away_winning_by_1_home_pressing", "Over Janela Curta", TARGETS_OVER, lambda r, w: r["team_side"] == "home" and r["score_diff"] == -1 and (r[f"team_dangerous_attacks_{w}m"] >= p(r, w, f"team_dangerous_attacks_{w}m", "p75") or r[f"team_shots_on_target_{w}m"] >= 1)),
    ]


def classify_status(n: int, diff: float | None, p_value: float | None, effect: float | None) -> str:
    if (
        n >= 20
        and diff is not None
        and diff >= 0.08
        and ((p_value is not None and p_value <= 0.10) or (effect is not None and effect >= 1.8))
    ):
        return "PROMISSOR"
    if n >= 10 and diff is not None and diff > 0:
        return "OBSERVACAO"
    return "DESCARTADO"


def evaluate_strategies(rows: list[dict[str, Any]], strategies: list[Strategy]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    summary: list[dict[str, Any]] = []
    entries: list[dict[str, Any]] = []

    for strategy in strategies:
        for window in WINDOWS:
            for start, end in strategy.targets:
                target = target_name(strategy.family, start, end)
                scoped = [
                    row for row in rows if row["cutoff"] == start and row["window"] == f"last_{window}m" and target in row
                ]
                if not scoped:
                    continue
                baseline = sum(row[target] for row in scoped) / len(scoped)
                selected = [row for row in scoped if strategy.condition(row, window)]
                n = len(selected)
                hits = sum(row[target] for row in selected)
                errors = n - hits
                rest_n = len(scoped) - n
                rest_hits = sum(row[target] for row in scoped) - hits
                rest_errors = rest_n - rest_hits
                rate = hits / n if n else None
                diff = (rate - baseline) if rate is not None else None
                effect = odds_ratio(hits, errors, rest_hits, rest_errors) if n else None
                p_value = fisher_two_sided(hits, errors, rest_hits, rest_errors) if n else None
                status = classify_status(n, diff, p_value, effect)
                strategy_id = f"{strategy.family}|{strategy.name}|c{start}|{target}|last_{window}m"

                summary.append(
                    {
                        "strategy_name": strategy.name,
                        "family": strategy.family,
                        "cutoff": start,
                        "target": target,
                        "window": f"last_{window}m",
                        "N": n,
                        "hits": hits,
                        "errors": errors,
                        "rate": rate if rate is not None else "",
                        "baseline": baseline,
                        "diff_vs_baseline": diff if diff is not None else "",
                        "odds_ratio": effect if effect is not None else "",
                        "p_value": p_value if p_value is not None else "",
                        "status": status,
                        "strategy_id": strategy_id,
                    }
                )

                for row in selected:
                    entry = {
                        "strategy_id": strategy_id,
                        "strategy_name": strategy.name,
                        "family": strategy.family,
                        "target": target,
                        "hit": row[target],
                    }
                    for key in [
                        "fixture_id",
                        "fixture_name",
                        "cutoff",
                        "window",
                        "period_id",
                        "team_side",
                        "participant_id",
                        "opponent_participant_id",
                        "team_name",
                        "opponent_name",
                        "team_score_cutoff",
                        "opponent_score_cutoff",
                        "score_diff",
                        "favorite_side",
                        "favorite_odd",
                        "home_odd",
                        "draw_odd",
                        "away_odd",
                        "odds_gap",
                    ]:
                        entry[key] = row.get(key)
                    for indicator in INDICATORS:
                        indicator_key = key_for_indicator(indicator)
                        window_minutes = int(str(row["window"]).replace("last_", "").replace("m", ""))
                        entry[f"team_{indicator_key}"] = row.get(f"team_{indicator_key}_{window_minutes}m")
                        entry[f"opp_{indicator_key}"] = row.get(f"opp_{indicator_key}_{window_minutes}m")
                    entries.append(entry)
    return summary, entries


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def pct(value: Any) -> str:
    if value in ("", None):
        return "NA"
    return f"{float(value) * 100:.1f}%"


def num(value: Any) -> str:
    if value in ("", None):
        return "NA"
    return f"{float(value):.4f}"


def write_report(
    path: Path,
    summary: list[dict[str, Any]],
    entries: list[dict[str, Any]],
    fixtures_count: int,
    missing_odds: int,
    season_label: str,
    summary_csv: Path,
    entries_csv: Path,
) -> str:
    promissor = [row for row in summary if row["status"] == "PROMISSOR"]
    observacao = [row for row in summary if row["status"] == "OBSERVACAO"]
    decision = "APROVADO COM RESSALVAS" if promissor else ("PROMISSOR MAS INCONCLUSIVO" if observacao else "BLOQUEADO")
    ranked = sorted(
        summary,
        key=lambda row: (
            row["status"] != "PROMISSOR",
            -(float(row["diff_vs_baseline"]) if row["diff_vs_baseline"] != "" else -999),
            -int(row["N"]),
        ),
    )[:35]

    lines = [
        "# SPORTMONKS_TEAM_SIDE_STRATEGY_DISCOVERY_RESULTS_V2",
        "",
        f"Data: {datetime.now().date().isoformat()}",
        "",
        f"Decisao final: **{decision}**",
        "",
        "## Escopo",
        f"- Temporada/label: `{season_label}`.",
        "- Fonte de jogo: SportMonks EPL 2025/26 ja coletado localmente.",
        "- Fonte de favorito: Football-Data odds pre-jogo 1X2 (`AvgH/AvgD/AvgA`).",
        f"- Fixtures SportMonks processadas: `{fixtures_count}`.",
        f"- Fixtures sem pareamento de odds Football-Data: `{missing_odds}`.",
        "- Grao: fixture + cutoff + janela + participant_id.",
        "",
        "## Cobertura",
        f"- Combos avaliados: `{len(summary)}`.",
        f"- Entradas geradas: `{len(entries)}`.",
        f"- PROMISSOR: `{len(promissor)}`.",
        f"- OBSERVACAO: `{len(observacao)}`.",
        f"- DESCARTADO: `{len(summary) - len(promissor) - len(observacao)}`.",
        "",
        "## Top resultados",
        "| status | familia | estrategia | cutoff | target | janela | N | taxa | baseline | diff | OR | p |",
        "| --- | --- | --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in ranked:
        lines.append(
            f"| {row['status']} | {row['family']} | {row['strategy_name']} | {row['cutoff']} | "
            f"{row['target']} | {row['window']} | {row['N']} | {pct(row['rate'])} | "
            f"{pct(row['baseline'])} | {pct(row['diff_vs_baseline'])} | "
            f"{num(row['odds_ratio'])} | {num(row['p_value'])} |"
        )

    favorite_rows = [row for row in ranked if "favorite" in row["strategy_name"] or "underdog" in row["strategy_name"]]
    lines.extend(
        [
            "",
            "## Nota sobre favoritos",
            "- Diferente da V1, esta V2 usa Football-Data para permitir combos com favorito real.",
            "- Draw nao define favorito; favorito e menor odd entre Home e Away.",
            f"- Resultados favoritos no top exibido: `{len(favorite_rows)}`.",
            "",
            "## Anti-leakage",
            "- Todas as features usam apenas registros com minuto <= cutoff.",
            "- Acumulados sao deltas `valor_cutoff - valor_cutoff_janela`.",
            "- Placar final nao foi usado como feature.",
            "- Football-Data entra somente como odds pre-jogo; nenhuma odd live foi usada.",
            "- `xgfixture` e `statistics` final nao foram usados.",
            "- Nenhum modelo, baseline preditivo, schema, robo ou backtesting financeiro foi criado.",
            "",
            "## Como reproduzir",
            "- Use `Crawler/Sportmonks/sportmonks_team_side_strategy_discovery_v2.py`.",
            "- Para outra liga/temporada, altere `--sportmonks-root`, `--football-data-csv` e `--season-label`.",
            "",
            "## Artefatos",
            f"- CSV summary: `{summary_csv}`",
            f"- CSV entries: `{entries_csv}`",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return decision


def main() -> None:
    args = parse_args()
    sportmonks_root = Path(args.sportmonks_root)
    football_data_csv = Path(args.football_data_csv)
    summary_csv = Path(args.summary_csv)
    entries_csv = Path(args.entries_csv)
    report_md = Path(args.report_md)

    football_data = load_football_data(football_data_csv)
    fixtures = load_sportmonks_fixtures(sportmonks_root)
    base_rows, missing_odds = build_base_rows(fixtures, football_data)
    thresholds = calculate_thresholds(base_rows)
    strategies = build_strategies(thresholds)
    summary, entries = evaluate_strategies(base_rows, strategies)

    write_csv(
        summary_csv,
        summary,
        [
            "strategy_name",
            "family",
            "cutoff",
            "target",
            "window",
            "N",
            "hits",
            "errors",
            "rate",
            "baseline",
            "diff_vs_baseline",
            "odds_ratio",
            "p_value",
            "status",
            "strategy_id",
        ],
    )
    write_csv(entries_csv, entries)
    decision = write_report(
        report_md,
        summary,
        entries,
        len(fixtures),
        missing_odds,
        args.season_label,
        summary_csv,
        entries_csv,
    )

    print(
        json.dumps(
            {
                "decision": decision,
                "fixtures": len(fixtures),
                "missing_odds": missing_odds,
                "summary_rows": len(summary),
                "entries": len(entries),
                "promissor": sum(1 for row in summary if row["status"] == "PROMISSOR"),
                "observacao": sum(1 for row in summary if row["status"] == "OBSERVACAO"),
                "summary_csv": str(summary_csv),
                "entries_csv": str(entries_csv),
                "report_md": str(report_md),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
