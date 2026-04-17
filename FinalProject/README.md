# Final Project — ISM6251 Spring 2026

This folder contains all materials for the course final project.

## Which Guide Applies to You?

### Undergraduates

Read [`undergraduate-project-guide.md`](undergraduate-project-guide.md).

You will select **one of 20 binary classification scenarios** (scenarios 01–20). Individual project. Due Week 12 (May 8).

### Graduate Students

Read [`graduate-project-guide.md`](graduate-project-guide.md).

Your team will select **one of 10 multi-modal scenarios** (scenarios 21–30) involving text + structured data. Team project (3–4 students). Due Week 12 (May 8).

---

## Folder Structure

```
FinalProject/
├── undergraduate-project-guide.md    ← Undergrad spec
├── graduate-project-guide.md         ← Graduate spec
├── cases/
│   ├── 01-credit-card-fraud/          ← Scenario folder
│   │   ├── scenario.md                  Business context + cost structure
│   │   ├── train.csv                    Training data (with target)
│   │   ├── test.csv                     Test data (with target)
│   │   └── holdout_features.csv         Holdout features only — no target (for predictions)
│   ├── 02-employee-attrition/
│   ...
│   └── 30-movie-revenue/
└── templates/                         ← Reference materials for students
    ├── solution-exemplar.md             A-level writing example
    ├── solution-exemplar.ipynb          A-level notebook example
    ├── executive-summary-template.md    Format + example for 1-page summary
    ├── example-responses.md             C/B/A-level response calibration
    └── validate_submission.py           Pre-submission format validator
```

---

## Quick Timeline (Both Versions)

| Week | Undergrad | Graduate |
|------|-----------|----------|
| 9  | Scenario selected; cost-analysis peer session | Teams formed; roles assigned |
| 10 | "Show your worst model" peer session | Scenario selected; Part 1 team presentation |
| 11 | Draft Part 5 (no AI); record video presentation | Ablation intermediate results; peer feedback; individual Part 5 drafting + video recording |
| 12 | Submit final project + video presentation (May 8) | Submit team project + individual video presentations (May 8) |

---

*README — Version 1.0 — Spring 2026*
