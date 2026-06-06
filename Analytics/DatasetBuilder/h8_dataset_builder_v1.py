"""Build Dataset H8 V1 with explicit target join.

Reads H8 features and Dataset V1 target, joins target_late_goal_75 by
match_id + sofascore_event_id, and writes CSV/Parquet/metadata/validation.
No database writes, no model, no baseline.
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
DATASET_NAME = "late_goal_dataset_h8_v1"
DATASET_VERSION = "h8_v1"
EXPECTED_MATCHES = 380
CUTOFFS = [60, 65, 70, 75]
EXPECTED_ROWS = EXPECTED_MATCHES * len(CUTOFFS)
KNOWN_MISSING_GRAPH_EVENT_IDS = {12437015}

FEATURE_INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "features" / "h8_features_v1.csv"
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
    "cutoff_minute",
]
COVERAGE_COLUMNS = [
    "graph_available",
    "graph_known_missing",
    "shotmap_available",
    "graph_points_until_cutoff",
    "graph_points_last_5m",
    "graph_points_last_10m",
    "shots_until_cutoff",
]
GRAPH_FEATURES = [
    "momentum_last_5m_avg",
    "momentum_last_10m_avg",
    "momentum_trend_last_10m",
    "momentum_sum_until_cutoff",
]
SHOTMAP_FEATURES = [
    "xg_last_5m",
    "xg_last_10m",
    "shots_last_5m",
    "shots_last_10m",
    "xg_sum_until_cutoff",
]
FEATURE_COLUMNS = GRAPH_FEATURES + SHOTMAP_FEATURES
TARGET_COLUMN = "target_late_goal_75"
OUTPUT_COLUMNS = [*IDENTIFIER_COLUMNS, *COVERAGE_COLUMNS, *FEATURE_COLUMNS, TARGET_COLUMN]
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Dataset H8 V1 by joining H8 features with Dataset V1 target.")
    parser.add_argument("--features", default=str(FEATURE_INPUT_PATH), help="Path to h8_features_v1.csv.")
    parser.add_argument("--target", default=str(TARGET_INPUT_PATH), help="Path to late_goal_dataset_v1.csv.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directory for dataset outputs.")
    return parser.parse_args()


def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    return str(value)


def parquet_engine_available() -> bool:
    return bool(importlib.util.find_spec("pyarrow") or importlib.util.find_spec("fastparquet"))


def load_features(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = [*IDENTIFIER_COLUMNS, *COVERAGE_COLUMNS, *FEATURE_COLUMNS]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Feature input missing required columns: {missing}")
    return df


def load_target(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = ["match_id", "sofascore_event_id", TARGET_COLUMN]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Target input missing required columns: {missing}")
    return df[required].copy()


def build_dataset(features: pd.DataFrame, target: pd.DataFrame) -> pd.DataFrame:
    df = features.merge(target, on=["match_id", "sofascore_event_id"], how="left", validate="many_to_one")
    return df[OUTPUT_COLUMNS].sort_values(["match_date", "match_id", "cutoff_minute"]).reset_index(drop=True)


def validate_dataset(df: pd.DataFrame, target: pd.DataFrame) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    cutoff_counts = {int(k): int(v) for k, v in df["cutoff_minute"].value_counts().sort_index().to_dict().items()}
    key_duplicates = int(df.duplicated(subset=["match_id", "cutoff_minute"]).sum())
    null_required = {
        column: int(df[column].isna().sum())
        for column in ["match_id", "sofascore_event_id", "match_date", "cutoff_minute", TARGET_COLUMN]
    }
    target_check = df[["match_id", "sofascore_event_id", TARGET_COLUMN]].drop_duplicates()
    target_source = target.rename(columns={TARGET_COLUMN: "source_target_late_goal_75"})
    compare = target_check.merge(target_source, on=["match_id", "sofascore_event_id"], how="left", validate="one_to_one")
    target_mismatches = int((compare[TARGET_COLUMN] != compare["source_target_late_goal_75"]).sum())
    unexpected_columns = [
        column
        for column in df.columns
        if column not in IDENTIFIER_COLUMNS + COVERAGE_COLUMNS + FEATURE_COLUMNS + [TARGET_COLUMN]
    ]
    blocked_columns_present = sorted(column for column in TARGET_DERIVED_BLOCKLIST if column in df.columns)
    known_missing = df[df["sofascore_event_id"].isin(KNOWN_MISSING_GRAPH_EVENT_IDS)]
    graph_non_null_known_missing = int(known_missing[GRAPH_FEATURES].notna().any(axis=1).sum())
    shotmap_zero_inconsistencies = int(
        ((df["shots_last_5m"] == 0) & (df["xg_last_5m"] != 0)).sum()
        + ((df["shots_last_10m"] == 0) & (df["xg_last_10m"] != 0)).sum()
    )

    if len(df) != EXPECTED_ROWS:
        errors.append(f"Expected {EXPECTED_ROWS} rows, found {len(df)}.")
    if df["match_id"].nunique() != EXPECTED_MATCHES:
        errors.append(f"Expected {EXPECTED_MATCHES} unique matches, found {df['match_id'].nunique()}.")
    if set(cutoff_counts) != set(CUTOFFS):
        errors.append("Unexpected cutoff_minute values found.")
    if any(count != EXPECTED_MATCHES for count in cutoff_counts.values()):
        errors.append("At least one cutoff does not contain 380 matches.")
    if key_duplicates:
        errors.append(f"Duplicate match_id + cutoff_minute rows found: {key_duplicates}.")
    if any(value > 0 for value in null_required.values()):
        errors.append(f"Required columns contain null values: {null_required}.")
    if target_mismatches:
        errors.append(f"Target join mismatch found in {target_mismatches} matches.")
    if unexpected_columns:
        errors.append(f"Unexpected non-whitelisted columns found: {unexpected_columns}.")
    if blocked_columns_present:
        errors.append(f"Target-derived/final-score blocklisted columns found: {blocked_columns_present}.")
    if set(known_missing["sofascore_event_id"].astype(int).unique()) != KNOWN_MISSING_GRAPH_EVENT_IDS:
        errors.append("Known missing Graph event policy was not preserved.")
    if graph_non_null_known_missing:
        errors.append("Known missing Graph rows contain Graph feature values.")
    if int(df["graph_known_missing"].sum()) != len(CUTOFFS):
        errors.append("graph_known_missing should appear once per cutoff for event_id 12437015.")
    if int(df["shotmap_available"].sum()) != EXPECTED_ROWS:
        errors.append("Shotmap availability should be preserved for all rows.")
    if shotmap_zero_inconsistencies:
        errors.append(f"Shotmap zero preservation failed in {shotmap_zero_inconsistencies} rows.")

    warnings.append("Dataset H8 V1 includes the target column for supervised analysis; X must use only FEATURE_COLUMNS.")
    warnings.append("Graph features are null for known_missing event_id 12437015 and require explicit downstream handling.")

    return {
        "dataset_name": DATASET_NAME,
        "dataset_version": DATASET_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "NAO APTO" if errors else "APTO COM RESSALVAS" if warnings else "APTO",
        "row_count": int(len(df)),
        "expected_rows": EXPECTED_ROWS,
        "unique_matches": int(df["match_id"].nunique()),
        "cutoffs": CUTOFFS,
        "cutoff_counts": cutoff_counts,
        "key_duplicates": key_duplicates,
        "target_column": TARGET_COLUMN,
        "target_counts": {str(k): int(v) for k, v in df[TARGET_COLUMN].value_counts(dropna=False).sort_index().to_dict().items()},
        "target_mismatches": target_mismatches,
        "graph_known_missing_event_ids": sorted(KNOWN_MISSING_GRAPH_EVENT_IDS),
        "graph_known_missing_rows": int(df["graph_known_missing"].sum()),
        "shotmap_available_rows": int(df["shotmap_available"].sum()),
        "shotmap_zero_inconsistencies": shotmap_zero_inconsistencies,
        "feature_columns_for_x": FEATURE_COLUMNS,
        "coverage_columns_not_for_x": COVERAGE_COLUMNS,
        "blocked_columns_present": blocked_columns_present,
        "unexpected_columns": unexpected_columns,
        "anti_leakage_checks": {
            "target_join_explicit": True,
            "uses_only_precomputed_h8_features": True,
            "feature_whitelist_enforced": not unexpected_columns,
            "no_target_derived_columns_in_x": not blocked_columns_present and TARGET_COLUMN not in FEATURE_COLUMNS,
            "no_final_score_columns": not bool({"home_goals", "away_goals", "total_goals"} & set(df.columns)),
            "graph_known_missing_preserved": not graph_non_null_known_missing,
            "shotmap_zeros_preserved": shotmap_zero_inconsistencies == 0,
        },
        "errors": errors,
        "warnings": warnings,
    }


def build_metadata(df: pd.DataFrame, validation: dict[str, Any], features_path: Path, target_path: Path) -> dict[str, Any]:
    return {
        "dataset_name": DATASET_NAME,
        "dataset_version": DATASET_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "grain": "one row per match_id + cutoff_minute",
        "input_features": str(features_path),
        "input_target": str(target_path),
        "row_count": int(len(df)),
        "unique_matches": int(df["match_id"].nunique()),
        "cutoffs": CUTOFFS,
        "target_column": TARGET_COLUMN,
        "feature_columns_for_x": FEATURE_COLUMNS,
        "identifier_columns": IDENTIFIER_COLUMNS,
        "coverage_columns_not_for_x": COVERAGE_COLUMNS,
        "known_missing_graph_event_ids": sorted(KNOWN_MISSING_GRAPH_EVENT_IDS),
        "output_columns": list(df.columns),
        "validation_status": validation["status"],
        "anti_leakage_rules": [
            "Target is joined explicitly from late_goal_dataset_v1 by match_id + sofascore_event_id.",
            "X must use only feature_columns_for_x.",
            "Coverage columns are audit fields and are not part of X by default.",
            "No late-goal count, final-score or target-derived columns are included as features.",
            "H8 features are inherited from h8_features_v1, which uses only minute <= cutoff.",
        ],
    }


def write_outputs(df: pd.DataFrame, validation: dict[str, Any], metadata: dict[str, Any], output_dir: Path) -> dict[str, str | None]:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / CSV_PATH.name
    parquet_path = output_dir / PARQUET_PATH.name
    metadata_path = output_dir / METADATA_PATH.name
    validation_path = output_dir / VALIDATION_PATH.name
    df.to_csv(csv_path, index=False)
    parquet_written = False
    if parquet_engine_available():
        df.to_parquet(parquet_path, index=False)
        parquet_written = True
    else:
        validation.setdefault("warnings", []).append("Parquet not written because pyarrow/fastparquet is unavailable.")
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")
    validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")
    return {
        "csv": str(csv_path),
        "parquet": str(parquet_path) if parquet_written else None,
        "metadata": str(metadata_path),
        "validation_report": str(validation_path),
    }


def main() -> int:
    args = parse_args()
    features_path = Path(args.features)
    target_path = Path(args.target)
    output_dir = Path(args.output_dir)
    print("Building Dataset H8 V1")
    print(f"features={features_path}")
    print(f"target={target_path}")
    print(f"output_dir={output_dir}")
    features = load_features(features_path)
    target = load_target(target_path)
    df = build_dataset(features, target)
    validation = validate_dataset(df, target)
    metadata = build_metadata(df, validation, features_path, target_path)
    outputs = write_outputs(df, validation, metadata, output_dir)
    print("FINAL SUMMARY")
    print(f"rows={len(df)}")
    print(f"unique_matches={df['match_id'].nunique()}")
    print(f"cutoffs={sorted(df['cutoff_minute'].unique().tolist())}")
    print(f"status={validation['status']}")
    print(f"errors={len(validation['errors'])}")
    print(f"warnings={len(validation['warnings'])}")
    print(json.dumps(outputs, ensure_ascii=False, indent=2))
    return 1 if validation["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
