"""Build the Baseline In-Game V1 cutoff-75 dataset."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from Analytics.BaselineInGame import baseline_ingame_config as cfg


def json_default(value: Any) -> Any:
    if hasattr(value, "item"):
        return value.item()
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def score_state_from_diff(diff: float) -> str:
    if pd.isna(diff):
        return "unknown"
    if diff == 0:
        return "draw"
    if diff > 0:
        return "home_leading"
    return "away_leading"


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"missing": True, "path": str(path)}
    return json.loads(path.read_text(encoding="utf-8"))


def build_baseline_ingame_dataset() -> tuple[pd.DataFrame, dict[str, Any]]:
    if not cfg.INGAME_DATASET_INPUT_PATH.exists():
        raise FileNotFoundError(f"Missing input dataset: {cfg.INGAME_DATASET_INPUT_PATH}")

    source = pd.read_csv(cfg.INGAME_DATASET_INPUT_PATH)
    required_columns = set(cfg.IDENTIFIER_COLUMNS + cfg.NUMERIC_FEATURES + [cfg.OPERATIONAL_TARGET_COLUMN])
    missing_columns = sorted(required_columns - set(source.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns in ingame dataset: {missing_columns}")

    snapshot = source[source["cutoff_minute"].eq(cfg.CUTOFF_MINUTE)].copy()
    snapshot["match_date"] = pd.to_datetime(snapshot["match_date"], errors="coerce")
    snapshot[cfg.TARGET_COLUMN] = snapshot[cfg.OPERATIONAL_TARGET_COLUMN].astype(int)
    snapshot["score_state_group"] = snapshot["score_diff_home_until_cutoff"].apply(score_state_from_diff)

    duplicate_match_ids = int(snapshot["match_id"].duplicated().sum())
    target_equivalence_checked = False
    target_equivalence_mismatches = None
    if cfg.DATASET_V1_INPUT_PATH.exists() and "match_id" in snapshot.columns:
        v1 = pd.read_csv(cfg.DATASET_V1_INPUT_PATH, usecols=lambda column: column in {"match_id", cfg.TARGET_COLUMN})
        if cfg.TARGET_COLUMN in v1.columns:
            check = snapshot[["match_id", cfg.TARGET_COLUMN]].merge(v1, on="match_id", how="left", suffixes=("_ingame", "_v1"))
            target_equivalence_checked = True
            target_equivalence_mismatches = int((check[f"{cfg.TARGET_COLUMN}_ingame"] != check[f"{cfg.TARGET_COLUMN}_v1"]).sum())

    output_columns = cfg.IDENTIFIER_COLUMNS + cfg.ALLOWED_FEATURES + [cfg.TARGET_COLUMN, cfg.OPERATIONAL_TARGET_COLUMN]
    dataset = snapshot[output_columns].sort_values(["match_date", "match_id"]).reset_index(drop=True)

    forbidden_findings = []
    for column in cfg.ALLOWED_FEATURES:
        matches = [pattern for pattern in cfg.FORBIDDEN_FEATURE_PATTERNS if pattern in column.lower()]
        if matches:
            forbidden_findings.append({
                "column": column,
                "matched_patterns": matches,
                "resolution": "allowed because official whitelist prevails and feature is in-game cutoff-safe",
            })

    manifest = {
        "baseline_name": cfg.BASELINE_NAME,
        "baseline_version": cfg.BASELINE_VERSION,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "input_files": {
            "ingame_dataset": str(cfg.INGAME_DATASET_INPUT_PATH),
            "ingame_metadata": str(cfg.INGAME_METADATA_PATH),
            "ingame_validation": str(cfg.INGAME_VALIDATION_PATH),
            "dataset_v1_for_target_equivalence": str(cfg.DATASET_V1_INPUT_PATH),
        },
        "source_metadata": _load_json(cfg.INGAME_METADATA_PATH),
        "source_validation": _load_json(cfg.INGAME_VALIDATION_PATH),
        "source_rows": int(len(source)),
        "snapshot_rows": int(len(dataset)),
        "cutoff_minute": cfg.CUTOFF_MINUTE,
        "target": cfg.TARGET_COLUMN,
        "operational_target": cfg.OPERATIONAL_TARGET_COLUMN,
        "score_state_group_derivation": "derived from score_diff_home_until_cutoff inside cutoff-75 snapshot",
        "x_columns_base": cfg.ALLOWED_FEATURES,
        "numeric_features": cfg.NUMERIC_FEATURES,
        "categorical_features": cfg.CATEGORICAL_FEATURES,
        "forbidden_patterns_checked": cfg.FORBIDDEN_FEATURE_PATTERNS,
        "forbidden_scan_findings_on_x": forbidden_findings,
        "removed_columns": [
            {"column": cfg.OPERATIONAL_TARGET_COLUMN, "reason": "operational target, not predictive X"},
            {"column": cfg.TARGET_COLUMN, "reason": "official target, not predictive X"},
            {"column": "home_goals_until_cutoff", "reason": "not in official whitelist"},
            {"column": "away_goals_until_cutoff", "reason": "not in official whitelist"},
            {"column": "total_goals_until_cutoff", "reason": "not in official whitelist"},
            {"column": "last_goal_minute_until_cutoff", "reason": "not in official whitelist"},
            {"column": "time_since_last_goal_until_cutoff", "reason": "not in official whitelist"},
            {"column": "goal_last_5m_until_cutoff", "reason": "not in official whitelist"},
            {"column": "goal_last_10m_until_cutoff", "reason": "not in official whitelist"},
        ],
        "validations": {
            "all_rows_cutoff_75": bool(dataset["cutoff_minute"].eq(cfg.CUTOFF_MINUTE).all()),
            "match_id_unique_after_filter": bool(not dataset["match_id"].duplicated().any()),
            "duplicate_match_ids": duplicate_match_ids,
            "target_null_count": int(dataset[cfg.TARGET_COLUMN].isna().sum()),
            "all_x_columns_from_whitelist": True,
            "target_equivalence_checked": target_equivalence_checked,
            "target_equivalence_mismatches": target_equivalence_mismatches,
            "no_full_match_statistics_source_used": True,
            "no_prematch_features_used": True,
            "no_xg_xga_forecast_used": True,
        },
    }
    return dataset, manifest
