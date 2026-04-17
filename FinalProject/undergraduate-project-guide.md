# Undergraduate Final Project Guide

## ISM6251 — Machine Learning for Business Applications
## Binary Classification Under Business Constraints (Scenarios 01–20)

**Due Date:** Week 12 (May 8 — Finals Week)
**Weight:** 30% of final grade
**Format:** Team project (3–4 students per team)

---

## What This Project Is

Your team will act as a data science consulting group hired by an organization facing a specific business problem that requires a binary classifier (yes/no, fraud/legitimate, churn/retain, etc.). Your team selects **one** of 20 provided scenarios, each with:

- A realistic business narrative describing the problem
- A specific cost structure for false positives and false negatives
- Stakeholder requirements that constrain your choices
- A training dataset and a test dataset

Your job is to build the best classifier for the business — not the best classifier by accuracy. Those are different things.

### Why a Specific Cost Structure Changes Everything

Every scenario gives you explicit dollar amounts: *what does a false positive cost this business? What does a false negative cost?* These numbers should drive every decision you make:

- **Which metric you use** (accuracy is almost never correct when costs are asymmetric)
- **What classification threshold you pick** (the default 0.5 is almost never optimal)
- **Which model you recommend deploying** (the highest-AUC model may not be the most cost-effective)

A team that picks XGBoost because "XGBoost is the best" has missed the point. A team that picks Logistic Regression with a carefully tuned threshold and explains why that decision minimizes total business cost has understood the point.

### What Makes This Project Hard (and Valuable)

- **No single correct answer.** Two teams working on the same scenario can arrive at different final models and both earn full marks if their reasoning is sound.
- **Scenarios are not equally difficult.** Some have clear signal and obvious answers; others have weak signal where even a well-tuned model barely beats the naive baseline. *Your grade is based on your process, not on your savings magnitude.*
- **The "no model" baseline is your true competition.** Before deploying ML, the business would either do nothing (ignore all risks) or flag everything (treat everyone as a risk). A model that doesn't clearly beat both of these naive strategies probably shouldn't be deployed.

---

## What You Are Given

For your chosen scenario, you will find these files in `cases/XX-scenario-name/`:

| File | Contents | How You Use It |
|------|---------|----------------|
| `scenario.md` | Business context, stakeholders, cost structure, special considerations | Read this first. It defines what "good" means for this scenario. |
| `train.csv` | ~3,000 rows with features + target | Model training, cross-validation, feature engineering. |
| `test.csv` | ~1,000 rows with features + target | Evaluate your tuned model's expected real-world performance. |

---

## Project Structure

### Part 1: Business Understanding (15%)

**Before writing any code.**

**1.1 Problem Restatement (in your own words)**
What is the business problem? Who are the stakeholders? What decision will your model inform — and what decision is the business currently making without a model?

