"""Build Dataset V1B in-game cutoff rows for H6/H9 validation.

Read-only PostgreSQL flow:
- one row per match_id + cutoff_minute;
- features use only match_incidents with minute <= cutoff;
- target uses goal incidents after cutoff;
- no full-match statistics are used.
"""

from __future__ import annotations

import argparse
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

DATASET_NAME = "late_goal_dataset_v1b_ingame"
DATASET_VERSION = "v1b"
KNOWN_SKIPPED_MATCH_IDS = {"12436452"}
CUTOFFS = [60, 65, 70, 75, 80]
EXPECTED_MATCHES = 380
EXPECTED_ROWS = EXPECTED_MATCHES * len(CUTOFFS)
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "datasets"
CSV_PATH = OUTPUT_DIR / f"{DATASET_NAME}.csv"
METADATA_PATH = OUTPUT_DIR / f"{DATASET_NAME}_metadata.json"
VALIDATION_PATH = OUTPUT_DIR / f"{DATASET_NAME}_validation_report.json"

COLUMNS = [
    "match_id",
    "sofascore_event_id",
    "match_date",
    "home_team",
    "away_team",
    "cutoff_minute",
    "home_goals_until_cutoff",
    "away_goals_until_cutoff",
    "score_diff_home_until_cutoff",
    "is_draw_until_cutoff",
    "home_leading_until_cutoff",
    "away_leading_until_cutoff",
    "total_goals_until_cutoff",
    "last_goal_minute_until_cutoff",
    "time_since_last_goal_until_cutoff",
    "red_cards_until_cutoff",
    "yellow_cards_until_cutoff",
    "cards_until_cutoff",
    "substitutions_until_cutoff",
    "goal_last_5m_until_cutoff",
    "goal_last_10m_until_cutoff",
    "target_goal_after_cutoff",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Dataset V1B in-game cutoff dataset for H6/H9 validation.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directory for CSV and reports.")
    return parser.parse_args()


def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    return str(value)


def build_dataframe() -> pd.DataFrame:
    sql = text(
        """
        WITH cutoffs(cutoff_minute) AS (
            VALUES (60), (65), (70), (75), (80)
        ),
        base AS (
            SELECT
                m.match_id,
                m.sofascore_event_id,
                m.match_date,
                m.home_team,
                m.away_team,
                c.cutoff_minute
            FROM matches_master m
            CROSS JOIN cutoffs c
            WHERE m.sofascore_event_id::text NOT IN :skipped_ids
        ),
        feature_agg AS (
            SELECT
                b.match_id,
                b.cutoff_minute,
                MAX(i.home_score) FILTER (
                    WHERE LOWER(COALESCE(i.incident_type, '')) = 'goal'
                      AND i.minute <= b.cutoff_minute
                ) AS home_goals_until_cutoff,
                MAX(i.away_score) FILTER (
                    WHERE LOWER(COALESCE(i.incident_type, '')) = 'goal'
                      AND i.minute <= b.cutoff_minute
                ) AS away_goals_until_cutoff,
                MAX(i.minute) FILTER (
                    WHERE LOWER(COALESCE(i.incident_type, '')) = 'goal'
                      AND i.minute <= b.cutoff_minute
                ) AS last_goal_minute_until_cutoff,
                COUNT(i.id) FILTER (
                    WHERE LOWER(COALESCE(i.incident_type, '')) = 'card'
                      AND i.minute <= b.cutoff_minute
                ) AS cards_until_cutoff,
                COUNT(i.id) FILTER (
                    WHERE LOWER(COALESCE(i.incident_type, '')) = 'substitution'
                      AND i.minute <= b.cutoff_minute
                ) AS substitutions_until_cutoff,
                COUNT(i.id) FILTER (
                    WHERE LOWER(COALESCE(i.incident_type, '')) = 'goal'
                      AND i.minute > b.cutoff_minute - 5
                      AND i.minute <= b.cutoff_minute
                ) AS goal_last_5m_count,
                COUNT(i.id) FILTER (
                    WHERE LOWER(COALESCE(i.incident_type, '')) = 'goal'
                      AND i.minute > b.cutoff_minute - 10
                      AND i.minute <= b.cutoff_minute
                ) AS goal_last_10m_count,
                COUNT(i.id) FILTER (
                    WHERE LOWER(COALESCE(i.incident_type, '')) = 'goal'
                      AND i.minute > b.cutoff_minute
                ) AS target_goal_count_after_cutoff
            FROM base b
            LEFT JOIN match_incidents i
              ON i.sofascore_event_id = b.sofascore_event_id
            GROUP BY b.match_id, b.cutoff_minute
        )
        SELECT
            b.match_id,
            b.sofascore_event_id,
            b.match_date,
            b.home_team,
            b.away_team,
            b.cutoff_minute,
            COALESCE(f.home_goals_until_cutoff, 0) AS home_goals_until_cutoff,
            COALESCE(f.away_goals_until_cutoff, 0) AS away_goals_until_cutoff,
            COALESCE(f.home_goals_until_cutoff, 0) - COALESCE(f.away_goals_until_cutoff, 0) AS score_diff_home_until_cutoff,
            CASE WHEN COALESCE(f.home_goals_until_cutoff, 0) = COALESCE(f.away_goals_until_cutoff, 0) THEN 1 ELSE 0 END AS is_draw_until_cutoff,
            CASE WHEN COALESCE(f.home_goals_until_cutoff, 0) > COALESCE(f.away_goals_until_cutoff, 0) THEN 1 ELSE 0 END AS home_leading_until_cutoff,
            CASE WHEN COALESCE(f.away_goals_until_cutoff, 0) > COALESCE(f.home_goals_until_cutoff, 0) THEN 1 ELSE 0 END AS away_leading_until_cutoff,
            COALESCE(f.home_goals_until_cutoff, 0) + COALESCE(f.away_goals_until_cutoff, 0) AS total_goals_until_cutoff,
            f.last_goal_minute_until_cutoff,
            CASE
                WHEN f.last_goal_minute_until_cutoff IS NULL THEN NULL
                ELSE b.cutoff_minute - f.last_goal_minute_until_cutoff
            END AS time_since_last_goal_until_cutoff,
            NULL::integer AS red_cards_until_cutoff,
            NULL::integer AS yellow_cards_until_cutoff,
            COALESCE(f.cards_until_cutoff, 0) AS cards_until_cutoff,
            COALESCE(f.substitutions_until_cutoff, 0) AS substitutions_until_cutoff,
            CASE WHEN COALESCE(f.goal_last_5m_count, 0) > 0 THEN 1 ELSE 0 END AS goal_last_5m_until_cutoff,
            CASE WHEN COALESCE(f.goal_last_10m_count, 0) > 0 THEN 1 ELSE 0 END AS goal_last_10m_until_cutoff,
            CASE WHEN COALESCE(f.target_goal_count_after_cutoff, 0) > 0 THEN 1 ELSE 0 END AS target_goal_after_cutoff
        FROM base b
        LEFT JOIN feature_agg f
          ON f.match_id = b.match_id
         AND f.cutoff_minute = b.cutoff_minute
        ORDER BY b.match_date, b.match_id, b.cutoff_minute
        """
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn, params={"skipped_ids": tuple(KNOWN_SKIPPED_MATCH_IDS)})
    for column in COLUMNS:
        if column not in df.columns:
            df[column] = None
    return df[COLUMNS]


def validate_dataset(df: pd.DataFrame) -> dict[str, Any]:
    key_duplicates = int(df.duplicated(subset=["match_id", "cutoff_minute"]).sum())
    target_counts = df["target_goal_after_cutoff"].value_counts(dropna=False).sort_index().to_dict()
    cutoff_counts = df["cutoff_minute"].value_counts().sort_index().to_dict()
    null_required = {
        column: int(df[column].isna().sum())
        for column in [
            "match_id",
            "sofascore_event_id",
            "match_date",
            "home_team",
            "away_team",
            "cutoff_minute",
            "target_goal_after_cutoff",
        ]
    }
    errors: list[str] = []
    warnings: list[str] = []

    if len(df) != EXPECTED_ROWS:
        errors.append(f"Expected {EXPECTED_ROWS} rows, found {len(df)}.")
    if key_duplicates:
        errors.append(f"Duplicate match_id + cutoff_minute rows found: {key_duplicates}.")
    if set(cutoff_counts.keys()) != set(CUTOFFS):
        errors.append("Unexpected cutoff_minute values found.")
    if any(count != EXPECTED_MATCHES for count in cutoff_counts.values()):
        errors.append("At least one cutoff does not contain one row for every match.")
    if any(value > 0 for value in null_required.values()):
        errors.append("Required identifiers or target contain null values.")
    if set(target_counts.keys()) != {0, 1}:
        errors.append("Target does not contain both positive and negative classes.")
    if ((df["goal_last_5m_until_cutoff"] == 1) & (df["goal_last_10m_until_cutoff"] == 0)).any():
        errors.append("Found goal_last_5m=1 with goal_last_10m=0, which is inconsistent.")
    if (df["time_since_last_goal_until_cutoff"].dropna() < 0).any():
        errors.append("Negative time_since_last_goal_until_cutoff found.")

    warnings.append(
        "Card color is not available in imported match_incidents; red_cards_until_cutoff and yellow_cards_until_cutoff are null by design. Use cards_until_cutoff for current H9 validation."
    )

    status = "NAO APTO" if errors else "APTO COM RESSALVAS" if warnings else "APTO"
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "dataset_name": DATASET_NAME,
        "dataset_version": DATASET_VERSION,
        "status": status,
        "grain": "one row per match_id + cutoff_minute",
        "cutoffs": CUTOFFS,
        "row_count": int(len(df)),
        "expected_row_count": EXPECTED_ROWS,
        "unique_matches": int(df["match_id"].nunique()),
        "duplicate_match_cutoff_rows": key_duplicates,
        "cutoff_counts": {str(key): int(value) for key, value in cutoff_counts.items()},
        "target_counts": {str(key): int(value) for key, value in target_counts.items()},
        "target_positive_count": int(df["target_goal_after_cutoff"].sum()),
        "target_negative_count": int((df["target_goal_after_cutoff"] == 0).sum()),
        "target_positive_rate": round(float(df["target_goal_after_cutoff"].mean()), 6) if len(df) else None,
        "required_null_counts": null_required,
        "red_cards_null_count": int(df["red_cards_until_cutoff"].isna().sum()),
        "yellow_cards_null_count": int(df["yellow_cards_until_cutoff"].isna().sum()),
        "cards_until_cutoff_max": int(df["cards_until_cutoff"].max()) if len(df) else None,
        "substitutions_until_cutoff_max": int(df["substitutions_until_cutoff"].max()) if len(df) else None,
        "validation_errors": errors,
        "validation_warnings": warnings,
    }


