# Executive Summary Template

**Purpose:** 1-page summary for C-level executives with no ML background.
**Format:** Convert to PDF for submission.
**Hard limit:** 1 page. No jargon. No technical terminology. No code.

---

## Template Structure

```
[Scenario Title] — Model Deployment Recommendation
[Your Name], [Date]

BOTTOM LINE
[2-3 sentences. What should they do, expressed as a concrete action?]

BUSINESS IMPACT
[One table or two paragraphs, quantified in dollars.]
- Expected annual impact: $X
- Estimated payback period: X months
- Comparison to current approach: $Y worse/better per year

THE APPROACH IN PLAIN ENGLISH
[3-4 sentences. What does the model do? What information does it use?
Do NOT say "Random Forest" or "AUC" — say "a pattern-recognition algorithm
trained on past outcomes" or "the model gets 4 out of 5 decisions right."]

KEY RISKS
[Bullet list of 2-3 things that could go wrong and what would happen.
Focus on operational risks, not technical ones.]
- Risk 1: [e.g., patient mix changes → model accuracy drops by X%]
- Risk 2: [e.g., staff doesn't trust scores → intervention rate falls]
- Risk 3: [e.g., regulatory change → need to retrain]

RECOMMENDATION
[One of: Deploy | Pilot | Wait. Explain in 2-3 sentences why.]
```

---

## Exemplar: Hospital Readmission Risk (Scenario 06)

> *The following is a complete exemplar. Your own summary should match this
> in tone and length — readable by a hospital board chair in under 2 minutes.*

---

### Hospital Readmission Risk — Model Deployment Recommendation
**[Your Name], April 2026**

**BOTTOM LINE**
I recommend MercyFirst proceed with a **pilot deployment** of the readmission risk model at our flagship hospital for 90 days before system-wide rollout. The model is expected to reduce CMS penalty exposure by approximately $4.2M annually, but requires one-time operational changes to the care coordination workflow that deserve a controlled trial.

**BUSINESS IMPACT**

| Metric | Current State | With Model | Change |
|---|---|---|---|
| Annual CMS penalty exposure | $3.2M | $1.0M (est.) | −$2.2M |
| Avoidable readmissions/year | ~800 | ~400 (est.) | −400 |
| Care coordinator workload | Reactive, post-discharge | 300 targeted pre-discharge interventions/month | No headcount change needed |
| Net annual impact | — | — | **+$4.2M** |

**THE APPROACH IN PLAIN ENGLISH**
The model reviews each patient's clinical record at the time of discharge — things like length of stay, number of diagnoses, medication list, and lab values — and produces a risk score from 0 to 100. Patients scoring above 22 (about 7% of discharges) are flagged for the enhanced care bundle. The model was trained on 3,000 past discharge records with known outcomes, and it correctly identifies about 3 out of every 4 patients who will actually return. It is not perfect and will occasionally flag patients who would have been fine without intervention, but the extra attention does no harm.

**KEY RISKS**

- **Trust risk:** If clinicians ignore the model scores, the investment produces no benefit. We should pair the rollout with brief training explaining what the model sees (and what it doesn't — e.g., social determinants). The pilot will measure clinician adoption directly.
- **Drift risk:** Patient populations change as demographics and standards of care evolve. The model's accuracy will gradually degrade. We should retrain it every 6 months and monitor its performance monthly.
- **Capacity risk:** The care coordination team can handle 300 interventions per month. If the monthly discharge volume grows meaningfully, the model's output will need to be reprioritized or the team will need to expand.

**RECOMMENDATION**
**Pilot for 90 days** at our flagship hospital. During the pilot, measure: (1) actual readmission rate for flagged vs. unflagged patients, (2) clinician adoption rate, and (3) operational feedback from the care coordination team. If pilot results match projections within 25%, proceed to system-wide rollout in Q3. If results fall short, revisit the model rather than scale a disappointing result.

---

## What Makes a Good Executive Summary

### Do:
- **Lead with the action** — the CEO should know what you recommend before reading paragraph two
- **Quantify everything you claim** — "significant reduction" is meaningless; "$2.2M reduction in penalty exposure" is actionable
- **Acknowledge risks honestly** — executives trust recommendations that engage with what could go wrong
- **Match the vocabulary of the scenario** — a hospital scenario uses "readmissions," "discharge," "clinical"; a banking scenario uses "fraud losses," "investigation capacity," "customer experience"
- **Recommend pilot over full deployment** when uncertainty is high — pilots are rarely wrong; full deployments can be expensive wrong

### Don't:
- Mention algorithm names (Random Forest, XGBoost, LightGBM)
- Use metrics from ML vocabulary without translation (AUC, F1, precision)
- Report performance in decimals the executive doesn't know how to interpret (AP=0.402 means nothing; "correctly identifies 3 of 4 actual readmissions" does)
- Be so cautious that no recommendation emerges (executives hired you for a decision)
- Exceed one page. The 1-page limit is a feature, not a constraint. If it doesn't fit, it's not clear enough.
