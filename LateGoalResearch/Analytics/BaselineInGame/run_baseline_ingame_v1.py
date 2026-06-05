"""Run the controlled Baseline In-Game V1 experiment."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Analytics.BaselineInGame import baseline_ingame_config as cfg  # noqa: E402
from Analytics.BaselineInGame.build_ingame_baseline_dataset import build_baseline_ingame_dataset, json_default  # noqa: E402
from Analytics.BaselineInGame.evaluate_ingame_baseline import evaluate_model  # noqa: E402
from Analytics.BaselineInGame.preprocessing import fit_transform_preprocess  # noqa: E402
from Analytics.BaselineInGame.temporal_split import split_dataset  # noqa: E402
from Analytics.BaselineInGame.train_ingame_model import train_model  # noqa: E402


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")


def fmt(value: Any, digits: int = 4) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def validation_report(manifest: dict[str, Any], split_report: dict[str, Any], preprocessing_report: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    validations = manifest["validations"]
    if not validations["all_rows_cutoff_75"]:
        errors.append("Snapshot contains rows outside cutoff_minute = 75.")
    if not validations["match_id_unique_after_filter"]:
        errors.append("match_id is not unique after cutoff filter.")
    if validations["target_null_count"] != 0:
        errors.append("Target contains null values.")
    if validations["target_equivalence_checked"] and validations["target_equivalence_mismatches"] != 0:
        errors.append("target_goal_after_cutoff does not match target_late_goal_75 for at least one match.")
    if not validations["all_x_columns_from_whitelist"]:
        errors.append("At least one X column is outside the official whitelist.")
    if any(split_report["overlaps"].values()):
        errors.append("At least one match_id appears in more than one split.")
    if not split_report["temporal_order_valid"]:
        errors.append("Temporal split order is invalid.")
    if any(value > 0 for split in preprocessing_report["nulls_after"].values() for value in split.values()):
        errors.append("Null values remain after preprocessing.")
    if metrics["approval_checks"]["baseline_status"] != "APROVADO":
        warnings.append("Baseline In-Game V1 did not meet all approval thresholds in the controlled run.")
    warnings.extend(preprocessing_report.get("warnings", []))
    status = "NAO APTO" if errors else "APTO COM RESSALVAS" if warnings else "APTO"
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "snapshot": {
                "cutoff_minute": cfg.CUTOFF_MINUTE,
                "all_rows_cutoff_75": validations["all_rows_cutoff_75"],
                "match_id_unique_after_filter": validations["match_id_unique_after_filter"],
                "target_equivalence_checked": validations["target_equivalence_checked"],
                "target_equivalence_mismatches": validations["target_equivalence_mismatches"],
            },
            "anti_leakage": {
                "official_whitelist_precedence": True,
                "base_x_columns": cfg.ALLOWED_FEATURES,
                "encoded_x_columns": metrics["encoded_x_columns"],
                "target": cfg.TARGET_COLUMN,
                "operational_target": cfg.OPERATIONAL_TARGET_COLUMN,
                "removed_columns": manifest["removed_columns"],
                "forbidden_scan_findings_on_x": manifest["forbidden_scan_findings_on_x"],
                "no_full_match_statistics_source_used": validations["no_full_match_statistics_source_used"],
                "no_prematch_features_used": validations["no_prematch_features_used"],
                "no_xg_xga_forecast_used": validations["no_xg_xga_forecast_used"],
            },
            "split": split_report,
            "preprocessing": preprocessing_report,
            "metrics_approval": metrics["approval_checks"],
        },
    }


def metric_line(metrics: dict[str, Any], split: str, model_key: str) -> str:
    item = metrics["splits"][split][model_key]
    return (
        f"| {split} | {model_key} | {item['rows']} | {item['positive']} | {item['negative']} | "
        f"{fmt(item['prevalence'])} | {fmt(item['roc_auc'])} | {fmt(item['pr_auc'])} | "
        f"{fmt(item['brier_score'])} | {fmt(item['log_loss'])} | {fmt(item['lift_at_top20']['lift'])} |"
    )


def write_markdown_report(metrics: dict[str, Any], split_report: dict[str, Any], preprocessing_report: dict[str, Any], validation: dict[str, Any]) -> None:
    test_metrics = metrics["splits"]["test"]["trained_model"]
    approval = metrics["approval_checks"]
    metric_rows = [
        "| Split | Modelo | N | Pos | Neg | Prev | ROC-AUC | PR-AUC | Brier | Log Loss | Lift@20% |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for split in ["train", "validation", "test"]:
        metric_rows.append(metric_line(metrics, split, "null_baseline"))
        metric_rows.append(metric_line(metrics, split, "trained_model"))

    comparison_rows = [
        "| Split | Delta Brier modelo-nulo | Delta LogLoss modelo-nulo | Delta ROC-AUC | Delta PR-AUC | Delta Lift@20% |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for split in ["train", "validation", "test"]:
        item = metrics["comparison_model_vs_null"][split]
        comparison_rows.append(
            f"| {split} | {fmt(item['brier_score_delta_model_minus_null'])} | "
            f"{fmt(item['log_loss_delta_model_minus_null'])} | {fmt(item['roc_auc_delta_model_minus_null'])} | "
            f"{fmt(item['pr_auc_delta_model_minus_null'])} | {fmt(item['lift_at_top20_delta_model_minus_null'])} |"
        )

    split_rows = [
        "| Split | N | Data inicial | Data final | Pos | Neg | Prevalencia |",
        "|---|---:|---|---|---:|---:|---:|",
    ]
    for split in ["train", "validation", "test"]:
        item = split_report["summaries"][split]
        split_rows.append(
            f"| {split} | {item['rows']} | {item['date_min']} | {item['date_max']} | "
            f"{item['positive']} | {item['negative']} | {fmt(item['prevalence'])} |"
        )

    report = f"""# Baseline In-Game V1 Results