def build_metadata(df: pd.DataFrame, validation: dict[str, Any]) -> dict[str, Any]:
    feature_columns = [
        "home_goals_until_cutoff",
        "away_goals_until_cutoff",
        "score_diff_home_until_cutoff",
        "is_draw_until_cutoff",
        "home_leading_until_cutoff",
        "away_leading_until_cutoff",
        "total_goals_until_cutoff",
        "last_goal_minute_until_cutoff",
        "time_since_last_goal_until_cutoff",
        "cards_until_cutoff",
        "substitutions_until_cutoff",
        "goal_last_5m_until_cutoff",
        "goal_last_10m_until_cutoff",
    ]
    unavailable_columns = ["red_cards_until_cutoff", "yellow_cards_until_cutoff"]
    return {
        "dataset_name": DATASET_NAME,
        "dataset_version": DATASET_VERSION,
        "generated_at": validation["generated_at"],
        "status": validation["status"],
        "grain": validation["grain"],
        "source_tables": ["matches_master", "match_incidents"],
        "excluded_source_tables": ["match_statistics", "match_graph"],
        "known_skipped_match_ids": sorted(KNOWN_SKIPPED_MATCH_IDS),
        "cutoffs": CUTOFFS,
        "row_count": int(len(df)),
        "columns": list(df.columns),
        "feature_columns_allowed_for_initial_h6_h9_validation": feature_columns,
        "unavailable_columns_kept_for_contract": unavailable_columns,
        "target": {
            "name": "target_goal_after_cutoff",
            "definition": "1 if at least one goal incident has minute > cutoff_minute; otherwise 0.",
            "source": "match_incidents",
            "feature_use": "prohibited",
        },
        "leakage_rules": [
            "Features are computed only from incidents with minute <= cutoff_minute.",
            "target_goal_after_cutoff is computed from goal incidents with minute > cutoff_minute and must not be used as a feature.",
            "No full-match statistics are used in Dataset V1B.",
            "No final score columns from matches_master are used as predictors.",
        ],
        "caveats": [
            "Card color is not available in the imported match_incidents table; use cards_until_cutoff for current H9 validation.",
            "red_cards_until_cutoff and yellow_cards_until_cutoff are null by design until importer/schema captures card color.",
        ],
        "outputs": {
            "csv": str(CSV_PATH),
            "metadata": str(METADATA_PATH),
            "validation_report": str(VALIDATION_PATH),
        },
    }


