"""Generate the synthetic Meridian Home Goods RFM dataset for the ISM 6251 Week 11 sample solution.

Produces `meridian_rfm.csv` (3,000 rows) with the three classic RFM features — Recency
(days since last purchase), Frequency (purchases in the last 12 months), and Monetary
(total spend in the last 12 months). Five overlapping customer behaviors are planted —
Champions, Loyal, Potential Loyalists, At Risk, and Hibernating — so K-Means and GMM
can separate them while DBSCAN, which expects density separation, will under-cluster.

Running this script is reproducible (`seed=42`). The committed CSV in this folder is
the output of running this script on that seed.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate(seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    # Segment 1: Champions - ~15%
    n1 = 450
    r1 = np.random.exponential(15, n1).clip(1, 45).astype(int)
    f1 = np.random.normal(12, 3, n1).clip(8, 25).astype(int)
    m1 = np.random.normal(2500, 800, n1).clip(1000, 5000)

    # Segment 2: Loyal - ~20%
    n2 = 600
    r2 = np.random.normal(45, 20, n2).clip(15, 90).astype(int)
    f2 = np.random.normal(6, 2, n2).clip(4, 12).astype(int)
    m2 = np.random.normal(1200, 400, n2).clip(500, 2500)

    # Segment 3: Potential Loyalists - ~15%
    n3 = 450
    r3 = np.random.exponential(20, n3).clip(1, 60).astype(int)
    f3 = np.random.poisson(2, n3).clip(1, 4).astype(int)
    m3 = np.random.normal(400, 150, n3).clip(100, 900)

    # Segment 4: At Risk - ~20%
    n4 = 600
    r4 = np.random.normal(150, 50, n4).clip(90, 270).astype(int)
    f4 = np.random.normal(5, 2, n4).clip(3, 10).astype(int)
    m4 = np.random.normal(1000, 350, n4).clip(400, 2000)

    # Segment 5: Hibernating - ~30%
    n5 = 900
    r5 = np.random.normal(250, 80, n5).clip(150, 400).astype(int)
    f5 = np.random.poisson(2, n5).clip(1, 5).astype(int)
    m5 = np.random.normal(300, 150, n5).clip(50, 700)

    recency   = np.concatenate([r1, r2, r3, r4, r5])
    frequency = np.concatenate([f1, f2, f3, f4, f5])
    monetary  = np.concatenate([m1, m2, m3, m4, m5])

    n_customers = len(recency)
    df = pd.DataFrame({
        "customer_id": range(1, n_customers + 1),
        "recency":     recency,
        "frequency":   frequency,
        "monetary":    monetary.round(2),
    })
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


def main() -> None:
    df = generate()
    out = Path(__file__).parent / "meridian_rfm.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {out}  ({len(df):,} rows, {df.shape[1]} cols)")


if __name__ == "__main__":
    main()
