# ISM6251 Spring 2026 — Sample Datasets

Datasets used in lecture slides and notebooks for **ISM6251: Machine Learning for Business Applications** (Spring 2026).

## Structure

| Folder | Week | Contents |
|--------|------|----------|
| `W02/` | Week 2 — ML Foundations & Python | `sales_data.csv` |
| `W03/` | Week 3 — Data Preparation | CSV, JSON, and SQLite files for Horizon Coffee Roasters scenario |

## Usage

Load directly from a notebook or script:

```python
import pandas as pd

url = "https://raw.githubusercontent.com/prof-tcsmith/ism6251s26-data/main/W03/sales_transactions.csv"
df = pd.read_csv(url)
```
