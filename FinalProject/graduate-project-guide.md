# Graduate Final Project Guide

## ISM6251 — Machine Learning for Business Applications
## Multi-Modal Modeling with Text + Structured Data (Scenarios 21–30)

**Due Date:** Week 12 (May 8 — Finals Week)
**Weight:** 30% of final grade
**Format:** Team project (3–4 students per team)

---

## What This Project Is

Your team will act as a data science consulting group hired to build a predictive system that integrates **text data with structured numeric features**. The target may be multi-class (categorical with 3+ levels), regression (continuous), or binary — depending on scenario.

Unlike the undergraduate version (binary classification on structured data only), graduate scenarios force you to confront the core challenges of multi-modal modeling:

- **How do you represent text as numeric features?** TF-IDF with what parameters? How many n-grams?
- **Do you reduce the text feature space?** TruncatedSVD or PCA on the TF-IDF matrix, with how many components?
- **How do you combine text features with structured features?** Concatenation? Stacked models? Weighted ensemble?
- **What's the right metric for your target type?** Weighted F1 for multi-class? RMSE for regression? Both?

These decisions compound. A team that tunes the classifier carefully but uses default TF-IDF parameters will likely underperform a team that tunes both the text representation and the model. The project is explicitly designed so that **representation choices matter as much as algorithm choices**.

### Why This Is Graduate-Level

The undergraduate project tests whether you can apply algorithms correctly under business constraints. The graduate project adds two dimensions:

1. **Representation design.** You're not just picking a model from sklearn — you're designing the pipeline that turns raw text into features a model can learn from. Two teams using the same model can achieve very different performance based on their TF-IDF and dimensionality-reduction choices.

2. **Ablation and justification.** You must demonstrate through experiments that your combined text+structured approach beats either modality alone. Teams that just concatenate everything and hope for the best will lose points even if their final number is good — the project requires you to *show* that combining modalities was the right call.

---

## What You Are Given

For your chosen scenario, you will find these files in `cases/XX-scenario-name/`:

| File | Contents | Usage |
|------|---------|-------|
| `scenario.md` | Business narrative, stakeholders, target description, evaluation metric | Read first. Defines what "good" means. |
| `train.csv` | ~2,000 rows with structured features + text column + target | Model training + CV |
| `test.csv` | ~700 rows with structured features + text column + target | Performance estimation |
| `holdout_features.csv` | ~700 rows with features + text, **no target column** | Prediction generation |

**What you do NOT receive:** the holdout labels. The instructor keeps them privately. Your submitted predictions on the holdout will be scored against the held-back labels. This simulates production deployment — your model must generalize to data it has never seen, including subtle distributional shifts on 2–3 features (realistic data drift).

---

## Scenario Summary

| # | Scenario | Target Type | Text Source | Primary Metric |
|---|----------|-------------|-------------|----------------|
| 21 | Product Review Sentiment | Multi-class (5 rating levels) | Customer reviews | Weighted F1 |
| 22 | Support Ticket Routing | Multi-class (6 departments) | Ticket descriptions | Weighted F1 |
| 23 | Job Posting Salary Prediction | Continuous (dollars) | Job descriptions | RMSE |
| 24 | News Article Categorization | Multi-class (8 topics) | Article text | Weighted F1 |
| 25 | Patient Triage Priority | Multi-class (4 urgency levels) | Chief complaint notes | Weighted F1 |
| 26 | Legal Case Outcome | Multi-class (3 outcomes) | Case summaries | Weighted F1 |
| 27 | Real Estate Price Estimation | Continuous (dollars) | Property descriptions | RMSE |
| 28 | Financial Complaint Severity | Multi-class (4 severity) | Complaint narratives | Weighted F1 |
| 29 | Research Grant Funding | **Binary** (`funded` 0/1) | Proposal abstracts | F1 at chosen threshold |
| 30 | Movie Revenue Prediction | Continuous ($ millions) | Plot summaries | RMSE |

**Note on scenario 29:** The dataset includes `award_amount` (continuous) for funded grants only, but **model the binary `funded` target**. `award_amount` may be used as a feature engineering source but not as a direct target.

---

## Project Structure

### Part 1: Business Understanding & Text Strategy (15%)

**1.1 Problem Restatement**
What is the business problem? Who are the stakeholders? What decision does your model inform? Is this multi-class, regression, or binary — and what are the implications of that?

**1.2 Metric Selection**
Based on the target type and the business context, which metric best captures the cost of being wrong?

