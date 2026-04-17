# Scenario 03: Loan Default Prediction

## Business Context

Heritage Credit Union is a community-based lending institution serving approximately 120,000 members across a tri-state region. The credit union offers personal loans, auto loans, and small home improvement loans ranging from $1,000 to $100,000. Over the past three years, the institution's default rate has hovered around 12%, which is slightly above the industry average for credit unions and has drawn scrutiny from the board of directors and the NCUA (National Credit Union Administration).

The Chief Lending Officer has tasked the data analytics team with building a predictive model to assess default risk at the time of loan application. The model will not replace human underwriters but will serve as a decision-support tool: applications flagged as high-risk will receive additional manual review, and the model's risk score will inform the interest rate offered. The goal is to reduce default losses while maintaining the credit union's mission of serving its community, including borrowers who might be declined by larger banks.

The analytics team has assembled a dataset of historical loan outcomes, linking application-time features (credit score, income, debt-to-income ratio, employment history) with the ultimate outcome of each loan (fully repaid vs. defaulted). Loans that are currently active and in good standing are excluded; only completed loans are in the dataset. The average loss on a defaulted loan, after recovery efforts and collateral liquidation, is approximately $12,000. When the model incorrectly flags a good applicant as high-risk, the resulting loan denial costs the credit union roughly $800 in lost interest revenue over the life of the loan.

A critical nuance is that the credit union's board has expressed concern about fairness: the model should not systematically deny loans to members in underserved communities who could successfully repay. The team has been asked to evaluate the model's performance across different demographic segments, though the dataset does not include race or ethnicity directly.

## Key Stakeholders

- **Chief Lending Officer:** Owns the underwriting process; wants to reduce the default rate from 12% to under 8% without dramatically shrinking the loan portfolio.
- **Loan Underwriters:** Will use the model as a decision-support tool; need interpretable risk scores, not just binary predictions.
- **Board of Directors:** Focused on overall financial health and community mission; concerned about both losses and access to credit.
- **NCUA Examiners:** Regulatory oversight; interested in the soundness of lending practices and any use of automated decision-making.
- **Members/Borrowers:** Expect fair treatment and transparent lending criteria.

## Cost Structure

| Prediction | Actual | Outcome | Cost |
|---|---|---|---|
| Repays (0) | Repays (0) | True Negative | $0 (loan performs as expected) |
| Defaults (1) | Defaults (1) | True Positive | $0 (loan denied or priced appropriately, loss avoided) |
| Defaults (1) | Repays (0) | **False Positive** | **$800** (good applicant denied, lost interest revenue) |
| Repays (0) | Defaults (1) | **False Negative** | **$12,000** (loan defaults, net loss after recovery) |

## Special Considerations

- The FN/FP cost ratio is 15:1. Missing a default is far more costly than denying a good applicant, but access to credit is part of the institution's mission.
- Credit score has a strongly non-linear relationship with default: the risk increases dramatically below 600 and again below 550, but the marginal effect of going from 700 to 750 is small.
- Debt-to-income ratio interacts with income level: a high DTI is much more dangerous for low-income borrowers than for high-income borrowers.
- Loan purpose interacts with loan amount: large loans for certain purposes carry disproportionate risk.
- Several features are correlated (e.g., credit score and interest rate are inversely correlated; revolving utilization and DTI are correlated), which may affect certain model types.
- The months_since_last_delinquency feature is zero for borrowers with no delinquency history, creating a bimodal distribution that requires careful handling.
