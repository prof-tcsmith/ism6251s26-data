# Scenario 15: Restaurant Health Code Violation Prediction

## Company Background

**Metro City Health Department** oversees food safety inspection for a large metropolitan area with approximately 12,000 active restaurants. The department employs 35 health inspectors who conduct both routine and complaint-driven inspections. Each inspector can complete approximately 3 full inspections per day, resulting in a department-wide capacity of roughly 400 inspections per month.

## Business Problem

Current inspection scheduling follows a simple rotation: restaurants are inspected roughly every 6-12 months, with higher-risk categories (e.g., full-service restaurants with liquor) inspected more frequently. This approach treats all restaurants equally, regardless of their actual risk profile. As a result, inspectors spend significant time at low-risk establishments (e.g., well-managed chain restaurants) while high-risk restaurants may go months without scrutiny.

A critical health code violation — such as improper food storage temperatures, pest infestation, or cross-contamination — can lead to foodborne illness outbreaks affecting dozens or hundreds of people. In 2024, Metro City experienced three significant outbreaks traced to restaurants, resulting in 180 confirmed illnesses, two hospitalizations, and over $3 million in combined medical costs, lawsuits, and business losses.

The Health Department wants a model to **prioritize inspections** — identifying restaurants most likely to have critical violations so inspectors can focus their limited time where it matters most.

## Stakeholders

- **Director of Environmental Health** — Wants to reduce foodborne illness outbreaks by 50% within two years. Needs to justify the data-driven approach to city council.
- **Lead Inspector** — Skeptical of "algorithm-based" scheduling. Wants to understand why certain restaurants are flagged and retain professional judgment.
- **City Attorney** — Concerned about liability if the model systematically under-inspects certain restaurant types or neighborhoods, creating the appearance of discrimination.
- **Restaurant Owners' Association** — Wants transparent, fair inspection criteria. Does not want restaurants penalized by "black box" algorithms.

## Cost Structure

| Prediction | Reality | Outcome | Cost/Benefit |
|-----------|---------|---------|-------------|
| **Priority inspection** (Predict 1) | **Critical violation found** (Actually 1) | True Positive | **Saves up to $50,000** (violation caught before outbreak) |
| **Priority inspection** (Predict 1) | **No violation** (Actually 0) | False Positive | **-$800** (inspector time wasted on low-risk restaurant) |
| **Routine schedule** (Predict 0) | **No violation** (Actually 0) | True Negative | **$0** (normal inspection rotation) |
| **Routine schedule** (Predict 0) | **Critical violation exists** (Actually 1) | False Negative | **-$50,000** (potential outbreak: medical costs, lawsuits, closure costs) |

**Key asymmetry:** Missing a critical violation ($50,000+ in potential harm) costs about **63x** an unnecessary priority inspection ($800). This strongly favors recall, but inspector capacity is genuinely limited — flagging too many restaurants creates an infeasible workload.

## Target Variable

- `target = 1`: Restaurant found to have a critical health code violation during inspection
- `target = 0`: Restaurant passes inspection (minor or no violations)

**Class balance:** Approximately 15% critical violation rate.

## Features

| Feature | Description |
|---------|-------------|
| `days_since_last_inspection` | Days since the restaurant's most recent inspection |
| `previous_violation_count` | Total number of violations (any severity) in inspection history |
| `previous_critical_violations` | Number of previous critical violations |
| `restaurant_type` | Type of establishment (encoded 0-7: fast food, full service, buffet, bakery, etc.) |
| `years_in_operation` | Years the restaurant has been operating at this location |
| `num_employees` | Number of employees |
| `seating_capacity` | Indoor seating capacity |
| `has_liquor_license` | 1 = serves alcohol, 0 = does not |
| `complaint_count_last_6months` | Number of public complaints in the past 6 months |
| `avg_health_score_history` | Average health inspection score across all past inspections (0-100) |
| `owner_change_last_year` | 1 = ownership changed in the past year, 0 = same owner |
| `renovation_last_year` | 1 = significant renovation in the past year, 0 = no renovation |
| `chain_restaurant` | 1 = part of a chain, 0 = independent |
| `neighborhood_income_level` | Median household income in the restaurant's census tract ($) |
| `inspection_month` | Month of inspection (1-12) |
| `food_handler_certifications_pct` | Percentage of staff with current food handler certifications |
| `cuisine_risk_category` | Cuisine type risk category (encoded 0-4, based on food handling complexity) |
| `delivery_service_partner` | 1 = partners with delivery services, 0 = does not |
| `outdoor_seating` | 1 = has outdoor seating, 0 = does not |
| `kitchen_size_sqft` | Kitchen area in square feet |

## What Makes This Problem Interesting

1. **Temporal Interactions:** A long gap since the last inspection is much more concerning when the restaurant has a history of critical violations. The two features interact strongly.

2. **Ownership Changes:** A change of ownership is one of the strongest predictors of violations, because new owners may not maintain the same food safety standards — but this signal is rare (only ~8% of restaurants).

3. **Seasonal Effects:** Foodborne illness risk increases in summer months (June-September) due to higher ambient temperatures and increased bacterial growth. The model should capture this without being given the pattern explicitly.

4. **Equity Concerns:** If the model systematically targets restaurants in lower-income neighborhoods or of certain cuisine types, it could face criticism for discriminatory enforcement. Consider whether `neighborhood_income_level` and `cuisine_risk_category` are appropriate features.

5. **Capacity Constraint:** The department can only do ~400 inspections per month. If your model flags 2,000 restaurants as high-risk, the prediction is useless — the team needs a ranked list, not just a binary flag. Probability calibration matters here.

## Evaluation Considerations

Precision-recall tradeoff is critical given the inspector capacity constraint. Consider: if you could only inspect the top 100 restaurants flagged by your model each month, how many actual violations would you catch? This "precision at K" framing is more operationally relevant than overall AUC.

---

*Dataset contains 20 features across train.csv (~3,000 rows), test.csv (~1,000 rows), and holdout.csv (~1,000 rows).*
