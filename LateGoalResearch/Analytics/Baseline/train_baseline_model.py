"""Training utilities for Baseline 1."""
from __future__ import annotations
from datetime import datetime
from typing import Any
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from . import baseline_config as cfg

def train_model(train_df: pd.DataFrame) -> tuple[Pipeline, dict[str, Any]]:
    x_train = train_df[cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A]
    y_train = train_df[cfg.TARGET_COLUMN]
    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("logistic_regression", LogisticRegression(max_iter=1000, random_state=cfg.RANDOM_STATE, solver="lbfgs")),
        ]
    )
    model.fit(x_train, y_train)
    cfg.MODEL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, cfg.MODEL_PATH)
    train_report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "model_type": "sklearn.pipeline.Pipeline(StandardScaler + LogisticRegression)",
        "model_path": str(cfg.MODEL_PATH),
        "fit_split": "train",
        "x_columns": cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A,
        "target": cfg.TARGET_COLUMN,
        "train_rows": int(len(train_df)),
        "parameters": model.named_steps["logistic_regression"].get_params(),
    }
    return model, train_report
