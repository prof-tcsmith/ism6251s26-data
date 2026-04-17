# Scenario 28: Financial Complaint Severity Classification

## Company Background

**RegWatch Financial Services** is a regulatory analytics unit within a federal consumer finance agency responsible for overseeing banks, credit unions, and non-bank financial companies. RegWatch processes over 400,000 consumer complaints per year across product categories including mortgages, credit cards, bank accounts, student loans, auto loans, and personal loans. The unit employs approximately 150 investigators and examiners who review complaints and take enforcement actions when warranted.

## Business Problem

Every consumer complaint that arrives at RegWatch must be triaged for severity and assigned to the appropriate investigation queue. Currently, a team of 12 intake analysts manually reads each complaint narrative, reviews the accompanying metadata, and assigns a severity level: Low, Medium, High, or Critical. This manual process takes an average of 8 minutes per complaint and introduces significant inconsistency --- different analysts assign different severity levels to identical complaints approximately 25% of the time.

More concerning, the manual process is too slow for Critical complaints, which require action within 24 hours. In the past year, 47 Critical complaints sat in the general queue for over 72 hours before being identified, allowing ongoing consumer harm to continue unchecked. Conversely, approximately 15% of complaints flagged as High or Critical by analysts turn out to be routine issues that consumed senior investigator time unnecessarily.

RegWatch wants an automated severity classification model that combines the structured metadata of a complaint (product type, monetary loss, response times, complaint history) with the narrative text to assign a severity level. The model should surface Critical complaints immediately and accurately route other complaints to the appropriate queue.

## Prediction Problem

Predict the `severity` of a consumer financial complaint: **Low**, **Medium**, **High**, or **Critical**.

This is a **multi-class classification** problem (4 ordinal classes).

**Why it matters:** Correct severity classification ensures Critical complaints receive immediate attention, prevents ongoing consumer harm, and allocates investigator resources efficiently. Misclassification in either direction has serious consequences.

## Evaluation Criteria

**Primary metric:** Weighted F1 score, with additional emphasis on Critical-class recall.

**Business justification:** While overall weighted F1 captures balanced performance, the agency has a strong regulatory obligation to catch Critical complaints. A model that misses Critical complaints (low Critical recall) is unacceptable even if it performs well on the other classes. Report Critical recall separately.

**Secondary considerations:**
- Critical-class recall (must be above 80%)
- Confusion matrix focusing on off-by-more-than-one errors (e.g., Critical predicted as Low)
- Ordinal distance of misclassifications (predicting Medium when the truth is High is better than predicting Low)

## Features

| Feature | Description |
|---------|-------------|
| `product_type` | Financial product involved (encoded 0-5: mortgage, credit card, bank account, student loan, auto loan, personal loan) |
| `company_size` | Size of the financial institution (encoded 0-2: small, medium, large) |
| `prior_complaints_against_company` | Number of prior complaints filed against this company |
| `consumer_age_bracket` | Age group of the consumer (encoded 0-4: 18-25, 26-35, 36-50, 51-65, 65+) |
| `state_regulatory_strictness` | Strictness of the consumer's state's financial regulations (1-5) |
| `days_since_incident` | Days between the incident and the complaint filing |
| `monetary_loss_reported` | Dollar amount of reported financial loss |
| `company_response_time_days` | Days the company took to respond to the consumer |
| `previously_disputed` | Whether the consumer has previously disputed a company response (0 or 1) |
| `is_repeat_complaint` | Whether this is a repeat complaint about the same issue (0 or 1) |
| `submission_channel` | How the complaint was submitted (encoded 0-3: web, phone, mail, referral) |

## Text Field

`complaint_narrative` --- The consumer's written description of their complaint (40-100 words). Low-severity narratives describe minor billing errors and questions about policies. Medium-severity narratives mention unauthorized charges, unresolved disputes, and poor customer service. High-severity narratives describe significant financial harm, account freezes, identity theft, and debt collector harassment. Critical narratives reference discriminatory practices, elder abuse, systemic fraud, and regulatory violations (citing specific laws like FDCPA, TILA, ECOA, or UDAAP). The escalation of language from inconvenience to systemic harm is a strong text-based signal.

## Special Considerations and Challenges

1. **Class imbalance:** Critical complaints represent only ~10% of the data. The model must avoid being overwhelmed by the majority Low class. Consider class weighting, oversampling, or threshold adjustment.

2. **Ordinal structure:** Severity levels are ordered (Low < Medium < High < Critical). Predicting Low when the truth is Critical is far worse than predicting High when the truth is Critical. Consider whether ordinal regression or ordinal-aware loss functions improve performance.

3. **Text contains the strongest Critical-class signal:** The structured features distinguish Low from High reasonably well (monetary loss, response time), but the distinction between High and Critical depends heavily on the narrative text. Critical complaints mention specific regulations, vulnerable populations, and systemic patterns that are not captured in the structured data.

4. **Holdout drift:** The holdout set exhibits distributional drift in monetary losses (higher), company response times (slower), and prior complaint counts (more). This simulates a period of economic stress where complaints become more severe on average and companies are slower to respond.

5. **Deceptive cases (~5%):** Some complaints use language mismatched to their severity --- a Critical-sounding narrative filed about a Low-severity issue, or mild language describing what is actually a Critical situation. These reflect real-world variation in consumer writing ability.

## Error Impact

| Predicted | Actual | Impact |
|-----------|--------|--------|
| Low | Critical | **Most dangerous error.** Ongoing consumer harm continues undetected. Potential regulatory embarrassment if harm is later discovered. Estimated cost: $500K+ in enforcement actions and reputational damage. |
| Low | High | Significant financial harm to the consumer goes unaddressed for weeks. Consumer loses trust in the regulatory process. |
| Medium | Critical | Critical complaint enters the standard queue instead of the expedited queue. Delay of 48-72 hours in response. |
| High | Low | Senior investigator time wasted on a routine inquiry. Estimated cost: $500 in misallocated staff time per false escalation. |
| Critical | Low | Extreme over-escalation. Rare but wastes significant senior resources and creates alarm where none is warranted. |
| Adjacent errors (off by 1 level) | Moderate impact. Complaints still reach an appropriate queue within a reasonable timeframe. |

---

*Dataset contains 11 structured features plus 1 text column across train.csv (~2,000 rows), test.csv (~700 rows), and holdout.csv (~700 rows).*