def write_outputs(df: pd.DataFrame, output_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    global OUTPUT_DIR, CSV_PATH, METADATA_PATH, VALIDATION_PATH
    OUTPUT_DIR = output_dir
    CSV_PATH = OUTPUT_DIR / f"{DATASET_NAME}.csv"
    METADATA_PATH = OUTPUT_DIR / f"{DATASET_NAME}_metadata.json"
    VALIDATION_PATH = OUTPUT_DIR / f"{DATASET_NAME}_validation_report.json"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CSV_PATH, index=False, encoding="utf-8")
    validation = validate_dataset(df)
    metadata = build_metadata(df, validation)
    METADATA_PATH.write_text(json.dumps(metadata, indent=2, ensure_ascii=False, default=json_default), encoding="utf-8")
    VALIDATION_PATH.write_text(json.dumps(validation, indent=2, ensure_ascii=False, default=json_default), encoding="utf-8")
    return metadata, validation


def main() -> None:
    args = parse_args()
    print("Building late_goal_dataset_v1b_ingame from PostgreSQL with SELECT-only queries")
    df = build_dataframe()
    _, validation = write_outputs(df, Path(args.output_dir))
    print(f"status={validation['status']}")
    print(f"rows={validation['row_count']}")
    print(f"unique_matches={validation['unique_matches']}")
    print(f"target_positive={validation['target_positive_count']}")
    print(f"target_negative={validation['target_negative_count']}")
    print(f"csv={CSV_PATH}")
    print(f"metadata={METADATA_PATH}")
    print(f"validation_report={VALIDATION_PATH}")
    if validation["validation_errors"]:
        print("validation_errors:")
        for error in validation["validation_errors"]:
            print(f"- {error}")
    if validation["validation_warnings"]:
        print("validation_warnings:")
        for warning in validation["validation_warnings"]:
            print(f"- {warning}")


if __name__ == "__main__":
    main()
