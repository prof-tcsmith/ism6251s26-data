# Scenario 07: Auto Insurance Claim Fraud Detection

## Business Context

SafeHarbor Insurance Group is a top-20 auto insurer in the United States, underwriting approximately 4 million policies and processing over 600,000 claims annually. The company's Special Investigations Unit (SIU) estimates that roughly 8% of all claims involve some degree of fraud, ranging from exaggerated injury claims to staged accidents to entirely fabricated events. Annual fraud losses are estimated at $180 million, representing a significant drag on the company's combined ratio and profitability.

The VP of Claims has commissioned a predictive model to score incoming claims for fraud likelihood at the point of first notice of loss (FNOL). Claims receiving high fraud scores will be routed to the SIU for detailed investigation before any payment is issued. The SIU investigation process -- which includes recorded statements, surveillance, independent medical examinations, and repair shop audits -- costs an average of $1,500 per investigated claim. Beyond the direct cost, investigating a legitimate claim introduces delays that damage the customer relationship; policyholders whose valid claims are flagged for investigation report 40% lower satisfaction scores and are 3x more likely to switch carriers at renewal.

The analytics team has compiled a dataset linking claim characteristics, policyholder attributes, and claim circumstances with the ultimate fraud determination. Claims were labeled as fraudulent based on SIU investigation findings, court outcomes, or claimant admission. The dataset includes behavioral signals (days to report, police report filing, witness availability) alongside financial indicators (claim amount, policy details, claimant financial stress). The financial_stress_score is a proprietary composite metric derived from credit bureau data that the company licenses for underwriting and claims purposes.

SafeHarbor's Chief Claims Officer has stressed that the model must be defensible in court: if a claim is denied based in part on model scores, the company needs to be able to articulate the factors that contributed to the flag. Pure black-box models are acceptable for screening purposes, but the team should also explore interpretable approaches.

## Key Stakeholders

- **VP of Claims:** Owns the claims process end-to-end; wants to reduce fraud payout while maintaining fast, fair processing for legitimate claims.
- **Special Investigations Unit (SIU):** Investigates flagged claims; has capacity for approximately 4,000 investigations per year and needs high-quality referrals.
- **Customer Retention:** Monitors the impact of investigations on customer satisfaction and renewal rates.
- **Legal/Compliance:** Ensures fraud investigations comply with state regulations; needs documentation of why specific claims were flagged.
- **Actuarial:** Uses fraud rate estimates for pricing; interested in whether the model reveals fraud pattern shifts that should inform rate filings.

## Cost Structure

| Prediction | Actual | Outcome | Cost |
|---|---|---|---|
| Legitimate (0) | Legitimate (0) | True Negative | $0 |
| Fraudulent (1) | Fraudulent (1) | True Positive | $1,500 (investigation cost, but saves ~$8,000 in fraudulent payout) |
| Fraudulent (1) | Legitimate (0) | **False Positive** | **$1,500** (SIU investigation of valid claim + customer relationship damage) |
| Legitimate (0) | Fraudulent (1) | **False Negative** | **$8,000** (fraudulent claim paid out) |

## Special Considerations

- The FN/FP cost ratio is approximately 5.3:1. Both types of errors are expensive, making this a scenario where threshold optimization is important but the optimal threshold is less extreme than in some other scenarios.
- Days to report interacts with claim type: a delay in reporting a collision is more suspicious than a delay in reporting a comprehensive claim (e.g., hail damage discovered later).
- Financial stress score interacts with claim amount: financially stressed claimants filing large claims are at elevated fraud risk, but financial stress alone is not a strong indicator.
- Prior fraud flags and prior claims have a multiplicative relationship: one prior fraud flag on a claimant with many claims is much more concerning than one flag on a first-time claimant.
- The absence of a police report is associated with higher fraud rates, counterintuitively -- fraudsters often avoid involving law enforcement.
- The is_weekend and is_holiday_adjacent features are relatively weak predictors (near-noise), testing whether students can identify features that do not meaningfully improve the model.
- The claimant_age feature has minimal predictive power in this dataset and serves as a red herring.
