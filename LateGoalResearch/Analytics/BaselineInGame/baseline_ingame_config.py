"""Configuration for Baseline In-Game V1 controlled experiment."""
from __future__ import annotations
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BASELINE_NAME = "baseline_ingame_v1_h6_h9"
BASELINE_VERSION = "v1"
CUTOFF_MINUTE = 75
TARGET_COLUMN = "target_late_goal_75"
OPERATIONAL_TARGET_COLUMN = "target_goal_after_cutoff"
TRAIN_RATIO = 0.60
VALIDATION_RATIO = 0.20
TEST_RATIO = 0.20
SHUFFLE = False
RANDOM_STATE = 42

INGAME_DATASET_INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_v1b_ingame.csv"
INGAME_METADATA_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_v1b_ingame_metadata.json"
INGAME_VALIDATION_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_v1b_ingame_validation_report.json"
DATASET_V1_INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "datasets" / "late_goal_dataset_v1.csv"

BASELINE_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "baseline_ingame"
REPORT_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "reports"
DOC_REPORT_PATH = PROJECT_ROOT / "docs" / "04_RESEARCH" / "BASELINE_INGAME_V1_RESULTS.md"

BASELINE_DATASET_PATH = BASELINE_OUTPUT_DIR / "baseline_ingame_v1_dataset.csv"
TRAIN_DATASET_PATH = BASELINE_OUTPUT_DIR / "baseline_ingame_v1_train.csv"
VALIDATION_DATASET_PATH = BASELINE_OUTPUT_DIR / "baseline_ingame_v1_validation.csv"
TEST_DATASET_PATH = BASELINE_OUTPUT_DIR / "baseline_ingame_v1_test.csv"
FEATURE_MANIFEST_PATH = REPORT_OUTPUT_DIR / "baseline_ingame_v1_feature_manifest.json"
SPLIT_REPORT_PATH = REPORT_OUTPUT_DIR / "baseline_ingame_v1_split_report.json"
PREPROCESSING_REPORT_PATH = REPORT_OUTPUT_DIR / "baseline_ingame_v1_preprocessing_report.json"
METRICS_PATH = REPORT_OUTPUT_DIR / "baseline_ingame_v1_metrics.json"
VALIDATION_REPORT_PATH = REPORT_OUTPUT_DIR / "baseline_ingame_v1_validation_report.json"

NUMERIC_FEATURES = [
    "score_diff_home_until_cutoff",
    "cards_until_cutoff",
    "substitutions_until_cutoff",
]
CATEGORICAL_FEATURES = ["score_state_group"]
ALLOWED_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
IDENTIFIER_COLUMNS = [
    "match_id",
    "sofascore_event_id",
    "match_date",
    "home_team",
    "away_team",
    "cutoff_minute",
]
FORBIDDEN_FEATURE_PATTERNS = [
    "xg", "xga", "forecast", "late_goal", "target", "after_cutoff",
    "final", "full_match", "home_goals", "away_goals", "total_goals",
    "goal_last", "last_goal", "time_since_last_goal", "prematch",
]
APPROVAL_CRITERIA = {
    "roc_auc_test_min": 0.55,
    "pr_auc_test_margin_vs_prevalence": 0.03,
}
BASELINE_1A_REFERENCE = {
    "roc_auc_test": 0.4910,
    "pr_auc_test": 0.5364,
}
