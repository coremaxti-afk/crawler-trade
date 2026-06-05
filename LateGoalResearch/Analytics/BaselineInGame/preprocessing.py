"""Preprocessing utilities for Baseline In-Game V1."""
from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

from Analytics.BaselineInGame import baseline_ingame_config as cfg


def fit_preprocessor(train_df: pd.DataFrame) -> ColumnTransformer:
    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric_imputer", SimpleImputer(strategy="median"), cfg.NUMERIC_FEATURES),
            ("categorical_encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cfg.CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )
    preprocessor.fit(train_df[cfg.ALLOWED_FEATURES])
    return preprocessor


def transformed_feature_names(preprocessor: ColumnTransformer) -> list[str]:
    names = list(cfg.NUMERIC_FEATURES)
    encoder = preprocessor.named_transformers_["categorical_encoder"]
    names.extend(encoder.get_feature_names_out(cfg.CATEGORICAL_FEATURES).tolist())
    return names


def transform_split(preprocessor: ColumnTransformer, frame: pd.DataFrame) -> pd.DataFrame:
    values = preprocessor.transform(frame[cfg.ALLOWED_FEATURES])
    transformed = pd.DataFrame(values, columns=transformed_feature_names(preprocessor), index=frame.index)
    keep = cfg.IDENTIFIER_COLUMNS + [cfg.TARGET_COLUMN]
    return pd.concat([frame[keep].reset_index(drop=True), transformed.reset_index(drop=True)], axis=1)


def fit_transform_preprocess(splits: dict[str, pd.DataFrame]) -> tuple[dict[str, pd.DataFrame], Any, dict[str, Any]]:
    preprocessor = fit_preprocessor(splits["train"])
    transformed = {name: transform_split(preprocessor, split_df) for name, split_df in splits.items()}

    numeric_imputer = preprocessor.named_transformers_["numeric_imputer"]
    categorical_encoder = preprocessor.named_transformers_["categorical_encoder"]
    nulls_before = {name: split_df[cfg.ALLOWED_FEATURES].isna().sum().astype(int).to_dict() for name, split_df in splits.items()}
    nulls_after = {name: frame[transformed_feature_names(preprocessor)].isna().sum().astype(int).to_dict() for name, frame in transformed.items()}
    category_counts = {
        name: split_df["score_state_group"].fillna("__MISSING__").value_counts().astype(int).to_dict()
        for name, split_df in splits.items()
    }

    report = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "numeric_imputation": {
            "method": "median fitted on train only",
            "fit_split": "train",
            "medians": dict(zip(cfg.NUMERIC_FEATURES, [float(value) for value in numeric_imputer.statistics_])),
        },
        "categorical_encoding": {
            "method": "one-hot fitted on train only",
            "fit_split": "train",
            "handle_unknown": "ignore",
            "train_categories": {
                cfg.CATEGORICAL_FEATURES[index]: categories.tolist()
                for index, categories in enumerate(categorical_encoder.categories_)
            },
            "category_counts_by_split": category_counts,
        },
        "transformed_feature_names": transformed_feature_names(preprocessor),
        "nulls_before": nulls_before,
        "nulls_after": nulls_after,
        "warnings": [],
    }
    return transformed, preprocessor, report
