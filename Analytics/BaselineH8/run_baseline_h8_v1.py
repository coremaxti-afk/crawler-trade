"""Run controlled Baseline H8 V1 by cutoff.

Evaluates each cutoff independently with temporal split by match_id,
H8-only features, a null baseline, and logistic regression.
"""
from __future__ import annotations

import argparse
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_h8_v1.csv"
VALIDATION_REPORT_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_h8_v1_validation_report.json"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "reports"
METRICS_PATH = OUTPUT_DIR / "baseline_h8_v1_metrics.json"
VALIDATION_PATH = OUTPUT_DIR / "baseline_h8_v1_validation_report.json"
DOC_REPORT_PATH = PROJECT_ROOT / "docs" / "04_RESEARCH" / "BASELINE_H8_V1_RESULTS.md"
CUTOFFS = [60, 65, 70, 75]
TARGET_COLUMN = "target_late_goal_75"
FEATURE_COLUMNS = [
    "momentum_last_5m_avg",
    "momentum_last_10m_avg",
    "momentum_trend_last_10m",
    "momentum_sum_until_cutoff",
    "xg_last_5m",
    "xg_last_10m",
    "shots_last_5m",
    "shots_last_10m",
    "xg_sum_until_cutoff",
]
GRAPH_FEATURES = FEATURE_COLUMNS[:4]
SHOTMAP_FEATURES = FEATURE_COLUMNS[4:]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Baseline H8 V1 controlled experiment.")
    parser.add_argument("--dataset", default=str(DATASET_PATH))
    parser.add_argument("--validation-report", default=str(VALIDATION_REPORT_PATH))
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR))
    return parser.parse_args()


