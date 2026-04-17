# Scenario 04: Telecom Customer Churn Prediction

## Business Context

ConnectPlus Wireless is a regional telecommunications provider with approximately 2 million subscribers across the southeastern United States. The company offers mobile phone service, broadband internet, and streaming bundles through a mix of month-to-month, one-year, and two-year contracts. Over the past year, the company has experienced a quarterly churn rate of roughly 22%, with the vast majority of churn concentrated among month-to-month subscribers. The average customer lifetime value for a retained subscriber over the remaining potential contract period is estimated at $2,400.

The Chief Marketing Officer has initiated a proactive retention program that uses predictive analytics to identify subscribers likely to churn within the next 90 days. Customers flagged as high-risk receive targeted retention offers: discounted plan upgrades, loyalty credits, or free equipment upgrades. These retention interventions cost an average of $200 per customer. When offered to customers who were not actually going to churn, this represents pure margin loss -- money spent on someone who would have stayed anyway.

The analytics team has compiled a dataset combining billing records, service usage patterns, customer support interactions, and account demographics. The data captures the 90-day period leading up to either a churn event or a confirmed retention point. All categorical features have been numerically encoded. A notable feature is the strong correlation between total_charges and the combination of tenure and monthly charges, since total_charges is essentially their product.

ConnectPlus management has noted that the competitive landscape has shifted significantly: two major national carriers have recently launched aggressive pricing in the region, putting particular pressure on month-to-month subscribers and price-sensitive segments. The holdout evaluation period captures transactions from this more competitive environment, which may affect model generalization.

## Key Stakeholders

- **Chief Marketing Officer (CMO):** Owns the retention budget; needs to maximize the ROI of retention spending by targeting only genuine churn risks.
- **Customer Success Team:** Executes retention outreach; has capacity for approximately 400 interventions per month and needs prioritized lists.
- **Finance:** Monitors subscriber metrics and ARPU (average revenue per user); concerned about giving discounts to customers who would have stayed.
- **Network Operations:** Interested in understanding whether service quality (failures, data speeds) drives churn, as this informs infrastructure investment.

## Cost Structure

| Prediction | Actual | Outcome | Cost |
|---|---|---|---|
| Stays (0) | Stays (0) | True Negative | $0 |
| Churns (1) | Churns (1) | True Positive | $200 (retention offer; if successful, saves $2,400 in CLV) |
| Churns (1) | Stays (0) | **False Positive** | **$200** (retention offer wasted on non-churner) |
| Stays (0) | Churns (1) | **False Negative** | **$2,400** (customer lost, lifetime value forfeited) |

## Special Considerations

- The FN/FP cost ratio is 12:1. Missing a churner is much costlier than wasting a retention offer.
- Contract type is the single most predictive feature, but it interacts strongly with tenure: a month-to-month customer with 5+ years of tenure is actually quite loyal, while a new month-to-month customer is highly volatile.
- Monthly charges have a non-linear relationship with churn: very low charges indicate minimal service engagement (high churn risk from apathy), while very high charges signal price sensitivity (high churn risk from frustration). The sweet spot is in the middle.
- Support calls are a weak signal on their own but become a strong churn predictor when combined with service failures -- customers who call support AND experience outages are much more likely to leave than those who just call with billing questions.
- The is_senior feature is perfectly correlated with customer_age >= 65 by construction. One of these is redundant, which tests whether students handle multicollinearity.
- total_charges is largely a function of tenure_months x monthly_charges, introducing another source of multicollinearity.
