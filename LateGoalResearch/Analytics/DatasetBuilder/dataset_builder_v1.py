"""Build Dataset Analitico V1 for late goal research.

Read-only PostgreSQL flow:
- reads matches_master, match_statistics and match_incidents;
- builds one row per match;
- creates the late goal target from goal incidents after minute 75;
- writes CSV, Parquet, metadata and validation report locally.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import engine  # noqa: E402

DATASET_VERSION = "v1"
DEFAULT_LATE_MINUTE = 75
KNOWN_SKIPPED_MATCH_IDS = {"12436452"}
EXPECTED_ROWS = 380
EXPECTED_TABLE_COUNTS = {
    "matches_master": 380,
    "match_statistics": 380,
    "match_incidents": 7647,
}
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "datasets"
CSV_PATH = OUTPUT_DIR / "late_goal_dataset_v1.csv"
PARQUET_PATH = OUTPUT_DIR / "late_goal_dataset_v1.parquet"
METADATA_PATH = OUTPUT_DIR / "late_goal_dataset_v1_metadata.json"
VALIDATION_PATH = OUTPUT_DIR / "late_goal_dataset_v1_validation_report.json"

BASE_COLUMNS = [
    "match_id",
    "sofascore_event_id",
    "league",
    "season",
    "match_date",
    "home_team",
    "away_team",
    "home_goals",
    "away_goals",
    "total_goals",
    "possession_home",
    "possession_away",
    "shots_home",
    "shots_away",
    "shots_on_target_home",
    "shots_on_target_away",
    "corners_home",
    "corners_away",
    "big_chances_home",
    "big_chances_away",
    "xg_home",
    "xg_away",
    "incident_count",
    "goal_count",
    "late_goal_count_75",
    "home_late_goal_count_75",
    "away_late_goal_count_75",
    "first_late_goal_minute_75",
    "last_goal_minute",
    "card_count",
    "substitution_count",
    "has_late_goal",
    "target_late_goal_75",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build late goal analytical dataset V1 from PostgreSQL.")
    parser.add_argument("--late-minute", type=int, default=DEFAULT_LATE_MINUTE, help="Minute cutoff for late goal target.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directory for CSV, Parquet and reports.")
    return parser.parse_args()


def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    return str(value)


def table_counts() -> dict[str, int]:
    with engine.connect() as conn:
        return {table: int(conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()) for table in EXPECTED_TABLE_COUNTS}


def build_dataframe(late_minute: int) -> pd.DataFrame:
    skipped_ids = tuple(KNOWN_SKIPPED_MATCH_IDS)
    sql = text(
        """
        WITH incident_agg AS (
            SELECT
                sofascore_event_id,
                COUNT(*) AS incident_count,
                COUNT(*) FILTER (WHERE LOWER(COALESCE(incident_type, '')) = 'goal') AS goal_count,
                COUNT(*) FILTER (
                    WHERE LOWER(COALESCE(incident_type, '')) = 'goal'
                      AND minute > :late_minute
                ) AS late_goal_count_75,
                COUNT(*) FILTER (
                    WHERE LOWER(COALESCE(incident_type, '')) = 'goal'
                      AND minute > :late_minute
                      AND is_home IS true
                ) AS home_late_goal_count_75,
                COUNT(*) FILTER (
                    WHERE LOWER(COALESCE(incident_type, '')) = 'goal'
                      AND minute > :late_minute
                      AND is_home IS false
                ) AS away_late_goal_count_75,
                MIN(minute) FILTER (
                    WHERE LOWER(COALESCE(incident_type, '')) = 'goal'
                      AND minute > :late_minute
                ) AS first_late_goal_minute_75,
                MAX(minute) FILTER (WHERE LOWER(COALESCE(incident_type, '')) = 'goal') AS last_goal_minute,
                COUNT(*) FILTER (WHERE LOWER(COALESCE(incident_type, '')) = 'card') AS card_count,
                COUNT(*) FILTER (WHERE LOWER(COALESCE(incident_type, '')) = 'substitution') AS substitution_count
            FROM match_incidents
            WHERE sofascore_event_id::text NOT IN :skipped_ids
            GROUP BY sofascore_event_id
        )
        SELECT
            m.match_id,
            m.sofascore_event_id,
            m.league,
            m.season,
            m.match_date,
            m.home_team,
            m.away_team,
            m.home_goals,
            m.away_goals,
            COALESCE(m.home_goals, 0) + COALESCE(m.away_goals, 0) AS total_goals,
            s.possession_home,
            s.possession_away,
            s.shots_home,
            s.shots_away,
            s.shots_on_target_home,
            s.shots_on_target_away,
            s.corners_home,
            s.corners_away,
            s.big_chances_home,
            s.big_chances_away,
            s.xg_home,
            s.xg_away,
            COALESCE(i.incident_count, 0) AS incident_count,
            COALESCE(i.goal_count, 0) AS goal_count,
            COALESCE(i.late_goal_count_75, 0) AS late_goal_count_75,
            COALESCE(i.home_late_goal_count_75, 0) AS home_late_goal_count_75,
            COALESCE(i.away_late_goal_count_75, 0) AS away_late_goal_count_75,
            i.first_late_goal_minute_75,
            i.last_goal_minute,
            COALESCE(i.card_count, 0) AS card_count,
            COALESCE(i.substitution_count, 0) AS substitution_count,
            CASE WHEN COALESCE(i.late_goal_count_75, 0) > 0 THEN 1 ELSE 0 END AS has_late_goal,
            CASE WHEN COALESCE(i.late_goal_count_75, 0) > 0 THEN 1 ELSE 0 END AS target_late_goal_75
        FROM matches_master m
        LEFT JOIN match_statistics s ON s.sofascore_event_id = m.sofascore_event_id
        LEFT JOIN incident_agg i ON i.sofascore_event_id = m.sofascore_event_id
        WHERE m.sofascore_event_id::text NOT IN :skipped_ids
        ORDER BY m.match_date, m.match_id
        """
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn, params={"late_minute": late_minute, "skipped_ids": skipped_ids})

    for column in BASE_COLUMNS:
        if column not in df.columns:
            df[column] = None
    return df[BASE_COLUMNS]


def parquet_engine_available() -> bool:
    return bool(importlib.util.find_spec("pyarrow") or importlib.util.find_spec("fastparquet"))


def validate_dataset(df: pd.DataFrame, counts: dict[str, int], parquet_written: bool, late_minute: int) -> dict[str, Any]:
    target_counts = df["has_late_goal"].value_counts(dropna=False).sort_index().to_dict()
    duplicate_match_id_count = int(df["match_id"].duplicated().sum())
    duplicate_event_id_count = int(df["sofascore_event_id"].duplicated().sum())
    required_null_counts = {
        column: int(df[column].isna().sum())
        for column in ["match_id", "sofascore_event_id", "match_date", "home_team", "away_team", "has_late_goal"]
    }
    count_mismatches = {
        table: {"expected": expected, "actual": counts.get(table)}
        for table, expected in EXPECTED_TABLE_COUNTS.items()
        if counts.get(table) != expected
    }
    validation_errors = []
    validation_warnings = []

    if len(df) != EXPECTED_ROWS:
        validation_errors.append(f"Expected {EXPECTED_ROWS} dataset rows, found {len(df)}.")
    if duplicate_match_id_count:
        validation_errors.append(f"Duplicate match_id rows found: {duplicate_match_id_count}.")
    if duplicate_event_id_count:
        validation_errors.append(f"Duplicate sofascore_event_id rows found: {duplicate_event_id_count}.")
    if count_mismatches:
        validation_errors.append("Source table counts differ from expected import baseline.")
    if required_null_counts["has_late_goal"]:
        validation_errors.append("Target has_late_goal contains nulls.")
    if set(target_counts.keys()) != {0, 1}:
        validation_errors.append("Target does not contain both positive and negative classes.")
    if not parquet_written:
        validation_errors.append("Parquet export was not created.")

    big_chance_nulls = {
        "big_chances_home": int(df["big_chances_home"].isna().sum()),
        "big_chances_away": int(df["big_chances_away"].isna().sum()),
    }
    if any(value > 0 for value in big_chance_nulls.values()):
        validation_warnings.append("big_chances_home/big_chances_away contain known nulls and should be optional features only.")

    status = "NAO APTO" if validation_errors else "APTO COM RESSALVAS" if validation_warnings else "APTO"
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dataset_version": DATASET_VERSION,
        "late_minute_cutoff": late_minute,
        "status": status,
        "row_count": int(len(df)),
        "expected_row_count": EXPECTED_ROWS,
        "source_table_counts": counts,
        "source_count_mismatches": count_mismatches,
        "duplicate_match_id_count": duplicate_match_id_count,
        "duplicate_sofascore_event_id_count": duplicate_event_id_count,
        "required_null_counts": required_null_counts,
        "target_counts": {str(key): int(value) for key, value in target_counts.items()},
        "target_positive_count": int(df["has_late_goal"].sum()),
        "target_negative_count": int((df["has_late_goal"] == 0).sum()),
        "target_positive_rate": round(float(df["has_late_goal"].mean()), 6) if len(df) else None,
        "big_chance_nulls": big_chance_nulls,
        "late_goal_minute_min": None if df["first_late_goal_minute_75"].dropna().empty else int(df["first_late_goal_minute_75"].dropna().min()),
        "late_goal_minute_max": None if df["first_late_goal_minute_75"].dropna().empty else int(df["first_late_goal_minute_75"].dropna().max()),
        "parquet_written": parquet_written,
        "validation_errors": validation_errors,
        "validation_warnings": validation_warnings,
    }


def build_metadata(df: pd.DataFrame, validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "dataset_name": "late_goal_dataset_v1",
        "dataset_version": DATASET_VERSION,
        "generated_at": validation["generated_at"],
        "grain": "one row per match",
        "source_tables": ["matches_master", "match_statistics", "match_incidents"],
        "known_skipped_match_ids": sorted(KNOWN_SKIPPED_MATCH_IDS),
        "row_count": int(len(df)),
        "columns": list(df.columns),
        "target": {
            "primary_name": "has_late_goal",
            "alias": "target_late_goal_75",
            "definition": "1 if at least one goal incident has minute > 75; otherwise 0.",
            "source": "match_incidents",
        },
        "outputs": {
            "csv": str(CSV_PATH),
            "parquet": str(PARQUET_PATH),
            "metadata": str(METADATA_PATH),
            "validation_report": str(VALIDATION_PATH),
        },
        "caveats": [
            "Full-match statistics are included as raw analytical columns and must not be used as in-game cutoff predictors without leakage review.",
            "big_chances_home and big_chances_away contain known nulls and should remain optional in V1.",
            "match_graph, lineups and h2h are outside Dataset V1 scope.",
        ],
    }


def write_outputs(df: pd.DataFrame, output_dir: Path, late_minute: int) -> dict[str, Any]:
    global OUTPUT_DIR, CSV_PATH, PARQUET_PATH, METADATA_PATH, VALIDATION_PATH
    OUTPUT_DIR = output_dir
    CSV_PATH = OUTPUT_DIR / "late_goal_dataset_v1.csv"
    PARQUET_PATH = OUTPUT_DIR / "late_goal_dataset_v1.parquet"
    METADATA_PATH = OUTPUT_DIR / "late_goal_dataset_v1_metadata.json"
    VALIDATION_PATH = OUTPUT_DIR / "late_goal_dataset_v1_validation_report.json"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")

    parquet_written = False
    if parquet_engine_available():
        df.to_parquet(PARQUET_PATH, index=False)
        parquet_written = True

    counts = table_counts()
    validation = validate_dataset(df, counts, parquet_written, late_minute)
    metadata = build_metadata(df, validation)
    METADATA_PATH.write_text(json.dumps(metadata, indent=2, ensure_ascii=False, default=json_default), encoding="utf-8")
    VALIDATION_PATH.write_text(json.dumps(validation, indent=2, ensure_ascii=False, default=json_default), encoding="utf-8")
    return {"metadata": metadata, "validation": validation}


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    print("Building late_goal_dataset_v1 from PostgreSQL with SELECT-only queries")
    df = build_dataframe(args.late_minute)
    result = write_outputs(df, output_dir, args.late_minute)
    validation = result["validation"]

    print(f"status={validation['status']}")
    print(f"rows={validation['row_count']}")
    print(f"target_positive={validation['target_positive_count']}")
    print(f"target_negative={validation['target_negative_count']}")
    print(f"csv={CSV_PATH}")
    print(f"parquet={PARQUET_PATH if validation['parquet_written'] else 'NOT_WRITTEN'}")
    print(f"metadata={METADATA_PATH}")
    print(f"validation_report={VALIDATION_PATH}")
    if validation["validation_errors"]:
        print("validation_errors:")
        for error in validation["validation_errors"]:
            print(f"- {error}")


if __name__ == "__main__":
    main()
