# Scenario 13: Online Lending Credit Screening

## Company Background

**QuickFund Digital** is an online personal loan platform that has grown rapidly since its founding in 2019. The company offers unsecured personal loans ranging from $1,000 to $50,000 with terms of 12-60 months. Unlike traditional banks, QuickFund promises a credit decision within 15 minutes and funds deposited within 24 hours. This speed is a core competitive advantage — and it means the credit screening model must be fast, automated, and reliable.

QuickFund currently serves approximately 50,000 loan applications per month, approving about 40% of applicants. The average loan size is $8,500.

## Business Problem

QuickFund's current credit model was built two years ago using a simpler logistic regression. As the company has scaled, default rates have crept up from 12% to 18%, eroding profitability. The CEO has asked the data science team to build a more sophisticated model that better identifies applicants likely to default while preserving the company's approval rate (and thus revenue growth).

The tension is clear: **approve too many risky borrowers and losses mount; reject too many good borrowers and competitors capture the business.** A rejected applicant goes to a competitor within hours — there are no second chances.

## Stakeholders

- **Chief Credit Officer** — Accountable for portfolio loss rates. Wants default rate back below 15% without cutting approval volume by more than 10%.
- **VP of Growth** — Measured on loan origination volume. Argues that rejecting borderline applicants loses more revenue than the defaults cost.
- **Head of Risk Analytics** — Wants a model that is not only accurate but also fair and compliant with lending regulations (ECOA, Fair Lending).
- **Compliance Team** — Concerned about any features that could serve as proxies for protected characteristics (race, gender, age). The `zip_risk_score` feature, in particular, has raised fairness questions.

## Cost Structure

| Prediction | Reality | Outcome | Cost/Benefit |
|-----------|---------|---------|-------------|
| **Approve loan** (Predict 0) | **Repays successfully** (Actually 0) | True Negative | **+$1,200** (avg interest income over loan life) |
| **Approve loan** (Predict 0) | **Defaults** (Actually 1) | False Negative | **-$3,000** (avg net loss on defaulted loan after recovery) |
| **Reject applicant** (Predict 1) | **Would have defaulted** (Actually 1) | True Positive | **$0** (dodged a loss) |
| **Reject applicant** (Predict 1) | **Would have repaid** (Actually 0) | False Positive | **-$500** (lost revenue from good applicant who goes to competitor) |

**Key asymmetry:** A defaulted loan ($3,000 loss) costs **6x** a rejected good applicant ($500 lost revenue). This means the model should lean toward caution — but not so much that it kills the business by rejecting everyone.

## Target Variable

- `target = 1`: Applicant defaults on the loan (misses 3+ consecutive payments)
- `target = 0`: Applicant repays the loan successfully

**Class balance:** Approximately 18% default rate.

## Features

| Feature | Description |
|---------|-------------|
| `requested_loan_amount` | Loan amount requested by the applicant ($) |
| `annual_income` | Self-reported annual income ($) |
| `employment_length_months` | Length of current employment (months) |
| `credit_score` | Credit bureau score (300-850 range) |
| `num_open_accounts` | Number of open credit accounts |
| `total_debt` | Total outstanding debt ($) |
| `debt_to_income` | Debt-to-income ratio (total_debt / annual_income) |
| `num_derogatory_marks` | Number of derogatory marks on credit report |
| `months_since_last_derogatory` | Months since most recent derogatory mark (0 if none) |
| `home_ownership` | 0 = rent, 1 = mortgage, 2 = own outright |
| `purpose` | Stated loan purpose (encoded 0-5) |
| `application_hour` | Hour of day application was submitted (0-23) |
| `time_on_page_seconds` | Time spent on the application page (seconds) |
| `num_page_revisits` | Number of times applicant returned to the application |
| `device_type` | Device used for application (0 = desktop, 1 = mobile, 2 = tablet) |
| `previous_applications` | Number of previous loan applications with QuickFund |
| `referral_source` | How the applicant found QuickFund (encoded 0-4) |
| `verification_status` | Income verification status (0 = not verified, 1 = source verified, 2 = fully verified) |
| `zip_risk_score` | Risk score based on applicant's zip code (0-10 scale) |

## What Makes This Problem Interesting

1. **Credit Score Non-Linearity:** Credit scores below ~600 represent a fundamentally different risk profile than those above. The relationship is not linear — there may be a "cliff" where default probability jumps sharply.

2. **Behavioral Signals:** Application behavior features (time on page, page revisits) are weak predictors individually, but they capture something traditional credit features miss — how carefully the applicant is considering the loan.

3. **Interaction Effects:** Debt-to-income ratio means different things at different income levels. A DTI of 0.4 for someone earning $30,000/year is far more precarious than the same ratio for someone earning $150,000/year.

4. **Fairness Concerns:** The `zip_risk_score` is correlated with neighborhood demographics. Using it improves prediction accuracy but raises fair lending concerns. How you handle this feature — and whether you discuss the trade-off — matters.

5. **Business Trade-off:** The Chief Credit Officer and VP of Growth want different things. Your model and threshold choice implicitly sides with one or the other. A thoughtful analysis acknowledges this tension.

## Evaluation Considerations

In lending, the traditional metric is the KS statistic or Gini coefficient, but AUC and precision-recall curves are also informative. Think about what "good enough" means here: if the model reduces the default rate by 3 percentage points while maintaining 85%+ of current approval volume, is that worth deploying? Quantify the expected annual savings.

---

*Dataset contains 19 features across train.csv (~3,000 rows), test.csv (~1,000 rows), and test.csv (~1,000 rows).*