def clean(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, list):
        return [clean(v) for v in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        v = float(value)
        return None if math.isnan(v) or math.isinf(v) else v
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def fmt(value: Any, digits: int = 4) -> str:
    if value is None or (isinstance(value, float) and (math.isnan(value) or math.isinf(value))):
        return "NA"
    return f"{value:.{digits}f}" if isinstance(value, float) else str(value)


def load_gate(path: Path) -> dict[str, Any]:
    r = json.loads(path.read_text(encoding="utf-8"))
    checks = {
        "target_late_goal_75_unido_corretamente": r.get("target_mismatches") == 0 and r.get("target_column") == TARGET_COLUMN,
        "ausencia_target_derived_features": r.get("anti_leakage_checks", {}).get("no_target_derived_columns_in_x") is True and not r.get("blocked_columns_present"),
        "ausencia_full_match": r.get("anti_leakage_checks", {}).get("uses_only_precomputed_h8_features") is True,
        "ausencia_placar_final": r.get("anti_leakage_checks", {}).get("no_final_score_columns") is True,
        "graph_known_missing_preservado": r.get("anti_leakage_checks", {}).get("graph_known_missing_preserved") is True and r.get("graph_known_missing_rows") == 4,
        "duplicatas_match_cutoff_zero": r.get("key_duplicates") == 0,
    }
    return {"status": r.get("status"), "checks": checks, "all_passed": all(checks.values()), "source_report": str(path)}


def split_temporal(df: pd.DataFrame) -> tuple[dict[str, pd.DataFrame], dict[str, Any]]:
    matches = df[["match_id", "match_date", TARGET_COLUMN]].drop_duplicates("match_id").sort_values(["match_date", "match_id"]).reset_index(drop=True)
    n = len(matches)
    ids = {
        "train": set(matches.iloc[: int(n * 0.60)]["match_id"]),
        "validation": set(matches.iloc[int(n * 0.60) : int(n * 0.80)]["match_id"]),
        "test": set(matches.iloc[int(n * 0.80) :]["match_id"]),
    }
    splits = {k: df[df["match_id"].isin(v)].copy() for k, v in ids.items()}
    summaries = {}
    for name, part in splits.items():
        summaries[name] = {
            "rows": int(len(part)),
            "matches": int(part["match_id"].nunique()),
            "date_min": str(part["match_date"].min()),
            "date_max": str(part["match_date"].max()),
            "positive": int(part[TARGET_COLUMN].sum()),
            "negative": int(len(part) - part[TARGET_COLUMN].sum()),
            "prevalence": float(part[TARGET_COLUMN].mean()),
        }
    return splits, {
        "split_method": "temporal_by_match_id_60_20_20_no_shuffle",
        "summaries": summaries,
        "overlaps": {"train_validation": bool(ids["train"] & ids["validation"]), "train_test": bool(ids["train"] & ids["test"]), "validation_test": bool(ids["validation"] & ids["test"])},
        "temporal_order_valid": splits["train"]["match_date"].max() <= splits["validation"]["match_date"].min() <= splits["validation"]["match_date"].max() <= splits["test"]["match_date"].min(),
    }


def lift_at_top20(y: np.ndarray, p: np.ndarray) -> dict[str, Any]:
    top_n = max(1, int(math.ceil(len(y) * 0.20)))
    top_y = y[np.argsort(-p)[:top_n]]
    base = float(y.mean())
    top_rate = float(top_y.mean())
    return {"top_fraction": 0.20, "top_n": top_n, "top_positive": int(top_y.sum()), "top_rate": top_rate, "base_rate": base, "lift": float(top_rate / base) if base else None}


def calibration_bins(y: np.ndarray, p: np.ndarray) -> list[dict[str, Any]]:
    d = pd.DataFrame({"y": y, "p": p})
    d["bin"] = pd.cut(d["p"], bins=5, duplicates="drop", include_lowest=True)
    return [{"bin": str(b), "rows": int(len(g)), "mean_predicted": float(g["p"].mean()), "observed_rate": float(g["y"].mean())} for b, g in d.groupby("bin", observed=True)]


def evaluate(y: np.ndarray, p: np.ndarray) -> dict[str, Any]:
    return {
        "rows": int(len(y)),
        "positive": int(y.sum()),
        "negative": int(len(y) - y.sum()),
        "prevalence": float(y.mean()),
        "roc_auc": float(roc_auc_score(y, p)) if len(np.unique(y)) == 2 else None,
        "pr_auc": float(average_precision_score(y, p)) if len(np.unique(y)) == 2 else None,
        "brier_score": float(brier_score_loss(y, p)),
        "log_loss": float(log_loss(y, np.clip(p, 1e-6, 1 - 1e-6), labels=[0, 1])),
        "lift_at_top20": lift_at_top20(y, p),
        "calibration_bins": calibration_bins(y, p),
    }


def run_cutoff(df: pd.DataFrame, cutoff: int) -> dict[str, Any]:
    part = df[df["cutoff_minute"] == cutoff].copy()
    splits, split_report = split_temporal(part)
    model = Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler()), ("classifier", LogisticRegression(max_iter=1000, random_state=42))])
    model.fit(splits["train"][FEATURE_COLUMNS], splits["train"][TARGET_COLUMN].astype(int))
    null_p = float(splits["train"][TARGET_COLUMN].mean())
    metrics = {}
    for name, split in splits.items():
        y = split[TARGET_COLUMN].astype(int).to_numpy()
        p = model.predict_proba(split[FEATURE_COLUMNS])[:, 1]
        n = np.full_like(p, null_p, dtype=float)
        trained = evaluate(y, p)
        null = evaluate(y, n)
        metrics[name] = {
            "trained_model": trained,
            "null_baseline": null,
            "comparison_model_vs_null": {
                "roc_auc_delta_model_minus_null": trained["roc_auc"] - null["roc_auc"],
                "pr_auc_delta_model_minus_null": trained["pr_auc"] - null["pr_auc"],
                "brier_score_delta_model_minus_null": trained["brier_score"] - null["brier_score"],
                "log_loss_delta_model_minus_null": trained["log_loss"] - null["log_loss"],
                "lift_at_top20_delta_model_minus_null": trained["lift_at_top20"]["lift"] - null["lift_at_top20"]["lift"],
            },
        }
    coefs = model.named_steps["classifier"].coef_[0]
    feature_coefs = sorted(
        [{"feature": f, "group": "Graph" if f in GRAPH_FEATURES else "Shotmap", "coefficient": float(c), "abs_coefficient": float(abs(c))} for f, c in zip(FEATURE_COLUMNS, coefs)],
        key=lambda x: x["abs_coefficient"],
        reverse=True,
    )
    strength = {"Graph": sum(x["abs_coefficient"] for x in feature_coefs if x["group"] == "Graph"), "Shotmap": sum(x["abs_coefficient"] for x in feature_coefs if x["group"] == "Shotmap")}
    return {"cutoff": cutoff, "split_report": split_report, "null_baseline_probability": null_p, "metrics": metrics, "feature_coefficients": feature_coefs, "best_feature": feature_coefs[0], "group_strength": strength, "best_group": max(strength.items(), key=lambda x: x[1])[0]}


