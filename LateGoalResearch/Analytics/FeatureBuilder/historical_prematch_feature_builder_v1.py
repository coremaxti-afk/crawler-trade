"""Build Historical Pre-Match Features V1 for H3/H4 validation.

Read-only PostgreSQL flow:
- reads matches_master, match_statistics and match_incidents metadata;
- builds one row per team per match;
- computes only historical pre-match rolling features;
- uses shift(1) before every rolling/expanding calculation;
- writes CSV, Parquet, metadata and validation report locally.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import engine  # noqa: E402

FEATURE_SET_NAME = "historical_prematch_features_v1"
FEATURE_SET_VERSION = "v1"
KNOWN_SKIPPED_MATCH_IDS = {"12436452"}
EXPECTED_MATCHES = 380
EXPECTED_ROWS = EXPECTED_MATCHES * 2
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "features"
CSV_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}.csv"
PARQUET_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}.parquet"
METADATA_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}_metadata.json"
VALIDATION_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}_validation_report.json"
GROUP_KEYS = ["season", "team_name"]
SORT_COLUMNS = ["season", "team_name", "match_date", "match_id"]
BASE_METRICS = [
    "goals_for",
    "goals_against",
    "shots_for",
    "shots_against",
    "shots_on_target_for",
    "shots_on_target_against",
    "big_chances_for",
    "big_chances_against",
]
REQUIRED_FEATURE_COLUMNS = [
    "goals_for_avg_last_3",
    "goals_for_avg_last_5",
    "goals_for_avg_last_10",
    "shots_for_avg_last_5",
    "shots_on_target_for_avg_last_5",
    "big_chances_for_avg_last_5",
    "goals_against_avg_last_3",
    "goals_against_avg_last_5",
    "goals_against_avg_last_10",
    "shots_against_avg_last_5",
    "shots_on_target_against_avg_last_5",
    "big_chances_against_avg_last_5",
]
SEASON_TO_DATE_FEATURE_COLUMNS = [f"{metric}_avg_season_to_date" for metric in BASE_METRICS]
OUTPUT_COLUMNS = [
    "match_id",
    "sofascore_event_id",
    "league",
    "season",
    "match_date",
    "team_name",
    "opponent_team",
    "is_home",
    "history_matches_available",
    "history_window_3_complete",
    "history_window_5_complete",
    "history_window_10_complete",
    "is_early_season",
    *REQUIRED_FEATURE_COLUMNS,
    *SEASON_TO_DATE_FEATURE_COLUMNS,
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build historical pre-match features V1 from PostgreSQL.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directory for CSV, Parquet and reports.")
    return parser.parse_args()


def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    return str(value)


def parquet_engine_available() -> bool:
    return bool(importlib.util.find_spec("pyarrow") or importlib.util.find_spec("fastparquet"))


def table_counts() -> dict[str, int]:
    tables = ["matches_master", "match_statistics", "match_incidents"]
    with engine.connect() as conn:
        return {table: int(conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()) for table in tables}


def fetch_match_level_source() -> pd.DataFrame:
    sql = text(
        """
        SELECT
            m.match_id,
            m.sofascore_event_id,
            m.league,
            m.season,
            m.match_date,
            m.home_team,
            m.away_team,
            m.home_goals,
            m.away_goals,
            s.shots_home,
            s.shots_away,
            s.shots_on_target_home,
            s.shots_on_target_away,
            s.big_chances_home,
            s.big_chances_away
        FROM matches_master m
        LEFT JOIN match_statistics s
          ON s.sofascore_event_id = m.sofascore_event_id
        WHERE m.sofascore_event_id::text NOT IN :skipped_ids
        ORDER BY m.match_date, m.match_id
        """
    )
    with engine.connect() as conn:
        return pd.read_sql_query(sql, conn, params={"skipped_ids": tuple(KNOWN_SKIPPED_MATCH_IDS)})


def build_team_match_rows(match_df: pd.DataFrame) -> pd.DataFrame:
    home = pd.DataFrame(
        {
            "match_id": match_df["match_id"],
            "sofascore_event_id": match_df["sofascore_event_id"],
            "league": match_df["league"],
            "season": match_df["season"],
            "match_date": match_df["match_date"],
            "team_name": match_df["home_team"],
            "opponent_team": match_df["away_team"],
            "is_home": 1,
            "goals_for": match_df["home_goals"],
            "goals_against": match_df["away_goals"],
            "shots_for": match_df["shots_home"],
            "shots_against": match_df["shots_away"],
            "shots_on_target_for": match_df["shots_on_target_home"],
            "shots_on_target_against": match_df["shots_on_target_away"],
            "big_chances_for": match_df["big_chances_home"],
            "big_chances_against": match_df["big_chances_away"],
        }
    )
    away = pd.DataFrame(
        {
            "match_id": match_df["match_id"],
            "sofascore_event_id": match_df["sofascore_event_id"],
            "league": match_df["league"],
            "season": match_df["season"],
            "match_date": match_df["match_date"],
            "team_name": match_df["away_team"],
            "opponent_team": match_df["home_team"],
            "is_home": 0,
            "goals_for": match_df["away_goals"],
            "goals_against": match_df["home_goals"],
            "shots_for": match_df["shots_away"],
            "shots_against": match_df["shots_home"],
            "shots_on_target_for": match_df["shots_on_target_away"],
            "shots_on_target_against": match_df["shots_on_target_home"],
            "big_chances_for": match_df["big_chances_away"],
            "big_chances_against": match_df["big_chances_home"],
        }
    )
    team_df = pd.concat([home, away], ignore_index=True)
    team_df["match_date"] = pd.to_datetime(team_df["match_date"])
    return team_df.sort_values(SORT_COLUMNS).reset_index(drop=True)


def add_historical_features(team_df: pd.DataFrame) -> pd.DataFrame:
    df = team_df.copy()
    df["history_matches_available"] = df.groupby(GROUP_KEYS).cumcount()
    df["history_window_3_complete"] = (df["history_matches_available"] >= 3).astype(int)
    df["history_window_5_complete"] = (df["history_matches_available"] >= 5).astype(int)
    df["history_window_10_complete"] = (df["history_matches_available"] >= 10).astype(int)
    df["is_early_season"] = (df["history_matches_available"] < 5).astype(int)

    for metric in BASE_METRICS:
        prior_col = f"{metric}_prior"
        df[prior_col] = df.groupby(GROUP_KEYS)[metric].shift(1)
        for window in [3, 5, 10]:
            df[f"{metric}_avg_last_{window}"] = df.groupby(GROUP_KEYS)[prior_col].transform(
                lambda values, w=window: values.rolling(window=w, min_periods=1).mean()
            )
        df[f"{metric}_avg_season_to_date"] = df.groupby(GROUP_KEYS)[prior_col].transform(
            lambda values: values.expanding(min_periods=1).mean()
        )

    return df


def expected_mean(values: pd.Series) -> float | None:
    clean = pd.to_numeric(values, errors="coerce").dropna()
    if clean.empty:
        return None
    return float(clean.mean())


def values_match(actual: Any, expected: float | None) -> bool:
    if expected is None:
        return pd.isna(actual)
    if pd.isna(actual):
        return False
    return abs(float(actual) - expected) < 1e-9


def validate_rolling_no_leakage(df: pd.DataFrame) -> dict[str, Any]:
    checks_run = 0
    mismatches: list[dict[str, Any]] = []
    rolling_specs = []
    for metric in BASE_METRICS:
        for window in [3, 5, 10]:
            rolling_specs.append((metric, window, f"{metric}_avg_last_{window}"))
        rolling_specs.append((metric, None, f"{metric}_avg_season_to_date"))

    for _, group in df.groupby(GROUP_KEYS, sort=False):
        group = group.sort_values(["match_date", "match_id"])
        for position, (idx, row) in enumerate(group.iterrows()):
            for metric, window, feature_col in rolling_specs:
                prior_values = group.iloc[:position][metric]
                if window is not None:
                    prior_values = prior_values.tail(window)
                expected = expected_mean(prior_values)
                actual = row[feature_col]
                checks_run += 1
                if not values_match(actual, expected):
                    mismatches.append(
                        {
                            "match_id": int(row["match_id"]),
                            "team_name": row["team_name"],
                            "feature": feature_col,
                            "actual": None if pd.isna(actual) else float(actual),
                            "expected": expected,
                        }
                    )
                    if len(mismatches) >= 20:
                        return {"checks_run": checks_run, "mismatch_count": len(mismatches), "sample_mismatches": mismatches}
    return {"checks_run": checks_run, "mismatch_count": len(mismatches), "sample_mismatches": mismatches}


def validate_dataset(df: pd.DataFrame, match_count: int, source_counts: dict[str, int], parquet_written: bool) -> dict[str, Any]:
    duplicate_key_count = int(df.duplicated(subset=["match_id", "team_name"]).sum())
    rows_per_match = df.groupby("match_id").size()
    invalid_rows_per_match = rows_per_match[rows_per_match != 2]
    first_rows = df.sort_values(SORT_COLUMNS).groupby(GROUP_KEYS, as_index=False).head(1)
    required_nulls = {column: int(df[column].isna().sum()) for column in ["match_id", "sofascore_event_id", "match_date", "team_name", "opponent_team"]}
    first_feature_non_null = int(first_rows[REQUIRED_FEATURE_COLUMNS + SEASON_TO_DATE_FEATURE_COLUMNS].notna().sum().sum())
    first_history_not_zero = int((first_rows["history_matches_available"] != 0).sum())
    no_history_rows = df[df["history_matches_available"] == 0]
    no_history_feature_non_null = int(no_history_rows[REQUIRED_FEATURE_COLUMNS + SEASON_TO_DATE_FEATURE_COLUMNS].notna().sum().sum())
    leakage_check = validate_rolling_no_leakage(df)

    feature_null_counts = {column: int(df[column].isna().sum()) for column in REQUIRED_FEATURE_COLUMNS + SEASON_TO_DATE_FEATURE_COLUMNS}
    errors: list[str] = []
    warnings: list[str] = []

    if match_count != EXPECTED_MATCHES:
        errors.append(f"Expected {EXPECTED_MATCHES} matches, found {match_count}.")
    if len(df) != EXPECTED_ROWS:
        errors.append(f"Expected {EXPECTED_ROWS} team-match rows, found {len(df)}.")
    if duplicate_key_count:
        errors.append(f"Duplicate match_id + team_name rows found: {duplicate_key_count}.")
    if len(invalid_rows_per_match):
        errors.append(f"Found {len(invalid_rows_per_match)} matches without exactly 2 team rows.")
    if any(value > 0 for value in required_nulls.values()):
        errors.append("Required identifier columns contain null values.")
    if first_history_not_zero:
        errors.append("At least one team first match does not have history_matches_available = 0.")
    if first_feature_non_null or no_history_feature_non_null:
        errors.append("Historical features are populated for rows with no prior team history.")
    if leakage_check["mismatch_count"]:
        errors.append("Rolling feature recomputation found temporal leakage mismatches.")
    if not parquet_written:
        errors.append("Parquet export was not created.")

    expected_first_row_nulls = len(no_history_rows)
    big_chance_null_features = {
        k: v for k, v in feature_null_counts.items()
        if k.startswith("big_chances") and v > expected_first_row_nulls
    }
    if big_chance_null_features:
        warnings.append("big_chances source columns contain nulls beyond first-match no-history rows; rolling averages may be null when no prior non-null observations exist.")

    status = "NAO APTO" if errors else "APTO COM RESSALVAS" if warnings else "APTO"
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "feature_set_name": FEATURE_SET_NAME,
        "feature_set_version": FEATURE_SET_VERSION,
        "status": status,
        "grain": "one row per team per match",
        "row_count": int(len(df)),
        "expected_row_count": EXPECTED_ROWS,
        "match_count": int(match_count),
        "expected_match_count": EXPECTED_MATCHES,
        "team_count": int(df["team_name"].nunique()),
        "source_table_counts": source_counts,
        "duplicate_match_team_rows": duplicate_key_count,
        "matches_without_two_team_rows": int(len(invalid_rows_per_match)),
        "invalid_rows_per_match_sample": {str(k): int(v) for k, v in invalid_rows_per_match.head(20).to_dict().items()},
        "required_null_counts": required_nulls,
        "history_rows_without_prior_match": int(len(no_history_rows)),
        "first_rows_checked": int(len(first_rows)),
        "first_team_match_feature_non_null_count": first_feature_non_null,
        "no_history_feature_non_null_count": no_history_feature_non_null,
        "history_window_3_complete_count": int(df["history_window_3_complete"].sum()),
        "history_window_5_complete_count": int(df["history_window_5_complete"].sum()),
        "history_window_10_complete_count": int(df["history_window_10_complete"].sum()),
        "early_season_rows": int(df["is_early_season"].sum()),
        "feature_null_counts": feature_null_counts,
        "temporal_leakage_validation": leakage_check,
        "parquet_written": parquet_written,
        "validation_errors": errors,
        "validation_warnings": warnings,
    }


def build_metadata(df: pd.DataFrame, validation: dict[str, Any]) -> dict[str, Any]:
    feature_columns = REQUIRED_FEATURE_COLUMNS + SEASON_TO_DATE_FEATURE_COLUMNS
    return {
        "feature_set_name": FEATURE_SET_NAME,
        "feature_set_version": FEATURE_SET_VERSION,
        "generated_at": validation["generated_at"],
        "grain": "one row per team per match; each match creates one home row and one away row",
        "source_tables": ["matches_master", "match_statistics", "match_incidents"],
        "read_only_postgresql": True,
        "known_skipped_match_ids": sorted(KNOWN_SKIPPED_MATCH_IDS),
        "ordering_rule": "season, team_name, match_date, match_id",
        "anti_leakage_rule": "groupby(season, team_name).shift(1) is applied before rolling or expanding calculations",
        "target_columns_excluded": ["has_late_goal", "target_late_goal_75", "target_goal_after_cutoff"],
        "row_count": int(len(df)),
        "match_count": int(validation["match_count"]),
        "team_count": int(validation["team_count"]),
        "history_columns": [
            "history_matches_available",
            "history_window_3_complete",
            "history_window_5_complete",
            "history_window_10_complete",
            "is_early_season",
        ],
        "h3_offensive_features": [
            "goals_for_avg_last_3",
            "goals_for_avg_last_5",
            "goals_for_avg_last_10",
            "shots_for_avg_last_5",
            "shots_on_target_for_avg_last_5",
            "big_chances_for_avg_last_5",
        ],
        "h4_defensive_features": [
            "goals_against_avg_last_3",
            "goals_against_avg_last_5",
            "goals_against_avg_last_10",
            "shots_against_avg_last_5",
            "shots_on_target_against_avg_last_5",
            "big_chances_against_avg_last_5",
        ],
        "season_to_date_features": SEASON_TO_DATE_FEATURE_COLUMNS,
        "all_feature_columns": feature_columns,
        "output_files": {
            "csv": str(CSV_PATH),
            "parquet": str(PARQUET_PATH),
            "metadata": str(METADATA_PATH),
            "validation_report": str(VALIDATION_PATH),
        },
        "validation_status": validation["status"],
        "limitations": [
            "Feature values depend on imported SofaScore full-time match statistics from prior matches only.",
            "No target columns, full-match statistics from the current match, crawler data writes or model outputs are included.",
            "big_chances rolling features can be null early in the season when prior source observations are null.",
        ],
    }


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)

    print("Building historical pre-match feature set V1...")
    source_counts = table_counts()
    match_df = fetch_match_level_source()
    print(f"Source matches loaded: {len(match_df)}")

    team_rows = build_team_match_rows(match_df)
    feature_df_internal = add_historical_features(team_rows)
    output_df = feature_df_internal[OUTPUT_COLUMNS].copy()

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / CSV_PATH.name
    parquet_path = output_dir / PARQUET_PATH.name
    metadata_path = output_dir / METADATA_PATH.name
    validation_path = output_dir / VALIDATION_PATH.name

    output_df.to_csv(csv_path, index=False)
    parquet_written = False
    if parquet_engine_available():
        output_df.to_parquet(parquet_path, index=False)
        parquet_written = True

    validation = validate_dataset(feature_df_internal, match_count=len(match_df), source_counts=source_counts, parquet_written=parquet_written)
    metadata = build_metadata(output_df, validation)
    with metadata_path.open("w", encoding="utf-8") as fh:
        json.dump(metadata, fh, ensure_ascii=False, indent=2, default=json_default)
    with validation_path.open("w", encoding="utf-8") as fh:
        json.dump(validation, fh, ensure_ascii=False, indent=2, default=json_default)

    print("Feature Builder V1 completed.")
    print(f"Status: {validation['status']}")
    print(f"Rows: {validation['row_count']}")
    print(f"Matches: {validation['match_count']}")
    print(f"Teams: {validation['team_count']}")
    print(f"Temporal leakage mismatches: {validation['temporal_leakage_validation']['mismatch_count']}")
    print(f"CSV: {csv_path}")
    print(f"Parquet: {parquet_path if parquet_written else 'not written - pyarrow/fastparquet unavailable'}")
    print(f"Metadata: {metadata_path}")
    print(f"Validation report: {validation_path}")


if __name__ == "__main__":
    main()
