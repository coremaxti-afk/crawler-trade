"""Wrapper operacional do discovery V2 com ajustes locais.

Este arquivo aplica os ajustes usados na frente LaLiga/tempos expandidos sem duplicar
integralmente o script base. Ele estende targets, aliases e formato de exportacao.
"""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path
from typing import Any

BASE_PATH = Path(__file__).with_name("sportmonks_team_side_strategy_discovery_v2.py")


def load_base_module():
    spec = importlib.util.spec_from_file_location("sportmonks_discovery_v2_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Nao foi possivel carregar script base: {BASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def patch_targets(module: Any) -> None:
    module.TARGETS_UNDER = [
        (60, 75), (60, 80), (60, 85), (60, 90),
        (65, 75), (65, 80), (65, 85), (65, 90),
        (70, 85), (70, 90),
        (75, 85), (75, 90),
        (80, 90),
    ]
    module.TARGETS_OVER = [
        (60, 70), (60, 75), (60, 80), (60, 85), (60, 90),
        (65, 75), (65, 80), (65, 85), (65, 90),
        (70, 80), (70, 85), (70, 90),
        (75, 85), (75, 90),
        (80, 90),
    ]


def patch_aliases(module: Any) -> None:
    module.TEAM_ALIASES.update(
        {
            "athletic club": "athletic bilbao",
            "ath bilbao": "athletic bilbao",
            "athletic bilbao": "athletic bilbao",
            "atletico de madrid": "atletico madrid",
            "atlético de madrid": "atletico madrid",
            "atletico madrid": "atletico madrid",
            "ath madrid": "atletico madrid",
            "fc barcelona": "barcelona",
            "barcelona": "barcelona",
            "real betis": "real betis",
            "betis": "real betis",
            "real sociedad": "real sociedad",
            "sociedad": "real sociedad",
            "rayo vallecano": "rayo vallecano",
            "vallecano": "rayo vallecano",
            "deportivo alaves": "deportivo alaves",
            "deportivo alavés": "deportivo alaves",
            "alaves": "deportivo alaves",
            "celta de vigo": "celta vigo",
            "celta": "celta vigo",
            "celta vigo": "celta vigo",
            "espanyol": "espanyol",
            "espanol": "espanyol",
            "real oviedo": "real oviedo",
            "oviedo": "real oviedo",
            "elche": "elche",
            "getafe": "getafe",
            "girona": "girona",
            "levante": "levante",
            "mallorca": "mallorca",
            "osasuna": "osasuna",
            "real madrid": "real madrid",
            "sevilla": "sevilla",
            "valencia": "valencia",
            "villarreal": "villarreal",
        }
    )


def pct(value: Any) -> str:
    if value in ("", None):
        return "NA"
    return f"{float(value) * 100:.1f}%"


def pp(value: Any) -> str:
    if value in ("", None):
        return "NA"
    return f"{float(value) * 100:+.1f} pp"


def num(value: Any) -> str:
    if value in ("", None):
        return "NA"
    return f"{float(value):.4f}"


def patch_summary(module: Any) -> None:
    original_evaluate = module.evaluate_strategies

    def evaluate(rows, strategies):
        summary, entries = original_evaluate(rows, strategies)
        for row in summary:
            row["rate_pct"] = pct(row.get("rate"))
            row["baseline_pct"] = pct(row.get("baseline"))
            row["diff_vs_baseline_pp"] = pp(row.get("diff_vs_baseline"))
            row["odds_ratio_fmt"] = num(row.get("odds_ratio"))
            row["p_value_fmt"] = num(row.get("p_value"))
        return summary, entries

    def order_rows_for_analysis(rows):
        status_rank = {"PROMISSOR": 0, "OBSERVACAO": 1, "DESCARTADO": 2}

        def as_float(value, default=-999.0):
            try:
                if value in ("", None):
                    return default
                return float(value)
            except (TypeError, ValueError):
                return default

        return sorted(
            rows,
            key=lambda row: (
                status_rank.get(str(row.get("status")), 9),
                -as_float(row.get("diff_vs_baseline")),
                -as_float(row.get("rate")),
                -as_float(row.get("N")),
            ),
        )

    def write_csv(path, rows, fieldnames=None):
        path.parent.mkdir(parents=True, exist_ok=True)
        if fieldnames is None:
            fieldnames = []
            for row in rows:
                for key in row:
                    if key not in fieldnames:
                        fieldnames.append(key)
        if "summary" in path.name:
            rows = order_rows_for_analysis(rows)
        with path.open("w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(rows)

    module.evaluate_strategies = evaluate
    module.write_csv = write_csv
    module.pct = pct
    module.num = num


def main() -> None:
    module = load_base_module()
    patch_targets(module)
    patch_aliases(module)
    patch_summary(module)
    module.main()


if __name__ == "__main__":
    main()