Gerado em: {datetime.now().isoformat(timespec='seconds')}

## Resumo Executivo

Baseline In-Game V1 executado em rodada controlada com cutoff 75, features H6/H9 aprovadas, target `{cfg.TARGET_COLUMN}`, split temporal 60/20/20 sem shuffle, imputacao numerica por mediana fitada apenas no treino, codificacao categorica fitada apenas no treino, baseline nulo por prevalencia do treino e modelo treinado de regressao logistica.

Status operacional: `{validation['status']}`.

Status dos criterios quantitativos: `{approval['baseline_status']}`.

Resultado no teste:

- ROC-AUC Test: {fmt(test_metrics['roc_auc'])}
- PR-AUC Test: {fmt(test_metrics['pr_auc'])}
- Prevalencia Test: {fmt(test_metrics['prevalence'])}
- ROC-AUC aprovado: {approval['roc_auc_test_pass']}
- PR-AUC aprovado: {approval['pr_auc_test_pass']}
- Brier contra nulo aprovado: {approval['brier_score_pass']}
- Log Loss contra nulo aprovado: {approval['log_loss_pass']}

## Objetivo

Avaliar se features in-game disponiveis ate o minuto 75 possuem sinal preditivo minimo para estimar a probabilidade de uma partida ter pelo menos um gol apos 75:00.

## Arquivos de Entrada

- `{cfg.INGAME_DATASET_INPUT_PATH}`
- `{cfg.INGAME_METADATA_PATH}`
- `{cfg.INGAME_VALIDATION_PATH}`
- `{cfg.DATASET_V1_INPUT_PATH}` usado somente para validar equivalencia do target, quando disponivel.

## Snapshot Oficial

- Cutoff: `{cfg.CUTOFF_MINUTE}`
- Filtro aplicado: `cutoff_minute == 75`
- Features: informacoes ate `minute <= 75`
- Target operacional: `{cfg.OPERATIONAL_TARGET_COLUMN}` em cutoff 75
- Target final do experimento: `{cfg.TARGET_COLUMN}`

## Features Usadas

Features base:

""" + "\n".join(f"- `{column}`" for column in cfg.ALLOWED_FEATURES) + f"""

Features apos codificacao:

""" + "\n".join(f"- `{column}`" for column in metrics["encoded_x_columns"]) + f"""

## Auditoria Anti-Leakage

- Whitelist oficial prevaleceu sobre blacklist: `true`.
- Target fora de X: `true`.
- Operational target fora de X: `true`.
- `match_statistics` full-match usado: `false`.
- Features pre-jogo usadas: `false`.
- xG/xGA/forecast usados: `false`.
- `score_state_group` foi derivado de `score_diff_home_until_cutoff` dentro do snapshot cutoff 75.

## Validacao do Snapshot

- Todas as linhas com `cutoff_minute = 75`: `{validation['checks']['snapshot']['all_rows_cutoff_75']}`.
- Uma linha por `match_id`: `{validation['checks']['snapshot']['match_id_unique_after_filter']}`.
- Equivalencia de target checada: `{validation['checks']['snapshot']['target_equivalence_checked']}`.
- Divergencias de target: `{validation['checks']['snapshot']['target_equivalence_mismatches']}`.

## Split Temporal

{chr(10).join(split_rows)}

## Imputacao e Codificacao

- Numericas: mediana fitada apenas no treino.
- Categorica: OneHotEncoder fitado apenas no treino, com `handle_unknown=ignore`.
- Categorias de treino: `{preprocessing_report['categorical_encoding']['train_categories']}`.
- Medianas de treino: `{preprocessing_report['numeric_imputation']['medians']}`.

## Baseline Nulo

Probabilidade constante aprendida no treino: `{fmt(metrics['null_baseline_probability'])}`.

