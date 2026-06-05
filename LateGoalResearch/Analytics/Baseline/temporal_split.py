"""Temporal split utilities for Baseline 1."""
from __future__ import annotations
from datetime import datetime
from typing import Any
import pandas as pd
from . import baseline_config as cfg

def split_dataset(df: pd.DataFrame) -> tuple[dict[str, pd.DataFrame], dict[str, Any]]:
    ordered = df.copy()
    ordered["match_date"] = pd.to_datetime(ordered["match_date"])
    ordered = ordered.sort_values(["match_date", "match_id"]).reset_index(drop=True)
    n_rows = len(ordered)
    train_end = int(n_rows * cfg.TRAIN_RATIO)
    validation_end = train_end + int(n_rows * cfg.VALIDATION_RATIO)
    splits = {
        "train": ordered.iloc[:train_end].copy(),
        "validation": ordered.iloc[train_end:validation_end].copy(),
        "test": ordered.iloc[validation_end:].copy(),
    }
    for split_name, split_df in splits.items():
        split_df.loc[:, "split"] = split_name
    overlaps = {
        "train_validation": sorted(set(splits["train"]["match_id"]) & set(splits["validation"]["match_id"])),
        "train_test": sorted(set(splits["train"]["match_id"]) & set(splits["test"]["match_id"])),
        "validation_test": sorted(set(splits["validation"]["match_id"]) & set(splits["test"]["match_id"])),
    }
    temporal_order_valid = (
        splits["train"]["match_date"].max() <= splits["validation"]["match_date"].min()
        and splits["validation"]["match_date"].max() <= splits["test"]["match_date"].min()
    )
    split_report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "shuffle": cfg.SHUFFLE,
        "ratios": {"train": cfg.TRAIN_RATIO, "validation": cfg.VALIDATION_RATIO, "test": cfg.TEST_RATIO},
        "total_rows": int(n_rows),
        "split_counts": {name: int(len(split_df)) for name, split_df in splits.items()},
        "date_ranges": {},
        "target_distribution": {},
        "history_absent_rows": {},
        "overlaps": {key: len(value) for key, value in overlaps.items()},
        "temporal_order_valid": bool(temporal_order_valid),
    }
    for name, split_df in splits.items():
        target = split_df[cfg.TARGET_COLUMN]
        history_absent = (split_df["home_history_matches_available"] == 0) | (split_df["away_history_matches_available"] == 0)
        split_report["date_ranges"][name] = {
            "min": split_df["match_date"].min().isoformat() if len(split_df) else None,
            "max": split_df["match_date"].max().isoformat() if len(split_df) else None,
        }
        split_report["target_distribution"][name] = {
            "positive": int(target.sum()),
            "negative": int((target == 0).sum()),
            "prevalence": round(float(target.mean()), 6) if len(target) else None,
        }
        split_report["history_absent_rows"][name] = int(history_absent.sum())
    return splits, split_report
