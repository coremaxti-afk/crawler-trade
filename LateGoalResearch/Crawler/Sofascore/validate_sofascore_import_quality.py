"""Read-only SofaScore post-import quality validation.

Generates local Markdown/JSON reports with SELECT-only database checks.
"""

from __future__ import annotations

import json
import statistics
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import engine  # noqa: E402

KNOWN_SKIPPED_MATCH_IDS = {"12436452"}
EXPECTED_COUNTS = {"matches_master": 380, "match_statistics": 380, "match_incidents": 7647}
REPORT_DIR = PROJECT_ROOT / "data" / "reports"
REPORT_MD = REPORT_DIR / "sofascore_import_quality_report.md"
REPORT_JSON = REPORT_DIR / "sofascore_import_quality_report.json"
RARE_TYPE_THRESHOLD = 3
NUMERIC_STAT_FIELDS = [
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
]


def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return str(value)


def rows(result: Any) -> list[dict[str, Any]]:
    return [dict(row._mapping) for row in result]


def fetch_all(conn: Any, sql: str, params: dict[str, Any]) -> list[dict[str, Any]]:
    return rows(conn.execute(text(sql), params))


def scalar(conn: Any, sql: str, params: dict[str, Any] | None = None) -> Any:
    return conn.execute(text(sql), params or {}).scalar_one()


def number_summary(values: list[float | int]) -> dict[str, Any]:
    clean = [value for value in values if value is not None]
    if not clean:
        return {"count": 0, "min": None, "max": None, "mean": None, "median": None}
    return {
        "count": len(clean),
        "min": min(clean),
        "max": max(clean),
        "mean": round(float(statistics.mean(clean)), 4),
        "median": round(float(statistics.median(clean)), 4),
    }


def md_table(table_rows: list[dict[str, Any]], columns: list[str], limit: int | None = None) -> str:
    selected = table_rows if limit is None else table_rows[:limit]
    if not selected:
        return "Nenhum registro."
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in selected:
        output.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(output)