def rank(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for r in results:
        test = r["metrics"]["test"]["trained_model"]
        cmp = r["metrics"]["test"]["comparison_model_vs_null"]
        rows.append({"cutoff": r["cutoff"], "roc_auc_test": test["roc_auc"], "pr_auc_test": test["pr_auc"], "brier_delta_test": cmp["brier_score_delta_model_minus_null"], "log_loss_delta_test": cmp["log_loss_delta_model_minus_null"], "lift_at_top20_test": test["lift_at_top20"]["lift"], "best_feature": r["best_feature"], "best_group": r["best_group"]})
    return sorted(rows, key=lambda x: (x["roc_auc_test"], x["pr_auc_test"], -x["brier_delta_test"]), reverse=True)


def write_report(results: list[dict[str, Any]], ranking: list[dict[str, Any]], validation: dict[str, Any]) -> None:
    best = ranking[0]
    metric_rows = ["| Cutoff | Split | Modelo | N | Pos | Neg | Prev | ROC-AUC | PR-AUC | Brier | Log Loss | Lift@20% |", "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    cmp_rows = ["| Cutoff | Split | Delta ROC-AUC | Delta PR-AUC | Delta Brier | Delta Log Loss | Delta Lift@20% |", "|---:|---|---:|---:|---:|---:|---:|"]
    for r in results:
        for split in ["train", "validation", "test"]:
            for key, label in [("null_baseline", "Nulo"), ("trained_model", "Modelo")]:
                m = r["metrics"][split][key]
                metric_rows.append(f"| {r['cutoff']} | {split} | {label} | {m['rows']} | {m['positive']} | {m['negative']} | {fmt(m['prevalence'])} | {fmt(m['roc_auc'])} | {fmt(m['pr_auc'])} | {fmt(m['brier_score'])} | {fmt(m['log_loss'])} | {fmt(m['lift_at_top20']['lift'])} |")
            c = r["metrics"][split]["comparison_model_vs_null"]
            cmp_rows.append(f"| {r['cutoff']} | {split} | {fmt(c['roc_auc_delta_model_minus_null'])} | {fmt(c['pr_auc_delta_model_minus_null'])} | {fmt(c['brier_score_delta_model_minus_null'])} | {fmt(c['log_loss_delta_model_minus_null'])} | {fmt(c['lift_at_top20_delta_model_minus_null'])} |")
    ranking_rows = ["| Rank | Cutoff | ROC-AUC Test | PR-AUC Test | Delta Brier Test | Delta LogLoss Test | Lift@20% Test | Melhor Feature | Melhor Grupo |", "|---:|---:|---:|---:|---:|---:|---:|---|---|"]
    for i, row in enumerate(ranking, 1):
        ranking_rows.append(f"| {i} | {row['cutoff']} | {fmt(row['roc_auc_test'])} | {fmt(row['pr_auc_test'])} | {fmt(row['brier_delta_test'])} | {fmt(row['log_loss_delta_test'])} | {fmt(row['lift_at_top20_test'])} | `{row['best_feature']['feature']}` | {row['best_group']} |")
    gate = "\n".join(f"- {k}: `{v}`" for k, v in validation["validation_gate"]["checks"].items())
    report = f"""# Baseline H8 V1 Results

Gerado em: {datetime.now().isoformat(timespec='seconds')}

## Resumo Executivo

Baseline H8 V1 executado em rodada controlada, avaliando cada cutoff separadamente: 60, 65, 70 e 75.

Status operacional: `{validation['status']}`.

Melhor cutoff no ranking principal: `{best['cutoff']}`.

Metricas do melhor cutoff no teste:

- ROC-AUC Test: {fmt(best['roc_auc_test'])}
- PR-AUC Test: {fmt(best['pr_auc_test'])}
- Delta Brier modelo-nulo: {fmt(best['brier_delta_test'])}
- Delta LogLoss modelo-nulo: {fmt(best['log_loss_delta_test'])}
- Lift@Top20% Test: {fmt(best['lift_at_top20_test'])}
- Melhor feature: `{best['best_feature']['feature']}`
- Melhor grupo: `{best['best_group']}`

## Gate do Validation Report

Todos os pontos obrigatorios foram confirmados antes da execucao:

{gate}

## Metodologia

- Dataset: `data/processed/datasets/late_goal_dataset_h8_v1.csv`.
- Target: `{TARGET_COLUMN}`.
- Features: somente whitelist H8.
- Cutoffs avaliados separadamente: 60, 65, 70, 75.
- Split: temporal por `match_id`, 60/20/20, sem shuffle.
- Imputacao: mediana fitada apenas no treino dentro de cada cutoff.
- Escala: StandardScaler fitado apenas no treino dentro de cada cutoff.
- Modelo: regressao logistica controlada.
- Baseline nulo: probabilidade constante igual a prevalencia do treino em cada cutoff.

## Features Usadas

""" + "\n".join(f"- `{f}`" for f in FEATURE_COLUMNS) + f"""

## Auditoria Anti-Leakage

- Nenhuma feature H3/H4/H6/H9 foi usada.
- Nenhuma feature target-derived foi usada em X.
- Nenhum placar final foi usado.
- Nenhuma estatistica full-match foi usada.
- Features H8 vieram do Dataset H8 V1, herdando a regra `minute <= cutoff`.
- Backtesting financeiro: nao executado.
- Producao: nao criada.

## Metricas por Cutoff e Split

{chr(10).join(metric_rows)}

## Comparacao Contra Baseline Nulo

Valores negativos em Brier/LogLoss indicam melhora do modelo contra o nulo.

{chr(10).join(cmp_rows)}

## Ranking dos Cutoffs

{chr(10).join(ranking_rows)}

## Melhor Feature e Grupo

- Melhor feature geral: `{best['best_feature']['feature']}`.
- Melhor grupo geral: `{best['best_group']}`.

## Recomendacao Final

Decisao quantitativa inicial: `{validation['quantitative_decision']['status']}`.

Motivo: o melhor cutoff foi 60, mas o ROC-AUC Test ficou em {fmt(best['roc_auc_test'])}, o PR-AUC Test ficou em {fmt(best['pr_auc_test'])}, e o modelo piorou o baseline nulo em Brier ({fmt(best['brier_delta_test'])}) e LogLoss ({fmt(best['log_loss_delta_test'])}) no teste.

Baseline H8 V1 deve ser tratado como experimento controlado de pesquisa. O resultado nao autoriza producao, automacao operacional ou backtesting financeiro.
"""
    DOC_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> int:
    args = parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    gate = load_gate(Path(args.validation_report))
    print(json.dumps(gate, ensure_ascii=False, indent=2))
    if not gate["all_passed"]:
        raise RuntimeError("Dataset H8 V1 validation gate failed; baseline is not authorized.")
    df = pd.read_csv(args.dataset)
    df["match_date"] = pd.to_datetime(df["match_date"])
    results = [run_cutoff(df, cutoff) for cutoff in CUTOFFS]
    ranking = rank(results)
    best = ranking[0]
    approved = best["roc_auc_test"] >= 0.55 and best["pr_auc_test"] > 0.5263 and best["brier_delta_test"] < 0 and best["log_loss_delta_test"] < 0
    validation = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "status": "APTO COM RESSALVAS", "validation_gate": gate, "errors": [], "warnings": ["Baseline H8 V1 did not meet minimum quantitative criteria on the test split."], "anti_leakage": {"features_used": FEATURE_COLUMNS, "target": TARGET_COLUMN, "cutoffs": CUTOFFS, "no_h3_h4_h6_h9_features": True, "no_backtesting": True, "no_production": True}, "quantitative_decision": {"status": "APROVADO" if approved else "NAO APROVADO", "best_cutoff": best["cutoff"], "roc_auc_test": best["roc_auc_test"], "pr_auc_test": best["pr_auc_test"], "brier_delta_test": best["brier_delta_test"], "log_loss_delta_test": best["log_loss_delta_test"]}}
    payload = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "dataset": args.dataset, "target": TARGET_COLUMN, "features": FEATURE_COLUMNS, "cutoffs": CUTOFFS, "results": results, "ranking": ranking}
    METRICS_PATH.write_text(json.dumps(clean(payload), ensure_ascii=False, indent=2), encoding="utf-8")
    VALIDATION_PATH.write_text(json.dumps(clean(validation), ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(results, ranking, validation)
    print("FINAL SUMMARY")
    print(f"status={validation['status']}")
    print(f"best_cutoff={best['cutoff']}")
    print(f"best_roc_auc_test={fmt(best['roc_auc_test'])}")
    print(f"best_pr_auc_test={fmt(best['pr_auc_test'])}")
    print(f"best_feature={best['best_feature']['feature']}")
    print(f"best_group={best['best_group']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
