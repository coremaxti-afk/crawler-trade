"""Configuration for Baseline 1 pre-match H3/H4 experiment."""
from __future__ import annotations
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
BASELINE_NAME = "baseline_1_prematch_h3_h4"
BASELINE_VERSION = "v1a"
TARGET_COLUMN = "target_late_goal_75"
TRAIN_RATIO = 0.60
VALIDATION_RATIO = 0.20
TEST_RATIO = 0.20
SHUFFLE = False
RANDOM_STATE = 42
FEATURE_INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "features" / "historical_prematch_features_v1.csv"
FEATURE_METADATA_PATH = PROJECT_ROOT / "data" / "processed" / "features" / "historical_prematch_features_v1_metadata.json"
FEATURE_VALIDATION_PATH = PROJECT_ROOT / "data" / "processed" / "features" / "historical_prematch_features_v1_validation_report.json"
DATASET_INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_v1.csv"
DATASET_METADATA_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_v1_metadata.json"
DATASET_VALIDATION_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_v1_validation_report.json"
BASELINE_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "baseline"
REPORT_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "reports"
MODEL_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "models"
DOC_REPORT_PATH = PROJECT_ROOT / "docs" / "04_RESEARCH" / "BASELINE_PREMATCH_H3_H4_RESULTS.md"
BASELINE_DATASET_PATH = BASELINE_OUTPUT_DIR / "baseline_1_prematch_dataset.csv"
TRAIN_DATASET_PATH = BASELINE_OUTPUT_DIR / "baseline_1_prematch_train.csv"
VALIDATION_DATASET_PATH = BASELINE_OUTPUT_DIR / "baseline_1_prematch_validation.csv"
TEST_DATASET_PATH = BASELINE_OUTPUT_DIR / "baseline_1_prematch_test.csv"
FEATURE_MANIFEST_PATH = REPORT_OUTPUT_DIR / "baseline_1_prematch_feature_manifest.json"
SPLIT_REPORT_PATH = REPORT_OUTPUT_DIR / "baseline_1_prematch_split_report.json"
IMPUTATION_REPORT_PATH = REPORT_OUTPUT_DIR / "baseline_1_prematch_imputation_report.json"
METRICS_PATH = REPORT_OUTPUT_DIR / "baseline_1_prematch_metrics.json"
VALIDATION_REPORT_PATH = REPORT_OUTPUT_DIR / "baseline_1_prematch_validation_report.json"
MODEL_PATH = MODEL_OUTPUT_DIR / "baseline_1_prematch_model.pkl"
ALLOWED_TEAM_LEVEL_FEATURES = [
    "goals_for_avg_last_3",
    "goals_for_avg_last_10",
    "shots_on_target_for_avg_last_5",
    "shots_against_avg_last_5",
    "shots_on_target_against_avg_last_5",
    "big_chances_against_avg_last_5",
]
ALLOWED_MATCH_LEVEL_FEATURES_1A = [
    "home_goals_for_avg_last_3",
    "home_goals_for_avg_last_10",
    "home_shots_on_target_for_avg_last_5",
    "home_shots_against_avg_last_5",
    "home_shots_on_target_against_avg_last_5",
    "home_big_chances_against_avg_last_5",
    "away_goals_for_avg_last_3",
    "away_goals_for_avg_last_10",
    "away_shots_on_target_for_avg_last_5",
    "away_shots_against_avg_last_5",
    "away_shots_on_target_against_avg_last_5",
    "away_big_chances_against_avg_last_5",
]
OPTIONAL_DIFF_FEATURES_1B = [
    "diff_goals_for_avg_last_3",
    "diff_goals_for_avg_last_10",
    "diff_shots_on_target_for_avg_last_5",
    "diff_shots_against_avg_last_5",
    "diff_shots_on_target_against_avg_last_5",
    "diff_big_chances_against_avg_last_5",
]
IDENTIFIER_COLUMNS = [
    "match_id",
    "sofascore_event_id",
    "league",
    "season",
    "match_date",
    "home_team",
    "away_team",
    "home_history_matches_available",
    "away_history_matches_available",
    "home_is_early_season",
    "away_is_early_season",
]
FORBIDDEN_FEATURE_PATTERNS = [
    "target", "late_goal", "has_late_goal", "home_late_goal", "away_late_goal",
    "first_late_goal", "last_goal", "incident", "score", "cutoff", "cards_until",
    "substitutions_until", "xg", "xga", "forecast", "home_goals", "away_goals", "total_goals",
]
APPROVAL_CRITERIA = {
    "roc_auc_test_min": 0.55,
    "pr_auc_test_margin_vs_prevalence": 0.03,
    "roc_auc_validation_test_max_gap": 0.07,
}
