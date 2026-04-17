# Scenario 26: Legal Case Outcome Prediction

## Company Background

**JurisAnalytics** is a legal technology firm headquartered in Washington, D.C., serving over 200 law firms and corporate legal departments across the United States. The company's platform aggregates case data from federal and state court filings, docket entries, and judicial records to help attorneys make data-driven decisions about litigation strategy. JurisAnalytics processes approximately 50,000 case records per year and maintains a historical database spanning fifteen years of litigation outcomes.

## Business Problem

Law firms spend an average of $150,000--$300,000 preparing a case for trial. Many of these cases ultimately settle, and a significant fraction result in outcomes that could have been predicted with better data analysis. JurisAnalytics has observed that experienced attorneys develop intuition about case outcomes based on patterns in case summaries, but this intuition is inconsistent across attorneys and difficult to scale.

JurisAnalytics wants to build a predictive model that combines structured case metadata (court level, case type, number of motions, evidence volume) with the textual content of case summaries to predict whether a case will result in a Plaintiff win, Defendant win, or Settlement. The goal is to provide early-stage guidance so that attorneys can advise clients on realistic expectations and allocate resources appropriately.

A key challenge is that the text of a case summary contains signals about case strength that are not fully captured by the structured features alone. For example, phrases like "clear breach of duty" or "undisputed facts" suggest a strong plaintiff position, while "insufficient evidence" or "statute of limitations" suggest the defendant is likely to prevail. Settlement language like "mutual agreement" or "mediation" indicates compromise. However, some cases have misleading summaries --- strong-sounding language that masks a weak factual position, or neutral language in cases that ultimately reach a clear verdict.

## Prediction Problem

Predict the `outcome` of a legal case: **Plaintiff_Wins**, **Defendant_Wins**, or **Settlement**.

This is a **multi-class classification** problem (3 classes).

**Why it matters:** Accurate outcome predictions help attorneys advise clients on whether to proceed to trial, pursue settlement, or abandon weak cases early. Misclassification wastes client resources and damages the firm's credibility.

## Evaluation Criteria

**Primary metric:** Macro-averaged F1 score (balances performance across all three classes).

**Business justification:** All three outcome types matter equally from a strategic standpoint. A model that is excellent at predicting settlements but poor at distinguishing plaintiff and defendant wins is not useful for litigation planning. Macro F1 ensures the model performs well across the board.

**Secondary considerations:**
- Per-class precision and recall (which class is the model weakest on?)
- Confusion matrix (are Plaintiff_Wins being confused with Defendant_Wins, or with Settlements?)

## Features

| Feature | Description |
|---------|-------------|
| `case_type` | Type of legal case (encoded 0-5: contract, tort, employment, intellectual property, real estate, regulatory) |
| `court_level` | Court where the case was filed (encoded 0-2: district, appellate, supreme) |
| `plaintiff_type` | Type of plaintiff (encoded 0-2: individual, small business, corporation) |
| `defendant_type` | Type of defendant (encoded 0-2: individual, small business, corporation) |
| `case_duration_months` | Length of the case from filing to resolution (months) |
| `num_motions_filed` | Total number of motions filed by all parties |
| `num_witnesses` | Number of witnesses listed in the case record |
| `evidence_volume_pages` | Total pages of evidence submitted |
| `prior_similar_cases_win_rate` | Historical win rate for the plaintiff in similar case types (0-1) |
| `judge_experience_years` | Years of experience of the presiding judge |
| `jurisdiction_region` | Geographic region of the court (encoded 0-3) |
| `monetary_amount_claimed` | Dollar amount claimed by the plaintiff |

## Text Field

`case_summary` --- A brief textual summary of the case (60-120 words). Contains legal language describing allegations, evidence, findings, and procedural status. The vocabulary and tone of the summary carry predictive signal: plaintiff-favorable summaries mention clear liability, breach of duty, and strong evidence; defendant-favorable summaries reference insufficient evidence, procedural defenses, and immunity; settlement-oriented summaries discuss compromise, negotiation, and mutual agreement.

## Special Considerations and Challenges

1. **Text-structured feature interaction:** The text summary and structured features both carry signal, but neither alone is sufficient. A case with high evidence volume and strong plaintiff language is highly likely to be a Plaintiff_Wins outcome, but either feature alone is less conclusive.

2. **Deceptive cases (~5%):** Some case summaries use language typical of one outcome class while the actual outcome is different. This reflects real-world scenarios where summary language does not always align with results.

3. **Class overlap in structured features:** Defendant_Wins and Settlement cases have similar distributions for some numeric features (e.g., number of motions), making the text signal essential for disambiguation.

4. **Holdout drift:** The holdout set exhibits distributional drift in case duration (longer cases), judge experience (less experienced judges), and monetary amounts claimed (higher claims). This simulates a scenario where JurisAnalytics expands to a new jurisdiction with different case characteristics.

## Error Impact

| Predicted | Actual | Impact |
|-----------|--------|--------|
| Plaintiff_Wins | Defendant_Wins | Attorney overestimates case strength; client invests heavily in a losing case. Potential $200K+ in wasted litigation costs. |
| Plaintiff_Wins | Settlement | Attorney fails to pursue early settlement; case drags on longer than necessary, increasing costs for both parties. |
| Defendant_Wins | Plaintiff_Wins | Attorney advises client to give up or settle cheaply; client misses a legitimate recovery opportunity. |
| Defendant_Wins | Settlement | Attorney pushes client to abandon the case; client misses a reasonable compromise. |
| Settlement | Plaintiff_Wins | Attorney pushes for settlement when a stronger outcome was achievable; client leaves money on the table. |
| Settlement | Defendant_Wins | Attorney wastes time in settlement negotiations when the case should have been dropped or the defense was clearly winning. |

---

*Dataset contains 12 structured features plus 1 text column across train.csv (~2,000 rows), test.csv (~700 rows), and holdout.csv (~700 rows).*
