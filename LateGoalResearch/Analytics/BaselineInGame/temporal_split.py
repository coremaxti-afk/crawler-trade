"""Temporal split utilities for Baseline In-Game V1."""
from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd

from Analytics.BaselineInGame import baseline_ingame_config as cfg


def _split_summary(frame: pd.DataFrame) -> dict[str, Any]:
    return {
        "rows": int(len(frame)),
        "date_min": None if frame.empty else frame["match_date"].min().isoformat(),
        "date_max": None if frame.empty else frame["match_date"].max().isoformat(),
        "positive": int(frame[cfg.TARGET_COLUMN].sum()),
        "negative": int((frame[cfg.TARGET_COLUMN] == 0).sum()),
        "prevalence": None if frame.empty else float(frame[cfg.TARGET_COLUMN].mean()),
    }


def split_dataset(dataset: pd.DataFrame) -> tuple[dict[str, pd.DataFrame], dict[str, Any]]:
    ordered = dataset.sort_values(["match_date", "match_id"]).reset_index(drop=True)
    total = len(ordered)
    train_end = int(total * cfg.TRAIN_RATIO)
    validation_end = train_end + int(total * cfg.VALIDATION_RATIO)

    splits = {
        "train": ordered.iloc[:train_end].copy(),
        "validation": ordered.iloc[train_end:validation_end].copy(),
        "test": ordered.iloc[validation_end:].copy(),
    }

    overlap = {
        "train_validation": len(set(splits["train"]["match_id"]) & set(splits["validation"]["match_id"])),
        "train_test": len(set(splits["train"]["match_id"]) & set(splits["test"]["match_id"])),
        "validation_test": len(set(splits["validation"]["match_id"]) & set(splits["test"]["match_id"])),
    }
    temporal_order_valid = (
        splits["train"]["match_date"].max() <= splits["validation"]["match_date"].min()
        and splits["validation"]["match_date"].max() <= splits["test"]["match_date"].min()
    )

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "shuffle": cfg.SHUFFLE,
        "ratios": {"train": cfg.TRAIN_RATIO, "validation": cfg.VALIDATION_RATIO, "test": cfg.TEST_RATIO},
        "total_rows": int(total),
        "split_counts": {name: int(len(frame)) for name, frame in splits.items()},
        "summaries": {name: _split_summary(frame) for name, frame in splits.items()},
        "overlaps": overlap,
        "temporal_order_valid": bool(temporal_order_valid),
    }
    return splits, report
