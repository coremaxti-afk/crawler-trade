"""Build the Baseline 1 match-level dataset from approved pre-match features."""
from __future__ import annotations
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any
import pandas as pd
from . import baseline_config as cfg

def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    return str(value)

def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def validate_input_files() -> None:
    required_paths = [cfg.FEATURE_INPUT_PATH, cfg.FEATURE_METADATA_PATH, cfg.FEATURE_VALIDATION_PATH, cfg.DATASET_INPUT_PATH, cfg.DATASET_METADATA_PATH, cfg.DATASET_VALIDATION_PATH]
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required input files: {missing}")

def validate_source_reports() -> dict[str, Any]:
    feature_validation = read_json(cfg.FEATURE_VALIDATION_PATH)
    dataset_validation = read_json(cfg.DATASET_VALIDATION_PATH)
    feature_status = feature_validation.get("status")
    dataset_status = dataset_validation.get("status")
    if feature_status not in {"APTO", "APTO COM RESSALVAS"}:
        raise ValueError(f"Feature validation status is not approved: {feature_status}")
    if dataset_status not in {"APTO", "APTO COM RESSALVAS"}:
        raise ValueError(f"Dataset validation status is not approved: {dataset_status}")
    return {"feature_validation": feature_validation, "dataset_validation": dataset_validation}

