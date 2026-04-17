#!/usr/bin/env python3
"""
Validate a final project holdout predictions submission.

Usage:
    python validate_submission.py path/to/LastName_FirstName_holdout_predictions.csv SCENARIO_NUM

Example:
    python validate_submission.py Smith_Jane_holdout_predictions.csv 06
    python validate_submission.py TeamName_holdout_predictions.csv 25

The scenario number is required — it determines which submission format is expected:
    - Binary scenarios (01-20, 29):     id, predicted_probability
    - Multi-class scenarios (21, 22,
      24, 25, 26, 28):                   id, predicted_class, prob_<class1>, prob_<class2>, ...
    - Regression scenarios (23, 27, 30): id, predicted_value

Exit codes:
    0 = submission passes all checks
    1 = one or more checks failed
"""
import sys
import os
from pathlib import Path


BINARY = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 29}
MULTICLASS = {21, 22, 24, 25, 26, 28}
REGRESSION = {23, 27, 30}


def error(msg):
    print(f"\033[91m✗ {msg}\033[0m")


def ok(msg):
    print(f"\033[92m✓ {msg}\033[0m")


def warn(msg):
    print(f"\033[93m⚠ {msg}\033[0m")


def info(msg):
    print(f"  {msg}")


def load_csv(path):
    try:
        import pandas as pd
    except ImportError:
        error("pandas is required. Install with: pip install pandas")
        sys.exit(1)
    try:
        return pd.read_csv(path)
    except Exception as e:
        error(f"Cannot read file as CSV: {e}")
        sys.exit(1)


def expected_rows(scenario_num):
    cases_dir = Path(__file__).parent.parent / 'cases'
    matching = [d for d in cases_dir.iterdir()
                if d.is_dir() and d.name.startswith(f"{scenario_num:02d}-")]
    if not matching:
        return None
    holdout_path = matching[0] / 'holdout_features.csv'
    if not holdout_path.exists():
        return None
    try:
        return sum(1 for _ in open(holdout_path)) - 1
    except Exception:
        return None


def check_id_column(df):
    issues = 0
    if df['id'].dtype.kind not in 'iu':
        error(f"'id' column must be integer (got {df['id'].dtype})")
        issues += 1
    else:
        ok("'id' column is integer type")
    if df['id'].duplicated().any():
        n_dups = df['id'].duplicated().sum()
        error(f"'id' column has {n_dups} duplicate values — each row must have a unique id")
        issues += 1
    else:
        ok("'id' values are unique")
    return issues


def check_prob_column(df, col, label=None):
    """Check that a column is float-valued in [0,1] with no NaN."""
    issues = 0
    tag = f"'{col}'" if label is None else f"'{col}' ({label})"
    if df[col].dtype.kind != 'f':
        error(f"{tag} must be float (got {df[col].dtype})")
        return issues + 1
    n_nan = df[col].isna().sum()
    if n_nan > 0:
        error(f"{tag} has {n_nan} missing/NaN values")
        issues += 1
    min_p, max_p = df[col].min(), df[col].max()
    if min_p < 0 or max_p > 1:
        error(f"{tag} must be in [0, 1] (got min={min_p:.4f}, max={max_p:.4f})")
        issues += 1
    return issues


def validate_binary(df, scenario_num):
    issues = 0
    expected = {'id', 'predicted_probability'}
    missing = expected - set(df.columns)
    if missing:
        error(f"Missing required columns: {missing}")
        return 1
    ok("Required columns present: 'id', 'predicted_probability'")
    extra = set(df.columns) - expected
    if extra:
        warn(f"Extra columns will be ignored: {extra}")
    issues += check_id_column(df)
    issues += check_prob_column(df, 'predicted_probability')
    if issues == 0:
        min_p, max_p = df['predicted_probability'].min(), df['predicted_probability'].max()
        ok(f"Probabilities in valid range [{min_p:.4f}, {max_p:.4f}]")
        if min_p == max_p:
            warn(f"All probabilities are identical ({min_p}) — is this intentional?")
            issues += 1
        n_extreme = ((df['predicted_probability'] == 0) | (df['predicted_probability'] == 1)).sum()
        if n_extreme == len(df):
            warn("All probabilities are exactly 0 or 1 — did you submit class labels instead of probabilities?")
            issues += 1
        mean_p = df['predicted_probability'].mean()
        if mean_p < 0.001 or mean_p > 0.999:
            warn(f"Mean probability is extreme ({mean_p:.4f}) — all rows classified the same way?")
            issues += 1
        else:
            info(f"Mean probability: {mean_p:.4f}")
        n_above = (df['predicted_probability'] >= 0.5).sum()
        info(f"Predictions >= 0.5: {n_above} / {len(df)} ({n_above/len(df):.1%})")
    return issues