- For multi-class scenarios: Weighted F1 vs Macro F1 vs per-class precision/recall — which fits the business problem? Are all classes equally important, or is misclassifying the critical class (e.g., Immediate triage) catastrophically worse than misclassifying between non-critical classes?
- For regression scenarios: RMSE vs MAE vs R² — which captures the business loss function? Is predicting $50K salary instead of $100K (50% off in log-scale) worse than predicting $200K instead of $250K (20% off in log-scale)? If so, consider MAPE or log-RMSE.

**1.3 Text Strategy Plan**
Before loading any data, outline your text processing strategy:
- Preprocessing: lowercasing, punctuation handling, stop words, stemming/lemmatization — what will you do and why?
- TF-IDF configuration: `max_features`, `ngram_range`, `min_df`, `max_df` — starting values and what you'll tune
- Dimensionality reduction: will you apply TruncatedSVD to the TF-IDF matrix? How will you decide on `n_components`?

**1.4 Feature Integration Strategy**
How will text and structured features combine?

- **Concatenation** — simplest: scale structured + optionally SVD-reduce TF-IDF, then stack column-wise
- **Stacked models** — train separate models on text-only and structured-only, combine their predictions as meta-features for a final model
- **Model-specific** — some models (tree-based) handle sparse TF-IDF directly; others (LogReg, SVM) work well with it; some (kNN) do not

Justify your starting approach. You'll revisit this after seeing ablation results.

---

### Part 2: Data Exploration & Preparation (15%)

**2.1 Structured Data EDA**
Standard exploration of numeric/categorical features, distributions, correlations, missing values.

**2.2 Text Data EDA**
- Vocabulary size before and after preprocessing
- Document length distribution (word count histogram)
- Most common terms overall
- **Most common terms by target class/level** — does the vocabulary differentiate classes visibly? This preview tells you how much signal TF-IDF will extract.
- Sample documents from different target categories

**2.3 Reproducible Pipeline**
Build a preprocessing pipeline that:
- Fits TF-IDF vectorizer on *training data only* (critical for no leakage)
- Applies TruncatedSVD only after TF-IDF
- Scales structured features with StandardScaler inside a Pipeline (refit per CV fold)
- Produces a combined feature matrix

Every parameter choice must have a reason. `max_features=3000` because — why? Not because the default was 3000; because the training vocabulary had 8,000 unique terms and you estimated the top 3,000 captured 95% of signal based on term frequency analysis.

---

### Part 3: Model Development (25%)

**3.1 Required Ablation Study**

You must compare three configurations for every model type you try:

| Configuration | What it uses |
|---------------|-------------|
| **Structured-only** | Scaled structured features, no text |
| **Text-only** | TF-IDF → (optional SVD), no structured features |
| **Combined** | Both, concatenated |

The ablation demonstrates whether combining modalities was the right call. Sometimes text alone dominates and structured is noise (low signal on structured features); sometimes structured dominates (short or uninformative text); sometimes combining is clearly better. Your project must show *which* situation you're in.

**3.2 Model Exploration**

Train at least four model types appropriate to your target:

**Multi-class:**
- Linear: Logistic Regression (multinomial) or Linear SVM
- Tree-based: Random Forest or Gradient Boosting
- Boosted: XGBoost or LightGBM
- Ensemble: VotingClassifier or StackingClassifier

**Regression:**
- Linear: Ridge, Lasso, or Linear Regression
- Tree-based: Random Forest Regressor
- Boosted: XGBoost Regressor or LightGBM Regressor
- Ensemble: VotingRegressor or StackingRegressor

**Binary (scenario 29):**
- Same four types as the undergraduate project, with text + structured features

For each: specify tuned hyperparameters and why those, use cross-validation, use early stopping for boosting models, report the metric from Part 1.2.

**3.3 Hyperparameter Tuning — Jointly on Representation and Model**

This is the graduate twist. Don't just tune the model's hyperparameters — tune the *text representation* alongside:

```python
pipeline_params = {
    # Text representation
    'tfidf__max_features': [1000, 2000, 5000],
    'tfidf__ngram_range': [(1,1), (1,2), (1,3)],
    'tfidf__min_df': [2, 5, 10],
    'svd__n_components': [50, 100, 200],
    # Model
    'model__learning_rate': [0.01, 0.05, 0.1],
    'model__max_depth': [3, 5, 7],
    # ... etc
}
```

