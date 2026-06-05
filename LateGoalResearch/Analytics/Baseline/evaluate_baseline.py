"""Evaluation utilities for Baseline 1."""
from __future__ import annotations
from datetime import datetime
from typing import Any
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score
from . import baseline_config as cfg

def clipped(probabilities: np.ndarray) -> np.ndarray:
    return np.clip(probabilities, 1e-15, 1 - 1e-15)

def lift_at_top_fraction(y_true: pd.Series, y_score: np.ndarray, fraction: float = 0.20) -> dict[str, Any]:
    work = pd.DataFrame({"y": y_true.to_numpy(), "score": y_score})
    n_top = max(1, int(np.ceil(len(work) * fraction)))
    top = work.sort_values("score", ascending=False).head(n_top)
    overall = float(work["y"].mean()) if len(work) else np.nan
    top_rate = float(top["y"].mean()) if len(top) else np.nan
    lift = top_rate / overall if overall and not np.isnan(overall) else np.nan
    return {"fraction": fraction, "n_top": int(n_top), "top_positive_rate": top_rate, "overall_positive_rate": overall, "lift": lift}

def calibration_bins(y_true: pd.Series, y_score: np.ndarray, bins: int = 5) -> list[dict[str, Any]]:
    work = pd.DataFrame({"y": y_true.to_numpy(), "score": y_score})
    try:
        work["bin"] = pd.qcut(work["score"], q=bins, duplicates="drop")
    except ValueError:
        work["bin"] = "single_bin"
    rows = []
    for bin_value, group in work.groupby("bin", observed=False):
        rows.append({"bin": str(bin_value), "n": int(len(group)), "predicted_mean": float(group["score"].mean()), "observed_rate": float(group["y"].mean())})
    return rows

def compute_metrics(y_true: pd.Series, y_score: np.ndarray) -> dict[str, Any]:
    y_score = np.asarray(y_score, dtype=float)
    y_true = y_true.astype(int)
    has_two_classes = y_true.nunique() == 2
    return {
        "rows": int(len(y_true)),
        "positive": int(y_true.sum()),
        "negative": int((y_true == 0).sum()),
        "prevalence": float(y_true.mean()) if len(y_true) else None,
        "roc_auc": float(roc_auc_score(y_true, y_score)) if has_two_classes else None,
        "pr_auc": float(average_precision_score(y_true, y_score)) if has_two_classes else None,
        "brier_score": float(brier_score_loss(y_true, y_score)),
        "log_loss": float(log_loss(y_true, clipped(y_score), labels=[0, 1])),
        "lift_at_top20": lift_at_top_fraction(y_true, y_score),
        "calibration_bins": calibration_bins(y_true, y_score),
    }

def evaluate_model(model: Any, splits: dict[str, pd.DataFrame]) -> dict[str, Any]:
    train_prevalence = float(splits["train"][cfg.TARGET_COLUMN].mean())
    results = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "target": cfg.TARGET_COLUMN,
        "x_columns": cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A,
        "null_baseline_probability": train_prevalence,
        "splits": {},
        "comparison_model_vs_null": {},
    }
    for name, split_df in splits.items():
        y_true = split_df[cfg.TARGET_COLUMN].astype(int)
        null_score = np.full(len(split_df), train_prevalence)
        model_score = model.predict_proba(split_df[cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A])[:, 1]
        null_metrics = compute_metrics(y_true, null_score)
        model_metrics = compute_metrics(y_true, model_score)
        results["splits"][name] = {"null_baseline": null_metrics, "trained_model": model_metrics}
        results["comparison_model_vs_null"][name] = {
            "brier_score_delta_model_minus_null": model_metrics["brier_score"] - null_metrics["brier_score"],
            "log_loss_delta_model_minus_null": model_metrics["log_loss"] - null_metrics["log_loss"],
            "roc_auc_delta_model_minus_null": None if null_metrics["roc_auc"] is None else model_metrics["roc_auc"] - null_metrics["roc_auc"],
            "pr_auc_delta_model_minus_null": None if null_metrics["pr_auc"] is None else model_metrics["pr_auc"] - null_metrics["pr_auc"],
        }
    test = results["splits"]["test"]["trained_model"]
    validation = results["splits"]["validation"]["trained_model"]
    test_prevalence = test["prevalence"]
    checks = {
        "roc_auc_test": test["roc_auc"],
        "roc_auc_test_min": cfg.APPROVAL_CRITERIA["roc_auc_test_min"],
        "roc_auc_test_pass": bool(test["roc_auc"] is not None and test["roc_auc"] > cfg.APPROVAL_CRITERIA["roc_auc_test_min"]),
        "pr_auc_test": test["pr_auc"],
        "pr_auc_test_required": None if test_prevalence is None else test_prevalence + cfg.APPROVAL_CRITERIA["pr_auc_test_margin_vs_prevalence"],
        "pr_auc_test_pass": bool(test["pr_auc"] is not None and test_prevalence is not None and test["pr_auc"] > test_prevalence + cfg.APPROVAL_CRITERIA["pr_auc_test_margin_vs_prevalence"]),
        "roc_auc_validation_test_gap": None if validation["roc_auc"] is None or test["roc_auc"] is None else abs(validation["roc_auc"] - test["roc_auc"]),
    }
    checks["roc_auc_gap_pass"] = bool(checks["roc_auc_validation_test_gap"] is not None and checks["roc_auc_validation_test_gap"] <= cfg.APPROVAL_CRITERIA["roc_auc_validation_test_max_gap"])
    checks["baseline_status"] = "APROVADO" if checks["roc_auc_test_pass"] and checks["pr_auc_test_pass"] and checks["roc_auc_gap_pass"] else "NAO APROVADO"
    results["approval_checks"] = checks
    return results