def collect_report() -> dict[str, Any]:
    params = {"skipped_ids": tuple(KNOWN_SKIPPED_MATCH_IDS)}
    stat_select = ", ".join(NUMERIC_STAT_FIELDS)

    with engine.connect() as conn:
        table_counts = {table: scalar(conn, f"SELECT COUNT(*) FROM {table}") for table in EXPECTED_COUNTS}
        duplicate_matches = fetch_all(
            conn,
            """
            SELECT sofascore_event_id, COUNT(*) AS total
            FROM matches_master
            WHERE sofascore_event_id IS NOT NULL
              AND sofascore_event_id::text NOT IN :skipped_ids
            GROUP BY sofascore_event_id
            HAVING COUNT(*) > 1
            ORDER BY total DESC, sofascore_event_id
            """,
            params,
        )
        duplicate_statistics = fetch_all(
            conn,
            """
            SELECT sofascore_event_id, COUNT(*) AS total
            FROM match_statistics
            WHERE sofascore_event_id::text NOT IN :skipped_ids
            GROUP BY sofascore_event_id
            HAVING COUNT(*) > 1
            ORDER BY total DESC, sofascore_event_id
            """,
            params,
        )
        incident_counts = fetch_all(
            conn,
            """
            SELECT m.sofascore_event_id, m.match_date, m.home_team, m.away_team, COUNT(i.id) AS incident_count
            FROM matches_master m
            LEFT JOIN match_incidents i ON i.sofascore_event_id = m.sofascore_event_id
            WHERE m.sofascore_event_id::text NOT IN :skipped_ids
            GROUP BY m.sofascore_event_id, m.match_date, m.home_team, m.away_team
            ORDER BY m.match_date, m.sofascore_event_id
            """,
            params,
        )
        incident_values = [int(row["incident_count"] or 0) for row in incident_counts]
        zero_incident_matches = [row for row in incident_counts if int(row["incident_count"] or 0) == 0]
        top_incident_matches = sorted(incident_counts, key=lambda row: int(row["incident_count"] or 0), reverse=True)[:10]
        incident_type_distribution = fetch_all(
            conn,
            """
            SELECT incident_type, COUNT(*) AS total
            FROM match_incidents
            WHERE sofascore_event_id::text NOT IN :skipped_ids
            GROUP BY incident_type
            ORDER BY total DESC, incident_type NULLS LAST
            """,
            params,
        )
        null_incident_types = scalar(
            conn,
            """
            SELECT COUNT(*)
            FROM match_incidents
            WHERE sofascore_event_id::text NOT IN :skipped_ids
              AND incident_type IS NULL
            """,
            params,
        )
        no_goal_incident_matches = fetch_all(
            conn,
            """
            WITH goal_counts AS (
                SELECT sofascore_event_id,
                       COUNT(*) FILTER (WHERE LOWER(COALESCE(incident_type, '')) = 'goal') AS goal_incidents
                FROM match_incidents
                WHERE sofascore_event_id::text NOT IN :skipped_ids
                GROUP BY sofascore_event_id
            )
            SELECT m.sofascore_event_id, m.match_date, m.home_team, m.away_team,
                   m.home_goals, m.away_goals, COALESCE(g.goal_incidents, 0) AS goal_incidents,
                   COALESCE(m.home_goals, 0) + COALESCE(m.away_goals, 0) = 0 AS master_score_is_0_0
            FROM matches_master m
            LEFT JOIN goal_counts g ON g.sofascore_event_id = m.sofascore_event_id
            WHERE m.sofascore_event_id::text NOT IN :skipped_ids
              AND COALESCE(g.goal_incidents, 0) = 0
            ORDER BY m.match_date, m.sofascore_event_id
            """,
            params,
        )
        goal_divergences = fetch_all(
            conn,
            """
            WITH incident_scores AS (
                SELECT sofascore_event_id,
                       MAX(home_score) AS incident_home_goals,
                       MAX(away_score) AS incident_away_goals,
                       COUNT(*) FILTER (WHERE LOWER(COALESCE(incident_type, '')) = 'goal' AND is_home IS true) AS home_goal_events,
                       COUNT(*) FILTER (WHERE LOWER(COALESCE(incident_type, '')) = 'goal' AND is_home IS false) AS away_goal_events
                FROM match_incidents
                WHERE sofascore_event_id::text NOT IN :skipped_ids
                GROUP BY sofascore_event_id
            )
            SELECT m.sofascore_event_id, m.match_date, m.home_team, m.away_team,
                   m.home_goals AS master_home_goals, m.away_goals AS master_away_goals,
                   COALESCE(s.incident_home_goals, 0) AS incident_home_goals,
                   COALESCE(s.incident_away_goals, 0) AS incident_away_goals,
                   COALESCE(s.home_goal_events, 0) AS home_goal_events,
                   COALESCE(s.away_goal_events, 0) AS away_goal_events
            FROM matches_master m
            LEFT JOIN incident_scores s ON s.sofascore_event_id = m.sofascore_event_id
            WHERE m.sofascore_event_id::text NOT IN :skipped_ids
              AND (COALESCE(m.home_goals, 0) <> COALESCE(s.incident_home_goals, 0)
                   OR COALESCE(m.away_goals, 0) <> COALESCE(s.incident_away_goals, 0))
            ORDER BY m.match_date, m.sofascore_event_id
            """,
            params,
        )
        stat_rows = fetch_all(
            conn,
            f"""
            SELECT sofascore_event_id, {stat_select}
            FROM match_statistics
            WHERE sofascore_event_id::text NOT IN :skipped_ids
            ORDER BY sofascore_event_id
            """,
            params,
        )
        matches_without_statistics = fetch_all(
            conn,
            """
            SELECT m.sofascore_event_id, m.match_date, m.home_team, m.away_team
            FROM matches_master m
            LEFT JOIN match_statistics s ON s.sofascore_event_id = m.sofascore_event_id
            WHERE m.sofascore_event_id::text NOT IN :skipped_ids
              AND s.sofascore_event_id IS NULL
            ORDER BY m.match_date, m.sofascore_event_id
            """,
            params,
        )

    stat_null_counts = {field: sum(1 for row in stat_rows if row.get(field) is None) for field in NUMERIC_STAT_FIELDS}
    empty_stat_records = [row["sofascore_event_id"] for row in stat_rows if all(row.get(field) is None for field in NUMERIC_STAT_FIELDS)]
    no_goal_suspicious = [row for row in no_goal_incident_matches if not row["master_score_is_0_0"]]
    count_mismatches = {
        table: {"expected": expected, "actual": table_counts.get(table)}
        for table, expected in EXPECTED_COUNTS.items()
        if table_counts.get(table) != expected
    }
    blocking = bool(count_mismatches or duplicate_matches or duplicate_statistics or matches_without_statistics)
    warnings = bool(
        zero_incident_matches
        or null_incident_types
        or no_goal_suspicious
        or goal_divergences
        or empty_stat_records
        or any(total > 0 for total in stat_null_counts.values())
    )
    status = "NAO APTO" if blocking else "APTO COM RESSALVAS" if warnings else "APTO"

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "known_skipped_match_ids": sorted(KNOWN_SKIPPED_MATCH_IDS),
        "expected_counts": EXPECTED_COUNTS,
        "table_counts": table_counts,
        "count_mismatches": count_mismatches,
        "duplicates": {"matches_master": duplicate_matches, "match_statistics": duplicate_statistics},
        "incident_counts": {
            "summary": number_summary(incident_values),
            "zero_incident_matches": zero_incident_matches,
            "top_10_most_incidents": top_incident_matches,
        },
        "incident_types": {
            "distribution": incident_type_distribution,
            "null_types": null_incident_types,
            "rare_threshold": RARE_TYPE_THRESHOLD,
            "rare_types": [row for row in incident_type_distribution if int(row["total"] or 0) <= RARE_TYPE_THRESHOLD],
        },
        "goals": {
            "matches_without_goal_incidents": no_goal_incident_matches,
            "matches_without_goal_incidents_but_master_has_goals": no_goal_suspicious,
            "master_vs_incidents_divergences": goal_divergences,
        },
        "match_statistics": {
            "row_count": len(stat_rows),
            "null_counts": stat_null_counts,
            "empty_records": empty_stat_records,
            "numeric_distributions": {
                field: number_summary([row[field] for row in stat_rows if row.get(field) is not None])
                for field in NUMERIC_STAT_FIELDS
            },
            "matches_without_statistics": matches_without_statistics,
        },
        "final_status": status,
    }


