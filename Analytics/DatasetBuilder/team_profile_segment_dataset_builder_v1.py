"""Build Team Profile Segment Dataset V1.

Local, file-based flow:
- reads team_profile_segments_v1 features;
- reads late_goal_dataset_v1 only for match_id + target_late_goal_75;
- joins target explicitly by match_id;
- validates target integrity, leakage constraints and segment coverage;
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
DATASET_NAME = "team_profile_segment_dataset_v1"
DATASET_VERSION = "v1"
BUILDER_VERSION = "team_profile_segment_dataset_builder_v1"
FEATURE_SET_NAME = "team_profile_segments_v1"
SOURCE_FEATURE_PATH = PROJECT_ROOT / "data" / "processed" / "features" / "team_profile_segments_v1.csv"
SOURCE_TARGET_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_v1.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "datasets"
CSV_PATH = OUTPUT_DIR / f"{DATASET_NAME}.csv"
PARQUET_PATH = OUTPUT_DIR / f"{DATASET_NAME}.parquet"
METADATA_PATH = OUTPUT_DIR / f"{DATASET_NAME}_metadata.json"
VALIDATION_PATH = OUTPUT_DIR / f"{DATASET_NAME}_validation_report.json"
EXPECTED_ROWS = 380
TARGET_COLUMN = "target_late_goal_75"
JOIN_KEY = "match_id"
SEGMENT_COLUMNS = [
    "ofensivo_forte_vs_defesa_fragil",
    "ambos_defesa_forte",
    "defesa_fragil_vs_defesa_fragil",
    "ofensivo_forte_vs_ofensivo_forte",
    "ofensivo_fraco_vs_defesa_forte",
    "ao_menos_um_ofensivo_forte",
    "ao_menos_uma_defesa_fragil",
    "sem_ofensivo_forte_sem_defesa_fragil",
]
WHITELIST_FEATURES = [
    "home_offense_profile",
    "away_offense_profile",
    "home_defense_profile",
    "away_defense_profile",
    "home_offense_index_prior",
    "away_offense_index_prior",
    "home_defense_fragility_index_prior",
    "away_defense_fragility_index_prior",
    "home_ofensivo_strong",
    "home_ofensivo_middle",
    "home_ofensivo_weak",
    "away_ofensivo_strong",
    "away_ofensivo_middle",
    "away_ofensivo_weak",
    "home_defensivo_fragile",
    "home_defensivo_middle",
    "home_defensivo_strong",
    "away_defensivo_fragile",
    "away_defensivo_middle",
    "away_defensivo_strong",
    *SEGMENT_COLUMNS,
]
FORBIDDEN_FEATURE_COLUMNS = {
    "home_goals",
    "away_goals",
    "total_goals",
    "has_late_goal",
    "late_goal_count_75",
    "home_late_goal_count_75",
    "away_late_goal_count_75",
    "first_late_goal_minute_75",
    "last_goal_minute",
    "xg_home",
    "xg_away",
    "forecast_home",
    "forecast_draw",
    "forecast_away",
}
TARGET_DERIVED_PATTERNS = ["late_goal", "goal_after"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Team Profile Segment Dataset V1.")
    parser.add_argument("--features", default=str(SOURCE_FEATURE_PATH), help="Path to team profile segment feature CSV.")
    parser.add_argument("--target-dataset", default=str(SOURCE_TARGET_PATH), help="Path to late_goal_dataset_v1 CSV.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Output directory for dataset artifacts.")
    return parser.parse_args()


def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    return str(value)


def parquet_engine_available() -> bool:
    return bool(importlib.util.find_spec("pyarrow") or importlib.util.find_spec("fastparquet"))


def read_inputs(features_path: Path, target_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = pd.read_csv(features_path)
    target_dataset = pd.read_csv(target_path)
    required_target_cols = [JOIN_KEY, "sofascore_event_id", TARGET_COLUMN]
    missing = [column for column in required_target_cols if column not in target_dataset.columns]
    if missing:
        raise ValueError(f"Target dataset is missing required columns: {missing}")
    targets = target_dataset[required_target_cols].copy()
    return features, targets


def build_dataset(features: pd.DataFrame, targets: pd.DataFrame) -> pd.DataFrame:
    dataset = features.merge(
        targets.rename(columns={"sofascore_event_id": "target_source_sofascore_event_id"}),
        on=JOIN_KEY,
        how="left",
        validate="one_to_one",
    )
    dataset["target_joined"] = dataset[TARGET_COLUMN].notna().astype(int)
    dataset["target_source"] = "late_goal_dataset_v1"
    dataset["dataset_name"] = DATASET_NAME
    dataset["dataset_version"] = DATASET_VERSION
    dataset["dataset_builder_version"] = BUILDER_VERSION
    dataset["dataset_generated_at_utc"] = datetime.now(timezone.utc).isoformat()
    return dataset


def segment_summary(dataset: pd.DataFrame) -> dict[str, dict[str, Any]]:
    summary: dict[str, dict[str, Any]] = {}
    eligible = dataset[dataset["match_segment_eligible"].eq(1)].copy()
    for segment in SEGMENT_COLUMNS:
        seg_df = eligible[eligible[segment].eq(1)] if segment in eligible.columns else eligible.iloc[0:0]
        n = int(len(seg_df))
        positives = int(seg_df[TARGET_COLUMN].sum()) if n else 0
        summary[segment] = {
            "n": n,
            "positives": positives,
            "negatives": int(n - positives),
            "target_rate": None if n == 0 else float(positives / n),
        }
    return summary


def validate_dataset(dataset: pd.DataFrame, features: pd.DataFrame, targets: pd.DataFrame, parquet_written: bool) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    duplicate_keys = int(dataset.duplicated(subset=[JOIN_KEY]).sum())
    target_nulls = int(dataset[TARGET_COLUMN].isna().sum())
    target_joined_count = int(dataset["target_joined"].sum())
    target_counts = {str(k): int(v) for k, v in dataset[TARGET_COLUMN].value_counts(dropna=False).sort_index().to_dict().items()}
    source_target_counts = {str(k): int(v) for k, v in targets[TARGET_COLUMN].value_counts(dropna=False).sort_index().to_dict().items()}
    check = dataset[[JOIN_KEY, TARGET_COLUMN]].merge(targets[[JOIN_KEY, TARGET_COLUMN]], on=JOIN_KEY, how="left", suffixes=("_dataset", "_source"))
    target_mismatches = int((check[f"{TARGET_COLUMN}_dataset"] != check[f"{TARGET_COLUMN}_source"]).sum())
    feature_columns_for_x = [column for column in WHITELIST_FEATURES if column in dataset.columns]
    missing_whitelist = [column for column in WHITELIST_FEATURES if column not in dataset.columns]
    forbidden_present = [column for column in FORBIDDEN_FEATURE_COLUMNS if column in feature_columns_for_x]
    target_derived_features = [
        column
        for column in feature_columns_for_x
        if column.startswith("target") or any(pattern in column for pattern in TARGET_DERIVED_PATTERNS)
    ]
    full_match_columns_present = [column for column in FORBIDDEN_FEATURE_COLUMNS if column in dataset.columns]
    home_dates = pd.to_datetime(dataset["home_profile_max_match_date_used"], errors="coerce")
    away_dates = pd.to_datetime(dataset["away_profile_max_match_date_used"], errors="coerce")
    match_dates = pd.to_datetime(dataset["match_date"], errors="coerce")
    temporal_violations = int((home_dates.notna() & (home_dates >= match_dates)).sum() + (away_dates.notna() & (away_dates >= match_dates)).sum())

    if len(dataset) != EXPECTED_ROWS:
        errors.append(f"Expected {EXPECTED_ROWS} rows, found {len(dataset)}.")
    if duplicate_keys:
        errors.append(f"Duplicate match_id rows found: {duplicate_keys}.")
    if target_nulls:
        errors.append(f"Rows without joined target: {target_nulls}.")
    if target_joined_count != len(dataset):
        errors.append("Not every row has target_joined = 1.")
    if target_mismatches:
        errors.append(f"Target mismatch count after join: {target_mismatches}.")
    if missing_whitelist:
        errors.append(f"Missing whitelist features: {missing_whitelist}.")
    if forbidden_present:
        errors.append(f"Forbidden columns present in X whitelist: {forbidden_present}.")
    if target_derived_features:
        errors.append(f"Target-derived features present in X whitelist: {target_derived_features}.")
    if temporal_violations:
        errors.append(f"Temporal leakage violations found: {temporal_violations}.")
    if not parquet_written:
        errors.append("Parquet export was not created.")
    if full_match_columns_present:
        warnings.append(f"Dataset contains source/audit columns not allowed in X and must be excluded downstream: {full_match_columns_present}")
    if int(dataset["match_segment_eligible"].sum()) < int(dataset["match_profile_eligible"].sum()):
        warnings.append("Some profile-eligible matches remain unsegmentable because strict prior-date threshold pools were insufficient early in the season.")
    warnings.append("Segment classifications must be reviewed by Quant as PROMISSOR, OBSERVAR or DESCARTAR before baseline use.")
    warnings.append("Segment ambos_defesa_forte remains under Quant review.")
    status = "NAO APTO" if errors else "APTO COM RESSALVAS" if warnings else "APTO"
    return {
        "dataset_name": DATASET_NAME,
        "dataset_version": DATASET_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "row_count": int(len(dataset)),
        "expected_rows": EXPECTED_ROWS,
        "unique_matches": int(dataset[JOIN_KEY].nunique()),
        "source_feature_rows": int(len(features)),
        "source_target_rows": int(len(targets)),
        "duplicate_match_id_rows": duplicate_keys,
        "target_column": TARGET_COLUMN,
        "target_joined_count": target_joined_count,
        "target_null_count": target_nulls,
        "target_mismatch_count": target_mismatches,
        "target_counts": target_counts,
        "source_target_counts": source_target_counts,
        "match_profile_eligible_count": int(dataset["match_profile_eligible"].sum()),
        "match_segment_eligible_count": int(dataset["match_segment_eligible"].sum()),
        "match_profile_ineligible_count": int((dataset["match_profile_eligible"].eq(0)).sum()),
        "segment_summary": segment_summary(dataset),
        "feature_columns_for_x": feature_columns_for_x,
        "missing_whitelist_features": missing_whitelist,
        "target_derived_features_in_x": target_derived_features,
        "forbidden_columns_in_x": forbidden_present,
        "full_match_columns_present_in_dataset": full_match_columns_present,
        "temporal_leakage_violations": temporal_violations,
        "parquet_written": parquet_written,
        "validation_errors": errors,
        "validation_warnings": warnings,
    }


def build_metadata(dataset: pd.DataFrame, validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "dataset_name": DATASET_NAME,
        "dataset_version": DATASET_VERSION,
        "builder_version": BUILDER_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "grain": "one row per match_id",
        "source_features": str(SOURCE_FEATURE_PATH),
        "source_target_dataset": str(SOURCE_TARGET_PATH),
        "feature_set_name": FEATURE_SET_NAME,
        "target_column": TARGET_COLUMN,
        "join_key": JOIN_KEY,
        "row_count": int(len(dataset)),
        "unique_matches": int(dataset[JOIN_KEY].nunique()),
        "whitelist_features": WHITELIST_FEATURES,
        "segment_columns": SEGMENT_COLUMNS,
        "feature_columns_for_x": validation["feature_columns_for_x"],
        "anti_leakage_rules": [
            "Target is joined explicitly by match_id from late_goal_dataset_v1.",
            "Only target_late_goal_75 is added as target; it is not part of X.",
            "Whitelisted X columns exclude target-derived, final-score and full-match outcome columns.",
            "Feature profiles were generated with shift(1) before expanding calculations.",
            "No PostgreSQL writes, schema changes, crawler, importer or raw data changes are performed.",
        ],
        "validation_status": validation["status"],
        "output_files": {"csv": str(CSV_PATH), "parquet": str(PARQUET_PATH), "metadata": str(METADATA_PATH), "validation_report": str(VALIDATION_PATH)},
    }


def write_outputs(dataset: pd.DataFrame, metadata: dict[str, Any], validation: dict[str, Any], output_dir: Path) -> dict[str, str | None]:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / CSV_PATH.name
    parquet_path = output_dir / PARQUET_PATH.name
    metadata_path = output_dir / METADATA_PATH.name
    validation_path = output_dir / VALIDATION_PATH.name
    dataset.to_csv(csv_path, index=False)
    parquet_written = False
    if parquet_engine_available():
        dataset.to_parquet(parquet_path, index=False)
        parquet_written = True
    validation["parquet_written"] = parquet_written
    if not parquet_written and "Parquet export was not created." not in validation["validation_errors"]:
        validation["validation_errors"].append("Parquet export was not created.")
        validation["status"] = "NAO APTO"
    metadata["validation_status"] = validation["status"]
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")
    validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")
    return {"csv": str(csv_path), "parquet": str(parquet_path) if parquet_written else None, "metadata": str(metadata_path), "validation_report": str(validation_path)}


def main() -> int:
    args = parse_args()
    features, targets = read_inputs(Path(args.features), Path(args.target_dataset))
    dataset = build_dataset(features, targets)
    validation = validate_dataset(dataset, features, targets, parquet_written=parquet_engine_available())
    metadata = build_metadata(dataset, validation)
    outputs = write_outputs(dataset, metadata, validation, Path(args.output_dir))
    print("FINAL SUMMARY")
    print(f"rows={len(dataset)}")
    print(f"unique_matches={dataset[JOIN_KEY].nunique()}")
    print(f"target_joined={validation['target_joined_count']}")
    print(f"match_segment_eligible={validation['match_segment_eligible_count']}")
    print(f"status={validation['status']}")
    print(f"errors={len(validation['validation_errors'])}")
    print(f"warnings={len(validation['validation_warnings'])}")
    print(json.dumps(outputs, ensure_ascii=False, indent=2))
    return 1 if validation["validation_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
