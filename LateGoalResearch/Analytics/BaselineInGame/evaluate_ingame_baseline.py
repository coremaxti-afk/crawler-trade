"""Evaluation utilities for Baseline In-Game V1."""
from __future__ import annotations

from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score

from Analytics.BaselineInGame import baseline_ingame_config as cfg


def _clip(probabilities: np.ndarray) -> np.ndarray:
    return np.clip(probabilities, 1e-15, 1 - 1e-15)


def lift_at_top_fraction(y_true: pd.Series, y_score: np.ndarray, fraction: float = 0.20) -> dict[str, Any]:
    work = pd.DataFrame({"y": y_true.to_numpy(), "score": y_score})
    n_top = max(1, int(np.ceil(len(work) * fraction)))
    top = work.sort_values("score", ascending=False).head(n_top)
    overall_rate = float(work["y"].mean()) if len(work) else None
    top_rate = float(top["y"].mean()) if len(top) else None
    lift = None if not overall_rate else top_rate / overall_rate
    return {
        "fraction": fraction,
        "n_top": int(n_top),
        "top_positive_rate": top_rate,
        "overall_positive_rate": overall_rate,
        "lift": lift,
    }


def calibration_bins(y_true: pd.Series, y_score: np.ndarray, bins: int = 5) -> list[dict[str, Any]]:
    work = pd.DataFrame({"y": y_true.to_numpy(), "score": y_score})
    try:
        work["bin"] = pd.qcut(work["score"], q=bins, duplicates="drop")
    except ValueError:
        work["bin"] = "single_bin"
    rows = []
    for bin_value, group in work.groupby("bin", observed=False):
        rows.append({
            "bin": str(bin_value),
            "n": int(len(group)),
            "predicted_mean": float(group["score"].mean()),
            "observed_rate": float(group["y"].mean()),
        })
    return rows


def compute_metrics(y_true: pd.Series, y_score: np.ndarray) -> dict[str, Any]:
    y_true = y_true.astype(int)
    y_score = np.asarray(y_score, dtype=float)
    has_two_classes = y_true.nunique() == 2
    return {
        "rows": int(len(y_true)),
        "positive": int(y_true.sum()),
        "negative": int((y_true == 0).sum()),
        "prevalence": float(y_true.mean()) if len(y_true) else None,
        "roc_auc": float(roc_auc_score(y_true, y_score)) if has_two_classes else None,
        "pr_auc": float(average_precision_score(y_true, y_score)) if has_two_classes else None,
        "brier_score": float(brier_score_loss(y_true, y_score)),
        "log_loss": float(log_loss(y_true, _clip(y_score), labels=[0, 1])),
        "lift_at_top20": lift_at_top_fraction(y_true, y_score),
        "calibration_bins": calibration_bins(y_true, y_score),
    }


def evaluate_model(model: Any, splits: dict[str, pd.DataFrame], feature_columns: list[str]) -> dict[str, Any]:
    train_prevalence = float(splits["train"][cfg.TARGET_COLUMN].mean())
    results = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "target": cfg.TARGET_COLUMN,
        "operational_target": cfg.OPERATIONAL_TARGET_COLUMN,
        "cutoff_minute": cfg.CUTOFF_MINUTE,
        "base_x_columns": cfg.ALLOWED_FEATURES,
        "encoded_x_columns": feature_columns,
        "null_baseline_probability": train_prevalence,
        "splits": {},
        "comparison_model_vs_null": {},
        "baseline_1a_external_reference": cfg.BASELINE_1A_REFERENCE,
    }
    for split_name, split_df in splits.items():
        y_true = split_df[cfg.TARGET_COLUMN].astype(int)
        null_score = np.full(len(split_df), train_prevalence)
        model_score = model.predict_proba(split_df[feature_columns])[:, 1]
        null_metrics = compute_metrics(y_true, null_score)
        model_metrics = compute_metrics(y_true, model_score)
        results["splits"][split_name] = {
            "null_baseline": null_metrics,
            "trained_model": model_metrics,
        }
        results["comparison_model_vs_null"][split_name] = {
            "brier_score_delta_model_minus_null": model_metrics["brier_score"] - null_metrics["brier_score"],
            "log_loss_delta_model_minus_null": model_metrics["log_loss"] - null_metrics["log_loss"],
            "roc_auc_delta_model_minus_null": None if null_metrics["roc_auc"] is None else model_metrics["roc_auc"] - null_metrics["roc_auc"],
            "pr_auc_delta_model_minus_null": None if null_metrics["pr_auc"] is None else model_metrics["pr_auc"] - null_metrics["pr_auc"],
            "lift_at_top20_delta_model_minus_null": None if null_metrics["lift_at_top20"]["lift"] is None else model_metrics["lift_at_top20"]["lift"] - null_metrics["lift_at_top20"]["lift"],
        }

    test = results["splits"]["test"]["trained_model"]
    test_null = results["splits"]["test"]["null_baseline"]
    test_prevalence = test["prevalence"]
    roc_auc_pass = bool(test["roc_auc"] is not None and test["roc_auc"] > cfg.APPROVAL_CRITERIA["roc_auc_test_min"])
    pr_auc_required = None if test_prevalence is None else test_prevalence + cfg.APPROVAL_CRITERIA["pr_auc_test_margin_vs_prevalence"]
    pr_auc_pass = bool(test["pr_auc"] is not None and pr_auc_required is not None and test["pr_auc"] > pr_auc_required)
    brier_pass = bool(test["brier_score"] <= test_null["brier_score"])
    log_loss_pass = bool(test["log_loss"] <= test_null["log_loss"])
    if not (roc_auc_pass and pr_auc_pass):
        baseline_status = "NAO APROVADO"
    elif not (brier_pass and log_loss_pass):
        baseline_status = "APTO COM RESSALVAS"
    else:
        baseline_status = "APROVADO"

    results["approval_checks"] = {
        "roc_auc_test": test["roc_auc"],
        "roc_auc_test_min": cfg.APPROVAL_CRITERIA["roc_auc_test_min"],
        "roc_auc_test_pass": roc_auc_pass,
        "pr_auc_test": test["pr_auc"],
        "pr_auc_test_required": pr_auc_required,
        "pr_auc_test_pass": pr_auc_pass,
        "brier_score_test": test["brier_score"],
        "brier_score_null_test": test_null["brier_score"],
        "brier_score_pass": brier_pass,
        "log_loss_test": test["log_loss"],
        "log_loss_null_test": test_null["log_loss"],
        "log_loss_pass": log_loss_pass,
        "baseline_status": baseline_status,
    }
    return results
