# Scenario 11: Direct Mail Campaign Response Prediction

## Company Background

**HomeStyle Furnishings** is a national home goods retailer with 200+ stores and a thriving catalog/online business. The company has been in operation for over 30 years and maintains a customer database of approximately 2 million households. Their direct mail catalog remains a significant revenue driver, accounting for 25% of total sales.

## Business Problem

HomeStyle is preparing its Spring 2026 direct mail campaign. Printing and mailing a full-color catalog costs approximately $15 per household. With a limited marketing budget of $1.5 million for this campaign, they cannot mail to every customer. The marketing team needs a model to predict which customers are most likely to respond to the catalog mailing, so they can target their spend effectively.

Historically, the overall response rate for untargeted mailings is around **10%** — meaning 90% of catalogs are effectively wasted. The average responding customer places an order worth $320, yielding approximately $80 in gross margin.

## Stakeholders

- **VP of Marketing** — Owns the campaign budget and is accountable for marketing ROI. Wants to maximize total campaign profit, not just response rate.
- **Director of Customer Analytics** — Wants a model that is interpretable enough to explain to the marketing team why certain customers are targeted.
- **CFO** — Concerned about wasteful spending. Has questioned whether direct mail is still viable and wants data-driven justification.

## Cost Structure

| Prediction | Reality | Outcome | Cost/Benefit |
|-----------|---------|---------|-------------|
| **Send catalog** (Predict 1) | **Responds** (Actually 1) | True Positive | **+$65 net** ($80 margin - $15 mailing cost) |
| **Send catalog** (Predict 1) | **Doesn't respond** (Actually 0) | False Positive | **-$15** (wasted printing + postage) |
| **Don't send** (Predict 0) | **Doesn't respond** (Actually 0) | True Negative | **$0** (correct savings) |
| **Don't send** (Predict 0) | **Would have responded** (Actually 1) | False Negative | **-$80** (missed sale opportunity) |

**Key asymmetry:** Missing a potential responder ($80 lost opportunity) costs more than 5x a wasted mailing ($15). However, because non-responders vastly outnumber responders, the total FP cost can still dominate if the model is too liberal with predictions.

## Target Variable

- `target = 1`: Customer responds to the direct mail campaign (places an order within 60 days)
- `target = 0`: Customer does not respond

**Class balance:** Approximately 10% response rate.

## Features

| Feature | Description |
|---------|-------------|
| `recency_days_since_last_purchase` | Days since the customer's most recent purchase |
| `frequency_purchases_last_year` | Number of purchases in the last 12 months |
| `monetary_total_spend` | Total dollar amount spent historically |
| `avg_order_value` | Average order value (monetary / frequency) |
| `num_catalog_requests` | Number of times customer requested a catalog |
| `email_open_rate` | Proportion of marketing emails opened (0-1) |
| `website_visits_last_month` | Number of website visits in the past 30 days |
| `loyalty_program_member` | 1 = enrolled in loyalty program, 0 = not enrolled |
| `years_as_customer` | Years since first purchase |
| `age` | Customer age in years |
| `household_income_bracket` | Income bracket (0 = lowest, 4 = highest) |
| `home_ownership` | 0 = renter, 1 = homeowner, 2 = other |
| `num_children` | Number of children in household |
| `distance_to_store_miles` | Distance from customer to nearest store |
| `previous_campaign_responses` | Number of previous campaign responses |
| `category_preference` | Primary product category preference (encoded 0-5) |
| `seasonality_score` | Seasonal engagement index (0-1) |
| `credit_card_on_file` | 1 = has credit card on file, 0 = does not |
| `returned_items_last_year` | Number of items returned in the last year |

## What Makes This Problem Interesting

1. **RFM Framework:** Recency, Frequency, and Monetary value are classic direct marketing features. They interact with each other in non-obvious ways — a high-monetary customer who hasn't purchased recently may be different from one who purchases frequently but in small amounts.

2. **Diminishing Returns:** Previous campaign responses are highly predictive, but at some point, a customer who has responded to many campaigns may be near saturation.

3. **Cost-Sensitive Optimization:** The optimal classification threshold is NOT 0.5. Given the cost structure, you need to think carefully about where to set the cutoff — and this decision directly determines the campaign's profitability.

4. **Business Constraint:** The VP of Marketing doesn't just want predictions — she wants to know the expected ROI of the campaign given your model's performance. Can you estimate total campaign profit at different threshold settings?

## Evaluation Considerations

Think carefully about which metric matters most here. Accuracy is misleading when 90% of customers don't respond. Consider how precision and recall translate directly to dollars in this context: precision tells you what fraction of your mailings generate a response, while recall tells you what fraction of potential responders you're reaching.

---

*Dataset contains 19 features across train.csv (~3,000 rows), test.csv (~1,000 rows), and holdout.csv (~1,000 rows).*
