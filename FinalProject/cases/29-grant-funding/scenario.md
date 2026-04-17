# Scenario 29: Research Grant Funding Prediction

## Company Background

**FundScope Analytics** is a higher education analytics company based in Boston, Massachusetts, serving over 150 research universities and funding agencies across North America. The platform helps institutions understand their competitive position in the research funding landscape by analyzing proposal data, reviewer feedback patterns, and funding outcomes. FundScope's database contains records from approximately 80,000 proposals submitted over the past decade across all major federal and private funding agencies.

## Business Problem

Research universities invest significant internal resources in grant proposals that are never funded. Faculty spend an average of 170 hours preparing a major grant proposal, and the institutional cost of supporting each submission (administrative staff, compliance review, budget preparation, facilities documentation) averages $12,000. With typical funding rates of 15-35% depending on the agency and program, a substantial majority of this investment yields no return.

University research offices want to allocate their limited support resources strategically: provide more intensive proposal development assistance to submissions that are competitive but not yet strong enough, and redirect effort away from proposals with very low probability of success. However, current assessment methods rely on subjective faculty opinions and simple heuristics (e.g., "PI with an h-index above 20 is more likely to be funded").

FundScope wants to build a predictive model that combines structured PI and institutional data (publication record, prior funding history, institutional rank) with the text of proposal abstracts to predict two outcomes: (1) whether a proposal will be funded (binary), and (2) if funded, the expected award amount. The abstract text encodes important quality signals --- funded abstracts tend to describe novel, high-impact, interdisciplinary work with strong preliminary data, while unfunded abstracts often describe incremental work with unclear methodology.

## Prediction Problem

**Target (required):** `funded` --- Binary classification (0 = not funded, 1 = funded). Approximately 35% of proposals are funded.

> **Important:** A related variable, `award_amount` (the dollar value of the award, $0 for unfunded proposals), is a **post-outcome field** determined by the funding decision itself. It is therefore **not available at prediction time** and **not provided as a feature** in the data files. Do not attempt to recover or engineer it from any source — doing so is label leakage and would fail in deployment. Your task is strictly the binary `funded` prediction.

**Why it matters:** Accurate funding predictions help research offices prioritize support for competitive proposals and manage institutional expectations about research revenue.

## Evaluation Criteria

- **Primary metric:** F1 score (funded class) at your chosen threshold.
- **Business justification:** The university wants to identify proposals that will be funded. Precision matters (don't waste resources on proposals incorrectly predicted as funded) and recall matters (don't miss genuinely competitive proposals). F1 balances both.

**Secondary considerations:**
- AUC-ROC (how well does the model rank proposals by competitiveness?)
- Calibration of predicted probabilities (if the model says 60% chance of funding, are ~60% actually funded?)

## Features

| Feature | Description |
|---------|-------------|
| `pi_h_index` | H-index of the principal investigator |
| `pi_years_experience` | Years of research experience of the PI |
| `pi_num_publications` | Total number of publications by the PI |
| `institution_rank` | US News research ranking of the PI's institution (1-50, lower is better) |
| `institution_type` | Type of institution (encoded 0-2: R1 research university, R2 research university, teaching-focused) |
| `department_size` | Number of faculty in the PI's department |
| `num_co_investigators` | Number of co-investigators on the proposal |
| `budget_requested` | Total dollar amount requested in the proposal |
| `funding_agency` | Funding agency the proposal was submitted to (encoded 0-4) |
| `research_area` | Primary research area (encoded 0-7: CS/AI, genomics/biology, climate science, quantum computing, neuroscience, materials science, epidemiology/public health, energy) |
| `prior_grants_count` | Number of prior grants the PI has received |
| `prior_grant_total_funding` | Total dollar amount of the PI's prior grant funding |
| `is_resubmission` | Whether this is a resubmission of a previously declined proposal (0 or 1) |
| `review_panel_competitiveness` | Competitiveness score of the review panel (1-10, higher means more competition) |

## Text Field

`proposal_abstract` --- The research proposal abstract (80-150 words). Funded abstracts typically describe novel approaches, innovative methodologies, strong preliminary results, interdisciplinary collaboration, and transformative potential. They use confident, specific language about impact and rigor. Unfunded abstracts tend to describe incremental work using established methods, with vague methodology and limited scope. The abstract also contains research-area-specific terminology that correlates with the `research_area` feature but provides additional granularity about the specific subfield and approach.

## Special Considerations and Challenges

1. **PI credentials dominate but text adds signal:** The structured features (especially h-index, institution rank, prior grants) are the strongest predictors of funding. However, abstract quality provides incremental predictive power, particularly for borderline cases where PI credentials are average. The best model should benefit from combining both feature types.

2. **Two-target modeling:** Students choosing to model both targets face the challenge of a zero-inflated continuous variable (award_amount is $0 for ~65% of observations). A two-stage approach (predict funded first, then predict amount conditional on funded=1) may outperform a single regression model.

3. **Research area as a confounder:** Funding rates vary significantly across research areas, and the abstract text naturally varies by area. The model must distinguish between area-specific vocabulary (which is captured by the structured `research_area` feature) and quality-specific vocabulary (which provides incremental text signal).

4. **Holdout drift:** The holdout set simulates a shift toward a more competitive funding environment: higher budget requests, more competitive review panels, and proposals from lower-ranked institutions. This reflects a scenario where funding pools shrink relative to demand.

5. **Resubmission effect:** Resubmitted proposals have a higher funding rate than first submissions, reflecting the fact that PIs incorporate reviewer feedback. This feature interacts with text quality --- a resubmission with a still-weak abstract may not benefit from the resubmission boost.

## Error Impact

**For the binary model:**

| Predicted | Actual | Impact |
|-----------|--------|--------|
| Funded | Not Funded | University allocates startup funds, hires staff in anticipation of grant revenue that never materializes. Cost: $10K-$50K in premature commitments. |
| Not Funded | Funded | University fails to provide pre-award support to a competitive proposal; PI may feel unsupported and consider moving to another institution. Opportunity cost of lost retention. |

**For the amount model:**

| Error Type | Impact |
|-----------|--------|
| Overestimate by >50% | University overcommits resources based on inflated revenue projections. Budget shortfall when actual award is smaller. |
| Underestimate by >50% | University under-allocates space and support; PI cannot fully execute the funded project without additional institutional investment. |

---

*Dataset contains 14 structured features plus 1 text column and 2 target variables across train.csv (~2,000 rows), test.csv (~700 rows), and holdout.csv (~700 rows).*
