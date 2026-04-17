"""Generate the synthetic insurance-claims dataset for the ISM 6251 Week 9 assignment.

Produces `insurance_claims.csv` (10,000 rows) with ~6% fraud rate. The fraud_score
mixes small marginal effects with strong pairwise and three-way interactions between
claim characteristics, policy age, reporting delay, corroboration, and prior fraud
flags. Ensembles recover the interactions; linear / shallow-tree baselines catch
only the marginals — which is exactly the pedagogical point of the assignment.

Running this script is reproducible (`np.random.seed(42)`). The committed CSV in
this folder is the output of running this script on that seed.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate(n_claims: int = 10_000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    # Policy characteristics
    policy_age_months = np.random.exponential(36, n_claims).clip(1, 240).astype(int)
    policy_type = np.random.choice(
        ["auto", "home", "commercial"], n_claims, p=[0.6, 0.3, 0.1]
    )
    premium_amount = np.random.lognormal(7, 0.5, n_claims).clip(500, 50000)

    # Claimant characteristics
    claimant_tenure_years = np.random.exponential(5, n_claims).clip(0.1, 30)
    prior_claims_3yr = np.random.poisson(0.8, n_claims)
    prior_fraud_flags = np.random.binomial(1, 0.02, n_claims)

    # Claim characteristics
    claim_amount = np.random.lognormal(8.5, 1, n_claims).clip(500, 200000)
    days_to_report = np.random.exponential(5, n_claims).clip(0, 90).astype(int)
    police_report_filed = np.random.binomial(1, 0.4, n_claims)
    witnesses_present = np.random.binomial(1, 0.3, n_claims)
    claim_description_length = (
        np.random.lognormal(5, 0.5, n_claims).clip(50, 2000).astype(int)
    )

    # Situational factors
    incident_hour = np.random.choice(range(24), n_claims)
    weekend_incident = np.random.binomial(1, 2 / 7, n_claims)
    holiday_adjacent = np.random.binomial(1, 0.08, n_claims)
    out_of_state = np.random.binomial(1, 0.12, n_claims)

    # Financial stress indicators
    recent_policy_change = np.random.binomial(1, 0.15, n_claims)
    coverage_increase_90d = np.random.binomial(1, 0.08, n_claims)
    payment_issues = np.random.binomial(1, 0.10, n_claims)

    # Claim processing
    adjuster_experience_years = np.random.exponential(5, n_claims).clip(0.5, 25)
    documentation_complete = np.random.binomial(1, 0.85, n_claims)
    repair_shop_preferred = np.random.binomial(1, 0.6, n_claims)

    # Interaction flags — real fraud combines signals (new policy + big claim,
    # late report without police report, etc.). Linear and shallow models
    # capture the marginals but miss the interactions; ensembles recover them.
    high_claim_flag = (claim_amount > np.percentile(claim_amount, 85)).astype(int)
    new_policy_flag = (policy_age_months < 6).astype(int)
    late_report_flag = (days_to_report > 14).astype(int)
    no_police_flag = 1 - police_report_filed
    no_witness_flag = 1 - witnesses_present
    night_flag = ((incident_hour >= 22) | (incident_hour <= 4)).astype(int)
    distress_flag = (
        (coverage_increase_90d + payment_issues + recent_policy_change) >= 1
    ).astype(int)

    fraud_score = (
        -4.5
        # Weak marginal effects
        + 0.15 * new_policy_flag + 0.15 * late_report_flag
        - 0.25 * police_report_filed - 0.15 * witnesses_present
        + 0.10 * coverage_increase_90d + 0.10 * payment_issues + 0.10 * night_flag
        # Strong interaction effects — only ensembles reliably recover these
        + 3.0 * new_policy_flag * high_claim_flag
        + 2.5 * late_report_flag * no_police_flag
        + 2.5 * high_claim_flag * no_witness_flag * no_police_flag
        + 2.0 * distress_flag * high_claim_flag
        + 2.0 * new_policy_flag * prior_fraud_flags
        + 1.5 * night_flag * no_witness_flag
        + 1.5 * out_of_state * late_report_flag
        + 3.0 * prior_fraud_flags
        + np.random.normal(0, 0.1, n_claims)
    )

    fraud_probability = 1 / (1 + np.exp(-fraud_score))
    is_fraud = (np.random.random(n_claims) < fraud_probability).astype(int)

    df = pd.DataFrame(
        {
            "claim_id": range(1, n_claims + 1),
            "policy_age_months": policy_age_months,
            "policy_type": policy_type,
            "premium_amount": premium_amount.round(2),
            "claimant_tenure_years": claimant_tenure_years.round(1),
            "prior_claims_3yr": prior_claims_3yr,
            "prior_fraud_flags": prior_fraud_flags,
            "claim_amount": claim_amount.round(2),
            "days_to_report": days_to_report,
            "police_report_filed": police_report_filed,
            "witnesses_present": witnesses_present,
            "claim_description_length": claim_description_length,
            "incident_hour": incident_hour,
            "weekend_incident": weekend_incident,
            "holiday_adjacent": holiday_adjacent,
            "out_of_state": out_of_state,
            "recent_policy_change": recent_policy_change,
            "coverage_increase_90d": coverage_increase_90d,
            "payment_issues": payment_issues,
            "adjuster_experience_years": adjuster_experience_years.round(1),
            "documentation_complete": documentation_complete,
            "repair_shop_preferred": repair_shop_preferred,
            "is_fraud": is_fraud,
        }
    )
    return df


def main() -> None:
    out_path = Path(__file__).with_name("insurance_claims.csv")
    df = generate()
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path}")
    print(f"  {len(df):,} claims, fraud rate {df['is_fraud'].mean():.2%} "
          f"({df['is_fraud'].sum():,} fraudulent)")


if __name__ == "__main__":
    main()
