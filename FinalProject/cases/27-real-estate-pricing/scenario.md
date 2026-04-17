# Scenario 27: Real Estate Price Estimation

## Company Background

**HomeWise Analytics** is a real estate data platform based in Austin, Texas, serving over 3,000 real estate agents, brokerages, and institutional investors across the southern United States. The platform provides market analytics, comparative market analyses (CMAs), and pricing tools. HomeWise processes approximately 120,000 property listings per year and maintains a historical dataset of over 1.5 million transactions.

## Business Problem

Accurate pricing is the single most important factor in determining how quickly a home sells and at what price. Overpriced homes sit on the market, accumulate stigma, and eventually sell below fair value. Underpriced homes leave money on the table for sellers and create legal liability for agents who failed to advise properly.

HomeWise currently uses a regression model built on structured property data (square footage, bedrooms, lot size, etc.) to estimate listing prices. While this model captures roughly 70% of price variation, it misses an important signal: the language agents use in listing descriptions. Experienced agents know that words like "stunning," "gourmet kitchen," and "panoramic views" signal luxury properties, while "cozy," "potential," and "as-is" signal budget properties. This vocabulary choice is not random --- it reflects the agent's professional assessment of the property's market position.

HomeWise wants to build an improved pricing model that combines structured property data with the text of listing descriptions. The hypothesis is that the agent's word choices encode soft information about property condition, appeal, and market positioning that is not fully captured by the numeric features. For example, two homes with identical square footage and bedroom counts may have very different prices if one is described as having "designer finishes" and the other as needing "cosmetic updates."

## Prediction Problem

Predict the `price` of a residential property (in US dollars, range $80,000--$2,000,000).

This is a **regression** problem.

**Why it matters:** More accurate pricing helps agents set competitive listing prices, helps buyers assess fair market value, and helps investors identify undervalued properties.

## Evaluation Criteria

**Primary metric:** Root Mean Squared Error (RMSE).

**Business justification:** RMSE penalizes large errors more heavily than Mean Absolute Error, which aligns with the business reality that a $100,000 pricing error is far more damaging than ten $10,000 errors. Large mispricings lead to failed transactions and lost client trust.

**Secondary considerations:**
- Mean Absolute Percentage Error (MAPE) to understand relative accuracy across different price ranges
- R-squared to measure overall explanatory power
- Performance stratified by price tier (are errors concentrated in luxury or budget segments?)

## Features

| Feature | Description |
|---------|-------------|
| `bedrooms` | Number of bedrooms (1-6) |
| `bathrooms` | Number of bathrooms (1-6) |
| `square_footage` | Total living area in square feet |
| `lot_size_acres` | Lot size in acres |
| `year_built` | Year the property was constructed |
| `garage_spaces` | Number of garage spaces (0-3) |
| `property_type` | Type of property (encoded 0-3: house, condo, townhouse, multi-family) |
| `neighborhood_quality` | Neighborhood quality rating (1-5, higher is better) |
| `school_rating` | Average rating of nearby schools (1-10) |
| `crime_rate_index` | Local crime rate index (0-10, higher means more crime) |
| `distance_to_downtown_miles` | Distance to the nearest downtown center in miles |
| `has_pool` | Whether the property has a swimming pool (0 or 1) |
| `has_renovation` | Whether the property has been recently renovated (0 or 1) |
| `tax_assessed_value` | Tax assessor's appraised value (often lower than market price) |
| `days_on_market` | Number of days the listing has been active |

## Text Field

`listing_description` --- The marketing description written by the listing agent (50-120 words). This text reflects the agent's professional positioning of the property. Luxury properties feature language like "stunning," "gourmet kitchen," "marble countertops," and "panoramic views." Mid-range properties are described as "spacious," "well-maintained," and "family-friendly." Budget properties use terms like "potential," "as-is," "handyman special," and "investor opportunity." The text encodes soft information about property condition and market positioning that is not captured by the structured features.

## Special Considerations and Challenges

1. **Text is an agent's subjective signal:** The listing description is not an objective property assessment --- it is marketing copy. Agents may use aspirational language to justify higher prices or deliberately understated language to generate bidding wars. The model must learn to use text as a noisy signal rather than ground truth.

2. **Non-linear price drivers:** The relationship between features and price is highly non-linear. A pool adds significant value to a luxury home but negligible value to a budget home. Square footage has diminishing returns at very high levels. Models must capture these interactions.

3. **Holdout drift:** The holdout set simulates a market shift where properties take longer to sell (inflated days_on_market), crime rates have increased, and properties are farther from downtown. This reflects HomeWise expanding into suburban or exurban markets with different characteristics than the training data.

4. **Text-structured redundancy:** Some listing text repeats information in the structured features ("4 bedrooms, 3 bathrooms"). The model must extract incremental signal from text beyond what structured features already provide.

5. **Log-transformed target:** The price distribution is right-skewed. Students should consider whether transforming the target (e.g., log price) improves model performance.

## Error Impact

| Error Type | Business Impact |
|-----------|-----------------|
| Overpricing by >15% | Property sits on market for months; seller loses confidence in the agent; eventual sale price drops below fair market value. Average cost: $15,000-$30,000 in lost value. |
| Overpricing by 5-15% | Property takes 2-4 weeks longer to sell; minor impact on final sale price. Moderate inconvenience. |
| Accurate within 5% | Ideal outcome. Property sells within expected timeframe at a competitive price. |
| Underpricing by 5-15% | Seller may leave money on the table; potential for bidding wars that partially compensate. Seller may be unhappy with agent. |
| Underpricing by >15% | Seller significantly undervalues property; agent faces potential legal liability for negligent pricing advice. Average cost: $20,000-$50,000 in lost seller equity. |

---

*Dataset contains 15 structured features plus 1 text column across train.csv (~2,000 rows), test.csv (~700 rows), and holdout.csv (~700 rows).*
