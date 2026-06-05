"""Orchestrate Baseline 1 pre-match H3/H4 controlled run."""
from __future__ import annotations
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from Analytics.Baseline import baseline_config as cfg  # noqa: E402
from Analytics.Baseline.build_baseline_dataset import build_baseline_dataset, json_default  # noqa: E402
from Analytics.Baseline.evaluate_baseline import evaluate_model  # noqa: E402
from Analytics.Baseline.imputation import fit_transform_impute  # noqa: E402
from Analytics.Baseline.temporal_split import split_dataset  # noqa: E402
from Analytics.Baseline.train_baseline_model import train_model  # noqa: E402

def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")

def fmt(value: Any, digits: int = 4) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)

def validation_report(manifest: dict[str, Any], split_report: dict[str, Any], imputation_report: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not manifest["validations"]["match_id_unique_after_conversion"]:
        errors.append("match_id is not unique after match-level conversion.")
    if any(split_report["overlaps"].values()):
        errors.append("At least one match_id appears in more than one split.")
    if not split_report["temporal_order_valid"]:
        errors.append("Temporal split order is invalid.")
    if any(value > 0 for counts in imputation_report["nulls_after"].values() for value in counts.values()):
        errors.append("Null values remain after imputation.")
    if manifest["validations"]["target_null_count"] != 0:
        errors.append("Target contains null values.")
    if not manifest["validations"]["all_x_columns_from_whitelist"]:
        errors.append("At least one X column is outside the official whitelist.")
    warnings.extend(imputation_report.get("warnings", []))
    if metrics["approval_checks"]["baseline_status"] != "APROVADO":
        warnings.append("Baseline did not meet all approval thresholds in the controlled run.")
    status = "NAO APTO" if errors else "APTO COM RESSALVAS" if warnings else "APTO"
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "anti_leakage": {
                "official_whitelist_precedence": True,
                "x_columns": cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A,
                "target": cfg.TARGET_COLUMN,
                "removed_columns": manifest["removed_columns"],
                "forbidden_scan_findings_on_x": manifest["forbidden_scan_findings_on_x"],
                "all_x_columns_from_whitelist": manifest["validations"]["all_x_columns_from_whitelist"],
            },
            "split": split_report,
            "imputation": imputation_report,
            "metrics_approval": metrics["approval_checks"],
        },
    }

def metric_line(metrics: dict[str, Any], split: str, model_key: str) -> str:
    item = metrics["splits"][split][model_key]
    return f"| {split} | {model_key} | {item['rows']} | {item['positive']} | {item['negative']} | {fmt(item['prevalence'])} | {fmt(item['roc_auc'])} | {fmt(item['pr_auc'])} | {fmt(item['brier_score'])} | {fmt(item['log_loss'])} | {fmt(item['lift_at_top20']['lift'])} |"