def prefix_columns(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    keep = ["match_id", "team_name", "opponent_team", "history_matches_available", "is_early_season", *cfg.ALLOWED_TEAM_LEVEL_FEATURES]
    renamed = df[keep].copy()
    rename_map = {"team_name": f"{prefix}_team_from_features", "opponent_team": f"{prefix}_opponent_from_features", "history_matches_available": f"{prefix}_history_matches_available", "is_early_season": f"{prefix}_is_early_season"}
    rename_map.update({feature: f"{prefix}_{feature}" for feature in cfg.ALLOWED_TEAM_LEVEL_FEATURES})
    return renamed.rename(columns=rename_map)

def audit_removed_columns(all_columns: list[str], final_columns: list[str]) -> list[dict[str, str]]:
    final_set = set(final_columns)
    removed = []
    for column in all_columns:
        if column in final_set:
            continue
        lower = column.lower()
        if column == cfg.TARGET_COLUMN:
            reason = "target column, excluded from X"
        elif any(pattern in lower for pattern in ["target", "late_goal", "has_late_goal"]):
            reason = "target-derived or target-adjacent column"
        elif column in cfg.OPTIONAL_DIFF_FEATURES_1B:
            reason = "Baseline 1B optional feature not authorized for this run"
        elif column in cfg.IDENTIFIER_COLUMNS or column.endswith("_team_from_features") or column.endswith("_opponent_from_features"):
            reason = "identifier or audit column, not predictive X"
        else:
            reason = "not in official Baseline 1A whitelist"
        removed.append({"column": column, "reason": reason})
    return removed

def forbidden_scan(selected_features: list[str]) -> list[dict[str, str]]:
    findings = []
    for column in selected_features:
        lower = column.lower()
        matched = [pattern for pattern in cfg.FORBIDDEN_FEATURE_PATTERNS if pattern in lower]
        if matched:
            findings.append({"column": column, "matched_patterns": ", ".join(matched), "resolution": "allowed because official whitelist prevails and feature is historical pre-match"})
    return findings

def build_baseline_dataset() -> tuple[pd.DataFrame, dict[str, Any]]:
    validate_input_files()
    source_reports = validate_source_reports()
    features = pd.read_csv(cfg.FEATURE_INPUT_PATH)
    dataset = pd.read_csv(cfg.DATASET_INPUT_PATH)
    required_feature_columns = ["match_id", "is_home", "team_name", "opponent_team", "history_matches_available", "is_early_season", *cfg.ALLOWED_TEAM_LEVEL_FEATURES]
    missing_feature_columns = [column for column in required_feature_columns if column not in features.columns]
    if missing_feature_columns:
        raise ValueError(f"Missing required feature columns: {missing_feature_columns}")
    required_dataset_columns = ["match_id", "sofascore_event_id", "league", "season", "match_date", "home_team", "away_team", cfg.TARGET_COLUMN]
    missing_dataset_columns = [column for column in required_dataset_columns if column not in dataset.columns]
    if missing_dataset_columns:
        raise ValueError(f"Missing required dataset columns: {missing_dataset_columns}")
    rows_per_match = features.groupby("match_id").size()
    invalid_match_rows = rows_per_match[rows_per_match != 2]
    if len(invalid_match_rows):
        raise ValueError(f"Feature set must have exactly 2 rows per match. Invalid matches: {invalid_match_rows.head(10).to_dict()}")
    home = features[features["is_home"].astype(int) == 1].copy()
    away = features[features["is_home"].astype(int) == 0].copy()
    if home["match_id"].duplicated().any():
        raise ValueError("Duplicate home rows found for at least one match_id.")
    if away["match_id"].duplicated().any():
        raise ValueError("Duplicate away rows found for at least one match_id.")
    home_prefixed = prefix_columns(home, "home")
    away_prefixed = prefix_columns(away, "away")
    match_level = dataset[required_dataset_columns].merge(home_prefixed, on="match_id", how="inner", validate="one_to_one")
    match_level = match_level.merge(away_prefixed, on="match_id", how="inner", validate="one_to_one")
    match_level["match_date"] = pd.to_datetime(match_level["match_date"])
    match_level = match_level.sort_values(["match_date", "match_id"]).reset_index(drop=True)
    if match_level["match_id"].duplicated().any():
        raise ValueError("Final baseline dataset has duplicate match_id rows.")
    if match_level[cfg.TARGET_COLUMN].isna().any():
        raise ValueError("Target contains null values after join.")
    final_columns = [*cfg.IDENTIFIER_COLUMNS, *cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A, cfg.TARGET_COLUMN]
    baseline_df = match_level[final_columns].copy()
    manifest = {
        "baseline_name": cfg.BASELINE_NAME,
        "baseline_version": cfg.BASELINE_VERSION,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input_files": {"features": str(cfg.FEATURE_INPUT_PATH), "feature_metadata": str(cfg.FEATURE_METADATA_PATH), "feature_validation": str(cfg.FEATURE_VALIDATION_PATH), "dataset": str(cfg.DATASET_INPUT_PATH), "dataset_metadata": str(cfg.DATASET_METADATA_PATH), "dataset_validation": str(cfg.DATASET_VALIDATION_PATH)},
        "source_status": {"feature_validation_status": source_reports["feature_validation"].get("status"), "feature_temporal_leakage_mismatches": source_reports["feature_validation"].get("temporal_leakage_validation", {}).get("mismatch_count"), "dataset_validation_status": source_reports["dataset_validation"].get("status")},
        "grain": "one row per match",
        "source_team_level_rows": int(len(features)),
        "output_match_level_rows": int(len(baseline_df)),
        "target": cfg.TARGET_COLUMN,
        "official_whitelist_precedence": True,
        "allowed_team_level_features": cfg.ALLOWED_TEAM_LEVEL_FEATURES,
        "x_columns": cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A,
        "forbidden_patterns_checked": cfg.FORBIDDEN_FEATURE_PATTERNS,
        "forbidden_scan_findings_on_x": forbidden_scan(cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A),
        "removed_columns": audit_removed_columns(list(match_level.columns), final_columns),
        "validations": {"feature_rows_per_match_all_equal_2": bool((rows_per_match == 2).all()), "one_home_row_per_match": bool(len(home) == features["match_id"].nunique()), "one_away_row_per_match": bool(len(away) == features["match_id"].nunique()), "match_id_unique_after_conversion": bool(not baseline_df["match_id"].duplicated().any()), "target_null_count": int(baseline_df[cfg.TARGET_COLUMN].isna().sum()), "all_x_columns_from_whitelist": True},
    }
    return baseline_df, manifest
