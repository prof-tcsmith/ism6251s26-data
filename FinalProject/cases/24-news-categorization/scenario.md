# Scenario 24: News Article Topic Classification

## Business Context

InfoPulse Media is a digital news aggregation platform that curates content from over 500 sources — wire services, major newspapers, blogs, trade magazines, and broadcast networks — delivering personalized news feeds to 12 million monthly active users. The platform's core value proposition is intelligent categorization: users subscribe to topic channels (Politics, Business, Technology, Sports, Health, Science, Entertainment, World) and expect a clean, well-organized feed with minimal cross-contamination between categories.

Currently, InfoPulse relies on a combination of source-level metadata (e.g., articles from ESPN default to Sports) and manual editor tagging for articles from general sources. This approach breaks down frequently: a wire service article about a tech company's earnings could be Business or Technology; a story about health policy legislation crosses Health and Politics; an international sports event might belong in both Sports and World. Editors spend an average of 3 hours per day reclassifying mistagged articles, and user complaints about "articles in the wrong channel" are the second most common support ticket after login issues.

The Head of Product has authorized the development of a machine learning classifier that analyzes the article text alongside metadata features (word count, source type, publication timing, engagement metrics) to predict the correct topic category. The classifier would run in near-real-time as articles are ingested, assigning a primary category and a confidence score. Articles with low confidence would be flagged for human review rather than auto-categorized.

Key stakeholders include the Head of Product (owns user engagement metrics), the Editorial team (wants to reduce manual categorization burden), the Advertising team (topic accuracy affects ad targeting revenue — showing a sports ad on a politics article wastes impressions), and the User Experience team (monitors channel quality and user satisfaction).

## The Problem

Predict the topic category (one of 8 classes: Politics, Business, Technology, Sports, Health, Science, Entertainment, World) for a news article based on its text and metadata features. This is a **multi-class classification** problem with 8 roughly balanced classes.

## Evaluation Criteria

The primary metric is **macro F1 score**, which treats all 8 categories equally regardless of slight class size differences. This is appropriate because InfoPulse values consistent quality across all topic channels — not just accuracy on the most common categories.

Additional considerations:
- **Per-class F1 scores:** Some categories are inherently easier to classify (Sports has distinctive vocabulary) while others overlap substantially (Politics/World, Business/Technology). Per-class metrics reveal where the model struggles.
- **Confusion matrix analysis:** Understanding *which* categories are confused with which is more valuable than aggregate accuracy. Business-Technology confusion is expected and somewhat tolerable (similar audience); Health-Entertainment confusion would indicate a fundamental model failure.
- **Confidence calibration:** In production, InfoPulse would use the model's probability estimates to decide which articles to auto-categorize vs. flag for review. Well-calibrated probabilities are valuable.

## Data Description

| Feature | Type | Description |
|---------|------|-------------|
| `article_text` | text | First 100-200 words of the news article |
| `word_count` | int | Total word count of the full article |
| `num_named_entities` | int | Number of named entities detected in the article |
| `avg_sentence_length` | float | Average sentence length in words |
| `num_quotes` | int | Number of direct quotes in the article |
| `has_numbers` | binary | Whether the article contains numeric data (0/1) |
| `publish_hour` | int (0-23) | Hour of publication |
| `source_type` | int (0-4) | 0=Wire, 1=Newspaper, 2=Blog, 3=Magazine, 4=Broadcast |
| `author_article_count` | int | Number of articles previously published by this author |
| `article_shares` | int | Number of social media shares within first 24 hours |
| `reading_time_minutes` | float | Estimated reading time |
| `sentiment_score` | float (-1 to 1) | Article sentiment: -1=very negative, 0=neutral, 1=very positive |
| `num_images` | int | Number of images in the article |
| **`category`** | **categorical** | **Target: topic category (8 classes)** |

## Text Field Details

The `article_text` column contains the first 100-200 words of each news article. Each category has a characteristic vocabulary:

- **Politics:** government, president, congress, legislation, senator, vote, policy, election, partisan, administration
- **Business:** market, stock, revenue, CEO, quarterly, profit, merger, acquisition, investors, economy
- **Technology:** app, software, AI, startup, data, digital, platform, cloud, release, smartphone
- **Sports:** game, team, season, score, championship, player, coach, tournament, victory, league
- **Health:** patients, treatment, study, disease, clinical, vaccine, hospital, symptoms, medical, therapy
- **Science:** research, discovery, NASA, species, experiment, molecule, climate, universe, genome, quantum
- **Entertainment:** movie, actor, album, concert, streaming, award, show, celebrity, series, premiere
- **World:** international, UN, diplomat, foreign, treaty, conflict, refugees, sanctions, summit, humanitarian

Approximately 8% of articles contain vocabulary from multiple categories, reflecting genuinely cross-topic stories (e.g., a tech company earnings report uses both Business and Technology vocabulary). These ambiguous articles are where structured features — particularly `source_type`, `has_numbers`, `num_quotes`, and `sentiment_score` — provide the most additional value.

## Special Considerations

- **Roughly balanced classes:** Unlike many classification problems, this one has roughly equal class sizes (~12-13% each). Standard accuracy is more meaningful here, though macro F1 remains the primary metric.
- **High-dimensional text with clear clusters:** News text has strong category-specific vocabulary, making TF-IDF features highly informative. However, the ambiguous cross-topic articles prevent any model from reaching perfect accuracy.
- **Structured features add modest but real value:** Features like `num_quotes` (higher in Politics and Sports), `has_numbers` (higher in Business and Sports), `sentiment_score` (more positive in Entertainment and Sports), and `source_type` (wire services for World, blogs for Technology) provide complementary signal. The ablation study should show measurable improvement when combining text and structured features.
- **Natural confusion pairs:** Expect higher confusion between Politics/World, Business/Technology, and Health/Science. These pairs share vocabulary and conceptual overlap. A model that confuses these pairs is making reasonable errors; a model that confuses Sports with Science is making unreasonable errors.
- **Holdout drift:** The holdout period reflects a more viral content environment (higher share counts), slightly more negative overall sentiment, and later publication times — simulating a shift in the news cycle.

## Cost/Impact Table

| Misclassification | Impact on InfoPulse | Severity |
|-------------------|-------------------|----------|
| Politics to World (or vice versa) | Related audiences, moderate overlap; some users subscribe to both | Low |
| Business to Technology (or vice versa) | Related audiences; ad targeting slightly off but not irrelevant | Low |
| Health to Science (or vice versa) | Related audiences; minor user friction | Low |
| Sports to any non-Sports | Sports fans notice immediately; highest engagement category has the least tolerance for noise | High |
| Entertainment to Politics (or vice versa) | Completely wrong audience; user frustration and potential advertiser complaints | High |
| Any to Science (false positive) | Science channel has the most discerning users; off-topic articles generate complaints | Medium |
| Consistent miscategorization of a source | Systematic errors affect user trust in the entire channel | High |
| Low-confidence correct classification | Auto-categorized correctly but could have been sent for human review unnecessarily | Low |
