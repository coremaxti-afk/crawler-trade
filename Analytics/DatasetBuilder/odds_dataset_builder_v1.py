"""Build Dataset Odds V1 with explicit target join.

Local file flow:
- reads Odds Feature Builder V1 output;
- verifies the Odds Feature Builder validation report is APTO;
- joins target_late_goal_75 explicitly by match_id + sofascore_event_id;
- validates whitelist, anti-leakage and coverage;
- writes CSV, Parquet, metadata and validation report.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATASET_NAME = "late_goal_dataset_odds_v1"
DATASET_VERSION = "odds_v1"
EXPECTED_MATCHES = 380

FEATURE_INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "features" / "odds_features_v1.csv"
FEATURE_VALIDATION_PATH = PROJECT_ROOT / "data" / "processed" / "features" / "odds_features_v1_validation_report.json"
TARGET_INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_v1.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "datasets"
CSV_PATH = OUTPUT_DIR / f"{DATASET_NAME}.csv"
PARQUET_PATH = OUTPUT_DIR / f"{DATASET_NAME}.parquet"
METADATA_PATH = OUTPUT_DIR / f"{DATASET_NAME}_metadata.json"
VALIDATION_PATH = OUTPUT_DIR / f"{DATASET_NAME}_validation_report.json"

IDENTIFIER_COLUMNS = [
    "match_id",
    "sofascore_event_id",
    "league",
    "season",
    "match_date",
    "home_team",
    "away_team",
]
ODDS_FEATURE_COLUMNS = [
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
AUDIT_COLUMNS_NOT_FOR_X = [
    "ou25_closing_bookmakers_count",
    "match_odds_closing_bookmakers_count",
    "ou25_source_columns",
    "match_odds_source_columns",
]
TARGET_COLUMN = "target_late_goal_75"
OUTPUT_COLUMNS = [*IDENTIFIER_COLUMNS, *ODDS_FEATURE_COLUMNS, TARGET_COLUMN]
TARGET_DERIVED_BLOCKLIST = {
    "has_late_goal",
    "late_goal_count_75",
    "home_late_goal_count_75",
    "away_late_goal_count_75",
    "first_late_goal_minute_75",
    "home_goals",
    "away_goals",
    "total_goals",
}
ASIAN_HANDICAP_PATTERNS = ["handicap", "asian"]
LIVE_INPLAY_PATTERNS = ["live", "inplay", "in_play"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Dataset Odds V1 by joining odds features with Dataset V1 target.")
    parser.add_argument("--features", default=str(FEATURE_INPUT_PATH), help="Path to odds_features_v1.csv.")
    parser.add_argument("--feature-validation", default=str(FEATURE_VALIDATION_PATH), help="Path to odds_features_v1_validation_report.json.")
    parser.add_argument("--target", default=str(TARGET_INPUT_PATH), help="Path to late_goal_dataset_v1.csv.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directory for dataset outputs.")
    return parser.parse_args()


def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    return str(value)


def parquet_engine_available() -> bool:
    return bool(importlib.util.find_spec("pyarrow") or importlib.util.find_spec("fastparquet"))


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_features(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = [*IDENTIFIER_COLUMNS, *ODDS_FEATURE_COLUMNS]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Odds feature input missing required columns: {missing}")
    return df


def load_target(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = ["match_id", "sofascore_event_id", TARGET_COLUMN]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Target input missing required columns: {missing}")
    return df[required].copy()


def build_dataset(features: pd.DataFrame, target: pd.DataFrame) -> pd.DataFrame:
    df = features[[*IDENTIFIER_COLUMNS, *ODDS_FEATURE_COLUMNS]].copy()
    df = df.merge(target, on=["match_id", "sofascore_event_id"], how="left", validate="one_to_one")
    for column in OUTPUT_COLUMNS:
        if column not in df.columns:
            df[column] = None
    return df[OUTPUT_COLUMNS].sort_values(["match_date", "match_id"]).reset_index(drop=True)


def probability_sum_error(df: pd.DataFrame, columns: list[str]) -> float | None:
    sums = df[columns].sum(axis=1, min_count=len(columns)).dropna()
    if sums.empty:
        return None
    return float((sums - 1.0).abs().max())


def validate_dataset(df: pd.DataFrame, target: pd.DataFrame, feature_validation: dict[str, Any], parquet_written: bool) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    duplicate_match_id_rows = int(df.duplicated(subset=["match_id"]).sum())
    null_required = {column: int(df[column].isna().sum()) for column in ["match_id", "sofascore_event_id", "match_date", TARGET_COLUMN]}
    target_check = df[["match_id", "sofascore_event_id", TARGET_COLUMN]].drop_duplicates()
    target_source = target.rename(columns={TARGET_COLUMN: "source_target_late_goal_75"})
    target_compare = target_check.merge(target_source, on=["match_id", "sofascore_event_id"], how="left", validate="one_to_one")
    target_mismatches = int((target_compare[TARGET_COLUMN] != target_compare["source_target_late_goal_75"]).sum())
    blocked_columns_present = sorted(column for column in TARGET_DERIVED_BLOCKLIST if column in df.columns)
    asian_handicap_columns_present = sorted(column for column in df.columns if any(pattern in column.lower() for pattern in ASIAN_HANDICAP_PATTERNS))
    live_inplay_columns_present = sorted(column for column in df.columns if any(pattern in column.lower() for pattern in LIVE_INPLAY_PATTERNS))
    unexpected_columns = [column for column in df.columns if column not in OUTPUT_COLUMNS]
    target_columns_in_x = sorted(column for column in ODDS_FEATURE_COLUMNS if column.startswith("target") or "late_goal" in column)
    invalid_odds_count = int((df[["odds_over25_close", "odds_under25_close", "odds_home_close", "odds_draw_close", "odds_away_close"]].le(1.0)).sum().sum())
    probability_columns = [
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
    invalid_probability_count = int(((df[probability_columns] < 0) | (df[probability_columns] > 1)).sum().sum())
    probability_sum_ou25_max_abs_error = probability_sum_error(df, ["implied_prob_over25_norm", "implied_prob_under25_norm"])
    probability_sum_1x2_max_abs_error = probability_sum_error(df, ["implied_prob_home_norm", "implied_prob_draw_norm", "implied_prob_away_norm"])
    target_values = sorted(df[TARGET_COLUMN].dropna().unique().tolist())

    if feature_validation.get("status") != "APTO":
        errors.append(f"Odds Feature Builder validation status is not APTO: {feature_validation.get('status')}.")
    if len(df) != EXPECTED_MATCHES:
        errors.append(f"Expected {EXPECTED_MATCHES} rows, found {len(df)}.")
    if df["match_id"].nunique() != EXPECTED_MATCHES:
        errors.append(f"Expected {EXPECTED_MATCHES} unique matches, found {df['match_id'].nunique()}.")
    if duplicate_match_id_rows:
        errors.append(f"Duplicate match_id rows found: {duplicate_match_id_rows}.")
    if any(value > 0 for value in null_required.values()):
        errors.append(f"Required columns contain null values: {null_required}.")
    if target_mismatches:
        errors.append(f"Target join mismatch found in {target_mismatches} matches.")
    if target_values != [0, 1]:
        errors.append(f"Unexpected target values: {target_values}.")
    if unexpected_columns:
        errors.append(f"Unexpected non-whitelisted columns found: {unexpected_columns}.")
    if blocked_columns_present:
        errors.append(f"Target-derived/final-score blocklisted columns found: {blocked_columns_present}.")
    if target_columns_in_x:
        errors.append(f"Target-like columns found in X whitelist: {target_columns_in_x}.")
    if asian_handicap_columns_present:
        errors.append(f"Asian Handicap columns are present: {asian_handicap_columns_present}.")
    if live_inplay_columns_present:
        errors.append(f"Live/in-play columns are present: {live_inplay_columns_present}.")
    if invalid_odds_count:
        errors.append(f"Invalid odds <= 1.0 found: {invalid_odds_count}.")
    if invalid_probability_count:
        errors.append(f"Invalid probability values outside [0, 1] found: {invalid_probability_count}.")
    if probability_sum_ou25_max_abs_error is not None and probability_sum_ou25_max_abs_error > 1e-9:
        errors.append("Over/Under 2.5 normalized probabilities do not sum to 1.")
    if probability_sum_1x2_max_abs_error is not None and probability_sum_1x2_max_abs_error > 1e-9:
        errors.append("1X2 normalized probabilities do not sum to 1.")
    if not parquet_written:
        errors.append("Parquet export was not created.")

    warnings.append("Dataset Odds V1 includes the target column for supervised validation; X must use only odds_feature_columns.")
    warnings.append("Football-Data closing odds do not include individual timestamps; source semantics are treated as pre-match closing.")

    return {
        "dataset_name": DATASET_NAME,
        "dataset_version": DATASET_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "NAO APTO" if errors else "APTO COM RESSALVAS" if warnings else "APTO",
        "row_count": int(len(df)),
        "expected_rows": EXPECTED_MATCHES,
        "unique_matches": int(df["match_id"].nunique()),
        "duplicate_match_id_rows": duplicate_match_id_rows,
        "target_column": TARGET_COLUMN,
        "target_counts": {str(key): int(value) for key, value in df[TARGET_COLUMN].value_counts(dropna=False).sort_index().to_dict().items()},
        "target_mismatches": target_mismatches,
        "null_required": null_required,
        "feature_columns_for_x": ODDS_FEATURE_COLUMNS,
        "audit_columns_not_for_x": AUDIT_COLUMNS_NOT_FOR_X,
        "blocked_columns_present": blocked_columns_present,
        "asian_handicap_columns_present": asian_handicap_columns_present,
        "live_inplay_columns_present": live_inplay_columns_present,
        "unexpected_columns": unexpected_columns,
        "invalid_odds_count": invalid_odds_count,
        "invalid_probability_count": invalid_probability_count,
        "probability_sum_1x2_max_abs_error": probability_sum_1x2_max_abs_error,
        "probability_sum_ou25_max_abs_error": probability_sum_ou25_max_abs_error,
        "source_feature_validation_status": feature_validation.get("status"),
        "anti_leakage_checks": {
            "target_join_explicit": True,
            "features_source_apto": feature_validation.get("status") == "APTO",
            "feature_whitelist_enforced": not unexpected_columns,
            "no_target_derived_columns_in_x": not target_columns_in_x and TARGET_COLUMN not in ODDS_FEATURE_COLUMNS,
            "no_final_score_columns": not bool({"home_goals", "away_goals", "total_goals"} & set(df.columns)),
            "no_asian_handicap": not asian_handicap_columns_present,
            "no_live_inplay_odds": not live_inplay_columns_present,
            "no_full_match_columns": not blocked_columns_present,
        },
        "errors": errors,
        "warnings": warnings,
    }


def build_metadata(df: pd.DataFrame, validation: dict[str, Any], features_path: Path, target_path: Path, feature_validation_path: Path) -> dict[str, Any]:
    return {
        "dataset_name": DATASET_NAME,
        "dataset_version": DATASET_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "grain": "one row per match_id",
        "input_features": str(features_path),
        "input_feature_validation": str(feature_validation_path),
        "input_target": str(target_path),
        "row_count": int(len(df)),
        "unique_matches": int(df["match_id"].nunique()),
        "target_column": TARGET_COLUMN,
        "feature_columns_for_x": ODDS_FEATURE_COLUMNS,
        "identifier_columns": IDENTIFIER_COLUMNS,
        "audit_columns_not_for_x": AUDIT_COLUMNS_NOT_FOR_X,
        "output_columns": list(df.columns),
        "validation_status": validation["status"],
        "anti_leakage_rules": [
            "Target is joined explicitly from late_goal_dataset_v1 by match_id + sofascore_event_id.",
            "X must use only feature_columns_for_x.",
            "No target-derived, final-score, full-match, live/in-play or Asian Handicap columns are included in X.",
            "Odds features are inherited from odds_features_v1, which uses only Football-Data closing odds.",
            "The dataset builder is file-based and does not read or write PostgreSQL.",
        ],
        "known_limitations": [
            "Football-Data closing odds do not provide individual timestamps; source semantics are treated as pre-match closing.",
            "Dataset contains target_late_goal_75 for validation; downstream modeling remains unauthorized.",
            "No imputation is performed at dataset creation time.",
        ],
    }


def main() -> int:
    args = parse_args()
    features_path = Path(args.features)
    feature_validation_path = Path(args.feature_validation)
    target_path = Path(args.target)
    output_dir = Path(args.output_dir)

    print("Building Dataset Odds V1")
    print(f"features={features_path}")
    print(f"feature_validation={feature_validation_path}")
    print(f"target={target_path}")
    print(f"output_dir={output_dir}")

    features = load_features(features_path)
    target = load_target(target_path)
    feature_validation = load_json(feature_validation_path)
    df = build_dataset(features, target)
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / CSV_PATH.name
    parquet_path = output_dir / PARQUET_PATH.name
    df.to_csv(csv_path, index=False)
    parquet_written = False
    if parquet_engine_available():
        df.to_parquet(parquet_path, index=False)
        parquet_written = True

    validation = validate_dataset(df, target, feature_validation, parquet_written=parquet_written)
    metadata = build_metadata(df, validation, features_path, target_path, feature_validation_path)
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
    print(f"target_counts={validation['target_counts']}")
    print(f"status={validation['status']}")
    print(f"errors={len(validation['errors'])}")
    print(f"warnings={len(validation['warnings'])}")
    print(json.dumps(outputs, ensure_ascii=False, indent=2))
    return 1 if validation["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
