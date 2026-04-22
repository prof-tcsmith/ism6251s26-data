"""Generate the synthetic Heritage Community Bank dataset for the ISM 6251 Week 11 assignment.

Produces `heritage_customers.csv` (5,000 rows) with realistic retail-bank behavioral
data: account balances (checking, savings, CD, investment), transaction patterns,
channel-preference counts (mobile / online / branch), product holdings, and
demographics. Several natural segments are planted by boosting features for three
overlapping archetypes (young digital-first, affluent investors, mature savers).

Students segment this data with K-Means, Agglomerative, DBSCAN, and GMM, and compare
families. No ground-truth label column is included — segmentation is unsupervised.

Running this script is reproducible (`seed=42`). The committed CSV in this folder
is the output of running this script on that seed.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate(n_customers: int = 5_000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    tenure_months = np.random.exponential(60, n_customers).clip(3, 360).astype(int)

    checking_balance   = np.random.lognormal(7, 1.5, n_customers).clip(100, 500_000)
    savings_balance    = np.random.lognormal(8, 2.0, n_customers).clip(0, 1_000_000)
    cd_balance         = np.random.exponential(15_000, n_customers).clip(0, 500_000)
    investment_balance = np.random.lognormal(9, 2.5, n_customers).clip(0, 2_000_000)

    # Zero-out some balances to create realistic product adoption
    savings_balance    *= np.random.binomial(1, 0.70, n_customers)  # 30% have none
    cd_balance         *= np.random.binomial(1, 0.25, n_customers)  # 75% have none
    investment_balance *= np.random.binomial(1, 0.20, n_customers)  # 80% have none

    monthly_transactions   = np.random.poisson(25, n_customers).clip(1, 200)
    avg_transaction_amount = np.random.lognormal(3.5, 0.8, n_customers).clip(10, 5_000)
    debit_card_usage       = np.random.poisson(15, n_customers).clip(0, 100)
    atm_withdrawals        = np.random.poisson(3, n_customers).clip(0, 30)

    mobile_logins_monthly  = np.random.poisson(12, n_customers).clip(0, 60).astype(float)
    online_logins_monthly  = np.random.poisson(8,  n_customers).clip(0, 40).astype(int)
    branch_visits_monthly  = np.random.poisson(1,  n_customers).clip(0, 10).astype(float)

    has_mortgage      = np.random.binomial(1, 0.25, n_customers)
    has_auto_loan     = np.random.binomial(1, 0.15, n_customers)
    has_credit_card   = np.random.binomial(1, 0.55, n_customers)
    has_personal_loan = np.random.binomial(1, 0.08, n_customers)

    age             = np.random.normal(45, 15, n_customers).clip(18, 85).astype(int)
    income_estimate = np.random.lognormal(10.8, 0.7, n_customers).clip(20_000, 500_000)

    # Planted archetypes: young digital-first
    young_digital = (age < 35) & (np.random.random(n_customers) > 0.5)
    mobile_logins_monthly = np.where(young_digital, mobile_logins_monthly * 2,   mobile_logins_monthly)
    branch_visits_monthly = np.where(young_digital, branch_visits_monthly * 0.2, branch_visits_monthly)

    # Planted archetype: affluent investors
    affluent = (income_estimate > 150_000) & (np.random.random(n_customers) > 0.4)
    investment_balance = np.where(
        affluent,
        investment_balance + np.random.lognormal(11, 1, n_customers),
        investment_balance,
    )
    checking_balance = np.where(affluent, checking_balance * 1.5, checking_balance)

    # Planted archetype: mature savers
    mature = (age > 60) & (np.random.random(n_customers) > 0.5)
    cd_balance            = np.where(mature, cd_balance + np.random.lognormal(10, 0.8, n_customers), cd_balance)
    savings_balance       = np.where(mature, savings_balance * 1.5, savings_balance)
    mobile_logins_monthly = np.where(mature, mobile_logins_monthly * 0.3, mobile_logins_monthly)
    branch_visits_monthly = np.where(mature, branch_visits_monthly * 2,   branch_visits_monthly)

    df = pd.DataFrame({
        "customer_id":             range(1, n_customers + 1),
        "tenure_months":           tenure_months,
        "age":                     age,
        "income_estimate":         income_estimate.round(0),
        "checking_balance":        checking_balance.round(2),
        "savings_balance":         savings_balance.round(2),
        "cd_balance":              cd_balance.round(2),
        "investment_balance":      investment_balance.round(2),
        "monthly_transactions":    monthly_transactions,
        "avg_transaction_amount":  avg_transaction_amount.round(2),
        "debit_card_usage":        debit_card_usage,
        "atm_withdrawals":         atm_withdrawals,
        "mobile_logins_monthly":   mobile_logins_monthly.astype(int),
        "online_logins_monthly":   online_logins_monthly,
        "branch_visits_monthly":   branch_visits_monthly.round(1),
        "has_mortgage":            has_mortgage,
        "has_auto_loan":           has_auto_loan,
        "has_credit_card":         has_credit_card,
        "has_personal_loan":       has_personal_loan,
    })

    df["total_deposits"]     = df["checking_balance"] + df["savings_balance"] + df["cd_balance"]
    df["total_relationship"] = df["total_deposits"] + df["investment_balance"]
    df["num_products"]       = (
        df["has_mortgage"] + df["has_auto_loan"] + df["has_credit_card"] + df["has_personal_loan"]
        + (df["savings_balance"]    > 0).astype(int)
        + (df["cd_balance"]         > 0).astype(int)
        + (df["investment_balance"] > 0).astype(int)
    )
    df["digital_engagement"] = df["mobile_logins_monthly"] + df["online_logins_monthly"]
    return df


def main() -> None:
    df = generate()
    out = Path(__file__).parent / "heritage_customers.csv"
    df.to_csv(out, index=False)
    print(f"Wrote {out}  ({len(df):,} rows, {df.shape[1]} cols)")


if __name__ == "__main__":
    main()
