# Scenario 30: Movie Revenue Prediction

## Company Background

**BoxOffice Intelligence** is an entertainment analytics firm based in Los Angeles, California, serving major film studios, independent distributors, and theater chains. The company provides pre-release revenue forecasts, marketing optimization recommendations, and release-date strategy analysis. BoxOffice Intelligence tracks over 800 film releases per year across domestic and international markets and maintains a proprietary database of production metadata, marketing spend, and box office results spanning twenty years.

## Business Problem

Film distribution is a high-stakes business where the difference between a profitable release and a financial disaster often hinges on decisions made months before opening weekend: how many theaters to book, how much to spend on marketing, and when to release. These decisions require accurate revenue forecasts, but traditional approaches based on genre, budget, and star power leave significant prediction error.

BoxOffice Intelligence has identified that plot synopses --- short descriptions of a film's story --- carry predictive signal beyond what production metadata alone provides. High-grossing films tend to have synopses featuring epic, globe-spanning narratives with clear stakes and spectacle. Mid-grossing films describe engaging, character-driven stories with broad appeal. Low-grossing films often have introspective, experimental, or niche narratives. Importantly, when budget and plot tone conflict (e.g., a high-budget film with an introspective, art-house synopsis), revenue tends to be lower than the budget alone would predict.

BoxOffice Intelligence wants to build a model that combines structured production data (budget, marketing spend, theater count, genre, director and actor track records) with the text of plot synopses to predict worldwide opening-month gross revenue. The model should capture the interaction between production scale (structured) and audience appeal as signaled by the story description (text).

## Prediction Problem

Predict `worldwide_gross_millions` --- the worldwide gross revenue of a film in its opening month, in millions of US dollars (range approximately $0.5M-$500M, log-distributed).

This is a **regression** problem.

**Why it matters:** Accurate revenue forecasts enable studios to optimize marketing spend (don't overspend on a film that will underperform), theater chains to allocate screens (book more screens for likely hits), and distributors to negotiate better deals for international rights.

## Evaluation Criteria

**Primary metric:** Root Mean Squared Log Error (RMSLE).

**Business justification:** Revenue is log-distributed, spanning from under $1M to over $300M. RMSLE treats a 50% error on a $10M film and a 50% error on a $200M film equally, which aligns with the business reality that relative accuracy matters more than absolute dollar accuracy. A $50M error on a $200M blockbuster (25% off) is more acceptable than a $50M error on a $60M mid-range film (83% off).

**Secondary considerations:**
- RMSE in raw dollars (to understand absolute error magnitude)
- Performance stratified by budget tier (are errors concentrated in big-budget or small-budget films?)
- Performance stratified by genre (are certain genres harder to predict?)

## Features

| Feature | Description |
|---------|-------------|
| `budget_millions` | Production budget in millions of US dollars |
| `runtime_minutes` | Runtime of the film in minutes |
| `genre_primary` | Primary genre (encoded 0-7: action, comedy, drama, horror, sci-fi, animation, thriller, romance) |
| `sequel_number` | Sequel indicator (0 = original, 1 = first sequel, 2 = second sequel or beyond) |
| `director_avg_gross` | Director's average worldwide gross across prior films (millions) |
| `lead_actor_avg_gross` | Lead actor's average worldwide gross across prior films (millions) |
| `studio_tier` | Studio size and resources (encoded 0-2: major studio, mid-tier, independent) |
| `release_month` | Month of theatrical release (1-12) |
| `is_holiday_release` | Whether the film opens during a peak period: June, July, November, or December (0 or 1) |
| `mpaa_rating` | MPAA rating (encoded 0-3: G, PG, PG-13, R) |
| `num_theaters_opening` | Number of theaters showing the film on opening weekend |
| `marketing_spend_millions` | Pre-release marketing expenditure in millions of dollars |
| `critic_score_pre_release` | Aggregate critic score from pre-release screenings (5-100 scale) |
| `social_media_buzz_index` | Proprietary index measuring pre-release social media conversation volume |

## Text Field

`plot_summary` --- A synopsis of the film's plot (60-130 words). High-grossing films feature synopses with epic scope, high stakes, spectacle, and genre-specific action vocabulary. Mid-grossing films have engaging, accessible plots with themes of family, friendship, and personal growth. Low-grossing films feature introspective, experimental, or avant-garde narratives with understated, contemplative tone. Genre-specific vocabulary (e.g., horror films reference haunting and supernatural elements, sci-fi films reference space and technology) correlates with the `genre_primary` feature but adds granularity. Sequels include franchise-continuation language.

## Special Considerations and Challenges

1. **Budget and marketing dominate but text adds signal:** The structured features `budget_millions`, `marketing_spend_millions`, and `num_theaters_opening` are the strongest individual predictors. However, the plot synopsis provides incremental signal, especially when production scale and story tone conflict. A big-budget film with an intimate, contemplative synopsis tends to underperform its budget-based prediction.

2. **Log-distributed target:** Revenue spans three orders of magnitude. Students should consider log-transforming the target variable before fitting regression models. The raw distribution is heavily right-skewed.

3. **Genre-text interaction:** Genre is encoded as a structured feature, but the plot text also contains genre-specific vocabulary. The model must extract signal from text that goes beyond what genre alone provides --- for example, distinguishing between a formulaic action film and a creative, audience-pleasing action film based on the synopsis language.

4. **Sequel effect:** Sequels have a built-in audience but also carry franchise fatigue risk. The interaction between sequel status and other features (budget, social media buzz, critic score) is complex and non-linear.

5. **Evaluation drift:** The test set simulates a shift in the industry environment: lower budgets (economic downturn), fewer opening theaters (streaming competition reducing theatrical windows), and inflated social media buzz (viral marketing becoming more common but less correlated with actual audience intent). This means the model must cope with budget-revenue and buzz-revenue relationships that have shifted.

6. **Critic score paradox:** Pre-release critic scores are informative but imperfect. Some critically panned films (low score) become box-office hits due to spectacle and marketing, while some critically acclaimed films (high score) fail commercially due to niche appeal. The model should not over-rely on this feature.

## Error Impact

| Error Type | Business Impact |
|-----------|-----------------|
| Overestimate by >50% | Studio overcommits to marketing spend and wide theatrical release; when revenue disappoints, the film becomes a financial loss. Theater chains that booked extra screens lose revenue opportunity from alternative films. Estimated cost: $10M-$30M for a mid-budget film. |
| Overestimate by 20-50% | Marketing spend is slightly misallocated; opening weekend disappoints but the film may recover over time. Moderate reputational impact. |
| Accurate within 20% | Ideal outcome. Marketing and distribution plans match actual demand. |
| Underestimate by 20-50% | Studio under-invests in marketing; film opens in too few theaters. Revenue is left on the table due to insufficient screen availability. Estimated missed revenue: 5-15% of potential gross. |
| Underestimate by >50% | Studio treats a potential hit as a mid-tier release. Severely constrained marketing and theater allocation means the film cannot reach its natural audience. Missed revenue: $20M-$100M for a would-be blockbuster. |

---

*Dataset contains 14 structured features plus 1 text column across train.csv (~2,000 rows), test.csv (~700 rows), and test.csv (~700 rows).*
