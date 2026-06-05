"""Train-only median imputation for Baseline 1."""
from __future__ import annotations
from datetime import datetime
from typing import Any
import pandas as pd
from . import baseline_config as cfg

def fit_transform_impute(splits: dict[str, pd.DataFrame]) -> tuple[dict[str, pd.DataFrame], dict[str, Any]]:
    train = splits["train"]
    medians = train[cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A].median(numeric_only=True).to_dict()
    before = {}
    after = {}
    imputed_counts = {}
    transformed = {}
    for name, split_df in splits.items():
        work = split_df.copy()
        before[name] = {column: int(work[column].isna().sum()) for column in cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A}
        for column, median in medians.items():
            work[column] = work[column].fillna(median)
        after[name] = {column: int(work[column].isna().sum()) for column in cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A}
        imputed_counts[name] = {column: before[name][column] - after[name][column] for column in cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A}
        transformed[name] = work
    warnings = []
    for name, counts in imputed_counts.items():
        split_size = max(len(transformed[name]), 1)
        for column, count in counts.items():
            if count / split_size > 0.10:
                warnings.append(f"{name}:{column} imputed above 10% ({count}/{split_size}).")
    if any(value > 0 for counts in after.values() for value in counts.values()):
        raise ValueError("At least one feature remains null after train-median imputation.")
    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "method": "median fitted on train only",
        "fit_split": "train",
        "medians": {key: None if pd.isna(value) else float(value) for key, value in medians.items()},
        "nulls_before": before,
        "nulls_after": after,
        "imputed_counts": imputed_counts,
        "history_absent_rows": {
            name: int(((df["home_history_matches_available"] == 0) | (df["away_history_matches_available"] == 0)).sum())
            for name, df in transformed.items()
        },
        "warnings": warnings,
    }
    return transformed, report
