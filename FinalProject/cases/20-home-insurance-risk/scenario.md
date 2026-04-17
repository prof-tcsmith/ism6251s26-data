# Scenario 20: Home Insurance Risk Assessment

## Company Background

**HearthGuard Insurance** is a regional home insurance provider operating in eight southeastern US states. The company insures approximately 250,000 homes and writes $400 million in annual premiums. HearthGuard offers standard homeowner's policies (HO-3) covering fire, wind, theft, liability, and other perils. The company has a combined ratio of 103% — meaning it is currently paying out slightly more in claims and expenses than it collects in premiums.

## Business Problem

HearthGuard's actuarial team currently prices policies using a traditional rating model built on a small number of factors (property value, location, construction type, credit score). This model was adequate when the company was smaller, but as the portfolio has grown and climate-related risks have intensified, the model's predictions have become less accurate.

In 2025, HearthGuard paid out $62 million in claims on policies where the expected loss was far below the actual loss — these were homes the model rated as low-risk but that ended up filing significant claims (>$10,000). Conversely, the company lost an estimated $18 million in potential premium revenue from homeowners who were overpriced by the model and switched to competitors.

HearthGuard wants a more sophisticated risk model to:
- **Identify high-risk properties** that should be priced higher or declined
- **Identify over-priced low-risk properties** where premiums can be reduced to retain customers
- **Improve loss ratio** by better matching premiums to actual risk

## Stakeholders

- **Chief Actuary** — Responsible for pricing accuracy. Needs the model to produce well-calibrated risk probabilities, not just binary classifications. Regulatory filings require justification for pricing factors.
- **VP of Underwriting** — Makes accept/decline decisions on new applications. Currently accepts 88% of applications; wants to be more selective without losing profitable business.
- **Head of Retention** — Losing low-risk customers to competitors who price them more accurately. Wants to identify customers who are overcharged relative to their actual risk.
- **State Insurance Commissioner** — Requires that pricing models be transparent and not unfairly discriminatory. Features like credit score are permitted in most states but scrutinized.

## Cost Structure

| Prediction | Reality | Outcome | Cost/Benefit |
|-----------|---------|---------|-------------|
| **Price high / decline** (Predict 1) | **Files significant claim** (Actually 1) | True Positive | **Saves up to $25,000** (avoided underpriced risk) |
| **Price high / decline** (Predict 1) | **No significant claim** (Actually 0) | False Positive | **-$1,000** (overpriced customer shops elsewhere; lost premium revenue) |
| **Standard pricing** (Predict 0) | **No significant claim** (Actually 0) | True Negative | **+$1,600** (average annual premium collected, normal profit) |
| **Standard pricing** (Predict 0) | **Files significant claim** (Actually 1) | False Negative | **-$25,000** (underpriced policy; claim far exceeds collected premiums) |

**Key asymmetry:** An underpriced policy that results in a major claim ($25,000 net loss) costs **25x** an overpriced policy that loses a customer ($1,000). This strongly favors identifying high-risk properties, but losing too many low-risk customers destroys the portfolio's profitability.

## Target Variable

- `target = 1`: Policy results in a significant claim exceeding $10,000 during the policy year
- `target = 0`: No claim or minor claims only (below $10,000)

**Class balance:** Approximately 7% significant claim rate.

## Features

| Feature | Description |
|---------|-------------|
| `property_age_years` | Age of the home in years |
| `property_value` | Current assessed value of the property ($) |
| `square_footage` | Total living area (square feet) |
| `num_stories` | Number of stories (1, 2, or 3) |
| `roof_age_years` | Age of the current roof in years |
| `roof_material` | Roof material type (encoded 0-4: asphalt shingle, metal, tile, slate, other) |
| `heating_type` | Primary heating system (encoded 0-3: central gas, electric, heat pump, oil/wood) |
| `has_security_system` | 1 = monitored security system installed, 0 = none |
| `has_fire_alarm` | 1 = fire/smoke alarm system installed, 0 = none |
| `distance_to_fire_station_miles` | Distance to the nearest fire station (miles) |
| `distance_to_coast_miles` | Distance to the nearest coastline (miles) |
| `flood_zone_risk` | FEMA flood zone designation (0 = minimal, 4 = high risk) |
| `wildfire_risk_score` | Wildfire risk assessment score (0-10) |
| `crime_rate_index` | Local crime rate index (0-10) |
| `num_prior_claims` | Number of insurance claims filed in the past 5 years |
| `years_as_customer` | Years as a HearthGuard customer |
| `credit_score` | Insurance credit score (350-850) |
| `num_occupants` | Number of occupants in the home |
| `has_pool` | 1 = property has a swimming pool, 0 = no pool |
| `has_trampoline` | 1 = property has a trampoline, 0 = no trampoline |
| `dog_breed_risk` | Dog breed liability category (0 = no dog/low risk, 3 = high-risk breed) |
| `tree_coverage_pct` | Percentage of property covered by tree canopy |

## What Makes This Problem Interesting

1. **Geographic Risk Interactions:** Properties near the coast AND in a high flood zone are at compounded risk — the interaction is much stronger than either factor alone. A property 5 miles from the coast in flood zone 0 is very different from one 5 miles from the coast in flood zone 3.

2. **Property Age and Roof Age:** An old property with a new roof has been maintained and is relatively low risk. An old property with an old roof is a claim waiting to happen. The interaction between these two features is critical.

3. **Security as Risk Modifier:** Having a security system reduces the risk of theft-related claims, but only in areas with elevated crime rates. In low-crime areas, a security system doesn't meaningfully reduce risk. This is a classic interaction effect.

4. **Non-Linear Tree Coverage:** Moderate tree coverage provides shade and wind protection (reducing risk), but very high tree coverage (>70%) increases risk from falling branches and trees. The relationship is non-linear — an inverted U-shape for risk.

5. **Rare Event Challenge:** With only ~7% of policies resulting in significant claims, the model must handle class imbalance while maintaining calibrated probability estimates. Underwriting decisions are made on continuous risk scores, not binary accept/reject.

6. **Regulatory Constraints:** Insurance pricing models must be defensible to state regulators. Features like `credit_score` are legally permitted in most states but face increasing scrutiny. The model's use of such features should be documented and justified.

## Evaluation Considerations

For insurance risk models, calibration is as important as discrimination. AUC tells you whether the model can rank-order risks correctly, but the actuary needs to know: if the model says a property has 15% claim probability, do approximately 15% of such properties actually file claims? Consider reliability diagrams (calibration curves) alongside discrimination metrics. Also consider the business impact at various thresholds — what's the expected annual loss reduction if the model is used to adjust pricing for the riskiest 10% of the portfolio?

---

*Dataset contains 22 features across train.csv (~3,000 rows), test.csv (~1,000 rows), and holdout.csv (~1,000 rows).*
