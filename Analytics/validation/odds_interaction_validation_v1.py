"""Run controlled Odds Interaction Validation V1.

File-only analysis:
- reads Dataset Odds V1, Dataset H8 V1 and V1B in-game match state;
- evaluates the pre-approved interactions from ODDS_INTERACTION_PLAN_V1;
- uses cutoff 60 as the primary decision point;
- evaluates 65/70/75 only for interactions classified as MANTER/OBSERVAR at 60;
- writes Markdown plus JSON metrics/report artifacts.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from scipy.stats import fisher_exact

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ODDS_DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_odds_v1.csv"
H8_DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_h8_v1.csv"
INGAME_DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_v1b_ingame.csv"
OUTPUT_DOC_PATH = PROJECT_ROOT / "docs" / "04_RESEARCH" / "ODDS_INTERACTION_VALIDATION_RESULTS_V1.md"
OUTPUT_REPORT_DIR = PROJECT_ROOT / "data" / "processed" / "reports"
OUTPUT_METRICS_PATH = OUTPUT_REPORT_DIR / "odds_interaction_validation_v1_metrics.json"
OUTPUT_REPORT_JSON_PATH = OUTPUT_REPORT_DIR / "odds_interaction_validation_v1_report.json"

PRIMARY_CUTOFF = 60
ROBUSTNESS_CUTOFFS = [65, 70, 75]
ALL_CUTOFFS = [60, 65, 70, 75]
TARGET_BY_CUTOFF = {
    60: "goal_after_60",
    65: "goal_after_65",
    70: "goal_after_70",
    75: "goal_after_75",
}


@dataclass(frozen=True)
class InteractionSpec:
    group: str
    name: str
    odds_component: str
    dynamic_component: str
    dynamic_type: str
    description: str


INTERACTIONS = [
    InteractionSpec("A - favorite_strength + H8", "favorite_strength_high + shots_last_10m_high", "favorite_strength_high", "shots_last_10m_high", "h8", "Favorito forte com alta atividade de finalizacao nos 10 minutos anteriores ao cutoff."),
    InteractionSpec("A - favorite_strength + H8", "favorite_strength_high + momentum_trend_last_10m_positive", "favorite_strength_high", "momentum_trend_last_10m_positive", "h8", "Favorito forte com tendencia positiva de momentum nos 10 minutos anteriores ao cutoff."),
    InteractionSpec("A - favorite_strength + H8", "favorite_strength_low + shots_last_10m_high", "favorite_strength_low", "shots_last_10m_high", "h8", "Jogo sem favorito forte com alta atividade de finalizacao nos 10 minutos anteriores ao cutoff."),
    InteractionSpec("B - match_balance + H8", "match_balance_high + shots_last_10m_high", "match_balance_high", "shots_last_10m_high", "h8", "Jogo equilibrado pre-jogo com alta atividade de finalizacao nos 10 minutos anteriores ao cutoff."),
    InteractionSpec("B - match_balance + H8", "match_balance_high + momentum_trend_last_10m_positive", "match_balance_high", "momentum_trend_last_10m_positive", "h8", "Jogo equilibrado pre-jogo com tendencia positiva de momentum nos 10 minutos anteriores ao cutoff."),
    InteractionSpec("B - match_balance + H8", "match_balance_low + shots_last_10m_high", "match_balance_low", "shots_last_10m_high", "h8", "Jogo desequilibrado pre-jogo com alta atividade de finalizacao nos 10 minutos anteriores ao cutoff."),
    InteractionSpec("C - favorite_strength + Match State", "favorite_strength_high + empate_aos_cutoff", "favorite_strength_high", "draw_at_cutoff", "match_state", "Favorito forte em jogo empatado no cutoff."),
    InteractionSpec("C - favorite_strength + Match State", "favorite_strength_high + favorito_perdendo_aos_cutoff", "favorite_strength_high", "favorite_losing_at_cutoff", "match_state", "Favorito forte perdendo no cutoff."),
    InteractionSpec("C - favorite_strength + Match State", "favorite_strength_high + favorito_vencendo_por_1_aos_cutoff", "favorite_strength_high", "favorite_winning_by_1_at_cutoff", "match_state", "Favorito forte vencendo por 1 no cutoff."),
    InteractionSpec("D - match_balance + Match State", "match_balance_high + empate_aos_cutoff", "match_balance_high", "draw_at_cutoff", "match_state", "Jogo equilibrado pre-jogo e empatado no cutoff."),
    InteractionSpec("D - match_balance + Match State", "match_balance_high + total_goals_until_cutoff_eq_2_or_3", "match_balance_high", "total_goals_2_or_3_at_cutoff", "match_state", "Jogo equilibrado pre-jogo com 2 ou 3 gols ja marcados no cutoff."),
    InteractionSpec("D - match_balance + Match State", "match_balance_low + empate_aos_cutoff", "match_balance_low", "draw_at_cutoff", "match_state", "Jogo desequilibrado pre-jogo e empatado no cutoff."),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run controlled Odds Interaction Validation V1.")
    parser.add_argument("--odds", default=str(ODDS_DATASET_PATH))
    parser.add_argument("--h8", default=str(H8_DATASET_PATH))
    parser.add_argument("--ingame", default=str(INGAME_DATASET_PATH))
    parser.add_argument("--output-doc", default=str(OUTPUT_DOC_PATH))
    parser.add_argument("--output-report-dir", default=str(OUTPUT_REPORT_DIR))
    return parser.parse_args()


def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    return str(value)


def classify_score_state(diff: int | float) -> str:
    if diff == 0:
        return "draw"
    if diff == 1:
        return "home_leading_by_1"
    if diff == -1:
        return "away_leading_by_1"
    if diff >= 2:
        return "home_leading_by_2plus"
    return "away_leading_by_2plus"


def load_analysis_frame(odds_path: Path, h8_path: Path, ingame_path: Path) -> pd.DataFrame:
    odds = pd.read_csv(odds_path)
    h8 = pd.read_csv(h8_path)
    ingame = pd.read_csv(ingame_path)

    h8_cols = [
        "match_id",
        "sofascore_event_id",
        "cutoff_minute",
        "shots_last_10m",
        "momentum_trend_last_10m",
    ]
    ingame_cols = [
        "match_id",
        "sofascore_event_id",
        "cutoff_minute",
        "score_diff_home_until_cutoff",
        "total_goals_until_cutoff",
        "target_goal_after_cutoff",
    ]
    odds_cols = [
        "match_id",
        "sofascore_event_id",
        "match_date",
        "home_team",
        "away_team",
        "favorite_strength",
        "match_balance",
        "favorite_side",
        "implied_prob_over25_norm",
    ]

    df = h8[h8["cutoff_minute"].isin(ALL_CUTOFFS)][h8_cols].merge(
        ingame[ingame["cutoff_minute"].isin(ALL_CUTOFFS)][ingame_cols],
        on=["match_id", "sofascore_event_id", "cutoff_minute"],
        how="inner",
        validate="one_to_one",
    )
    df = df.merge(odds[odds_cols], on=["match_id", "sofascore_event_id"], how="inner", validate="many_to_one")
    df["match_date"] = pd.to_datetime(df["match_date"])
    df["score_state_group"] = df["score_diff_home_until_cutoff"].apply(classify_score_state)
    df["target"] = df["target_goal_after_cutoff"].astype(int)
    return df.sort_values(["cutoff_minute", "match_date", "match_id"]).reset_index(drop=True)


def add_component_flags(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    out = df.copy()
    odds_base = out.drop_duplicates("match_id")
    thresholds = {
        "favorite_strength_high_q75": float(odds_base["favorite_strength"].quantile(0.75)),
        "favorite_strength_low_q25": float(odds_base["favorite_strength"].quantile(0.25)),
        "match_balance_high_q75": float(odds_base["match_balance"].quantile(0.75)),
        "match_balance_low_q25": float(odds_base["match_balance"].quantile(0.25)),
    }
    out["favorite_strength_high"] = out["favorite_strength"] >= thresholds["favorite_strength_high_q75"]
    out["favorite_strength_low"] = out["favorite_strength"] <= thresholds["favorite_strength_low_q25"]
    out["match_balance_high"] = out["match_balance"] >= thresholds["match_balance_high_q75"]
    out["match_balance_low"] = out["match_balance"] <= thresholds["match_balance_low_q25"]

    shot_thresholds: dict[int, float] = {}
    for cutoff, group in out.groupby("cutoff_minute"):
        threshold = float(group["shots_last_10m"].quantile(0.75))
        shot_thresholds[int(cutoff)] = threshold
        mask = out["cutoff_minute"].eq(cutoff)
        out.loc[mask, "shots_last_10m_high"] = out.loc[mask, "shots_last_10m"] >= threshold

    out["momentum_trend_last_10m_positive"] = out["momentum_trend_last_10m"] > 0
    out["draw_at_cutoff"] = out["score_diff_home_until_cutoff"] == 0
    out["favorite_losing_at_cutoff"] = (
        (out["favorite_side"].eq("home") & out["score_diff_home_until_cutoff"].lt(0))
        | (out["favorite_side"].eq("away") & out["score_diff_home_until_cutoff"].gt(0))
    )
    out["favorite_winning_by_1_at_cutoff"] = (
        (out["favorite_side"].eq("home") & out["score_diff_home_until_cutoff"].eq(1))
        | (out["favorite_side"].eq("away") & out["score_diff_home_until_cutoff"].eq(-1))
    )
    out["total_goals_2_or_3_at_cutoff"] = out["total_goals_until_cutoff"].isin([2, 3])
    thresholds["shots_last_10m_high_q75_by_cutoff"] = shot_thresholds
    return out, thresholds


def odds_ratio_ci(table: list[list[int]]) -> tuple[float | None, float | None, float | None]:
    a, b = table[0]
    c, d = table[1]
    if min(a, b, c, d) == 0:
        ah, bh, ch, dh = a + 0.5, b + 0.5, c + 0.5, d + 0.5
    else:
        ah, bh, ch, dh = a, b, c, d
    odds_ratio = (ah * dh) / (bh * ch)
    se = math.sqrt((1 / ah) + (1 / bh) + (1 / ch) + (1 / dh))
    log_or = math.log(odds_ratio)
    ci_low = math.exp(log_or - 1.96 * se)
    ci_high = math.exp(log_or + 1.96 * se)
    return float(odds_ratio), float(ci_low), float(ci_high)


def evaluate_mask(frame: pd.DataFrame, mask: pd.Series) -> dict[str, Any]:
    target = frame["target"].astype(int)
    in_group = mask.fillna(False).astype(bool)
    positives = int(target[in_group].sum())
    n = int(in_group.sum())
    negatives = n - positives
    baseline_pos = int(target.sum())
    baseline_n = int(len(target))
    baseline_neg = baseline_n - baseline_pos
    outside_pos = baseline_pos - positives
    outside_neg = baseline_neg - negatives
    table = [[positives, negatives], [outside_pos, outside_neg]]
    if n == 0 or n == baseline_n:
        p_value = None
        fisher_or = None
    else:
        fisher_or, p_value = fisher_exact(table, alternative="two-sided")
    or_value, ci_low, ci_high = odds_ratio_ci(table)
    rate = positives / n if n else None
    baseline_rate = baseline_pos / baseline_n if baseline_n else None
    diff_pp = (rate - baseline_rate) * 100 if rate is not None and baseline_rate is not None else None
    return {
        "n": n,
        "positives": positives,
        "negatives": negatives,
        "positive_rate": rate,
        "baseline_n": baseline_n,
        "baseline_positives": baseline_pos,
        "baseline_rate": baseline_rate,
        "diff_pp": diff_pp,
        "odds_ratio": or_value,
        "odds_ratio_fisher": None if fisher_or is None else float(fisher_or),
        "ci95_low": ci_low,
        "ci95_high": ci_high,
        "p_value": None if p_value is None else float(p_value),
        "table": table,
    }


def top_team_share(frame: pd.DataFrame, mask: pd.Series) -> dict[str, Any]:
    selected = frame[mask.fillna(False)].copy()
    if selected.empty:
        return {"top_team": None, "top_team_matches": 0, "top_team_share": None}
    teams = pd.concat([selected["home_team"], selected["away_team"]])
    counts = teams.value_counts()
    top_team = str(counts.index[0])
    # Each selected match contributes two team appearances.
    share = float(counts.iloc[0] / len(selected))
    return {"top_team": top_team, "top_team_matches": int(counts.iloc[0]), "top_team_share": share}


def classify_interaction(metrics: dict[str, Any], component_comparison: dict[str, Any], concentration: dict[str, Any]) -> str:
    n = metrics["n"]
    diff = metrics["diff_pp"]
    odds_ratio = metrics["odds_ratio"]
    p_value = metrics["p_value"]
    superior = component_comparison["superior_to_all_components"]
    top_share = concentration["top_team_share"]
    concentrated = top_share is not None and top_share > 0.45

    if (
        n >= 30
        and diff is not None
        and diff >= 8
        and odds_ratio is not None
        and odds_ratio > 1.50
        and p_value is not None
        and p_value < 0.10
        and superior
        and not concentrated
    ):
        return "MANTER"
    if n >= 20 and diff is not None and (diff >= 5 or (odds_ratio is not None and odds_ratio > 1.25)):
        return "OBSERVAR"
    return "DESCARTAR"


def evaluate_interaction(frame: pd.DataFrame, spec: InteractionSpec, cutoff: int) -> dict[str, Any]:
    cutoff_frame = frame[frame["cutoff_minute"].eq(cutoff)].copy()
    interaction_mask = cutoff_frame[spec.odds_component] & cutoff_frame[spec.dynamic_component]
    odds_mask = cutoff_frame[spec.odds_component]
    dynamic_mask = cutoff_frame[spec.dynamic_component]
    metrics = evaluate_mask(cutoff_frame, interaction_mask)
    odds_metrics = evaluate_mask(cutoff_frame, odds_mask)
    dynamic_metrics = evaluate_mask(cutoff_frame, dynamic_mask)
    concentration = top_team_share(cutoff_frame, interaction_mask)
    component_rates = {
        "odds_component": spec.odds_component,
        "odds_component_n": odds_metrics["n"],
        "odds_component_rate": odds_metrics["positive_rate"],
        "dynamic_component": spec.dynamic_component,
        "dynamic_component_n": dynamic_metrics["n"],
        "dynamic_component_rate": dynamic_metrics["positive_rate"],
        "superior_to_odds_component": (
            metrics["positive_rate"] is not None
            and odds_metrics["positive_rate"] is not None
            and metrics["positive_rate"] > odds_metrics["positive_rate"]
        ),
        "superior_to_dynamic_component": (
            metrics["positive_rate"] is not None
            and dynamic_metrics["positive_rate"] is not None
            and metrics["positive_rate"] > dynamic_metrics["positive_rate"]
        ),
    }
    component_rates["superior_to_all_components"] = bool(
        component_rates["superior_to_odds_component"] and component_rates["superior_to_dynamic_component"]
    )
    classification = classify_interaction(metrics, component_rates, concentration)
    return {
        "group": spec.group,
        "interaction": spec.name,
        "description": spec.description,
        "cutoff": cutoff,
        "target": TARGET_BY_CUTOFF[cutoff],
        **metrics,
        "component_comparison": component_rates,
        "team_concentration": concentration,
        "classification": classification,
    }


def build_results(frame: pd.DataFrame) -> dict[str, Any]:
    primary_results = [evaluate_interaction(frame, spec, PRIMARY_CUTOFF) for spec in INTERACTIONS]
    keep_or_observe = {
        item["interaction"]
        for item in primary_results
        if item["classification"] in {"MANTER", "OBSERVAR"}
    }
    robustness_results = []
    if keep_or_observe:
        for spec in INTERACTIONS:
            if spec.name not in keep_or_observe:
                continue
            for cutoff in ROBUSTNESS_CUTOFFS:
                robustness_results.append(evaluate_interaction(frame, spec, cutoff))
    return {
        "primary_results": primary_results,
        "robustness_results": robustness_results,
        "interactions_selected_for_robustness": sorted(keep_or_observe),
    }


def fmt_pct(value: float | None, digits: int = 1) -> str:
    if value is None or pd.isna(value):
        return "NA"
    return f"{value * 100:.{digits}f}%"


def fmt_num(value: float | None, digits: int = 3) -> str:
    if value is None or pd.isna(value):
        return "NA"
    return f"{value:.{digits}f}"


def fmt_pp(value: float | None, digits: int = 1) -> str:
    if value is None or pd.isna(value):
        return "NA"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.{digits}f}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = [
        "Grupo",
        "Interacao",
        "Cutoff",
        "Target",
        "N",
        "Pos",
        "Neg",
        "Taxa",
        "Baseline",
        "Diff p.p.",
        "OR",
        "IC 95%",
        "p-value",
        "Comp. isolados",
        "Class.",
    ]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for item in rows:
        comp = item["component_comparison"]
        comp_text = (
            f"{comp['odds_component']}={fmt_pct(comp['odds_component_rate'])}; "
            f"{comp['dynamic_component']}={fmt_pct(comp['dynamic_component_rate'])}"
        )
        ci = f"{fmt_num(item['ci95_low'], 2)}-{fmt_num(item['ci95_high'], 2)}"
        lines.append(
            "| "
            + " | ".join(
                [
                    item["group"],
                    item["interaction"],
                    str(item["cutoff"]),
                    item["target"],
                    str(item["n"]),
                    str(item["positives"]),
                    str(item["negatives"]),
                    fmt_pct(item["positive_rate"]),
                    fmt_pct(item["baseline_rate"]),
                    fmt_pp(item["diff_pp"]),
                    fmt_num(item["odds_ratio"], 2),
                    ci,
                    fmt_num(item["p_value"], 4),
                    comp_text,
                    item["classification"],
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def summarize_rankings(primary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        primary,
        key=lambda item: (
            item["classification"] != "MANTER",
            item["classification"] != "OBSERVAR",
            -(item["diff_pp"] if item["diff_pp"] is not None else -999),
            item["p_value"] if item["p_value"] is not None else 999,
        ),
    )


def build_markdown(frame: pd.DataFrame, thresholds: dict[str, Any], results: dict[str, Any]) -> str:
    primary = results["primary_results"]
    robust = results["robustness_results"]
    ranking = summarize_rankings(primary)
    class_counts = pd.Series([item["classification"] for item in primary]).value_counts().to_dict()
    baseline_by_cutoff = {
        int(cutoff): float(group["target"].mean())
        for cutoff, group in frame.groupby("cutoff_minute")
    }
    best = ranking[0] if ranking else None
    manter = [item for item in primary if item["classification"] == "MANTER"]
    observar = [item for item in primary if item["classification"] == "OBSERVAR"]

    lines = [
        "# ODDS INTERACTION VALIDATION RESULTS V1",
        "",
        "## Resumo Executivo",
        "",
        "- Validacao controlada executada conforme `docs/04_RESEARCH/ODDS_INTERACTION_PLAN_V1.md`.",
        "- Foco principal: cutoff 60 com target `goal_after_60`.",
        "- Targets secundarios avaliados apenas para robustez de sinais `MANTER` ou `OBSERVAR` no cutoff 60.",
        f"- Amostra principal @60: {len(frame[frame['cutoff_minute'].eq(60)])} partidas.",
        f"- Baseline `goal_after_60`: {fmt_pct(baseline_by_cutoff.get(60))}.",
        f"- Classificacao @60: MANTER={class_counts.get('MANTER', 0)}, OBSERVAR={class_counts.get('OBSERVAR', 0)}, DESCARTAR={class_counts.get('DESCARTAR', 0)}.",
    ]
    if best:
        lines.append(
            f"- Melhor efeito observado @60: `{best['interaction']}` com N={best['n']}, taxa={fmt_pct(best['positive_rate'])}, diff={fmt_pp(best['diff_pp'])} p.p., OR={fmt_num(best['odds_ratio'], 2)}, p-value={fmt_num(best['p_value'], 4)} e classificacao `{best['classification']}`."
        )
    if not manter:
        lines.append("- Nenhuma interacao atingiu criterio `MANTER` no cutoff 60.")
    if observar:
        lines.append(f"- Interacoes `OBSERVAR` seguiram para robustez em 65/70/75: {', '.join('`' + item['interaction'] + '`' for item in observar)}.")
    else:
        lines.append("- Nenhuma interacao `OBSERVAR` no cutoff 60; robustez secundaria nao foi necessaria.")

    lines.extend([
        "",
        "## Metodologia",
        "",
        "- Fontes: Dataset Odds V1, Dataset H8 V1 e Dataset V1B In-Game.",
        "- Odds usadas: `favorite_strength`, `match_balance`, `favorite_side` e `implied_prob_over25_norm` apenas como auxiliar contextual.",
        "- H8 usado: `shots_last_10m` e `momentum_trend_last_10m`, sempre calculados ate o cutoff.",
        "- Match State usado: `score_state_group`, `score_diff_home_until_cutoff` e `total_goals_until_cutoff`, sempre calculados ate o cutoff.",
        "- Teste estatistico: Fisher exact test bicaudal contra o complemento do grupo.",
        "- Odds ratio e IC 95% calculados por tabela 2x2; quando houve zero em alguma celula, foi usada correcao de Haldane-Anscombe para o IC.",
        "- Classificacao: MANTER, OBSERVAR ou DESCARTAR conforme criterios do plano.",
        "",
        "## Cortes Aplicados",
        "",
        f"- `favorite_strength_high`: top 25%, limiar >= {thresholds['favorite_strength_high_q75']:.4f}.",
        f"- `favorite_strength_low`: bottom 25%, limiar <= {thresholds['favorite_strength_low_q25']:.4f}.",
        f"- `match_balance_high`: top 25%, limiar >= {thresholds['match_balance_high_q75']:.4f}.",
        f"- `match_balance_low`: bottom 25%, limiar <= {thresholds['match_balance_low_q25']:.4f}.",
        "- `shots_last_10m_high`: top 25% por cutoff.",
    ])
    for cutoff, threshold in thresholds["shots_last_10m_high_q75_by_cutoff"].items():
        lines.append(f"  - cutoff {cutoff}: limiar >= {threshold:.2f}.")
    lines.extend([
        "- `momentum_trend_last_10m_positive`: `momentum_trend_last_10m > 0`.",
        "",
        "## Baseline Por Cutoff",
        "",
        "| Cutoff | Target | N | Positivos | Taxa |",
        "| --- | --- | --- | --- | --- |",
    ])
    for cutoff in ALL_CUTOFFS:
        group = frame[frame["cutoff_minute"].eq(cutoff)]
        lines.append(
            f"| {cutoff} | {TARGET_BY_CUTOFF[cutoff]} | {len(group)} | {int(group['target'].sum())} | {fmt_pct(group['target'].mean())} |"
        )

    lines.extend([
        "",
        "## Resultados Cutoff 60",
        "",
        markdown_table(primary),
        "",
        "## Ranking @60",
        "",
        "| Rank | Interacao | Classificacao | N | Taxa | Diff p.p. | OR | p-value | Superior aos componentes? |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ])
    for idx, item in enumerate(ranking, start=1):
        comp = item["component_comparison"]
        lines.append(
            f"| {idx} | {item['interaction']} | {item['classification']} | {item['n']} | {fmt_pct(item['positive_rate'])} | {fmt_pp(item['diff_pp'])} | {fmt_num(item['odds_ratio'], 2)} | {fmt_num(item['p_value'], 4)} | {comp['superior_to_all_components']} |"
        )

    lines.extend([
        "",
        "## Robustez 65/70/75",
        "",
    ])
    if robust:
        lines.append(markdown_table(robust))
    else:
        lines.append("Nenhuma interacao em cutoff 60 foi classificada como MANTER ou OBSERVAR; robustez secundaria nao foi executada.")

    lines.extend([
        "",
        "## Comparacao Com Componentes Isolados",
        "",
        "- A coluna `Comp. isolados` nas tabelas reporta a taxa do componente odds isolado e do componente H8/Match State isolado.",
        "- Uma interacao so atende integralmente o criterio `MANTER` quando supera ambos os componentes isolados, alem de N, efeito, OR e p-value.",
        "- Nos resultados @60, os sinais fortes foram avaliados contra seus componentes equivalentes para reduzir risco de atribuir ao par uma informacao que ja estava em um componente isolado.",
        "",
        "## Respostas As Perguntas Do Plano",
        "",
    ])
    superior_any = any(item["component_comparison"]["superior_to_all_components"] for item in primary)
    h8_superior = any(
        item["component_comparison"]["superior_to_dynamic_component"]
        for item in primary
        if "H8" in item["group"]
    )
    match_state_superior = any(
        item["component_comparison"]["superior_to_dynamic_component"]
        for item in primary
        if "Match State" in item["group"]
    )
    lines.extend([
        f"1. Existe interacao superior aos componentes isolados? {'Sim' if superior_any else 'Nao'} em pelo menos uma combinacao @60.",
        f"2. Existe interacao superior ao H8 isolado? {'Sim' if h8_superior else 'Nao'} nas combinacoes Odds + H8 @60.",
        f"3. Existe interacao superior ao Match State isolado? {'Sim' if match_state_superior else 'Nao'} nas combinacoes Odds + Match State @60.",
    ])
    if best:
        lines.append(f"4. Maior efeito observado: `{best['interaction']}`.")
    lines.append(f"5. Existe pelo menos uma interacao MANTER? {'Sim' if manter else 'Nao'}.")

    lines.extend([
        "",
        "## Regras Anti-Leakage Confirmadas",
        "",
        "- Odds usadas sao pre-jogo/closing Football-Data; nenhuma odd live/in-play foi usada.",
        "- Asian Handicap nao foi usado.",
        "- H8 usa somente dados ate o cutoff correspondente.",
        "- Match State usa somente placar/eventos ate o cutoff correspondente.",
        "- Target usa somente `target_goal_after_cutoff` do cutoff correspondente.",
        "- Placar final e estatisticas full-match nao foram usados como features.",
        "- Cutoff 60 foi avaliado primeiro e nao foi escolhido retroativamente.",
        "",
        "## Limitacoes",
        "",
        "- Football-Data nao fornece timestamp individual das closing odds; a semantica closing foi tratada como pre-jogo conforme documentado.",
        "- A amostra de interacoes pode ficar pequena apos cruzamentos.",
        "- Uma unica temporada limita inferencia estatistica.",
        "- P-values nao foram ajustados para multipla testagem; por isso classificacoes `OBSERVAR` devem ser tratadas como exploratorias.",
        "- Alguns sinais podem refletir componentes isolados, por isso a comparacao contra odds/H8/Match State isolados foi reportada.",
        "",
        "## Recomendacao Quant",
        "",
    ])
    if manter:
        lines.append("- Recomendacao: manter as interacoes `MANTER` como candidatas para uma validacao estatistica expandida antes de qualquer baseline.")
    elif observar:
        lines.append("- Recomendacao: observar os sinais classificados como `OBSERVAR`; nao autorizar baseline ainda sem revisao Quant da robustez.")
    else:
        lines.append("- Recomendacao: descartar esta formulacao Odds Interaction V1 para baseline imediato; odds podem permanecer como contexto auxiliar, mas nao ha sinal estatistico suficiente nesta execucao controlada.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    odds_path = Path(args.odds)
    h8_path = Path(args.h8)
    ingame_path = Path(args.ingame)
    output_doc = Path(args.output_doc)
    output_report_dir = Path(args.output_report_dir)
    output_report_dir.mkdir(parents=True, exist_ok=True)
    output_doc.parent.mkdir(parents=True, exist_ok=True)

    frame = load_analysis_frame(odds_path, h8_path, ingame_path)
    frame, thresholds = add_component_flags(frame)
    results = build_results(frame)
    markdown = build_markdown(frame, thresholds, results)
    output_doc.write_text(markdown, encoding="utf-8")

    report = {
        "report_name": "odds_interaction_validation_v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": {
            "odds_dataset": str(odds_path),
            "h8_dataset": str(h8_path),
            "ingame_dataset": str(ingame_path),
        },
        "cutoff_policy": {
            "primary_cutoff": PRIMARY_CUTOFF,
            "robustness_cutoffs": ROBUSTNESS_CUTOFFS,
            "robustness_only_for": "MANTER or OBSERVAR at cutoff 60",
        },
        "thresholds": thresholds,
        "row_count": int(len(frame)),
        "matches_by_cutoff": {str(k): int(v) for k, v in frame.groupby("cutoff_minute")["match_id"].nunique().to_dict().items()},
        "primary_results": results["primary_results"],
        "robustness_results": results["robustness_results"],
        "interactions_selected_for_robustness": results["interactions_selected_for_robustness"],
        "anti_leakage": {
            "no_model": True,
            "no_baseline": True,
            "no_backtesting": True,
            "no_production": True,
            "no_asian_handicap": True,
            "no_live_inplay_odds": True,
            "h8_features_use_cutoff": True,
            "match_state_uses_cutoff": True,
            "target_after_cutoff": True,
        },
    }
    OUTPUT_METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_METRICS_PATH.write_text(json.dumps(results, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")
    OUTPUT_REPORT_JSON_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")

    print("FINAL SUMMARY")
    print(f"rows={len(frame)}")
    print(f"primary_results={len(results['primary_results'])}")
    print(f"robustness_results={len(results['robustness_results'])}")
    print(f"selected_for_robustness={results['interactions_selected_for_robustness']}")
    print(f"doc={output_doc}")
    print(f"metrics={OUTPUT_METRICS_PATH}")
    print(f"report_json={OUTPUT_REPORT_JSON_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