## Metricas por Split

{chr(10).join(metric_rows)}

## Comparacao Modelo vs Baseline Nulo

Valores negativos em Brier/LogLoss indicam melhora probabilistica do modelo contra o baseline nulo.

{chr(10).join(comparison_rows)}

## Comparacao Externa com Baseline 1A

Referencia externa aprovada:

- Baseline 1A ROC-AUC Test: {cfg.BASELINE_1A_REFERENCE['roc_auc_test']:.4f}
- Baseline 1A PR-AUC Test: {cfg.BASELINE_1A_REFERENCE['pr_auc_test']:.4f}

Comparacao direta e apenas contextual, pois Baseline 1A e pre-jogo e Baseline In-Game V1 usa informacao disponivel aos 75 minutos.

## Calibration by Bins

A calibracao por bins esta registrada em `{cfg.METRICS_PATH}` para train, validation e test, tanto para baseline nulo quanto para modelo treinado.

## Decisao Final

Status dos criterios quantitativos: `{approval['baseline_status']}`.

Status operacional do artefato: `{validation['status']}`.

Esta execucao nao autoriza producao, automacao operacional, backtesting financeiro ou uso como sistema decisorio.

## Limitacoes

- Amostra de uma unica temporada EPL.
- Modelo simples e exploratorio.
- `score_state_group` precisou ser derivado operacionalmente porque a coluna nao estava materializada no dataset V1B.
- Apenas cutoff 75 foi avaliado; comparacao de cutoffs 60/65/70/75 permanece fora do V1.
- Nenhum threshold decisorio foi aprovado.

## Recomendacoes

1. Quant Research deve revisar ROC-AUC Test, PR-AUC Test e comparacao contra baseline nulo.
2. PM deve decidir se o resultado autoriza nova iteracao metodologica.
3. Nao avancar para producao nem backtesting financeiro.
4. Se aprovado futuramente, planejar Baseline In-Game V2 para comparar cutoffs.

## Artefatos Gerados

- `{cfg.BASELINE_DATASET_PATH}`
- `{cfg.TRAIN_DATASET_PATH}`
- `{cfg.VALIDATION_DATASET_PATH}`
- `{cfg.TEST_DATASET_PATH}`
- `{cfg.FEATURE_MANIFEST_PATH}`
- `{cfg.SPLIT_REPORT_PATH}`
- `{cfg.PREPROCESSING_REPORT_PATH}`
- `{cfg.METRICS_PATH}`
- `{cfg.VALIDATION_REPORT_PATH}`
"""
    cfg.DOC_REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cfg.DOC_REPORT_PATH.write_text(report, encoding="utf-8")


def main() -> None:
    print("Building Baseline In-Game V1 dataset...")
    dataset, manifest = build_baseline_ingame_dataset()
    cfg.BASELINE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    cfg.REPORT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(cfg.BASELINE_DATASET_PATH, index=False)

    splits, split_report = split_dataset(dataset)
    transformed_splits, preprocessor, preprocessing_report = fit_transform_preprocess(splits)
    transformed_features = preprocessing_report["transformed_feature_names"]

    transformed_splits["train"].to_csv(cfg.TRAIN_DATASET_PATH, index=False)
    transformed_splits["validation"].to_csv(cfg.VALIDATION_DATASET_PATH, index=False)
    transformed_splits["test"].to_csv(cfg.TEST_DATASET_PATH, index=False)

    print("Training controlled in-game logistic baseline...")
    model, train_report = train_model(transformed_splits["train"], transformed_features)
    metrics = evaluate_model(model, transformed_splits, transformed_features)
    metrics["train_report"] = train_report
    validation = validation_report(manifest, split_report, preprocessing_report, metrics)

    write_json(cfg.FEATURE_MANIFEST_PATH, manifest)
    write_json(cfg.SPLIT_REPORT_PATH, split_report)
    write_json(cfg.PREPROCESSING_REPORT_PATH, preprocessing_report)
    write_json(cfg.METRICS_PATH, metrics)
    write_json(cfg.VALIDATION_REPORT_PATH, validation)
    write_markdown_report(metrics, split_report, preprocessing_report, validation)

    print("Baseline In-Game V1 controlled run completed.")
    print(f"Rows: {len(dataset)}")
    print(f"Train/Validation/Test: {len(transformed_splits['train'])}/{len(transformed_splits['validation'])}/{len(transformed_splits['test'])}")
    print(f"Status: {validation['status']}")
    print(f"Criteria status: {metrics['approval_checks']['baseline_status']}")
    print(f"ROC-AUC Test: {fmt(metrics['approval_checks']['roc_auc_test'])}")
    print(f"PR-AUC Test: {fmt(metrics['approval_checks']['pr_auc_test'])}")
    print(f"Report: {cfg.DOC_REPORT_PATH}")


if __name__ == "__main__":
    main()
