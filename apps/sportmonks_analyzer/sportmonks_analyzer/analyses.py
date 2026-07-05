from __future__ import annotations

from typing import Any

import pandas as pd


MINUTE_CANDIDATES = ["minute", "time.minute", "time", "game_time", "elapsed", "period.minute"]
TYPE_CANDIDATES = ["type", "type.name", "event_type", "name", "code"]
VALUE_CANDIDATES = ["value", "count", "total", "amount", "data.value"]
PARTICIPANT_CANDIDATES = ["participant_id", "team_id", "participant.id", "team.id"]


def _first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    normalized = {str(column).lower(): column for column in df.columns}
    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]
    return None


def _to_number(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def data_quality_summary(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for name, df in tables.items():
        null_cells = int(df.isna().sum().sum()) if not df.empty else 0
        total_cells = int(df.shape[0] * df.shape[1]) if not df.empty else 0
        rows.append(
            {
                "table": name,
                "rows": len(df),
                "columns": len(df.columns),
                "null_cells": null_cells,
                "null_pct": round(null_cells / total_cells * 100, 2) if total_cells else 0,
                "columns_preview": ", ".join(map(str, list(df.columns[:12]))),
            }
        )
    return pd.DataFrame(rows).sort_values(["rows", "columns"], ascending=False)


def coverage_summary(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    fixtures = tables.get("fixtures")
    if fixtures is None or fixtures.empty:
        return pd.DataFrame()

    bool_columns = [column for column in fixtures.columns if str(column).startswith("has_")]
    if not bool_columns:
        return pd.DataFrame()

    rows = []
    total = len(fixtures)
    for column in bool_columns:
        count = int(fixtures[column].fillna(False).astype(bool).sum())
        rows.append({"category": column.replace("has_", ""), "fixtures": count, "coverage_pct": round(count / total * 100, 2)})
    return pd.DataFrame(rows).sort_values("coverage_pct", ascending=False)


def find_goal_events(df: pd.DataFrame, minute_threshold: int = 75) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()

    minute_col = _first_existing_column(df, MINUTE_CANDIDATES)
    type_col = _first_existing_column(df, TYPE_CANDIDATES)
    if minute_col is None or type_col is None:
        return pd.DataFrame()

    work = df.copy()
    work["_minute"] = _to_number(work[minute_col])
    work["_type_text"] = work[type_col].astype(str).str.lower()
    goal_mask = work["_type_text"].str.contains("goal|gol", regex=True, na=False)
    work = work[goal_mask & (work["_minute"] >= minute_threshold)]
    if work.empty:
        return pd.DataFrame()

    columns = [column for column in ["fixture_id", minute_col, type_col, "participant_id", "player_name", "player.name"] if column in work.columns]
    if not columns:
        columns = list(work.columns[:8])
    return work[columns].sort_values(["fixture_id", minute_col] if "fixture_id" in columns else [minute_col])


def late_goal_summary(events: pd.DataFrame | None, timeline: pd.DataFrame | None, minute_threshold: int = 75) -> pd.DataFrame:
    candidates = []
    if events is not None and not events.empty:
        candidates.append(events)
    if timeline is not None and not timeline.empty:
        candidates.append(timeline)

    all_goals = []
    for df in candidates:
        goals = find_goal_events(df, minute_threshold=minute_threshold)
        if not goals.empty:
            all_goals.append(goals)

    if not all_goals:
        return pd.DataFrame()

    goals_df = pd.concat(all_goals, ignore_index=True, sort=False)
    if "fixture_id" not in goals_df.columns:
        return pd.DataFrame({"metric": ["late_goals"], "value": [len(goals_df)]})

    return (
        goals_df.groupby("fixture_id")
        .size()
        .reset_index(name="late_goals")
        .sort_values("late_goals", ascending=False)
    )


def pressure_window_summary(trends: pd.DataFrame | None, cutoff: int = 75, window: int = 10) -> pd.DataFrame:
    if trends is None or trends.empty:
        return pd.DataFrame()

    minute_col = _first_existing_column(trends, MINUTE_CANDIDATES)
    type_col = _first_existing_column(trends, TYPE_CANDIDATES)
    value_col = _first_existing_column(trends, VALUE_CANDIDATES)
    participant_col = _first_existing_column(trends, PARTICIPANT_CANDIDATES)

    if minute_col is None or type_col is None or value_col is None:
        return pd.DataFrame()

    work = trends.copy()
    work["_minute"] = _to_number(work[minute_col])
    work["_value"] = _to_number(work[value_col])
    work = work.dropna(subset=["_minute", "_value"])
    work = work[work["_minute"] <= cutoff]
    if work.empty:
        return pd.DataFrame()

    group_cols = [column for column in ["fixture_id", participant_col, type_col] if column is not None and column in work.columns]
    if not group_cols:
        group_cols = [type_col]

    rows: list[dict[str, Any]] = []
    start_minute = max(0, cutoff - window)
    for keys, group in work.groupby(group_cols, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        group = group.sort_values("_minute")
        before = group[group["_minute"] <= start_minute]
        after = group[group["_minute"] <= cutoff]
        if after.empty:
            continue
        start_value = float(before.iloc[-1]["_value"]) if not before.empty else 0.0
        end_value = float(after.iloc[-1]["_value"])
        row = {column: value for column, value in zip(group_cols, keys)}
        row.update(
            {
                "cutoff": cutoff,
                "window": window,
                "start_minute": start_minute,
                "start_value": start_value,
                "end_value": end_value,
                "delta": max(0.0, end_value - start_value),
            }
        )
        rows.append(row)

    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values("delta", ascending=False)


def odds_favorite_summary(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[pd.DataFrame] = []
    for name, df in tables.items():
        required = {"AvgH", "AvgD", "AvgA"}
        if not required.issubset(set(map(str, df.columns))):
            continue
        work = df.copy()
        work["_source_table"] = name
        for column in ["AvgH", "AvgD", "AvgA"]:
            work[column] = _to_number(work[column])
        work = work.dropna(subset=["AvgH", "AvgD", "AvgA"])
        if work.empty:
            continue

        work["favorite_side"] = work[["AvgH", "AvgA"]].idxmin(axis=1).map({"AvgH": "home", "AvgA": "away"})
        work["favorite_odd"] = work[["AvgH", "AvgA"]].min(axis=1)
        work["implied_home_raw"] = 1 / work["AvgH"]
        work["implied_draw_raw"] = 1 / work["AvgD"]
        work["implied_away_raw"] = 1 / work["AvgA"]
        total = work[["implied_home_raw", "implied_draw_raw", "implied_away_raw"]].sum(axis=1)
        work["favorite_prob_norm"] = work.apply(
            lambda row: (row["implied_home_raw"] if row["favorite_side"] == "home" else row["implied_away_raw"]) / total.loc[row.name],
            axis=1,
        )
        work["favorite_band"] = pd.cut(
            work["favorite_odd"],
            bins=[0, 1.65, 2.10, 99],
            labels=["favorito_forte", "favorito_medio", "sem_favorito_claro"],
        )
        rows.append(work)

    if not rows:
        return pd.DataFrame()

    result = pd.concat(rows, ignore_index=True, sort=False)
    keep = [column for column in ["_source_table", "Date", "Time", "HomeTeam", "AwayTeam", "AvgH", "AvgD", "AvgA", "favorite_side", "favorite_odd", "favorite_prob_norm", "favorite_band"] if column in result.columns]
    return result[keep].sort_values("favorite_odd")
