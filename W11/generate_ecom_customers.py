"""Generate the synthetic e-commerce customer dataset for the ISM 6251 Week 11 lecture.

Produces `ecom_customers.csv` (1,000 rows) with four planted behavioral segments —
Champions, At-Risk, New, and Loyal Regulars — described by RFM-style features plus
tenure and derived average-order-value. A `true_segment` column is retained so the
lecture notebook can compute external metrics (ARI, NMI) when evaluating each
clustering family; the clustering models themselves never see this column.

Running this script is reproducible (`seed=42`). The committed CSV in this folder
is the output of running this script on that seed.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    def block(n, r_mean, r_sd, f_mean, f_sd, m_mean, m_sd, label):
        return pd.DataFrame({
            "recency_days":   rng.normal(r_mean, r_sd, n).clip(1, 365),
            "frequency":      rng.normal(f_mean, f_sd, n).clip(1, None),
            "monetary":       rng.lognormal(m_mean, m_sd, n),
            "tenure_months":  rng.normal(24, 12, n).clip(1, 96),
            "true_segment":   label,
        })

    df = pd.concat([
        block(200,  10,  4, 20, 4, 7.5, 0.4, "Champions"),
        block(250, 120, 40,  8, 3, 6.5, 0.5, "At-Risk"),
        block(300,   8,  5,  2, 1, 5.5, 0.6, "New"),
        block(250,  20,  8, 12, 3, 6.0, 0.3, "Loyal Regulars"),
    ], ignore_index=True)

    df["avg_order_value"] = df["monetary"] / df["frequency"]
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


def main() -> None:
    df = generate()
    out = Path(__file__).parent / "ecom_customers.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {out}  ({len(df):,} rows, {df.shape[1]} cols)")
    print(df["true_segment"].value_counts().to_string())


if __name__ == "__main__":
    main()
