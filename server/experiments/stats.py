"""Statistics helpers for experiment analysis.

Provides Wilson confidence intervals for proportions, a chi-square test of
independence over a contingency table, and Cramer's V as an effect size.
"""

from __future__ import annotations

import math
from typing import Dict, List, Sequence

import numpy as np
from scipy import stats


def mean_metric_by_group(
    values_by_group: Dict[str, List[float]]
) -> Dict[str, Dict[str, float]]:
    """Summarize a numeric metric (e.g. chosen-pen price) per group.

    Returns ``{group: {mean, sd, n, sem}}``. Used for the budget experiment's
    headline measure (mean spend per step-structure condition), which the
    categorical chi-square chart does not express.
    """
    out: Dict[str, Dict[str, float]] = {}
    for group, xs in values_by_group.items():
        n = len(xs)
        if n == 0:
            out[group] = {"mean": None, "sd": None, "n": 0, "sem": None}
            continue
        arr = np.array(xs, dtype=float)
        sd = float(arr.std(ddof=1)) if n > 1 else 0.0
        out[group] = {
            "mean": round(float(arr.mean()), 4),
            "sd": round(sd, 4),
            "n": n,
            "sem": round(sd / math.sqrt(n), 4) if n > 1 else 0.0,
        }
    return out


def two_sample_t(a: Sequence[float], b: Sequence[float]) -> Dict[str, object]:
    """Welch's two-sample t-test comparing two groups of numeric values.

    Returns a null-ish result when either group is too small to test.
    """
    if len(a) < 2 or len(b) < 2:
        return {
            "t": None,
            "pValue": None,
            "significant": False,
            "testable": False,
        }
    t, p = stats.ttest_ind(np.array(a, dtype=float), np.array(b, dtype=float), equal_var=False)
    return {
        "t": round(float(t), 4),
        "pValue": float(p),
        "significant": bool(p < 0.05),
        "testable": True,
    }


def wilson_interval(count: int, total: int, z: float = 1.96) -> List[float]:
    """Return the [low, high] Wilson score interval for a proportion.

    The Wilson interval behaves well for small samples and proportions near 0
    or 1, which is exactly the regime these experiments operate in.
    """
    if total == 0:
        return [0.0, 0.0]
    phat = count / total
    denom = 1.0 + (z * z) / total
    center = (phat + (z * z) / (2 * total)) / denom
    margin = (
        z
        * math.sqrt((phat * (1 - phat) + (z * z) / (4 * total)) / total)
        / denom
    )
    low = max(0.0, center - margin)
    high = min(1.0, center + margin)
    return [round(low, 4), round(high, 4)]


def chi_square_contingency(table: Sequence[Sequence[int]]) -> Dict[str, object]:
    """Run a chi-square test of independence on a contingency table.

    Rows are typically variants, columns are decision options. Returns the test
    statistic, p-value, degrees of freedom, a significance flag (alpha = 0.05),
    and Cramer's V effect size. Returns a null-ish result when the table is too
    sparse for a meaningful test.
    """
    matrix = np.array(table, dtype=float)

    # Drop options (columns) and variants (rows) that never occur: an option no
    # model ever chose carries no information for a test of independence, and an
    # all-zero row/column would force a zero marginal that breaks chi-square.
    if matrix.size:
        matrix = matrix[matrix.sum(axis=1) != 0]
        if matrix.size:
            matrix = matrix[:, matrix.sum(axis=0) != 0]

    grand_total = float(matrix.sum()) if matrix.size else 0.0

    # A degenerate table (empty or only a single row/column) cannot be tested.
    if (
        matrix.size == 0
        or grand_total == 0
        or matrix.shape[0] < 2
        or matrix.shape[1] < 2
    ):
        return {
            "statistic": None,
            "pValue": None,
            "dof": None,
            "significant": False,
            "cramersV": None,
            "testable": False,
        }

    chi2, p_value, dof, _expected = stats.chi2_contingency(matrix)

    n_rows, n_cols = matrix.shape
    min_dim = min(n_rows - 1, n_cols - 1)
    cramers_v = (
        math.sqrt(chi2 / (grand_total * min_dim)) if min_dim > 0 else None
    )

    return {
        "statistic": round(float(chi2), 4),
        "pValue": float(p_value),
        "dof": int(dof),
        "significant": bool(p_value < 0.05),
        "cramersV": round(float(cramers_v), 4) if cramers_v is not None else None,
        "testable": True,
    }