def validate_multiclass(df, scenario_num):
    issues = 0
    if 'id' not in df.columns:
        error("Missing required column: 'id'")
        return 1
    if 'predicted_class' not in df.columns:
        error("Missing required column: 'predicted_class'")
        return 1
    ok("Required columns present: 'id', 'predicted_class'")
    prob_cols = [c for c in df.columns if c.startswith('prob_')]
    if not prob_cols:
        error("No probability columns found. Expected one column per class named 'prob_<class>'.")
        return issues + 1
    ok(f"Per-class probability columns: {prob_cols}")
    issues += check_id_column(df)
    pred_classes = set(df['predicted_class'].dropna().astype(str).unique())
    prob_classes = {c[len('prob_'):] for c in prob_cols}
    missing_prob = pred_classes - prob_classes
    if missing_prob:
        warn(f"predicted_class values without matching prob_<class> column: {missing_prob}")
        issues += 1
    for c in prob_cols:
        issues += check_prob_column(df, c)
    try:
        row_sums = df[prob_cols].sum(axis=1)
        off = (row_sums - 1).abs()
        if (off > 0.02).any():
            n_bad = (off > 0.02).sum()
            warn(f"{n_bad} rows have per-class probabilities that don't sum to ~1 (tolerance 0.02). Did you forget to normalize?")
            issues += 1
        else:
            ok("Per-class probabilities sum to ~1 on all rows")
    except Exception as e:
        warn(f"Could not verify probability normalization: {e}")
    info(f"predicted_class distribution: {dict(df['predicted_class'].value_counts())}")
    return issues


def validate_regression(df, scenario_num):
    issues = 0
    expected = {'id', 'predicted_value'}
    missing = expected - set(df.columns)
    if missing:
        error(f"Missing required columns: {missing}")
        return 1
    ok("Required columns present: 'id', 'predicted_value'")
    extra = set(df.columns) - expected
    if extra:
        warn(f"Extra columns will be ignored: {extra}")
    issues += check_id_column(df)
    if df['predicted_value'].dtype.kind != 'f':
        error(f"'predicted_value' must be float (got {df['predicted_value'].dtype})")
        issues += 1
    n_nan = df['predicted_value'].isna().sum()
    if n_nan > 0:
        error(f"'predicted_value' has {n_nan} missing/NaN values")
        issues += 1
    if issues == 0:
        vmin, vmax, vmean = df['predicted_value'].min(), df['predicted_value'].max(), df['predicted_value'].mean()
        info(f"predicted_value: min={vmin:.4g}, mean={vmean:.4g}, max={vmax:.4g}")
        if (df['predicted_value'] < 0).any() and scenario_num in REGRESSION:
            warn("Some predicted_value entries are negative — confirm this is expected for your target.")
    return issues


def validate(path, scenario_num):
    if not os.path.isfile(path):
        error(f"File not found: {path}")
        return 1
    ok(f"File exists: {path}")
    filename = os.path.basename(path)
    if not filename.endswith('_holdout_predictions.csv'):
        warn(f"Filename should end with '_holdout_predictions.csv' (got: {filename})")
    else:
        ok(f"Filename format: {filename}")
    df = load_csv(path)
    ok(f"File readable as CSV ({len(df)} rows, {len(df.columns)} columns)")

    if scenario_num in BINARY:
        mode = "binary"
        issues = validate_binary(df, scenario_num)
    elif scenario_num in MULTICLASS:
        mode = "multi-class"
        issues = validate_multiclass(df, scenario_num)
    elif scenario_num in REGRESSION:
        mode = "regression"
        issues = validate_regression(df, scenario_num)
    else:
        error(f"Unknown scenario number: {scenario_num}. Must be 01-30.")
        return 1
    info(f"Validated as {mode} submission (scenario {scenario_num:02d})")

    expected = expected_rows(scenario_num)
    if expected is None:
        warn(f"Could not locate holdout_features.csv for scenario {scenario_num:02d} — skipping row-count check")
    elif len(df) == expected:
        ok(f"Row count matches holdout_features.csv ({expected} rows)")
    else:
        error(f"Row count mismatch: submission has {len(df)} rows, holdout_features.csv has {expected} rows")
        issues += 1

    print()
    if issues == 0:
        ok("All checks passed. Submission looks valid.")
        return 0
    error(f"{issues} issue(s) found. Fix before submitting.")
    return 1


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        return 0
    if len(sys.argv) < 3:
        error("Scenario number is required. Usage: python validate_submission.py FILE.csv SCENARIO_NUM")
        return 1
    path = sys.argv[1]
    try:
        scenario_num = int(sys.argv[2])
    except ValueError:
        error(f"Scenario number must be an integer (got: {sys.argv[2]})")
        return 1
    return validate(path, scenario_num)


if __name__ == '__main__':
    sys.exit(main())
