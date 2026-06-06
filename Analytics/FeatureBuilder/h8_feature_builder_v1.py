"""Build H8 Graph/Shotmap feature set V1.

Read-only PostgreSQL flow:
- reads matches_master, match_graph, match_shotmap and match_source_status;
- builds one row per match_id + cutoff_minute;
- computes only whitelisted H8 features with minute <= cutoff;
- keeps Graph and Shotmap features separated and auditable;
- writes CSV, Parquet, metadata and validation report locally.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import engine  # noqa: E402

FEATURE_SET_NAME = "h8_features_v1"
FEATURE_SET_VERSION = "v1"
KNOWN_SKIPPED_MATCH_IDS = {"12436452"}
KNOWN_MISSING_GRAPH_EVENT_IDS = {12437015}
EXPECTED_MATCHES = 380
CUTOFFS = [60, 65, 70, 75]
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "features"
CSV_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}.csv"
PARQUET_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}.parquet"
METADATA_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}_metadata.json"
VALIDATION_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}_validation_report.json"

GRAPH_FEATURES = [
    "momentum_last_5m_avg",
    "momentum_last_10m_avg",
    "momentum_trend_last_10m",
    "momentum_sum_until_cutoff",
]
SHOTMAP_FEATURES = [
    "xg_last_5m",
    "xg_last_10m",
    "shots_last_5m",
    "shots_last_10m",
    "xg_sum_until_cutoff",
]
WHITELIST_FEATURES = GRAPH_FEATURES + SHOTMAP_FEATURES
OUTPUT_COLUMNS = [
    "match_id",
    "sofascore_event_id",
    "league",
    "season",
    "match_date",
    "home_team",
    "away_team",
    "cutoff_minute",
    "graph_available",
    "graph_known_missing",
    "shotmap_available",
    "graph_points_until_cutoff",
    "graph_points_last_5m",
    "graph_points_last_10m",
    "shots_until_cutoff",
    *GRAPH_FEATURES,
    *SHOTMAP_FEATURES,
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build H8 Graph/Shotmap features V1 from PostgreSQL.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directory for CSV, Parquet and reports.")
    parser.add_argument(
        "--cutoffs",
        default=",".join(str(cutoff) for cutoff in CUTOFFS),
        help="Comma-separated cutoff minutes. Default: 60,65,70,75.",
    )
    return parser.parse_args()


def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    return str(value)


def parquet_engine_available() -> bool:
    return bool(importlib.util.find_spec("pyarrow") or importlib.util.find_spec("fastparquet"))


def parse_cutoffs(raw: str) -> list[int]:
    cutoffs = sorted({int(value.strip()) for value in raw.split(",") if value.strip()})
    if not cutoffs:
        raise ValueError("At least one cutoff is required.")
    if any(cutoff <= 0 for cutoff in cutoffs):
        raise ValueError("Cutoffs must be positive minutes.")
    return cutoffs


def table_counts() -> dict[str, int]:
    tables = ["matches_master", "match_graph", "match_shotmap", "match_source_status"]
    with engine.connect() as conn:
        return {table: int(conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()) for table in tables}


def fetch_matches() -> pd.DataFrame:
    sql = text(
        """
        SELECT
            match_id,
            sofascore_event_id,
            league,
            season,
            match_date,
            home_team,
            away_team
        FROM matches_master
        WHERE sofascore_event_id::text NOT IN :skipped_ids
        ORDER BY match_date, match_id
        """
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn, params={"skipped_ids": tuple(KNOWN_SKIPPED_MATCH_IDS)})
    df["sofascore_event_id"] = df["sofascore_event_id"].astype(int)
    df["match_date"] = pd.to_datetime(df["match_date"])
    return df


def fetch_graph() -> pd.DataFrame:
    sql = text(
        """
        SELECT
            sofascore_event_id,
            point_index,
            minute,
            momentum_value
        FROM match_graph
        ORDER BY sofascore_event_id, point_index
        """
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn)
    if df.empty:
        return pd.DataFrame(columns=["sofascore_event_id", "point_index", "minute", "momentum_value"])
    df["sofascore_event_id"] = df["sofascore_event_id"].astype(int)
    df["point_index"] = pd.to_numeric(df["point_index"], errors="coerce")
    df["minute"] = pd.to_numeric(df["minute"], errors="coerce")
    df["momentum_value"] = pd.to_numeric(df["momentum_value"], errors="coerce")
    return df.dropna(subset=["sofascore_event_id", "minute", "momentum_value"])


def fetch_shotmap() -> pd.DataFrame:
    sql = text(
        """
        SELECT
            sofascore_event_id,
            shot_index,
            minute,
            xg
        FROM match_shotmap
        ORDER BY sofascore_event_id, shot_index
        """
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn)
    if df.empty:
        return pd.DataFrame(columns=["sofascore_event_id", "shot_index", "minute", "xg"])
    df["sofascore_event_id"] = df["sofascore_event_id"].astype(int)
    df["shot_index"] = pd.to_numeric(df["shot_index"], errors="coerce")
    df["minute"] = pd.to_numeric(df["minute"], errors="coerce")
    df["xg"] = pd.to_numeric(df["xg"], errors="coerce").fillna(0.0)
    return df.dropna(subset=["sofascore_event_id", "minute"])


def fetch_known_missing_graph() -> set[int]:
    sql = text(
        """
        SELECT sofascore_event_id
        FROM match_source_status
        WHERE artifact_name = 'graph.json'
          AND status = 'known_missing'
        """
    )
    with engine.connect() as conn:
        values = conn.execute(sql).scalars().all()
    return {int(value) for value in values} | KNOWN_MISSING_GRAPH_EVENT_IDS


def compute_graph_features(event_graph: pd.DataFrame, cutoff: int) -> dict[str, Any]:
    until_cutoff = event_graph[event_graph["minute"].le(cutoff)].sort_values(["minute", "point_index"])
    last_5m = event_graph[event_graph["minute"].gt(cutoff - 5) & event_graph["minute"].le(cutoff)]
    last_10m = event_graph[event_graph["minute"].gt(cutoff - 10) & event_graph["minute"].le(cutoff)].sort_values(
        ["minute", "point_index"]
    )
    trend = None
    if len(last_10m) >= 2:
        trend = float(last_10m["momentum_value"].iloc[-1] - last_10m["momentum_value"].iloc[0])
    return {
        "graph_points_until_cutoff": int(len(until_cutoff)),
        "graph_points_last_5m": int(len(last_5m)),
        "graph_points_last_10m": int(len(last_10m)),
        "momentum_last_5m_avg": float(last_5m["momentum_value"].mean()) if len(last_5m) else None,
        "momentum_last_10m_avg": float(last_10m["momentum_value"].mean()) if len(last_10m) else None,
        "momentum_trend_last_10m": trend,
        "momentum_sum_until_cutoff": float(until_cutoff["momentum_value"].sum()) if len(until_cutoff) else None,
    }


def compute_shotmap_features(event_shots: pd.DataFrame, cutoff: int) -> dict[str, Any]:
    until_cutoff = event_shots[event_shots["minute"].le(cutoff)]
    last_5m = event_shots[event_shots["minute"].gt(cutoff - 5) & event_shots["minute"].le(cutoff)]
    last_10m = event_shots[event_shots["minute"].gt(cutoff - 10) & event_shots["minute"].le(cutoff)]
    return {
        "shots_until_cutoff": int(len(until_cutoff)),
        "xg_last_5m": float(last_5m["xg"].sum()) if len(last_5m) else 0.0,
        "xg_last_10m": float(last_10m["xg"].sum()) if len(last_10m) else 0.0,
        "shots_last_5m": int(len(last_5m)),
        "shots_last_10m": int(len(last_10m)),
        "xg_sum_until_cutoff": float(until_cutoff["xg"].sum()) if len(until_cutoff) else 0.0,
    }


def build_feature_dataframe(cutoffs: list[int]) -> pd.DataFrame:
    matches = fetch_matches()
    graph = fetch_graph()
    shotmap = fetch_shotmap()
    known_missing_graph = fetch_known_missing_graph()
    graph_event_ids = set(graph["sofascore_event_id"].unique())
    shotmap_event_ids = set(shotmap["sofascore_event_id"].unique())
    graph_by_event = {event_id: rows for event_id, rows in graph.groupby("sofascore_event_id", sort=False)}
    shotmap_by_event = {event_id: rows for event_id, rows in shotmap.groupby("sofascore_event_id", sort=False)}

    rows: list[dict[str, Any]] = []
    for match in matches.to_dict("records"):
        event_id = int(match["sofascore_event_id"])
        event_graph = graph_by_event.get(event_id, graph.iloc[0:0])
        event_shots = shotmap_by_event.get(event_id, shotmap.iloc[0:0])
        for cutoff in cutoffs:
            row = {
                **match,
                "cutoff_minute": cutoff,
                "graph_available": int(event_id in graph_event_ids),
                "graph_known_missing": int(event_id in known_missing_graph),
                "shotmap_available": int(event_id in shotmap_event_ids),
                **compute_graph_features(event_graph, cutoff),
                **compute_shotmap_features(event_shots, cutoff),
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    for column in OUTPUT_COLUMNS:
        if column not in df.columns:
            df[column] = None
    return df[OUTPUT_COLUMNS].sort_values(["match_date", "match_id", "cutoff_minute"]).reset_index(drop=True)


def validate_features(df: pd.DataFrame, cutoffs: list[int]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    key_duplicates = int(df.duplicated(subset=["match_id", "cutoff_minute"]).sum())
    cutoff_counts = {int(key): int(value) for key, value in df["cutoff_minute"].value_counts().sort_index().to_dict().items()}
    null_required = {
        column: int(df[column].isna().sum())
        for column in ["match_id", "sofascore_event_id", "match_date", "home_team", "away_team", "cutoff_minute"]
    }
    missing_feature_columns = [column for column in WHITELIST_FEATURES if column not in df.columns]
    extra_feature_like_columns = [
        column
        for column in df.columns
        if column.startswith("target") or "late_goal" in column or column in {"home_goals", "away_goals", "total_goals"}
    ]
    graph_rows = df[df["graph_available"].eq(1)]
    shotmap_rows = df[df["shotmap_available"].eq(1)]
    known_missing_graph_rows = df[df["graph_known_missing"].eq(1)]

    if len(df) != len(cutoffs) * EXPECTED_MATCHES:
        errors.append(f"Expected {len(cutoffs) * EXPECTED_MATCHES} rows, found {len(df)}.")
    if key_duplicates:
        errors.append(f"Duplicate match_id + cutoff_minute rows found: {key_duplicates}.")
    if set(cutoff_counts.keys()) != set(cutoffs):
        errors.append("Unexpected cutoff_minute values found.")
    if any(count != EXPECTED_MATCHES for count in cutoff_counts.values()):
        errors.append("At least one cutoff does not contain one row for every importable match.")
    if any(value > 0 for value in null_required.values()):
        errors.append("Required identifiers contain null values.")
    if missing_feature_columns:
        errors.append(f"Missing whitelisted feature columns: {missing_feature_columns}.")
    if extra_feature_like_columns:
        errors.append(f"Potential target/final-score leakage columns found: {extra_feature_like_columns}.")
    if int(df["graph_available"].sum()) != 379 * len(cutoffs):
        errors.append("Graph availability does not match expected 379 events across cutoffs.")
    if int(df["shotmap_available"].sum()) != EXPECTED_MATCHES * len(cutoffs):
        errors.append("Shotmap availability does not match expected 380 events across cutoffs.")
    if set(known_missing_graph_rows["sofascore_event_id"].astype(int).unique()) != KNOWN_MISSING_GRAPH_EVENT_IDS:
        errors.append("Known missing Graph event set does not match expected policy.")
    if graph_rows[GRAPH_FEATURES].isna().any().any():
        errors.append("Graph-available rows contain null Graph features.")
    if shotmap_rows[SHOTMAP_FEATURES].isna().any().any():
        errors.append("Shotmap-available rows contain null Shotmap features.")
    if (known_missing_graph_rows[GRAPH_FEATURES].notna().any(axis=1)).any():
        errors.append("Known-missing Graph rows contain Graph feature values.")
    if (df[["graph_points_until_cutoff", "graph_points_last_5m", "graph_points_last_10m", "shots_until_cutoff"]].fillna(0) < 0).any().any():
        errors.append("Negative count fields found.")

    warnings.append("Feature set is match-level and not team-directional; Graph momentum sign is preserved as imported.")
    warnings.append("The feature set does not include target columns by design; join with target dataset must be explicit in downstream analysis.")

    return {
        "feature_set_name": FEATURE_SET_NAME,
        "feature_set_version": FEATURE_SET_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "NAO APTO" if errors else "APTO COM RESSALVAS" if warnings else "APTO",
        "row_count": int(len(df)),
        "expected_rows": int(len(cutoffs) * EXPECTED_MATCHES),
        "unique_matches": int(df["match_id"].nunique()),
        "cutoffs": cutoffs,
        "cutoff_counts": cutoff_counts,
        "key_duplicates": key_duplicates,
        "null_required": null_required,
        "graph_available_rows": int(df["graph_available"].sum()),
        "graph_available_events": int(df[df["graph_available"].eq(1)]["sofascore_event_id"].nunique()),
        "graph_known_missing_events": sorted(int(value) for value in df[df["graph_known_missing"].eq(1)]["sofascore_event_id"].unique()),
        "shotmap_available_rows": int(df["shotmap_available"].sum()),
        "shotmap_available_events": int(df[df["shotmap_available"].eq(1)]["sofascore_event_id"].nunique()),
        "whitelist_features": WHITELIST_FEATURES,
        "graph_features": GRAPH_FEATURES,
        "shotmap_features": SHOTMAP_FEATURES,
        "anti_leakage_checks": {
            "uses_only_minute_lte_cutoff": True,
            "contains_target_columns": bool(extra_feature_like_columns),
            "contains_full_time_score_columns": bool(set(df.columns) & {"home_goals", "away_goals", "total_goals"}),
            "graph_and_shotmap_separated": True,
            "whitelist_enforced": not missing_feature_columns and not extra_feature_like_columns,
        },
        "errors": errors,
        "warnings": warnings,
    }


def build_metadata(df: pd.DataFrame, validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "feature_set_name": FEATURE_SET_NAME,
        "feature_set_version": FEATURE_SET_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "grain": "one row per match_id + cutoff_minute",
        "sources": ["matches_master", "match_graph", "match_shotmap", "match_source_status"],
        "row_count": int(len(df)),
        "cutoffs": validation["cutoffs"],
        "known_skipped_match_ids": sorted(KNOWN_SKIPPED_MATCH_IDS),
        "known_missing_graph_event_ids": sorted(KNOWN_MISSING_GRAPH_EVENT_IDS),
        "graph_features": GRAPH_FEATURES,
        "shotmap_features": SHOTMAP_FEATURES,
        "whitelist_features": WHITELIST_FEATURES,
        "output_columns": list(df.columns),
        "anti_leakage_rules": [
            "Only rows with minute <= cutoff_minute are used for every H8 feature.",
            "Graph and Shotmap features are computed separately.",
            "No target, late-goal, final-score or full-match-statistics columns are included.",
            "momentum_value is preserved as imported; no sign inversion or normalization is applied.",
            "12437015 is known_missing for graph.json and Graph features remain null for that event.",
        ],
        "validation_status": validation["status"],
    }


def write_outputs(df: pd.DataFrame, validation: dict[str, Any], metadata: dict[str, Any], output_dir: Path) -> dict[str, str | None]:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / CSV_PATH.name
    parquet_path = output_dir / PARQUET_PATH.name
    metadata_path = output_dir / METADATA_PATH.name
    validation_path = output_dir / VALIDATION_PATH.name

    df.to_csv(csv_path, index=False)
    parquet_written = False
    if parquet_engine_available():
        df.to_parquet(parquet_path, index=False)
        parquet_written = True
    else:
        validation.setdefault("warnings", []).append("Parquet not written because pyarrow/fastparquet is unavailable.")

    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")
    validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")
    return {
        "csv": str(csv_path),
        "parquet": str(parquet_path) if parquet_written else None,
        "metadata": str(metadata_path),
        "validation_report": str(validation_path),
    }


def main() -> int:
    args = parse_args()
    cutoffs = parse_cutoffs(args.cutoffs)
    output_dir = Path(args.output_dir)

    print("Building H8 Feature Set V1")
    print(f"cutoffs={cutoffs}")
    print(f"output_dir={output_dir}")
    print(f"table_counts={table_counts()}")

    df = build_feature_dataframe(cutoffs)
    validation = validate_features(df, cutoffs)
    metadata = build_metadata(df, validation)
    outputs = write_outputs(df, validation, metadata, output_dir)

    print("FINAL SUMMARY")
    print(f"rows={len(df)}")
    print(f"unique_matches={df['match_id'].nunique()}")
    print(f"graph_events={df[df['graph_available'].eq(1)]['sofascore_event_id'].nunique()}")
    print(f"shotmap_events={df[df['shotmap_available'].eq(1)]['sofascore_event_id'].nunique()}")
    print(f"status={validation['status']}")
    print(f"errors={len(validation['errors'])}")
    print(f"warnings={len(validation['warnings'])}")
    print(json.dumps(outputs, ensure_ascii=False, indent=2))
    return 1 if validation["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
