"""Build Team Profile Segment Features V1.

Read-only PostgreSQL flow:
- reads matches_master and match_statistics;
- builds historical expanding profiles using only prior team matches;
- classifies offensive/defensive team profiles dynamically;
- generates match-level segment flags without target columns;
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

import numpy as np
import pandas as pd
from sqlalchemy import text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.database import engine  # noqa: E402

FEATURE_SET_NAME = "team_profile_segments_v1"
FEATURE_SET_VERSION = "v1"
BUILDER_VERSION = "team_profile_segment_feature_builder_v1"
KNOWN_SKIPPED_MATCH_IDS = {"12436452"}
EXPECTED_MATCHES = 380
MIN_GAMES = 5
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "features"
CSV_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}.csv"
PARQUET_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}.parquet"
METADATA_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}_metadata.json"
VALIDATION_PATH = OUTPUT_DIR / f"{FEATURE_SET_NAME}_validation_report.json"
GROUP_KEYS = ["season", "team_name"]
SORT_COLUMNS = ["season", "team_name", "match_date", "match_id"]

PROFILE_SOURCE_METRICS = [
    "goals_for",
    "shots_for",
    "shots_on_target_for",
    "big_chances_for",
    "goals_against",
    "shots_against",
    "shots_on_target_against",
    "big_chances_against",
]
OFFENSE_PRIOR_COLUMNS = [
    "goals_for_expanding_prior",
    "shots_for_expanding_prior",
    "shots_on_target_for_expanding_prior",
    "big_chances_for_expanding_prior",
]
DEFENSE_PRIOR_COLUMNS = [
    "goals_against_expanding_prior",
    "shots_against_expanding_prior",
    "shots_on_target_against_expanding_prior",
    "big_chances_against_expanding_prior",
]
PROFILE_VALUE_COLUMNS = OFFENSE_PRIOR_COLUMNS + DEFENSE_PRIOR_COLUMNS

TEAM_PROFILE_COLUMNS = [
    "offense_profile",
    "defense_profile",
    "offense_index_prior",
    "defense_fragility_index_prior",
    *PROFILE_VALUE_COLUMNS,
    "history_matches_available",
    "profile_eligible",
    "profile_max_match_date_used",
    "profile_source_match_count",
    "profile_source_match_ids",
    "offense_threshold_low",
    "offense_threshold_high",
    "defense_threshold_low",
    "defense_threshold_high",
]

WHITELIST_FEATURES = [
    "home_offense_profile",
    "away_offense_profile",
    "home_defense_profile",
    "away_defense_profile",
    "home_offense_index_prior",
    "away_offense_index_prior",
    "home_defense_fragility_index_prior",
    "away_defense_fragility_index_prior",
    "home_ofensivo_strong",
    "home_ofensivo_middle",
    "home_ofensivo_weak",
    "away_ofensivo_strong",
    "away_ofensivo_middle",
    "away_ofensivo_weak",
    "home_defensivo_fragile",
    "home_defensivo_middle",
    "home_defensivo_strong",
    "away_defensivo_fragile",
    "away_defensivo_middle",
    "away_defensivo_strong",
    "ofensivo_forte_vs_defesa_fragil",
    "ambos_defesa_forte",
    "defesa_fragil_vs_defesa_fragil",
    "ofensivo_forte_vs_ofensivo_forte",
    "ofensivo_fraco_vs_defesa_forte",
    "ao_menos_um_ofensivo_forte",
    "ao_menos_uma_defesa_fragil",
    "sem_ofensivo_forte_sem_defesa_fragil",
]

AUDIT_COLUMNS = [
    "match_id",
    "sofascore_event_id",
    "league",
    "season",
    "match_date",
    "home_team",
    "away_team",
    "home_history_matches_available",
    "away_history_matches_available",
    "home_profile_eligible",
    "away_profile_eligible",
    "match_profile_eligible",
    "match_segment_eligible",
    "home_profile_max_match_date_used",
    "away_profile_max_match_date_used",
    "home_profile_source_match_count",
    "away_profile_source_match_count",
    "home_profile_source_match_ids",
    "away_profile_source_match_ids",
    "home_offense_threshold_low",
    "home_offense_threshold_high",
    "away_offense_threshold_low",
    "away_offense_threshold_high",
    "home_defense_threshold_low",
    "home_defense_threshold_high",
    "away_defense_threshold_low",
    "away_defense_threshold_high",
    "profile_min_games_rule",
    "profile_method",
    "profile_threshold_method",
    "builder_version",
    "generated_at_utc",
]

HISTORICAL_AUDIT_COLUMNS = [f"home_{column}" for column in PROFILE_VALUE_COLUMNS] + [
    f"away_{column}" for column in PROFILE_VALUE_COLUMNS
]
OUTPUT_COLUMNS = AUDIT_COLUMNS + WHITELIST_FEATURES + HISTORICAL_AUDIT_COLUMNS
TARGET_DERIVED_PATTERNS = ["late_goal", "goal_after"]
FORBIDDEN_OUTPUT_COLUMNS = {
    "home_goals",
    "away_goals",
    "total_goals",
    "home_xg",
    "away_xg",
    "forecast_home",
    "forecast_draw",
    "forecast_away",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Team Profile Segment Features V1 from PostgreSQL.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Directory for CSV, Parquet and reports.")
    parser.add_argument("--min-games", type=int, default=MIN_GAMES, help="Minimum prior matches required for profile eligibility.")
    return parser.parse_args()


def json_default(value: Any) -> str:
    if isinstance(value, (datetime, date, pd.Timestamp)):
        return value.isoformat()
    return str(value)


def parquet_engine_available() -> bool:
    return bool(importlib.util.find_spec("pyarrow") or importlib.util.find_spec("fastparquet"))


def table_counts() -> dict[str, int]:
    tables = ["matches_master", "match_statistics"]
    with engine.connect() as conn:
        return {table: int(conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()) for table in tables}


def fetch_match_level_source() -> pd.DataFrame:
    sql = text(
        """
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
            s.shots_home,
            s.shots_away,
            s.shots_on_target_home,
            s.shots_on_target_away,
            s.big_chances_home,
            s.big_chances_away
        FROM matches_master m
        LEFT JOIN match_statistics s
          ON s.match_id = m.match_id
        WHERE m.sofascore_event_id::text NOT IN :skipped_ids
        ORDER BY m.match_date, m.match_id
        """
    )
    with engine.connect() as conn:
        df = pd.read_sql_query(sql, conn, params={"skipped_ids": tuple(KNOWN_SKIPPED_MATCH_IDS)})
    df["match_date"] = pd.to_datetime(df["match_date"])
    numeric_columns = [
        "home_goals",
        "away_goals",
        "shots_home",
        "shots_away",
        "shots_on_target_home",
        "shots_on_target_away",
        "big_chances_home",
        "big_chances_away",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def build_team_match_rows(match_df: pd.DataFrame) -> pd.DataFrame:
    home = pd.DataFrame(
        {
            "match_id": match_df["match_id"],
            "sofascore_event_id": match_df["sofascore_event_id"],
            "league": match_df["league"],
            "season": match_df["season"],
            "match_date": match_df["match_date"],
            "team_name": match_df["home_team"],
            "opponent_team": match_df["away_team"],
            "is_home": 1,
            "goals_for": match_df["home_goals"],
            "goals_against": match_df["away_goals"],
            "shots_for": match_df["shots_home"],
            "shots_against": match_df["shots_away"],
            "shots_on_target_for": match_df["shots_on_target_home"],
            "shots_on_target_against": match_df["shots_on_target_away"],
            "big_chances_for": match_df["big_chances_home"],
            "big_chances_against": match_df["big_chances_away"],
        }
    )
    away = pd.DataFrame(
        {
            "match_id": match_df["match_id"],
            "sofascore_event_id": match_df["sofascore_event_id"],
            "league": match_df["league"],
            "season": match_df["season"],
            "match_date": match_df["match_date"],
            "team_name": match_df["away_team"],
            "opponent_team": match_df["home_team"],
            "is_home": 0,
            "goals_for": match_df["away_goals"],
            "goals_against": match_df["home_goals"],
            "shots_for": match_df["shots_away"],
            "shots_against": match_df["shots_home"],
            "shots_on_target_for": match_df["shots_on_target_away"],
            "shots_on_target_against": match_df["shots_on_target_home"],
            "big_chances_for": match_df["big_chances_away"],
            "big_chances_against": match_df["big_chances_home"],
        }
    )
    team_df = pd.concat([home, away], ignore_index=True)
    return team_df.sort_values(SORT_COLUMNS).reset_index(drop=True)


def expanding_prior_mean(values: pd.Series) -> pd.Series:
    return values.shift(1).expanding(min_periods=1).mean()


def prior_source_match_ids(match_ids: pd.Series) -> list[str]:
    seen: list[str] = []
    output: list[str] = []
    for match_id in match_ids:
        output.append(json.dumps(seen, ensure_ascii=False))
        seen.append(str(int(match_id)))
    return output


def add_historical_profiles(team_df: pd.DataFrame, min_games: int) -> pd.DataFrame:
    df = team_df.copy().sort_values(SORT_COLUMNS).reset_index(drop=True)
    df["history_matches_available"] = df.groupby(GROUP_KEYS).cumcount()
    df["profile_eligible"] = df["history_matches_available"].ge(min_games).astype(int)
    for metric in PROFILE_SOURCE_METRICS:
        df[f"{metric}_expanding_prior"] = df.groupby(GROUP_KEYS)[metric].transform(expanding_prior_mean)
    shifted_dates = df.groupby(GROUP_KEYS)["match_date"].shift(1)
    df["profile_max_match_date_used"] = shifted_dates.groupby([df["season"], df["team_name"]]).cummax()
    df["profile_source_match_count"] = df["history_matches_available"]
    df["profile_source_match_ids"] = df.groupby(GROUP_KEYS)["match_id"].transform(prior_source_match_ids)
    return df


def zscore(values: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(values, errors="coerce")
    std = numeric.std(skipna=True)
    if pd.isna(std) or std == 0:
        return pd.Series(np.zeros(len(numeric)), index=numeric.index)
    return (numeric - numeric.mean(skipna=True)) / std


def add_profile_indices(team_df: pd.DataFrame) -> pd.DataFrame:
    df = team_df.copy()
    for column in PROFILE_VALUE_COLUMNS:
        df[f"{column}_z"] = zscore(df[column])
    df["offense_index_prior"] = df[[f"{column}_z" for column in OFFENSE_PRIOR_COLUMNS]].mean(axis=1, skipna=True)
    df["defense_fragility_index_prior"] = df[[f"{column}_z" for column in DEFENSE_PRIOR_COLUMNS]].mean(axis=1, skipna=True)
    return df


def categorize_value(value: float | None, low: float | None, high: float | None, low_label: str, mid_label: str, high_label: str) -> str:
    if value is None or low is None or high is None or pd.isna(value) or pd.isna(low) or pd.isna(high):
        return "unknown"
    if value <= low:
        return low_label
    if value >= high:
        return high_label
    return mid_label


def add_dynamic_profile_categories(team_df: pd.DataFrame, min_games: int) -> pd.DataFrame:
    df = team_df.copy().sort_values(["match_date", "match_id", "team_name"]).reset_index(drop=True)
    for column in ["offense_profile", "defense_profile", "offense_threshold_low", "offense_threshold_high", "defense_threshold_low", "defense_threshold_high"]:
        df[column] = np.nan
    df["offense_profile"] = "unknown"
    df["defense_profile"] = "unknown"
    for idx, row in df.iterrows():
        if int(row["profile_eligible"]) != 1:
            continue
        threshold_pool = df[(df["season"].eq(row["season"])) & (df["profile_eligible"].eq(1)) & (df["match_date"] < row["match_date"])]
        if len(threshold_pool) < max(20, min_games * 4):
            continue
        offense_low, offense_high = threshold_pool["offense_index_prior"].quantile([1 / 3, 2 / 3])
        defense_low, defense_high = threshold_pool["defense_fragility_index_prior"].quantile([1 / 3, 2 / 3])
        df.at[idx, "offense_threshold_low"] = float(offense_low)
        df.at[idx, "offense_threshold_high"] = float(offense_high)
        df.at[idx, "defense_threshold_low"] = float(defense_low)
        df.at[idx, "defense_threshold_high"] = float(defense_high)
        df.at[idx, "offense_profile"] = categorize_value(row["offense_index_prior"], offense_low, offense_high, "weak", "middle", "strong")
        df.at[idx, "defense_profile"] = categorize_value(row["defense_fragility_index_prior"], defense_low, defense_high, "strong", "middle", "fragile")
    return df.sort_values(SORT_COLUMNS).reset_index(drop=True)


def prefixed_profile_rows(team_df: pd.DataFrame, is_home: int, prefix: str) -> pd.DataFrame:
    side = team_df[team_df["is_home"].eq(is_home)].copy()
    keep = ["match_id", *TEAM_PROFILE_COLUMNS]
    side = side[keep]
    return side.rename(columns={column: f"{prefix}_{column}" for column in keep if column != "match_id"})


def add_flag_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for side in ["home", "away"]:
        out[f"{side}_ofensivo_strong"] = out[f"{side}_offense_profile"].eq("strong").astype(int)
        out[f"{side}_ofensivo_middle"] = out[f"{side}_offense_profile"].eq("middle").astype(int)
        out[f"{side}_ofensivo_weak"] = out[f"{side}_offense_profile"].eq("weak").astype(int)
        out[f"{side}_defensivo_fragile"] = out[f"{side}_defense_profile"].eq("fragile").astype(int)
        out[f"{side}_defensivo_middle"] = out[f"{side}_defense_profile"].eq("middle").astype(int)
        out[f"{side}_defensivo_strong"] = out[f"{side}_defense_profile"].eq("strong").astype(int)
    out["ofensivo_forte_vs_defesa_fragil"] = ((out["home_ofensivo_strong"].eq(1) & out["away_defensivo_fragile"].eq(1)) | (out["away_ofensivo_strong"].eq(1) & out["home_defensivo_fragile"].eq(1))).astype(int)
    out["ambos_defesa_forte"] = (out["home_defensivo_strong"].eq(1) & out["away_defensivo_strong"].eq(1)).astype(int)
    out["defesa_fragil_vs_defesa_fragil"] = (out["home_defensivo_fragile"].eq(1) & out["away_defensivo_fragile"].eq(1)).astype(int)
    out["ofensivo_forte_vs_ofensivo_forte"] = (out["home_ofensivo_strong"].eq(1) & out["away_ofensivo_strong"].eq(1)).astype(int)
    out["ofensivo_fraco_vs_defesa_forte"] = ((out["home_ofensivo_weak"].eq(1) & out["away_defensivo_strong"].eq(1)) | (out["away_ofensivo_weak"].eq(1) & out["home_defensivo_strong"].eq(1))).astype(int)
    out["ao_menos_um_ofensivo_forte"] = (out["home_ofensivo_strong"].eq(1) | out["away_ofensivo_strong"].eq(1)).astype(int)
    out["ao_menos_uma_defesa_fragil"] = (out["home_defensivo_fragile"].eq(1) | out["away_defensivo_fragile"].eq(1)).astype(int)
    out["sem_ofensivo_forte_sem_defesa_fragil"] = (out["home_ofensivo_strong"].eq(0) & out["away_ofensivo_strong"].eq(0) & out["home_defensivo_fragile"].eq(0) & out["away_defensivo_fragile"].eq(0) & out["match_segment_eligible"].eq(1)).astype(int)
    return out


def build_feature_dataframe(min_games: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    match_df = fetch_match_level_source()
    team_rows = build_team_match_rows(match_df)
    team_profiles = add_historical_profiles(team_rows, min_games=min_games)
    team_profiles = add_profile_indices(team_profiles)
    team_profiles = add_dynamic_profile_categories(team_profiles, min_games=min_games)
    home_profiles = prefixed_profile_rows(team_profiles, is_home=1, prefix="home")
    away_profiles = prefixed_profile_rows(team_profiles, is_home=0, prefix="away")
    features = match_df[["match_id", "sofascore_event_id", "league", "season", "match_date", "home_team", "away_team"]].copy()
    features = features.merge(home_profiles, on="match_id", how="left")
    features = features.merge(away_profiles, on="match_id", how="left")
    features["home_profile_eligible"] = features["home_profile_eligible"].fillna(0).astype(int)
    features["away_profile_eligible"] = features["away_profile_eligible"].fillna(0).astype(int)
    features["match_profile_eligible"] = (features["home_history_matches_available"].ge(min_games) & features["away_history_matches_available"].ge(min_games)).astype(int)
    features["match_segment_eligible"] = (features["match_profile_eligible"].eq(1) & features["home_offense_profile"].ne("unknown") & features["away_offense_profile"].ne("unknown") & features["home_defense_profile"].ne("unknown") & features["away_defense_profile"].ne("unknown")).astype(int)
    features["profile_min_games_rule"] = min_games
    features["profile_method"] = "expanding_prior_season_to_date_shift_1"
    features["profile_threshold_method"] = "dynamic_terciles_from_prior_match_dates_only"
    features["builder_version"] = BUILDER_VERSION
    features["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
    features = add_flag_columns(features)
    for column in OUTPUT_COLUMNS:
        if column not in features.columns:
            features[column] = None
    features = features[OUTPUT_COLUMNS].sort_values(["match_date", "match_id"]).reset_index(drop=True)
    return features, team_profiles, match_df


def validate_no_profile_leakage(team_profiles: pd.DataFrame) -> dict[str, Any]:
    mismatches: list[dict[str, Any]] = []
    checks_run = 0
    for _, group in team_profiles.groupby(GROUP_KEYS, sort=False):
        group = group.sort_values(["match_date", "match_id"]).reset_index(drop=True)
        for pos, row in group.iterrows():
            prior = group.iloc[:pos]
            for metric in PROFILE_SOURCE_METRICS:
                feature_col = f"{metric}_expanding_prior"
                expected = prior[metric].mean(skipna=True) if len(prior) else np.nan
                actual = row[feature_col]
                checks_run += 1
                if pd.isna(expected) and pd.isna(actual):
                    continue
                if pd.isna(expected) != pd.isna(actual) or abs(float(expected) - float(actual)) > 1e-9:
                    mismatches.append({"match_id": int(row["match_id"]), "team_name": row["team_name"], "feature": feature_col})
                if len(mismatches) >= 20:
                    return {"checks_run": checks_run, "mismatch_count": len(mismatches), "sample_mismatches": mismatches}
    return {"checks_run": checks_run, "mismatch_count": len(mismatches), "sample_mismatches": mismatches}


def validate_features(df: pd.DataFrame, team_profiles: pd.DataFrame, match_df: pd.DataFrame, min_games: int, parquet_written: bool) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    duplicate_match_id = int(df.duplicated(subset=["match_id"]).sum())
    required_nulls = {column: int(df[column].isna().sum()) for column in ["match_id", "sofascore_event_id", "season", "match_date", "home_team", "away_team"]}
    forbidden_present = [column for column in df.columns if column in FORBIDDEN_OUTPUT_COLUMNS]
    target_like_present = [column for column in df.columns if column.startswith("target") or any(pattern in column for pattern in TARGET_DERIVED_PATTERNS)]
    missing_whitelist = [column for column in WHITELIST_FEATURES if column not in df.columns]
    missing_audit = [column for column in AUDIT_COLUMNS if column not in df.columns]
    leakage_validation = validate_no_profile_leakage(team_profiles)
    home_dates = pd.to_datetime(df["home_profile_max_match_date_used"], errors="coerce")
    away_dates = pd.to_datetime(df["away_profile_max_match_date_used"], errors="coerce")
    match_dates = pd.to_datetime(df["match_date"], errors="coerce")
    home_temporal_violations = int((home_dates.notna() & (home_dates >= match_dates)).sum())
    away_temporal_violations = int((away_dates.notna() & (away_dates >= match_dates)).sum())
    threshold_unknown_eligible = int((df["match_profile_eligible"].eq(1) & df["match_segment_eligible"].eq(0)).sum())
    if len(match_df) != EXPECTED_MATCHES:
        errors.append(f"Expected {EXPECTED_MATCHES} source matches, found {len(match_df)}.")
    if len(df) != EXPECTED_MATCHES:
        errors.append(f"Expected {EXPECTED_MATCHES} output rows, found {len(df)}.")
    if duplicate_match_id:
        errors.append(f"Duplicate match_id rows found: {duplicate_match_id}.")
    if any(required_nulls.values()):
        errors.append("Required identifier columns contain null values.")
    if forbidden_present:
        errors.append(f"Forbidden full-match/leakage columns present in output: {forbidden_present}.")
    if target_like_present:
        errors.append(f"Target-derived columns present in output: {target_like_present}.")
    if missing_whitelist:
        errors.append(f"Missing whitelisted columns: {missing_whitelist}.")
    if missing_audit:
        errors.append(f"Missing audit columns: {missing_audit}.")
    if leakage_validation["mismatch_count"]:
        errors.append("Historical profile recomputation found shift/expanding mismatches.")
    if home_temporal_violations or away_temporal_violations:
        errors.append("Profile max match_date used is not strictly before current match_date for at least one row.")
    if not parquet_written:
        errors.append("Parquet export was not created.")
    if threshold_unknown_eligible:
        warnings.append(f"{threshold_unknown_eligible} matches have min_games satisfied but unknown segments because strict prior-date threshold pools were not yet sufficient.")
    warnings.append("Segment ambos_defesa_forte remains under Quant review due to counterintuitive exploratory signal.")
    warnings.append("Dynamic tercile classification may be unstable in small early-season samples.")
    warnings.append("Same-day matches are handled conservatively: threshold pools use prior match dates only.")
    segment_columns = ["ofensivo_forte_vs_defesa_fragil", "ambos_defesa_forte", "defesa_fragil_vs_defesa_fragil", "ofensivo_forte_vs_ofensivo_forte", "ofensivo_fraco_vs_defesa_forte", "ao_menos_um_ofensivo_forte", "ao_menos_uma_defesa_fragil", "sem_ofensivo_forte_sem_defesa_fragil"]
    return {
        "feature_set_name": FEATURE_SET_NAME,
        "feature_set_version": FEATURE_SET_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "NAO APTO" if errors else "APTO COM RESSALVAS" if warnings else "APTO",
        "row_count": int(len(df)),
        "expected_rows": EXPECTED_MATCHES,
        "unique_matches": int(df["match_id"].nunique()),
        "team_rows": int(len(team_profiles)),
        "min_games": int(min_games),
        "match_profile_eligible_count": int(df["match_profile_eligible"].sum()),
        "match_segment_eligible_count": int(df["match_segment_eligible"].sum()),
        "match_profile_ineligible_count": int((df["match_profile_eligible"].eq(0)).sum()),
        "threshold_unknown_eligible_count": threshold_unknown_eligible,
        "segment_counts": {column: int(df[column].sum()) for column in segment_columns},
        "duplicate_match_id_rows": duplicate_match_id,
        "required_null_counts": required_nulls,
        "forbidden_columns_present": forbidden_present,
        "target_like_columns_present": target_like_present,
        "missing_whitelist_columns": missing_whitelist,
        "missing_audit_columns": missing_audit,
        "temporal_leakage_validation": {
            "profile_recompute": leakage_validation,
            "home_profile_max_date_violations": home_temporal_violations,
            "away_profile_max_date_violations": away_temporal_violations,
            "shift_1_before_expanding": True,
            "same_day_threshold_policy": "prior_match_dates_only",
            "target_columns_excluded": True,
        },
        "parquet_written": parquet_written,
        "validation_errors": errors,
        "validation_warnings": warnings,
    }


def build_metadata(df: pd.DataFrame, validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "feature_set_name": FEATURE_SET_NAME,
        "feature_set_version": FEATURE_SET_VERSION,
        "builder_version": BUILDER_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "grain": "one row per match_id",
        "source_tables": ["matches_master", "match_statistics"],
        "read_only_postgresql": True,
        "known_skipped_match_ids": sorted(KNOWN_SKIPPED_MATCH_IDS),
        "expected_matches": EXPECTED_MATCHES,
        "row_count": int(len(df)),
        "min_games": validation["min_games"],
        "profile_method": "expanding_prior_season_to_date_shift_1",
        "profile_threshold_method": "dynamic_terciles_from_prior_match_dates_only",
        "whitelist_features": WHITELIST_FEATURES,
        "audit_columns": AUDIT_COLUMNS,
        "historical_audit_columns": HISTORICAL_AUDIT_COLUMNS,
        "output_columns": list(df.columns),
        "anti_leakage_rules": [
            "groupby(season, team_name).shift(1) is applied before expanding means.",
            "Current match statistics are never used in the current match profile.",
            "Threshold pools use only prior match dates to avoid same-day/same-round leakage.",
            "No target, late-goal, final-score, xG, forecast, H8 graph or shotmap columns are exported.",
            "Rows with min_games < 5 are preserved and marked ineligible.",
        ],
        "limitations": [
            "ambos_defesa_forte remains under Quant review.",
            "Dynamic terciles can be unstable in small samples.",
            "Same-day matches are handled conservatively because reliable round/kickoff ordering is limited.",
            "No target is attached by default; downstream validation must join targets explicitly if approved.",
        ],
        "validation_status": validation["status"],
        "output_files": {"csv": str(CSV_PATH), "parquet": str(PARQUET_PATH), "metadata": str(METADATA_PATH), "validation_report": str(VALIDATION_PATH)},
    }


def write_outputs(df: pd.DataFrame, metadata: dict[str, Any], validation: dict[str, Any], output_dir: Path) -> dict[str, str | None]:
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
    validation["parquet_written"] = parquet_written
    if not parquet_written and "Parquet export was not created." not in validation["validation_errors"]:
        validation["validation_errors"].append("Parquet export was not created.")
        validation["status"] = "NAO APTO"
    metadata["validation_status"] = validation["status"]
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")
    validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2, default=json_default), encoding="utf-8")
    return {"csv": str(csv_path), "parquet": str(parquet_path) if parquet_written else None, "metadata": str(metadata_path), "validation_report": str(validation_path)}


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir)
    min_games = int(args.min_games)
    print("Building Team Profile Segment Feature Set V1")
    print(f"output_dir={output_dir}")
    print(f"min_games={min_games}")
    print(f"table_counts={table_counts()}")
    df, team_profiles, match_df = build_feature_dataframe(min_games=min_games)
    validation = validate_features(df, team_profiles, match_df, min_games=min_games, parquet_written=parquet_engine_available())
    metadata = build_metadata(df, validation)
    outputs = write_outputs(df, metadata, validation, output_dir)
    print("FINAL SUMMARY")
    print(f"rows={len(df)}")
    print(f"unique_matches={df['match_id'].nunique()}")
    print(f"match_profile_eligible={int(df['match_profile_eligible'].sum())}")
    print(f"match_segment_eligible={int(df['match_segment_eligible'].sum())}")
    print(f"status={validation['status']}")
    print(f"errors={len(validation['validation_errors'])}")
    print(f"warnings={len(validation['validation_warnings'])}")
    print(json.dumps(outputs, ensure_ascii=False, indent=2))
    return 1 if validation["validation_errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