Search this joint space with RandomizedSearchCV (GridSearch is combinatorially infeasible). Document which representation parameters ended up mattering most.

**3.4 Threshold/Output Calibration (binary + multi-class only)**

- **Binary (scenario 29):** Optimize threshold for business cost, same way as undergraduate project.
- **Multi-class:** Consider whether default decision rule (argmax of predicted probabilities) is optimal, or whether certain misclassifications matter more than others. In scenario 25 (triage), misclassifying Immediate → Urgent is far worse than misclassifying Urgent → Non-Urgent. A cost-sensitive decision rule may help.

---

### Part 4: Model Evaluation & Selection (20%)

**4.1 Ablation Analysis**

Present a clear comparison:

| Model | Structured only | Text only | Combined | Δ Combined vs best modality |
|-------|----------------|-----------|----------|----------------------------|
| LogReg | 0.512 | 0.687 | 0.721 | +0.034 |
| Random Forest | 0.489 | 0.631 | 0.668 | +0.037 |
| XGBoost | 0.534 | 0.698 | 0.739 | +0.041 |

Is the combined model *meaningfully* better than the best single modality? Small differences may fall within cross-validation noise. Include confidence intervals.

**4.2 Model Comparison (on combined feature matrix)**
Cross-validation scores with confidence intervals. Are differences statistically meaningful?

**4.3 Final Model Selection — Defense**
Select your final model and defend it:
- Why this model over the runner-up?
- Is your representation choice portable (would it hold on new data) or overfitted to quirks of your training set?
- What trade-offs did you accept?
- **What do the TF-IDF top features / SVD components tell you about what the text contributes?** This is a key graduate-level question — you should be able to interpret what the model learned from the text, not just that it learned something.

**4.4 Error Analysis**
Where does the model fail? Are certain classes harder (multi-class)? Are certain text lengths or structured feature combinations problematic? Can you characterize the failures?

---

### Part 5: Critical Reflection (15%)

> **⚠ Part 5 must be written without AI assistance. Each team member must also present the work in an individually-recorded video in Week 12.**
>
> **Video presentation:** Each team member records an individual 5–7 minute video walking through the team's Part 5 answers in their own words. Talking-head plus a screen share of your notebook or write-up is fine. Each member must demonstrate ownership of the team's reasoning — not every member needs to have written every section, but every member must be able to speak to the whole project. The video is pass/fail per student; failing (no submission, or a presentation that doesn't demonstrate ownership) forfeits your Part 5 points (the team's Parts 1–4 and 6 are unaffected).

**5.1 Text Representation Decisions**
- Why did TF-IDF with your chosen parameters work (or not) for this problem? What would bigram-only or trigram-only have missed?
- Would word embeddings (Word2Vec, sentence transformers) likely have helped here? Why or why not? What would be the cost of switching?
- What information is *lost* in the bag-of-words assumption? Did this cost you performance?

**5.2 Structured vs Text Feature Contribution**
- Which modality contributed more to predictive accuracy? Why do you think that is — is it about the information content of each modality, the way your model processes them, or something else?
- Were there cases where text captured information that structured features missed (or vice versa)? Give a specific example.

**5.3 Counterfactual Questions**
(3–5 sentences each)
- What if text field were unavailable in production? How much performance would you lose? Would the model still be worth deploying?
- What if you had 10× more training data? Which pipeline component would benefit most — text representation, structured preprocessing, model, or ensemble?
- What if the text were in a different language (or much noisier, or much shorter)? How would your pipeline need to change?
- What if the target distribution shifted meaningfully after deployment? Which part of your pipeline is most sensitive to distributional shift?

**5.4 Team Reflection**
- How did your team divide the work? What worked? What would you do differently?
- What's the most important thing your team learned about multi-modal modeling?
- Where did disagreements arise on methodology, and how did you resolve them?

---

### Part 6: Stakeholder Communication (10%)

**6.1 Executive Summary (1 page, separate PDF)**
Write for the non-technical stakeholders in `scenario.md`. No jargon, no algorithm names, no raw metric numbers. Use the template at `templates/executive-summary-template.md` — note that the example is binary-classification-themed but the structure applies to your scenario type.

**6.2 Model Card**
What the model does, what it doesn't do, performance metrics, known failure modes, recommended monitoring.

---

## Deliverables

Submit as a team through the course portal:

1. **`TeamName_FinalProject.ipynb`** — Your complete team notebook. Must run top-to-bottom. Use `random_state=42` throughout.

