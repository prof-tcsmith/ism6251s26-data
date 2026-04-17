# Scenario 19: Warranty Claim Legitimacy Prediction

## Company Background

**DuraHome Appliances** is a major home appliance manufacturer producing refrigerators, washing machines, dishwashers, ovens, and HVAC units. The company sells approximately 3 million units annually through retailers and direct channels, with a standard 2-year warranty on all products. DuraHome's warranty program processes about 180,000 claims per year, costing $95 million in parts, labor, and shipping.

## Business Problem

DuraHome estimates that approximately **12% of warranty claims are illegitimate** — ranging from outright fraud (filing claims for self-inflicted damage) to gray-area cases (products damaged by misuse, items past warranty dressed up as in-warranty, or exaggerated defect claims). These illegitimate claims cost the company an estimated $11 million annually.

Currently, DuraHome's claims processors review each claim manually, approving approximately 92% of claims within 48 hours. The remaining 8% are flagged for investigation based on simple rules (e.g., "claim amount > $500" or "more than 3 claims on same product"). This approach catches some fraud but is both too aggressive (flagging many legitimate high-value claims) and too lenient (missing sophisticated illegitimate claims).

DuraHome wants a model that can score each incoming warranty claim for legitimacy risk, allowing the claims team to:
- **Auto-approve** low-risk claims (faster customer experience)
- **Flag** high-risk claims for investigation (targeted fraud prevention)
- **Prioritize** investigations by risk score (most impactful cases first)

## Stakeholders

- **VP of Customer Service** — Primary concern is customer satisfaction. Denying or delaying a legitimate claim is a major source of negative reviews and customer loss. A wrongly denied claim can result in social media backlash with significant brand damage.
- **Director of Warranty Operations** — Manages a team of 25 claims processors. Wants to reduce processing time for legitimate claims while catching more fraud.
- **Chief Financial Officer** — Sees the $11M in illegitimate claims as a direct hit to margins. Wants to recover at least 40% of that ($4.4M) through better screening.
- **Legal Counsel** — Concerned about wrongful denial lawsuits. Denying a legitimate claim can result in consumer protection complaints, regulatory scrutiny, and litigation.

## Cost Structure

| Prediction | Reality | Outcome | Cost/Benefit |
|-----------|---------|---------|-------------|
| **Flag for investigation** (Predict 1) | **Illegitimate claim** (Actually 1) | True Positive | **Saves ~$600** (illegitimate claim denied after investigation) |
| **Flag for investigation** (Predict 1) | **Legitimate claim** (Actually 0) | False Positive | **-$150** (investigation cost + customer frustration + delayed service + reputation risk) |
| **Auto-approve** (Predict 0) | **Legitimate claim** (Actually 0) | True Negative | **+$50** (fast processing improves satisfaction, efficiency savings) |
| **Auto-approve** (Predict 0) | **Illegitimate claim** (Actually 1) | False Negative | **-$600** (fraudulent claim paid out: parts + labor + shipping) |

**Key asymmetry:** An undetected illegitimate claim ($600) costs **4x** a wrongly investigated legitimate claim ($150). However, the reputational cost of false positives is harder to quantify — a denied valid claim can cost a customer worth $2,000 in lifetime value.

## Target Variable

- `target = 1`: Warranty claim is illegitimate (fraudulent, misuse, or warranty-expired misrepresentation)
- `target = 0`: Warranty claim is legitimate (genuine product defect within warranty)

**Class balance:** Approximately 12% illegitimate claims.

## Features

| Feature | Description |
|---------|-------------|
| `product_age_months` | Age of the product at time of claim (months) |
| `warranty_remaining_months` | Months remaining on warranty when claim is filed |
| `claim_amount` | Dollar amount of the warranty claim ($) |
| `product_category` | Product type (encoded 0-5: refrigerator, washer, dishwasher, oven, HVAC, other) |
| `purchase_channel` | Where the product was purchased (encoded 0-3: big-box retailer, online, direct, other) |
| `num_previous_claims` | Number of previous warranty claims by this customer |
| `days_since_last_claim` | Days since the customer's most recent prior claim (999 if no prior claims) |
| `issue_description_length` | Length of the written issue description (character count) |
| `photo_submitted` | 1 = customer submitted photos of the defect, 0 = no photos |
| `receipt_provided` | 1 = customer provided proof of purchase, 0 = no receipt |
| `registered_product` | 1 = product was registered with DuraHome at purchase, 0 = not registered |
| `customer_account_age_months` | Age of the customer's DuraHome account (months) |
| `claim_filed_hour` | Hour of day the claim was submitted online (0-23) |
| `claim_filed_day_of_week` | Day of week claim was submitted (0 = Monday, 6 = Sunday) |
| `product_price_original` | Original retail price of the product ($) |
| `repair_type_requested` | Type of repair requested (encoded 0-3: in-home, ship-to, replacement, refund) |
| `distance_to_service_center` | Distance from customer to nearest authorized service center (miles) |
| `serial_number_verified` | 1 = serial number matches DuraHome records, 0 = could not verify |
| `customer_satisfaction_history` | Average satisfaction rating from previous interactions (0-10) |

## What Makes This Problem Interesting

1. **Near-Expiry Pattern:** Claims filed when the warranty has almost expired AND with high claim amounts are more suspicious — customers may be trying to get one last claim in before coverage ends. This is an interaction effect between warranty remaining and claim amount.

2. **Documentation as Signal:** Legitimate customers are more likely to have registered their product, kept their receipt, and taken photos of the defect. The absence of ALL these forms of documentation (no photo, no receipt, not registered) is a strong signal — but each alone is not conclusive.

3. **Repeat Claimers:** Multiple claims from the same customer, especially on young products, are suspicious. But a customer with a genuinely defective product line also files multiple claims. The interaction between claim frequency and product age matters.

4. **False Positive Sensitivity:** Unlike fraud detection in banking where customers rarely know they were flagged, warranty customers directly experience the investigation (delayed service, additional documentation requests). False positives create angry customers who write negative reviews and may never buy DuraHome again.

5. **Ethical Considerations:** The model must be careful not to discriminate based on features that correlate with demographics (e.g., `distance_to_service_center` or `customer_account_age_months` could correlate with socioeconomic status). A model that disproportionately flags certain customer groups faces legal and ethical risks.

## Evaluation Considerations

The claims team can investigate approximately 50 flagged claims per week. If the model flags more than that, the team will cherry-pick from the list based on their own judgment, reducing the model's value. Consider precision at the top of the ranked list: if you sort all claims by predicted fraud probability, are the top 50 genuinely the highest-risk claims? Also consider the dollar-weighted impact — catching a $600 fraudulent claim matters more than catching a $50 one.

---

*Dataset contains 19 features across train.csv (~3,000 rows), test.csv (~1,000 rows), and test.csv (~1,000 rows).*
