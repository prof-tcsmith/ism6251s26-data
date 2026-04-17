# ISM 6251 Course Data Repository

Public datasets and student-facing materials for **ISM 6251 — Machine Learning for Business Applications** (Spring 2026, graduate), taught by Dr. Tim Smith at the University of South Florida.

## Structure

| Folder | Course | Contents |
|--------|--------|----------|
| `W02/` | ISM 6251 | Week 2 — ML Foundations & Python: `sales_data.csv` |
| `W03/` | ISM 6251 | Week 3 — Data Preparation: CSV, JSON, and SQLite files for the Horizon Coffee Roasters scenario |
| `W05/` | ISM 6251 | Week 5 — Logistic Regression: customer-churn, employee-attrition, loan-default datasets |
| `W06/` | ISM 6251 | Week 6 — KNN: insurance-churn, trial-conversions datasets |
| `W09/` | ISM 6251 | Week 9 — Ensembles: `insurance_claims.csv` (Pinnacle fraud-detection assignment) + generator script |
| `FinalProject/` | **ISM 6251 Spring 2026** | Final Project — undergraduate and graduate project guides, 30 scenario folders (train/test splits + business context), and templates |

## Loading Data

All files are accessible directly via raw GitHub URLs. Example:

```python
import pandas as pd

url = "https://raw.githubusercontent.com/prof-tcsmith/ism6251s26-data/main/W03/sales_transactions.csv"
df = pd.read_csv(url)
```

## Final Project (ISM 6251 Spring 2026)

`FinalProject/` contains everything students need:

- `README.md` — overview and folder structure
- `undergraduate-project-guide.md` — spec for the team-based undergraduate project (scenarios 01–20)
- `graduate-project-guide.md` — spec for the team-based graduate multi-modal project (scenarios 21–30)
- `cases/NN-.../` — one folder per scenario containing `scenario.md` (business context + cost structure), `train.csv`, and `test.csv`
- `templates/` — executive-summary template and response-calibration examples

See [`FinalProject/README.md`](FinalProject/README.md) for full details.
