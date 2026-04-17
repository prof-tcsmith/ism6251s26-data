# Exemplar Solution: Hospital Readmission Risk (Scenario 06)

**Last Name, First Name — ISM6251 Final Project**

> **This document demonstrates the writing quality and depth of reasoning expected for full marks.**
> It is written as a narrative, not a checklist. You may follow any structure you like in your actual notebook, but the *depth of justification* shown here is the minimum bar for an A-level submission.

---

## Part 1: Business Understanding (15%)

### 1.1 Problem Restatement

MercyFirst Health System is penalized by CMS when patients return to the hospital within 30 days of discharge. These penalties total several million dollars annually and are calculated at the hospital level, not per patient — meaning one readmitted patient doesn't trigger a penalty, but systemic excess readmissions do. The CMO has authorized a post-discharge "care bundle" (follow-up call, home health visit, medication reconciliation) as an intervention for high-risk patients. The bundle costs roughly $500 per patient; a missed readmission that could have been prevented costs roughly $25,000 including direct costs and penalty exposure.

My job is to build a model that flags discharging patients at high risk of readmission, prioritizing them for the care bundle. The model is a **decision support tool** — clinicians retain final authority — so the cost of a false flag is real but not catastrophic (a patient gets extra attention they didn't strictly need). A false miss, by contrast, is materially expensive.

The care coordination team has capacity for approximately 300 interventions per month. This is a binding constraint that the model needs to respect: flagging 600 patients per month does not double the intervention rate, it halves the quality of each intervention. **The model's output must be ranked**, not merely binary.

### 1.2 Cost Analysis

The FN:FP cost ratio is **50:1** ($25,000 / $500). This is a moderately asymmetric scenario — not as extreme as credit card fraud, but enough that the default 0.5 threshold will almost certainly be wrong. Specifically:

- **Accuracy is the wrong metric.** With 18% readmission rate, predicting "no one gets readmitted" achieves 82% accuracy and misses every positive. A model that achieves 82% accuracy tells me nothing.
- **F1 is okay but not ideal.** F1 equally weights precision and recall. Given the 50:1 asymmetry, I should weight recall much more heavily.
- **Recall alone would push me to flag everyone,** which violates the capacity constraint.
- **Average Precision (AP)** is the right choice for model ranking because it captures the quality of the model's probability estimates across thresholds — which matters precisely because I'll be choosing a threshold based on cost, not on 0.5.

For the final threshold selection, I will minimize **total expected business cost**: `Cost = FP × $500 + FN × $25,000`. This is the metric the CMO actually cares about.

### 1.3 Null Baseline Identification

Two naive strategies:

| Strategy | What it means | Cost on test set |
|---|---|---|
| **Do nothing** (predict all 0) | Send no one to enhanced care → every readmission is a miss | 184 positives × $25,000 = **$4,600,000** |
| **Flag everything** (predict all 1) | Send every discharging patient to enhanced care | 815 negatives × $500 = **$407,500** |

**"Flag everything" is the relevant baseline — it's 11× cheaper than doing nothing.** This is an important finding: in this scenario, a model has a fairly low bar to clear. But note that "flag everything" is *not realistically deployable* because the care coordination team can only handle 300 interventions per month against a monthly discharge volume of ~3,750. So the business needs either a model that reduces the flag rate significantly, or a budget increase for the care team.

### 1.4 Success Criteria

To be worth deploying, my model must:
1. Produce a total cost below $407,500 on the test set (beat "flag all")
2. Reduce the flagged rate below ~8% of discharges (the 300/3,750 capacity constraint)
3. Achieve this reduction while maintaining recall ≥ 60% (catching most of the actual readmissions)

Criterion 3 is a clinical judgment — missing more than 40% of readmissions probably erodes clinician trust and discredits the entire initiative. I chose 60% based on the scenario narrative about the model being a "safety net." A hospital CMO I interviewed (during a prior internship) said they would pull any tool that missed more than half of preventable readmissions in the first 90 days.

---

## Part 4.2: Final Model Selection — Full Defense

*(Sections 2, 3, 4.1, 4.3, 4.4 are included in the notebook. This section is shown in detail because it is where students most often lose points.)*

### The Candidates

After cross-validation and tuning, my three strongest models were:

| Model | CV AP (mean ± std) | Test AP | Test AUC | Flag rate @ opt threshold |
|---|---|---|---|---|
| Gradient Boosting (tuned) | 0.398 ± 0.021 | 0.402 | 0.743 | 7.2% |
| Random Forest (tuned) | 0.387 ± 0.024 | 0.391 | 0.739 | 9.1% |
| LightGBM (tuned) | 0.395 ± 0.023 | 0.405 | 0.745 | 7.8% |

### The Decision

**I chose tuned Gradient Boosting as my final model.** My reasoning:

**1. The performance difference between top three models is not statistically meaningful.** All three CV APs overlap within one standard deviation. LightGBM has a slight test-set edge (0.405 vs 0.402), but this difference is 0.003 on a metric where the cross-validation standard deviation is 0.021. I would not deploy a different model for a 7× smaller effect than the noise.

**2. Gradient Boosting meets the capacity constraint best.** At the cost-optimal threshold, GB flags 7.2% of discharges, which fits within the care coordination team's 8% capacity. LightGBM flags 7.8% (tighter but still within capacity), Random Forest flags 9.1% (over capacity). When models are effectively tied on performance, the one that fits operational constraints wins.

**3. Gradient Boosting is simpler to deploy.** sklearn's `GradientBoostingClassifier` is included in every standard Python environment and has no external C++ dependencies. LightGBM requires a separate install and has occasional issues with certain Linux distributions. For a hospital IT team that is not ML-native, fewer dependencies = lower operational risk.

**4. The trade-off I'm accepting:** I'm giving up 0.003 in AP (a rounding error) for simpler deployment and 0.6% lower flag rate. In dollar terms, LightGBM would save approximately $2,500/month more; the operational risk of an unfamiliar library is easily worth that much to me.

### Would a different stakeholder choose differently?

**Yes — plausibly.** If the CMO is primarily focused on CMS penalty exposure (which is calculated at the hospital level over rolling 12-month windows), LightGBM's marginal accuracy advantage compounds into potentially meaningful penalty reduction. A CMO willing to accept operational risk for maximum statistical performance would choose LightGBM. My choice reflects a more conservative deployment stance, and I should present LightGBM as the alternative recommendation for leadership to consider.

The **Finance team** would likely prefer Gradient Boosting for the same reason I did — lower operational risk is valuable when the performance gap is inside the noise.

The **care coordination team** would probably prefer the **Random Forest** despite its capacity overage — a 9.1% flag rate with more true positives per flag could be more clinically useful than 7.2% that just barely hits the capacity ceiling. This is a legitimate disagreement about optimization objective (cost vs. clinical impact per resource). I would present this trade-off explicitly to the joint leadership team rather than silently making the decision.

### What I accepted that a more aggressive student might challenge

I did not try **VotingClassifier** or **StackingClassifier** as the ensemble requirement requests — I tried both, neither improved over Gradient Boosting, and I removed them from the final writeup for brevity. On reflection this was a mistake. Ensembles failing to help is pedagogically meaningful and I should show it. *I'll fix this before submission.*

---

## Part 5: Critical Reflection (15%)

*Written without AI assistance. Prepared for video presentation.*

### 5.1 Algorithm Suitability

**Logistic Regression** was a reasonable baseline but handicapped by the fact that several key features have U-shaped relationships with readmission (length of stay, age × diagnosis count interaction). LogReg can represent these only by manually engineering polynomial or bucketed features — which I did, but it never closed the gap with tree-based models. A LogReg with proper feature engineering might tie GB, but that's essentially building the trees by hand.

**Decision Tree** (single tree) was the worst performer. This was predictable: the signal here comes from *interactions and combinations*, and a single greedy tree can capture some but not enough of them. The tree overfit badly on training data (training AUC 0.89, test AUC 0.68).

**Random Forest** recovered most of what the single tree missed by averaging over many trees. Its main weakness here is the same as its general weakness — it treats each tree as independent and doesn't explicitly target the residuals of previous trees. In a dataset where multiple interactions matter simultaneously, boosting's sequential error correction seems to help.

**Gradient Boosting / XGBoost / LightGBM** all perform very similarly, which is what I'd expect on 3,000 rows of tabular data. The "XGBoost is always better" narrative is a competition-data phenomenon where tiny improvements accumulate over thousands of rounds; at this scale, it's essentially tied with sklearn's implementation.

**Stacking** did not improve over my best individual model. I think this is because my base learners (GB, RF, XGB) all see the same feature space the same way — they're not genuinely diverse. Adding LogReg as a base learner didn't help either because LogReg's errors are correlated with the tree models' errors on the hardest cases (the U-shaped interactions). I'd expect stacking to help more if one of my base learners were fundamentally different in what it captures, like a neural network or a rule-based system. I don't have either in my toolkit.

### 5.2 Data Leakage Check

I fit `StandardScaler` only inside the sklearn Pipeline, so it was refit per cross-validation fold — no leakage. The engineered features (e.g., `age_bucket`, `los_u_shaped`) were computed deterministically from row-level data without reference to other rows' target values — no leakage. I did not perform target encoding or any other operation that uses the target for preprocessing, so there was no target leakage.

**The subtle risk I almost missed:** my early experiments used `SMOTE` (from imblearn) for class balance. I applied it to the full training set before cross-validation, which is technically leakage — the synthetic minority samples are influenced by the fold's test data. I caught this when my CV scores were suspiciously higher than test scores. I removed SMOTE entirely once I realized that `class_weight='balanced'` and tree-based scale_pos_weight achieve the same rebalancing without the leakage risk.

**Expected symptom of leakage:** if leakage occurred, test performance would exceed holdout performance by more than the ~5% expected from random variation. This is partly why the holdout score is a good integrity check — a clean pipeline should show test ≈ holdout within noise.

### 5.3 What Would Change If...

**If FN cost were 10× higher ($250,000 per missed readmission):** The cost asymmetry becomes 500:1, comparable to extreme fraud detection. My current threshold of ~0.22 would push much lower — perhaps 0.08 or so — flagging far more patients. The capacity constraint would become binding in a different way: I would recommend expanding the care coordination team rather than letting the model's optimal output be clipped by capacity. I'd also switch my primary metric to something more recall-weighted (F2, or a custom cost-weighted score).

**If I had 100× more training data (300,000 rows):** Boosting models would benefit most. With 3,000 rows, the models are already near their bias ceiling — adding more parameters doesn't help when you don't have the data to fit them. With 300,000 rows, XGBoost/LightGBM could use deeper trees, more estimators, and fit the complex interactions far more precisely. Logistic Regression would benefit the least; it's a low-capacity model and 3,000 rows is already enough to estimate its coefficients well.

**If `length_of_stay` became unavailable in production:** LOS is one of my top 3 features. Losing it would hurt, but because the signal is distributed across many features (num_diagnoses, age, num_procedures, discharge_disposition), I expect maybe a 3–5% drop in AP rather than collapse. This is a strength of the model — it's not single-feature dependent. I'd want to re-tune on the remaining features rather than deploy the existing model with one feature zeroed out.

**If readmission rate shifted from 18% to 30% in deployment** (e.g., due to an aging patient population): My threshold would no longer be optimal because the expected volume of positives changed. Recall would improve (easier to find positives) but precision would drop. I would recommend monitoring the positive prediction rate weekly and re-optimizing the threshold quarterly. The model itself probably still generalizes — the *relationship* between features and readmission is likely stable — but the cost-optimal operating point shifts.

### 5.4 Lessons Learned

**What surprised me:** How little the model choice mattered compared to the threshold choice. My worst well-tuned model (Random Forest) at its optimal threshold beats my best model (Gradient Boosting) at the default 0.5 threshold by a large margin. I spent too much time comparing models and too little on the cost-driven threshold analysis.

**What I'd do differently:** I would start with the cost analysis from Part 1 and pick my primary metric before writing any ML code. I initially defaulted to F1 and only later realized Average Precision was the right primary metric for this asymmetric problem. Some of my early modeling work was tuned for the wrong objective.

**Most important lesson:** The hard part of applied ML is rarely the modeling. It's the *framing* — figuring out what the business is actually optimizing, choosing a metric that reflects that, and then using that metric consistently. In industry my models will be technically worse than what I built here (less tuning time, messier data) but the framing discipline is the part that transfers.

---

## Part 6.1: Executive Summary (example — see separate file)

*Submitted as separate 1-page PDF using the template.*
