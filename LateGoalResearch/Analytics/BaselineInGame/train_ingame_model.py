"""Training utilities for Baseline In-Game V1."""
from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from Analytics.BaselineInGame import baseline_ingame_config as cfg


def train_model(train_df: pd.DataFrame, feature_columns: list[str]) -> tuple[Pipeline, dict[str, Any]]:
    X_train = train_df[feature_columns]
    y_train = train_df[cfg.TARGET_COLUMN].astype(int)
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=1000, random_state=cfg.RANDOM_STATE)),
        ]
    )
    model.fit(X_train, y_train)
    return model, {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "model_type": "sklearn.pipeline.Pipeline(StandardScaler + LogisticRegression)",
        "fit_split": "train",
        "rows": int(len(train_df)),
        "positive": int(y_train.sum()),
        "negative": int((y_train == 0).sum()),
        "feature_columns_after_encoding": feature_columns,
    }