def render_markdown(report: dict[str, Any]) -> str:
    incident = report["incident_counts"]["summary"]
    lines = [
        "# SofaScore Import Quality Report",
        "",
        f"Generated at: {report['generated_at']}",
        f"Final status for Quant Research: **{report['final_status']}**",
        "",
        "## Scope",
        "",
        "Lightweight post-import validation for SofaScore EPL 2024/25. The script runs SELECT-only database checks and writes local reports.",
        "",
        "## Expected vs Found Counts",
        "",
        "| Table | Expected | Found |",
        "| --- | ---: | ---: |",
    ]
    for table, expected in report["expected_counts"].items():
        lines.append(f"| {table} | {expected} | {report['table_counts'].get(table)} |")
    lines += [
        "",
        "## Incidents Per Match",
        "",
        f"- Min: {incident['min']}",
        f"- Max: {incident['max']}",
        f"- Mean: {incident['mean']}",
        f"- Median: {incident['median']}",
        f"- Matches with 0 incidents: {len(report['incident_counts']['zero_incident_matches'])}",
        "",
        "### Top 10 Most Incidents",
        "",
        md_table(report["incident_counts"]["top_10_most_incidents"], ["sofascore_event_id", "match_date", "home_team", "away_team", "incident_count"]),
        "",
        "## Incident Types",
        "",
        f"- Null types: {report['incident_types']['null_types']}",
        f"- Rare types <= {report['incident_types']['rare_threshold']}: {len(report['incident_types']['rare_types'])}",
        "",
        md_table(report["incident_types"]["distribution"], ["incident_type", "total"]),
        "",
        "## Matches Without Goal Incidents",
        "",
        f"- Total without goal incidents: {len(report['goals']['matches_without_goal_incidents'])}",
        f"- Without goal incidents but master score has goals: {len(report['goals']['matches_without_goal_incidents_but_master_has_goals'])}",
        "",
        md_table(report["goals"]["matches_without_goal_incidents_but_master_has_goals"], ["sofascore_event_id", "match_date", "home_team", "away_team", "home_goals", "away_goals", "goal_incidents"]),
        "",
        "## matches_master vs match_incidents Divergence",
        "",
        f"- Divergences found: {len(report['goals']['master_vs_incidents_divergences'])}",
        "",
        md_table(report["goals"]["master_vs_incidents_divergences"], ["sofascore_event_id", "match_date", "home_team", "away_team", "master_home_goals", "master_away_goals", "incident_home_goals", "incident_away_goals", "home_goal_events", "away_goal_events"], limit=50),
        "",
        "## match_statistics",
        "",
        f"- Rows: {report['match_statistics']['row_count']}",
        f"- Empty rows: {len(report['match_statistics']['empty_records'])}",
        f"- Matches without statistics: {len(report['match_statistics']['matches_without_statistics'])}",
        "",
        "### Null Fields",
        "",
        "| Field | Nulls |",
        "| --- | ---: |",
    ]
    for field, total in report["match_statistics"]["null_counts"].items():
        lines.append(f"| {field} | {total} |")
    lines += ["", "### Numeric Field Distribution", "", "| Field | Count | Min | Max | Mean | Median |", "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for field, stats in report["match_statistics"]["numeric_distributions"].items():
        lines.append(f"| {field} | {stats['count']} | {stats['min']} | {stats['max']} | {stats['mean']} | {stats['median']} |")
    lines += ["", "## Conclusion", ""]
    if report["final_status"] == "APTO":
        lines.append("Imported base is approved for Quant Research.")
    elif report["final_status"] == "APTO COM RESSALVAS":
        lines.append("Imported base can move to Quant Research with the documented caveats above.")
    else:
        lines.append("Imported base should not move to Quant Research before the blocking issues above are fixed.")
    return "\n".join(lines) + "\n"


def main() -> None:
    report = collect_report()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=json_default), encoding="utf-8")
    REPORT_MD.write_text(render_markdown(report), encoding="utf-8")
    print("SofaScore import quality validation complete")
    print(f"status={report['final_status']}")
    print(f"matches_master={report['table_counts']['matches_master']}")
    print(f"match_statistics={report['table_counts']['match_statistics']}")
    print(f"match_incidents={report['table_counts']['match_incidents']}")
    print(f"markdown_report={REPORT_MD}")
    print(f"json_report={REPORT_JSON}")


if __name__ == "__main__":
    main()