**1.2 Cost Analysis**
Using the costs from `scenario.md`, compute the **FN:FP cost ratio**. Which error is more expensive? By how much? Then reason through:
- Which evaluation metric fits this cost structure? (accuracy, precision, recall, F1, F2, Average Precision, or something else — pick one and justify)
- Will the default 0.5 threshold be too aggressive or too conservative for this cost structure? (Don't just say "it depends" — predict the direction.)
- What model selection criterion flows from this?

**1.3 Null Baseline Identification**
Compute the cost of two naive strategies on the test set:
- **"Do nothing"** (predict all negative) — miss every positive. Cost = `n_positives × FN_cost`.
- **"Flag everything"** (predict all positive) — false alarm on every negative. Cost = `n_negatives × FP_cost`.

Which is cheaper? That's your **null baseline** — the bar your model must clear to be worth deploying. In some scenarios (extreme asymmetry + weak model), the smart null is actually very hard to beat.

**1.4 Success Criteria**
Define "good enough" in concrete terms:
- Minimum dollar savings that make deployment worthwhile
- Minimum recall/precision acceptable to the stakeholders described in `scenario.md`
- Maximum flag rate (consider operational capacity described in the scenario)

---

### Part 2: Data Exploration & Preparation (15%)

**2.1 Exploratory Analysis**
Class distribution, feature distributions, correlations, missing values, outliers. Show meaningful visualizations, not just `.describe()` output.

**2.2 Feature Engineering**
Did you create new features? Did you remove or transform any? Did you address multicollinearity? Every decision here should have a reason tied to the business problem.

**2.3 Preprocessing Decisions**
Which models require feature scaling? Which don't? How did this affect your pipeline design? *Critical:* did any preprocessing step (imputation, scaling, encoding) fit on data that included your test set? If so, that's data leakage — explain how you prevented it.

---

### Part 3: Model Development (25%)

**3.1 Baseline Model**
Start simple — Logistic Regression or a shallow Decision Tree. Report its performance. This is the floor; everything else must beat this.

**3.2 Model Exploration**
Train **at least four** model types. You must include:

| Requirement | Examples from the course |
|-------------|-------------------------|
| A linear model | Logistic Regression, Linear SVM |
| A tree-based model | Decision Tree, Random Forest, sklearn Gradient Boosting |
| A boosted model | XGBoost, LightGBM, sklearn GradientBoosting |
| An ensemble combination | VotingClassifier or StackingClassifier |

> **Note on ensembles at 3K-row scale:** VotingClassifier and StackingClassifier often fail to improve over your best individual model on small tabular datasets. **This is acceptable — and worth discussing.** A team that tries an ensemble, finds it doesn't help, and explains *why* (base learners too correlated, insufficient data diversity, etc.) demonstrates real understanding. A team that silently drops the ensemble because it didn't help loses points.

For each model: specify the hyperparameters you tuned and why, use 5-fold cross-validation (not just train/test), use early stopping for boosting, and report the metric you chose in Part 1.2.

**3.3 Hyperparameter Tuning**
For your top 2–3 models, conduct systematic tuning. Document:
- Which parameters and why *those* (not every parameter)
- Your search strategy (Grid, Random, or Random → Grid hybrid)
- Improvement over default configuration

**3.4 Threshold Optimization & Confusion Matrix Interpretation**
The default 0.5 threshold is rarely optimal. Using the cost structure from Part 1:
- Plot precision, recall, and **total business cost** across thresholds (0.01 to 0.99)
- Identify the threshold that minimizes total cost
- Show confusion matrices at both 0.5 and your optimized threshold
- Calculate the dollar impact of threshold optimization vs the default

**Confusion-matrix interpretation (required).** At your chosen threshold, produce a table that translates every cell of the confusion matrix into concrete business language. This is not "TP = correct positive"; it is "TP = a fraudulent transaction we caught before it settled — the customer is not charged, the issuer avoids chargeback, investigator time is spent." Fill in one row per cell:

| Cell | Count on test set | Who this is (in scenario terms) | What happens to them | Per-case cost / benefit ($) | Non-dollar consequence |
|------|------------------:|---------------------------------|----------------------|----------------------------:|------------------------|
| TP   | | | | | |
| FP   | | | | | |
| FN   | | | | | |
| TN   | | | | | |

The "Non-dollar consequence" column is required, not optional — it captures effects that the cost structure in `scenario.md` does *not* capture: customer friction, investigator workload, regulatory exposure, reputational harm, fairness concerns. A student who only fills the dollar column has half-completed the analysis.

---

### Part 4: Model Evaluation & Selection (20%)

**4.1 Model Comparison**
Cross-validation scores with confidence intervals (standard deviations). Are performance differences between your top models *statistically meaningful*, or within the noise? Present both a table and visualization.

**4.2 Final Model Selection — The Critical Defense**
Pick your final model. Then defend the choice:

- **Why this model over the runner-up?** Is the difference meaningful?
- **How does this model's behavior align with the business cost structure?**
- **What trade-offs did you accept?** (e.g., 2% lower recall for 15% higher precision)
- **Would a different stakeholder pick differently?** The CRO, the Operations VP, and the Finance team may disagree — explain what each would prefer and why.

This is where most students lose points. *Naming your best model is not defending it.*

**4.3 Feature Importance & Interpretability**
Which features drive predictions? Do they make business sense? Compare built-in (Gini) importance to permutation importance — do they agree? Could you explain a single specific prediction to a stakeholder?

**4.4 Error Analysis**
Examine the cases your model gets wrong. Are there patterns? Are certain customer segments harder to classify? What would improve these errors?

**4.5 Deployment Impact Assessment**
If this model were deployed tomorrow under your recommended threshold, what would actually change for the business? Answer in four explicit components — each is required. Numbers must be grounded in your test-set confusion matrix (Part 3.4) scaled to a realistic operating volume stated in `scenario.md` or estimated explicitly by you.

1. **Financial impact (annualized).**
   - Expected net savings vs the null baseline (dollars/year), with the arithmetic shown.
   - Expected cost of running the model itself where relevant (investigator hours, manual review labor, infrastructure) — subtract from savings.
   - Break-even sensitivity: how far off can the FN:FP cost ratio be before your recommendation flips? (One sentence with a number.)

2. **Operational impact.**
   - Daily or weekly volume of positive flags the model will produce.
   - Does this fit within the stakeholder capacity described in `scenario.md`? If it exceeds capacity, what do you recommend (raise threshold, triage by score, add staff)?
   - Any process change required: new queues, new SLAs, retraining cadence.

3. **Stakeholder impact.**
   - For each stakeholder group named in `scenario.md`, state in one sentence what changes for them — benefit *and* cost. "Customers" is not a stakeholder; "customers who are correctly not-flagged," "customers who are falsely flagged," and "customers who are missed and suffer harm" are three distinct groups.

4. **Ethical, regulatory, or reputational risk.**
   - Name at least one risk that the dollar cost structure does not capture: disparate impact across a subgroup, regulatory disclosure requirement, reputational exposure if a high-profile FN surfaces, data-use consent issues, etc.
   - What mitigation or monitoring would you recommend?

This section is what separates a student who built a model from a student who can recommend a deployment decision.

---

### Part 5: Critical Reflection (15%)

> **⚠ Part 5 must be written without AI assistance. The team presents it together in a single recorded video in Week 12.**
>
> **Video presentation:** The team records a single video using **Microsoft Teams** in which *every* team member presents a portion of the team's Part 5 answers in their own words. Talking-head plus a screen share of the notebook or write-up is fine. Target length is **~10 minutes total, with a hard cutoff at 11 minutes** — anything recorded past 11:00 will not be reviewed, so plan the division of speaking time in advance. Each member must demonstrate ownership of the portion they present (and be able to speak to the whole project). The video is pass/fail per student; failing (didn't speak, or what you presented doesn't demonstrate ownership) forfeits that student's Part 5 points. The team's Parts 1–4 and 6 are unaffected.

**5.1 Algorithm Suitability**
For each model type you tried, explain in 2–3 sentences why it was or wasn't well-suited to this specific problem. Connect your reasoning to algorithm mechanics: bias-variance tradeoff, decision boundary shape, feature interaction handling, scale sensitivity. "It performed well" is not an answer; "it worked well here because the decision boundary is non-linear and this algorithm can capture axis-aligned interactions without requiring manual feature engineering" is.

**5.2 Data Leakage Check**
Walk through your preprocessing pipeline step by step. For each transformation: was it fit on training data only? What's the specific risk if leakage occurred? What *would* a leakage symptom look like in your results?

**5.3 Counterfactual Questions**
For each of these (3–5 sentences):
- What if FN cost were 10× higher? How would your approach change?
- What if you had 100× more training data? Which model would benefit most and why?
- What if a key feature became unavailable in production? How robust is your model?
- What if the class balance shifted significantly after deployment? What would break?

**5.4 Team Reflection**
- How did your team divide the work? What worked? What would you do differently?
- What surprised you? What's the single most important thing you learned about model selection?
- Where did disagreements arise on methodology, and how did you resolve them?

*See `templates/example-responses.md` for calibration of what A-level vs C-level writing looks like.*

---

### Part 6: Stakeholder Communication (10%)

**6.1 Executive Summary (1 page, separate PDF)**
Use `templates/executive-summary-template.md`. Write for the non-technical stakeholders described in `scenario.md`. No jargon, no algorithm names, no raw metric numbers.

**6.2 Model Card**
Brief card documenting what the model does, what it doesn't do, performance on the test set, known limitations and failure modes, recommended monitoring approach.

---

## Deliverables

Submit as a team through the course portal by the deadline:

1. **`TeamName_FinalProject.ipynb`** — Your team's complete analysis notebook. Must run top-to-bottom without errors. Use `random_state=42` throughout for reproducibility.

2. **`TeamName_ExecSummary.pdf`** — 1-page executive summary

**Peer evaluation (submitted separately, by email):** Immediately after the final project submission deadline, the instructor will post an announcement requesting peer evaluations. **Each student must email the instructor a score out of 10 for every other team member.** A score of 10/10 means full contribution; score a teammate lower if you feel they did not contribute fairly. The purpose is to ensure every student participates — the default expectation is 10/10. Your individual grade on the team project is adjusted by a peer-evaluation factor computed from the average score your teammates give you (10/10 = no adjustment; lower scores scale your team grade down proportionally).

---

## Grading Rubric

| Component | Weight | What earns full marks |
|-----------|--------|----------------------|
| Business Understanding | 15% | Genuine engagement with cost structure; null baseline identified and reasoned about |
| Data Exploration & Prep | 15% | Every preprocessing decision justified; no data leakage; meaningful EDA |
| Model Development | 25% | 4+ model types including required ensemble; proper CV and tuning; threshold optimization tied to costs |
| Evaluation & Selection | 20% | Final model defended with trade-offs and runner-up discussion; confusion-matrix cells interpreted in business terms (per Part 3.4 table); deployment impact addressed across all four components — financial, operational, stakeholder, ethical/regulatory (Part 4.5) |
| Critical Reflection | 15% | Written in the team's own voice; per-student video presentation demonstrates ownership; counterfactuals show real algorithmic understanding |
| Stakeholder Communication | 10% | Executive summary readable by a non-technical reader in under 2 minutes; model card complete |

---

## Rules

1. **Part 5 is your team's own work.** AI-assisted answers will fail the individual video presentations. See Part 5 description.

2. **You may use AI assistance** for Parts 1–4, 6. Document significant AI interactions briefly in your notebook.

3. **Reproducibility:** Use `random_state=42` for every model, split, and CV operation. Your notebook must produce identical results when re-run.

4. **Team formation and scenario selection by the end of Week 9** — each team emails the instructor and the GA with its member list and chosen scenario. First-come, first-served on a per-section basis; no two teams in the same section may take the same scenario.

5. **Peer evaluations are mandatory.** You must email your per-teammate scores after the instructor's post-submission announcement. Failure to send peer scores → your own peer-evaluation factor is capped at 80%.

6. **Late submissions** lose 10% per day per the syllabus.

---

## Timeline

| Week | Milestone |
|------|-----------|
| 9  | Teams formed and scenario selected. Roles assigned within team. |
| 12 | Submit team project + team video presentation via the course portal. Due **May 8**. |

Use the time between Week 9 and the deadline to complete Parts 1–6, draft Part 5 (no AI), and record the team video presentation (MS Teams, ~10 min, 11 min hard cutoff; every member presents).

---

## Resources

All in the `templates/` folder:

| File | Purpose |
|------|---------|
| `executive-summary-template.md` | Format + exemplar executive summary |
| `example-responses.md` | C-level vs A-level response calibration for Part 5 |

The mechanics of training a classifier are the easy part; the reasoning that connects modeling choices to the business cost structure is what differentiates grades.

---

*Undergraduate Project Guide — Version 3.0 — Spring 2026*
