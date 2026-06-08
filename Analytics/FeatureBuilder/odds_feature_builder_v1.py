"""Build Odds Features V1 from Football-Data closing odds.

Read-only PostgreSQL flow:
- reads matches_master and football_data_odds;
- uses only pre-match/closing Football-Data odds for 1X2 and Over/Under 2.5;
- excludes Asian Handicap and target columns by design;
- writes CSV, Parquet, metadata and validation report locally.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import engine  # noqa: E402

FEATURE_SET_NAME = "odds_features_v1"
FEATURE_SET_VERSION = "v1"
EXPECTED_MATCHES = 380
FAVORITE_SIDE_THRESHOLD = 0.03
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "features"
CSV_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}.csv"
PARQUET_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}.parquet"
METADATA_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}_metadata.json"
VALIDATION_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}_validation_report.json"

MARKETS_INCLUDED = ["over_under_2_5", "match_odds_1x2"]
MARKETS_BLOCKED = ["asian_handicap"]
ODDS_TYPES_INCLUDED = ["closing"]
SOURCE_TABLES = ["matches_master", "football_data_odds"]

IDENTIFIER_COLUMNS = [
    "match_id",
    "sofascore_event_id",
    "league",
    "season",
    "match_date",
    "home_team",
    "away_team",
]
AUDIT_COLUMNS = [
    "ou25_closing_bookmakers_count",
    "match_odds_closing_bookmakers_count",
    "ou25_source_columns",
    "match_odds_source_columns",
]
FEATURE_COLUMNS = [
    "odds_over25_close",
    "odds_under25_close",
    "implied_prob_over25_raw",
    "implied_prob_under25_raw",
    "implied_prob_over25_norm",
    "implied_prob_under25_norm",
    "over25_closing_strength",
    "over25_market_balance",
    "odds_home_close",
    "odds_draw_close",
    "odds_away_close",
    "implied_prob_home_raw",
    "implied_prob_draw_raw",
    "implied_prob_away_raw",
    "implied_prob_home_norm",
    "implied_prob_draw_norm",
    "implied_prob_away_norm",
    "favorite_side",
    "favorite_strength",
    "match_balance",
]
OUTPUT_COLUMNS = [*IDENTIFIER_COLUMNS, *AUDIT_COLUMNS, *FEATURE_COLUMNS]
PROBABILITY_COLUMNS = [
    "implied_prob_over25_raw",
    "implied_prob_under25_raw",
    "implied_prob_over25_norm",
    "implied_prob_under25_norm",
    "implied_prob_home_raw",
    "implied_prob_draw_raw",
    "implied_prob_away_raw",
    "implied_prob_home_norm",
    "implied_prob_draw_norm",
    "implied_prob_away_norm",
]
ODDS_COLUMNS = [
    "odds_over25_close",
    "odds_under25_close",
    "odds_home_close",
    "odds_draw_close",
    "odds_away_close",
]
RANGE_COLUMNS = [
    "implied_prob_over25_norm",
    "implied_prob_home_norm",
    "implied_prob_draw_norm",
    "implied_prob_away_norm",
    "favorite_strength",
    "match_balance",
    "over25_closing_strength",
]
TARGET_OR_FULL_MATCH_BLOCKLIST = {
    "target_late_goal_75",
    "has_late_goal",
    "late_goal_count_75",
    "home_late_goal_count_75",
    "away_late_goal_count_75",
    "home_goals",
    "away_goals",
    "total_goals",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Odds Features V1 from PostgreSQL Football-Data odds.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directory for CSV, Parquet and reports.")
    return parser.parse_args()


def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    return str(value)


def parquet_engine_available() -> bool:
    return bool(importlib.util.find_spec("pyarrow") or importlib.util.find_spec("fastparquet"))


def table_counts() -> dict[str, int]:
    tables = ["matches_master", "football_data_odds"]
    with engine.connect() as conn:
        return {table: int(conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()) for table in tables}


def fetch_matches() -> pd.DataFrame:
    sql = text(
        """
        SELECT
            match_id,
            sofascore_event_id,
            league,
            season,
            match_date,
            home_team,
            away_team
        FROM matches_master
        WHERE sofascore_event_id IS NOT NULL
        ORDER BY match_date, match_id
        """
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn)
    df["match_date"] = pd.to_datetime(df["match_date"])
    return df


def fetch_closing_odds() -> pd.DataFrame:
    sql = text(
        """
        SELECT
            match_id,
            sofascore_event_id,
            market,
            selection,
            bookmaker_or_aggregator,
            source_column,
            odds_value::float AS odds_value
        FROM football_data_odds
        WHERE market IN ('match_odds_1x2', 'over_under_2_5')
          AND odds_type = 'closing'
          AND is_closing = true
          AND is_average = false
          AND is_maximum = false
          AND odds_value > 1.0
        ORDER BY match_id, market, selection, bookmaker_or_aggregator
        """
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn)
    if df.empty:
        return pd.DataFrame(
            columns=[
                "match_id",
                "sofascore_event_id",
                "market",
                "selection",
                "bookmaker_or_aggregator",
                "source_column",
                "odds_value",
            ]
        )
    df["odds_value"] = pd.to_numeric(df["odds_value"], errors="coerce")
    return df.dropna(subset=["match_id", "market", "selection", "odds_value"])


def mean_odd(odds: pd.DataFrame, market: str, selection: str) -> pd.Series:
    subset = odds[(odds["market"] == market) & (odds["selection"] == selection)]
    if subset.empty:
        return pd.Series(dtype="float64")
    return subset.groupby("match_id")["odds_value"].mean()


def selection_counts(odds: pd.DataFrame, market: str) -> pd.Series:
    subset = odds[odds["market"] == market]
    if subset.empty:
        return pd.Series(dtype="int64")
    counts = subset.groupby(["match_id", "selection"])["bookmaker_or_aggregator"].nunique()
    return counts.groupby("match_id").min()


def source_columns(odds: pd.DataFrame, market: str) -> pd.Series:
    subset = odds[odds["market"] == market]
    if subset.empty:
        return pd.Series(dtype="object")
    return subset.groupby("match_id")["source_column"].apply(lambda values: "|".join(sorted(set(map(str, values)))))


def normalize_binary(df: pd.DataFrame, raw_a: str, raw_b: str, norm_a: str, norm_b: str) -> None:
    denom = df[raw_a] + df[raw_b]
    valid = denom.gt(0)
    df.loc[valid, norm_a] = df.loc[valid, raw_a] / denom[valid]
    df.loc[valid, norm_b] = df.loc[valid, raw_b] / denom[valid]


def normalize_three_way(df: pd.DataFrame, raw_cols: list[str], norm_cols: list[str]) -> None:
    denom = df[raw_cols].sum(axis=1, min_count=len(raw_cols))
    valid = denom.gt(0)
    for raw_col, norm_col in zip(raw_cols, norm_cols):
        df.loc[valid, norm_col] = df.loc[valid, raw_col] / denom[valid]


def calculate_favorite_side(row: pd.Series) -> str | None:
    home = row.get("implied_prob_home_norm")
    away = row.get("implied_prob_away_norm")
    if pd.isna(home) or pd.isna(away):
        return None
    diff = float(home) - float(away)
    if abs(diff) < FAVORITE_SIDE_THRESHOLD:
        return "none_clear"
    return "home" if diff > 0 else "away"


def build_feature_dataframe() -> pd.DataFrame:
    matches = fetch_matches()
    odds = fetch_closing_odds()
    df = matches.copy()

    odd_series = {
        "odds_over25_close": mean_odd(odds, "over_under_2_5", "over_2_5"),
        "odds_under25_close": mean_odd(odds, "over_under_2_5", "under_2_5"),
        "odds_home_close": mean_odd(odds, "match_odds_1x2", "home_win"),
        "odds_draw_close": mean_odd(odds, "match_odds_1x2", "draw"),
        "odds_away_close": mean_odd(odds, "match_odds_1x2", "away_win"),
        "ou25_closing_bookmakers_count": selection_counts(odds, "over_under_2_5"),
        "match_odds_closing_bookmakers_count": selection_counts(odds, "match_odds_1x2"),
        "ou25_source_columns": source_columns(odds, "over_under_2_5"),
        "match_odds_source_columns": source_columns(odds, "match_odds_1x2"),
    }
    for column, series in odd_series.items():
        df[column] = df["match_id"].map(series)

    for odds_col, prob_col in [
        ("odds_over25_close", "implied_prob_over25_raw"),
        ("odds_under25_close", "implied_prob_under25_raw"),
        ("odds_home_close", "implied_prob_home_raw"),
        ("odds_draw_close", "implied_prob_draw_raw"),
        ("odds_away_close", "implied_prob_away_raw"),
    ]:
        df[prob_col] = 1.0 / df[odds_col]

    normalize_binary(
        df,
        "implied_prob_over25_raw",
        "implied_prob_under25_raw",
        "implied_prob_over25_norm",
        "implied_prob_under25_norm",
    )
    normalize_three_way(
        df,
        ["implied_prob_home_raw", "implied_prob_draw_raw", "implied_prob_away_raw"],
        ["implied_prob_home_norm", "implied_prob_draw_norm", "implied_prob_away_norm"],
    )

    df["over25_closing_strength"] = df["implied_prob_over25_norm"] - df["implied_prob_under25_norm"]
    df["over25_market_balance"] = (df["implied_prob_over25_norm"] - df["implied_prob_under25_norm"]).abs()
    df["favorite_side"] = df.apply(calculate_favorite_side, axis=1)
    df["favorite_strength"] = (
        df[["implied_prob_home_norm", "implied_prob_away_norm"]].max(axis=1)
        - df[["implied_prob_home_norm", "implied_prob_away_norm"]].min(axis=1)
    )
    df["match_balance"] = 1 - (
        df[["implied_prob_home_norm", "implied_prob_draw_norm", "implied_prob_away_norm"]].max(axis=1)
        - df[["implied_prob_home_norm", "implied_prob_draw_norm", "implied_prob_away_norm"]].min(axis=1)
    )

    for column in OUTPUT_COLUMNS:
        if column not in df.columns:
            df[column] = None
    return df[OUTPUT_COLUMNS].sort_values(["match_date", "match_id"]).reset_index(drop=True)


def max_abs_error(series: pd.Series, expected: float) -> float | None:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return None
    return float((clean - expected).abs().max())


def range_summary(df: pd.DataFrame, columns: list[str]) -> dict[str, dict[str, float | None]]:
    summary: dict[str, dict[str, float | None]] = {}
    for column in columns:
        clean = pd.to_numeric(df[column], errors="coerce").dropna()
        summary[column] = {
            "min": float(clean.min()) if not clean.empty else None,
            "max": float(clean.max()) if not clean.empty else None,
            "mean": float(clean.mean()) if not clean.empty else None,
        }
    return summary


def validate_features(df: pd.DataFrame, parquet_written: bool) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    duplicate_match_id_rows = int(df.duplicated(subset=["match_id"]).sum())
    target_columns_present = sorted(column for column in df.columns if column.startswith("target") or "late_goal" in column)
    full_match_columns_present = sorted(column for column in TARGET_OR_FULL_MATCH_BLOCKLIST if column in df.columns)
    invalid_odds_count = int((df[ODDS_COLUMNS].le(1.0)).sum().sum())
    invalid_probability_count = int(
        ((df[PROBABILITY_COLUMNS] < 0) | (df[PROBABILITY_COLUMNS] > 1)).sum().sum()
    )
    sum_ou25 = df["implied_prob_over25_norm"] + df["implied_prob_under25_norm"]
    sum_1x2 = df["implied_prob_home_norm"] + df["implied_prob_draw_norm"] + df["implied_prob_away_norm"]
    favorite_side_expected = df.apply(calculate_favorite_side, axis=1)
    favorite_side_mismatches = int((df["favorite_side"].fillna("") != favorite_side_expected.fillna("")).sum())
    asian_handicap_columns_present = [column for column in df.columns if "handicap" in column.lower()]
    nulls_by_feature = {column: int(df[column].isna().sum()) for column in FEATURE_COLUMNS}
    coverage_ou25_count = int(df[["odds_over25_close", "odds_under25_close"]].notna().all(axis=1).sum())
    coverage_1x2_count = int(df[["odds_home_close", "odds_draw_close", "odds_away_close"]].notna().all(axis=1).sum())
    coverage_both_count = int(
        df[["odds_over25_close", "odds_under25_close", "odds_home_close", "odds_draw_close", "odds_away_close"]]
        .notna()
        .all(axis=1)
        .sum()
    )

    if len(df) != EXPECTED_MATCHES:
        errors.append(f"Expected {EXPECTED_MATCHES} rows, found {len(df)}.")
    if df["match_id"].nunique() != EXPECTED_MATCHES:
        errors.append(f"Expected {EXPECTED_MATCHES} unique match_id values, found {df['match_id'].nunique()}.")
    if duplicate_match_id_rows:
        errors.append(f"Duplicate match_id rows found: {duplicate_match_id_rows}.")
    if invalid_odds_count:
        errors.append(f"Invalid odds <= 1.0 found: {invalid_odds_count}.")
    if invalid_probability_count:
        errors.append(f"Invalid probability values outside [0, 1] found: {invalid_probability_count}.")
    if max_abs_error(sum_ou25, 1.0) is not None and max_abs_error(sum_ou25, 1.0) > 1e-9:
        errors.append("Over/Under 2.5 normalized probabilities do not sum to 1.")
    if max_abs_error(sum_1x2, 1.0) is not None and max_abs_error(sum_1x2, 1.0) > 1e-9:
        errors.append("1X2 normalized probabilities do not sum to 1.")
    if favorite_side_mismatches:
        errors.append(f"favorite_side mismatches found: {favorite_side_mismatches}.")
    if asian_handicap_columns_present:
        errors.append(f"Asian Handicap columns are present in V1 output: {asian_handicap_columns_present}.")
    if target_columns_present or full_match_columns_present:
        errors.append("Target-derived or full-match columns found in output.")
    if not parquet_written:
        errors.append("Parquet export was not created.")
    if coverage_both_count < EXPECTED_MATCHES:
        warnings.append("Some matches are missing complete V1 odds coverage.")

    return {
        "feature_set_name": FEATURE_SET_NAME,
        "feature_set_version": FEATURE_SET_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "BLOQUEADO" if errors else "APTO COM RESSALVAS" if warnings else "APTO",
        "row_count": int(len(df)),
        "expected_matches": EXPECTED_MATCHES,
        "unique_matches": int(df["match_id"].nunique()),
        "duplicate_match_id_rows": duplicate_match_id_rows,
        "coverage_1x2_count": coverage_1x2_count,
        "coverage_ou25_count": coverage_ou25_count,
        "coverage_both_count": coverage_both_count,
        "coverage_1x2_percent": round(coverage_1x2_count / EXPECTED_MATCHES * 100, 2),
        "coverage_ou25_percent": round(coverage_ou25_count / EXPECTED_MATCHES * 100, 2),
        "coverage_both_percent": round(coverage_both_count / EXPECTED_MATCHES * 100, 2),
        "invalid_odds_count": invalid_odds_count,
        "invalid_probability_count": invalid_probability_count,
        "probability_sum_1x2_max_abs_error": max_abs_error(sum_1x2, 1.0),
        "probability_sum_ou25_max_abs_error": max_abs_error(sum_ou25, 1.0),
        "favorite_side_mismatches": favorite_side_mismatches,
        "target_columns_present": target_columns_present,
        "full_match_columns_present": full_match_columns_present,
        "asian_handicap_columns_present": asian_handicap_columns_present,
        "inplay_odds_detected": False,
        "leakage_warnings": [],
        "nulls_by_feature": nulls_by_feature,
        "ranges": range_summary(df, RANGE_COLUMNS),
        "favorite_side_distribution": {
            str(key): int(value) for key, value in df["favorite_side"].value_counts(dropna=False).sort_index().to_dict().items()
        },
        "closing_bookmaker_count_summary": {
            "ou25_min": None if df["ou25_closing_bookmakers_count"].dropna().empty else int(df["ou25_closing_bookmakers_count"].min()),
            "ou25_max": None if df["ou25_closing_bookmakers_count"].dropna().empty else int(df["ou25_closing_bookmakers_count"].max()),
            "match_odds_min": None if df["match_odds_closing_bookmakers_count"].dropna().empty else int(df["match_odds_closing_bookmakers_count"].min()),
            "match_odds_max": None if df["match_odds_closing_bookmakers_count"].dropna().empty else int(df["match_odds_closing_bookmakers_count"].max()),
        },
        "anti_leakage_checks": {
            "uses_only_closing_pre_match_odds": True,
            "excludes_live_inplay_odds": True,
            "excludes_asian_handicap": not asian_handicap_columns_present,
            "excludes_target_columns": not target_columns_present,
            "excludes_full_match_columns": not full_match_columns_present,
            "does_not_join_target": True,
        },
        "validation_errors": errors,
        "validation_warnings": warnings,
    }


def build_metadata(df: pd.DataFrame, validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "dataset_name": FEATURE_SET_NAME,
        "dataset_version": FEATURE_SET_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "grain": "one row per match_id",
        "source_tables": SOURCE_TABLES,
        "source_files": [],
        "markets_included": MARKETS_INCLUDED,
        "markets_blocked": MARKETS_BLOCKED,
        "odds_types_included": ODDS_TYPES_INCLUDED,
        "row_count": int(len(df)),
        "unique_matches": int(df["match_id"].nunique()),
        "favorite_side_threshold": FAVORITE_SIDE_THRESHOLD,
        "feature_columns": FEATURE_COLUMNS,
        "audit_columns": AUDIT_COLUMNS,
        "blocked_features": [
            "handicap_line",
            "favorite_handicap",
            "handicap_implied_strength",
            "handicap_market_confidence",
            "opening_vs_closing_movement",
            "live_odds",
            "inplay_odds",
        ],
        "output_columns": list(df.columns),
        "anti_leakage_rules": [
            "Only football_data_odds rows with odds_type='closing' and is_closing=true are used.",
            "Average and maximum aggregators are excluded from primary V1 features.",
            "No live, in-play, target, final-score, full-match-statistics or Asian Handicap columns are included.",
            "The builder reads PostgreSQL only and does not write to the database.",
        ],
        "known_limitations": [
            "Football-Data closing odds do not provide individual timestamps; they are treated as pre-match closing by source semantics.",
            "Feature values are averages across available closing bookmakers, not a single bookmaker line.",
            "Average/max odds are available in storage but intentionally not used as primary V1 features.",
            "No target is included by default; downstream validation must join target explicitly.",
        ],
        "status": validation["status"],
    }


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)

    print("Building Odds Features V1")
    print(f"output_dir={output_dir}")
    print(f"table_counts={table_counts()}")

    df = build_feature_dataframe()
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / CSV_PATH.name
    parquet_path = output_dir / PARQUET_PATH.name
    df.to_csv(csv_path, index=False)
    parquet_written = False
    if parquet_engine_available():
        df.to_parquet(parquet_path, index=False)
        parquet_written = True

    validation = validate_features(df, parquet_written=parquet_written)
    metadata = build_metadata(df, validation)
    metadata_path = output_dir / METADATA_PATH.name
    validation_path = output_dir / VALIDATION_PATH.name
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")
    validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")

    outputs = {
        "csv": str(csv_path),
        "parquet": str(parquet_path) if parquet_written else None,
        "metadata": str(metadata_path),
        "validation_report": str(validation_path),
    }
    print("FINAL SUMMARY")
    print(f"rows={len(df)}")
    print(f"unique_matches={df['match_id'].nunique()}")
    print(f"coverage_1x2={validation['coverage_1x2_count']}")
    print(f"coverage_ou25={validation['coverage_ou25_count']}")
    print(f"coverage_both={validation['coverage_both_count']}")
    print(f"status={validation['status']}")
    print(f"errors={len(validation['validation_errors'])}")
    print(f"warnings={len(validation['validation_warnings'])}")
    print(json.dumps(outputs, ensure_ascii=False, indent=2))
    return 1 if validation["validation_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())