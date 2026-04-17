# Example Responses: A-Level vs C-Level

This document shows the same prompts answered at three quality levels. Use it to calibrate your own writing.

**The pattern:** C-level answers *describe what they did*. A-level answers *explain why they chose it, what they considered, what they traded off, and what they'd do differently.*

---

## Example 1: Part 1.2 — Cost Analysis

**Prompt:** *"Analyze the asymmetry between false positives and false negatives. How should it influence your choice of evaluation metric?"*

### ❌ C-Level Response
> The FN cost is $25,000 and the FP cost is $500. FN is more expensive, so I will use F1 score since it balances precision and recall.

*(Two sentences, no reasoning, wrong conclusion — F1 weights precision and recall equally, which contradicts the asymmetric cost structure the student just identified.)*

### ⚠ B-Level Response
> The FN:FP ratio is 50:1, meaning each missed readmission costs 50 false alarms. This asymmetry means I should not use accuracy (which weights errors equally) or F1 (which weights precision and recall equally). Instead I'll use Average Precision because it captures the precision-recall tradeoff across thresholds, which is what I care about in an imbalanced cost setting.

*(Identifies the problem and picks an appropriate metric, but doesn't explain why AP specifically beats alternatives like F2 or cost-weighted scores.)*

### ✓ A-Level Response
> The FN:FP ratio is 50:1, meaning each missed readmission costs the bank what 50 false flags would cost. This rules out accuracy (ignores the asymmetry entirely) and F1 (assumes symmetric weighting of precision and recall). Three candidates fit the asymmetry: F2 score (which weights recall twice as heavily as precision), a custom cost-weighted objective, and Average Precision.
>
> I chose **Average Precision as my primary model-ranking metric** because it measures the quality of the probability ranking across all thresholds — and I know I'll be choosing my threshold based on cost, not on 0.5. A model with higher AP gives me better material to optimize. I'll separately optimize my classification threshold using **total business cost** (`FP × $500 + FN × $25,000`) because that's the number the CMO actually cares about.
>
> I considered F2 but rejected it because it fixes the precision-recall weighting at a specific ratio, and my actual weighting (50:1 in cost terms) is more extreme than F2's 2:1. I considered a fully custom cost-weighted CV objective, but AP is well-understood by downstream consumers of my work, so I'm using AP + explicit cost-based threshold selection as a clearer two-step approach.

*(Identifies the problem, considers multiple candidates, explains the choice, and articulates a two-step pipeline with a reason for separating ranking from thresholding.)*

---

## Example 2: Part 4.2 — Final Model Selection

**Prompt:** *"Defend your final model choice in depth. Why this model over the runner-up?"*

### ❌ C-Level Response
> XGBoost had the highest AP (0.42) so I chose it. The confusion matrix at threshold 0.22 has 145 true positives, 30 false negatives, 89 false positives.

*(Reports numbers without interpretation. Never mentions the runner-up, doesn't justify the threshold, offers no trade-off analysis.)*

### ⚠ B-Level Response
> My top three models (tuned Gradient Boosting, LightGBM, XGBoost) all scored within 0.005 AP of each other on cross-validation. I chose Gradient Boosting because it was marginally best and is the simplest to deploy in production. The runner-up, LightGBM, was very close — a different user might reasonably pick it.

*(Acknowledges ties and names runner-up, but doesn't quantify "simplest to deploy" or explain who would reasonably pick LightGBM and why.)*

### ✓ A-Level Response
> See the full defense in the exemplar — it covers:
> - Quantified comparison showing differences are smaller than CV standard deviation
> - Four specific reasons for choosing GB over LightGBM (statistical tie, capacity constraint fit, deployment simplicity, operational risk)
> - Dollar quantification of the trade-off ($2,500/month given up for lower risk)
> - Explicit counter-case: who would reasonably choose LightGBM instead (a CMO optimizing for CMS penalties)
> - Alternative recommendation to present both models to leadership for final call
> - Self-acknowledged limitation that the ensemble requirement wasn't shown in the writeup

*(This is what "defend in depth" means — identify the real decision, the real trade-offs, and the reasonable disagreements.)*

---

## Example 3: Part 5.1 — Algorithm Suitability

**Prompt:** *"For each model type you tried, explain in 2-3 sentences why it was or wasn't well-suited to this problem."*

### ❌ C-Level Response
> **Logistic Regression:** It's a linear model. The data was non-linear so it didn't work well.
> **Random Forest:** It's an ensemble of decision trees. It worked okay.
> **XGBoost:** It's the best model for tabular data. It worked best.

*(Meaningless. "Non-linear data" is a vague claim; "worked okay" is not an explanation; "best for tabular data" is a slogan, not reasoning.)*

### ✓ A-Level Response
> **Logistic Regression:** Underperformed here because several key features have U-shaped relationships with readmission (length of stay, age × diagnosis count). LogReg can represent those only through hand-engineered polynomial or bucketed features, which I tried; it closed some of the gap but never matched tree models. A LogReg with truly exhaustive feature engineering might tie boosting, but at that point I've built the trees by hand.
>
> **Random Forest:** Handled the interactions well because each tree samples features independently, letting different trees learn different interactions. Its main limitation here is that it treats each tree as independent and doesn't explicitly target the residuals of previous trees — in a dataset where multiple interactions matter simultaneously, boosting's sequential error correction seems to help slightly more.
>
> **Gradient Boosting / XGBoost / LightGBM:** Essentially tied in performance, as I'd expect on 3,000 rows. The "XGBoost dominates" narrative is mostly a competition-data phenomenon where tiny improvements compound over many rounds; at this scale the engineering differences between libraries don't translate to meaningfully different accuracy. Sklearn's GB was my choice for deployment reasons (see 4.2).
>
> **Stacking:** Did not improve over my best individual model. I believe this is because my base learners (GB, RF, XGB) all see the same tabular feature space through similar tree-based logic — they're not genuinely diverse in what they capture. Adding LogReg as a fourth base didn't help because LogReg's errors are correlated with tree errors on the hardest cases (the U-shaped interactions). Stacking would probably help more if one base learner were fundamentally different — e.g., a small neural network or a rule-based system.

*(Each model gets a mechanistic explanation connecting its properties to the specific problem. The reasoning would come across as genuine in a video presentation because it engages with actual algorithm mechanics.)*

---

## Example 4: Part 5.3 — "What if FN cost were 10× higher?"

### ❌ C-Level Response
> If FN cost were higher I would adjust the threshold to be lower to catch more positives.

*(True but trivial. Doesn't quantify the change, doesn't identify second-order consequences.)*

### ✓ A-Level Response
> The ratio would shift from 50:1 to 500:1 — comparable to extreme fraud detection. My current threshold (0.22) would push much lower, maybe 0.08, flagging substantially more patients. But then the capacity constraint becomes binding in a new way: the model's cost-optimal output would exceed the care coordination team's 300/month capacity, meaning the true constraint is no longer "find the cost-minimizing threshold" but "allocate 300 interventions across the highest-risk patients."
>
> Two second-order changes I'd make: (1) switch primary metric to a more recall-weighted score like F2 or a custom cost-weighted objective, and (2) recommend to leadership that the care coordination team expand, because at 500:1 asymmetry, the cost of capacity limits exceeds the cost of additional staff. In other words, if FN cost were 10× higher, the most valuable thing I could do isn't a better model — it's an organizational change.

*(Works through the first-order effect and then two distinct second-order consequences. The final sentence reframes the problem, which is what senior-level analysis looks like.)*

---

## Writing Guidelines Summary

| If your answer is... | ...it is probably: |
|---|---|
| 1–3 sentences describing what you did | C-level or below |
| A paragraph describing what you did and naming one trade-off | B-level |
| Multiple paragraphs engaging with alternatives, quantifying trade-offs, and acknowledging what a reasonable peer might choose differently | A-level |

### The "Could You Defend This On Camera?" Test

When writing Part 5, imagine the instructor stopping you mid-sentence and asking *"why?"*. If you can answer with specifics — names, numbers, explicit alternatives considered — you're A-level. If you'd have to stall or generalize, you're below A.

### Common Phrases That Signal AI-Generated Text

These phrases appear in common AI-assistant responses far more often than in student writing. Using them does not automatically mean you used AI, but reviewers find them a reliable red flag in context:

- "It is important to note that..."
- "In this section, we will..."
- "By leveraging..."
- "This highlights the importance of..."
- "In conclusion..."
- "Notably..."
- "Crucially..."
- "A holistic approach..."
- Repeated three-item parallel lists ("rigor, clarity, and precision")

**Write like yourself.** Part 5 is graded on your voice, not a polished voice. A slightly clumsy sentence that shows genuine engagement will score higher than a fluent sentence that shows rehearsed patterns.
