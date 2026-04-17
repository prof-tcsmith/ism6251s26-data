# Scenario 01: Credit Card Fraud Detection

## Business Context

CardShield Bank is one of the nation's largest retail banking institutions, processing over 50 million credit card transactions per day across its consumer and small business portfolios. In the past fiscal year, the bank absorbed $340 million in fraud losses, a figure that has been growing at roughly 12% year over year as criminal tactics become more sophisticated. The bank's existing rule-based fraud detection system catches many obvious cases but struggles with evolving fraud patterns, particularly those involving compromised card-not-present (online) transactions and geographically dispersed spending anomalies.

The bank's Chief Risk Officer has commissioned the development of a machine learning model to complement the existing rules engine. The model will score every incoming transaction in real time, and transactions flagged as high-risk will be temporarily blocked pending customer verification (typically a push notification or SMS confirmation). The goal is to significantly reduce fraud losses while keeping the false alarm rate low enough that legitimate customers are not repeatedly inconvenienced.

The fraud analytics team has assembled a historical dataset of transactions that were ultimately confirmed as either fraudulent or legitimate through the bank's investigation process. The dataset includes transaction-level features such as amount, timing, merchant characteristics, and behavioral velocity metrics. Because confirmed fraud is relatively rare (approximately 3% of investigated transactions), the dataset is heavily imbalanced, which presents a significant modeling challenge.

Leadership has emphasized that the cost structure is highly asymmetric. A missed fraud case (false negative) costs the bank an average of $5,000 in direct losses and chargeback fees, while a falsely blocked transaction (false positive) costs approximately $100 in call center handling and customer goodwill erosion. However, if the false positive rate becomes too high, customer attrition from the card product becomes a concern that is harder to quantify.

## Key Stakeholders

- **Chief Risk Officer (CRO):** Ultimately accountable for fraud losses; wants the lowest possible fraud miss rate without destroying customer experience.
- **Fraud Investigation Unit:** Reviews flagged transactions; capacity-constrained, so an overwhelming number of false positives degrades their ability to investigate real fraud.
- **Customer Experience Team:** Monitors complaint rates; concerned about legitimate customers being blocked during important purchases.
- **Finance/Compliance:** Tracks regulatory reporting metrics and overall loss ratios.

## Cost Structure

| Prediction | Actual | Outcome | Cost |
|---|---|---|---|
| Legitimate (0) | Legitimate (0) | True Negative | $0 |
| Fraudulent (1) | Fraudulent (1) | True Positive | $0 (fraud prevented) |
| Fraudulent (1) | Legitimate (0) | **False Positive** | **$100** (blocked transaction, call center, customer friction) |
| Legitimate (0) | Fraudulent (1) | **False Negative** | **$5,000** (fraud loss absorbed by bank) |

## Special Considerations

- The class imbalance is severe (~3% fraud). Standard accuracy is a misleading metric here.
- The FN/FP cost ratio is 200:1, meaning missing one fraud case is as costly as 200 false alarms. This should strongly influence threshold selection.
- The model must be evaluated on total expected cost, not just AUC or accuracy.
- Some features exhibit complex interaction effects (e.g., distance from home matters differently for online vs. in-person transactions).
- The velocity_score feature captures temporal transaction patterns and may be highly informative but also noisy.
- In production, the model would need to score transactions in under 100ms, so interpretability and computational cost matter (though this is not part of the graded evaluation).


---

*Note: FP cost updated: blocking a legitimate transaction involves lost sale revenue + call center time + customer frustration + potential card cancellation.*