def write_markdown_report(metrics: dict[str, Any], split_report: dict[str, Any], imputation_report: dict[str, Any], validation: dict[str, Any], train_report: dict[str, Any]) -> None:
    test_metrics = metrics["splits"]["test"]["trained_model"]
    approval = metrics["approval_checks"]
    metric_rows = ["| Split | Modelo | N | Pos | Neg | Prev | ROC-AUC | PR-AUC | Brier | Log Loss | Lift@20% |", "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for split in ["train", "validation", "test"]:
        metric_rows.append(metric_line(metrics, split, "null_baseline"))
        metric_rows.append(metric_line(metrics, split, "trained_model"))
    comparison_rows = ["| Split | Delta Brier modelo-nulo | Delta LogLoss modelo-nulo | Delta ROC-AUC | Delta PR-AUC |", "|---|---:|---:|---:|---:|"]
    for split in ["train", "validation", "test"]:
        item = metrics["comparison_model_vs_null"][split]
        comparison_rows.append(f"| {split} | {fmt(item['brier_score_delta_model_minus_null'])} | {fmt(item['log_loss_delta_model_minus_null'])} | {fmt(item['roc_auc_delta_model_minus_null'])} | {fmt(item['pr_auc_delta_model_minus_null'])} |")
    split_rows = ["| Split | N | Data inicial | Data final | Pos | Neg | Prevalencia | History zero |", "|---|---:|---|---|---:|---:|---:|---:|"]
    for split in ["train", "validation", "test"]:
        dist = split_report["target_distribution"][split]
        dates = split_report["date_ranges"][split]
        split_rows.append(f"| {split} | {split_report['split_counts'][split]} | {dates['min']} | {dates['max']} | {dist['positive']} | {dist['negative']} | {fmt(dist['prevalence'])} | {split_report['history_absent_rows'][split]} |")
    report = f"""# Baseline 1 Pre-Match H3/H4 Results

Gerado em: {datetime.now().isoformat(timespec='seconds')}

## Resumo Executivo

Baseline 1A executado em rodada controlada com features pre-jogo H3/H4 aprovadas, target `{cfg.TARGET_COLUMN}`, split temporal 60/20/20 sem shuffle, imputacao por mediana fitada apenas no treino, baseline nulo por prevalencia do treino e modelo treinado de regressao logistica.

Status operacional: `{validation['status']}`.

Resultado no teste:

- ROC-AUC Test: {fmt(test_metrics['roc_auc'])}
- PR-AUC Test: {fmt(test_metrics['pr_auc'])}
- Prevalencia Test: {fmt(test_metrics['prevalence'])}
- ROC-AUC aprovado: {approval['roc_auc_test_pass']}
- PR-AUC aprovado: {approval['pr_auc_test_pass']}
- Status dos criterios: {approval['baseline_status']}

## Features Usadas

""" + "\n".join(f"- `{column}`" for column in cfg.ALLOWED_MATCH_LEVEL_FEATURES_1A) + f"""

## Metodologia

- Unidade final: 1 linha por partida.
- Target: `{cfg.TARGET_COLUMN}`.
- Split: temporal cronologico 60/20/20, sem shuffle.
- Imputacao: mediana fitada apenas no treino.
- Baseline nulo: probabilidade constante igual a prevalencia do treino.
- Modelo treinado: {train_report['model_type']}.
- Producao, automacao operacional e backtesting financeiro: nao executados.

## Split Temporal

{chr(10).join(split_rows)}

## Imputacao

Medianas, nulos antes/depois e contagens detalhadas estao em `{cfg.IMPUTATION_REPORT_PATH}`. Observacoes sem historico foram mantidas no experimento principal.

## Metricas por Split

{chr(10).join(metric_rows)}

## Comparacao Modelo vs Baseline Nulo

Valores negativos em Brier/LogLoss indicam melhora probabilistica do modelo contra o baseline nulo.

{chr(10).join(comparison_rows)}

## Decisao Final

Status dos criterios quantitativos: `{approval['baseline_status']}`.

Status operacional do artefato: `{validation['status']}`.

Este resultado e uma primeira execucao controlada para revisao do Quant Research e PM. Nao autoriza producao, automacao operacional, backtesting financeiro ou uso como sistema decisorio.

## Artefatos Gerados

- `{cfg.BASELINE_DATASET_PATH}`
- `{cfg.TRAIN_DATASET_PATH}`
- `{cfg.VALIDATION_DATASET_PATH}`
- `{cfg.TEST_DATASET_PATH}`
- `{cfg.FEATURE_MANIFEST_PATH}`
- `{cfg.SPLIT_REPORT_PATH}`
- `{cfg.IMPUTATION_REPORT_PATH}`
- `{cfg.METRICS_PATH}`
- `{cfg.VALIDATION_REPORT_PATH}`
- `{cfg.MODEL_PATH}`
"""
    cfg.DOC_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cfg.DOC_REPORT_PATH.write_text(report, encoding="utf-8")

def main() -> None:
    print("Building Baseline 1 pre-match dataset...")
    baseline_df, manifest = build_baseline_dataset()
    cfg.BASELINE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cfg.REPORT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cfg.MODEL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    baseline_df.to_csv(cfg.BASELINE_DATASET_PATH, index=False)
    splits, split_report = split_dataset(baseline_df)
    imputed_splits, imputation_report = fit_transform_impute(splits)
    imputed_splits["train"].to_csv(cfg.TRAIN_DATASET_PATH, index=False)
    imputed_splits["validation"].to_csv(cfg.VALIDATION_DATASET_PATH, index=False)
    imputed_splits["test"].to_csv(cfg.TEST_DATASET_PATH, index=False)
    print("Training controlled logistic baseline...")
    model, train_report = train_model(imputed_splits["train"])
    metrics = evaluate_model(model, imputed_splits)
    validation = validation_report(manifest, split_report, imputation_report, metrics)
    write_json(cfg.FEATURE_MANIFEST_PATH, manifest)
    write_json(cfg.SPLIT_REPORT_PATH, split_report)
    write_json(cfg.IMPUTATION_REPORT_PATH, imputation_report)
    write_json(cfg.METRICS_PATH, metrics)
    write_json(cfg.VALIDATION_REPORT_PATH, validation)
    write_markdown_report(metrics, split_report, imputation_report, validation, train_report)
    print("Baseline 1 controlled run completed.")
    print(f"Rows: {len(baseline_df)}")
    print(f"Train/Validation/Test: {len(imputed_splits['train'])}/{len(imputed_splits['validation'])}/{len(imputed_splits['test'])}")
    print(f"Status: {validation['status']}")
    print(f"Criteria status: {metrics['approval_checks']['baseline_status']}")
    print(f"ROC-AUC Test: {fmt(metrics['approval_checks']['roc_auc_test'])}")
    print(f"PR-AUC Test: {fmt(metrics['approval_checks']['pr_auc_test'])}")
    print(f"Report: {cfg.DOC_REPORT_PATH}")

if __name__ == "__main__":
    main()
