# Scenario 21: Product Review Sentiment Rating Prediction

## Business Context

ShopSphere is one of the fastest-growing online marketplaces in North America, hosting over 200,000 third-party sellers and processing roughly 8 million product transactions per month. The platform spans consumer electronics, home goods, apparel, health and beauty, and a growing grocery vertical. Customer reviews are the lifeblood of the marketplace — they drive purchase decisions, influence search rankings, and serve as the primary feedback loop between buyers and sellers.

Over the past year, ShopSphere's Customer Experience team has noticed a troubling pattern: approximately 15% of customers who leave negative reviews (1-2 stars) had previously drafted partial reviews or engaged with the review prompt before ultimately submitting their feedback. The team hypothesizes that if they could predict a customer's likely rating *before* submission — using the draft review text combined with purchase metadata — they could proactively intervene with dissatisfied customers through targeted outreach, expedited resolutions, or service recovery offers.

The Director of Customer Experience, the VP of Marketplace Operations, and the Seller Success team are the primary stakeholders. The Director wants to reduce negative review volume by 20% through early intervention. The VP cares about overall marketplace health metrics and Net Promoter Score. The Seller Success team wants to identify systemic seller-level issues (e.g., a seller whose products consistently generate 1-2 star reviews despite positive delivery metrics, suggesting product quality problems).

Leadership has emphasized that this is fundamentally a *customer retention* initiative, not a review suppression tool. The model should identify genuinely dissatisfied customers who would benefit from proactive support — not attempt to influence or alter their feedback.

## The Problem

Predict the star rating (1-5) a customer will assign to a product based on their draft review text and purchase/product metadata. This is a **multi-class classification** problem with 5 ordered classes.

## Evaluation Criteria

The primary evaluation metric is **weighted F1 score**, which accounts for the class imbalance in ratings. However, the business particularly cares about:

- **Recall for 1-star and 2-star ratings:** Missing a dissatisfied customer (predicting 4-5 stars when the true rating is 1-2) means a lost intervention opportunity. These customers are most likely to churn.
- **Avoiding extreme misclassification:** Predicting 5 stars when the true rating is 1 star (or vice versa) is far worse than predicting 3 stars when the true rating is 2. The ordinal nature of ratings matters.
- **Precision for intervention triggers:** If the model triggers intervention for too many customers who are actually satisfied, the outreach team will be overwhelmed and the program loses credibility.

A secondary metric worth examining is **macro-averaged mean absolute error** across rating classes, which penalizes predictions that are far from the true rating more heavily.

## Data Description

| Feature | Type | Description |
|---------|------|-------------|
| `review_text` | text | Customer's draft product review (40-120 words) |
| `product_price` | float | Product price in dollars |
| `product_category` | int (0-7) | Encoded product category |
| `seller_rating` | float (1-5) | Seller's overall marketplace rating |
| `delivery_days` | int | Days from order to delivery |
| `product_age_months` | int | Months since product was first listed |
| `num_previous_reviews_by_user` | int | Number of prior reviews by this customer |
| `verified_purchase` | binary | Whether the purchase is verified (0/1) |
| `return_initiated` | binary | Whether a return was initiated (0/1) |
| `helpful_votes` | int | Helpful votes on the review draft (from preview) |
| `discount_pct` | float | Discount percentage applied at purchase |
| `product_weight_kg` | float | Product shipping weight in kilograms |
| `image_count` | int | Number of images attached to the review |
| **`rating`** | **int (1-5)** | **Target: star rating** |

## Text Field Details

The `review_text` column contains customer-written product reviews ranging from approximately 40 to 120 words. Reviews for higher ratings tend to use positive vocabulary (e.g., "amazing," "excellent," "recommend," "perfect"), while lower ratings use negative vocabulary (e.g., "terrible," "waste," "defective," "refund"). Three-star reviews often contain hedging language ("okay," "decent," "average," "mixed").

Importantly, approximately 10% of reviews are **"deceptive"** in that the text sentiment does not match the rating. For example, a customer may write positively about the product itself but assign a low rating due to delivery problems or seller issues captured in the structured features. Conversely, some forgiving customers write lukewarm text but still assign high ratings. This means **text alone is not sufficient** for accurate prediction — structured features provide complementary signal.

## Special Considerations

- **Ordinal target:** While treated as multi-class, the ratings have a natural order. A model that predicts 3 when the true value is 2 is less wrong than one that predicts 5. Consider whether ordinal approaches or standard multi-class classification work better.
- **Text-structure interaction:** Some low ratings stem from product quality issues (captured in text), while others stem from delivery or seller issues (captured in structured features like `delivery_days`, `return_initiated`, `seller_rating`). The best models should learn to combine both signals.
- **Class imbalance:** 1-star reviews are only 10% of the data. Consider stratified approaches or class weighting.
- **Deceptive reviews:** The ~10% of reviews where text and rating disagree create a ceiling on text-only model performance and reward models that integrate structured features.
- **Holdout drift:** The holdout period reflects a time with slightly slower delivery, lower seller ratings, and higher discount activity — simulating a post-holiday marketplace shift.

## Cost/Impact Table

| True Rating | Predicted Rating | Impact |
|-------------|-----------------|--------|
| 1-2 (dissatisfied) | 1-2 | Correct: customer flagged for proactive outreach, potential save |
| 1-2 (dissatisfied) | 4-5 | **Missed opportunity:** dissatisfied customer receives no intervention, likely churns |
| 4-5 (satisfied) | 1-2 | **False alarm:** outreach team contacts a happy customer unnecessarily, wastes resources |
| 4-5 (satisfied) | 4-5 | Correct: no action needed |
| 3 (neutral) | 1-2 | Minor false alarm: customer may appreciate proactive check-in regardless |
| 3 (neutral) | 4-5 | Acceptable: neutral customers are lower priority for intervention |
| 1 | 5 (or vice versa) | **Extreme misclassification:** suggests fundamental model failure, damages trust in system |