2. **`TeamName_holdout_predictions.csv`** — Predictions on the holdout features.
   - **Multi-class:** columns are `id` and `predicted_class` (the class label, not a probability); additionally include one column per class named `prob_<class>` for probability calibration scoring
   - **Regression:** columns are `id` and `predicted_value`
   - **Binary (scenario 29):** columns are `id` and `predicted_probability`
   - Before submitting, run `python templates/validate_submission.py YOUR_FILE XX` (where XX is your scenario number). The validator auto-detects the expected format from the scenario number.

3. **`TeamName_ExecSummary.pdf`** — 1-page executive summary

4. **`TeamName_PeerEvaluation.csv`** — Each team member submits individually, rating team member contributions (100% = full contribution, 90% = minor shortfall, 80% = significant shortfall). Individual grade = Team grade × Peer Evaluation Factor.

---

## How the Holdout Is Scored

The instructor will evaluate your holdout predictions using the metric specified in `scenario.md`:

- Multi-class scenarios (21, 22, 24, 25, 26, 28): **Weighted F1**
- Regression scenarios (23, 27, 30): **RMSE**
- Binary scenario (29): **F1 at your chosen threshold**

**Bonus/penalty:**
- Holdout metric within 5% of your reported test metric → no adjustment
- Holdout significantly worse than test → up to −5 points (overfitting or leakage)
- Holdout equal to or better than test → up to +3 bonus points (robust methodology)

---

## Grading Rubric

| Component | Weight | What earns full marks |
|-----------|--------|----------------------|
| Business Understanding & Text Strategy | 15% | Metric + text approach justified *before* modeling; clear ablation plan |
| Data Exploration & Prep | 15% | Reproducible pipeline; no leakage; informative text EDA (not just `.describe()`) |
| Model Development | 25% | Required ablation done thoroughly; joint hyperparameter tuning on representation + model |
| Evaluation & Selection | 20% | Final model defended including text-contribution interpretation; trade-offs acknowledged |
| Critical Reflection | 15% | Per-student video presentation demonstrates ownership of team reasoning |
| Stakeholder Communication | 10% | Exec summary readable in 2 minutes; model card clear |

---

## Rules

1. **Do not attempt to obtain the holdout labels.** You have `holdout_features.csv` only.

2. **Part 5 is your team's own work.** AI-assisted answers will fail the individual video presentations.

3. **You may use AI assistance** for Parts 1–4, 6. Document significant AI interactions briefly.

4. **Reproducibility:** `random_state=42` throughout. Notebook must run identically.

5. **Team formation by Week 10** via the course portal. Scenario selection by Week 11. First-come, first-served on scenario assignment — no two teams in the same section may take the same scenario.

6. **Peer evaluations are mandatory.** Failure to submit one → capped at 80% peer factor.

---

## Timeline & In-Class Support

| Week | Milestone |
|------|-----------|
| 9  | Teams formed. Roles assigned within team. |
| 10 | Scenario selected. In-class presentation of Part 1 (5 min per team). |
| 11 | Ablation study intermediate results shared — peer feedback session. Individual Part 5 drafting begins (no AI). Record individual video presentations. |
| 12 | Submit team project + individual video presentations via the course portal. Due May 8. |

---

## Resources

All in the `templates/` folder:

| File | Purpose |
|------|---------|
| `solution-exemplar.md` + `.ipynb` | Fully worked example (binary scenario). Structure and depth apply to graduate work. |
| `executive-summary-template.md` | Format + exemplar. Adapt the structure for your scenario type. |
| `example-responses.md` | C-level vs A-level response calibration for Part 5 |
| `validate_submission.py` | Automated check for your predictions CSV format |

Sample graduate solutions in `solutions/` (scenarios 21–30) show **technical mechanics** — TF-IDF + SVD + combined pipeline, ablation results, simple model comparison. The exemplar in `templates/` shows the **writing depth and reasoning quality** that earns A-level marks.

---

## A Note on Team Dynamics

Strong teams split work in ways that let each member own at least one substantive component:
- One member owns the text preprocessing / TF-IDF tuning
- One member owns the structured preprocessing / feature engineering
- One member owns the model exploration / tuning
- One member owns the evaluation / ablation / writing

Weak teams have one person doing modeling while the rest "help" vaguely. The per-student video presentation is designed to detect this — every team member must understand every part of the project well enough to speak to any section.

---

*Graduate Project Guide — Version 2.0 — Spring 2026*
